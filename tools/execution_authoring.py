"""Pure transformations for the v1 execution protocol; no IO or approvals."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

from tools.execution_state import (
    LIFECYCLE_TRANSITIONS, append_record_digest, canonical_json_bytes,
    canonical_json_digest, claim_payload_projection, completion_basis_projection,
    parse_strict_json_bytes, route_content_digest, terminal_authority_digest,
    validate_execution_state_contract,
)


@dataclass(frozen=True)
class AuthoredChange:
    documents: Mapping[str, bytes]
    removals: frozenset[str] = frozenset()
    state_revision: int | None = None
    candidate_route_digest: str | None = None
    candidate_completion_digest: str | None = None

    def __post_init__(self):
        object.__setattr__(self, 'documents', MappingProxyType(dict(self.documents)))
        object.__setattr__(self, 'removals', frozenset(self.removals))


def document_bytes(payload: dict) -> bytes:
    return canonical_json_bytes(payload) + b'\n'


def draft_initial_route(route: dict) -> AuthoredChange:
    candidate = deepcopy(route)
    if candidate.get('route_revision') != 1 or 'previous_route' in candidate:
        raise ValueError('route-draft supports only the initial route revision')
    candidate['route_digest'] = route_content_digest(candidate)
    return AuthoredChange(
        {'route-decision.r1.draft.json': document_bytes(candidate)},
        candidate_route_digest=candidate['route_digest'],
    )


def _copy_at_revision(state: dict, expected_revision: int) -> dict:
    if isinstance(expected_revision, bool) or expected_revision != state['state_revision']:
        raise ValueError('expected revision does not match current state_revision')
    return deepcopy(state)


def _checked(state: dict, route: dict) -> dict:
    result = validate_execution_state_contract(
        state, route, approved_route_digest=route['route_digest'],
        is_canonical_current=False, authority_mode=False,
    )
    if result.errors:
        raise ValueError('; '.join(result.errors))
    return state


def _transition(state: dict, target: str, reason: str, evidence: list, occurred_at: str):
    if not reason or not reason.strip():
        raise ValueError('transition reason is required')
    source = state['lifecycle_state']
    if (source, target) not in LIFECYCLE_TRANSITIONS:
        raise ValueError(f'illegal lifecycle transition: {source} -> {target}')
    state['state_revision'] += 1
    sequence = state['state_revision']
    record = {
        'recorded_sequence': sequence, 'from_state': source, 'to_state': target,
        'occurred_at': occurred_at, 'reason': reason, 'evidence_refs': deepcopy(evidence),
    }
    record['record_digest'] = append_record_digest(record)
    state['lifecycle_transitions'].append(record)
    state['lifecycle_state'] = target
    state['updated_at'] = occurred_at
    if target == 'blocked':
        state['block_contexts'].append({
            'transition_sequence': sequence, 'reason': reason, 'evidence_refs': deepcopy(evidence),
        })
    elif source == 'blocked' and target == 'executing':
        unresolved = [value for value in state['block_contexts'] if 'resume_transition_sequence' not in value]
        if len(unresolved) != 1:
            raise ValueError('resume requires exactly one active block context')
        unresolved[0]['resume_transition_sequence'] = sequence
    return record


def _binding(state: dict, route: dict, request: dict):
    obligation_id = request.get('obligation_id')
    obligations = [item for item in route['obligations'] if item['id'] == obligation_id]
    if len(obligations) != 1:
        raise ValueError('binding requires exactly one known obligation')
    obligation = obligations[0]
    assurance = obligation['assurance']
    extra = {'presence': set(), 'structural_valid': {'structural_evidence'}, 'approval_accepted': {'approval'}}[assurance]
    if set(request) != {'obligation_id', 'ref', 'subject_sha256'} | extra:
        raise ValueError('binding request must contain exactly the assurance-specific fields')
    state['state_revision'] += 1
    state['artifact_bindings'].append({
        **deepcopy(request), 'recorded_sequence': state['state_revision'],
        'artifact': obligation['artifact'], 'assurance': assurance,
    })


def initialize_state(route_bytes: bytes, approved_route_digest: str, initial_bindings: list,
                     transition_reason: str, transition_evidence: list, occurred_at: str) -> AuthoredChange:
    route = parse_strict_json_bytes(route_bytes, Path('route-decision.r1.draft.json'))
    if route.get('route_revision') != 1 or route_content_digest(route) != approved_route_digest or route.get('route_digest') != approved_route_digest:
        raise ValueError('approved route pin does not match the reviewed initial route')
    obligations = [item for item in route['obligations'] if item['gate'] == {
        'kind': 'lifecycle_transition', 'from_state': 'received', 'to_state': 'routed',
    }]
    request_ids = [item.get('obligation_id') for item in initial_bindings]
    if len(request_ids) != len(set(request_ids)) or set(request_ids) != {item['id'] for item in obligations}:
        raise ValueError('initial bindings must satisfy exactly every received -> routed obligation')
    state = {
        'artifact': 'execution-state', 'schema_version': 'execution-state.v1',
        'work_id': route['work_id'], 'state_revision': 0, 'updated_at': occurred_at,
        'route_binding': {'ref': 'route-decision.r1.json', **{key: route[key] for key in ('route_id', 'route_revision', 'route_digest')}},
        'lifecycle_state': 'received', 'lifecycle_transitions': [], 'phase_events': [],
        'artifact_bindings': [], 'block_contexts': [], 'completion_attempts': [],
    }
    by_id = {item['obligation_id']: item for item in initial_bindings}
    for obligation in obligations:
        _binding(state, route, by_id[obligation['id']])
    _transition(state, 'routed', transition_reason, transition_evidence, occurred_at)
    _checked(state, route)
    return AuthoredChange(
        {'route-decision.r1.json': route_bytes, 'execution-state.json': document_bytes(state)},
        frozenset({'route-decision.r1.draft.json'}), state['state_revision'],
    )


def append_transition(state: dict, route: dict, expected_revision: int, target: str,
                      reason: str, evidence: list, occurred_at: str) -> dict:
    if target not in {'gated', 'executing', 'blocked'}:
        raise ValueError('use the dedicated operation for initial or terminal transitions')
    candidate = _copy_at_revision(state, expected_revision)
    _transition(candidate, target, reason, evidence, occurred_at)
    return _checked(candidate, route)


def append_phase_event(state: dict, route: dict, expected_revision: int, kind: str,
                       phase_index: int, evidence: list, occurred_at: str) -> dict:
    candidate = _copy_at_revision(state, expected_revision)
    phases = route['workflow']['focus_sequence']
    if isinstance(phase_index, bool) or not 0 <= phase_index < len(phases):
        raise ValueError('phase index is outside the approved workflow')
    candidate['state_revision'] += 1
    event = {
        'recorded_sequence': candidate['state_revision'], 'kind': kind,
        'phase_index': phase_index, 'phase': phases[phase_index],
        'occurred_at': occurred_at, 'evidence_refs': deepcopy(evidence),
    }
    event['record_digest'] = append_record_digest(event)
    candidate['phase_events'].append(event)
    candidate['workflow_cursor'] = {'phase_index': phase_index, 'phase': phases[phase_index], 'checkpoint': kind}
    candidate['updated_at'] = occurred_at
    return _checked(candidate, route)


def bind_artifact(state: dict, route: dict, expected_revision: int, request: dict, occurred_at: str) -> dict:
    candidate = _copy_at_revision(state, expected_revision)
    _binding(candidate, route, request)
    candidate['updated_at'] = occurred_at
    return _checked(candidate, route)


def claim_completion(state: dict, route: dict, expected_revision: int, verification: dict,
                     verification_ref: str, verification_sha256: str, evidence_bindings: list,
                     work_snapshot: dict, reason: str, occurred_at: str) -> dict:
    candidate = _copy_at_revision(state, expected_revision)
    _transition(candidate, 'completion_claimed', reason, [], occurred_at)
    revision = len(candidate['completion_attempts']) + 1
    attempt = {
        'attempt_id': f'attempt-{revision}', 'attempt_revision': revision,
        'claim': verification['claim'], 'claim_scope': verification['claim_scope'],
        'claim_cut_sequence': candidate['state_revision'],
        **{key: route[key] for key in ('route_id', 'route_revision', 'route_digest')},
        'work_snapshot': deepcopy(work_snapshot), 'claimed_at': occurred_at,
        'verification_commitment': {
            'verification_record_ref': verification_ref, 'verification_record_sha256': verification_sha256,
            'evidence_bindings': deepcopy(evidence_bindings), 'work_snapshot': deepcopy(work_snapshot),
        },
        'terminal_transitions': [],
    }
    attempt['claim_digest'] = canonical_json_digest(claim_payload_projection(attempt))
    candidate['completion_attempts'].append(attempt)
    candidate['current_completion_attempt_id'] = attempt['attempt_id']
    attempt['completion_basis_digest'] = canonical_json_digest(completion_basis_projection(candidate, attempt))
    return _checked(candidate, route)


def record_outcome(state: dict, route: dict, expected_revision: int, outcome: str,
                   reason: str, occurred_at: str, approved_completion_digest: str | None = None) -> dict:
    if outcome not in {'verified', 'rejected', 'completed'}:
        raise ValueError('unsupported completion outcome')
    if outcome == 'completed':
        if not approved_completion_digest or terminal_authority_digest(state) != approved_completion_digest:
            raise ValueError('approved completion pin must match the current verified state')
    elif approved_completion_digest is not None:
        raise ValueError('completion pin is accepted only for verified -> completed')
    candidate = _copy_at_revision(state, expected_revision)
    event = _transition(candidate, outcome, reason, [], occurred_at)
    attempt = candidate['completion_attempts'][-1]
    attempt['terminal_transitions'].append({key: event[key] for key in ('recorded_sequence', 'record_digest')})
    if outcome == 'rejected':
        attempt.pop('completion_binding', None)
        candidate.pop('current_completion_attempt_id', None)
    else:
        attempt['completion_binding'] = {
            **{key: attempt[key] for key in ('attempt_id', 'attempt_revision', 'claim_digest', 'completion_basis_digest', 'route_id', 'route_revision', 'route_digest')},
            **deepcopy(attempt['verification_commitment']),
            'terminal_transition_digests': [item['record_digest'] for item in attempt['terminal_transitions']],
        }
    return _checked(candidate, route)
