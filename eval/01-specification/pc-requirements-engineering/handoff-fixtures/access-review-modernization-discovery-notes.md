# Discovery Notes

- Compliance admins currently run quarterly access-review campaigns in a 12-year-old Rails monolith.
- Admins need reusable campaign templates, reviewer reminders, delegated approvals when managers are on leave, and downloadable evidence packages for auditors.
- Several enterprise tenants rely on custom reviewer hierarchies and exception rules negotiated in MSAs, but the exact tenant list is incomplete.
- Release 1 must work alongside the legacy module because some regions cannot cut over during audit season.
- Historical campaigns older than two years may remain read-only in the legacy UI if auditors can still search and export the evidence package.
- Security wants stronger segregation-of-duties enforcement and tamper-evident audit trails.
- Customer success says the current module times out on large reviewer lists and users keep asking for the new experience to feel faster.
- Legal requires evidence packages to be retained for seven years.
- Support says data correction and reviewer reassignment workflows are still manual and not fully understood.
