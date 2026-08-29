#!/usr/bin/env python3
"""Validate Starlight Character Studio contracts, jobs, receipts, and asset programs.

The JSON Schemas provide the portable contract. This validator adds repository
truth checks that a schema cannot express: referenced files must exist, agent
IDs must agree with canonical cards, generated artifacts must match their
receipt, and a comparison batch must hold its controlled variables constant.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Sequence

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas" / "character-studio"
SCHEMAS = {
    "starlight.character_visual_contract.v1": "character-visual-contract.schema.json",
    "starlight.character_image_job.v1": "image-job.schema.json",
    "starlight.character_selection_receipt.v1": "selection-receipt.schema.json",
    "starlight.character_asset_program.v1": "asset-program.schema.json",
}


@dataclass(frozen=True)
class ValidationIssue:
    source: str
    message: str

    def __str__(self) -> str:
        return f"{self.source}: {self.message}"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("document root must be an object")
    return value


def _json_path(parts: Iterable[Any]) -> str:
    rendered = "$"
    for part in parts:
        rendered += f"[{part}]" if isinstance(part, int) else f".{part}"
    return rendered


def validate_document(
    document: dict[str, Any],
    *,
    source: str = "<memory>",
) -> list[ValidationIssue]:
    """Validate one in-memory document against its declared schema."""

    version = document.get("schema_version")
    schema_name = SCHEMAS.get(version)
    if schema_name is None:
        return [ValidationIssue(source, f"unsupported schema_version {version!r}")]

    schema = load_json(SCHEMA_DIR / schema_name)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        ValidationIssue(source, f"{_json_path(error.absolute_path)}: {error.message}")
        for error in sorted(validator.iter_errors(document), key=lambda item: list(item.absolute_path))
    ]


def resolve_repo_path(value: str) -> Path | None:
    """Resolve a slash-delimited repo path without allowing path escape."""

    if not isinstance(value, str) or not value or "\\" in value:
        return None
    candidate_path = PurePosixPath(value)
    if candidate_path.is_absolute() or ".." in candidate_path.parts:
        return None
    candidate = (ROOT / Path(*candidate_path.parts)).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        return None
    return candidate


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        from PIL import Image
    except ImportError:
        return None
    try:
        with Image.open(path) as image:
            return image.size
    except (OSError, ValueError):
        return None


def _require_existing_repo_path(
    value: Any,
    *,
    source: str,
    field: str,
    issues: list[ValidationIssue],
) -> Path | None:
    resolved = resolve_repo_path(value) if isinstance(value, str) else None
    if resolved is None:
        issues.append(ValidationIssue(source, f"{field} is not a safe repo-relative path"))
        return None
    if not resolved.is_file():
        issues.append(ValidationIssue(source, f"{field} does not exist: {value}"))
        return None
    return resolved


def validate_contract(document: dict[str, Any], *, source: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    authority = document.get("authority", {})
    if authority.get("visual_identity_only") is not True or authority.get("grants_runtime_authority") is not False:
        issues.append(ValidationIssue(source, "visual contracts must be identity-only and grant no runtime authority"))

    provenance = document.get("provenance", {})
    source_card = _require_existing_repo_path(
        provenance.get("source_card"), source=source, field="provenance.source_card", issues=issues
    )
    if source_card is not None:
        try:
            card = load_json(source_card)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            issues.append(ValidationIssue(source, f"source card cannot be read: {exc}"))
        else:
            if card.get("id") != document.get("agent_id"):
                issues.append(
                    ValidationIssue(
                        source,
                        f"agent_id {document.get('agent_id')!r} does not match source card id {card.get('id')!r}",
                    )
                )

    for index, reference in enumerate(document.get("references", [])):
        _require_existing_repo_path(
            reference.get("path"),
            source=source,
            field=f"references[{index}].path",
            issues=issues,
        )
        if reference.get("rights_status") == "blocked":
            issues.append(ValidationIssue(source, f"references[{index}] has blocked rights status"))

    for index, output in enumerate(document.get("outputs", [])):
        ratio_text = output.get("aspect_ratio", "")
        try:
            ratio_width, ratio_height = (int(value) for value in ratio_text.split(":"))
            actual = output["target_width"] / output["target_height"]
            expected = ratio_width / ratio_height
        except (KeyError, TypeError, ValueError, ZeroDivisionError):
            continue
        if abs(actual - expected) > 0.01:
            issues.append(
                ValidationIssue(source, f"outputs[{index}] dimensions do not match aspect_ratio {ratio_text}")
            )
    return issues


def validate_image_job(document: dict[str, Any], *, source: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    contract_path = _require_existing_repo_path(
        document.get("contract_ref"), source=source, field="contract_ref", issues=issues
    )
    if contract_path is not None:
        try:
            contract = load_json(contract_path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            issues.append(ValidationIssue(source, f"contract_ref cannot be read: {exc}"))
        else:
            if contract.get("agent_id") != document.get("agent_id"):
                issues.append(ValidationIssue(source, "image job agent_id does not match its visual contract"))

    for index, reference in enumerate(document.get("references", [])):
        _require_existing_repo_path(
            reference.get("path"),
            source=source,
            field=f"references[{index}].path",
            issues=issues,
        )
        if reference.get("rights_status") == "blocked":
            issues.append(ValidationIssue(source, f"references[{index}] has blocked rights status"))

    prompt = document.get("prompt", {})
    prompt_guards = " ".join(prompt.get("constraints", []) + prompt.get("avoid", [])).lower()
    if "text" not in prompt_guards or "logo" not in prompt_guards:
        issues.append(ValidationIssue(source, "prompt must explicitly prohibit generated text and logos"))

    output = document.get("output", {})
    output_path_value = output.get("path")
    output_path = resolve_repo_path(output_path_value) if isinstance(output_path_value, str) else None
    if output_path is None:
        issues.append(ValidationIssue(source, "output.path is not a safe repo-relative path"))
    elif output.get("status") in {"generated", "selected"}:
        if not output_path.is_file():
            issues.append(ValidationIssue(source, f"generated output does not exist: {output_path_value}"))
        else:
            expected_hash = output.get("sha256")
            actual_hash = file_sha256(output_path)
            if expected_hash != actual_hash:
                issues.append(ValidationIssue(source, "generated output SHA-256 does not match its receipt"))
            expected_dimensions = output.get("dimensions")
            actual_dimensions = image_dimensions(output_path)
            if actual_dimensions is not None and expected_dimensions != {
                "width": actual_dimensions[0],
                "height": actual_dimensions[1],
            }:
                issues.append(ValidationIssue(source, "generated output dimensions do not match its receipt"))

    if output.get("status") == "selected" and document.get("qa", {}).get("human_decision") != "approve":
        issues.append(ValidationIssue(source, "selected output requires an explicit human approval"))
    return issues


def validate_selection_receipt(document: dict[str, Any], *, source: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    agent_id = document.get("agent_id")
    for index, candidate in enumerate(document.get("candidates", [])):
        job_path = _require_existing_repo_path(
            candidate.get("job_ref"),
            source=source,
            field=f"candidates[{index}].job_ref",
            issues=issues,
        )
        if job_path is not None:
            try:
                job = load_json(job_path)
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                issues.append(ValidationIssue(source, f"candidate job cannot be read: {exc}"))
            else:
                if job.get("agent_id") != agent_id:
                    issues.append(ValidationIssue(source, f"candidates[{index}] belongs to a different agent"))
                if job.get("direction", {}).get("territory_id") != candidate.get("territory_id"):
                    issues.append(ValidationIssue(source, f"candidates[{index}] territory does not match its job"))

        if candidate.get("inspected"):
            artifact_path = _require_existing_repo_path(
                candidate.get("artifact_path"),
                source=source,
                field=f"candidates[{index}].artifact_path",
                issues=issues,
            )
            if artifact_path is not None and candidate.get("sha256") != file_sha256(artifact_path):
                issues.append(ValidationIssue(source, f"candidates[{index}] SHA-256 does not match artifact"))

    selected_job = document.get("selected_job")
    if selected_job is not None and not any(
        candidate.get("job_ref") == selected_job for candidate in document.get("candidates", [])
    ):
        issues.append(ValidationIssue(source, "selected_job must identify one of the candidate jobs"))
    return issues


def validate_asset_program(document: dict[str, Any], *, source: str) -> list[ValidationIssue]:
    """Validate scale arithmetic, human gates, evidence, and unique design IDs."""

    issues: list[ValidationIssue] = []
    authority = document.get("authority", {})
    if authority.get("visual_research_only") is not True or authority.get("grants_runtime_authority") is not False:
        issues.append(ValidationIssue(source, "asset programs must be visual research only and grant no runtime authority"))

    scale = document.get("scale_model", {})
    agent_count = scale.get("portfolio_agent_count")
    masters_per_agent = scale.get("master_assets_per_agent")
    derivatives_per_master = scale.get("derivatives_per_master")
    generated_masters = scale.get("generated_master_count")
    deterministic_derivatives = scale.get("deterministic_derivative_count")
    target_deliverables = scale.get("target_deliverable_count")
    if all(isinstance(value, int) for value in (agent_count, masters_per_agent, generated_masters)):
        expected_masters = agent_count * masters_per_agent
        if generated_masters != expected_masters:
            issues.append(
                ValidationIssue(
                    source,
                    f"generated_master_count must equal portfolio_agent_count x master_assets_per_agent ({expected_masters})",
                )
            )
    if all(isinstance(value, int) for value in (generated_masters, derivatives_per_master, deterministic_derivatives)):
        expected_derivatives = generated_masters * derivatives_per_master
        if deterministic_derivatives != expected_derivatives:
            issues.append(
                ValidationIssue(
                    source,
                    f"deterministic_derivative_count must equal generated_master_count x derivatives_per_master ({expected_derivatives})",
                )
            )
    if all(isinstance(value, int) for value in (generated_masters, deterministic_derivatives, target_deliverables)):
        expected_total = generated_masters + deterministic_derivatives
        if target_deliverables != expected_total:
            issues.append(
                ValidationIssue(
                    source,
                    f"target_deliverable_count must equal masters plus deterministic derivatives ({expected_total})",
                )
            )

    collections = {
        "style_territories": "id",
        "face_systems": "id",
        "surface_profiles": "id",
        "batches": "batch_id",
    }
    for collection_name, identifier_key in collections.items():
        identifiers = [
            item.get(identifier_key)
            for item in document.get(collection_name, [])
            if isinstance(item.get(identifier_key), str)
        ]
        duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
        if duplicates:
            issues.append(
                ValidationIssue(source, f"{collection_name} contains duplicate identifiers: {', '.join(duplicates)}")
            )

    territory_ids = {item.get("id") for item in document.get("style_territories", [])}
    identity_policy = document.get("identity_policy", {})
    for field in ("default_territory", "continuity_lane"):
        if identity_policy.get(field) not in territory_ids:
            issues.append(ValidationIssue(source, f"identity_policy.{field} must identify a declared style territory"))

    for index, profile in enumerate(document.get("surface_profiles", [])):
        ratio_text = profile.get("aspect_ratio", "")
        try:
            ratio_width, ratio_height = (int(value) for value in ratio_text.split(":"))
            actual = profile["target_width"] / profile["target_height"]
            expected = ratio_width / ratio_height
        except (KeyError, TypeError, ValueError, ZeroDivisionError):
            continue
        if abs(actual - expected) > 0.01:
            issues.append(
                ValidationIssue(
                    source,
                    f"surface_profiles[{index}] dimensions do not match aspect_ratio {ratio_text}",
                )
            )

    evidence = document.get("evidence", {})
    _require_existing_repo_path(
        evidence.get("founder_feedback_path"),
        source=source,
        field="evidence.founder_feedback_path",
        issues=issues,
    )
    for index, value in enumerate(evidence.get("rejected_research_paths", [])):
        _require_existing_repo_path(
            value,
            source=source,
            field=f"evidence.rejected_research_paths[{index}]",
            issues=issues,
        )

    generation_policy = document.get("generation_policy", {})
    if generation_policy.get("machine_admission") == "held":
        active_batches = [
            batch.get("batch_id")
            for batch in document.get("batches", [])
            if batch.get("status") in {"generating", "review", "approved", "complete"}
        ]
        if active_batches:
            issues.append(
                ValidationIssue(
                    source,
                    f"held machine admission cannot contain active or completed batches: {', '.join(active_batches)}",
                )
            )
    if document.get("status") == "held" and authority.get("production_mutation_allowed") is not False:
        issues.append(ValidationIssue(source, "a held asset program cannot allow production mutation"))
    return issues


def validate_direction_batch(
    jobs: Sequence[dict[str, Any]],
    *,
    source: str = "<batch>",
) -> list[ValidationIssue]:
    """Check that a comparison changes hypotheses, not the baseline."""

    if len(jobs) < 2:
        return []
    issues: list[ValidationIssue] = []
    baseline = tuple(jobs[0].get("direction", {}).get("controlled_variables", []))
    territories: set[str] = set()
    for job in jobs:
        direction = job.get("direction", {})
        territory = direction.get("territory_id")
        if tuple(direction.get("controlled_variables", [])) != baseline:
            issues.append(ValidationIssue(source, f"{job.get('job_id')} changes the controlled-variable baseline"))
        if territory in territories:
            issues.append(ValidationIssue(source, f"duplicate direction territory: {territory}"))
        territories.add(territory)
    return issues


def discover_documents() -> list[Path]:
    template_root = ROOT / "templates" / "starlight-character-studio"
    preview_root = ROOT / "assets" / "starlight-constellation" / "v2-preview"
    paths = list(template_root.rglob("*.json")) if template_root.exists() else []
    if preview_root.exists():
        paths.extend(
            path
            for path in preview_root.rglob("*.json")
            if path.parent.name == "prompts"
            or path.name.startswith("selection-receipt")
            or path.name.startswith("asset-program")
            or "visual-contract" in path.name
        )
    return sorted(set(paths))


def validate_repository(paths: Sequence[Path] | None = None) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    documents: list[tuple[Path, dict[str, Any]]] = []
    for path in paths or discover_documents():
        relative = path.resolve().relative_to(ROOT.resolve()).as_posix()
        try:
            document = load_json(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            issues.append(ValidationIssue(relative, f"invalid JSON object: {exc}"))
            continue
        documents.append((path, document))
        issues.extend(validate_document(document, source=relative))
        version = document.get("schema_version")
        if version == "starlight.character_visual_contract.v1":
            issues.extend(validate_contract(document, source=relative))
        elif version == "starlight.character_image_job.v1":
            issues.extend(validate_image_job(document, source=relative))
        elif version == "starlight.character_selection_receipt.v1":
            issues.extend(validate_selection_receipt(document, source=relative))
        elif version == "starlight.character_asset_program.v1":
            issues.extend(validate_asset_program(document, source=relative))

    batches: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for path, document in documents:
        if document.get("schema_version") != "starlight.character_image_job.v1":
            continue
        if "assets/starlight-constellation/v2-preview" not in path.as_posix():
            continue
        key = (document.get("agent_id", ""), path.parent.as_posix())
        batches.setdefault(key, []).append(document)
    for (agent_id, _), jobs in batches.items():
        issues.extend(validate_direction_batch(jobs, source=f"direction-batch:{agent_id}"))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="Optional JSON documents to validate")
    args = parser.parse_args()
    paths = [path if path.is_absolute() else ROOT / path for path in args.paths]
    issues = validate_repository(paths or None)
    if issues:
        print(f"Character Studio validation FAILED ({len(issues)} issue(s))")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print(f"Character Studio validation PASS ({len(paths) or len(discover_documents())} document(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
