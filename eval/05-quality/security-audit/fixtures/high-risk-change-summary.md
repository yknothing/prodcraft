# High-Risk Change Summary

## Change Surface

- adds `POST /v1/invite/accept`
- writes invite acceptance to the database
- logs the third-party provider response for debugging

## Risks Already Noted

- endpoint currently trusts `tenant_id` from the request body
- SQL is assembled with string interpolation in the acceptance path
- a new provider API key was added during the change
