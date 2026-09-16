---
phase: 1
title: House Style Cleanup
context-budget: medium
files-required:
  - /Users/paul/Claude/claude-plugins/docs/design-plans/2026-03-28-rpi-datasci.md
  - /Users/paul/Claude/claude-plugins/plugins/rpi-house-style/skills/coding-effectively/SKILL.md
  - /Users/paul/Claude/claude-plugins/plugins/rpi-house-style/skills/howto-functional-vs-imperative/SKILL.md
  - /Users/paul/Claude/claude-plugins/plugins/rpi-house-style/skills/defense-in-depth/SKILL.md
  - /Users/paul/Claude/claude-plugins/plugins/rpi-house-style/skills/writing-good-tests/SKILL.md
  - /Users/paul/Claude/claude-plugins/plugins/rpi-house-style/skills/howto-develop-with-postgres/SKILL.md
depends-on: []
---

# RPI Data Science Workflow Redesign Implementation Plan

**Goal:** Remove TypeScript/React-specific skills and adapt generic engineering skills for a neuroscience and data science context.

**Architecture:** This phase performs a "house cleaning" of the `rpi-house-style` plugin. It deletes obsolete web development skills, replaces the Postgres skill with a lean MySQL equivalent, and reframes generic engineering principles using neuroscience-relevant examples (array shape handling, NaN propagation, etc.).

**Tech Stack:** Markdown (Skills), Python/MATLAB/R (Examples), SQL (MySQL).

**Scope:** Phase 1 from original design.

**Codebase verified:** Sunday 29 March 2026

---

## Acceptance Criteria Coverage

This phase implements and tests:

### rpi-datasci.AC1: House Style Cleanup
- **rpi-datasci.AC1.1 Success:** `plugins/rpi-house-style/skills/howto-code-in-typescript/` directory does not exist
- **rpi-datasci.AC1.2 Success:** `plugins/rpi-house-style/skills/programming-in-react/` directory does not exist
- **rpi-datasci.AC1.3 Success:** `plugins/rpi-house-style/skills/property-based-testing/` directory does not exist
- **rpi-datasci.AC1.4 Success:** `plugins/rpi-house-style/skills/howto-develop-with-mysql/SKILL.md` exists; contains MySQL-specific content; no references to Drizzle ORM or TypeScript
- **rpi-datasci.AC1.5 Success:** `coding-effectively`, `howto-functional-vs-imperative`, `defense-in-depth`, `writing-good-tests` skills contain at least one neuroscience or scientific computing example each; no TypeScript-only examples remain
- **rpi-datasci.AC1.6 Failure:** `grep -r "typescript\|drizzle\|React\|\.tsx\|\.ts" plugins/rpi-house-style/skills/` returns matches in retained or new skill files

---

<!-- START_SUBCOMPONENT_A (tasks 1-3) -->
<!-- START_TASK_1 -->
### Task 1: Delete Obsolete Skills

**Verifies:** rpi-datasci.AC1.1, rpi-datasci.AC1.2, rpi-datasci.AC1.3

**Files:**
- Delete: `plugins/rpi-house-style/skills/howto-code-in-typescript/`
- Delete: `plugins/rpi-house-style/skills/programming-in-react/`
- Delete: `plugins/rpi-house-style/skills/property-based-testing/`

**Implementation:**
Remove the specified directories and all their contents.

**Verification:**
Run: `ls plugins/rpi-house-style/skills/`
Expected: The deleted directories are missing.

**Commit:** `chore(skills): remove obsolete typescript, react, and pbt skills`
<!-- END_TASK_1 -->

<!-- START_TASK_2 -->
### Task 2: Replace Postgres with MySQL Skill

**Verifies:** rpi-datasci.AC1.4

**Files:**
- Delete: `plugins/rpi-house-style/skills/howto-develop-with-postgres/`
- Create: `plugins/rpi-house-style/skills/howto-develop-with-mysql/SKILL.md`

**Implementation:**
Create `howto-develop-with-mysql/SKILL.md` by adapting the content from the old Postgres skill:
- Update naming to MySQL.
- Replace `SERIAL` with `AUTO_INCREMENT` if mentioned.
- Use backticks for identifiers if applicable.
- Remove all references to Drizzle ORM and `typescript-drizzle.md`.
- Keep the `TX_` naming convention for transactions as it's a useful organizational pattern.

**Verification:**
Run: `cat plugins/rpi-house-style/skills/howto-develop-with-mysql/SKILL.md`
Expected: Content is MySQL-specific and free of Drizzle/TypeScript references.

**Commit:** `feat(skills): replace postgres with mysql skill`
<!-- END_TASK_2 -->
<!-- END_SUBCOMPONENT_A -->

<!-- START_SUBCOMPONENT_B (tasks 3-6) -->
<!-- START_TASK_3 -->
### Task 3: Adapt Generic Skills for Neuroscience - Coding Effectively

