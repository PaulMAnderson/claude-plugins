---
phase: 7
title: Workspace Monitoring Integration
context-budget: medium
files-required:
  - /Users/paul/Claude/claude-plugins/docs/design-plans/2026-03-28-rpi-datasci.md
  - /Users/paul/Claude/claude-plugins/plugins/rpi-plan-and-execute/skills/compressing-context/SKILL.md
depends-on: [phase_06.md]
---

# RPI Data Science Workflow Redesign Implementation Plan

**Goal:** Integrate workspace-wide project monitoring to maintain a central dashboard of all Claude projects.

**Architecture:** This phase ports the `monitor.py` script into the `rpi-plan-and-execute` plugin. This script scans `/Users/paul/Claude/` to classify projects into lifecycle phases. A new `/workspace-dashboard` command is added to display the central `DASHBOARD.md`. The `compressing-context` skill is updated to trigger a monitor scan, ensuring the dashboard remains current.

**Tech Stack:** Python (Scanner), Markdown (Dashboard & Commands).

**Scope:** Phase 7 from original design.

**Codebase verified:** Sunday 29 March 2026

---

## Acceptance Criteria Coverage

This phase implements and tests:

### rpi-datasci.AC7: Workspace Monitoring
- **rpi-datasci.AC7.1 Success:** `plugins/rpi-plan-and-execute/scripts/monitor.py` exists; correctly identifies projects in `/Users/paul/Claude/` and classifies them into one of 10 lifecycle phases
- **rpi-datasci.AC7.2 Success:** `plugins/rpi-plan-and-execute/commands/workspace-dashboard.md` exists; `/workspace-dashboard` command displays the current `DASHBOARD.md` from the workspace root
- **rpi-datasci.AC7.3 Success:** `compressing-context` skill optionally triggers `monitor.py` after writing `PROJECT.md`, ensuring the dashboard reflects the latest project state
- **rpi-datasci.AC7.4 Success:** `.monitor/<project>.json` stubs are generated for each project, following the schema defined in the Monitor design
- **rpi-datasci.AC7.5 Failure:** `monitor.py` fails to exclude itself or hidden directories from the scan

---

<!-- START_SUBCOMPONENT_A (tasks 1-3) -->
<!-- START_TASK_1 -->
### Task 1: Port Workspace Monitor Script

**Verifies:** rpi-datasci.AC7.1, rpi-datasci.AC7.4, rpi-datasci.AC7.5

**Files:**
- Create: `plugins/rpi-plan-and-execute/scripts/monitor.py`

**Implementation:**
- Implement the classification logic:
  - Scans `/Users/paul/Claude/` recursively for directories.
  - Excludes `.git`, `.rpi`, and specifically the `Monitor` project directory itself.
  - Classifies projects into: `empty`, `scaffold`, `static-complete`, `design`, `design-complete`, `implementing`, `active`, `upstream-sync`, `maintenance`, `unknown`.
  - Uses project indicators: `README.md`, `package.json`, `docs/design-plans/`, `docs/implementation-plans/`, `.rpi/todos`.
- Generate output:
  - Writes a JSON stub for each project to `/Users/paul/Claude/.monitor/<project_name>.json`.
  - Generates/updates `/Users/paul/Claude/DASHBOARD.md` summarizing all projects.

**Verification:**
Run: `python3 plugins/rpi-plan-and-execute/scripts/monitor.py`
Expected: `.monitor/` directory populated and `DASHBOARD.md` created in `/Users/paul/Claude/`.

**Commit:** `feat(monitor): port workspace monitoring script`
<!-- END_TASK_1 -->

<!-- START_TASK_2 -->
### Task 2: Implement Workspace Dashboard Command

**Verifies:** rpi-datasci.AC7.2

**Files:**
- Create: `plugins/rpi-plan-and-execute/commands/workspace-dashboard.md`
- Create: `plugins/rpi-plan-and-execute/skills/workspace-dashboard/SKILL.md`

**Implementation:**
- `commands/workspace-dashboard.md`: Slash command `/workspace-dashboard` invoking the skill.
- `skills/workspace-dashboard/SKILL.md`: Skill that simply reads and displays `/Users/paul/Claude/DASHBOARD.md`.

**Verification:**
Run: `/workspace-dashboard`
Expected: The content of the workspace dashboard is displayed in the chat.

**Commit:** `feat(workflow): add workspace-dashboard command`
<!-- END_TASK_2 -->

<!-- START_TASK_3 -->
### Task 3: Trigger Monitor on Compression

**Verifies:** rpi-datasci.AC7.3

**Files:**
- Modify: `plugins/rpi-plan-and-execute/skills/compressing-context/SKILL.md`

**Implementation:**
- Add an instruction to the `compressing-context` skill to run the `monitor.py` script after updating `.rpi/PROJECT.md`.
- This ensures that whenever a project phase changes (e.g., from `implementing` to `active` based on `PROJECT.md` status), the central dashboard is updated immediately.

**Verification:**
Run: `compressing-context` (mock)
Expected: `DASHBOARD.md` is updated reflecting the current project's state.

**Commit:** `feat(skills): trigger workspace monitor on context compression`
<!-- END_TASK_3 -->
<!-- END_SUBCOMPONENT_A -->
