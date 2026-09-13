#!/usr/bin/env python3
"""Author a local v1 execution bundle using explicit review pins."""
from __future__ import annotations

import argparse
import base64
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import yaml
from tools import execution_authoring as authoring
from tools.execution_result import LIMIT_BYTES, authoring_result
from tools.execution_state import (
    FilesystemControlBundleIO, WorktreeSnapshotError, capture_git_worktree,
    canonical_json_bytes, file_sha256, load_strict_json, parse_strict_json_bytes,
    read_protocol_file, resolve_authority_context, resolve_control_ref,
    validate_execution_state_contract,
)
from tools.execution_validation import (
    CandidateBundleView, ValidationDisposition, authorize_execution_state,
    validate_completion_preflight, validate_execution_candidate,
    validate_registered_artifact_payload, validate_route_contract_from_repository,
)

STATE = 'execution-state.json'
ROUTE = 'route-decision.r1.json'
DRAFT = 'route-decision.r1.draft.json'
PIN = re.compile(r'^sha256:[0-9a-f]{64}$')
WORK_ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$')


class RecoveryRequired(ValueError):
    pass


def check_pin(pin):
    if not isinstance(pin, str) or not PIN.fullmatch(pin):
        raise ValueError('an explicit sha256 operator pin is required')


def safe_directory(path: Path, *, create=False):
    if create:
        try:
            path.mkdir(mode=0o700)
        except FileExistsError:
            pass
    metadata = path.lstat()
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise ValueError(f'directory must not be a symlink or special file: {path}')


def git_value(root, *arguments):
    environment = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
    result = subprocess.run(['git', '-C', str(root), *arguments], capture_output=True,
                            text=True, timeout=30, env=environment)
    if result.returncode:
        raise ValueError(result.stderr.strip() or 'Git context unavailable')
    return result.stdout.strip()


def initial_context(repo, work_id):
    if not WORK_ID.fullmatch(work_id or ''):
        raise ValueError('unsafe work_id')
    supplied = Path(repo).absolute()
    safe_directory(supplied)
    root = Path(git_value(supplied, 'rev-parse', '--show-toplevel')).resolve(strict=True)
    if supplied.resolve(strict=True) != root:
        raise ValueError('--repo-root must identify the Git worktree root')
    control = root
    for part in ('.prodcraft', 'artifacts', work_id):
        control /= part
        safe_directory(control, create=True)
    return root, control


def fsync_directory(directory):
    fd = os.open(directory, os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0))
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic_write(path, content, *, create=False, temporary_path=None):
    # Destination-local temporary keeps the final link/replace on one filesystem.
    temporary = None
    try:
        if temporary_path is None:
            handle = tempfile.NamedTemporaryFile(dir=path.parent, prefix='.prodcraft-write-', delete=False)
            temporary = Path(handle.name)
        else:
            fd = os.open(temporary_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o600)
            temporary = temporary_path
            handle = os.fdopen(fd, 'wb')
        with handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        if create:
            os.link(temporary, path, follow_symlinks=False)
        else:
            os.replace(temporary, path)
        if temporary.exists():
            temporary.unlink()
        fsync_directory(path.parent)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def sha_bytes(content):
    return 'sha256:' + hashlib.sha256(content).hexdigest()


def optional_bytes(path):
    try:
        path.lstat()
    except FileNotFoundError:
        return None
    return read_protocol_file(path)


@contextmanager
def locked_work(root, control):
    try:
        import fcntl
    except ImportError as exc:
        raise ValueError('local advisory locking is required on this platform') from exc
    common = Path(git_value(root, 'rev-parse', '--git-common-dir'))
    if not common.is_absolute():
        common = root / common
    common = common.resolve(strict=True)
    directory = common / 'prodcraft-authoring'
    safe_directory(directory, create=True)
    key = hashlib.sha256(str(control).encode('utf-8')).hexdigest()
    lock_path = directory / (key + '.lock')
    fd = os.open(lock_path, os.O_RDWR | os.O_CREAT | os.O_NONBLOCK | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode) or os.fstat(fd).st_nlink != 1:
            raise ValueError('authoring lock must be a single regular file')
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ValueError('another local authoring operation holds this work lock; retry with the current revision') from exc
        yield directory / (key + '.json')
    finally:
        os.close(fd)


