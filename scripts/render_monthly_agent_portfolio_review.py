#!/usr/bin/env python3
"""Render an advisory monthly agent-estate review from weekly evidence packets."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from render_weekly_agent_review import parse_timestamp, schema_errors
from validate_agent_workforce import DEFAULT_ROSTER, ROOT, load_json, validate_roster

WEEKLY_SCHEMA = ROOT / "schemas" / "agent-workforce-review" / "agent-workforce-review.schema.json"
MONTHLY_SCHEMA = ROOT / "schemas" / "agent-portfolio-review" / "agent-portfolio-review.schema.json"
SCORECARD_SCHEMA = ROOT / "schemas" / "agent-scorecard" / "agent-scorecard.schema.json"

EXPOSURES = ("RED", "AMBER", "GREEN", "PAUSED")
NO_DISPATCH_STATES = {"suspended", "retiring", "retired"}


def iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def read_weekly_review_directory(root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    reviews: list[dict[str, Any]] = []
    errors: list[str] = []
    if not root.is_dir():
        return reviews, [f"weekly review directory missing: {root}"]
    for path in sorted(root.glob("*.json")):
        try:
            reviews.append(load_json(path))
        except (ValueError, json.JSONDecodeError) as exc:
            errors.append(f"{path.name}: invalid JSON: {type(exc).__name__}")
    return reviews, errors


def value_from(mapping: dict[str, Any], *keys: str) -> int | float | None:
    for key in keys:
        value = mapping.get(key)
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)):
            return value
    return None


def scorecard_summary(
    evidence_root: Path, assignment_id: str, agent_id: str, deployment_id: str
) -> tuple[dict[str, Any], list[str]]:
    path = evidence_root / f"{assignment_id}.scorecard.json"
    empty = {
        "utilization": {
            "runs": None,
            "successful_outcomes": None,
            "model_calls": None,
            "tool_calls": None,
            "durable_artifact_rate": None,
        },
        "economics": {
            "actual_cash_cost_usd": None,
            "total_economic_cost_usd": None,
            "confidence_adjusted_value_usd": None,
            "confidence_adjusted_roi_ratio": None,
        },
        "goal_values": {},
    }
    if not path.is_file():
        return empty, ["current scorecard missing"]
    try:
        scorecard = load_json(path)
    except (ValueError, json.JSONDecodeError) as exc:
        return empty, [f"current scorecard invalid: {type(exc).__name__}"]
    errors = schema_errors(scorecard, SCORECARD_SCHEMA)
    limitations = ["current scorecard schema invalid: " + "; ".join(errors)] if errors else []
    if scorecard.get("agent_id") != agent_id:
        limitations.append("current scorecard agent_id mismatch")
    if scorecard.get("deployment_id") != deployment_id:
        limitations.append("current scorecard deployment_id mismatch")

    sample = scorecard.get("sample") or {}
    usage = scorecard.get("usage") or {}
    costs = scorecard.get("costs") or {}
    value = scorecard.get("value") or {}
    quality = scorecard.get("quality") or {}
    goal_values: dict[str, int | float] = {}
    for goal in scorecard.get("goals") or []:
        if not isinstance(goal, dict) or not goal.get("goal_id"):
            continue
        latest = value_from(goal, "latest_value", "value", "current")
        if latest is not None:
            goal_values[str(goal["goal_id"])] = latest

    return {
        "utilization": {
            "runs": value_from(sample, "runs"),
            "successful_outcomes": value_from(sample, "successful_outcomes", "successes"),
            "model_calls": value_from(usage, "model_calls", "llm_calls"),
            "tool_calls": value_from(usage, "tool_calls"),
            "durable_artifact_rate": value_from(quality, "durable_artifact_rate"),
        },
        "economics": {
            "actual_cash_cost_usd": value_from(costs, "actual_cash_cost_usd"),
            "total_economic_cost_usd": value_from(costs, "total_economic_cost_usd"),
            "confidence_adjusted_value_usd": value_from(value, "confidence_adjusted_value_usd"),
            "confidence_adjusted_roi_ratio": value_from(value, "confidence_adjusted_roi_ratio"),
        },
        "goal_values": goal_values,
    }, limitations


def monthly_decision(status: str, counts: Counter[str], observed: int, required: int) -> str:
    if status in NO_DISPATCH_STATES or counts["PAUSED"]:
        return "MAINTAIN_NO_DISPATCH"
    if counts["RED"]:
        return "SECURITY_AND_REMEDIATION_REVIEW"
    if observed < required:
        return "HOLD_FOR_EVIDENCE"
    if counts["AMBER"]:
        return "IMPROVEMENT_PLAN"
    if counts["GREEN"] == observed and observed:
        return "SCALE_REVIEW_ELIGIBLE"
    return "CONTINUE"


def build_monthly_review(
    roster: dict[str, Any],
    weekly_reviews: list[dict[str, Any]],
    evidence_root: Path,
    period_start: datetime,
    period_end: datetime,
    as_of: datetime,
    repo_root: Path = ROOT,
    source_errors: list[str] | None = None,
) -> dict[str, Any]:
    roster_errors = validate_roster(roster, repo_root)
    if roster_errors:
        raise ValueError("invalid roster: " + "; ".join(roster_errors))
    if period_end <= period_start:
        raise ValueError("period end must be after period start")

    input_errors = list(source_errors or [])
    valid_reviews: list[tuple[datetime, dict[str, Any]]] = []
    for index, review in enumerate(weekly_reviews):
        errors = schema_errors(review, WEEKLY_SCHEMA)
        if errors:
            input_errors.append(f"weekly review {index}: " + "; ".join(errors))
            continue
        generated_at = parse_timestamp(review.get("generated_at"))
        if generated_at is None:
            input_errors.append(f"weekly review {index}: generated_at invalid")
            continue
        if period_start <= generated_at < period_end:
            valid_reviews.append((generated_at, review))
    valid_reviews.sort(key=lambda item: item[0])

    required = int(roster["review_policy"]["min_weekly_reviews_per_month"])
    assignment_reviews: list[dict[str, Any]] = []
    runtime_mix: Counter[str] = Counter()
    latest_exposure_counts: Counter[str] = Counter()
    decision_counts: Counter[str] = Counter()
    total_runs = 0
    any_run_value = False

    for assignment in roster["assignments"]:
        assignment_id = assignment["assignment_id"]
        observations: list[tuple[datetime, dict[str, Any]]] = []
        for generated_at, review in valid_reviews:
            match = next(
                (item for item in review.get("assignments") or [] if item.get("assignment_id") == assignment_id),
                None,
            )
            if match:
                observations.append((generated_at, match))
        counts = Counter(item["exposure"] for _, item in observations)
        latest_exposure = observations[-1][1]["exposure"] if observations else None
        if latest_exposure:
            latest_exposure_counts[latest_exposure] += 1
        runtime = assignment["runtime"]["executor"]
        runtime_mix[runtime] += 1
        decision = monthly_decision(assignment["status"], counts, len(observations), required)
        decision_counts[decision] += 1

        deployment = load_json(repo_root / assignment["deployment_ref"])
        summary, limitations = scorecard_summary(
            evidence_root,
            assignment_id,
            assignment["agent_id"],
            str(deployment.get("deployment_id")),
        )
        runs = summary["utilization"]["runs"]
        if isinstance(runs, int):
            any_run_value = True
            total_runs += runs
        if len(observations) < required:
            limitations.append(f"only {len(observations)} of {required} required weekly reviews observed")

        goals: list[dict[str, Any]] = []
        for goal in deployment.get("goals") or []:
            target = goal.get("target") or {}
            goals.append(
                {
                    "goal_id": goal["goal_id"],
                    "status": goal["status"],
                    "metric_id": goal["metric_id"],
                    "target": target["value"],
                    "deadline": target["deadline"],
                    "latest_value": summary["goal_values"].get(goal["goal_id"]),
                }
            )

        assignment_reviews.append(
            {
                "assignment_id": assignment_id,
                "agent_id": assignment["agent_id"],
                "runtime": runtime,
                "lifecycle_status": assignment["status"],
                "weekly_reviews_observed": len(observations),
                "exposure_counts": {key: counts[key] for key in EXPOSURES},
                "latest_exposure": latest_exposure,
                "decision": decision,
                "utilization": summary["utilization"],
                "economics": summary["economics"],
                "goals": goals,
                "limitations": limitations,
            }
        )

    hold_decisions = {
        "SECURITY_AND_REMEDIATION_REVIEW",
        "HOLD_FOR_EVIDENCE",
        "IMPROVEMENT_PLAN",
    }
    outcome = "HOLD" if input_errors or any(item["decision"] in hold_decisions for item in assignment_reviews) else "VERIFIED"
    decisions = [
        f"{item['assignment_id']}: {item['decision']}"
        for item in assignment_reviews
        if item["decision"] != "CONTINUE"
    ]
    if not decisions:
        decisions = ["No consequential portfolio state change recommended."]

    review = {
        "schema_version": "agent-portfolio-review.v1",
        "cadence": "monthly",
        "generated_at": iso(as_of),
        "period": {
            "start": iso(period_start),
            "end": iso(period_end),
            "timezone": roster["review_policy"]["timezone"],
        },
        "execution_status": "error" if input_errors else "ok",
        "outcome_status": outcome,
        "authority": {
            "mode": "advisory",
            "human_owner": roster["authority"]["human_owner"],
            "automatic_state_change": False,
        },
        "coverage": {
            "weekly_reviews_observed": len(valid_reviews),
            "weekly_reviews_required": required,
            "assignments": len(assignment_reviews),
        },
        "summary": {
            **{key: latest_exposure_counts[key] for key in EXPOSURES},
            "decision_counts": dict(sorted(decision_counts.items())),
            "total_runs": total_runs if any_run_value else None,
        },
        "runtime_mix": dict(sorted(runtime_mix.items())),
        "assignments": assignment_reviews,
        "input_errors": input_errors,
        "portfolio_decisions": decisions,
    }
    monthly_schema_errors = schema_errors(review, MONTHLY_SCHEMA)
    if monthly_schema_errors:
        raise ValueError("generated monthly review invalid: " + "; ".join(monthly_schema_errors))
    return review


def markdown(review: dict[str, Any]) -> str:
    lines = [
        "# Monthly AI Agent Estate Review",
        "",
        f"- Period: `{review['period']['start']}` to `{review['period']['end']}`",
        f"- Generated: `{review['generated_at']}`",
        f"- Execution: `{review['execution_status']}`",
        f"- Outcome: `{review['outcome_status']}`",
        f"- Weekly coverage: `{review['coverage']['weekly_reviews_observed']}/{review['coverage']['weekly_reviews_required']}`",
        "- Authority: advisory. Promotion, restoration, permission/budget increases, deployment, external sends, and retirement remain human decisions.",
        "",
        "| Exposure | Assignment | Agent | Runtime | Reviews | Runs | Decision |",
        "| --- | --- | --- | --- | ---: | ---: | --- |",
    ]
    for item in review["assignments"]:
        runs = item["utilization"]["runs"]
        runs_text = str(runs) if runs is not None else "—"
        lines.append(
            f"| {item['latest_exposure'] or '—'} | `{item['assignment_id']}` | `{item['agent_id']}` | "
            f"{item['runtime']} | {item['weekly_reviews_observed']} | {runs_text} | `{item['decision']}` |"
        )
    lines.extend(["", "## Goal and improvement review", ""])
    for item in review["assignments"]:
        lines.extend([f"### {item['assignment_id']}", "", f"Decision: `{item['decision']}`", ""])
        for goal in item["goals"]:
            latest = "not measured" if goal["latest_value"] is None else goal["latest_value"]
            lines.append(
                f"- `{goal['goal_id']}` — {goal['status']}; `{goal['metric_id']}` latest `{latest}`, "
                f"target `{goal['target']}` by `{goal['deadline']}`."
            )
        for limitation in item["limitations"]:
            lines.append(f"- Limitation: {limitation}")
        lines.append("")
    lines.extend(["## Human decision queue", ""])
    for decision in review["portfolio_decisions"]:
        lines.append(f"- {decision}")
    if review["input_errors"]:
        lines.extend(["", "## Input errors", ""])
        for error in review["input_errors"]:
            lines.append(f"- {error}")
    lines.extend(
        [
            "",
            "No state change is inferred from this packet. Evidence of work is not evidence of business impact unless the linked outcome metric and artifact proof support it.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--roster", type=Path, default=DEFAULT_ROSTER)
    parser.add_argument("--weekly-reviews-root", type=Path, required=True)
    parser.add_argument("--evidence-root", type=Path, required=True)
    parser.add_argument("--period-start", required=True, help="ISO-8601 inclusive start")
    parser.add_argument("--period-end", required=True, help="ISO-8601 exclusive end")
    parser.add_argument("--as-of", help="ISO-8601 timestamp for deterministic runs")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()

    period_start = parse_timestamp(args.period_start)
    period_end = parse_timestamp(args.period_end)
    as_of = parse_timestamp(args.as_of) if args.as_of else datetime.now(timezone.utc)
    if not period_start or not period_end or not as_of:
        raise SystemExit("ERROR: period/as-of values must be ISO-8601 timestamps")
    weekly_reviews, source_errors = read_weekly_review_directory(args.weekly_reviews_root)
    try:
        review = build_monthly_review(
            load_json(args.roster),
            weekly_reviews,
            args.evidence_root,
            period_start,
            period_end,
            as_of,
            source_errors=source_errors,
        )
    except ValueError as exc:
        raise SystemExit(f"ERROR: {exc}") from exc

    rendered = markdown(review)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(rendered, end="")
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {args.json_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
