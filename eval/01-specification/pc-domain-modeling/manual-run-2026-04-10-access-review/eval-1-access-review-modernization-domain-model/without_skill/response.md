# Access Review Domain Notes

## Main Objects

- **Campaign**
- **Reviewer**
- **Review Assignment**
- **Evidence Export**
- **Audit Log**
- **Tenant Hierarchy Rule**
- **Legacy Campaign Mirror**
- **Sync Job**

## Relationship Notes

- A campaign has many review assignments and evidence exports.
- A reviewer can own many assignments.
- Tenant hierarchy rules can update reviewer assignments.
- Audit logs track campaign changes and evidence exports.
- Legacy campaign mirrors copy old campaign data into the new model when needed.
- Sync jobs keep new and legacy modules aligned.

## Candidate Contexts

This slice probably needs separate contexts for:

1. **Campaign Management**
2. **Policy Rules**
3. **Evidence**
4. **Legacy Sync**

These contexts appear necessary because evidence, policy, and sync have different technical concerns.

## Working Terms

- **campaign**: a batch of review work
- **assignment**: a reviewer-task row
- **evidence export**: a generated audit bundle
- **legacy mirror**: an imported historical campaign copy

## Assumption

Historical campaigns will gradually move into the new system through sync jobs, so the future model can treat legacy campaigns and new campaigns as the same concept over time.