def read_journal(path):
    # Two individually bounded documents, base64 encoded, plus a small manifest.
    fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | getattr(os, 'O_NOFOLLOW', 0))
    with os.fdopen(fd, 'rb') as handle:
        metadata = os.fstat(handle.fileno())
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > 48 * 1024 * 1024:
            raise RecoveryRequired('invalid initialization journal size or file type')
        content = handle.read(48 * 1024 * 1024 + 1)
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise RecoveryRequired('duplicate initialization journal key')
            result[key] = value
        return result
    payload = json.loads(content, object_pairs_hook=unique)
    if set(payload) != {'version', 'control_root', 'draft_sha256', 'documents', 'initially_absent'} or payload['version'] != 'prodcraft-state-init.v1' or payload['initially_absent'] != [ROUTE, STATE]:
        raise RecoveryRequired('invalid initialization journal contract')
    if set(payload['documents']) != {ROUTE, STATE}:
        raise RecoveryRequired('invalid initialization journal document set')
    documents = {}
    for name, encoded in payload['documents'].items():
        documents[name] = base64.b64decode(encoded, validate=True)
        parse_strict_json_bytes(documents[name], Path(name))
    if sha_bytes(documents[ROUTE]) != payload['draft_sha256']:
        raise RecoveryRequired('initialization journal route/draft mismatch')
    return payload, documents


def validate_materialized(root, control):
    state = load_strict_json(control / STATE)
    route = load_strict_json(resolve_control_ref(control, state['route_binding']['ref']))
    outcome = validate_execution_candidate(
        repo_root=root, control_root=control, state_path=control / STATE,
        state=state, route=route, view=CandidateBundleView(control),
        approved_route_digest=route['route_digest'],
    )
    # Recovery checks consistency only. It does not output gate/terminal authority.
    if outcome.disposition == ValidationDisposition.INVALID:
        raise RecoveryRequired('; '.join(outcome.errors))


def initialization_temporary(control, journal, name):
    return control / f'.prodcraft-write-{journal.stem}-{name}'


def recover_initialization(journal, root, control, mutations, approved_route_digest):
    if not journal.exists() and not journal.is_symlink():
        return None
    try:
        manifest, documents = read_journal(journal)
        if manifest['control_root'] != str(control):
            raise RecoveryRequired('journal belongs to another control root')
        route = parse_strict_json_bytes(documents[ROUTE], control / ROUTE)
        check_pin(approved_route_digest)
        if route['route_digest'] != approved_route_digest:
            raise RecoveryRequired('recovery requires the original reviewed route pin')
        live = {name: optional_bytes(control / name) for name in (ROUTE, STATE, DRAFT)}
        for name in (ROUTE, STATE):
            if live[name] is not None and live[name] != documents[name]:
                raise RecoveryRequired(f'initialization recovery found changed {name}; manual review required')
        if live[DRAFT] is not None and sha_bytes(live[DRAFT]) != manifest['draft_sha256']:
            raise RecoveryRequired('initialization recovery found changed draft; manual review required')
        temporaries = []
        for name in (ROUTE, STATE):
            temporary = initialization_temporary(control, journal, name)
            content = optional_bytes(temporary)
            if content is not None:
                if content != documents[name]:
                    raise RecoveryRequired('initialization temporary content mismatch; manual review required')
                temporaries.append(temporary)
        for temporary in temporaries:
            temporary.unlink()
        prefix = control.relative_to(root).as_posix() + '/'
        if live[STATE] is None:
            if live[DRAFT] is None:
                raise RecoveryRequired('pre-selector initialization lost its reviewed draft')
            if live[ROUTE] is not None:
                (control / ROUTE).unlink()
                mutations.append({'action': 'remove', 'path': prefix + ROUTE})
            fsync_directory(control)
        else:
            if live[ROUTE] is None:
                raise RecoveryRequired('committed initialization has no immutable route')
            # The journal proves both paths were absent and now contain the
            # exact successor. Report the resumed transaction's proven writes.
            mutations.extend({'action': 'create', 'path': prefix + name} for name in (ROUTE, STATE))
            if live[DRAFT] is not None:
                (control / DRAFT).unlink()
                mutations.append({'action': 'remove', 'path': prefix + DRAFT})
            fsync_directory(control)
            validate_materialized(root, control)
        journal.unlink()
        fsync_directory(journal.parent)
        return live[STATE] is not None
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise RecoveryRequired(str(exc)) from exc


