#!/usr/bin/env python3
"""Adversarial and behavior tests for the AI-agent workforce layer."""
from __future__ import annotations

import copy
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from render_weekly_agent_review import build_review
from validate_agent_workforce import DEFAULT_ROSTER, ROOT, load_json, validate_roster

AS_OF = datetime(2026, 8, 14, 12, 0, tzinfo=timezone.utc)


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value), encoding="utf-8")


class WorkforceValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.roster = load_json(DEFAULT_ROSTER)

    def test_checked_in_roster_is_semantically_valid(self) -> None:
        self.assertEqual(validate_roster(self.roster, ROOT), [])

    def test_n8n_cannot_become_executor(self) -> None:
        mutated = copy.deepcopy(self.roster)
        mutated["assignments"][0]["runtime"]["executor"] = "n8n"
        errors = validate_roster(mutated, ROOT)
        self.assertTrue(any("cannot be the workforce executor" in error for error in errors))

    def test_queen_cannot_auto_promote(self) -> None:
        mutated = copy.deepcopy(self.roster)
        mutated["authority"]["prohibited_automations"].remove("promote")
        errors = validate_roster(mutated, ROOT)
        self.assertTrue(any("missing prohibited automations" in error for error in errors))

    def test_traversal_reference_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.roster)
        mutated["assignments"][0]["card_ref"] = "../secrets.json"
        errors = validate_roster(mutated, ROOT)
        self.assertTrue(any("unsafe repository reference" in error for error in errors))


class WorkforceReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.roster = load_json(DEFAULT_ROSTER)
        self.assignment = self.roster["assignments"][0]
        self.assignment_id = self.assignment["assignment_id"]

    def review(self, evidence_root: Path) -> dict:
        return build_review(self.roster, evidence_root, AS_OF, ROOT)

    def write_green_evidence(self, evidence_root: Path) -> None:
        write_json(
            evidence_root / f"{self.assignment_id}.scorecard.json",
            {
                "schema_version": "agent-scorecard.v1",
                "generated_at": "2026-08-14T10:00:00Z",
                "deployment_id": "starlight-operator-hermes",
                "agent_id": "starlight-operator",
                "period": {
                    "start": "2026-08-07T10:00:00Z",
                    "end": "2026-08-14T10:00:00Z",
                    "timezone": "Europe/Amsterdam",
                },
                "sample": {"runs": 30},
                "usage": {},
                "costs": {},
                "value": {},
                "quality": {"critical_safety_failures": 0},
                "goals": [],
                "verdict": "SCALE",
                "limitations": [],
            },
        )
        write_json(
            evidence_root / f"{self.assignment_id}.eval.json",
            {
                "schema_version": "agent-eval-assessment.v1",
                "mode": "live",
                "generated_at": "2026-08-14T10:00:00Z",
                "assignment_id": self.assignment_id,
                "agent_id": "starlight-operator",
                "suite_id": "evals/starlight-operator.v1.json",
                "runtime": {
                    "executor": "hermes",
                    "model": "test-model",
                    "artifact_digests": {"card": "a" * 64},
                },
                "assessor": {"id": "independent-eval-lane", "independent": True},
                "passed": 3,
                "total": 3,
                "rate": 1.0,
                "raw_receipt_ref": "private:test/eval.json",
                "limitations": [],
            },
        )
        write_json(
            evidence_root / f"{self.assignment_id}.security.json",
            {
                "schema_version": "agent-security-assessment.v1",
                "generated_at": "2026-08-14T10:00:00Z",
                "assignment_id": self.assignment_id,
                "agent_id": "starlight-operator",
                "assessor": {"id": "independent-security-lane", "independent": True},
                "profile_id": "l4-private-operator",
                "target": {
                    "runtime": "hermes",
                    "environment": "sandbox",
                    "scope": ["prompt", "tools", "memory", "handoffs"],
                    "artifact_digests": {"card": "a" * 64},
                },
                "verdict": "PASS",
                "findings": {"critical": 0, "high": 0, "medium": 0, "low": 0},
                "probes": [
                    {
                        "id": "prompt-injection",
                        "category": "prompt-security",
                        "result": "PASS",
                        "evidence_ref": "private:test/security/prompt-injection.json",
                    }
                ],
                "limitations": [],
                "synthetic": False,
            },
        )

    def test_missing_evidence_is_amber_not_green(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            review = self.review(Path(temp))
        self.assertEqual(review["assignments"][0]["exposure"], "AMBER")
        self.assertEqual(review["outcome_status"], "HOLD")

    def test_complete_fresh_evidence_is_green_but_advisory(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_green_evidence(root)
            review = self.review(root)
        self.assertEqual(review["assignments"][0]["exposure"], "GREEN")
        self.assertFalse(review["authority"]["automatic_promotion"])

    def test_critical_security_finding_is_red(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_green_evidence(root)
            security_path = root / f"{self.assignment_id}.security.json"
            security = load_json(security_path)
            security["verdict"] = "FAIL"
            security["findings"]["critical"] = 1
            write_json(security_path, security)
            review = self.review(root)
        item = review["assignments"][0]
        self.assertEqual(item["exposure"], "RED")
        self.assertEqual(item["recommendation"], "QUARANTINE_OR_RESTRICT_REVIEW")

    def test_self_assessed_eval_is_red(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_green_evidence(root)
            eval_path = root / f"{self.assignment_id}.eval.json"
            receipt = load_json(eval_path)
            receipt["assessor"]["independent"] = False
            write_json(eval_path, receipt)
            review = self.review(root)
        self.assertEqual(review["assignments"][0]["exposure"], "RED")

    def test_stale_eval_cannot_be_green(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_green_evidence(root)
            eval_path = root / f"{self.assignment_id}.eval.json"
            receipt = load_json(eval_path)
            receipt["generated_at"] = "2026-07-01T10:00:00Z"
            write_json(eval_path, receipt)
            review = self.review(root)
        self.assertEqual(review["assignments"][0]["exposure"], "AMBER")

    def test_synthetic_security_cannot_be_green(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_green_evidence(root)
            security_path = root / f"{self.assignment_id}.security.json"
            security = load_json(security_path)
            security["synthetic"] = True
            write_json(security_path, security)
            review = self.review(root)
        self.assertEqual(review["assignments"][0]["exposure"], "AMBER")

    def test_scorecard_hold_is_red(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_green_evidence(root)
            scorecard_path = root / f"{self.assignment_id}.scorecard.json"
            scorecard = load_json(scorecard_path)
            scorecard["verdict"] = "HOLD"
            write_json(scorecard_path, scorecard)
            review = self.review(root)
        self.assertEqual(review["assignments"][0]["exposure"], "RED")

    def test_malformed_security_receipt_is_red(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_green_evidence(root)
            security_path = root / f"{self.assignment_id}.security.json"
            security = load_json(security_path)
            security.pop("target")
            write_json(security_path, security)
            review = self.review(root)
        item = review["assignments"][0]
        self.assertEqual(item["exposure"], "RED")
        self.assertTrue(any("schema invalid" in issue for issue in item["issues"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
