# RPI Data Science Workflow Redesign

## Summary

This design reshapes two existing Claude Code plugins — `rpi-house-style` and `rpi-plan-and-execute` — to better serve a data science and neuroscience context rather than the TypeScript/React web development workflows they were originally built around. The motivation is practical: the tooling no longer reflects the languages and patterns used in the target work (Python, MATLAB, R), and the context-management machinery relies on a crude proxy metric (tool-call count) instead of the real context window fill level. The redesign removes the web stack entirely from the house style plugin, replaces it with three language-specific guides, and upgrades several language-agnostic skills with scientifically relevant examples.

The implementation approach is layered across six phases, each building on the last. A new StatusLine hook feeds real context-window percentages into a shared JSON file on disk, which the existing session-monitor script then reads to decide when to fire compression directives — at natural break points (task completions, test runs) for soft-threshold crossings, and unconditionally for hard-threshold crossings. A persistent `PROJECT.md` file, generated at compression time from git history and session notes, lets agents resume work across context windows without losing track of what has been decided and what remains. Two lighter-weight entry points (`/quick-analysis` and `/helper-function`) are added alongside the existing full planning loop so that small tasks do not require the overhead of a full design-and-execute cycle. Finally, model assignment is tightened so that expensive Opus calls are reserved for design and planning, while implementation, review, and testing agents default to Sonnet.

## 🗂 Memory Tier Index

| Tier | Sections | When to read |
|------|----------|-------------|
| 🔴 **HOT** | DoD, Acceptance Criteria | Always — load before doing anything |
| 🟡 **WARM** | Architecture, Implementation Phases | When planning or implementing a specific phase |
| 🔵 **COLD** | Existing Patterns, Additional Considerations, Glossary | Reference on demand only |

## 🔴 Definition of Done

1. TypeScript/React-specific skills removed (`howto-code-in-typescript`, `programming-in-react`); Postgres skill replaced with a lean generic MySQL/SQL skill (Drizzle ORM references removed)
2. New language-specific house style skills added for Python, MATLAB, and R covering data science conventions for each language
3. Three tiered workflow entry points implemented: `quick-analysis` (no planning, just execute), `helper-function` (lightweight plan + implement), and the existing full RPI loop (for large-scale packages)
4. Fully automated context management: auto-compresses and triggers a fresh session when thresholds are hit (by context size OR progress checkpoint); compress-to-disk-only option also available without session restart
5. Persistent project-level progress log that tracks implementation status and decisions across sessions, designed for resuming work with an agent in a new context window
6. This design supersedes and integrates the existing work-in-progress on the `context-optimization` branch

## 🔴 Acceptance Criteria

### rpi-datasci.AC1 — House Style Cleanup

- **rpi-datasci.AC1.1 Success:** `plugins/rpi-house-style/skills/howto-code-in-typescript/` directory does not exist
- **rpi-datasci.AC1.2 Success:** `plugins/rpi-house-style/skills/programming-in-react/` directory does not exist
- **rpi-datasci.AC1.3 Success:** `plugins/rpi-house-style/skills/property-based-testing/` directory does not exist
- **rpi-datasci.AC1.4 Success:** `plugins/rpi-house-style/skills/howto-develop-with-mysql/SKILL.md` exists; contains MySQL-specific content; no references to Drizzle ORM or TypeScript
- **rpi-datasci.AC1.5 Success:** `coding-effectively`, `howto-functional-vs-imperative`, `defense-in-depth`, `writing-good-tests` skills contain at least one neuroscience or scientific computing example each; no TypeScript-only examples remain
- **rpi-datasci.AC1.6 Failure:** `grep -r "typescript\|drizzle\|React\|\.tsx\|\.ts" plugins/rpi-house-style/skills/` returns matches in retained or new skill files

### rpi-datasci.AC2 — Language-Specific Skills