def read_input(path):
    content = read_protocol_file(Path(path).absolute())
    if Path(path).suffix.lower() == '.json':
        return parse_strict_json_bytes(content, Path(path))
    class UniqueLoader(yaml.SafeLoader):
        pass
    def mapping(loader, node):
        result = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node)
            if not isinstance(key, str) or key in result:
                raise ValueError('input mapping contains invalid or duplicate keys')
            result[key] = loader.construct_object(value_node)
        return result
    UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
    payload = yaml.load(content, Loader=UniqueLoader)
    if not isinstance(payload, dict):
        raise ValueError('input must be a JSON/YAML object')
    canonical_json_bytes(payload)
    return payload


def evidence_refs(values):
    evidence = []
    for value in values or []:
        ref, separator, digest = value.rpartition('=')
        if not separator:
            raise ValueError('evidence must use REF=SHA256')
        check_pin(digest)
        evidence.append({'ref': ref, 'sha256': digest})
    return evidence


def bundle_identity(control):
    view = FilesystemControlBundleIO(control)
    return {name: view.sha256(name) for name in view.iter_relative_files()}


def validate_route(route, control):
    errors = []
    if validate_registered_artifact_payload(route, control / DRAFT, errors):
        errors.extend(validate_route_contract_from_repository(route, errors))
    if errors:
        raise ValueError('; '.join(errors))
    evidence = route['approval_evidence']
    if file_sha256(resolve_control_ref(control, evidence['ref'])) != evidence['sha256']:
        raise ValueError('route approval evidence content digest mismatch')


def build_change(args, root, control):
    occurred = args.occurred_at or datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    if args.operation == 'route-draft':
        if optional_bytes(control / STATE) is not None or optional_bytes(control / ROUTE) is not None:
            raise ValueError('route-draft requires no live state or immutable route')
        change = authoring.draft_initial_route(read_input(args.route_input))
        route = parse_strict_json_bytes(change.documents[DRAFT], control / DRAFT)
        if route['work_id'] != control.name:
            raise ValueError('route work_id does not match requested control root')
        validate_route(route, control)
        return change, None, route
    check_pin(args.approved_route_digest)
    if args.operation == 'state-init':
        if optional_bytes(control / STATE) is not None or optional_bytes(control / ROUTE) is not None:
            raise ValueError('state-init requires absent canonical state and immutable route')
        change = authoring.initialize_state(
            read_protocol_file(control / DRAFT), args.approved_route_digest,
            [read_input(path) for path in args.initial_binding], args.transition_reason,
            evidence_refs(args.transition_evidence_ref), occurred,
        )
        route = parse_strict_json_bytes(change.documents[ROUTE], control / ROUTE)
        state = parse_strict_json_bytes(change.documents[STATE], control / STATE)
        if state['work_id'] != control.name:
            raise ValueError('reviewed route work_id does not match requested control root')
        return change, state, route
    state = load_strict_json(control / STATE)
    route = load_strict_json(resolve_control_ref(control, state['route_binding']['ref']))
    if route['route_digest'] != args.approved_route_digest:
        raise ValueError('operator route pin does not match the current route')
    errors = []
    validate_registered_artifact_payload(state, control / STATE, errors)
    errors.extend(validate_execution_state_contract(
        state, route, approved_route_digest=args.approved_route_digest,
        is_canonical_current=True, authority_mode=True,
        terminal_validation_passed=state['lifecycle_state'] in {'verified', 'completed'},
        approved_completion_digest=getattr(args, 'approved_completion_digest', None),
    ).errors)
    if errors:
        raise ValueError('; '.join(errors))
    revision = args.expected_revision
    operation = args.operation
    if operation == 'transition':
        candidate = authoring.append_transition(state, route, revision, args.target, args.reason, evidence_refs(args.evidence_ref), occurred)
    elif operation == 'phase-event':
        candidate = authoring.append_phase_event(state, route, revision, args.kind, args.phase_index, evidence_refs(args.evidence_ref), occurred)
    elif operation == 'artifact-bind':
        request = {'obligation_id': args.obligation_id, 'ref': args.artifact_ref, 'subject_sha256': args.subject_sha256}
        for key in ('structural_evidence', 'approval'):
            value = getattr(args, key)
            if value is not None:
                request[key] = read_input(value)
        candidate = authoring.bind_artifact(state, route, revision, request, occurred)
    elif operation == 'claim-completion':
        verification_path = resolve_control_ref(control, args.verification_record_ref)
        verification = load_strict_json(verification_path)
        bindings = read_input(args.evidence_bindings)
        if set(bindings) != {'evidence_bindings'} or not isinstance(bindings['evidence_bindings'], list):
            raise ValueError('evidence-bindings input requires exactly the evidence_bindings array')
        # The record names the observation time; capture the same live content now.
        captured = verification.get('work_state_ref', {}).get('captured_at')
        if not isinstance(captured, str):
            raise ValueError('verification record requires its work snapshot observation time')
        snapshot = capture_git_worktree(root, excluded_control_root=control, captured_at=captured)
        candidate = authoring.claim_completion(state, route, revision, verification,
            args.verification_record_ref, file_sha256(verification_path), bindings['evidence_bindings'],
            snapshot, args.reason, occurred)
    else:
        if args.outcome == 'completed':
            check_pin(args.approved_completion_digest)
            errors = []
            authority = authorize_execution_state(control / STATE, args.approved_route_digest,
                                                   args.approved_completion_digest, errors)
            if authority.disposition != ValidationDisposition.VALID:
                raise ValueError('; '.join(errors))
        candidate = authoring.record_outcome(state, route, revision, args.outcome, args.reason, occurred, args.approved_completion_digest)
    return authoring.AuthoredChange({STATE: authoring.document_bytes(candidate)}, state_revision=candidate['state_revision']), candidate, route


