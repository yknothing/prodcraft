# Anti-Pattern Notes

1. **String extraction only** -- moving text to resource files does not solve locale behavior.
2. **English-first assumptions** -- hard-coded length, grammar, or format rules break quickly.
3. **No fallback policy** -- missing translations become runtime chaos if not designed upfront.
