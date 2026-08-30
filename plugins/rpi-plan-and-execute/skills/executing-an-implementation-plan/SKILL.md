---
name: executing-an-implementation-plan
description: Execute implementation plan tasks with fresh per-task subagents
user-invocable: false
---

# Executing an Implementation Plan

Execute plan phase-by-phase, loading each phase just-in-time to minimize context usage.

**Core principle:** Read one phase → execute all tasks → review → move to next phase. Never load all phases upfront.

**REQUIRED SKILL:** `requesting-code-review` - The review loop (dispatch, fix, re-review until zero issues)

## Overview

**When NOT to use:**
- No implementation plan exists yet (use writing-implementation-plans first)
- Plan needs revision (brainstorm first)

## MANDATORY: Human Transparency

**The human cannot see what subagents return. You are their window into the work.**

After EVERY subagent completes (task-implementor, bug-fixer, code-reviewer), you MUST:

1. **Print the subagent's full response** to the user before taking any other action
2. **Do not summarize or paraphrase** - show them what the subagent actually said
3. **Include all details:** test counts, issue lists, commit hashes, error messages

**Before dispatching any subagent:**
- Briefly explain (2-3 sentences) what you're asking the agent to do
- State which phase this covers

**Why this matters:** When you silently process subagent output without showing the user, they lose visibility into their own codebase. They can't catch errors, learn from the process, or intervene when needed. Transparency is not optional.

**Red flag:** If you find yourself thinking "I'll just move on to the next step" without printing the subagent's response, STOP. Print it first.

## REQUIRED: Implementation Plan Path

**DO NOT GUESS.** If the user has not provided a path to an implementation plan directory, you MUST ask for it.

Use AskUserQuestion:
```
Question: "Which implementation plan should I execute?"
Options:
  - [list any plan directories you find in docs/implementation-plans/]
  - "Let me provide the path"
```

If `docs/implementation-plans/` doesn't exist or is empty, ask the user to provide the path directly.

**Never assume, infer, or guess which plan to execute.** The user must explicitly tell you.

## The Process

### 1. Discover Phases

**DO NOT read the full phase files yet.** List them and read only the header and task markers.

```bash
# List phase files
ls [plan-directory]/phase_*.md

# For each file, get the header (first 10 lines include title and Goal)
head -10 [plan-directory]/phase_01.md

# Get task/subcomponent structure without reading full content
grep -E "START_TASK_|START_SUBCOMPONENT_" [plan-directory]/phase_01.md
```

The header includes the title (`# [Phase Title]`) and `**Goal:**` line. Extract the title for the task entry.

The grep output shows the task structure, e.g.:
```
<!-- START_TASK_1 -->
<!-- START_TASK_2 -->
<!-- START_SUBCOMPONENT_A (tasks 3-5) -->
<!-- START_TASK_3 -->
<!-- START_TASK_4 -->
<!-- START_TASK_5 -->
```

Examples of headers you might see:
- `# Document Infrastructure Implementation Plan` — Phase 1 implied
- `# Phase 4: Link Resolution` — Phase number explicit

**Check for implementation guidance:**

After discovering phases, check if `.rpi/implementation-plan-guidance.md` exists in the project root:

```bash
# Check for implementation guidance (note the absolute path for later use)
ls [project-root]/.rpi/implementation-plan-guidance.md
```

If the file exists, note its **absolute path** for use during code reviews. If it doesn't exist, proceed without it—do not pass a nonexistent path to reviewers.

**Check for test requirements:**

Check if `test-requirements.md` exists in the plan directory:

```bash
# Check for test requirements (note the absolute path for later use)
ls [plan-directory]/test-requirements.md
```

If the file exists, note its **absolute path** for use during final review. The test requirements document specifies what automated tests must exist for each acceptance criterion.

### 2. Create Phase-Level Task List

Use TaskCreate to create **three task entries per phase** (or TodoWrite in older Claude Code versions). Include the title from the header:

```
- [ ] Phase 1a: Read /absolute/path/to/phase_01.md — Document Infrastructure Implementation Plan
- [ ] Phase 1b: Execute tasks
- [ ] Phase 1c: Code review
- [ ] Phase 2a: Read /absolute/path/to/phase_02.md — API Integration
- [ ] Phase 2b: Execute tasks
- [ ] Phase 2c: Code review
...
```

**Why absolute paths in task entries:** After compaction, context may be summarized. The absolute path in the task entry ensures you always know exactly which file to read.

**Why include the title:** Gives visibility into what each phase covers without loading full content.

