from __future__ import annotations

import copy
import unittest

from tests import test_execution_state_completion as completion_fixture
from tools import execution_authoring as authoring
from tools.execution_state import (
    canonical_json_digest, claim_payload_projection, completion_basis_projection,
    parse_strict_json_bytes, terminal_authority_digest,
)


class AuthoringFixture(unittest.TestCase):
    setUp = completion_fixture.CompletionFixture.setUp
    tearDown = completion_fixture.CompletionFixture.tearDown
    git = completion_fixture.CompletionFixture.git
    write = completion_fixture.CompletionFixture.write
    make_route = completion_fixture.CompletionFixture.make_route
    make_verification = completion_fixture.CompletionFixture.make_verification
    make_completed_state = completion_fixture.CompletionFixture.make_completed_state
    state_result = completion_fixture.CompletionFixture.state_result


class AuthoringTests(AuthoringFixture):
    def initial(self):
        request = copy.deepcopy(self.state['artifact_bindings'][0])
        for key in ('recorded_sequence', 'artifact', 'assurance'):
            request.pop(key)
        draft = authoring.draft_initial_route(self.route)
        change = authoring.initialize_state(
            draft.documents['route-decision.r1.draft.json'], self.route['route_digest'],
            [request], 'Approved implementation', [], '2026-07-10T00:00:00Z',
        )
        return parse_strict_json_bytes(change.documents['execution-state.json'], self.control / 'execution-state.json')

    def advance(self, state, target):
        return authoring.append_transition(state, self.route, state['state_revision'], target, 'Continue approved work', [], '2026-07-10T00:00:00Z')

    def executing(self):
        state = self.initial()
        state = self.advance(state, 'gated')
        return self.advance(state, 'executing')

    def test_initialization_and_nonterminal_operations_are_constructed(self):
        state = self.initial()
        self.assertEqual(2, state['state_revision'])
        self.assertEqual('routed', state['lifecycle_state'])
        self.assertEqual([], self.state_result(state).errors)
        executing = self.executing()
        blocked = self.advance(executing, 'blocked')
        resumed = self.advance(blocked, 'executing')
        self.assertEqual(6, resumed['block_contexts'][0]['resume_transition_sequence'])
        for current in (executing, blocked, resumed):
            self.assertEqual([], self.state_result(current).errors)
        self.assertEqual('executing', executing['lifecycle_state'])
        with self.assertRaises(ValueError):
            self.advance(executing, 'completed')
        with self.assertRaisesRegex(ValueError, 'revision'):
            authoring.append_transition(executing, self.route, 1, 'blocked', 'Wait', [], '2026-07-10T00:00:00Z')

    def test_initialization_requires_exact_bindings_and_separate_pin(self):
        draft = authoring.draft_initial_route(self.route)
        content = draft.documents['route-decision.r1.draft.json']
        for pin, bindings in ((None, []), ('sha256:' + '0' * 64, []), (self.route['route_digest'], [])):
            with self.subTest(pin=pin), self.assertRaises(ValueError):
                authoring.initialize_state(content, pin, bindings, 'Approved', [], '2026-07-10T00:00:00Z')
        self.assertEqual(self.route['route_digest'], draft.candidate_route_digest)

    def claim(self):
        state = self.executing()
        for kind in ('entered', 'exited'):
            state = authoring.append_phase_event(state, self.route, state['state_revision'], kind, 0, [], '2026-07-10T00:00:00Z')
        attempt = self.state['completion_attempts'][0]
        claimed = authoring.claim_completion(
            state, self.route, state['state_revision'], self.verification,
            attempt['verification_commitment']['verification_record_ref'],
            attempt['verification_commitment']['verification_record_sha256'],
            attempt['verification_commitment']['evidence_bindings'],
            self.work_snapshot, 'All checks passed', '2026-07-10T00:02:00Z',
        )
        self.assertEqual([], self.state_result(claimed).errors)
        return claimed

    def test_claim_and_terminal_outcomes_preserve_digest_projections(self):
        claimed = self.claim()
        attempt = claimed['completion_attempts'][0]
        self.assertEqual(canonical_json_digest(claim_payload_projection(attempt)), attempt['claim_digest'])
        self.assertEqual(canonical_json_digest(completion_basis_projection(claimed, attempt)), attempt['completion_basis_digest'])
        verified = authoring.record_outcome(claimed, self.route, 7, 'verified', 'Reviewed', '2026-07-10T00:03:00Z')
        self.assertEqual([], self.state_result(verified, terminal_passed=True).errors)
        with self.assertRaisesRegex(ValueError, 'completion pin'):
            authoring.record_outcome(verified, self.route, 8, 'completed', 'Done', '2026-07-10T00:04:00Z')
        completed = authoring.record_outcome(verified, self.route, 8, 'completed', 'Done', '2026-07-10T00:04:00Z', terminal_authority_digest(verified))
        self.assertEqual([], self.state_result(completed, terminal_passed=True).errors)
        self.assertNotEqual(terminal_authority_digest(verified), terminal_authority_digest(completed))

    def test_rejection_preserves_commitment_and_requires_fresh_retry(self):
        claimed = self.claim()
        rejected = authoring.record_outcome(claimed, self.route, 7, 'rejected', 'Need independent evidence', '2026-07-10T00:03:00Z')
        self.assertNotIn('current_completion_attempt_id', rejected)
        self.assertNotIn('completion_binding', rejected['completion_attempts'][0])
        self.assertEqual(claimed['completion_attempts'][0]['verification_commitment'], rejected['completion_attempts'][0]['verification_commitment'])
        self.assertEqual([], self.state_result(rejected).errors)
        resumed = self.advance(self.advance(rejected, 'gated'), 'executing')
        self.assertEqual([], self.state_result(resumed).errors)
