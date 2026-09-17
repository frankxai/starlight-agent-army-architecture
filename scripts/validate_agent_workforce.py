#!/usr/bin/env python3
"""Validate the AI-agent workforce roster and its local SSOT references."""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

from validate_agent_governance import validate_access, validate_queen

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROSTER = ROOT / "configs" / "agent-workforce.example.json"
DEFAULT_SCHEMA = ROOT / "schemas" / "agent-workforce" / "agent-workforce.schema.json"

REQUIRED_PROHIBITIONS = {
    "promote",
    "restore_from_quarantine",
    "widen_tools",
    "widen_write_scope",
    "increase_budget",
    "deploy",
    "publish",
    "external_send",
    "retire_or_delete",
}
HIGH_RISK_GATES = {
    "publish",
    "external_send",
    "spend",
    "credentials",
    "destructive",
    "legal_ip",
    "promotion",
    "restore_from_quarantine",
    "retirement",
}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def resolve_repo_ref(root: Path, ref: str) -> Path:
    candidate = Path(ref)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"unsafe repository reference: {ref}")
    resolved_root = root.resolve()
    resolved = (resolved_root / candidate).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError(f"repository reference escapes root: {ref}") from exc
    return resolved


def validate_with_jsonschema(roster: dict[str, Any], schema_path: Path) -> list[str]:
    try:
        import jsonschema  # type: ignore
    except ImportError:
        return []
    schema = load_json(schema_path)
    validator = jsonschema.Draft202012Validator(schema)
    return [
        f"schema {'.'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(roster), key=lambda item: list(item.absolute_path))
    ]