### 2b. Check the Progress Ledger

Conversation memory does not survive compaction. Todos help, but they do not name commit ranges — and a controller that has lost its place can re-dispatch an entire completed phase, which is the single most expensive failure this workflow has.

**Before dispatching anything, check for a ledger:**

```bash
cat "$(git rev-parse --show-toplevel)/.rpi/exec/progress.md"
```

Anything listed there as complete **is** complete. Do not re-dispatch it. Resume at the first task or phase not marked complete.

**Append to the ledger as you go**, in the same message as your other bookkeeping:

- when a task's implementor returns `DONE` and is committed:
  `Phase N task M: complete (commits <base7>..<head7>)`
- when a phase's review comes back clean:
  `Phase N: complete (commits <base7>..<head7>, review clean)`

The ledger is your recovery map: the commits it names exist in git even when your context no longer remembers creating them. **After any compaction or resume, trust the ledger and `git log` over your own recollection.**

The ledger lives in the git-ignored workspace, so `git clean -fdx` will destroy it. If that happens, rebuild from `git log`.

### 3. Execute Each Phase

For each phase, follow this cycle:

#### 3a. Read Phase File (just-in-time)

Mark "Phase Na: Read [path]" as in_progress.

Read ONLY that phase file now. Extract:
- List of tasks in this phase
- Working directory
- Any phase-specific context

Mark "Phase Na: Read" as complete.

#### 3b. Execute All Tasks

Mark "Phase Nb: Execute tasks" as in_progress.

**Before dispatching, verify test coverage for functionality tasks:**

If a functionality task (code that does something) has no tests specified:
1. Check if a subsequent task in the same phase provides tests
2. If no tests exist anywhere for this functionality → **STOP**
3. This is a plan gap. Surface to user: "Task N implements [functionality] but no corresponding tests exist in the plan. This needs tests before implementation."

Do NOT implement functionality without tests. Missing tests = plan gap, not something to skip.

**Pre-flight conflict scan.** Before dispatching the first task of the phase, read the phase once looking for:
- tasks that contradict each other, or contradict the plan's constraints
- anything the plan explicitly mandates that a reviewer would treat as a defect (a test that asserts nothing, verbatim duplication of a logic block)

Present everything you find as **one batched question** — each finding beside the plan text that mandates it, asking which governs — before execution begins. Not one interrupt per discovery mid-phase. If the scan is clean, proceed without comment. The review loop remains the net for conflicts that only emerge from implementation.

**Record the phase BASE SHA now** — `git rev-parse HEAD` before the first task. You need it for the phase review, and `HEAD~1` will not do: a phase is many commits, and `HEAD~1` silently drops all but the last.

**Hand work over as files, not pasted text.** Everything you paste into a dispatch prompt — and everything a subagent prints back — stays in your context for the rest of the session and is re-read every turn. Use the scripts in this plugin's `scripts/` directory:

- `scripts/task-brief PHASE_FILE N` extracts one task's text to a file and prints the path. Pass a letter instead of a number (`scripts/task-brief PHASE_FILE A`) to extract a whole subcomponent.
- `scripts/review-package BASE HEAD` writes the commit list, stat summary, and full diff to a file and prints the path.

Neither output enters your context — only the path does.

#### Model Selection

The agents in this plugin pin `model: sonnet`, which is the right default for most tasks. You can override it per dispatch with the Task tool's `model` parameter. Override deliberately, in either direction:

**Down to haiku** when the task is transcription plus testing — the plan text contains the complete code to write, or it's a single-file mechanical fix.

**Up to opus** when the task needs design judgment, spans many files with real integration concerns, or requires broad codebase understanding. Also override up when re-dispatching a `BLOCKED` implementor whose blocker was reasoning, not missing context. The final whole-branch review is worth opus; per-phase reviews usually are not.

**Turn count beats token price.** Wall-clock and context cost scale with how many turns a subagent takes, and the cheapest model routinely takes 2–3× the turns on multi-step work — costing more overall. Sonnet is the floor for reviewers and for any implementor working from prose rather than complete code. Do not reach for haiku to save money on a task that will make it flail.

**Execute all tasks in sequence.** For each task, generate the brief, then dispatch:

```bash
scripts/task-brief [absolute path to phase file] N   # prints e.g. .rpi/exec/task-N-brief.md
```

