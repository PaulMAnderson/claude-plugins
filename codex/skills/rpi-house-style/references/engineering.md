# Architecture and validation

Separate functional core (deterministic algorithms/transforms) from imperative shell (file/database/network I/O and orchestration). Pass arrays/data/configuration into the core; inject clocks and random generators rather than reading global time/random/environment there. Prefer separate files where this improves a real boundary; document a necessary mixed module instead of forcing a cosmetic refactor.

In projects following RPI classification, add a language-appropriate `pattern: Functional Core` or `pattern: Imperative Shell` comment to new/meaningfully changed application source. A necessary mixed file records `pattern: Mixed (unavoidable)` and its reason. Documentation, configuration/data files, and shell scripts do not need classification. A logger may be injected into core code under the original house convention; keep it from changing outputs and use a no-op in tests.

Name files for purpose (`signal_processing.py`, `data_io.py`), not catch-all `utils`/`misc`. Keep visibility and module dependencies explicit. Use native platform paths and behavior; isolate substantial platform differences and verify supported targets. Avoid global workspace mutation, swallowed errors, loose types hiding unknown contracts, and speculative abstraction.

For scientific algorithms identify useful properties during design: roundtrips, idempotence, preserved shape/count/sum, symmetry, commutativity, associative grouping, identity, comparison to an oracle. Surface NaN handling, array orientation, sample-rate mismatch, filter stability, edge effects, and precision before implementation.

Validate at distinct relevant layers:

1. Entry: file/dataset existence, schema, type, dimensions.
2. Algorithm: units, positive sample rate, valid ranges, NaN policy, invariants that transformations can break.
3. Mutation context: correct destination, transaction, dry-run behavior when supported, meaningful nonempty results.
4. Diagnostics: bounded shape/range/context evidence for difficult pipeline failures.

Choose layers based on actual paths and risks. Avoid duplicate identical checks at adjacent layers and checks already guaranteed by trusted internal types/libraries. Do not use a shape heuristic as proof of orientation. Test bypass paths where multiple callers can reach an algorithm.

Distinguish actionable user-facing errors from programming errors; preserve root causes. Composable error fragments can use `failed to load recording: missing dataset 'raw_signal'`. Include expected vs actual values where useful, without exposing secrets or entire inputs.
