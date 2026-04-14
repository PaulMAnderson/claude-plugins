# Plan and Execute Context

This extension provides planning and execution workflows for software development projects. The workflows here are based on a structured design-then-implement-then-verify cycle.

## Core Workflow

The standard workflow is:

1. **Design** (`/start-design-plan`) — Collaboratively design the feature with brainstorming, clarification, and a written design plan
2. **Plan** (`/start-implementation-plan`) — Break the design into phased, task-level implementation plans
3. **Execute** (`/execute-implementation-plan`) — Execute each task with TDD, verification, and commits
4. **Review** (`/code-review`) — Validate completed work against plans and quality gates
5. **Fix** (`/fix-review-issues`) — Address any issues found in review
6. **Validate** (`/analyze-test-coverage`) — Confirm test coverage and generate human test plan

## Project Customization

Projects can customize the workflow by creating a `.rpi/` directory with guidance files:

- **`.rpi/design-plan-guidance.md`** — Domain terms, architectural constraints, technology preferences, scope boundaries. Read before design planning.
- **`.rpi/implementation-plan-guidance.md`** — Coding standards, testing requirements, review criteria, commit conventions. Read before implementation planning and during final review.

If these files don't exist, the standard workflow proceeds without project-specific guidance.

## Quality Standards

All code work in this workflow follows these non-negotiable standards:

### Test-Driven Development

- Write the failing test first — always
- Run the test to confirm it fails correctly before writing implementation
- Write minimal code to make the test pass
- Refactor with tests as safety net
- No production code without a failing test first

### Verification Before Completion

Before reporting any task complete:
- Run the full test suite and confirm it passes
- Run the build and confirm it succeeds
- Run the linter and confirm zero errors
- Provide specific command output as evidence — never claim success without it

### Code Review Standards

Code reviews enforce these quality gates:

| Standard | Requirement | Severity if violated |
|----------|-------------|----------------------|
| Type safety | No `any` without justification comment | Critical |
| Error handling | All external calls have error handling | Critical |
| Test coverage | All public functions tested | Critical |
| Security | Input validation, no injection vulnerabilities | Critical |
| Test validity | Tests verify behavior, not mock behavior | Critical |

**Critical issues block integration — no exceptions.**

Issue severity:
- **Critical**: Must fix before approval (failing tests, security issues, missing tests, untested error paths)
- **Important**: Should fix (code organization, documentation gaps, performance concerns)
- **Minor**: Fix before completion (naming, style, small refactoring)

### FCIS Pattern

Prefer Functional Core / Imperative Shell architecture:
- Business logic in pure functions (easy to test, no side effects)
- Side effects (I/O, database, network) at the shell layer
- Keep the boundary explicit

## Implementation Plan Structure

Implementation plans live in `docs/implementation-plans/<plan-name>/` and consist of:

- **`phase_01.md`, `phase_02.md`, ...** — Phase files executed sequentially
- **`test-requirements.md`** — Acceptance criteria tables for automated and manual verification

Each phase file contains tasks. Each task must be:
- **Independently executable** — completable without reading other tasks
- **Testable** — has clear, measurable acceptance criteria
- **Appropriately sized** — completable in one focused work session
- **Ordered** — dependencies explicit, tasks in dependency order

## Design Plan Structure

Design plans live in `docs/design-plans/<feature-name>.md` and include:
- Overview and requirements
- Selected approach with rationale
- Architecture (components, data flows, interfaces)
- Implementation phases (high-level, for planning)
- Rejected approaches with reasons
- Open questions

## Code Review Expertise

When performing code reviews:

- Run verification commands yourself — never trust reports from others
- Compare implementation to the plan, not just to abstract quality standards
- Check that tests verify behavior, not that they simply exist and pass
- Test validity: can the test fail? Does the assertion test the right thing?
- Provide specific `file:line` references for every issue
- Use the structured review template — it enables consistent follow-up
- Approve only when zero issues remain (Critical, Important, and Minor)

## Bug Fixing Expertise

When fixing review issues:

- Read all issues before starting any fixes — understand the full scope
- Identify root causes, not just symptoms — superficial fixes create new problems
- Fix in priority order: Critical first, then Important, then Minor
- Fix everything — don't skip Minor issues
- Make no unrelated changes while fixing
- Commit after all fixes with a clear message referencing the issues

## Test Analysis Expertise

When analyzing test coverage:

- File existence alone does not prove coverage — read the test and understand what it verifies
- Map every acceptance criterion to either an automated test or a manual verification step
- Report exact gaps with actionable descriptions so they can be fixed
- Human test plan steps must be specific enough for someone unfamiliar with the code to execute
- Build the human test plan from what you learned reading the tests — don't invent steps

## Context Compression

When context grows large, compress it to `.rpi/CONTEXT.md` using Anchored Iterative Summarization:

- Preserve verbatim: decisions made, constraints discovered, open questions, key facts
- Compress: supporting discussion, redundant content, superseded information
- The compressed context should be loadable at the start of a new session to restore working state