- **rpi-datasci.AC2.1 Success:** `plugins/rpi-house-style/skills/howto-code-in-python/SKILL.md` exists; covers numpy/scipy/pandas idioms, type hints, virtual environments, matplotlib conventions
- **rpi-datasci.AC2.2 Success:** `plugins/rpi-house-style/skills/howto-code-in-matlab/SKILL.md` exists; covers `arguments` validation blocks, OOP for stateful analysis objects, vectorisation, toolbox organisation
- **rpi-datasci.AC2.3 Success:** `plugins/rpi-house-style/skills/howto-code-in-r/SKILL.md` exists; covers tidyverse vs base R, `renv`, ggplot2, S3/S4 objects, Rmarkdown/Quarto
- **rpi-datasci.AC2.4 Failure:** Any language skill contains examples or patterns specific to a language other than its target

### rpi-datasci.AC3 — Smart Context Monitoring

- **rpi-datasci.AC3.1 Success:** `plugins/rpi-plan-and-execute/hooks/statusline.py` exists; registered in `hooks.json` as a StatusLine hook; outputs a visual bar string
- **rpi-datasci.AC3.2 Success:** StatusLine hook writes `context_window.used_percentage` to `.rpi/context-usage.json` on each invocation
- **rpi-datasci.AC3.3 Success:** `session-monitor.py` reads real % from `.rpi/context-usage.json`; emits WARNING `additionalContext` when ≥ soft threshold (default 50%) at a natural break event
- **rpi-datasci.AC3.4 Success:** `session-monitor.py` emits URGENT `additionalContext` when ≥ hard threshold (default 75%) regardless of break type
- **rpi-datasci.AC3.5 Success:** Natural break detection triggers on: `TaskUpdate` with `status: completed`; Bash calls containing `pytest`, `Rscript`, or `matlab -batch`
- **rpi-datasci.AC3.6 Success:** Thresholds configurable via `RPI_CONTEXT_SOFT_THRESHOLD` and `RPI_CONTEXT_HARD_THRESHOLD` environment variables
- **rpi-datasci.AC3.7 Failure:** `session-monitor.py` uses tool-call counter as primary signal when `.rpi/context-usage.json` exists and is fresh (< 60 seconds old)

### rpi-datasci.AC4 — Project-Level Progress Log

- **rpi-datasci.AC4.1 Success:** Running the `compressing-context` skill produces `.rpi/PROJECT.md` containing: current branch name, last 10 commits (short), implementation status table, decisions log entries
- **rpi-datasci.AC4.2 Success:** `.rpi/PROJECT.md` content is injected into session context by SessionStart hook when the file exists
- **rpi-datasci.AC4.3 Success:** `.rpi/CONTEXT.md` content is also injected by SessionStart hook when present (existing behaviour preserved)
- **rpi-datasci.AC4.4 Failure:** SessionStart hook fails or produces malformed JSON when `.rpi/PROJECT.md` or `.rpi/CONTEXT.md` does not yet exist

### rpi-datasci.AC5 — Tiered Workflow Entry Points

- **rpi-datasci.AC5.1 Success:** `/quick-analysis` command exists; invoking it loads `quick-analysis` skill; skill writes a brief outcome note to `.rpi/SESSION.md` on completion
- **rpi-datasci.AC5.2 Success:** `/helper-function` command exists; invoking it loads `helper-function` skill; skill produces an in-context plan before implementation; writes intent and outcome to `.rpi/SESSION.md`
- **rpi-datasci.AC5.3 Success:** `helper-function` skill instructs spawned subagents to use Sonnet model
- **rpi-datasci.AC5.4 Failure:** Either new skill invokes a design-doc or implementation-plan file write (these are single-session, no persistent plan artifacts)

### rpi-datasci.AC6 — Model Tiering

- **rpi-datasci.AC6.1 Success:** `code-reviewer.md`, `task-bug-fixer.md`, `test-analyst.md` agent files specify Sonnet as their model
- **rpi-datasci.AC6.2 Success:** `starting-a-design-plan` and `starting-an-implementation-plan` skill docs note that Opus is appropriate for design/planning phases
- **rpi-datasci.AC6.3 Failure:** Any implementation agent (`task-implementor-fast`, `code-reviewer`, `task-bug-fixer`, `test-analyst`) specifies Opus as its default model

