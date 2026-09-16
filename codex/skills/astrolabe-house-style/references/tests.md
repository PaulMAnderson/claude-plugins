# Test quality

Test observable scientific/business outcomes, not private implementation details or mock calls alone. A passing test must be capable of detecting the specified regression. Use arrange → act → assert, one coherent question per test, and exact AC IDs where the plan provides them.

Use small synthetic signals or known-good data with known outcomes for numerical logic. Include meaningful pipeline integration tests with real tiny files; test isolated pure functions when it helps pinpoint invariants. Prefer actual arrays/frames to mocking their behavior. Keep large datasets out of routine tests and use stable provenance for golden data.

Managed dependencies can use isolated real files/test databases. For uncontrolled hardware/APIs, use recorded inputs or doubles at your own adapter boundary. Match realistic shapes, dtypes, errors, and timing. Never run a test against live destructive resources simply because it is called an integration test.

Use appropriate floating-point tolerances, deterministic seeds, boundary/NaN policies, and inverse/idempotence/oracle properties. Avoid writing a second copy of the implementation as an expected result. Test assertions should survive a correct refactor.

Async checks wait for an observable condition with a bounded timeout, not arbitrary long sleeps. Clean up handles, threads, connections, and temporary files through fixtures/context managers. Unique IDs or isolated schemas prevent test interference. Required reproducibility checks should reflect supported platforms/library versions.

For behavior changes, write the regression first and confirm its intended failure, then implement and verify. For reversible low-impact/documentation/configuration edits, use relevant direct checks rather than implementation-mirroring tests. Run the necessary scope once evidence is current; expand only for changed behavior or unresolved concerns.
