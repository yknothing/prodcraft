# API Contract Summary

- `POST /v1/campaigns/{campaignId}/reassignments`
  - Request reviewer reassignment for the confirmed release-1 subset of reassignment flows.
  - Unsupported reassignment variants should return a structured `UNSUPPORTED_RELEASE1_FLOW` response.

## Error Envelope

```json
{
  "error": {
    "code": "UNSUPPORTED_RELEASE1_FLOW",
    "message": "Reviewer reassignment type is not supported in release 1.",
    "details": []
  }
}
```

## Open Questions

- Which reassignment and data-correction flows require first-class support in release 1?
- Which tenant-specific hierarchy variants affect reassignment authorization?
