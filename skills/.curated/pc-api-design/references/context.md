# Context Notes

API design defines how system components communicate. A well-designed API is intuitive, consistent, and evolvable. A poorly designed API creates coupling, breaks clients, and generates support burden for years.

In a lifecycle-aware system, API design must preserve upstream architecture boundaries and unresolved questions. Do not smuggle rollout plans, migration choreography, or internal data-model assumptions into the contract unless they are true contract requirements.