## 🔵 Glossary

- **RPI loop / full RPI loop**: The existing multi-phase workflow implemented by the `rpi-plan-and-execute` plugin, covering design, planning, implementation, and review.
- **Hot/Cold split**: A skill file organisation pattern where `SKILL.md` holds concise "hot" content loaded on every invocation, and `REFERENCE.md` holds verbose reference material loaded only when needed.
- **StatusLine hook**: A Claude Code hook type that fires on UI status-bar updates. Provides access to `context_window.used_percentage` — the real fill level of the context window.
- **`additionalContext`**: The JSON field in a hook's stdout payload that Claude Code injects into the model's context. Used by session-monitor directives and session-start injection.
- **Natural break event**: A moment in an agent session judged suitable for compression — specifically a `TaskUpdate` with `status: completed`, or a Bash call invoking `pytest`, `Rscript`, or `matlab -batch`.
- **Soft threshold / hard threshold**: Two configurable context-fill levels. Soft (default 50%) triggers a compression warning only at natural break events; hard (default 75%) triggers unconditionally. Configurable via `RPI_CONTEXT_SOFT_THRESHOLD` and `RPI_CONTEXT_HARD_THRESHOLD`.
- **`.rpi/` directory**: A project-local state directory (gitignored) used to persist files across sessions: `SESSION.md`, `CONTEXT.md`, `PROJECT.md`, `context-usage.json`.
- **`PROJECT.md`**: A persistent file written by the `compressing-context` skill recording current branch, recent commits, implementation status table, and decisions log. Designed for cross-session resumption.
- **`CONTEXT.md`**: A compressed summary of the current session written by the `compressing-context` skill and injected on session start.
- **`SESSION.md`**: A running log of outcomes within a session. `quick-analysis` and `helper-function` skills append brief notes to it on completion.
- **`compressing-context` skill**: An existing skill that summarises context to disk, allowing a fresh session to resume without overflow.
- **`session-monitor.py`**: An existing hook script that monitors session state and emits compression directives. Phase 3 upgrades it to use real context percentages.
- **`session-start.sh` / SessionStart hook**: A hook that fires on session start, clear, or resume. Enhanced to inject both `CONTEXT.md` and `PROJECT.md`.
- **Drizzle ORM**: A TypeScript-native database ORM previously referenced in the Postgres skill; removed as part of TypeScript cleanup.
- **`arguments` validation blocks**: A MATLAB language feature (R2019b+) for declarative input validation in functions, replacing manual `narginchk`/`validateattributes` calls.
- **`renv`**: An R package manager for reproducible environments, analogous to Python's `venv`/`pip freeze`.
- **`hypothesis`**: A Python library for property-based testing — generates arbitrary inputs to find edge cases automatically.
- **`hedgehog`**: An R library for property-based testing, the R equivalent of `hypothesis`.
- **Model tiering**: Assigning different Claude model sizes to task types by reasoning demand: Opus for design/planning, Sonnet for implementation/review, Haiku for mechanical hooks.
- **`task-implementor-fast`**: An agent definition in `rpi-plan-and-execute` for implementation subagents; already targets a smaller/faster model.
- **Quarto**: A scientific publishing system built on R Markdown, used for reproducible reporting in R and Python workflows.

## 🟡 Architecture

The redesign modifies two existing plugins: `rpi-house-style` and `rpi-plan-and-execute`. No new plugins are introduced.

**rpi-house-style changes:**
- Remove `howto-code-in-typescript/` and `programming-in-react/` skill directories entirely
- Replace `howto-develop-with-postgres/` with `howto-develop-with-mysql/` (strip Drizzle ORM, keep generic SQL + MySQL patterns)
- Adapt four language-agnostic skills (`coding-effectively`, `howto-functional-vs-imperative`, `defense-in-depth`, `writing-good-tests`) to replace TypeScript examples with neuroscience-relevant equivalents (NaN handling, array shape validation, analysis reproducibility)
- Remove `property-based-testing/` — principles absorbed into language-specific skills
- Add three new language skills: `howto-code-in-python/`, `howto-code-in-matlab/`, `howto-code-in-r/`

