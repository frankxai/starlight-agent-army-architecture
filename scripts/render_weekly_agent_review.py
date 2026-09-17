#!/usr/bin/env python3
"""Render an advisory weekly AI-agent workforce review from normalized evidence."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from validate_agent_workforce import DEFAULT_ROSTER, ROOT, load_json, validate_roster

SCORECARD_SCHEMA = Path("schemas/agent-scorecard/agent-scorecard.schema.json")
EVAL_SCHEMA = Path("schemas/agent-eval-assessment/agent-eval-assessment.schema.json")
SECURITY_SCHEMA = Path("schemas/agent-security-assessment/agent-security-assessment.schema.json")
WORKFORCE_REVIEW_SCHEMA = Path("schemas/agent-workforce-review/agent-workforce-review.schema.json")


def parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def evidence_path(root: Path, assignment_id: str, kind: str) -> Path:
    return root / f"{assignment_id}.{kind}.json"


def read_evidence(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not path.is_file():
        return None, "missing"
    try:
        return load_json(path), None
    except (ValueError, json.JSONDecodeError) as exc:
        return None, f"invalid: {type(exc).__name__}"


def schema_errors(document: dict[str, Any], schema_path: Path) -> list[str]:
    try:
        import jsonschema  # type: ignore
    except ImportError:
        return ["jsonschema validator unavailable"]
    schema = load_json(schema_path)
    validator = jsonschema.Draft202012Validator(schema)
    return [
        f"{'.'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(document), key=lambda item: list(item.absolute_path))
    ]


def is_stale(document: dict[str, Any], as_of: datetime, stale_after_days: int) -> bool:
    generated = parse_timestamp(document.get("generated_at"))
    if generated is None:
        return True
    age_seconds = (as_of - generated).total_seconds()
    return age_seconds < 0 or age_seconds > stale_after_days * 86400


def review_assignment(
    assignment: dict[str, Any],
    policy: dict[str, Any],
    evidence_root: Path,
    as_of: datetime,
    repo_root: Path = ROOT,
) -> dict[str, Any]:
    assignment_id = assignment["assignment_id"]
    issues: list[str] = []
    signals: list[str] = []
    red = False

    scorecard, scorecard_error = read_evidence(evidence_path(evidence_root, assignment_id, "scorecard"))
    eval_receipt, eval_error = read_evidence(evidence_path(evidence_root, assignment_id, "eval"))
    security, security_error = read_evidence(evidence_path(evidence_root, assignment_id, "security"))

    for kind, error in (("scorecard", scorecard_error), ("live eval", eval_error), ("security", security_error)):
        if error:
            issues.append(f"{kind} evidence {error}")
            red = red or error.startswith("invalid")

    if scorecard:
        scorecard_schema_errors = schema_errors(scorecard, repo_root / SCORECARD_SCHEMA)
        if scorecard_schema_errors:
            issues.append("scorecard schema invalid: " + "; ".join(scorecard_schema_errors))
            red = True
        if scorecard.get("agent_id") != assignment["agent_id"]:
            issues.append("scorecard agent_id mismatch")
            red = True
        deployment = load_json(repo_root / assignment["deployment_ref"])
        if scorecard.get("deployment_id") != deployment.get("deployment_id"):
            issues.append("scorecard deployment_id mismatch")
            red = True
        verdict = scorecard.get("verdict")
        signals.append(f"scorecard={verdict}")
        if verdict in {"HOLD", "STOP"}:
            red = True
        elif verdict in {"IMPROVE", "INSUFFICIENT_DATA"}:
            issues.append(f"scorecard verdict {verdict}")
        elif verdict != "SCALE":
            issues.append("scorecard verdict missing or unknown")
            red = True

    if eval_receipt:
        eval_schema_errors = schema_errors(eval_receipt, repo_root / EVAL_SCHEMA)
        if eval_schema_errors:
            issues.append("live eval schema invalid: " + "; ".join(eval_schema_errors))
            red = True
        suite = load_json(repo_root / assignment["eval_suite_ref"])
        if eval_receipt.get("assignment_id") != assignment_id or eval_receipt.get("agent_id") != assignment["agent_id"]:
            issues.append("live eval subject mismatch")
            red = True
        if eval_receipt.get("suite_id") != assignment["eval_suite_ref"]:
            issues.append("live eval suite mismatch")
            red = True
        if not eval_receipt.get("assessor", {}).get("independent"):
            issues.append("live eval assessor is not independent")
            red = True
        if eval_receipt.get("mode") != policy["required_eval_mode"]:
            issues.append("live eval required; dry/unknown mode is not behavioral evidence")
        if is_stale(eval_receipt, as_of, int(policy["evidence_stale_after_days"])):
            issues.append("live eval evidence stale or missing generated_at")
        rate = eval_receipt.get("rate")
        minimum = float(suite.get("min_pass_rate", 1.0))
        if not isinstance(rate, (int, float)) or float(rate) < minimum:
            issues.append(f"live eval below {minimum:.0%} suite bar")
            red = True
        signals.append(f"eval_rate={rate}")

    if security:
        security_schema_errors = schema_errors(security, repo_root / SECURITY_SCHEMA)
        if security_schema_errors:
            issues.append("security assessment schema invalid: " + "; ".join(security_schema_errors))
            red = True
        if security.get("schema_version") != "agent-security-assessment.v1":
            issues.append("security assessment schema mismatch")
            red = True
        if security.get("assignment_id") != assignment_id or security.get("agent_id") != assignment["agent_id"]:
            issues.append("security assessment subject mismatch")
            red = True
        if not security.get("assessor", {}).get("independent"):
            issues.append("security assessor is not independent")
            red = True
        if security.get("profile_id") != assignment["security"]["profile_id"]:
            issues.append("security profile mismatch")
            red = True
        if is_stale(security, as_of, int(policy["evidence_stale_after_days"])):
            issues.append("security assessment stale or missing generated_at")
        findings = security.get("findings") or {}
        critical = int(findings.get("critical", 0))
        high = int(findings.get("high", 0))
        verdict = security.get("verdict")
        synthetic = bool(security.get("synthetic"))
        signals.append(f"security={verdict} c={critical} h={high}")
        if critical > 0 or high > 0 or verdict in {"FAIL", "HOLD"}:
            red = True
        if verdict != policy["required_security_verdict"]:
            issues.append(f"security verdict {verdict}; PASS required")
        if synthetic:
            issues.append("security evidence is synthetic-only")

    status = assignment["status"]
    if status in {"suspended", "retiring", "retired"}:
        exposure = "PAUSED"
        recommendation = "MAINTAIN_NO_DISPATCH"
    elif red:
        exposure = "RED"
        recommendation = "QUARANTINE_OR_RESTRICT_REVIEW"
    elif issues:
        exposure = "AMBER"
        recommendation = "COLLECT_OR_REMEDIATE_EVIDENCE"
    else:
        exposure = "GREEN"
        recommendation = "PROMOTION_REVIEW_ELIGIBLE" if status == "probation" else "CONTINUE"

    return {
        "assignment_id": assignment_id,
        "agent_id": assignment["agent_id"],
        "status": status,
        "runtime": assignment["runtime"]["executor"],
        "exposure": exposure,
        "recommendation": recommendation,
        "issues": issues,
        "signals": signals,
    }


def build_review(
    roster: dict[str, Any], evidence_root: Path, as_of: datetime, repo_root: Path = ROOT
) -> dict[str, Any]:
    errors = validate_roster(roster, repo_root)
    if errors:
        raise ValueError("invalid roster: " + "; ".join(errors))
    reviews = [
        review_assignment(assignment, roster["review_policy"], evidence_root, as_of, repo_root)
        for assignment in roster["assignments"]
    ]
    counts = Counter(item["exposure"] for item in reviews)
    outcome = "VERIFIED" if not counts["RED"] and not counts["AMBER"] else "HOLD"
    review = {
        "schema_version": "agent-workforce-review.v1",
        "generated_at": as_of.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "execution_status": "ok",
        "outcome_status": outcome,
        "authority": {
            "mode": "advisory",
            "human_owner": roster["authority"]["human_owner"],
            "automatic_promotion": False,
        },
        "summary": {key: counts[key] for key in ("RED", "AMBER", "GREEN", "PAUSED")},
        "assignments": reviews,
        "evidence_root": str(evidence_root),
    }
    generated_errors = schema_errors(review, repo_root / WORKFORCE_REVIEW_SCHEMA)
    if generated_errors:
        raise ValueError("generated weekly review invalid: " + "; ".join(generated_errors))
    return review


def markdown(review: dict[str, Any]) -> str:
    lines = [
        "# Weekly AI Agent Workforce Review",
        "",
        f"- Generated: `{review['generated_at']}`",
        f"- Execution: `{review['execution_status']}`",
        f"- Outcome: `{review['outcome_status']}`",
        "- Authority: advisory; all promotions, restorations, permission/budget increases, deployments, and retirements require the human owner.",
        "",
        "| Exposure | Assignment | Agent | Status | Runtime | Recommendation |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in review["assignments"]:
        lines.append(
            f"| {item['exposure']} | `{item['assignment_id']}` | `{item['agent_id']}` | "
            f"{item['status']} | {item['runtime']} | `{item['recommendation']}` |"
        )
    lines.extend(["", "## Decision queue", ""])
    for item in review["assignments"]:
        details = item["issues"] or ["No blocking evidence issue."]
        lines.append(f"### {item['assignment_id']} — {item['exposure']}")
        lines.append("")
        lines.append(f"Recommendation: `{item['recommendation']}`")
        lines.append("")
        for detail in details:
            lines.append(f"- {detail}")
        for signal in item["signals"]:
            lines.append(f"- Signal: `{signal}`")
        lines.append("")
    lines.extend(
        [
            "## Human decision",
            "",
            "No decision is inferred from this packet. The human owner must explicitly approve any consequential state change.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--roster", type=Path, default=DEFAULT_ROSTER)
    parser.add_argument("--evidence-root", type=Path, required=True)
    parser.add_argument("--as-of", help="ISO-8601 timestamp for deterministic runs")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()

    as_of = parse_timestamp(args.as_of) if args.as_of else datetime.now(timezone.utc)
    if as_of is None:
        raise SystemExit("ERROR: --as-of must be ISO-8601")
    try:
        review = build_review(load_json(args.roster), args.evidence_root, as_of)
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
