# Project Tracking Design

## Summary
The project uses a shared `.astrolabe/` directory to keep each project's description, current status, history, deferred work, and planning documents in plain Markdown files. Four skill tiers—Micro, Quick, Spec, and Full—use the same entry and exit rules: initialize missing state, consult planned work, then update status and append an outcome. The new Spec tier adds a resumable checklist between lightweight work and the full design and implementation workflow.

Claude Code, Codex CLI, and Gemini CLI follow one documented file format while retaining tool-specific skill instructions. A future Hypercube service can read the versioned `STATUS.md` contract for projects explicitly added to its watch-list; projects remain usable locally without registration or network access. The migration renames the current RPI plugins and consolidates their project files under `.astrolabe/`.

## 🗂 Memory Tier Index

| Tier | Sections | When to read |
|------|----------|--------------|
| 🔴 **HOT** | Definition of Done, Acceptance Criteria | Always; these define the intended result |
| 🟡 **WARM** | Architecture, Implementation Phases | When planning or implementing a phase |
| 🔵 **COLD** | Glossary, Existing Patterns, Additional Considerations | Reference when needed |

## 🔴 Definition of Done
1. Rename `rpi-*` to `astrolabe-*` across plugin directories, manifests, `marketplace.json`, `CHANGELOG.md`, and docs (full migration, not a going-forward-only rename).
2. Extend the `.rpi/` (→ `.astrolabe/`) per-project state format with an append-only history log, an active backlog, and an explicit future-roadmap list distinct from the backlog.
3. Add a new intermediate scope tier between `quick-analysis` and full `starting-a-design-plan`, for jobs that want a written spec and step tracking without the full design-doc/implementation-plan/code-review cycle.
4. Existing and new skills auto-initialize this state if missing, consult the backlog/roadmap before starting work (so already-planned-for-later work can be deferred rather than redone or duplicated), and log outcomes at the tier-appropriate level of detail.
5. Design (not build) a cross-project registry concept intended for a Hypercube-hosted service to read later, so a future website/dashboard could show status across all tracked projects.
6. Everything continues to work fully local and untracked with zero setup, for one-off projects that never register with the central system.

**Explicitly out of scope:** vector DB / embedding search, remote-trigger or push-notification features, multi-user support or auth, actually building the website/dashboard (architecture must not preclude it, but building it is a separate effort).

## 🔴 Acceptance Criteria
### project-tracking.AC1: Rename and migration
- **project-tracking.AC1.1 Success:** Claude plugin directories, manifest names, marketplace entries, active skill references, and current documentation use `astrolabe-*`.
- **project-tracking.AC1.2 Success:** Codex skill names and Gemini extension names and references use Astrolabe naming.
- **project-tracking.AC1.3 Success:** Scripts and hooks read and write `.astrolabe/` paths; existing design and implementation documents in this repository are moved there.
- **project-tracking.AC1.4 Failure:** No active reference points to a removed `rpi-*` path or name; historical changelog text remains intelligible.

### project-tracking.AC2: Per-project state
- **project-tracking.AC2.1 Success:** A fresh project initializes the documented `.astrolabe/` structure with valid `PROJECT.md`, `STATUS.md`, `HISTORY.md`, and `PLANNED.md`.
- **project-tracking.AC2.2 Success:** `HISTORY.md` gains an entry without losing prior entries; `STATUS.md` reflects the latest state; `CONTEXT.md` keeps its resume-summary role.
- **project-tracking.AC2.3 Success:** Backlog and Roadmap are separate lists with stable, unique `B` and `R` identifiers.
- **project-tracking.AC2.4 Edge:** Repeat initialization preserves existing project state.

### project-tracking.AC3: Spec tier
- **project-tracking.AC3.1 Success:** The new skill creates a dated spec with intent, numbered steps, notes, and status.
- **project-tracking.AC3.2 Success:** A later invocation resumes the same spec and preserves completed steps and notes.
- **project-tracking.AC3.3 Success:** Completion marks the spec done, updates project status, and records the outcome in history.
- **project-tracking.AC3.4 Edge:** When architectural exploration or full acceptance criteria are needed, the skill directs work to the design tier using the existing spec as context.

### project-tracking.AC4: Shared tier behavior
- **project-tracking.AC4.1 Success:** Each tier initializes missing state and reads project description and status before work.
- **project-tracking.AC4.2 Success:** Each tier records an outcome at its documented level of detail and updates `STATUS.md`.
- **project-tracking.AC4.3 Success:** Before starting, each tier checks Backlog and Roadmap; a matching item is shown to the user before proceeding.
- **project-tracking.AC4.4 Edge:** No match allows work to proceed without an extra decision.
- **project-tracking.AC4.5 Success:** A deferred idea can be added to the chosen list with the next unused ID; declining the offer leaves `PLANNED.md` unchanged.

