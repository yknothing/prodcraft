"""Completion policy enforced by the strict native-host launch wrapper."""
from __future__ import annotations

from pathlib import Path
import re

from tools.execution_state import file_sha256, load_strict_json_with_digest, terminal_authority_digest
from tools.execution_validation import ValidationDisposition, authorize_execution_state


def presentation_locale(prompt: str, selected: str | None = None) -> str:
    """Select English/Chinese presentation without counting quoted code as prose."""
    if selected is not None:
        return 'zh-CN' if selected.lower().startswith('zh') else 'en'
    prose = re.sub(r'```[\s\S]*?```|`[^`]*`|(?m:^ {0,3}>[^\n]*$)', '', prompt)
    choices = []
    patterns = {
        'en': r'(?i:(?:respond|reply|answer)\s+in\s+English|use\s+English\b)|(?:\u8bf7)?(?:\u7528|\u4f7f\u7528|\u4ee5)\u82f1\u6587',
        'zh-CN': r'(?i:(?:respond|reply|answer)\s+in\s+Chinese|use\s+Chinese\b)|(?:\u8bf7)?(?:\u7528|\u4f7f\u7528|\u4ee5)\u4e2d\u6587',
    }
    for locale, pattern in patterns.items():
        choices.extend((match.start(), locale) for match in re.finditer(pattern, prose))
    if choices:
        return max(choices)[1]
    han = len(re.findall(r'[\u3400-\u9fff]', prose))
    words = len(re.findall(r'[A-Za-z]+', prose))
    return 'zh-CN' if han > words else 'en'


def completion_status(state_path: Path, route_pin: str, completion_pin: str | None) -> dict:
    errors: list[str] = []
    try:
        state, digest = load_strict_json_with_digest(state_path)
        outcome = authorize_execution_state(state_path, route_pin, completion_pin, errors)
        if file_sha256(state_path) != digest:
            raise ValueError('execution state changed during host completion validation')
        expected_terminal = outcome.candidate_completion_digest
        if outcome.authority == 'terminal-authorized':
            expected_terminal = completion_pin
        if expected_terminal is not None and terminal_authority_digest(state) != expected_terminal:
            raise ValueError('host completion snapshot does not match the validated terminal digest')
        lifecycle = state.get('lifecycle_state')
    except ValueError as exc:
        return {'status': 'invalid', 'lifecycle_state': None, 'authority': None,
                'candidate_completion_digest': None, 'errors': [str(exc)]}
    candidate = outcome.candidate_completion_digest
    if outcome.disposition == ValidationDisposition.APPROVAL_REQUIRED:
        status = 'approval-required'
    elif outcome.disposition != ValidationDisposition.VALID:
        status = 'invalid'
    elif lifecycle == 'completed' and outcome.authority == 'terminal-authorized':
        status = 'completed'
    elif lifecycle == 'blocked':
        status = 'blocked'
    elif lifecycle == 'verified':
        status = 'incomplete'
        errors.append('verified state still requires a completed transition and a separate completed-state pin')
    else:
        status = 'incomplete'
        errors.append('the canonical work item has not reached completed state')
    return {
        'status': status, 'lifecycle_state': lifecycle,
        'authority': outcome.authority if status == 'completed' else None,
        'candidate_completion_digest': candidate, 'errors': errors,
    }


def display_status(result: dict, locale: str) -> str:
    if locale.lower().startswith('zh'):
        labels = {'completed': '\u5b8c\u6210\u9a8c\u6536\u5df2\u901a\u8fc7', 'approval-required': '\u7b49\u5f85\u5916\u90e8\u786e\u8ba4\uff0c\u5c1a\u672a\u5b8c\u6210',
                  'blocked': '\u4efb\u52a1\u53d7\u963b\uff0c\u5c1a\u672a\u5b8c\u6210', 'invalid': '\u5b8c\u6210\u9a8c\u6536\u672a\u901a\u8fc7',
                  'incomplete': '\u4efb\u52a1\u5c1a\u672a\u5b8c\u6210', 'native-failure': '\u5bbf\u4e3b\u8fd0\u884c\u5931\u8d25\uff0c\u672a\u786e\u8ba4\u5b8c\u6210'}
        lead = 'Prodcraft\uff1a' + labels[result['status']]
    else:
        labels = {'completed': 'completion accepted', 'approval-required': 'awaiting operator approval; not completed',
                  'blocked': 'work blocked; not completed', 'invalid': 'completion validation failed',
                  'incomplete': 'work is not completed', 'native-failure': 'native host failed; completion not accepted'}
        lead = 'Prodcraft: ' + labels[result['status']]
    return lead + ('. ' + '; '.join(result['errors']) if result['errors'] else '')
