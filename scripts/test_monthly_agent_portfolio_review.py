#!/usr/bin/env python3
"""Focused tests for the monthly agent-estate portfolio review."""
from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from render_monthly_agent_portfolio_review import build_monthly_review
from validate_agent_workforce import DEFAULT_ROSTER, ROOT, load_json

PERIOD_START = datetime(2026, 8, 1, tzinfo=timezone.utc)
PERIOD_END = datetime(2026, 9, 1, tzinfo=timezone.utc)
AS_OF = datetime(2026, 9, 1, 8, 0, tzinfo=timezone.utc)


def weekly(generated_at: str, exposure: str) -> dict:
    recommendation = {
        "GREEN": "CONTINUE",
        "AMBER": "COLLECT_OR_REMEDIATE_EVIDENCE",
        "RED": "QUARANTINE_OR_RESTRICT_REVIEW",
        "PAUSED": "MAINTAIN_NO_DISPATCH",
    }[exposure]
    summary = {key: int(key == exposure) for key in ("RED", "AMBER", "GREEN", "PAUSED")}
    return {
        "schema_version": "agent-workforce-review.v1",
        "generated_at": generated_at,
        "execution_status": "ok",
        "outcome_status": "VERIFIED" if exposure in {"GREEN", "PAUSED"} else "HOLD",
        "authority": {"mode": "advisory", "human_owner": "frank", "automatic_promotion": False},
        "summary": summary,
        "assignments": [
            {
                "assignment_id": "starlight-operator-private",
                "agent_id": "starlight-operator",
                "status": "planned",
                "runtime": "hermes",
                "exposure": exposure,
                "recommendation": recommendation,
                "issues": [],
                "signals": [f"test={exposure}"],
            }
        ],
        "evidence_root": "private:test/weekly/",
    }


def write_scorecard(root: Path) -> None:
    value = {
        "schema_version": "agent-scorecard.v1",
        "generated_at": "2026-08-31T20:00:00Z",
        "deployment_id": "starlight-operator-hermes",
        "agent_id": "starlight-operator",
        "period": {
            "start": "2026-08-01T00:00:00Z",
            "end": "2026-09-01T00:00:00Z",
            "timezone": "Europe/Amsterdam",
        },
        "sample": {"runs": 40, "successful_outcomes": 34},
        "usage": {"model_calls": 80, "tool_calls": 120},
        "costs": {"actual_cash_cost_usd": 20.0, "total_economic_cost_usd": 80.0},
        "value": {"confidence_adjusted_value_usd": 160.0, "confidence_adjusted_roi_ratio": 1.0},
        "quality": {"critical_safety_failures": 0, "durable_artifact_rate": 0.8},
        "goals": [
            {"goal_id": "instrument-starlight-operator", "latest_value": 0.98},
            {"goal_id": "prove-starlight-residue", "latest_value": 0.8},
        ],
        "verdict": "SCALE",
        "limitations": [],
    }
    (root / "starlight-operator-private.scorecard.json").write_text(json.dumps(value), encoding="utf-8")


class MonthlyPortfolioReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.roster = load_json(DEFAULT_ROSTER)
        self.green_weeks = [
            weekly("2026-08-04T10:00:00Z", "GREEN"),
            weekly("2026-08-11T10:00:00Z", "GREEN"),
            weekly("2026-08-18T10:00:00Z", "GREEN"),
            weekly("2026-08-25T10:00:00Z", "GREEN"),
        ]

    def build(self, reviews: list[dict], evidence_root: Path) -> dict:
        return build_monthly_review(
            self.roster,
            reviews,
            evidence_root,
            PERIOD_START,
            PERIOD_END,
            AS_OF,
            ROOT,
        )

    def test_four_green_weeks_are_scale_review_eligible_but_advisory(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_scorecard(root)
            review = self.build(self.green_weeks, root)
        item = review["assignments"][0]
        self.assertEqual(item["decision"], "SCALE_REVIEW_ELIGIBLE")
        self.assertEqual(item["utilization"]["runs"], 40)
        self.assertEqual(review["outcome_status"], "VERIFIED")
        self.assertFalse(review["authority"]["automatic_state_change"])

    def test_red_week_requires_security_and_remediation_review(self) -> None:
        reviews = list(self.green_weeks)
        reviews[2] = weekly("2026-08-18T10:00:00Z", "RED")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_scorecard(root)
            review = self.build(reviews, root)
        self.assertEqual(review["assignments"][0]["decision"], "SECURITY_AND_REMEDIATION_REVIEW")
        self.assertEqual(review["outcome_status"], "HOLD")

    def test_insufficient_weekly_coverage_holds_for_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_scorecard(root)
            review = self.build(self.green_weeks[:2], root)
        self.assertEqual(review["assignments"][0]["decision"], "HOLD_FOR_EVIDENCE")

    def test_invalid_weekly_authority_is_an_input_error(self) -> None:
        reviews = list(self.green_weeks)
        reviews[0]["authority"]["automatic_promotion"] = True
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_scorecard(root)
            review = self.build(reviews, root)
        self.assertEqual(review["execution_status"], "error")
        self.assertEqual(review["outcome_status"], "HOLD")
        self.assertTrue(review["input_errors"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