### project-tracking.AC5: Future registry contract
- **project-tracking.AC5.1 Success:** `STATUS.md` follows the documented versioned schema after an exit from every tier.
- **project-tracking.AC5.2 Success:** The design specifies a Hypercube-side watch-list and pull-based read of registered projects’ `STATUS.md` files.
- **project-tracking.AC5.3 Edge:** A project absent from the watch-list remains invisible to the future registry without affecting local tracking.

### project-tracking.AC6: Local operation and portability
- **project-tracking.AC6.1 Success:** All tiers work in a fresh local project without registration, network access, credentials, or a running service.
- **project-tracking.AC6.2 Success:** Claude, Codex, and Gemini instructions refer to the same documented state format and expose equivalent entry and exit behavior.

## 🔵 Glossary
- **Astrolabe:** The renamed skill and project-state system described in this design.
- **RPI:** The previous name of the workflow and plugins being renamed to Astrolabe.
- **Hypercube:** The host intended to run the future cross-project registry service.
- **Tier:** A level of workflow formality. Micro and Quick log short outcomes; Spec tracks a resumable task; Full uses design and implementation plans.
- **Spec:** A dated, resumable task document with intent, numbered steps, notes, and completion status.
- **Backlog:** Concrete work planned for a future, relatively near-term effort in `PLANNED.md`.
- **Roadmap:** Less defined or longer-term ideas kept separately from the Backlog in `PLANNED.md`.
- **Frontmatter:** Structured fields between `---` delimiters at the start of a Markdown file, used here for machine-readable status and spec metadata.
- **Slug:** The short file-safe work name used in dated document paths and `STATUS.md`.
- **Watch-list:** The Hypercube-side list of project locations the future registry reads; registration means adding a project to this list.
- **Append-only history:** A log whose existing entries are preserved when new outcomes are recorded.

## 🟡 Architecture

The design has two layers: a **per-project state format** (`.astrolabe/`) that any tool can read/write with plain file I/O, and a **tier ladder** of skills that read and write it at increasing levels of formality.

**Per-project directory** (replaces both `.rpi/` and root-level `docs/design-plans`/`docs/implementation-plans`):

```
.astrolabe/
  PROJECT.md                        # stable, human-authored description
  STATUS.md                         # machine-updated live snapshot (frontmatter + 1 line)
  HISTORY.md                        # append-only event log (renamed from SESSION.md)
  CONTEXT.md                        # compressed session-resume summary (unchanged behavior)
  PLANNED.md                        # ## Backlog / ## Roadmap, flat lists with IDs (B1, R1, ...)
  docs/
    specs/YYYY-MM-DD-{slug}.md      # new Spec tier
    design-plans/YYYY-MM-DD-{slug}.md
    implementation-plans/{slug}/...
```

**`STATUS.md` contract** (the file a future Hypercube scanner reads — the only cross-project touchpoint this design commits to):

```yaml
---
schema_version: 1
status: active | paused | archived
current_tier: none | micro | quick | spec | design
current_work: <slug> | null
last_updated: <ISO 8601 timestamp>
---
<one human-readable line, e.g. "Implementing Phase 3 of project-tracking design.">
```

**Tier ladder** — four tiers, each writing a bigger slice of `.astrolabe/`:

| Tier | Skill | Writes | Escalates when |
|---|---|---|---|
| Micro | `helper-function` | `HISTORY.md` | scope grows beyond one function |
| Quick | `quick-analysis` | `HISTORY.md` | needs multi-session persistence or a real deliverable |
| Spec (new) | `starting-a-tracked-task` | `docs/specs/{slug}.md` + `HISTORY.md` | needs architectural exploration, multiple approaches, or AC-level rigor |
| Full | `starting-a-design-plan` → `starting-an-implementation-plan` | `docs/design-plans/`, `docs/implementation-plans/`, `CONTEXT.md`, `HISTORY.md` | (unchanged) |

Escalation between tiers means starting the next tier's skill against the same slug — no data migration, since `HISTORY.md` already holds the trail and the new tier reads the prior tier's file as context.

