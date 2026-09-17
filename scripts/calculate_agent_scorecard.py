#!/usr/bin/env python3
"""Calculate an evidence-labeled agent scorecard from deployment and run receipts."""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import fmean
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
QUALITY_AXES = (
    "task_success",
    "evidence_grounding",
    "reliability",
    "safety",
    "efficiency",
    "judgment_routing",
)


def load_receipts(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    if text.startswith("["):
        value = json.loads(text)
        if not isinstance(value, list):
            raise ValueError("receipt JSON must be an array or JSON Lines")
        return value
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def nearest_rank_p95(values: list[int]) -> int | None:
    if not values:
        return None
    ordered = sorted(values)
    return ordered[max(0, math.ceil(0.95 * len(ordered)) - 1)]


def round_or_none(value: float | None, places: int = 4) -> float | None:
    return None if value is None else round(value, places)


def deduplicated_value(receipt: dict[str, Any], confidence_adjusted: bool) -> float:
    unique_total = 0.0
    grouped: dict[str, list[float]] = defaultdict(list)
    for index, component in enumerate(receipt["outcome"].get("value_components", [])):
        amount = float(component["amount_usd"])
        if confidence_adjusted:
            amount *= float(component["attribution_confidence"])
        group = component.get("overlap_group")
        if group:
            grouped[str(group)].append(amount)
        else:
            unique_total += amount
    return unique_total + sum(max(values) for values in grouped.values())


def compare(actual: float | None, operator: str, target: float) -> bool | None:
    if actual is None:
        return None
    return {
        ">=": actual >= target,
        "<=": actual <= target,
        "=": actual == target,
        ">": actual > target,
        "<": actual < target,
    }[operator]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--receipts", required=True, type=Path)
    parser.add_argument(
        "--expected-runs",
        type=int,
        help="Independent completed/admitted run count from the runtime or scheduler census",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    profile = json.loads(args.profile.read_text(encoding="utf-8"))
    receipts = load_receipts(args.receipts)
    if not receipts:
        raise SystemExit("ERROR: no receipts")
    for receipt in receipts:
        if receipt.get("deployment_id") != profile.get("deployment_id"):
            raise SystemExit("ERROR: receipt deployment_id does not match profile")

    outcomes = Counter(receipt["outcome"]["status"] for receipt in receipts)
    successes = outcomes["success"]
    runs = len(receipts)
    if args.expected_runs is not None and args.expected_runs < runs:
        raise SystemExit("ERROR: --expected-runs cannot be smaller than the receipt count")
    receipt_completeness = (
        runs / args.expected_runs if args.expected_runs is not None and args.expected_runs > 0 else None
    )
    first_pass = sum(bool(receipt["outcome"]["accepted_first_pass"]) for receipt in receipts)
    durable = sum(bool(receipt["outcome"].get("durable_artifacts")) for receipt in receipts)
    traceable = sum(bool(receipt["outcome"]["traceable_output"]) for receipt in receipts)
    human_minutes = sum(float(receipt["outcome"]["human_review_minutes"]) for receipt in receipts)

    usage = Counter()
    for receipt in receipts:
        usage.update(receipt["usage"])

    costs_by_basis: dict[str, float] = defaultdict(float)
    costs_by_category: dict[str, float] = defaultdict(float)
    for receipt in receipts:
        for cost in receipt.get("costs", []):
            amount = float(cost["amount_usd"])
            costs_by_basis[cost["basis"]] += amount
            costs_by_category[cost["category"]] += amount
    total_cost = sum(costs_by_basis.values())
    actual_cash = costs_by_basis.get("actual_cash", 0.0)
    cost_per_success = total_cost / successes if successes else None

    gross_value = sum(deduplicated_value(receipt, False) for receipt in receipts)
    adjusted_value = sum(deduplicated_value(receipt, True) for receipt in receipts)
    roi = (adjusted_value - total_cost) / total_cost if total_cost else None

    dimensions = {
        axis: fmean(float(receipt["quality"][axis]) for receipt in receipts)
        for axis in QUALITY_AXES
    }
    weights = profile["quality"]["weights"]
    capability = 100 * sum(dimensions[axis] * float(weights[axis]) for axis in QUALITY_AXES)
    critical_failures = sum(
        int(receipt["quality"]["critical_safety_failures"]) for receipt in receipts
    )
    p95 = nearest_rank_p95([int(receipt["latency_ms"]) for receipt in receipts])

    metrics: dict[str, float | int | None] = {
        "receipt_completeness_ratio": receipt_completeness,
        "task_success_rate": successes / runs,
        "first_pass_acceptance_rate": first_pass / runs,
        "durable_artifact_rate": durable / runs,
        "traceable_output_rate": traceable / runs,
        "capability_score": capability,
        "critical_safety_failures": critical_failures,
        "p95_latency_ms": p95,
        "total_economic_cost_usd": total_cost,
        "actual_cash_cost_usd": actual_cash,
        "cost_per_success_usd": cost_per_success,
        "confidence_adjusted_value_usd": adjusted_value,
        "confidence_adjusted_roi_ratio": roi,
        "human_review_minutes_per_success": human_minutes / successes if successes else None,
    }
    has_synthetic = any(
        (receipt.get("metadata") or {}).get("synthetic") for receipt in receipts
    )

    goal_results = []
    for goal in profile.get("goals", []):
        actual = metrics.get(goal["metric_id"])
        passed = compare(
            float(actual) if actual is not None else None,
            goal["target"]["operator"],
            float(goal["target"]["value"]),
        )
        if has_synthetic:
            result_label = "not_evaluable_synthetic"
        elif goal["status"] in {"proposed", "baselining", "retired"}:
            result_label = "not_active"
        else:
            result_label = "pass" if passed else "miss" if passed is False else "insufficient"
        goal_results.append(
            {
                "goal_id": goal["goal_id"],
                "status": goal["status"],
                "metric_id": goal["metric_id"],
                "actual": round_or_none(float(actual)) if actual is not None else None,
                "operator": goal["target"]["operator"],
                "target": goal["target"]["value"],
                "deadline": goal["target"]["deadline"],
                "result": result_label,
            }
        )

    quality_cfg = profile["quality"]
    budgets = profile["economics"]["budgets"]
    quality_pass = (
        capability >= float(quality_cfg["min_capability_score"])
        and metrics["task_success_rate"] >= float(quality_cfg["min_task_success_rate"])
    )
    latency_cap = quality_cfg.get("max_p95_latency_ms")
    latency_pass = latency_cap is None or (p95 is not None and p95 <= int(latency_cap))
    cost_cap = budgets.get("max_cost_per_success_usd")
    cost_pass = cost_cap is None or (
        cost_per_success is not None and cost_per_success <= float(cost_cap)
    )
    sample_pass = runs >= int(quality_cfg["min_sample_size"])
    coverage_known = receipt_completeness is not None
    baselines_complete = all(
        (goal.get("baseline") or {}).get("status") == "measured"
        for goal in profile.get("goals", [])
        if goal.get("status") not in {"retired"}
    )
    economics_ready = profile["economics"]["budget_status"] == "approved"
    lifecycle_ready = profile.get("lifecycle_status") == "observed"

    if critical_failures > int(quality_cfg["max_critical_safety_failures"]):
        verdict = "HOLD"
    elif not sample_pass or not coverage_known or not baselines_complete:
        verdict = "INSUFFICIENT_DATA"
    elif not economics_ready or not lifecycle_ready:
        verdict = "IMPROVE"
    elif quality_pass and latency_pass and cost_pass:
        verdict = "SCALE"
    else:
        verdict = "IMPROVE"

    limitations = []
    if has_synthetic:
        limitations.append("Input includes synthetic receipts; results prove formulas, not real-world ROI.")
    if actual_cash == 0:
        limitations.append("No actual-cash cost was evidenced; provider amounts are estimates or allocations.")
    if not sample_pass:
        limitations.append(
            f"Sample size {runs} is below the decision minimum {quality_cfg['min_sample_size']}."
        )
    if not coverage_known:
        limitations.append(
            "Receipt coverage is unknown because no independent completed-run count was supplied."
        )
    if not baselines_complete:
        limitations.append("One or more active/proposed goals still lacks a measured baseline.")
    if profile["economics"]["budget_status"] != "approved":
        limitations.append("Budget thresholds are proposals, not owner-approved spend authority.")
    if not lifecycle_ready:
        limitations.append("Deployment lifecycle is not observed; SCALE is not available.")

    starts = [receipt["started_at"] for receipt in receipts]
    ends = [receipt["ended_at"] for receipt in receipts]
    scorecard = {
        "schema_version": "agent-scorecard.v1",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "deployment_id": profile["deployment_id"],
        "agent_id": profile["agent_id"],
        "period": {
            "start": min(starts),
            "end": max(ends),
            "timezone": profile["measurement"]["timezone"],
        },
        "sample": {
            "runs": runs,
            "expected_runs": args.expected_runs,
            "receipt_completeness_ratio": round_or_none(receipt_completeness),
            "outcomes": dict(sorted(outcomes.items())),
            "successes": successes,
            "first_pass_acceptance_rate": round(first_pass / runs, 4),
            "durable_artifact_rate": round(durable / runs, 4),
            "traceable_output_rate": round(traceable / runs, 4),
            "confidence": "decision-grade" if sample_pass else "insufficient",
        },
        "usage": {key: int(value) for key, value in sorted(usage.items())},
        "costs": {
            "by_basis_usd": {key: round(value, 4) for key, value in sorted(costs_by_basis.items())},
            "by_category_usd": {key: round(value, 4) for key, value in sorted(costs_by_category.items())},
            "actual_cash_cost_usd": round(actual_cash, 4),
            "total_economic_cost_usd": round(total_cost, 4),
            "cost_per_run_usd": round(total_cost / runs, 4),
            "cost_per_success_usd": round_or_none(cost_per_success),
            "human_review_minutes": round(human_minutes, 2),
            "human_review_minutes_per_success": round_or_none(
                human_minutes / successes if successes else None, 2
            ),
        },
        "value": {
            "gross_value_usd": round(gross_value, 4),
            "confidence_adjusted_value_usd": round(adjusted_value, 4),
            "confidence_adjusted_roi_ratio": round_or_none(roi),
            "confidence_adjusted_roi_percent": round_or_none(roi * 100 if roi is not None else None, 2),
        },
        "quality": {
            "capability_profile": quality_cfg["capability_profile"],
            "dimension_scores": {key: round(value, 4) for key, value in dimensions.items()},
            "capability_score": round(capability, 2),
            "critical_safety_failures": critical_failures,
            "p95_latency_ms": p95,
        },
        "goals": goal_results,
        "verdict": verdict,
        "limitations": limitations,
    }

    try:
        import jsonschema  # type: ignore

        schema = json.loads(
            (ROOT / "schemas" / "agent-scorecard" / "agent-scorecard.schema.json").read_text(
                encoding="utf-8"
            )
        )
        jsonschema.Draft202012Validator(schema).validate(scorecard)
    except ImportError:
        pass

    rendered = json.dumps(scorecard, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
