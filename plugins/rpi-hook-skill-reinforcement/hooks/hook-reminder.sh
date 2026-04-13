#!/usr/bin/env bash
# UserPromptSubmit hook - skill reinforcement
# Previously injected a per-message EXTREMELY_IMPORTANT reminder (~100 tokens each turn).
# Removed: the skills list in system context and using-plan-and-execute SKILL.md
# already establish the requirement to check skills. Per-message injection was redundant
# and compounded context usage across long conversations.
exit 0
