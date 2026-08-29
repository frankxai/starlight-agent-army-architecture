#!/usr/bin/env python3
"""Validate the canonical 10-swarm/50-agent source and compiled projections.

This is structural validation only. It never runs a model and never reports a
live pass rate, production admission, deployment, or runtime activation.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from generate_canonical_portfolio import (
    CARD_DIR,
    EVAL_DIR,
    EXPECTED_SWARMS,
    MANIFEST_PATH,
    PROMPT_DIR,
    ROOT,
    SOURCE_PATH,
    build_outputs,
    check_outputs,
    digest_object,
    load_json,
    validate_catalog,
)

AGENT_SCHEMA_PATH = ROOT / "schemas" / "agent-card" / "agent-card.schema.json"


def _validate_native_card(card: dict[str, Any], path: Path) -> list[str]:
    errors: list[str] = []
    schema = load_json(AGENT_SCHEMA_PATH)
    try:
        import jsonschema  # type: ignore

        validator = jsonschema.Draft202012Validator(schema)
        errors.extend(
            f"agent-card schema: {issue.message}"
            for issue in sorted(validator.iter_errors(card), key=lambda e: list(e.path))
        )
    except ImportError:
        from validate_agent_cards import basic_validate

        errors.extend(basic_validate(card, schema))

    metadata = (card.get("metadata") or {}).get("canonical_portfolio") or {}
    required_metadata = {
        "portfolio_id",
        "portfolio_version",
        "agent_version",
        "catalog_ref",
        "catalog_digest",
        "swarm",
        "role_lineage",
        "purpose",
        "outcomes",
        "public_profile",
        "prompt_contract",
        "capability_boundary",
        "stop_conditions",
        "escalation_conditions",
        "graph",
        "visual_dna",
        "capability_pack",
        "eval_evidence",
    }
    missing = sorted(required_metadata - set(metadata))
    errors.extend(f"canonical metadata missing {key}" for key in missing)
    if missing:
        return errors

    if card.get("status") != "draft":
        errors.append("canonical card must remain draft while live eval is not_run")
    if (card.get("mind") or {}).get("memory_scope") not in {"none", "session", "user", "org"}:
        errors.append("canonical card must use public-safe memory scope")
    if (card.get("mind") or {}).get("private_kb"):
        errors.append("canonical card must not contain private_kb references")
    surfaces = set((card.get("body") or {}).get("surfaces") or [])
    if surfaces != {"web", "coe_demo"}:
        errors.append(f"canonical card has unexpected surfaces: {sorted(surfaces)}")

    lineage = metadata["role_lineage"]
    if lineage.get("role_kind") == "conductor":
        if card.get("tier") != "persona" or not card.get("host"):
            errors.append("conductor must compile to a persona host")
        if lineage.get("parent_agent_id") is not None:
            errors.append("conductor must not have a parent_agent_id")
    elif lineage.get("role_kind") == "specialist":
        if card.get("tier") != "specialist" or card.get("host"):
            errors.append("specialist must compile to a non-host specialist")
        if card.get("parent_host_id") != lineage.get("conductor_agent_id"):
            errors.append("specialist parent_host_id must match conductor lineage")
    else:
        errors.append("invalid role lineage kind")

    profile = metadata["public_profile"]
    if profile.get("safe_for_public") is not True:
        errors.append("public profile must explicitly be safe_for_public")
    prompt = metadata["prompt_contract"]
    if "lease" not in str(prompt.get("runtime_authority", "")).lower():
        errors.append("prompt contract must keep authority in runtime leases")
    boundary = metadata["capability_boundary"]
    if not boundary.get("capabilities") or not boundary.get("non_capabilities"):
        errors.append("capability boundary needs capabilities and non_capabilities")
    if "never prompt prose" not in str(boundary.get("runtime_enforcement", "")).lower():
        errors.append("capability boundary must deny prompt-prose authority")
    if not metadata.get("stop_conditions") or not metadata.get("escalation_conditions"):
        errors.append("stop and escalation conditions must be non-empty")
    graph = metadata["graph"]
    if not isinstance(graph.get("depends_on"), list) or not graph.get("routes_to"):
        errors.append("graph must contain dependency and routing arrays")

    visual = metadata["visual_dna"]
    swarm_id = (metadata.get("swarm") or {}).get("id")
    expected_asset = (
        f"assets/starlight-constellation/v1/agents/{swarm_id}/{card.get('id')}.webp"
    )
    expected_avatar = f"{card.get('id')}-v1"
    face = (card.get("identity") or {}).get("face") or {}
    if face.get("avatar_id") != expected_avatar:
        errors.append(f"avatar_id must be {expected_avatar}")
    if face.get("asset_refs") != [expected_asset]:
        errors.append(f"asset_refs must be [{expected_asset!r}]")
    if visual.get("visual_asset_id") != expected_avatar:
        errors.append("visual_dna.visual_asset_id must match avatar_id")
    if visual.get("asset_ref") != expected_asset:
        errors.append("visual_dna.asset_ref must match identity.face.asset_refs")
    for key in (
        "archetype",
        "signature",
        "silhouette",
        "accent",
        "portrait_brief",
        "palette",
        "materials",
        "lighting",
        "setting",
        "negative_cues",
    ):
        if not visual.get(key):
            errors.append(f"visual_dna missing {key}")

    pack = metadata["capability_pack"]
    if pack.get("immutable") is not True or pack.get("grants_authority") is not False:
        errors.append("capability pack binding must be immutable and non-authoritative")
    eval_evidence = metadata["eval_evidence"]
    if eval_evidence.get("mode") != "structural_only":
        errors.append("eval evidence mode must be structural_only")
    if eval_evidence.get("live_eval_status") != "not_run":
        errors.append("live eval status must be not_run")

    prompt_path = ROOT / prompt.get("source", "")
    if not prompt_path.is_file():
        errors.append(f"prompt source missing: {prompt.get('source')}")
    else:
        prompt_text = prompt_path.read_text(encoding="utf-8")
        for required_text in (
            "## Authority boundary",
            "never tool grants",
            "## Stop conditions",
            "## Escalation conditions",
            "live evaluation not run",
        ):
            if required_text.lower() not in prompt_text.lower():
                errors.append(f"prompt source missing contract text: {required_text}")

    eval_ref = (card.get("evals") or {}).get("suite_id")
    if not isinstance(eval_ref, str) or not (ROOT / eval_ref).is_file():
        errors.append(f"eval suite missing: {eval_ref}")
    else:
        suite = load_json(ROOT / eval_ref)
        if suite.get("agent_id") != card.get("id"):
            errors.append("eval suite agent_id does not match card")
        if suite.get("evaluation_mode") != "structural_only":
            errors.append("eval suite must be labeled structural_only")
        if suite.get("live_eval_status") != "not_run":
            errors.append("eval suite live_eval_status must be not_run")
        cases = suite.get("cases") or []
        if len(cases) < 4:
            errors.append("eval suite needs common authority/privacy cases plus agent cases")
        case_ids = [case.get("id") for case in cases if isinstance(case, dict)]
        if len(case_ids) != len(set(case_ids)):
            errors.append("eval suite case ids must be unique")
        if "not a live model-graded result" not in str(suite.get("evidence_claim", "")):
            errors.append("eval suite must disclaim live model-graded evidence")

    return sorted(set(errors))


def _validate_pack(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    binding = manifest.get("capability_pack") or {}
    pack_path = ROOT / str(binding.get("path", ""))
    if not pack_path.is_file():
        return [f"capability pack missing: {binding.get('path')}"]
    pack = load_json(pack_path)
    if pack.get("immutable") is not True:
        errors.append("capability pack must be immutable")
    if pack.get("grants_authority") is not False:
        errors.append("capability pack must explicitly not grant authority")
    payload = pack.get("payload")
    actual_digest = f"sha256:{digest_object(payload)}"
    if pack.get("content_digest") != actual_digest:
        errors.append("capability pack payload digest mismatch")
    if binding.get("content_digest") != actual_digest:
        errors.append("portfolio manifest capability digest mismatch")
    if binding.get("pack_id") != pack.get("pack_id"):
        errors.append("portfolio manifest capability pack_id mismatch")
    if not str(pack_path.parent.name).startswith("sha256-"):
        errors.append("capability pack directory must be content addressed")
    elif pack_path.parent.name != f"sha256-{actual_digest.removeprefix('sha256:')}":
        errors.append("capability pack directory digest mismatch")
    members = (payload or {}).get("members") or []
    if len(members) != 50:
        errors.append(f"capability pack must contain exactly 50 members; found {len(members)}")
    member_ids = [member.get("agent_id") for member in members if isinstance(member, dict)]
    if len(member_ids) != len(set(member_ids)):
        errors.append("capability pack member ids must be unique")
    for member in members:
        if member.get("memory_scope") == "private_vault":
            errors.append(f"capability member {member.get('agent_id')} uses private_vault")
        if set(member.get("surfaces") or []).intersection({"hermes", "telegram", "cli"}):
            errors.append(f"capability member {member.get('agent_id')} exposes private surface")
    return sorted(set(errors))


def validate_current_tree() -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    catalog = load_json(SOURCE_PATH)
    errors.extend(validate_catalog(catalog))
    if errors:
        return errors, {"swarms": 0, "agents": 0, "cards": 0, "eval_cases": 0}

    outputs, expected_manifest = build_outputs(catalog)
    errors.extend(check_outputs(outputs))

    counts = {
        "swarms": len(catalog["swarms"]),
        "agents": sum(len(swarm["agents"]) for swarm in catalog["swarms"]),
        "cards": 0,
        "eval_cases": 0,
    }
    all_ids = {
        agent["id"] for swarm in catalog["swarms"] for agent in swarm["agents"]
    }
    if MANIFEST_PATH.is_file():
        manifest = load_json(MANIFEST_PATH)
        if manifest != expected_manifest:
            errors.append("compiled manifest does not match current catalog/compiler")
        if manifest.get("counts", {}).get("swarms") != 10:
            errors.append("compiled manifest must report exactly 10 swarms")
        if manifest.get("counts", {}).get("agents") != 50:
            errors.append("compiled manifest must report exactly 50 agents")
        evaluation = manifest.get("evaluation_evidence") or {}
        if evaluation.get("structural_only") is not True:
            errors.append("compiled manifest must label evidence structural_only")
        if evaluation.get("live_eval_status") != "not_run":
            errors.append("compiled manifest must label live_eval_status not_run")
        errors.extend(_validate_pack(manifest))

    cards = sorted(CARD_DIR.glob("*.json")) if CARD_DIR.exists() else []
    if len(cards) != 50:
        errors.append(f"cards/portfolio must contain exactly 50 cards; found {len(cards)}")
    if {path.stem for path in cards} != all_ids:
        errors.append("compiled card ids do not exactly match source catalog")
    for path in cards:
        try:
            card = load_json(path)
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT).as_posix()}: JSON parse error: {exc}")
            continue
        card_errors = _validate_native_card(card, path)
        errors.extend(
            f"{path.relative_to(ROOT).as_posix()}: {error}" for error in card_errors
        )
        counts["cards"] += 1

    prompts = sorted(PROMPT_DIR.glob("*.SYSTEM.md")) if PROMPT_DIR.exists() else []
    if len(prompts) != 50:
        errors.append(f"cards/portfolio/prompts must contain exactly 50 prompts; found {len(prompts)}")
    evals = sorted(EVAL_DIR.glob("*.json")) if EVAL_DIR.exists() else []
    if len(evals) != 50:
        errors.append(f"evals/portfolio must contain exactly 50 suites; found {len(evals)}")
    for path in evals:
        try:
            suite = load_json(path)
            counts["eval_cases"] += len(suite.get("cases") or [])
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT).as_posix()}: JSON parse error: {exc}")

    if set(EXPECTED_SWARMS) != {swarm["id"] for swarm in catalog["swarms"]}:
        errors.append("source domains drifted from the exact canonical ten")
    return sorted(set(errors)), counts


def main() -> int:
    try:
        errors, counts = validate_current_tree()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if errors:
        print("FAIL canonical portfolio structural validation")
        for error in errors:
            print(f"  - {error}")
        print("LIVE EVAL: NOT RUN")
        return 1
    print(
        "OK canonical portfolio: "
        f"{counts['swarms']} swarms x 5 = {counts['agents']} agents; "
        f"{counts['cards']} native cards; {counts['eval_cases']} structural eval cases"
    )
    print("OK graph, skill registry, public-safety, visual-DNA, prompt, pack, and drift gates")
    print("LIVE EVAL: NOT RUN — structural validation makes no model-quality claim")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