**Common entry/exit contract, shared by all four tiers:**
- **Entry:** initialize `.astrolabe/` with empty `PROJECT.md`/`STATUS.md`/`HISTORY.md`/`PLANNED.md` if absent → read `PROJECT.md` + `STATUS.md` → read `PLANNED.md` and check the requested work against existing Backlog/Roadmap entries; surface a match to the user rather than deciding silently.
- **Exit:** update `STATUS.md`; append one entry to `HISTORY.md`; if the work surfaced an out-of-scope idea, offer to add it to `PLANNED.md` (Backlog if concrete/near-term, Roadmap if vague/long-term).

This matching is prompt-driven (an agent reading `PLANNED.md` prose and comparing it to the request), not code-driven — consistent with how `.rpi/design-plan-guidance.md` is already conditionally read today, and appropriate at personal-project scale rather than building a keyword-matching layer.

**Cross-project registry (pull-based, design only):** a Hypercube-side service maintains its own watch-list of project repos/paths (config lives on Hypercube, not on any dev machine) and periodically reads each one's `.astrolabe/STATUS.md`. Registering a project centrally means adding it to that watch-list — an explicit action, not auto-discovery — which is what makes untracked one-off projects work for free: absence from the watch-list means invisible to Hypercube, but `.astrolabe/` still works standalone. No dev-machine agent, daemon, or credentials are required; the only project-side obligation is that `STATUS.md` stays current, which the tier contract above already guarantees. A future push-based agent would just be another writer of the same `STATUS.md` contract, not a redesign.

**Cross-tool portability:** the `.astrolabe/` file formats above carry no tool-specific vocabulary, so Claude Code, Codex CLI, and Gemini CLI can all read/write them with plain file I/O. The format is documented once, in `docs/astrolabe-state-format.md` at the repo root, which all three tool variants of every skill reference instead of re-describing inline. The skill *instructions* that act on this format still need hand-mirroring per tool (Codex uses a different `NOTICE.md` + `SKILL.md` structure and shortened names; Gemini uses different tool vocabulary — `ask_user`/`write_todos` vs. `AskUserQuestion`/`TaskCreate`) — no generator or symlink scheme replaces this, per the portability research.

## 🔵 Existing Patterns

This design extends rather than replaces two patterns already present in `plugins/rpi-plan-and-execute` (renamed to `plugins/astrolabe-plan-and-execute` in Phase 1):

- **The two-tier split** (`helper-function`/`quick-analysis` logging only to `.rpi/SESSION.md`, vs. `starting-a-design-plan`/`starting-an-implementation-plan` writing full `docs/design-plans/`+`docs/implementation-plans/`) already exists. This design inserts one new tier (Spec) between them rather than inventing a new ladder.
- **Conditional file reads** — `.rpi/design-plan-guidance.md` is already read by `starting-a-design-plan` only if it exists, with no error if it's absent. The auto-init and backlog-check behavior in every tier's entry step follows this same "read if present, initialize if absent" convention.
- **Regenerated vs. append-only state** — `CONTEXT.md` (regenerated by `compressing-context`) and `SESSION.md` (append-only, written by the lightweight tiers) already encode the event-sourced split this design formalizes. `STATUS.md` takes over `CONTEXT.md`'s "cheap, regenerated, machine-relevant" role for cross-project status specifically; `HISTORY.md` is `SESSION.md` renamed with its append-only role made explicit and extended to all four tiers, not just the two lightweight ones.
- **Programmatic path dependency** — investigation found `.rpi/` is not purely a documented convention: `plugins/rpi-plan-and-execute/scripts/{rpi-workspace,task-brief,review-package}` and `plugins/rpi-plan-and-execute/hooks/session-start.sh` hardcode `.rpi/` paths. Phase 1 must update these scripts/hooks to the new `.astrolabe/` layout, not just rename skill prose.

No existing pattern covers cross-project awareness or a machine-readable status contract — `STATUS.md` and the Hypercube watch-list concept are new.

## 🟡 Implementation Phases

<!-- START_PHASE_1 -->
### Phase 1: Rename and Directory Consolidation
**Goal:** Rebrand `rpi-*` to `astrolabe-*` everywhere and consolidate per-project state into the new `.astrolabe/` layout, in one pass so files aren't moved twice.

