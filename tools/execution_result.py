"""Closed v1 authoring result projection, separate from stored protocol state."""
from __future__ import annotations

LIMIT_BYTES = 16 * 1024 * 1024
WARNING_BYTES = 12 * 1024 * 1024


def authoring_result(operation, *, status='invalid', mutations=(), state_revision=None,
                     candidate_route_digest=None, candidate_completion_digest=None,
                     documents=None, errors=()):
    capacities = [
        {'path': path, 'used_bytes': len(content), 'warning_bytes': WARNING_BYTES,
         'limit_bytes': LIMIT_BYTES, 'remaining_bytes': max(0, LIMIT_BYTES - len(content))}
        for path, content in (documents or {}).items()
    ]
    # A resumed transaction can remove/reinstall one path before continuing.
    # The v1 result requires unique paths, so report its provable net action.
    actions = {}
    for mutation in mutations:
        path, action = mutation['path'], mutation['action']
        previous = actions.get(path)
        if previous == 'create' and action == 'remove':
            del actions[path]
        elif previous == 'create':
            actions[path] = 'create'
        elif previous == 'remove' and action == 'create':
            actions[path] = 'replace'
        else:
            actions[path] = action
    return {
        'schema_version': 'execution-authoring-result.v1', 'status': status,
        'operation': operation, 'mutations': [{'action': action, 'path': path} for path, action in actions.items()],
        'state_revision': state_revision,
        'candidate_route_digest': candidate_route_digest if status == 'candidate' else None,
        'candidate_completion_digest': candidate_completion_digest if status == 'candidate' else None,
        'capacities': capacities,
        'warnings': [f"{item['path']}: document reached the 12 MiB rollout-stop threshold"
                     for item in capacities if item['used_bytes'] >= WARNING_BYTES],
        'errors': list(errors),
    }
