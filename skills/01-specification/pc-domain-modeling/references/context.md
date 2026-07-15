# Context Notes

Domain modeling turns reviewed requirements into a stable business-language contract. Its job is to reduce ambiguity before later phases lock in schema, API, or implementation decisions.

In Prodcraft, this skill is most valuable when:

- the same noun may mean different things to product, operations, and engineering
- brownfield work must preserve legacy terms without letting them silently define the new model
- downstream skills need to know which concepts are authoritative, derived, transitional, or still unresolved

This is not database design, API design, or task planning. Stay at the domain layer.
