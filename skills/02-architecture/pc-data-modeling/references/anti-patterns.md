# Anti-Pattern Notes

1. **Schema-first architecture** -- letting database convenience redraw service boundaries.
2. **One model for every concern** -- forcing write, read, analytics, and migration needs into the same shape.
3. **Implicit ownership** -- multiple components update the same record without a canonical owner.
4. **Migration amnesia** -- designing a clean schema that ignores how real data will get there.
