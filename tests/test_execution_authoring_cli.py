from __future__ import annotations

import copy
from datetime import datetime, timezone
import json
import subprocess
import sys
import unittest
from unittest import mock
from pathlib import Path

from tests.test_execution_authoring import AuthoringFixture

CLI = Path(__file__).resolve().parents[1] / 'scripts/manage_execution_state.py'


class AuthoringCLIIntegrationTests(AuthoringFixture):
    def run_cli(self, command, *args, expected=0):
        result = subprocess.run([sys.executable, str(CLI), command, *map(str, args), '--output-format', 'json-v1'], capture_output=True, text=True)
        self.assertEqual(expected, result.returncode, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        from scripts.validate_prodcraft import validate_protocol_result_instance
        errors = []
        validate_protocol_result_instance('execution-authoring-result', payload, errors)
        self.assertEqual([], errors)
        return payload

    def prepare_draft(self):
        # Request documents live outside the excluded closed evidence bundle.
        route_input = self.repo / 'route-input.json'
        route_input.write_text(json.dumps(self.route))
        binding = copy.deepcopy(self.state['artifact_bindings'][0])
        for key in ('recorded_sequence', 'artifact', 'assurance'):
            binding.pop(key)
        binding_input = self.repo / 'initial-binding.json'
        binding_input.write_text(json.dumps(binding))
        for name in ('route-decision.r1.json', 'verification-record.json', 'test-output.txt'):
            (self.control / name).unlink()
        drafted = self.run_cli('route-draft', '--repo-root', self.repo, '--work-id', 'work-1', '--route-input', route_input)
        self.assertEqual('candidate', drafted['status'])
        self.assertFalse((self.control / 'execution-state.json').exists())
        draft_bytes = (self.control / 'route-decision.r1.draft.json').read_bytes()
        common = ['--repo-root', self.repo, '--work-id', 'work-1', '--initial-binding', binding_input, '--transition-reason', 'Approved path']
        return common, drafted, draft_bytes

    def prepare_initial(self):
        common, drafted, draft_bytes = self.prepare_draft()
        invalid = self.run_cli('state-init', *common, '--approved-route-digest', 'sha256:' + '0' * 64, expected=1)
        self.assertEqual([], invalid['mutations'])
        self.assertFalse((self.control / 'execution-state.json').exists())
        self.run_cli('state-init', *common, '--approved-route-digest', drafted['candidate_route_digest'])
        self.assertEqual(draft_bytes, (self.control / 'route-decision.r1.json').read_bytes())
        self.assertFalse((self.control / 'route-decision.r1.draft.json').exists())
        return self.control / 'execution-state.json'

    def test_native_cli_initialization_revision_and_pin_boundaries(self):
        state_path = self.prepare_initial()
        before = state_path.read_bytes()
        for pin, revision in (('sha256:' + '0' * 64, 2), (self.route['route_digest'], 1)):
            bad = self.run_cli('transition', '--state', state_path, '--expected-revision', revision, '--approved-route-digest', pin, '--target', 'gated', '--reason', 'Next', expected=1)
            self.assertEqual('invalid', bad['status'])
            self.assertEqual([], bad['mutations'])
            self.assertEqual(before, state_path.read_bytes())
        good = self.run_cli('transition', '--state', state_path, '--expected-revision', 2, '--approved-route-digest', self.route['route_digest'], '--target', 'gated', '--reason', 'Next')
        self.assertEqual(3, good['state_revision'])
        self.assertEqual('written', good['status'])
        self.assertEqual(len(state_path.read_bytes()), good['capacities'][0]['used_bytes'])

    def test_draft_rejects_missing_approval_evidence(self):
        route_input = self.repo / 'route-input.json'
        route_input.write_text(json.dumps(self.route))
        (self.control / 'route-decision.r1.json').unlink()
        (self.control / 'route-approval.json').unlink()
        bad = self.run_cli('route-draft', '--repo-root', self.repo, '--work-id', 'work-1', '--route-input', route_input, expected=1)
        self.assertEqual('invalid', bad['status'])
        self.assertIsNone(bad['candidate_route_digest'])
        self.assertFalse((self.control / 'route-decision.r1.draft.json').exists())

    def test_initialization_rejects_intermediate_symlink(self):
        route_input = self.repo / 'route-input.json'
        route_input.write_text(json.dumps(self.route))
        (self.control.parent / 'alias').symlink_to(self.control, target_is_directory=True)
        bad = self.run_cli('route-draft', '--repo-root', self.repo, '--work-id', 'alias', '--route-input', route_input, expected=1)
        self.assertIn('symlink', ' '.join(bad['errors']))

    def test_concurrent_cli_writer_cannot_mutate_locked_work(self):
        from scripts.manage_execution_state import locked_work
        state_path = self.prepare_initial()
        before = state_path.read_bytes()
        with locked_work(self.repo.resolve(), self.control.resolve()):
            rejected = self.mutate(state_path, 'transition', '--target', 'gated',
                                   '--reason', 'Concurrent writer', expected=1)
        self.assertEqual([], rejected['mutations'])
        self.assertIn('holds this work lock', ' '.join(rejected['errors']))
        self.assertEqual(before, state_path.read_bytes())
        accepted = self.mutate(state_path, 'transition', '--target', 'gated', '--reason', 'Retry current revision')
        self.assertEqual('written', accepted['status'])

    def test_document_capacity_warns_at_twelve_mib_and_rejects_over_sixteen(self):
        from tools.execution_result import WARNING_BYTES, LIMIT_BYTES
        from scripts.manage_execution_state import execute, parser
        from scripts.validate_prodcraft import validate_protocol_result_instance
        state_path = self.prepare_initial()
        def with_reason(target, reason):
            # Exercise real CLI argument parsing and execution in-process;
            # operating systems cannot pass a multi-MiB single argv value.
            args = parser().parse_args(['transition', '--state', str(state_path),
                '--expected-revision', str(json.loads(state_path.read_text())['state_revision']),
                '--approved-route-digest', self.route['route_digest'], '--target', target,
                '--reason', reason, '--output-format', 'json-v1'])
            result = execute(args)
            errors = []
            validate_protocol_result_instance('execution-authoring-result', result, errors)
            self.assertEqual([], errors)
            return result
        before = state_path.read_bytes()
        # A real, schema-valid transition reason exercises serialization,
        # candidate validation, materialization and the public result envelope.
        result = with_reason('gated', 'x' * (WARNING_BYTES - len(before) + 2000))
        self.assertTrue(result['warnings'])
        self.assertGreaterEqual(result['capacities'][0]['used_bytes'], WARNING_BYTES)
        self.assertEqual(len(state_path.read_bytes()), result['capacities'][0]['used_bytes'])
        before = state_path.read_bytes()
        result = with_reason('executing', 'x' * (LIMIT_BYTES - len(before) + 2000))
        self.assertEqual('invalid', result['status'])
        self.assertEqual([], result['mutations'])
        self.assertIsNone(result['candidate_completion_digest'])
        self.assertEqual(before, state_path.read_bytes())

    def mutate(self, state_path, operation, *args, expected=0):
        state = json.loads(state_path.read_text())
        return self.run_cli(operation, '--state', state_path,
            '--expected-revision', state['state_revision'],
            '--approved-route-digest', self.route['route_digest'], *args, expected=expected)

    def prepare_verification(self, attempt):
        from tools.execution_state import capture_git_worktree, file_sha256
        evidence_ref = f'test-output-{attempt}.txt'
        evidence_id = f'focused-tests-{attempt}'
        self.write(evidence_ref, f'Accepted regression evidence {attempt}\n', raw=True)
        bindings = self.repo / f'evidence-bindings-{attempt}.json'
        bindings.write_text(json.dumps({'evidence_bindings': [{
            'evidence_id': evidence_id, 'local_ref': evidence_ref,
            'sha256': file_sha256(self.control / evidence_ref),
        }]}))
        self.work_snapshot = capture_git_worktree(self.repo, excluded_control_root=self.control, captured_at='2026-07-10T00:00:00Z')
        verification = self.make_verification()
        verification['evidence_refs'][0]['id'] = evidence_id
        verification['checks_run'][0]['evidence_ref'] = evidence_id
        if self.work_snapshot['status'] == 'dirty':
            verification['work_state_ref']['diff_ref'] = self.work_snapshot['content_digest']
        verification_ref = f'verification-{attempt}.json'
        self.write(verification_ref, verification)
        return verification_ref, bindings

    def test_three_core_paths_complete_without_manual_derived_fields(self):
        state_path = self.prepare_initial()
        for target in ('gated', 'executing', 'blocked', 'executing'):
            self.mutate(state_path, 'transition', '--target', target, '--reason', 'Approved step')
        for kind in ('entered', 'exited'):
            self.mutate(state_path, 'phase-event', '--kind', kind, '--phase-index', 0)
        first_ref, first_bindings = self.prepare_verification(1)
        self.mutate(state_path, 'claim-completion', '--verification-record-ref', first_ref,
                    '--evidence-bindings', first_bindings, '--reason', 'Claim ready')
        immutable_verification = (self.control / first_ref).read_bytes()
        self.mutate(state_path, 'record-outcome', '--outcome', 'rejected', '--reason', 'Require independent fresh evidence')
        for target in ('gated', 'executing'):
            self.mutate(state_path, 'transition', '--target', target, '--reason', 'Retry approved')
        before = state_path.read_bytes()
        reused = self.mutate(state_path, 'claim-completion', '--verification-record-ref', first_ref,
                    '--evidence-bindings', first_bindings, '--reason', 'Retry stale evidence', expected=1)
        self.assertEqual('invalid', reused['status'])
        self.assertEqual(before, state_path.read_bytes())
        second_ref, second_bindings = self.prepare_verification(2)
        self.mutate(state_path, 'claim-completion', '--verification-record-ref', second_ref,
                    '--evidence-bindings', second_bindings, '--reason', 'Independent evidence ready')
        verified = self.mutate(state_path, 'record-outcome', '--outcome', 'verified', '--reason', 'Review accepted')
        self.assertEqual('candidate', verified['status'])
        self.assertIsNotNone(verified['candidate_completion_digest'])
        before = state_path.read_bytes()
        missing = self.mutate(state_path, 'record-outcome', '--outcome', 'completed', '--reason', 'Finalize', expected=1)
        self.assertEqual([], missing['mutations'])
        self.assertEqual(before, state_path.read_bytes())
        completed = self.mutate(state_path, 'record-outcome', '--outcome', 'completed',
            '--approved-completion-digest', verified['candidate_completion_digest'], '--reason', 'Finalize accepted work')
        self.assertNotEqual(verified['candidate_completion_digest'], completed['candidate_completion_digest'])
        from tools.execution_validation import authorize_execution_state, ValidationDisposition
        errors = []
        authorized = authorize_execution_state(state_path, self.route['route_digest'], completed['candidate_completion_digest'], errors)
        self.assertEqual([], errors)
        self.assertEqual(ValidationDisposition.VALID, authorized.disposition)
        self.assertEqual('terminal-authorized', authorized.authority)
        self.assertEqual(immutable_verification, (self.control / first_ref).read_bytes())
        (self.repo / 'app.txt').write_text('unreviewed change\n')
        errors = []
        stale = authorize_execution_state(state_path, self.route['route_digest'], completed['candidate_completion_digest'], errors)
        self.assertEqual(ValidationDisposition.INVALID, stale.disposition)

    def test_claim_rejects_failed_or_incomplete_verification_without_mutation(self):
        state_path = self.prepare_initial()
        for target in ('gated', 'executing'):
            self.mutate(state_path, 'transition', '--target', target, '--reason', 'Proceed')
        for kind in ('entered', 'exited'):
            self.mutate(state_path, 'phase-event', '--kind', kind, '--phase-index', 0)
        ref, bindings = self.prepare_verification(1)
        valid = json.loads((self.control / ref).read_text())
        before = state_path.read_bytes()
        for field, value in [('claim_may_be_made', False), ('remaining_unverified', ['UI behavior']), ('failed', ['focused tests'])]:
            bad = copy.deepcopy(valid)
            bad[field] = value
            self.write(ref, bad)
            result = self.mutate(state_path, 'claim-completion', '--verification-record-ref', ref,
                '--evidence-bindings', bindings, '--reason', 'Should fail', expected=1)
            self.assertEqual('invalid', result['status'])
            self.assertEqual(before, state_path.read_bytes())

    def test_same_second_verification_keeps_fractional_claim_time(self):
        from scripts.manage_execution_state import execute, parser
        state_path = self.prepare_initial()
        for target in ('gated', 'executing'):
            self.mutate(state_path, 'transition', '--target', target, '--reason', 'Proceed')
        for kind in ('entered', 'exited'):
            self.mutate(state_path, 'phase-event', '--kind', kind, '--phase-index', 0)
        ref, bindings = self.prepare_verification(1)
        verification = json.loads((self.control / ref).read_text())
        verification['work_state_ref']['captured_at'] = '2026-09-11T00:00:00.250000Z'
        verification['evidence_refs'][0]['captured_at'] = '2026-09-11T00:00:00.300000Z'
        verification['verified_at'] = '2026-09-11T00:00:00.400000Z'
        self.write(ref, verification)
        args = parser().parse_args(['claim-completion', '--state', str(state_path),
            '--expected-revision', str(json.loads(state_path.read_text())['state_revision']),
            '--approved-route-digest', self.route['route_digest'],
            '--verification-record-ref', ref, '--evidence-bindings', str(bindings), '--reason', 'Fresh verification'])
        # Replace only the external clock; real candidate and freshness checks run.
        with mock.patch('scripts.manage_execution_state.datetime') as clock:
            clock.now.return_value = datetime(2026, 9, 11, 0, 0, 0, 500000, tzinfo=timezone.utc)
            result = execute(args)
        self.assertEqual('written', result['status'], result['errors'])
        attempt = json.loads(state_path.read_text())['completion_attempts'][0]
        self.assertEqual('2026-09-11T00:00:00.500000Z', attempt['claimed_at'])