**Components:**
- 8 plugin directories under `plugins/` (`rpi-basic-agents`, `rpi-research-agents`, `rpi-hook-skill-reinforcement`, `rpi-getting-started`, `rpi-extending-claude`, `rpi-house-style`, `rpi-plan-and-execute`, `rpi-hook-claudemd-reminder`) → `astrolabe-*`, via `git mv`; matching Gemini extension directories and Codex skill directories are renamed in this phase so the full migration stays in sync
- `name` fields in each plugin's `.claude-plugin/plugin.json` (10 files) and all entries in root `.claude-plugin/marketplace.json`
- `rpi-<plugin>:<skill>` cross-references inside skill markdown bodies (~200+ occurrences) — reviewed individually, not blind-substituted, since some instances are the methodology name ("the RPI loop" → "the Astrolabe workflow") rather than a plugin prefix
- Path constants in `plugins/astrolabe-plan-and-execute/scripts/{rpi-workspace,task-brief,review-package}` and `plugins/astrolabe-plan-and-execute/hooks/session-start.sh`, updated to read/write the new `.astrolabe/` layout (Phase 1 owns both the rename and the directory-shape change to avoid a second migration)
- `CLAUDE.md` references to `rpi-`; a new `CHANGELOG.md` entry documenting the rename (existing historical entries stay as written)
- `docs/design-plans/` and `docs/implementation-plans/` moved to `.astrolabe/docs/design-plans/` and `.astrolabe/docs/implementation-plans/` (existing 3 design-plan files and their implementation-plan directories relocated with `git mv`)

**Dependencies:** None (first phase).

**Done when:** No active names, paths, or references use `rpi` in the Claude, Codex, or Gemini distributions; historical records may retain their original names. All plugins and extensions load under their new names; `astrolabe-workspace`/`task-brief`/`review-package`/`session-start.sh` operate against `.astrolabe/` paths. Covers `project-tracking.AC1.*`; verify with a reference sweep, path checks, and plugin load checks.
<!-- END_PHASE_1 -->

<!-- START_PHASE_2 -->
### Phase 2: Core State Files and Auto-Init/Read Behavior
**Goal:** Define the `.astrolabe/` file formats and wire every existing tier skill to auto-initialize and read them on entry, and update them on exit.

**Components:**
- `docs/astrolabe-state-format.md` at repo root — canonical schema for `PROJECT.md`, `STATUS.md` (frontmatter shape from Architecture), `HISTORY.md` (entry shape: timestamp, tier, intent, outcome), `PLANNED.md` (Backlog/Roadmap entry shape with `B{n}`/`R{n}` IDs)
- Entry/exit behavior added to `plugins/astrolabe-plan-and-execute/skills/{helper-function,quick-analysis,starting-a-design-plan,starting-an-implementation-plan}/SKILL.md`: auto-init `.astrolabe/` if absent, read `PROJECT.md`/`STATUS.md` on entry, update `STATUS.md` and append `HISTORY.md` on exit
- `plugins/astrolabe-plan-and-execute/skills/compressing-context/SKILL.md` updated to write `CONTEXT.md` under the new `.astrolabe/` path (behavior otherwise unchanged)

**Dependencies:** Phase 1 (new paths and plugin names must exist first).

**Done when:** Running any of the four existing tier skills against a project with no `.astrolabe/` directory creates one with correctly-shaped empty files; running them again updates `STATUS.md` and appends to `HISTORY.md`. Covers `project-tracking.AC2.1`–`AC2.2`, `project-tracking.AC2.4`, and `project-tracking.AC4.1`–`AC4.2` (see Acceptance Criteria) — verified with tests that run each skill against a fixture project directory and assert on file contents before/after.
<!-- END_PHASE_2 -->

<!-- START_PHASE_3 -->
### Phase 3: Backlog and Roadmap Consultation Behavior
**Goal:** Add the "check before starting" step to every tier so already-planned work is surfaced instead of silently duplicated.

