# Anti-Pattern Notes

1. **Database-first modeling** -- Design the domain model, then derive the database schema. Not the reverse.
2. **Bounded contexts by reflex** -- Splitting the model into contexts before the requirements prove the split.
3. **Premature optimization** -- Don't model for query performance. Model for clarity. Performance comes later.
4. **Legacy term capture** -- Letting transitional brownfield vocabulary silently become the canonical future model.