def validate_roster(roster: dict[str, Any], root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    if roster.get("schema_version") != "agent-workforce.v1":
        errors.append("schema_version must be agent-workforce.v1")
    try:
        date.fromisoformat(str(roster.get("effective_date")))
    except ValueError:
        errors.append("effective_date must be YYYY-MM-DD")

    authority = roster.get("authority") or {}
    if authority.get("controller") != "starlight-queen":
        errors.append("authority.controller must be starlight-queen")
    if authority.get("review_mode") != "advisory":
        errors.append("authority.review_mode must be advisory")
    missing_prohibitions = REQUIRED_PROHIBITIONS - set(authority.get("prohibited_automations") or [])
    if missing_prohibitions:
        errors.append(f"authority missing prohibited automations: {sorted(missing_prohibitions)}")
    control_plane_ref = authority.get("control_plane_ref")
    try:
        control_plane_path = resolve_repo_ref(root, str(control_plane_ref))
    except ValueError as exc:
        errors.append(f"authority.control_plane_ref: {exc}")
    else:
        if not control_plane_path.is_file():
            errors.append(f"authority.control_plane_ref: missing file {control_plane_ref}")
        else:
            queen = load_json(control_plane_path)
            errors.extend(f"authority.control_plane_ref: {error}" for error in validate_queen(queen))

    policy = roster.get("review_policy") or {}
    cadence = policy.get("cadence_days")
    if policy.get("required_eval_mode") != "live":
        errors.append("review_policy.required_eval_mode must be live")
    if policy.get("required_security_verdict") != "PASS":
        errors.append("review_policy.required_security_verdict must be PASS")
    if not isinstance(cadence, int) or cadence < 1:
        errors.append("review_policy.cadence_days must be a positive integer")
    monthly_cadence = policy.get("monthly_cadence_days")
    if not isinstance(monthly_cadence, int) or not 28 <= monthly_cadence <= 31:
        errors.append("review_policy.monthly_cadence_days must be between 28 and 31")
    minimum_weekly = policy.get("min_weekly_reviews_per_month")
    if not isinstance(minimum_weekly, int) or minimum_weekly < 2:
        errors.append("review_policy.min_weekly_reviews_per_month must be at least 2")

    assignments = roster.get("assignments") or []
    if not assignments:
        errors.append("at least one assignment is required")
        return errors

    seen_assignments: set[str] = set()
    seen_agent_placements: set[tuple[str, str]] = set()
    for index, assignment in enumerate(assignments):
        prefix = f"assignments[{index}]"
        assignment_id = assignment.get("assignment_id")
        agent_id = assignment.get("agent_id")
        if assignment_id in seen_assignments:
            errors.append(f"{prefix}: duplicate assignment_id {assignment_id}")
        seen_assignments.add(assignment_id)

        deployment_ref = assignment.get("deployment_ref")
        placement = (str(agent_id), str(deployment_ref))
        if placement in seen_agent_placements:
            errors.append(f"{prefix}: duplicate agent/deployment placement {placement}")
        seen_agent_placements.add(placement)

        if assignment.get("supervisor") != "starlight-queen":
            errors.append(f"{prefix}: supervisor must be starlight-queen")
        runtime = assignment.get("runtime") or {}
        if runtime.get("controller") != "starlight-queen":
            errors.append(f"{prefix}: runtime.controller must be starlight-queen")
        if runtime.get("executor") in {"n8n", "openclaw", "openhands"}:
            errors.append(f"{prefix}: integration/gateway/specialist cannot be the workforce executor")
        if assignment.get("review", {}).get("cadence_days") != cadence:
            errors.append(f"{prefix}: assignment review cadence must match review_policy")

        gates = set(assignment.get("human_gates") or [])
        if assignment.get("risk_tier") in {"high", "critical"}:
            missing_gates = HIGH_RISK_GATES - gates
            if missing_gates:
                errors.append(f"{prefix}: high-risk assignment missing human gates {sorted(missing_gates)}")
            security = assignment.get("security") or {}
            required_states = set(security.get("required_before_status") or [])
            if not {"probation", "active"}.issubset(required_states):
                errors.append(f"{prefix}: security assessment must be required before probation and active")

        evidence = assignment.get("evidence") or {}
        if not str(evidence.get("private_sink", "")).startswith("private:"):
            errors.append(f"{prefix}: evidence.private_sink must use the private: locator")
        if evidence.get("raw_content_policy") != "prohibited":
            errors.append(f"{prefix}: raw content must be prohibited")

        refs = {
            "card_ref": assignment.get("card_ref"),
            "access_bundle_ref": assignment.get("access_bundle_ref"),
            "deployment_ref": deployment_ref,
            "eval_suite_ref": assignment.get("eval_suite_ref"),
        }
        loaded: dict[str, dict[str, Any]] = {}
        for key, ref in refs.items():
            try:
                path = resolve_repo_ref(root, str(ref))
            except ValueError as exc:
                errors.append(f"{prefix}.{key}: {exc}")
                continue
            if not path.is_file():
                errors.append(f"{prefix}.{key}: missing file {ref}")
                continue
            try:
                loaded[key] = load_json(path)
            except (ValueError, json.JSONDecodeError) as exc:
                errors.append(f"{prefix}.{key}: invalid JSON: {exc}")

        card = loaded.get("card_ref")
        access = loaded.get("access_bundle_ref")
        deployment = loaded.get("deployment_ref")
        suite = loaded.get("eval_suite_ref")
        if card and card.get("id") != agent_id:
            errors.append(f"{prefix}: card id does not match agent_id")
        if access:
            errors.extend(f"{prefix}.access_bundle_ref: {error}" for error in validate_access(access))
            if access.get("assignment_id") != assignment_id:
                errors.append(f"{prefix}: access bundle assignment_id does not match")
            if access.get("agent_id") != agent_id:
                errors.append(f"{prefix}: access bundle agent_id does not match")
        if deployment:
            if deployment.get("agent_id") != agent_id:
                errors.append(f"{prefix}: deployment agent_id does not match")
            if deployment.get("card_ref") != assignment.get("card_ref"):
                errors.append(f"{prefix}: deployment card_ref does not match assignment")
        if suite and suite.get("agent_id") != agent_id:
            errors.append(f"{prefix}: eval suite agent_id does not match")
        if card and card.get("evals", {}).get("suite_id") != assignment.get("eval_suite_ref"):
            errors.append(f"{prefix}: card eval suite does not match assignment")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--roster", type=Path, default=DEFAULT_ROSTER)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    args = parser.parse_args()

    roster = load_json(args.roster)
    errors = validate_with_jsonschema(roster, args.schema)
    errors.extend(validate_roster(roster))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {len(roster['assignments'])} workforce assignment(s) validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
