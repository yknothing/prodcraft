from __future__ import annotations

import json
import copy
import os
from pathlib import Path
import subprocess
import signal
import sys
import tempfile
import time
from unittest import mock

from tests.test_execution_authoring import AuthoringFixture
from tools.host_completion import completion_status, display_status, presentation_locale
from tools.execution_state import terminal_authority_digest

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / 'scripts/run_codex_strict.py'


class HostCompletionTests(AuthoringFixture):
    def check(self, pin=None):
        path = self.write('execution-state.json', self.state)
        return completion_status(path, self.route['route_digest'], pin)

    def test_requires_fresh_completed_state_and_explicit_pin(self):
        pending = self.check()
        self.assertEqual('approval-required', pending['status'])
        self.assertIsNone(pending['authority'])
        pin = terminal_authority_digest(self.state)
        self.assertEqual('completed', self.check(pin)['status'])
        self.assertEqual('invalid', self.check('sha256:' + '0' * 64)['status'])
        (self.repo / 'app.txt').write_text('unreviewed change\n')
        self.assertEqual('invalid', self.check(pin)['status'])

    def test_human_labels_follow_explicit_locale_preserving_diagnostics(self):
        result = {'status': 'approval-required', 'errors': ['execution-state.json']}
        self.assertIn('awaiting operator approval', display_status(result, 'en'))
        self.assertIn('\u7b49\u5f85\u5916\u90e8\u786e\u8ba4', display_status(result, 'zh-CN'))
        self.assertIn('execution-state.json', display_status(result, 'zh-CN'))

    def test_prompt_locale_ignores_code_and_honors_explicit_selection(self):
        self.assertEqual('en', presentation_locale('Fix the login validation bug.'))
        self.assertEqual('zh-CN', presentation_locale('\u8bf7\u4fee\u590d login validation \u4e2d\u7684\u4e00\u4e2a\u7f3a\u9677\u3002'))
        self.assertEqual('zh-CN', presentation_locale('Fix the bug. Please respond in Chinese.'))
        self.assertEqual('en', presentation_locale('\u8bf7\u4fee\u590d\u767b\u5f55\u7f3a\u9677\u3002 Please respond in English.'))
        self.assertEqual('en', presentation_locale('Fix it. `\u4e2d\u6587\u5185\u5bb9\u4e0d\u9009\u8bed\u8a00`'))
        self.assertEqual('zh-CN', presentation_locale('> Reply in English\n\u8bf7\u4fee\u590d\u8fd9\u4e2a\u767b\u5f55\u7f3a\u9677\u3002'))
        self.assertEqual('en', presentation_locale('\u8bf7\u4fee\u590d\u767b\u5f55\u7f3a\u9677\u3002', 'en'))
        self.assertEqual('en', presentation_locale('\u8bf7\u4fee\u590d\u767b\u5f55\u7f3a\u9677\u3002\u7528\u82f1\u6587\u56de\u590d\u3002'))
        self.assertEqual('zh-CN', presentation_locale('Fix the bug. Use Chinese for all user-facing prose.'))
        self.assertEqual('zh-CN', presentation_locale('  > Reply in English\n\u8bf7\u4fee\u590d\u8fd9\u4e2a\u767b\u5f55\u7f3a\u9677\u3002'))

    def test_concurrent_state_change_cannot_mix_lifecycle_and_authority(self):
        path = self.write('execution-state.json', self.state)
        from tools.execution_state import file_sha256
        def change_then_hash(target):
            # Inject an actual external file change; authority evaluation and
            # its evidence checks execute unchanged before this boundary.
            current = json.loads(target.read_text())
            current['lifecycle_state'] = 'verified'
            target.write_text(json.dumps(current))
            return file_sha256(target)
        with mock.patch('tools.host_completion.file_sha256', side_effect=change_then_hash):
            result = completion_status(path, self.route['route_digest'], terminal_authority_digest(self.state))
        self.assertEqual('invalid', result['status'])
        self.assertIsNone(result['authority'])
        self.assertIn('changed during', result['errors'][0])

    def test_aba_change_cannot_mix_candidate_or_approved_digest_with_another_snapshot(self):
        from tools.execution_state import file_sha256, load_strict_json_with_digest
        path = self.write('execution-state.json', self.state)
        valid_bytes = path.read_bytes()
        changed = copy.deepcopy(self.state)
        changed['lifecycle_state'] = 'verified'
        changed_bytes = json.dumps(changed).encode()
        def read_then_swap(target):
            payload = load_strict_json_with_digest(target)
            target.write_bytes(valid_bytes)
            return payload
        def restore_then_hash(target):
            target.write_bytes(changed_bytes)
            return file_sha256(target)
        for pin in (None, terminal_authority_digest(self.state)):
            path.write_bytes(changed_bytes)
            # Real file swaps at I/O boundaries; no authority result is mocked.
            with mock.patch('tools.host_completion.load_strict_json_with_digest', side_effect=read_then_swap), \
                 mock.patch('tools.host_completion.file_sha256', side_effect=restore_then_hash):
                result = completion_status(path, self.route['route_digest'], pin)
            self.assertEqual('invalid', result['status'])
            self.assertIsNone(result['authority'])
            self.assertIsNone(result['candidate_completion_digest'])

    def run_external_host(self, *, pin=None, succeeds=True):
        # The dependency is the native host process. Its successful turn cannot
        # substitute for the real protocol validator, which remains unmocked.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            binary = root / 'native-host'
            event = {'type': 'turn.completed', 'usage': {'input_tokens': 1, 'output_tokens': 1}} if succeeds else {'type': 'turn.failed', 'error': {'message': 'host unavailable'}}
            binary.write_text('#!' + sys.executable + '\nimport json, sys\nassert "--ignore-rules" in sys.argv\nassert "--ignore-user-config" in sys.argv\nassert "--sandbox" in sys.argv\nprint(' + repr(json.dumps({'type':'item.completed','item':{'type':'agent_message','text':'Done'}})) + ')\nprint(' + repr(json.dumps(event)) + ')\n')
            os.chmod(binary, 0o700)
            prompt = root / 'prompt.txt'
            prompt.write_text('Report the status.\n')
            state = self.write('execution-state.json', self.state)
            # Initial state-init always creates this operational directory.
            (self.repo / '.git/prodcraft-authoring').mkdir(exist_ok=True)
            command = [sys.executable, str(RUNNER), '--state', str(state), '--approved-route-digest', self.route['route_digest'], '--prompt-file', str(prompt), '--codex', str(binary), '--output-format', 'json']
            if pin is not None:
                command.extend(['--approved-completion-digest', pin])
            result = subprocess.run(command, capture_output=True, text=True)
            return result.returncode, json.loads(result.stdout)

    def test_native_success_or_done_text_never_auto_approves_a_candidate(self):
        code, result = self.run_external_host()
        self.assertEqual(1, code)
        self.assertEqual('Done', result['response'])
        self.assertEqual('approval-required', result['status'])
        self.assertIsNone(result['authority'])
        code, result = self.run_external_host(pin=terminal_authority_digest(self.state))
        self.assertEqual(0, code)
        self.assertEqual('terminal-authorized', result['authority'])

    def test_native_failure_never_reports_success_despite_valid_state(self):
        code, result = self.run_external_host(pin=terminal_authority_digest(self.state), succeeds=False)
        self.assertEqual(1, code)
        self.assertEqual('native-failure', result['status'])
        self.assertIsNone(result['authority'])

    def test_unchanged_verified_state_does_not_request_its_approved_pin_again(self):
        from tests.test_execution_authoring import AuthoringTests
        from tools.execution_authoring import record_outcome
        fixture = AuthoringTests()
        fixture.setUp()
        try:
            fixture.state = record_outcome(fixture.claim(), fixture.route, 7,
                'verified', 'Reviewed', '2026-07-10T00:03:00Z')
            code, result = HostCompletionTests.run_external_host(fixture, pin=terminal_authority_digest(fixture.state))
            self.assertEqual(1, code)
            self.assertEqual('incomplete', result['status'])
            self.assertIsNone(result['authority'])
        finally:
            fixture.tearDown()

    def test_startup_failure_keeps_the_prompt_language_and_raw_diagnostic(self):
        state = self.write('execution-state.json', self.state)
        with tempfile.TemporaryDirectory() as directory:
            prompt = Path(directory) / 'prompt.txt'
            prompt.write_text('\u8bf7\u68c0\u67e5\u5b8c\u6210\u72b6\u6001\u3002\n')
            result = subprocess.run([sys.executable, str(RUNNER), '--state', str(state),
                '--approved-route-digest', self.route['route_digest'],
                '--approved-completion-digest', terminal_authority_digest(self.state),
                '--prompt-file', str(prompt), '--codex', str(Path(directory) / 'unavailable')],
                text=True, capture_output=True)
        self.assertEqual(1, result.returncode)
        self.assertIn('\u5b8c\u6210\u9a8c\u6536\u672a\u901a\u8fc7', result.stdout)
        self.assertIn('Codex executable was not found', result.stdout)

    def test_timeout_and_cancellation_stop_native_tool_children(self):
        state = self.write('execution-state.json', self.state)
        pin = terminal_authority_digest(self.state)
        for cancellation in (None, signal.SIGINT, signal.SIGTERM):
            with self.subTest(cancellation=cancellation), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                ready, sentinel = root / 'ready', root / 'late-write'
                child_ready, release = root / 'child-ready', root / 'release'
                binary, prompt = root / 'native-host', root / 'prompt.txt'
                child = ('import time\nfrom pathlib import Path\n'
                    + f'Path({str(child_ready)!r}).write_text("ready")\n'
                    + f'while not Path({str(release)!r}).exists():\n    time.sleep(0.01)\n'
                    + f'Path({str(sentinel)!r}).write_text("late")\n')
                binary.write_text('#!' + sys.executable + '\nimport os, subprocess, sys, time\nfrom pathlib import Path\n'
                    + f'subprocess.Popen([sys.executable, "-c", {child!r}])\n'
                    + f'Path({str(ready)!r}).write_text(str(os.getpid()))\ntime.sleep(30)\n')
                binary.chmod(0o700)
                prompt.write_text('Inspect status only.\n')
                command = [sys.executable, str(RUNNER), '--state', str(state),
                    '--approved-route-digest', self.route['route_digest'], '--approved-completion-digest', pin,
                    '--prompt-file', str(prompt), '--codex', str(binary), '--timeout', '5', '--output-format', 'json']
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                try:
                    deadline = time.monotonic() + 10
                    while not (ready.exists() and child_ready.exists()) and process.poll() is None and time.monotonic() < deadline:
                        time.sleep(0.02)
                    if not (ready.exists() and child_ready.exists()):
                        stdout, stderr = process.communicate(timeout=5)
                        self.fail('native host did not become ready: ' + stdout + stderr)
                    if cancellation is not None:
                        process.send_signal(cancellation)
                    process.communicate(timeout=10)
                    self.assertNotEqual(0, process.returncode)
                    release.write_text('release after parent termination')
                    time.sleep(1)
                    self.assertFalse(sentinel.exists(), 'native child continued after the strict runner stopped')
                finally:
                    if ready.exists():
                        try:
                            os.killpg(int(ready.read_text()), signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                    if process.poll() is None:
                        process.kill()
                    process.communicate()