**Verifies:** rpi-datasci.AC1.5, rpi-datasci.AC1.6

**Files:**
- Modify: `plugins/rpi-house-style/skills/coding-effectively/SKILL.md`

**Implementation:**
- Remove all TypeScript (`.ts`, `.tsx`) file examples and code snippets.
- Replace with Python/MATLAB/R examples.
- Update "File Organization" section to use `.py`, `.m`, or `.R` extensions.
- Add a section or examples about array shape handling (e.g., `[channels, time, trials]`) and NaN propagation in scientific computing.
- Update "Required Sub-Skills" list to match new skill names.

**Verification:**
Run: `grep -E "\.ts|\.tsx|TypeScript|React" plugins/rpi-house-style/skills/coding-effectively/SKILL.md`
Expected: No matches.

**Commit:** `feat(skills): adapt coding-effectively for neuroscience`
<!-- END_TASK_3 -->

<!-- START_TASK_4 -->
### Task 4: Adapt Generic Skills for Neuroscience - Functional Core, Imperative Shell

**Verifies:** rpi-datasci.AC1.5, rpi-datasci.AC1.6

**Files:**
- Modify: `plugins/rpi-house-style/skills/howto-functional-vs-imperative/SKILL.md`

**Implementation:**
- Ensure examples remain relevant for data science.
- Replace any remaining web-specific terminology with scientific computing terms (e.g., instead of "API response", use "recorded signal data" or "simulation parameters").
- Verify that the Python examples are clean and idiomatic for data science (use numpy-like examples).

**Verification:**
Check content for neuroscience context.

**Commit:** `feat(skills): adapt fcis for neuroscience`
<!-- END_TASK_4 -->

<!-- START_TASK_5 -->
### Task 5: Adapt Generic Skills for Neuroscience - Defense-in-Depth

**Verifies:** rpi-datasci.AC1.5, rpi-datasci.AC1.6

**Files:**
- Modify: `plugins/rpi-house-style/skills/defense-in-depth/SKILL.md`

**Implementation:**
- Replace TypeScript/Node.js examples with Python or MATLAB.
- Add neuroscience failure modes: timestamp misalignment, out-of-range signal values, mismatched array dimensions (e.g., verifying that data shape matches expected `[n_channels, n_samples]`).
- Replace `process.env.NODE_ENV` with a language-appropriate environment check or configuration guard.

**Verification:**
Run: `grep -E "typescript|node_env" plugins/rpi-house-style/skills/defense-in-depth/SKILL.md`
Expected: No matches.

**Commit:** `feat(skills): adapt defense-in-depth for neuroscience`
<!-- END_TASK_5 -->

<!-- START_TASK_6 -->
### Task 6: Adapt Generic Skills for Neuroscience - Writing Good Tests

**Verifies:** rpi-datasci.AC1.5, rpi-datasci.AC1.6

**Files:**
- Modify: `plugins/rpi-house-style/skills/writing-good-tests/SKILL.md`

**Implementation:**
- Use `pytest` (Python), `unittest` (MATLAB), or `testthat` (R) examples.
- Reframe the philosophy to emphasize reproducibility and correctness in analysis pipelines.
- Remove React-specific testing examples (`screen.getByRole`, etc.).
- Update "Managed vs Unmanaged Dependencies" to include data files (HDF5, .mat, .csv) and hardware interfaces (if applicable).

**Verification:**
Run: `grep -E "screen\.|getByRole|React" plugins/rpi-house-style/skills/writing-good-tests/SKILL.md`
Expected: No matches.

**Commit:** `feat(skills): adapt writing-good-tests for neuroscience`
<!-- END_TASK_6 -->
<!-- END_SUBCOMPONENT_B -->

<!-- START_TASK_7 -->
### Task 7: Final Global Cleanup Check

**Verifies:** rpi-datasci.AC1.6

**Files:**
- Global check in `plugins/rpi-house-style/skills/`

**Implementation:**
Run a recursive grep to ensure no TypeScript, React, or Drizzle references remain in any of the retained or new skills.

**Verification:**
Run: `grep -rEi "typescript|drizzle|react|\.ts\b|\.tsx\b" plugins/rpi-house-style/skills/`
Expected: No matches in the adapted skill files.

**Commit:** `chore(skills): final cleanup of web-dev references`
<!-- END_TASK_7 -->

<!-- START_TASK_8 -->
### Task 8: Remove Superseded Implementation Plans

**Verifies:** None

**Files:**
- Delete: `docs/implementation-plans/2026-03-26-context-optimization/`

**Implementation:**
Remove the directory containing the old implementation plans that are now superseded by this redesign.

**Verification:**
Run: `ls docs/implementation-plans/2026-03-26-context-optimization/`
Expected: Directory does not exist.

**Commit:** `chore: remove superseded implementation plans`
<!-- END_TASK_8 -->
