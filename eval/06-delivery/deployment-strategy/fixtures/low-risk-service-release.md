# Low-Risk Service Release

- Release type: stateless service update behind an unchanged API.
- Blast radius: low.
- Data migration: none.
- Reversibility: fast, by redeploying the previous image.
- Customer impact: limited to internal admin users if the release misbehaves.
- Deployment window: normal business hours with a short observation window.