**rpi-plan-and-execute changes:**

*Tiered workflows:* Two new entry points added alongside the existing full RPI loop:
- `commands/quick-analysis.md` + `skills/quick-analysis/SKILL.md` — single-shot, no docs, writes brief note to `.rpi/SESSION.md`
- `commands/helper-function.md` + `skills/helper-function/SKILL.md` — in-context plan + implement + test, writes intent/outcome to `.rpi/SESSION.md`

*Context monitoring stack* (layered, all writing to `.rpi/`):
- **StatusLine hook** (`hooks/statusline.py`): reads real `context_window.used_percentage` from hook stdin; writes to `.rpi/context-usage.json`; renders visual bar in terminal status line
- **session-monitor.py** (enhanced): reads `.rpi/context-usage.json` for real %; detects natural break events (TaskUpdate completed, test tool calls, code review invocations); fires compress directive when above 50% at a break OR above 75% at any time
- **SessionStart hook** (enhanced): reads `.rpi/CONTEXT.md` and `.rpi/PROJECT.md` and injects both into session context on every start/clear/resume

*Project-level log:* `compressing-context` skill enhanced to also generate/update `.rpi/PROJECT.md` by reading `git log` and `git status` output — accumulates implementation status, decision log, and current branch state across sessions.

*Model tiering:* Agent `.md` files and skill prompts updated to default subagents to Sonnet; Opus reserved for design/planning phases only; hook scripts use Haiku where model selection applies.

## 🔵 Existing Patterns

**Hooks:** `hooks/hooks.json` registers hook types with a `command` field pointing to a script path using `${CLAUDE_PLUGIN_ROOT}`. Scripts write JSON to stdout. `session-monitor.py` already follows this pattern; `statusline.py` extends it for the new StatusLine event type.

**Skills:** Each skill is a directory under `skills/{name}/` containing `SKILL.md`. The Hot/Cold split (`SKILL.md` + `REFERENCE.md`) introduced in the context-optimization branch is an established pattern — language skills follow it where appropriate.

**Commands:** Slash commands are `.md` files in `commands/` that invoke a skill by reference. `quick-analysis` and `helper-function` follow the same pattern as existing `compress-context.md` and `start-design-plan.md`.

**`.rpi/` directory:** Project-local state directory (gitignored). Already contains `context-monitor-count`, `journal.json`, `SESSION.md`, `CONTEXT.md`. `PROJECT.md` and `context-usage.json` extend this pattern.

**Session injection:** `session-start.sh` already reads a skill file and injects it as `additionalContext`. Enhanced version reads multiple files from `.rpi/` and concatenates them.

## 🟡 Implementation Phases

<!-- START_PHASE_1 -->
### Phase 1: House Style Cleanup

**Goal:** Remove TypeScript/React skills; adapt four generic skills for neuroscience; replace Postgres skill with MySQL.

**Components:**
- Delete: `plugins/rpi-house-style/skills/howto-code-in-typescript/` (entire directory including `type-fest.md`, `typebox.md`)
- Delete: `plugins/rpi-house-style/skills/programming-in-react/` (entire directory including `react-testing.md`, `useEffect-deep-dive.md`)
- Delete: `plugins/rpi-house-style/skills/property-based-testing/`
- Replace: `plugins/rpi-house-style/skills/howto-develop-with-postgres/` → `howto-develop-with-mysql/` (rewrite `SKILL.md`, remove `typescript-drizzle.md`)
- Adapt: `plugins/rpi-house-style/skills/coding-effectively/SKILL.md` — strip TS-specific content, add neuroscience examples (array shape handling, NaN propagation, analysis script organisation)
- Adapt: `plugins/rpi-house-style/skills/howto-functional-vs-imperative/SKILL.md` — reframe examples for Python/MATLAB/R scientific code
- Adapt: `plugins/rpi-house-style/skills/defense-in-depth/SKILL.md` — replace TS examples with neuroscience failure modes (timestamp misalignment, out-of-range values, mismatched array dimensions)
- Adapt: `plugins/rpi-house-style/skills/writing-good-tests/SKILL.md` — use Python/MATLAB/R test framework examples; note relevance is primarily for large-scale packages

