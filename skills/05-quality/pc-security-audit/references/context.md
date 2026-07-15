# Context Notes

Security audit is the focused quality pass for abuse resistance. It is narrower than full security architecture work and deeper than ordinary code review. Use it when a change crosses trust boundaries, handles sensitive data, touches authn/authz, introduces new dependencies, or materially changes deployment exposure.

In Prodcraft, security audit exists to stop avoidable release risk. It should produce concrete findings tied to the current slice, not a generic list of best practices.
