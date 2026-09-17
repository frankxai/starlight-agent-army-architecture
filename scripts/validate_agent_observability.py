#!/usr/bin/env python3
"""Validate deployment profiles, run receipts, metrics, and adoption state."""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEPLOYMENT_SCHEMA = ROOT / "schemas" / "agent-deployment" / "agent-deployment.schema.json"
RECEIPT_SCHEMA = ROOT / "schemas" / "agent-run-receipt" / "agent-run-receipt.schema.json"
DEPLOYMENTS = ROOT / "observability" / "deployments"
EXAMPLES = ROOT / "observability" / "examples"
METRIC_CATALOG = ROOT / "observability" / "metric-catalog.v1.json"
ADOPTION_REGISTRY = ROOT / "observability" / "adoption-registry.v1.json"
EVAL_DRY_RECEIPT = ROOT / "receipts" / "eval-run-dry.json"
FORBIDDEN_KEYS = {
    "prompt",
    "raw_prompt",
    "response",
    "raw_response",
    "transcript",
    "conversation",
    "secret",
    "api_key",
    "provider_payload",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def forbidden_paths(value: Any, prefix: str = "") -> list[str]:
    hits: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else key
            if key.lower() in FORBIDDEN_KEYS:
                hits.append(path)
            hits.extend(forbidden_paths(child, path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            hits.extend(forbidden_paths(child, f"{prefix}[{index}]"))
    return hits


def basic_required(data: dict[str, Any], keys: tuple[str, ...]) -> list[str]:
    return [f"missing {key}" for key in keys if key not in data]


def main() -> int:
    failed = 0
    metric_catalog = load_json(METRIC_CATALOG)
    metrics = set((metric_catalog.get("metrics") or {}).keys())
    if metric_catalog.get("schema_version") != "agent-metric-catalog.v1" or not metrics:
        print("FAIL observability/metric-catalog.v1.json: invalid or empty catalog")
        failed += 1
    elif forbidden := forbidden_paths(metric_catalog):
        print(
            "FAIL observability/metric-catalog.v1.json: forbidden raw-content keys: "
            + ", ".join(forbidden)
        )
        failed += 1
    else:
        print(f"OK   observability/metric-catalog.v1.json metrics={len(metrics)}")

    deployment_schema = load_json(DEPLOYMENT_SCHEMA)
    receipt_schema = load_json(RECEIPT_SCHEMA)
    try:
        import jsonschema  # type: ignore

        format_checker = jsonschema.FormatChecker()
        deployment_validator = jsonschema.Draft202012Validator(
            deployment_schema, format_checker=format_checker
        )
        receipt_validator = jsonschema.Draft202012Validator(
            receipt_schema, format_checker=format_checker
        )
        schema_mode = "jsonschema"
    except Exception:
        deployment_validator = None
        receipt_validator = None
        schema_mode = "basic-only"

    profiles: dict[str, dict[str, Any]] = {}
    for path in sorted(DEPLOYMENTS.glob("*.json")):
        rel = path.relative_to(ROOT).as_posix()
        try:
            profile = load_json(path)
        except Exception as exc:
            print(f"FAIL {rel}: JSON parse error: {exc}")
            failed += 1
            continue
        errors = basic_required(
            profile,
            (
                "schema_version",
                "deployment_id",
                "repo",
                "agent_id",
                "card_ref",
                "goals",
                "quality",
                "economics",
                "telemetry",
            ),
        )
        if deployment_validator is not None:
            errors.extend(error.message for error in deployment_validator.iter_errors(profile))
        forbidden = forbidden_paths(profile)
        if forbidden:
            errors.append(f"forbidden raw-content keys: {', '.join(forbidden)}")

        deployment_id = profile.get("deployment_id")
        if deployment_id in profiles:
            errors.append(f"duplicate deployment_id: {deployment_id}")
        card_ref = profile.get("card_ref")
        card_path = ROOT / str(card_ref)
        if not card_path.is_file():
            errors.append(f"card_ref missing: {card_ref}")
        else:
            card = load_json(card_path)
            if card.get("id") != profile.get("agent_id"):
                errors.append("agent_id does not match referenced card id")

        weights = (profile.get("quality") or {}).get("weights") or {}
        if abs(sum(float(value) for value in weights.values()) - 1.0) > 1e-9:
            errors.append("quality weights must sum to exactly 1.0")

        goals = profile.get("goals") or []
        goal_ids: set[str] = set()
        for goal in goals:
            goal_id = goal.get("goal_id")
            if goal_id in goal_ids:
                errors.append(f"duplicate goal_id: {goal_id}")
            goal_ids.add(goal_id)
            if goal.get("metric_id") not in metrics:
                errors.append(f"unknown metric_id: {goal.get('metric_id')}")
            baseline = goal.get("baseline") or {}
            if goal.get("status") in {"active", "met", "missed"}:
                if baseline.get("status") != "measured" or baseline.get("value") is None:
                    errors.append(f"active/closed goal requires measured baseline: {goal_id}")

        economics = profile.get("economics") or {}
        budgets = economics.get("budgets") or {}
        if economics.get("budget_status") == "approved" and any(
            value is None for value in budgets.values()
        ):
            errors.append("approved budgets cannot contain null values")

        errors = sorted(set(errors))
        if errors:
            print(f"FAIL {rel}")
            for error in errors:
                print(f"  - {error}")
            failed += 1
        else:
            profiles[str(deployment_id)] = profile
            print(f"OK   {rel} agent={profile['agent_id']} goals={len(goals)}")

    if not profiles:
        print("FAIL observability/deployments: no valid deployment profiles")
        failed += 1

    receipt_count = 0
    for path in sorted(EXAMPLES.glob("*.json")):
        rel = path.relative_to(ROOT).as_posix()
        try:
            document = load_json(path)
        except Exception as exc:
            print(f"FAIL {rel}: JSON parse error: {exc}")
            failed += 1
            continue
        receipts = document if isinstance(document, list) else [document]
        file_errors: list[str] = []
        for index, receipt in enumerate(receipts):
            receipt_count += 1
            errors = basic_required(
                receipt,
                (
                    "schema_version",
                    "run_id",
                    "deployment_id",
                    "agent_id",
                    "repo",
                    "started_at",
                    "ended_at",
                    "usage",
                    "costs",
                    "outcome",
                    "quality",
                ),
            )
            if receipt_validator is not None:
                errors.extend(error.message for error in receipt_validator.iter_errors(receipt))
            profile = profiles.get(str(receipt.get("deployment_id")))
            if profile is None:
                errors.append(f"unknown deployment_id: {receipt.get('deployment_id')}")
            else:
                for key in ("agent_id", "repo", "environment"):
                    if receipt.get(key) != profile.get(key):
                        errors.append(f"receipt {key} does not match deployment profile")
            try:
                started = parse_time(receipt["started_at"])
                ended = parse_time(receipt["ended_at"])
                if ended < started:
                    errors.append("ended_at precedes started_at")
                measured_ms = round((ended - started).total_seconds() * 1000)
                if abs(measured_ms - int(receipt.get("latency_ms", -1))) > 5:
                    errors.append("latency_ms does not match timestamps")
            except Exception as exc:
                errors.append(f"invalid timestamps: {exc}")
            if (receipt.get("metadata") or {}).get("synthetic") is not True:
                errors.append("committed example receipts must declare metadata.synthetic=true")
            forbidden = forbidden_paths(receipt)
            if forbidden:
                errors.append(f"forbidden raw-content keys: {', '.join(forbidden)}")
            provider_bases = {
                item.get("basis")
                for item in receipt.get("costs", [])
                if item.get("category") == "provider"
            }
            if "actual_cash" in provider_bases and "estimated_provider" in provider_bases:
                errors.append("provider charges cannot mix actual and estimated basis in one receipt")
            file_errors.extend(f"receipt[{index}]: {error}" for error in errors)

        if file_errors:
            print(f"FAIL {rel}")
            for error in sorted(set(file_errors)):
                print(f"  - {error}")
            failed += 1
        else:
            print(f"OK   {rel} receipts={len(receipts)} synthetic=yes")

    registry = load_json(ADOPTION_REGISTRY)
    registry_errors = basic_required(registry, ("schema_version", "observed_at", "surfaces"))
    forbidden = forbidden_paths(registry)
    if forbidden:
        registry_errors.append(f"forbidden raw-content keys: {', '.join(forbidden)}")
    surface_ids: set[str] = set()
    for surface in registry.get("surfaces") or []:
        registry_errors.extend(
            f"surface missing {key}"
            for key in ("surface_id", "brand", "repo", "state", "evidence", "next_gate")
            if key not in surface
        )
        surface_id = surface.get("surface_id")
        if surface_id in surface_ids:
            registry_errors.append(f"duplicate surface_id: {surface_id}")
        surface_ids.add(surface_id)
    try:
        parse_time(registry["observed_at"])
    except Exception as exc:
        registry_errors.append(f"invalid observed_at: {exc}")
    if registry_errors:
        print("FAIL observability/adoption-registry.v1.json")
        for error in sorted(set(registry_errors)):
            print(f"  - {error}")
        failed += 1
    else:
        print(f"OK   observability/adoption-registry.v1.json surfaces={len(surface_ids)}")

    eval_receipt = load_json(EVAL_DRY_RECEIPT)
    eval_receipt_errors = forbidden_paths(eval_receipt)
    if eval_receipt_errors:
        print(
            "FAIL receipts/eval-run-dry.json: forbidden raw-content keys: "
            + ", ".join(eval_receipt_errors)
        )
        failed += 1
    else:
        print("OK   receipts/eval-run-dry.json raw-content-keys=none")

    print(
        f"\nobservability validation: profiles={len(profiles)} receipts={receipt_count} "
        f"schema={schema_mode} failures={failed}"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
