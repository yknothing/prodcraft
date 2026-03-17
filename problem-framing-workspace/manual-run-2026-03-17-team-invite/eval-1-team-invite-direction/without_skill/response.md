# Team Invite Direction Note

## Current Problem

Workspace owners need a simple way to bring coworkers into a shared product space. The team needs to decide what release 1 of team invite should look like.

## Main Options

1. **Email invite flow**
   - Simple for most users
   - Fastest to ship
2. **Company domain claim / SSO-oriented flow**
   - Better for larger teams
   - More identity and admin complexity
3. **Bulk provisioning**
   - Useful for bigger customer groups
   - More operational and admin scope

## Recommendation

Start with an email invite flow for release 1 and leave domain claim and bulk provisioning for later phases.

## Why

- It gets shared-workspace collaboration in front of users fastest.
- It keeps release 1 focused.
- It avoids pulling enterprise identity work into the first slice.

## Open Questions

- How many customers need domain claim immediately?
- Is admin-assisted bulk import required for the first paying customer segment?
- Should invite flows include role selection at invite time?

## Next Step

Do lightweight user research with likely early customers, then turn the chosen direction into requirements.
