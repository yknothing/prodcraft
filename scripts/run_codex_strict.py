#!/usr/bin/env python3
"""Run an ephemeral Codex work item and enforce completion outside the model.

Native turn completion is not business-work completion. This parent process
accepts only the canonical completed state, fresh evidence and explicit pins.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys

if __name__ == "__main__":
    # Installed runtime files are immutable, including during isolated startup.
    sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tools.host_completion import completion_status, display_status, presentation_locale
from tools.execution_state import load_strict_json, read_protocol_file, resolve_authority_context


def run(args):
    state = args.state.absolute()
    initial = load_strict_json(state)
    context, errors = resolve_authority_context(state, initial)
    if errors or context is None:
        raise ValueError('; '.join(errors))
    if context.repo_root == ROOT or ROOT in context.repo_root.parents or context.repo_root in ROOT.parents:
        raise ValueError('strict host work must be separate from the trusted Prodcraft runtime checkout')
    prompt = getattr(args, 'prompt_text', None)
    if prompt is None:
        prompt = read_protocol_file(args.prompt_file.absolute()).decode('utf-8')
    locale = presentation_locale(prompt, args.locale)
    initial_status = completion_status(state, args.approved_route_digest, args.approved_completion_digest)
    if initial_status['status'] == 'invalid':
        return {**initial_status, 'schema_version': 'codex-strict-run.v1', 'native_exit_code': None,
                'response': '', 'native_events': [], 'usage': None, 'presentation_locale': locale}
    executable = shutil.which(args.codex)
    if not executable:
        raise ValueError('Codex executable was not found')
    python = sys.executable
    manage = ROOT / 'scripts/manage_execution_state.py'
    context_text = (
        f'This is a Prodcraft strict work item. Canonical state: {state}\n'
        f'Trusted authoring command: {python} -I {manage}\n'
        f'Externally approved route pin: {args.approved_route_digest}\n'
        'Use that command for state transitions, phase checkpoints, artifact bindings, completion '
        'claims and reviewer outcomes. Never edit derived state fields directly. Read the current '
        'revision before each command. A candidate digest does not grant approval. If an operator '
        'pin is needed, report the pending candidate and pause; do not invent or auto-forward approval. '
        'A blocked or approval-pending run is not completed. The parent validates completion after '
        'you stop. Match the user request language for prose, headings and human-facing labels, '
        'preserving machine identifiers, commands and raw diagnostics.\n'
    )
    if args.approved_completion_digest is not None:
        context_text += f'Externally supplied completion pin: {args.approved_completion_digest}\n'
    mode = 'read-only' if initial_status['lifecycle_state'] == 'completed' else 'workspace-write'
    command = [executable, 'exec', '--ignore-user-config', '--ignore-rules', '--ephemeral', '--json',
               '--sandbox', mode, '-c', 'approval_policy="never"', '-C', str(context.repo_root)]
    # Git's lock/journal location is outside the excluded control bundle. Grant
    # only that operational directory, not general write access to Git metadata.
    git = subprocess.run(['git', '-C', str(context.repo_root), 'rev-parse', '--git-common-dir'],
                         capture_output=True, text=True, check=True, timeout=30,
                         env={key: value for key, value in os.environ.items() if not key.startswith('GIT_')})
    common = Path(git.stdout.strip())
    if not common.is_absolute():
        common = context.repo_root / common
    operational = common.resolve(strict=True) / 'prodcraft-authoring'
    if mode == 'workspace-write':
        if operational.is_symlink() or not operational.is_dir():
            raise ValueError('initialize the work item through the authoring CLI before launching the host')
        command.extend(['--add-dir', str(operational)])
    if args.model:
        command.extend(['--model', args.model])
    command.append('-')
    # Terminate the entire native process group on timeout, including tool
    # children, before evaluating or returning the result to the operator.
    with subprocess.Popen(command, cwd=context.repo_root, text=True,
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, start_new_session=True) as process:
        try:
            language = 'Chinese' if locale == 'zh-CN' else 'English'
            native_prompt = context_text + '\nUser request:\n' + prompt + (
                f'\nPresentation for this request: use {language} for all user-facing prose, '
                'including progress messages, headings and human-facing status labels. '
                'Keep code, paths, canonical field names/enums and raw diagnostics unchanged.\n')
            stdout, stderr = process.communicate(native_prompt,
                                                 timeout=args.timeout)
        except BaseException:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.communicate()
            raise
        native = subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
    events = []
    for line in native.stdout.splitlines():
        try:
            event = json.loads(line)
            if isinstance(event, dict):
                events.append(event)
        except ValueError:
            continue
    completed = next((item for item in reversed(events) if item.get('type') == 'turn.completed'), None)
    responses = [item['item']['text'] for item in events if item.get('type') == 'item.completed'
                 and isinstance(item.get('item'), dict) and item['item'].get('type') == 'agent_message']
    # A verified-state pin may authorize its completed transition, but the
    # resulting completed state always needs separate operator confirmation.
    # Keep the parent input immutable and return the new candidate unapproved.
    final = completion_status(state, args.approved_route_digest, args.approved_completion_digest)
    if initial_status['lifecycle_state'] != 'completed' and final['lifecycle_state'] == 'completed':
        final = completion_status(state, args.approved_route_digest, None)
    if native.returncode != 0 or completed is None:
        native_errors = [str(item.get('error', item)) for item in events if item.get('type') in {'turn.failed', 'error'}]
        final = {**final, 'status': 'native-failure', 'authority': None,
                 'errors': [*final['errors'], *(native_errors or [native.stderr.strip()[-2000:] or 'native turn did not complete'])]}
    return {**final, 'schema_version': 'codex-strict-run.v1', 'native_exit_code': native.returncode,
            'response': responses[-1] if responses else '', 'native_events': events,
            'usage': completed.get('usage') if completed else None,
            'model_selection': args.model or 'codex-default', 'presentation_locale': locale}


def main():
    def cancel(signum, frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, cancel)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state', type=Path, required=True)
    parser.add_argument('--approved-route-digest', required=True)
    parser.add_argument('--approved-completion-digest')
    parser.add_argument('--prompt-file', type=Path, required=True)
    parser.add_argument('--codex', default='codex')
    parser.add_argument('--model')
    parser.add_argument('--locale', choices=('en', 'zh-CN'), help='override automatic English/Chinese presentation selection')
    parser.add_argument('--timeout', type=int, default=300)
    parser.add_argument('--output-format', choices=('text', 'json'), default='text')
    args = parser.parse_args()
    try:
        args.prompt_text = read_protocol_file(args.prompt_file.absolute()).decode('utf-8')
        args.locale = presentation_locale(args.prompt_text, args.locale)
        result = run(args)
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        result = {'schema_version': 'codex-strict-run.v1', 'status': 'invalid', 'authority': None,
                  'errors': [str(exc)], 'candidate_completion_digest': None,
                  'native_exit_code': None, 'response': '', 'presentation_locale': args.locale or 'en'}
    if args.output_format == 'json':
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(display_status(result, args.locale or result.get('presentation_locale', 'en')))
        if result.get('response'):
            print(result['response'])
        if result.get('candidate_completion_digest'):
            print('candidate_completion_digest: ' + result['candidate_completion_digest'])
    return 0 if result['status'] == 'completed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
