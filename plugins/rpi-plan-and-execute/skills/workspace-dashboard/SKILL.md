---
name: workspace-dashboard
description: Displays the central workspace dashboard summarizing all Claude projects
user-invocable: true
---

# Workspace Dashboard

## Overview

Displays the current `DASHBOARD.md` from the workspace root (`/Users/paul/Claude/`).

**Announce at start:** "I'm using the workspace-dashboard skill to display the project dashboard."

## Process

1. **READ:** Read `/Users/paul/Claude/DASHBOARD.md`.
2. **DISPLAY:** Output the content of the dashboard to the chat.
3. **REFRESH (Optional):** If requested, run `python3 plugins/rpi-plan-and-execute/scripts/monitor.py` to refresh the dashboard before displaying it.