**Dependencies:** None

**Done when:** No TypeScript/React/Postgres references remain in `rpi-house-style`; adapted skills contain neuroscience-relevant examples; MySQL skill exists with accurate SQL/MySQL content
<!-- END_PHASE_1 -->

<!-- START_PHASE_2 -->
### Phase 2: Language-Specific House Style Skills

**Goal:** Add Python, MATLAB, and R skills covering data science conventions.

**Components:**
- Create: `plugins/rpi-house-style/skills/howto-code-in-python/SKILL.md` — numpy/scipy/pandas idioms, type hints for array shapes, virtual environments, structuring analysis scripts vs packages, matplotlib/seaborn conventions, property-based testing with `hypothesis`
- Create: `plugins/rpi-house-style/skills/howto-code-in-matlab/SKILL.md` — script vs function files, modern `arguments` validation blocks, vectorisation over loops, avoiding global state, object-oriented patterns for stateful analysis (recording sessions, spike sorters, preprocessing pipelines), toolbox organisation for large packages
- Create: `plugins/rpi-house-style/skills/howto-code-in-r/SKILL.md` — tidyverse vs base R trade-offs, reproducible analysis with `renv`, ggplot2 conventions, S3 vs S4 objects for analysis objects, Rmarkdown/Quarto for reporting, property-based testing with `hedgehog`

**Dependencies:** Phase 1 (house style cleanup complete)

**Done when:** All three skills exist with language-appropriate examples; MATLAB skill explicitly covers argument blocks and OOP state patterns; Python skill covers scientific stack conventions
<!-- END_PHASE_2 -->

<!-- START_PHASE_3 -->
### Phase 3: Smart Context Monitoring

**Goal:** Replace tool-call-count proxy with real context percentage; add natural-break detection; add visual StatusLine display.

**Components:**
- Create: `plugins/rpi-plan-and-execute/hooks/statusline.py` — reads `context_window.used_percentage` from StatusLine hook stdin; writes to `.rpi/context-usage.json`; outputs visual bar string (e.g. `[████████░░░░░░░░] 52% · ⚠ compress at next break`)
- Register: StatusLine hook entry in `plugins/rpi-plan-and-execute/hooks/hooks.json`
- Enhance: `plugins/rpi-plan-and-execute/hooks/session-monitor.py` — read real % from `.rpi/context-usage.json` instead of tool count; detect natural break events (TaskUpdate with `status: completed`, Bash calls matching test patterns: `pytest`, `Rscript`, `matlab -batch`; code review invocations); fire WARNING directive above 50% at a break; fire URGENT directive above 75% at any time; configurable via `RPI_CONTEXT_SOFT_THRESHOLD` (default 50) and `RPI_CONTEXT_HARD_THRESHOLD` (default 75)

**Dependencies:** Phase 1 (hooks infrastructure unchanged, extends existing)

**Done when:** StatusLine shows visual bar with real %; `.rpi/context-usage.json` is written on each StatusLine event; session-monitor triggers correctly at soft threshold on natural breaks and hard threshold unconditionally
<!-- END_PHASE_3 -->

<!-- START_PHASE_4 -->
### Phase 4: Project-Level Progress Log

**Goal:** Add persistent `PROJECT.md` generated from git state at compress time; inject into every session start.

**Components:**
- Enhance: `plugins/rpi-plan-and-execute/skills/compressing-context/SKILL.md` — add instruction to generate/update `.rpi/PROJECT.md` by reading `git log --oneline -10` and `git status` output; format as: current branch, recent commits, implementation status table (manually maintained section), decisions log (appended from session journal), open questions
- Enhance: `plugins/rpi-plan-and-execute/hooks/session-start.sh` — read `.rpi/CONTEXT.md` and `.rpi/PROJECT.md` (if they exist) and include their content in the `additionalContext` payload alongside the existing skill injection

