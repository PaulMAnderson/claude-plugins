---
name: "astrolabe-review"
description: "Review Astrolabe plans or code, handle incoming review feedback, fix and re-review issues, and validate acceptance-criterion test coverage before completion."
---

# Review, fix, and validate

Read [the shared workflow contract](../astrolabe-workflow/references/workflow.md) and [review and coverage procedures](references/review.md). Use the mode the user or current phase requires:

- **Plan review:** compare phase files and test requirements to the design, verified repository, dependencies, and exact contracts. Check every deliverable and AC, executable order, meaningful tests, and complete prerequisites.
- **Code review:** inspect the full phase or whole-change package, surrounding code, applicable guidance, and test evidence. Report actionable defects with file/line and violated behavior/criterion. Check correctness, architecture, errors, input validation, relevant security/performance/concurrency, and test validity proportional to the change.
- **Incoming feedback:** read the whole review, restate unclear requirements, and verify claims against the repository. Accept valid technical findings and push back with evidence on incorrect ones. Do not blindly implement suggestions or automatically agree.
- **Fix issues:** record every finding verbatim, diagnose its cause, fix in severity order, rerun covering tests, and re-review old and new findings. This mode authorizes fixes when the request does; a review-only request produces findings without changing application code.
- **Coverage and final validation:** trace every scoped AC to actual assertions or justified manual steps. Fix gaps when implementation is authorized; otherwise report them. Generate a concrete human test plan after coverage passes, then inspect fresh final check evidence.

Default Astrolabe execution gate: zero unresolved valid issues, including Minor. Explicit rejection needs evidence; omission on a later review is not resolution. Do not silently downgrade a finding or waive a required check. If an actual conflict with a binding requirement needs user judgment, present the requirement and finding together.

Record whether review was independent or a local self-review. Role separation still applies when subagents are unavailable. Review reports and CLI success are evidence to inspect, not substitutes for inspecting the diff and assertions.