```
<invoke name="Task">
<parameter name="subagent_type">rpi-plan-and-execute:task-implementor-fast</parameter>
<parameter name="description">Implementing Phase X, Task Y: [description]</parameter>
<parameter name="prompt">
  Implement Task N.

  Read this first — it is your requirements, with the exact values to use verbatim:
  [path printed by task-brief]

  Where this fits: [one line on the task's place in the project]

  Interfaces and decisions from earlier tasks that the brief cannot know:
  [only what this task actually touches]

  Ambiguity I noticed in the brief and how to resolve it:
  [your resolution, or "none"]

  Write your full report to: [brief path with -brief.md → -report.md]
  Return only: status, commit SHAs, one-line test summary, concerns.

  Apply all relevant skills, such as (if available) rpi-house-style:coding-effectively.

  Work from: [directory]
</parameter>
</invoke>
```

**For subcomponents** (grouped tasks), extract the subcomponent brief with its letter (`scripts/task-brief PHASE_FILE A`) and dispatch once for the whole group, using the same prompt shape. Ask for one commit per task, or logical commits.

**A dispatch prompt describes one task, not the session's history.** Do not paste accumulated prior-task summaries into later dispatches. A fresh subagent needs its brief, the interfaces it touches, and nothing else. Exact values — numbers, magic strings, signatures, test cases — live only in the brief.

**Print each task-implementor's returned summary** before moving to the next task. If the human wants the detail, point them at the report file.

#### Handling Implementor Status

Every implementor reports one of four statuses. Handle each:

**DONE** — proceed to the next task.

**DONE_WITH_CONCERNS** — read the concerns before proceeding. If they bear on correctness or scope, resolve them now. If they are observations ("this file is getting large"), note them and continue.

**NEEDS_CONTEXT** — supply exactly what was missing and re-dispatch. Consider whether the plan should have carried it; if so, that is a plan gap worth surfacing.

**BLOCKED** — assess the blocker before doing anything else:
1. Context problem → provide more context, re-dispatch
2. Needs more reasoning → re-dispatch on a more capable model
3. Task too large → break it into smaller pieces
4. Plan itself is wrong → escalate to the human

**Never** ignore an escalation, and never force a re-dispatch with nothing changed. If the implementor said it was stuck, something has to change before it tries again.

**No code review between tasks.** Execute all tasks in the phase first.

After all tasks complete, mark "Phase Nb: Execute tasks" as complete.

#### 3c. Code Review for Phase

Mark "Phase Nc: Code review" as in_progress.

**MANDATORY:** Use the `requesting-code-review` skill for the review loop.

**Generate the review package first**, so the reviewer reads one file instead of re-deriving the diff with git commands:

```bash
scripts/review-package [phase BASE SHA] HEAD   # prints e.g. .rpi/exec/review-abc1234..def5678.diff
```

Use the BASE you recorded before the first task — never `HEAD~1`.