**Dependencies:** Phase 3 (session-monitor and compression infrastructure stable)

**Done when:** Compressing context produces both `.rpi/CONTEXT.md` and `.rpi/PROJECT.md`; SessionStart injects both files when present; new session after `/clear` begins with project state visible
<!-- END_PHASE_4 -->

<!-- START_PHASE_5 -->
### Phase 5: Tiered Workflow Entry Points

**Goal:** Add `quick-analysis` and `helper-function` as lightweight alternatives to the full RPI loop.

**Components:**
- Create: `plugins/rpi-plan-and-execute/commands/quick-analysis.md` — slash command invoking the skill
- Create: `plugins/rpi-plan-and-execute/skills/quick-analysis/SKILL.md` — load `.rpi/CONTEXT.md` if present; execute task directly with no design doc or plan file; write brief outcome note to `.rpi/SESSION.md` on completion
- Create: `plugins/rpi-plan-and-execute/commands/helper-function.md` — slash command invoking the skill
- Create: `plugins/rpi-plan-and-execute/skills/helper-function/SKILL.md` — load `.rpi/CONTEXT.md` if present; produce brief in-context plan (2-3 bullet intent); implement + test in single session using Sonnet subagents; write intent and outcome to `.rpi/SESSION.md`

**Dependencies:** Phase 4 (SESSION.md and CONTEXT.md infrastructure in place)

**Done when:** Both `/quick-analysis` and `/helper-function` commands exist and invoke their skills; skills write to `.rpi/SESSION.md`; helper-function skill instructs subagents to use Sonnet
<!-- END_PHASE_5 -->

<!-- START_PHASE_6 -->
### Phase 6: Model Tiering

**Goal:** Set correct default models across agents and skill prompts; reserve Opus for design/planning only.

**Components:**
- Update: `plugins/rpi-plan-and-execute/agents/task-implementor-fast.md` — confirm default is Sonnet (already named "fast", verify frontmatter)
- Update: `plugins/rpi-plan-and-execute/agents/code-reviewer.md` — set default to Sonnet (currently likely Opus)
- Update: `plugins/rpi-plan-and-execute/agents/task-bug-fixer.md` — set default to Sonnet
- Update: `plugins/rpi-plan-and-execute/agents/test-analyst.md` — set default to Sonnet
- Update: `plugins/rpi-basic-agents/agents/haiku-general-purpose.md` — confirm Haiku; used by hooks and mechanical subagents
- Document in `plugins/rpi-plan-and-execute/skills/starting-a-design-plan/SKILL.md` and `starting-an-implementation-plan/SKILL.md`: Opus is appropriate for design/planning phases; Sonnet for implementation

**Dependencies:** Phase 5 (all new skills/agents exist before model assignments are set)

**Done when:** Agent files reflect intended models; code-reviewer, bug-fixer, and test-analyst default to Sonnet; design/planning skill docs note Opus rationale
<!-- END_PHASE_6 -->

## 🔵 Additional Considerations

**Superseding context-optimization branch work:** The existing untracked files under `docs/implementation-plans/2026-03-26-context-optimization/` describe Phase 1 (Hot/Cold skill split) work. Phase 1 of this design supersedes that — the TypeScript skill being split is now removed entirely. The session-monitor enhancements in Phase 3 here supersede the Phase 2-4 work described in those plans. Those files should be removed before implementing this design.

**StatusLine hook timing:** The StatusLine hook fires on UI updates, not on every tool call. There may be a brief lag between a tool completing and `.rpi/context-usage.json` reflecting the updated percentage. `session-monitor.py` should handle a missing or stale `context-usage.json` gracefully (fall back to tool-count proxy if file is absent or older than 60 seconds).

**`.rpi/PROJECT.md` implementation status table:** The "Implementation Status" table in `PROJECT.md` cannot be fully auto-generated from git alone — it requires Claude to maintain it. The compression skill should instruct Claude to update the table based on recent commits and session journal, not just copy git log.
