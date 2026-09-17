#!/usr/bin/env python3
"""Focused adversarial tests for agent-estate governance contracts."""
from __future__ import annotations

import copy
import unittest

from validate_agent_governance import (
    DEFAULT_ACCESS,
    DEFAULT_MISSION,
    DEFAULT_N8N_HANDOFF,
    DEFAULT_QUEEN,
    load_json,
    validate_access,
    validate_mission,
    validate_n8n_handoff,
    validate_queen,
)


class QueenGovernanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.queen = load_json(DEFAULT_QUEEN)

    def test_checked_in_contract_is_valid(self) -> None:
        self.assertEqual(validate_queen(self.queen), [])

    def test_queen_cannot_auto_promote(self) -> None:
        mutated = copy.deepcopy(self.queen)
        mutated["constitution"]["automatic_actions"].append("promotion")
        errors = validate_queen(mutated)
        self.assertTrue(any("schema" in error or "overlap" in error for error in errors))

    def test_all_six_planes_are_required(self) -> None:
        mutated = copy.deepcopy(self.queen)
        mutated["planes"] = mutated["planes"][:-1]
        self.assertTrue(any("six constitutional planes" in error for error in validate_queen(mutated)))


class AccessBundleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.access = load_json(DEFAULT_ACCESS)

    def test_checked_in_contract_is_valid(self) -> None:
        self.assertEqual(validate_access(self.access), [])

    def test_raw_jwt_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.access)
        mutated["connectors"][0]["credential_ref"] = "eyJaaa.bbb.ccc"
        self.assertTrue(any("secret" in error or "schema" in error for error in validate_access(mutated)))

    def test_consequential_connector_requires_gate(self) -> None:
        mutated = copy.deepcopy(self.access)
        mutated["connectors"][0]["approval_gate"] = None
        self.assertTrue(any("approval_gate" in error for error in validate_access(mutated)))

    def test_restricted_knowledge_requires_private_memory(self) -> None:
        mutated = copy.deepcopy(self.access)
        mutated["memory"]["scope"] = "session"
        self.assertTrue(any("private_vault" in error for error in validate_access(mutated)))


class SwarmMissionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mission = load_json(DEFAULT_MISSION)

    def test_checked_in_contract_is_valid(self) -> None:
        self.assertEqual(validate_mission(self.mission), [])

    def test_maker_cannot_check_itself(self) -> None:
        mutated = copy.deepcopy(self.mission)
        mutated["separation_of_duties"]["checker_participant_ids"] = ["portfolio-maker"]
        errors = validate_mission(mutated)
        self.assertTrue(any("overlap" in error or "role is not checker" in error for error in errors))

    def test_workflow_cannot_assert_authority(self) -> None:
        mutated = copy.deepcopy(self.mission)
        mutated["participants"][-1]["authority_assertions"] = "security-pass"
        self.assertTrue(any("schema" in error for error in validate_mission(mutated)))

    def test_overlapping_write_scopes_fail(self) -> None:
        mutated = copy.deepcopy(self.mission)
        mutated["participants"][2]["write_scopes"] = ["scripts/*"]
        self.assertTrue(any("overlapping write scopes" in error for error in validate_mission(mutated)))

    def test_path_traversal_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.mission)
        mutated["participants"][1]["card_ref"] = "../secrets.json"
        self.assertTrue(any("unsafe repository reference" in error for error in validate_mission(mutated)))


class N8nAutomationHandoffTests(unittest.TestCase):
    def setUp(self) -> None:
        self.handoff = load_json(DEFAULT_N8N_HANDOFF)

    def test_checked_in_blocked_handoff_is_valid(self) -> None:
        self.assertEqual(validate_n8n_handoff(self.handoff), [])

    def test_blocked_handoff_cannot_request_activation(self) -> None:
        mutated = copy.deepcopy(self.handoff)
        mutated["target"]["activation_requested"] = True
        self.assertTrue(any("cannot request activation" in error for error in validate_n8n_handoff(mutated)))

    def test_execution_primitives_cannot_be_reordered(self) -> None:
        mutated = copy.deepcopy(self.handoff)
        mutated["execution_chain"][0], mutated["execution_chain"][1] = (
            mutated["execution_chain"][1],
            mutated["execution_chain"][0],
        )
        self.assertTrue(any("canonical order" in error for error in validate_n8n_handoff(mutated)))

    def test_approval_receipt_is_required_before_action(self) -> None:
        mutated = copy.deepcopy(self.handoff)
        mutated["event_contract"]["required_before_action"].remove("approval_receipt_ref")
        self.assertTrue(any("approval_receipt_ref" in error for error in validate_n8n_handoff(mutated)))

    def test_raw_token_field_is_always_forbidden(self) -> None:
        mutated = copy.deepcopy(self.handoff)
        mutated["event_contract"]["forbidden_fields"].remove("raw_access_token")
        self.assertTrue(any("raw_access_token" in error for error in validate_n8n_handoff(mutated)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
