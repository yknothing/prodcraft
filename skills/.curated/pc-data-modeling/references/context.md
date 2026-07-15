# Context Notes

Data modeling decides what the system remembers, how it relates, and how change propagates through storage over time. In Prodcraft, it bridges domain language and implementation reality: the model must reflect real ownership boundaries, consistency needs, and migration cost.

Use this skill after system design clarifies component boundaries. If storage design is left implicit, implementation invents schema rules piecemeal and migration risk surfaces late.

## Related Capability Notes

- `pc-migration-strategy` (planned) -- handles larger migration programs that depend on the model
