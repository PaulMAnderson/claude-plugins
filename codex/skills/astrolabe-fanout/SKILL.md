---
name: "astrolabe-fanout"
description: "Organize a requested corpus analysis as workers, critics, and synthesis with explicit coverage assignments, durable reports, and bounded failure recovery."
---

# Worker → critic → synthesis analysis

Use when the user requests this analysis structure or parallel corpus analysis. Use actual native subagents only when available and authorized. If delegation is unavailable, explain that the same stages will run sequentially with self-review, without claiming independent critic coverage.

1. Establish corpus, analysis question, desired thoroughness, and output. Estimate size and choose segment budgets from the actual context/tool limits, reserving room for reasoning/reports. Do not assume a fixed model context size. Use overlapping or semantic-boundary segments where needed to avoid losing boundary context.
2. Default effort: 3 segments per worker and 2 independent critic passes per segment; higher effort can use 3/3 or 2/3 when requested/appropriate. Compute the assignment table with code, ensuring each segment appears in the requested number of **distinct** critics' lists. With one small segment a bounded local analysis may suffice; disclose any reduced independence.
3. Write an orchestration plan containing source/segment boundaries, worker/critic assignments, dependency graph, output paths, and coverage checks. Use absolute input/output paths and dedicated `segments/`, `workers/`, `critics/` directories in a permitted workspace. Honor requested approval gates; otherwise continue within existing scope.
4. Track every worker, critic, and synthesis task before launch. Workers depend on inputs; each critic depends on all relevant worker reports; synthesis depends on every required critic report. Respect available concurrency limits and disjoint writes.
5. Workers read their complete segments and write evidence-linked findings, significance, and an explicit coverage/skipped-parts record. Inspect output existence and contents before completion.
6. Critics inspect assigned worker reports and original evidence as needed, finding gaps, contradictions, accuracy errors, and cross-segment patterns. Verify distinct per-segment coverage and report limitations explicitly.
7. Synthesize findings with source evidence, resolve or surface contradictions, and report methodology/coverage/limitations plus links to worker and critic artifacts. Verify the final file before delivering its path.

If context overflows, split the scope, record the original task as superseded (not successfully analyzed), and reconnect dependencies to replacements. Retry a missing report once with clarified output requirements; unresolved gaps remain visible. After three similar failures change approach or surface the blocker; never quietly report complete coverage with missing segments.
