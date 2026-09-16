# Test Requirements: RPI Data Science Workflow Redesign

## 1. Automated Tests

| Criterion | Test Type | Expected Test File Path / Command |
|-----------|-----------|-----------------------------------|
| rpi-datasci.AC1.1-1.3 (Cleanup) | Integration | `tests/verify-cleanup.sh` (ls/test -d checks) |
| rpi-datasci.AC1.4 (MySQL Skill) | Unit | `grep -L "Drizzle\|TypeScript" plugins/rpi-house-style/skills/howto-develop-with-mysql/SKILL.md` |
| rpi-datasci.AC1.6 (Cleanup failure) | Integration | `tests/verify-no-web-refs.sh` (recursive grep) |
| rpi-datasci.AC3.1 (StatusLine registration) | Integration | `grep "StatusLine" plugins/rpi-plan-and-execute/hooks/hooks.json` |
| rpi-datasci.AC3.2 (StatusLine logic) | Unit | `tests/test-statusline.py` (mock stdin -> check .json and stdout) |
| rpi-datasci.AC3.3-3.7 (Monitor Logic) | Unit | `tests/test-session-monitor.py` (simulated payloads and thresholds) |
| rpi-datasci.AC4.1 (PROJECT.md content) | Integration | `tests/verify-project-log.sh` (trigger compression and check file structure) |
| rpi-datasci.AC4.4 (SessionStart robustness) | Unit | `tests/test-session-start.sh` (run with missing files, expect valid JSON) |
| rpi-datasci.AC6.1 & AC6.3 (Model tiers) | Integration | `tests/verify-model-assignments.sh` (grep model field in agent files) |
| rpi-datasci.AC7.1 (Monitor script) | Unit | `tests/test-monitor-logic.py` (mock filesystem -> check classification) |
| rpi-datasci.AC7.5 (Exclusion logic) | Integration | `python3 scripts/monitor.py --check-exclusions` |

## 2. Human Verification

| Criterion | Justification | Verification Approach |
|-----------|---------------|-----------------------|
| rpi-datasci.AC1.5 (Neuro examples) | Qualitative judgment of 'relevance' to neuroscience. | Peer review of adapted skill files for scientific accuracy. |
| rpi-datasci.AC2.1-2.3 (Language Skills) | Idiomatic correctness of scientific code (numpy, tidyverse). | Expert review of Python/MATLAB/R code snippets. |
| rpi-datasci.AC5.1-5.2 (Workflow feel) | UX of the new slash commands and clarity of outcomes. | Manual walkthrough of /quick-analysis and /helper-function. |
| rpi-datasci.AC6.2 (Skill documentation) | Clarity of rationale for model selection. | Review of SKILL.md sections for 'Opus' vs 'Sonnet' guidance. |

## Rationalization
Implementation decisions emphasize the use of lightweight Python/Bash hooks and Markdown-based skills. Consequently, the testing strategy relies heavily on static analysis (grep) for content cleanup and behavioral simulation for logic hooks. Human verification is strictly limited to the semantic quality of the 'House Style' guidance.
