from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from tests import test_execution_authoring_cli as cli_fixture
from tests.test_execution_authoring import AuthoringFixture

ROOT = Path(__file__).resolve().parents[1]


class AuthoringRecoveryTests(AuthoringFixture):
    run_cli = cli_fixture.AuthoringCLIIntegrationTests.run_cli
    prepare_draft = cli_fixture.AuthoringCLIIntegrationTests.prepare_draft

    def crash_init(self, crash_path):
        common, drafted, draft_bytes = self.prepare_draft()
        arguments = ['state-init', *map(str, common), '--approved-route-digest', drafted['candidate_route_digest'], '--output-format', 'json-v1']
        # Fault injection at the OS dependency. The actual link has completed;
        # exiting the process bypasses all application finally/cleanup handlers.
        program = '''
import os,sys
from pathlib import Path
from scripts import manage_execution_state as cli
original_link = os.link
crash_path = sys.argv.pop(1)
def crash_after_link(source, target, **kwargs):
    original_link(source, target, **kwargs)
    if Path(target).name == crash_path:
        os._exit(73)
os.link = crash_after_link
sys.exit(cli.main())
'''
        result = subprocess.run([sys.executable, '-c', program, crash_path, *arguments], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(73, result.returncode, result.stderr + result.stdout)
        return common, drafted, draft_bytes

    def test_post_selector_crash_recovers_as_written_with_proven_mutations(self):
        common, drafted, draft_bytes = self.crash_init('execution-state.json')
        result = self.run_cli('state-init', *common, '--approved-route-digest', drafted['candidate_route_digest'])
        self.assertEqual('written', result['status'])
        self.assertEqual(2, result['state_revision'])
        self.assertTrue(result['mutations'])
        self.assertFalse((self.control / 'route-decision.r1.draft.json').exists())
        self.assertEqual(draft_bytes, (self.control / 'route-decision.r1.json').read_bytes())
        self.assertEqual([], list(self.control.glob('.prodcraft-write-*')))
        self.assertEqual([], list((self.repo / '.git/prodcraft-authoring').glob('*.json')))

    def test_pre_selector_crash_recovers_then_initializes_without_orphaned_files(self):
        common, drafted, _ = self.crash_init('route-decision.r1.json')
        self.assertFalse((self.control / 'execution-state.json').exists())
        result = self.run_cli('state-init', *common, '--approved-route-digest', drafted['candidate_route_digest'])
        self.assertEqual('written', result['status'])
        self.assertEqual([], list(self.control.glob('.prodcraft-write-*')))

    def test_changed_successor_requires_manual_review_without_deleting_draft(self):
        common, drafted, _ = self.crash_init('execution-state.json')
        path = self.control / 'execution-state.json'
        changed = path.read_bytes() + b'\n'
        path.write_bytes(changed)
        result = self.run_cli('state-init', *common, '--approved-route-digest', drafted['candidate_route_digest'], expected=1)
        self.assertEqual('recovery-required', result['status'])
        self.assertIsNone(result['candidate_route_digest'])
        self.assertEqual(changed, path.read_bytes())
        self.assertTrue((self.control / 'route-decision.r1.draft.json').exists())