**Components:**
- Shared instruction block (referenced by all tier skills per Architecture's entry contract) describing: read `PLANNED.md` in full, compare requested work against Backlog/Roadmap entries, surface a match via AskUserQuestion-style prompt ("work item B3 instead, extend it, or proceed separately?") before continuing
- Exit-time instruction added to each tier skill: if the work surfaces an out-of-scope idea, offer to append it to `PLANNED.md` under Backlog or Roadmap with the next available ID

**Dependencies:** Phase 2 (`PLANNED.md` must exist and be auto-initialized first).

**Done when:** A skill run against a project whose `PLANNED.md` contains a matching entry surfaces that entry before proceeding; a skill run that surfaces a new deferred idea successfully appends it to `PLANNED.md` with a correctly incremented ID. Covers `project-tracking.AC2.3` and `project-tracking.AC4.3`–`AC4.5` — verified with tests using fixture `PLANNED.md` files with and without matching entries.
<!-- END_PHASE_3 -->

<!-- START_PHASE_4 -->
### Phase 4: New Spec Tier Skill
**Goal:** Add the intermediate tier between `quick-analysis` and `starting-a-design-plan`.

**Components:**
- `plugins/astrolabe-plan-and-execute/skills/starting-a-tracked-task/SKILL.md` — new skill: gathers intent, writes `docs/specs/YYYY-MM-DD-{slug}.md` (frontmatter: `status: in_progress|done`, `tier: spec`; body: intent, numbered checklist, notes), mutates checkboxes in place as steps complete, logs to `HISTORY.md` on completion
- Escalation note in `starting-a-tracked-task` pointing to `starting-a-design-plan` when scope grows; corresponding de-escalation note in `quick-analysis`/`helper-function` pointing up to this new skill
- Corresponding command file under `plugins/astrolabe-plan-and-execute/commands/` (matching the existing pattern of one command per orchestrating skill, e.g. `start-design-plan.md`)

**Dependencies:** Phases 2 and 3 (auto-init and backlog-consultation behavior apply to this skill too, per the shared entry/exit contract).

**Done when:** Running the new skill against a project creates a correctly-shaped `docs/specs/{slug}.md`, updates its checkboxes across multiple invocations, and logs to `HISTORY.md` on completion. Covers `project-tracking.AC3.*` — verified with tests covering spec creation, in-place checkbox mutation, and completion logging.
<!-- END_PHASE_4 -->

<!-- START_PHASE_5 -->
### Phase 5: STATUS.md Contract Finalization
**Goal:** Harden the one file a future Hypercube scanner depends on, since it's the sole cross-project contract this design commits to.

**Components:**
- Validation of the `STATUS.md` frontmatter shape (Architecture section) against all four tiers' exit behavior, confirming `current_tier`/`current_work`/`last_updated` are set consistently regardless of which skill last touched the project
- `docs/astrolabe-state-format.md` updated with the finalized `STATUS.md` schema, including the `schema_version` field introduced with the initial format, so a future Hypercube scanner can detect format changes

**Dependencies:** Phases 2-4 (all tiers must already be writing `STATUS.md`).

**Done when:** `STATUS.md` after any tier's exit validates against the documented schema, including `schema_version`. Covers `project-tracking.AC5.1` with a schema-validation test against output from each tier. Covers the design-only `project-tracking.AC5.2`–`AC5.3` through review of the documented watch-list and local-operation contract.
<!-- END_PHASE_5 -->

<!-- START_PHASE_6 -->
### Phase 6: Codex and Gemini Mirroring
**Goal:** Bring the Codex CLI and Gemini CLI skill variants up to date with the new/changed skills from Phases 2-4.

**Components:**
- `codex/skills/` — new `astrolabe-spec/SKILL.md` and `NOTICE.md` for the Spec tier; auto-init/backlog-consultation instructions added to existing Codex skill equivalents
- `gemini/extensions/astrolabe-plan-and-execute/skills/` — new Spec-tier skill mirrored from the Claude version with Gemini tool vocabulary (`ask_user`/`write_todos`); same auto-init/backlog-consultation additions
- Sync checklist documented in `CLAUDE.md` (or a new `docs/skill-sync-checklist.md`) listing the three locations any future skill change must touch

**Dependencies:** Phases 2-4 (mirrors content that must already be finalized on the Claude side).

**Done when:** Codex and Gemini variants exist for the new Spec tier and reflect the auto-init/backlog behavior; the sync checklist is committed. Covers `project-tracking.AC6.1`–`AC6.2`; verify each tool loads the skill and, in a local fixture, follows the same state contract without registration or network access.
<!-- END_PHASE_6 -->

## 🔵 Additional Considerations

**Rename risk:** the ~200+ `rpi-<plugin>:<skill>` cross-references are regular enough to script-generate candidates for, but each should be diffed rather than blindly substituted, since a handful of prose mentions of "RPI" refer to the methodology name rather than a literal plugin prefix (both convert to "Astrolabe" per the confirmed scope, but conflating the two during scripting risks mangled sentences, not incorrect references).

**Deferred, not designed here:** the actual Hypercube scanning service/script and the website/dashboard that renders the aggregated view. Two items are earmarked as the first two entries to seed in this repo's own `.astrolabe/PLANNED.md` once Phase 6 lands (dogfooding): (1) the Hypercube crawler + minimal web UI, and (2) a legacy `.rpi/` → `.astrolabe/` migration script/skill for other projects that already accumulated history under the old layout — distinct from Phase 1's in-repo rename, which only affects this `claude-plugins` repo.

**No migration path for other projects in this plan:** projects other than this repo that already have `.rpi/PROJECT.md`/`CONTEXT.md`/`SESSION.md` from using the pre-rename skills are not migrated by this plan. They keep working under the old layout until the deferred migration skill (above) exists.
