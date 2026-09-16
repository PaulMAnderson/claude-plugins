# Design artifact structure

Use `.astrolabe/docs/design-plans/YYYY-MM-DD-<slug>.md`. Fill every applicable section with actual project facts; omit irrelevant sections. The tier index helps later context selection without discarding binding details.

```markdown
# Feature design

## Summary
What is being built and the chosen approach, written after the body.

## Memory Tier Index
- Hot: Definition of Done, acceptance criteria, binding constraints, unresolved decisions
- Warm: Architecture, contracts, implementation phases
- Cold: Investigation history, rejected approaches, glossary

## Definition of Done
Concrete deliverables and observable success; exact user constraints.
Decision status: supplied by user / confirmed / assumption (identify which).

## Acceptance Criteria
### feature.AC1: Observable outcome
- feature.AC1.1 Success: Specific input/action and expected result.
- feature.AC1.2 Failure: Specific invalid input and expected error behavior.
- feature.AC1.3 Edge: Boundary and expected result.

## Glossary
Only terms needed to understand this design.

## Architecture and contracts
Components, verified/proposed paths, data flow, complete public contracts.

## Existing patterns and investigation
Evidence paths, dependency versions, source links, date checked, limitations.

## Alternatives and rationale
Chosen approach and reasons alternatives were rejected.

## Implementation phases
<!-- START_PHASE_1 -->
### Phase 1: Cohesive goal
Components: concrete paths and responsibilities.
Dependencies: none, or named earlier phases.
Acceptance criteria: full scoped IDs.
Done when: operational checks or passing behavioral tests for those ACs.
<!-- END_PHASE_1 -->

## Open decisions and risks
Uncertainty, impact, owner, and what resolves it.
```

Preserve scoped AC identifiers across planning, test names/comments, reports, and review. If a requirement changes, record why and update every affected mapping. Do not silently reuse an old identifier for a different outcome.