def execute(args):
    mutations = []
    documents = {}
    revision = None
    materialization_started = False
    try:
        if args.operation in {'route-draft', 'state-init'}:
            root, control = initial_context(args.repo_root, args.work_id)
        else:
            state_path = Path(args.state).absolute()
            state = load_strict_json(state_path)
            context, errors = resolve_authority_context(state_path, state)
            if errors or context is None:
                raise ValueError('; '.join(errors))
            root, control = context.repo_root, context.control_root
        prefix = control.relative_to(root).as_posix() + '/'
        with locked_work(root, control) as journal:
            recovered = recover_initialization(journal, root, control, mutations, getattr(args, 'approved_route_digest', None))
            if recovered is True and args.operation == 'state-init':
                state = load_strict_json(control / STATE)
                return authoring_result(args.operation, status='written', mutations=mutations,
                                        state_revision=state['state_revision'],
                                        documents={prefix + name: read_protocol_file(control / name) for name in (ROUTE, STATE)})
            before = bundle_identity(control)
            change, state, route = build_change(args, root, control)
            documents = {prefix + name: content for name, content in change.documents.items()}
            revision = change.state_revision
            excess = [(name, len(value)) for name, value in documents.items() if len(value) > LIMIT_BYTES]
            if excess:
                # Over-limit bytes are rejected, not a valid capacity record.
                documents = {}
                raise ValueError('; '.join(f'{name}: candidate uses {size} bytes, exceeding the {LIMIT_BYTES}-byte hard limit' for name, size in excess))
            completion_candidate = None
            if state is not None:
                view = CandidateBundleView(control, dict(change.documents), change.removals)
                outcome = validate_execution_candidate(
                    repo_root=root, control_root=control, state_path=control / STATE,
                    state=state, route=route, view=view,
                    approved_route_digest=args.approved_route_digest,
                )
                if outcome.disposition == ValidationDisposition.INVALID:
                    raise ValueError('; '.join(outcome.errors))
                if args.operation == 'claim-completion':
                    errors = validate_completion_preflight(state, repo_root=root, control_root=control, view=view)
                    if errors:
                        raise ValueError('; '.join(errors))
                completion_candidate = outcome.candidate_completion_digest
            if bundle_identity(control) != before:
                raise ValueError('control bundle changed before materialization')
            if args.operation == 'state-init':
                for name in change.documents:
                    temporary = initialization_temporary(control, journal, name)
                    if temporary.exists() or temporary.is_symlink():
                        raise RecoveryRequired('unexpected initialization temporary already exists')
                manifest = {
                    'version': 'prodcraft-state-init.v1', 'control_root': str(control),
                    'draft_sha256': before[DRAFT], 'initially_absent': [ROUTE, STATE],
                    'documents': {name: base64.b64encode(content).decode('ascii') for name, content in change.documents.items()},
                }
                atomic_write(journal, canonical_json_bytes(manifest), create=True)
            materialization_started = True
            for name, content in change.documents.items():
                action = 'replace' if name in before else 'create'
                atomic_write(control / name, content, create=action == 'create',
                             temporary_path=initialization_temporary(control, journal, name) if args.operation == 'state-init' else None)
                mutations.append({'action': action, 'path': prefix + name})
            for name in change.removals:
                if file_sha256(control / name) != before[name]:
                    raise RecoveryRequired('draft changed before cleanup')
                (control / name).unlink()
                mutations.append({'action': 'remove', 'path': prefix + name})
            fsync_directory(control)
            if any(read_protocol_file(control / name) != content for name, content in change.documents.items()):
                raise RecoveryRequired('authored document changed after materialization')
            if state is not None:
                validate_materialized(root, control)
                if args.operation == 'claim-completion':
                    errors = validate_completion_preflight(state, repo_root=root, control_root=control, view=CandidateBundleView(control))
                    if errors:
                        raise RecoveryRequired('; '.join(errors))
            else:
                if read_protocol_file(control / DRAFT) != change.documents[DRAFT]:
                    raise RecoveryRequired('route draft changed after materialization')
                validate_route(route, control)
            if args.operation == 'state-init':
                journal.unlink()
                fsync_directory(journal.parent)
            if any(read_protocol_file(control / name) != content for name, content in change.documents.items()):
                raise RecoveryRequired('authored document changed during final validation')
            pending = change.candidate_route_digest or completion_candidate
            return authoring_result(args.operation, status='candidate' if pending else 'written',
                mutations=mutations, state_revision=revision, documents=documents,
                candidate_route_digest=change.candidate_route_digest,
                candidate_completion_digest=completion_candidate)
    except (OSError, ValueError, KeyError, TypeError, IndexError, RecursionError, yaml.YAMLError, WorktreeSnapshotError, subprocess.SubprocessError) as exc:
        status = 'recovery-required' if materialization_started or mutations or isinstance(exc, RecoveryRequired) else 'invalid'
        return authoring_result(args.operation, status=status, mutations=mutations,
                                state_revision=revision, documents=documents, errors=[str(exc) or type(exc).__name__])


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest='operation', required=True)
    for name in ('route-draft', 'state-init', 'transition', 'phase-event', 'artifact-bind', 'claim-completion', 'record-outcome'):
        command = commands.add_parser(name)
        command.add_argument('--output-format', choices=('text', 'json-v1'), default='text')
        command.add_argument('--occurred-at')
        if name in {'route-draft', 'state-init'}:
            command.add_argument('--repo-root', required=True)
            command.add_argument('--work-id', required=True)
        else:
            command.add_argument('--state', required=True)
            command.add_argument('--expected-revision', type=int, required=True)
        if name != 'route-draft':
            command.add_argument('--approved-route-digest')
        if name == 'route-draft':
            command.add_argument('--route-input', required=True)
        elif name == 'state-init':
            command.add_argument('--initial-binding', action='append', default=[])
            command.add_argument('--transition-reason', required=True)
            command.add_argument('--transition-evidence-ref', action='append', default=[])
        elif name == 'transition':
            command.add_argument('--target', required=True)
            command.add_argument('--reason', required=True)
            command.add_argument('--evidence-ref', action='append', default=[])
        elif name == 'phase-event':
            command.add_argument('--kind', choices=('entered', 'exited'), required=True)
            command.add_argument('--phase-index', type=int, required=True)
            command.add_argument('--evidence-ref', action='append', default=[])
        elif name == 'artifact-bind':
            for option in ('obligation-id', 'artifact-ref', 'subject-sha256'):
                command.add_argument('--' + option, required=True)
            evidence = command.add_mutually_exclusive_group()
            evidence.add_argument('--structural-evidence')
            evidence.add_argument('--approval')
        elif name == 'claim-completion':
            for option in ('verification-record-ref', 'evidence-bindings', 'reason'):
                command.add_argument('--' + option, required=True)
        else:
            command.add_argument('--outcome', choices=('verified', 'rejected', 'completed'), required=True)
            command.add_argument('--reason', required=True)
            command.add_argument('--approved-completion-digest')
    return result


def main():
    args = parser().parse_args()
    result = execute(args)
    if args.output_format == 'json-v1':
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"Prodcraft {result['operation']}: {result['status']}")
        for key in ('candidate_route_digest', 'candidate_completion_digest'):
            if result[key]:
                print(f"{key}: {result[key]} (candidate; separate operator review required)")
        for message in result['warnings'] + result['errors']:
            print(message)
    return 0 if result['status'] in {'written', 'candidate'} else 1


if __name__ == '__main__':
    raise SystemExit(main())
