#!/usr/bin/env python3
"""Validate Queen, access-bundle, and bounded-swarm governance contracts."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUEEN = ROOT / "configs" / "starlight-queen-control-plane.example.json"
DEFAULT_ACCESS = ROOT / "configs" / "agent-access-bundle.example.json"
DEFAULT_MISSION = ROOT / "configs" / "swarm-mission.example.json"
DEFAULT_N8N_HANDOFF = ROOT / "configs" / "n8n-agent-estate-handoff.example.json"

SCHEMAS = {
    "queen": ROOT / "schemas" / "queen-control-plane" / "queen-control-plane.schema.json",
    "access": ROOT / "schemas" / "agent-access-bundle" / "agent-access-bundle.schema.json",
    "mission": ROOT / "schemas" / "swarm-mission" / "swarm-mission.schema.json",
    "n8n_handoff": ROOT / "schemas" / "n8n-agent-automation-handoff" / "n8n-agent-automation-handoff.schema.json",
}

N8N_EXECUTION_CHAIN = [
    "AuthenticatedIntake",
    "NormalizeValidate",
    "IdempotentLedgerUpsert",
    "PolicyRiskGate",
    "HumanApprovalResume",
    "DeterministicAction",
    "ReceiptMetrics",
    "ErrorDLQIncident",
]

CONSEQUENTIAL_GATES = {
    "publish",
    "external_send",
    "spend",
    "dns",
    "credentials",
    "destructive",
    "legal_ip",
    "brand_identity",
    "promotion",
    "restore_from_quarantine",
    "retirement",
}

SECRET_SHAPES = (
    re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"),
    re.compile(r"\b(?:sk|ghp|github_pat|xox[baprs])[-_][A-Za-z0-9_-]{12,}\b", re.IGNORECASE),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def resolve_repo_ref(ref: str, root: Path = ROOT) -> Path:
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


def schema_errors(document: dict[str, Any], schema_path: Path, label: str) -> list[str]:
    try:
        import jsonschema  # type: ignore
    except ImportError:
        return [f"{label}: jsonschema is required for closed-contract validation"]
    schema = load_json(schema_path)
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    return [
        f"{label} schema {'.'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(document), key=lambda item: list(item.absolute_path))
    ]


def serialized_secret_findings(document: dict[str, Any], label: str) -> list[str]:
    serialized = json.dumps(document, sort_keys=True)
    return [f"{label}: probable raw secret material matches a prohibited shape" for pattern in SECRET_SHAPES if pattern.search(serialized)]


def parse_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def validate_queen(document: dict[str, Any]) -> list[str]:
    errors = schema_errors(document, SCHEMAS["queen"], "queen")
    errors.extend(serialized_secret_findings(document, "queen"))
    constitution = document.get("constitution") or {}
    automatic = set(constitution.get("automatic_actions") or [])
    gated = set(constitution.get("human_gated_actions") or [])
    if automatic & gated:
        errors.append(f"queen: automatic and human-gated actions overlap: {sorted(automatic & gated)}")
    missing = CONSEQUENTIAL_GATES - gated
    if missing:
        errors.append(f"queen: missing consequential human gates: {sorted(missing)}")
    plane_ids = [plane.get("plane_id") for plane in document.get("planes") or []]
    if len(plane_ids) != len(set(plane_ids)):
        errors.append("queen: plane_id values must be unique")
    if set(plane_ids) != {"identity", "admission", "mission", "observation", "workforce", "decision"}:
        errors.append("queen: all six constitutional planes are required")
    return errors


def validate_access(document: dict[str, Any]) -> list[str]:
    errors = schema_errors(document, SCHEMAS["access"], "access")
    errors.extend(serialized_secret_findings(document, "access"))
    connectors = document.get("connectors") or []
    seen_connectors: set[str] = set()
    for index, connector in enumerate(connectors):
        prefix = f"access.connectors[{index}]"
        connector_id = connector.get("connector_id")
        if connector_id in seen_connectors:
            errors.append(f"{prefix}: duplicate connector_id {connector_id}")
        seen_connectors.add(str(connector_id))
        auth_mode = connector.get("auth_mode")
        credential_ref = connector.get("credential_ref")
        if auth_mode == "none" and credential_ref is not None:
            errors.append(f"{prefix}: auth_mode none cannot carry a credential_ref")
        if auth_mode != "none" and not credential_ref:
            errors.append(f"{prefix}: authenticated connector requires an opaque credential_ref")
        side_effect = connector.get("side_effect_class")
        if side_effect in {"draft", "reversible-write", "consequential"} and not connector.get("approval_gate"):
            errors.append(f"{prefix}: side-effecting connector requires an approval_gate")
        if side_effect == "consequential" and not set(document.get("human_gates") or []):
            errors.append(f"{prefix}: consequential connector requires bundle human gates")

    memory = document.get("memory") or {}
    for index, source in enumerate(document.get("knowledge_sources") or []):
        prefix = f"access.knowledge_sources[{index}]"
        operations = set(source.get("operations") or [])
        if operations & {"append", "update"} and source.get("writeback") != "human-approved":
            errors.append(f"{prefix}: append/update requires human-approved writeback")
        if source.get("classification") in {"confidential", "restricted"}:
            if memory.get("scope") != "private_vault":
                errors.append(f"{prefix}: confidential/restricted source requires private_vault memory")
            if memory.get("raw_content_policy") != "prohibited":
                errors.append(f"{prefix}: restricted access requires prohibited raw-content retention")

    validity = document.get("validity") or {}
    not_before = parse_datetime(validity.get("not_before"))
    expires_at = parse_datetime(validity.get("expires_at"))
    if not_before and expires_at and expires_at <= not_before:
        errors.append("access: expires_at must be after not_before")
    if document.get("status") == "leased" and expires_at is None:
        errors.append("access: leased bundle requires expires_at")
    return errors


def scope_base(value: str) -> str:
    return value.rstrip("*").rstrip("/")


def scopes_overlap(left: str, right: str) -> bool:
    left_base = scope_base(left)
    right_base = scope_base(right)
    if not left_base or not right_base:
        return True
    return (
        left_base == right_base
        or left_base.startswith(right_base + "/")
        or right_base.startswith(left_base + "/")
    )


def validate_mission(document: dict[str, Any], root: Path = ROOT) -> list[str]:
    errors = schema_errors(document, SCHEMAS["mission"], "mission")
    errors.extend(serialized_secret_findings(document, "mission"))
    participants = document.get("participants") or []
    by_id: dict[str, dict[str, Any]] = {}
    for index, participant in enumerate(participants):
        participant_id = str(participant.get("participant_id"))
        prefix = f"mission.participants[{index}]"
        if participant_id in by_id:
            errors.append(f"{prefix}: duplicate participant_id {participant_id}")
        by_id[participant_id] = participant

        if participant.get("participant_kind") == "agent":
            try:
                card_path = resolve_repo_ref(str(participant.get("card_ref")), root)
            except ValueError as exc:
                errors.append(f"{prefix}: {exc}")
                continue
            if not card_path.is_file():
                errors.append(f"{prefix}: missing card_ref {participant.get('card_ref')}")
            else:
                card = load_json(card_path)
                if card.get("id") != participant.get("agent_id"):
                    errors.append(f"{prefix}: card id does not match agent_id")
            access_ref = participant.get("access_bundle_ref")
            if access_ref:
                try:
                    access_path = resolve_repo_ref(str(access_ref), root)
                except ValueError as exc:
                    errors.append(f"{prefix}: {exc}")
                else:
                    if not access_path.is_file():
                        errors.append(f"{prefix}: missing access_bundle_ref {access_ref}")
                    else:
                        access = load_json(access_path)
                        access_errors = validate_access(access)
                        errors.extend(f"{prefix}: {error}" for error in access_errors)
                        if access.get("agent_id") != participant.get("agent_id"):
                            errors.append(f"{prefix}: access bundle agent_id mismatch")

        for dependency in participant.get("depends_on") or []:
            if dependency == participant_id:
                errors.append(f"{prefix}: participant cannot depend on itself")

    participant_ids = set(by_id)
    for participant_id, participant in by_id.items():
        unknown = set(participant.get("depends_on") or []) - participant_ids
        if unknown:
            errors.append(f"mission participant {participant_id}: unknown dependencies {sorted(unknown)}")

    milestone_ids: set[str] = set()
    for index, milestone in enumerate(document.get("milestones") or []):
        milestone_id = str(milestone.get("milestone_id"))
        if milestone_id in milestone_ids:
            errors.append(f"mission.milestones[{index}]: duplicate milestone_id {milestone_id}")
        milestone_ids.add(milestone_id)
        if milestone.get("owner_participant_id") not in participant_ids:
            errors.append(f"mission.milestones[{index}]: owner participant does not exist")

    separation = document.get("separation_of_duties") or {}
    makers = set(separation.get("maker_participant_ids") or [])
    checkers = set(separation.get("checker_participant_ids") or [])
    if makers & checkers:
        errors.append(f"mission: maker and checker participants overlap: {sorted(makers & checkers)}")
    if (makers | checkers) - participant_ids:
        errors.append("mission: maker/checker list references unknown participants")
    for participant_id in makers:
        if by_id.get(participant_id, {}).get("role") != "maker":
            errors.append(f"mission: {participant_id} is listed as maker but role is not maker")
    for participant_id in checkers:
        if by_id.get(participant_id, {}).get("role") != "checker":
            errors.append(f"mission: {participant_id} is listed as checker but role is not checker")
    for maker_id in makers:
        for checker_id in checkers:
            maker = by_id.get(maker_id) or {}
            checker = by_id.get(checker_id) or {}
            if maker.get("agent_id") == checker.get("agent_id"):
                errors.append(f"mission: maker {maker_id} and checker {checker_id} cannot use the same agent identity")

    writers = [participant for participant in participants if participant.get("participant_kind") == "agent"]
    for left_index, left in enumerate(writers):
        for right in writers[left_index + 1 :]:
            for left_scope in left.get("write_scopes") or []:
                for right_scope in right.get("write_scopes") or []:
                    if scopes_overlap(str(left_scope), str(right_scope)):
                        errors.append(
                            "mission: overlapping write scopes without a serial handoff: "
                            f"{left.get('participant_id')}={left_scope}, {right.get('participant_id')}={right_scope}"
                        )

    deadline = parse_datetime((document.get("timebox") or {}).get("deadline"))
    for milestone in document.get("milestones") or []:
        milestone_deadline = parse_datetime(milestone.get("deadline"))
        if deadline and milestone_deadline and milestone_deadline > deadline:
            errors.append(f"mission milestone {milestone.get('milestone_id')}: deadline exceeds mission deadline")
    return errors


def validate_n8n_handoff(document: dict[str, Any], root: Path = ROOT) -> list[str]:
    errors = schema_errors(document, SCHEMAS["n8n_handoff"], "n8n_handoff")
    errors.extend(serialized_secret_findings(document, "n8n_handoff"))
    if document.get("execution_chain") != N8N_EXECUTION_CHAIN:
        errors.append("n8n_handoff: execution_chain must use the eight shared primitives in canonical order")

    refs = document.get("estate_contract_refs") or {}
    for key, ref in refs.items():
        try:
            path = resolve_repo_ref(str(ref), root)
        except ValueError as exc:
            errors.append(f"n8n_handoff.estate_contract_refs.{key}: {exc}")
            continue
        if not path.is_file():
            errors.append(f"n8n_handoff.estate_contract_refs.{key}: missing file {ref}")

    target = document.get("target") or {}
    status = document.get("deployment_status")
    blockers = document.get("blockers") or []
    if status in {"design-only", "blocked"}:
        if target.get("activation_requested"):
            errors.append("n8n_handoff: blocked/design-only handoff cannot request activation")
        if not blockers:
            errors.append("n8n_handoff: blocked/design-only handoff must name blockers")
    if status in {"pilot-authorized", "active"}:
        if target.get("authentication_status") != "verified":
            errors.append("n8n_handoff: pilot/active handoff requires verified authentication")
        if not target.get("workflow_id"):
            errors.append("n8n_handoff: pilot/active handoff requires workflow_id")

    event_contract = document.get("event_contract") or {}
    intake = set(event_contract.get("required_at_intake") or [])
    before_action = set(event_contract.get("required_before_action") or [])
    receipts = set(event_contract.get("receipt_fields") or [])
    forbidden = set(event_contract.get("forbidden_fields") or [])
    required_intake = {
        "event_id",
        "correlation_id",
        "idempotency_key",
        "authentication_context_ref",
        "assignment_id",
        "agent_id",
        "mission_id",
        "requested_action",
        "target_resource",
        "risk_tier",
        "payload_ref",
        "trace_id",
    }
    required_before_action = {
        "policy_decision_id",
        "lease_id",
        "approval_status",
        "approval_receipt_ref",
        "normalized_action_hash",
    }
    required_receipts = {
        "receipt_id",
        "event_id",
        "correlation_id",
        "trace_id",
        "execution_status",
        "outcome_status",
        "action_hash",
        "attempt_count",
        "dlq_ref",
        "incident_ref",
    }
    required_forbidden = {
        "raw_access_token",
        "raw_refresh_token",
        "raw_secret",
        "raw_prompt",
        "raw_response",
        "private_payload",
        "approval_assertion",
        "security_pass_assertion",
        "promotion_assertion",
    }
    for label, missing in (
        ("required_at_intake", required_intake - intake),
        ("required_before_action", required_before_action - before_action),
        ("receipt_fields", required_receipts - receipts),
        ("forbidden_fields", required_forbidden - forbidden),
    ):
        if missing:
            errors.append(f"n8n_handoff.event_contract.{label}: missing {sorted(missing)}")
    if intake & forbidden or before_action & forbidden or receipts & forbidden:
        errors.append("n8n_handoff: forbidden fields cannot appear in intake, action, or receipt contracts")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queen", type=Path, default=DEFAULT_QUEEN)
    parser.add_argument("--access", type=Path, default=DEFAULT_ACCESS)
    parser.add_argument("--mission", type=Path, default=DEFAULT_MISSION)
    parser.add_argument("--n8n-handoff", type=Path, default=DEFAULT_N8N_HANDOFF)
    args = parser.parse_args()

    errors: list[str] = []
    errors.extend(validate_queen(load_json(args.queen)))
    errors.extend(validate_access(load_json(args.access)))
    errors.extend(validate_mission(load_json(args.mission)))
    errors.extend(validate_n8n_handoff(load_json(args.n8n_handoff)))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK: Queen, access-bundle, bounded-swarm, and n8n handoff governance contracts validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
