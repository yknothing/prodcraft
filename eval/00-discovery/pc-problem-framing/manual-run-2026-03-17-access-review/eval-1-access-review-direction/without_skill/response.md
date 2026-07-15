# Access Review Modernization Direction Note

## Recommended Direction

Release 1 should focus on modernizing the main campaign workflow while keeping the legacy module available during audit season.

## Main Options

1. **Campaign and evidence workflow first**
   - Modernize campaign creation, reminders, delegated approvals, and evidence packaging
   - Leave some legacy and edge workflows in place
2. **Near-parity release 1**
   - Include reassignment, data correction, and more tenant-specific rule handling immediately
   - More complete, but broader scope
3. **Migration-first direction**
   - Prioritize strong sync and transition behavior up front
   - Better for future cutover, but risks delaying visible release-1 value

## Recommendation

Choose the campaign-and-evidence-first direction for release 1.

## Why

- It delivers value without forcing a full replacement approach.
- It fits the coexistence requirement.
- It keeps release 1 focused during audit season.

## Open Questions

- Which tenant-specific exception rules are mandatory for release 1?
- Is same-day synchronization good enough, or is near-real-time required?
- Which reassignment and correction flows must be included immediately?

## Next Step

Turn the chosen direction into requirements, then design architecture around coexistence with the legacy module.