**Context to provide:**
- WHAT_WAS_IMPLEMENTED: Summary of all tasks in this phase
- PLAN_OR_REQUIREMENTS: All tasks from this phase
- REVIEW_PACKAGE: path printed by `scripts/review-package`
- BASE_SHA: commit before phase started
- HEAD_SHA: current commit
- IMPLEMENTATION_GUIDANCE: absolute path to `.rpi/implementation-plan-guidance.md` (**only if it exists**—omit entirely if the file doesn't exist)

**Constructing the reviewer prompt:**

- **Never tell a reviewer what not to flag.** If your prompt contains "don't flag X", "at most Minor", "the plan chose this", or "don't treat X as a defect" — stop. You are pre-judging a finding to spare yourself a review cycle. Let the reviewer raise it and adjudicate it in the loop.
- **Don't pre-rate severity.** The reviewer assigns Critical/Important/Minor, not you.
- **Don't add open-ended directives** ("check all uses", "run the race tests if useful") without a concrete, task-specific reason.
- **Don't ask the reviewer to re-run tests the implementor already ran** on the same code — the report carries that evidence.
- **Copy binding constraints verbatim** from the plan: exact values, exact formats, and stated relationships between components ("same layout as X", "matches Y"). The reviewer template already carries the process rules; this block is for what *this* project's spec demands.

**A finding that conflicts with what the plan mandates is the human's decision.** Present the finding beside the plan text and ask which governs. Do not dismiss the finding because the plan required it, and do not dispatch a fix that contradicts the plan without asking. The plan's example code is a starting point, not evidence that its weaknesses were chosen deliberately.

The implementation guidance file contains project-specific coding standards, testing requirements, and review criteria. When provided, the code reviewer should read it and apply those standards during review.

**Note:** Test requirements validation happens at final review, not per-phase. Per-phase reviews focus on code quality and whether the phase includes tests for its functionality.

**If code reviewer returns a context limit error:**

The phase changed too much for a single review. Chunk the review:

1. Identify the midpoint of tasks in the phase
2. Run code review for first half of tasks (commits for tasks 1 through N/2)
3. Fix any issues found
4. Run code review for second half of tasks (commits for tasks N/2+1 through N)
5. Fix any issues found

**When issues are found:**

1. **Create a task for EACH issue** (survives compaction):
   ```
   TaskCreate: "Phase N fix [Critical]: <VERBATIM issue description from reviewer>"
   TaskCreate: "Phase N fix [Important]: <VERBATIM issue description from reviewer>"
   TaskCreate: "Phase N fix [Minor]: <VERBATIM issue description from reviewer>"
   ...one task per issue...
   TaskCreate: "Phase N: Re-review after fixes"
   TaskUpdate: set "Re-review" blocked by all fix tasks
   ```

   **Copy issue descriptions VERBATIM**, even if long. After compaction, the task description is all that remains — it must contain the full issue details for the bug-fixer to understand what to fix.

2. **Dispatch `task-bug-fixer`** with the phase file:

```
<invoke name="Task">
<parameter name="subagent_type">rpi-plan-and-execute:task-bug-fixer</parameter>
<parameter name="description">Fixing review issues for Phase X</parameter>
<parameter name="prompt">
  Fix issues from code review for Phase X.

  Phase file: [absolute path to phase file]

  Code reviewer found these issues:
  [list all issues - Critical, Important, and Minor]

  Read the phase file to understand the tasks and context.

  Your job is to:
  1. Understand root cause of each issue
  2. Apply fixes systematically (Critical → Important → Minor)
  3. Verify with tests/build/lint
  4. Commit your fixes
  5. Report back with evidence

  Work from: [directory]

  Fix ALL issues — including every Minor issue. The goal is ZERO issues on re-review.
  Minor issues are not optional. Do not skip them.

  Re-run the tests covering your changes and report: the covering test files,
  the command you ran, and its output. A one-line fix does not need the whole suite.
</parameter>
</invoke>
```

3. **Mark "Fix issues" complete.** Before re-dispatching the reviewer, confirm the fix report contains the covering test files, the command run, and the output. Once all three are present, re-review per the `requesting-code-review` skill — generating a fresh review package for the new range.

4. **If re-review finds more issues**, create new fix/re-review tasks. Continue loop until zero issues.

5. **Mark "Re-review" complete** when zero issues.

**Plan execution policy (stricter than general code review):**
- ALL issues must be fixed (Critical, Important, AND Minor)
- Ignore APPROVED/BLOCKED status - count issues only
- **Three-strike rule:** If same issues persist after three review cycles, stop and ask human for help

**Minor issues are NOT optional.** Do not rationalize skipping them with "they're just style issues" or "we can fix those later." The reviewer flagged them for a reason. Fix every single one.

**Exit condition:** Zero issues in all categories — including Minor.

Mark "Phase Nc: Code review" as complete.

#### 3d. Move to Next Phase

Proceed to the next phase's "Read" step. Repeat 3a-3c for each phase.

### 4. Update Project Context

After all phases complete, invoke the `rpi-extending-claude:project-claude-librarian` subagent (when available) to review changes and update CLAUDE.md files if needed.

```
<invoke name="Task">
<parameter name="subagent_type">rpi-extending-claude:project-claude-librarian</parameter>
<parameter name="description">Updating project context after implementation</parameter>
<parameter name="prompt">
  Review what changed during this implementation and update CLAUDE.md files if contracts or structure changed.

  Base commit: <commit SHA at start of first phase>
  Current HEAD: <current commit>
  Working directory: <directory>

  Follow the rpi-extending-claude:maintaining-project-context skill to:
  1. Diff against base to see what changed
  2. Identify contract/API/structure changes
  3. Update affected CLAUDE.md files
  4. Commit documentation updates

  Report back with what was updated (or that no updates were needed).
</parameter>
</invoke>
```

**If librarian reports updates:** Review the changes, then proceed to final review.
**If librarian reports no updates needed:** Proceed to final review.
**If librarian subagent is unavailable:** skip this entire step. Say aloud that you're skipping it because the `rpi-extending-claude` plugin is not available.

### 5. Final Review Sequence

After all phases complete, run a sequence of specialized agents:

```
Code Review → Test Analysis (Coverage + Plan)
```

#### 5a. Final Code Review

Use the `requesting-code-review` skill for final code review:

Generate a whole-branch review package first:

```bash
scripts/review-package $(git merge-base main HEAD) HEAD
```

**Context to provide:**
- WHAT_WAS_IMPLEMENTED: Summary of all phases completed
- PLAN_OR_REQUIREMENTS: Reference to the full implementation plan directory
- REVIEW_PACKAGE: path printed by `scripts/review-package`
- BASE_SHA: commit before first phase started
- HEAD_SHA: current commit
- IMPLEMENTATION_GUIDANCE: absolute path (if exists)
- AC_COVERAGE_CHECK: "Verify all acceptance criteria (using scoped format `{slug}.AC*`) from the design plan are covered by at least one phase. Flag any ACs not addressed."

Continue the review loop until zero issues remain.

#### 5b. Test Analysis

**Only after final code review passes with zero issues.**

**Skip this step if test-requirements.md does not exist.**

The test-analyst agent performs two sequential tasks with shared analysis:
1. Validate coverage against acceptance criteria
2. Generate human test plan (only if coverage passes)

Dispatch the test-analyst agent:

```
<invoke name="Task">
<parameter name="subagent_type">rpi-plan-and-execute:test-analyst</parameter>
<parameter name="description">Analyzing test coverage and generating test plan</parameter>
<parameter name="prompt">
Analyze test implementation against acceptance criteria.

TEST_REQUIREMENTS_PATH: [absolute path to test-requirements.md]
WORKING_DIRECTORY: [project root]
BASE_SHA: [commit before first phase]
HEAD_SHA: [current commit]

Phase 1: Validate that automated tests exist for all acceptance criteria.
Phase 2: If coverage passes, generate human test plan using your analysis.

Return coverage validation result. If PASS, include the human test plan.
</parameter>
</invoke>
```

**If analyst returns coverage FAIL:**

1. Dispatch bug-fixer to add missing tests:
   ```
   <invoke name="Task">
   <parameter name="subagent_type">rpi-plan-and-execute:task-bug-fixer</parameter>
   <parameter name="description">Adding missing test coverage</parameter>
   <parameter name="prompt">
   Add missing tests identified by the test analyst.

   Missing coverage:
   [list from analyst output]

   For each missing test:
   1. Read the acceptance criterion carefully
   2. Create the test file at the expected location
   3. Write tests that verify the criterion's actual behavior—not just code that passes, but code that would fail if the criterion weren't met
   4. Run tests to confirm they pass
   5. Commit the new tests

   Work from: [directory]
   </parameter>
   </invoke>
   ```

2. Re-run test-analyst
3. Repeat until coverage PASS or three attempts fail (then escalate to human)

**If analyst returns coverage PASS:**

The response will include the human test plan. Extract the "Human Test Plan" section.

**Write the test plan:**

```bash
# Create test-plans directory if needed
mkdir -p docs/test-plans

# The filename uses the implementation plan directory name
# e.g., impl plan dir: docs/implementation-plans/2025-01-24-oauth/
#       test plan:     docs/test-plans/2025-01-24-oauth.md
```

Write the test plan content to `docs/test-plans/[impl-plan-dir-name].md`, then commit:

```bash
git add docs/test-plans/[impl-plan-dir-name].md
git commit -m "docs: add test plan for [feature name]"
```

Announce: "Human test plan written to `docs/test-plans/[impl-plan-dir-name].md`"

### 6. Complete Development

After final review passes:

- Provide a report to the human operator
  - For each phase:
    - How many tasks were implemented
    - How many review cycles were needed
    - Any compromises made (there should be NO compromises, but if any were made). Examples:
      - "I couldn't run the integration tests, so I continued on"
      - "I couldn't generate the client because the dev environment was down"
      - Note that these are PARTIAL FAILURE CASES and explain to the user what the user must do now.
    - Were any code-review issues left outstanding at any point?

- Activate the `finishing-a-development-branch` skill. DO NOT activate it before this point.

## Common Rationalizations - STOP

| Excuse | Reality |
|--------|---------|
| "I'll read all phases upfront to understand the full picture" | No. Read one phase at a time. Context limits are real. |
| "I'll skip the read step, I remember what's in the file" | No. Always read just-in-time. Context may have been compacted. |
| "I'll review after each task to catch issues early" | No. Review once per phase. Task-level review wastes context. |
| "Context error on review, I'll skip the review" | No. Chunk the review into halves. Never skip review. |
| "Minor issues can wait" | No. Fix ALL issues including Minor. |
