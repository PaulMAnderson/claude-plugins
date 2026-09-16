---
phase: 2
title: Language-Specific House Style Skills
context-budget: small
files-required:
  - /Users/paul/Claude/claude-plugins/docs/design-plans/2026-03-28-rpi-datasci.md
depends-on: [phase_01.md]
---

# RPI Data Science Workflow Redesign Implementation Plan

**Goal:** Add specialized house style skills for Python, MATLAB, and R, tailored for data science and neuroscience workflows.

**Architecture:** This phase introduces three new skill directories under `plugins/rpi-house-style/skills/`. Each skill provides idiomatic guidance, best practices, and property-based testing patterns for its respective language in a scientific context.

**Tech Stack:** Markdown (Skills), Python, MATLAB, R.

**Scope:** Phase 2 from original design.

**Codebase verified:** Sunday 29 March 2026

---

## Acceptance Criteria Coverage

This phase implements and tests:

### rpi-datasci.AC2: Language-Specific Skills
- **rpi-datasci.AC2.1 Success:** `plugins/rpi-house-style/skills/howto-code-in-python/SKILL.md` exists; covers numpy/scipy/pandas idioms, type hints, virtual environments, matplotlib conventions
- **rpi-datasci.AC2.2 Success:** `plugins/rpi-house-style/skills/howto-code-in-matlab/SKILL.md` exists; covers `arguments` validation blocks, OOP for stateful analysis objects, vectorisation, toolbox organisation
- **rpi-datasci.AC2.3 Success:** `plugins/rpi-house-style/skills/howto-code-in-r/SKILL.md` exists; covers tidyverse vs base R, `renv`, ggplot2 conventions, S3 vs S4 objects, Rmarkdown/Quarto
- **rpi-datasci.AC2.4 Failure:** Any language skill contains examples or patterns specific to a language other than its target

---

<!-- START_SUBCOMPONENT_A (tasks 1-3) -->
<!-- START_TASK_1 -->
### Task 1: Create Python House Style Skill

**Verifies:** rpi-datasci.AC2.1

**Files:**
- Create: `plugins/rpi-house-style/skills/howto-code-in-python/SKILL.md`

**Implementation:**
Write `SKILL.md` for Python including:
- **NumPy/SciPy/Pandas Idioms:** Vectorization over loops, array shape handling (`[channels, time, trials]`), indexing conventions.
- **Type Hints:** Using `numpy.typing.NDArray` and `Annotated` for array shapes.
- **Environments:** Use of `venv` or `conda` for reproducibility.
- **Project Structure:** Differentiating between analysis scripts (linear, figure-focused) and local packages (modular, reusable logic).
- **Visualization:** Matplotlib Object-Oriented API vs Seaborn for statistical plotting.
- **Property-Based Testing:** Patterns using the `hypothesis` library.

**Verification:**
Run: `cat plugins/rpi-house-style/skills/howto-code-in-python/SKILL.md`
Expected: Comprehensive coverage of the above topics with Python-specific examples.

**Commit:** `feat(skills): add python house style skill`
<!-- END_TASK_1 -->

<!-- START_TASK_2 -->
### Task 2: Create MATLAB House Style Skill

**Verifies:** rpi-datasci.AC2.2

**Files:**
- Create: `plugins/rpi-house-style/skills/howto-code-in-matlab/SKILL.md`

**Implementation:**
Write `SKILL.md` for MATLAB including:
- **Script vs Function:** Preferring functions for modularity; use of Live Scripts for documentation.
- **Argument Validation:** Using modern `arguments` blocks (R2019b+) for input type and shape checking.
- **Vectorization:** Leveraging matrix operations, but noting when loops are preferred (JIT, memory constraints).
- **OOP for Stateful Analysis:** Handle vs Value classes; using objects to represent experimental sessions or preprocessing pipelines.
- **Toolbox Organization:** Using `+package` namespaces, `private/` folders, and `@class` directories.
- **Avoiding Global State:** Rationale and alternatives (passing objects/structs).

**Verification:**
Run: `cat plugins/rpi-house-style/skills/howto-code-in-matlab/SKILL.md`
Expected: Comprehensive coverage of the above topics with MATLAB-specific examples.

**Commit:** `feat(skills): add matlab house style skill`
<!-- END_TASK_2 -->

<!-- START_TASK_3 -->
### Task 3: Create R House Style Skill

**Verifies:** rpi-datasci.AC2.3

**Files:**
- Create: `plugins/rpi-house-style/skills/howto-code-in-r/SKILL.md`

**Implementation:**
Write `SKILL.md` for R including:
- **Tidyverse vs Base R:** Use cases for each (readability vs performance).
- **Reproducibility:** Using `renv` for package management.
- **Visualization:** `ggplot2` conventions for publication-ready figures.
- **Object Systems:** When to use S3 (simple models) vs S4 (strict validation, Bioconductor style).
- **Reporting:** Using Rmarkdown/Quarto for reproducible scientific reports.
- **Property-Based Testing:** Patterns using the `hedgehog` library.

**Verification:**
Run: `cat plugins/rpi-house-style/skills/howto-code-in-r/SKILL.md`
Expected: Comprehensive coverage of the above topics with R-specific examples.

**Commit:** `feat(skills): add r house style skill`
<!-- END_TASK_3 -->
<!-- END_SUBCOMPONENT_A -->

<!-- START_TASK_4 -->
### Task 4: Cross-Language Integrity Check

**Verifies:** rpi-datasci.AC2.4

**Files:**
- Check: `plugins/rpi-house-style/skills/howto-code-in-{python,matlab,r}/SKILL.md`

**Implementation:**
Review each new skill file to ensure no examples from other languages leaked in (e.g., no Python code in the MATLAB skill).

**Verification:**
Manual review or targeted greps for language-specific keywords in wrong files.

**Commit:** `chore(skills): verify language skill isolation`
<!-- END_TASK_4 -->
