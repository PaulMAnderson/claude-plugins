# RPI Context Engineering Design

## Summary

This design covers two interlocking changes to the ed3d-plugins fork: (1) a full rebrand from `ed3d-*` to `rpi-*` naming with updated attribution and documentation, and (2) integration of Context Engineering (CE) principles into the RPI workflow via a context monitor hook, a compression skill, and upgraded CE-aware file templates. The result is an independent, clearly-attributed fork that actively manages context degradation rather than leaving it entirely to the user.

---

## 🗂 Memory Tier Index

> **This section is itself a demonstration of the CE memory-tier template upgrade.**
> Future agents reading this document should use this index to decide what to load.

| Tier | Sections | When to read |
|------|----------|-------------|
| 🔴 **HOT** | DoD, Acceptance Criteria | Always — load before doing anything |
| 🟡 **WARM** | Architecture, File Map, Implementation Phases | When planning or implementing a specific phase |
| 🔵 **COLD** | Background, Alternatives Considered, Glossary | Reference on demand only |

---

## 🔴 Definition of Done

1. All `ed3d-*` plugin directories renamed to `rpi-*`; all internal references updated; `marketplace.json`, `CLAUDE.md`, `CHANGELOG.md`, and `README.md` updated; attribution to `ed3dai/ed3d-plugins` and `obra/superpowers` (Jesse Vincent) preserved and made explicit
2. A `PostToolUse` context monitor hook fires after every tool call, debounced via a call-count file, and injects a context-pressure warning into Claude's context at configurable thresholds (default: warn at 40 tool calls, urgent at 70)
3. A `compressing-context` skill produces an Anchored Iterative Summary written to `.rpi/CONTEXT.md`; a `/compress-context` command invokes it manually; the skill is called automatically at RPI phase-boundary transitions (design→plan, plan→execute)
4. The `writing-design-plans` skill template is upgraded to include a Memory Tier Index section and hot/warm/cold annotations on each section; the `writing-implementation-plans` skill template is upgraded to annotate each phase file with a context budget estimate

---

## 🔴 Acceptance Criteria

### rpi-context-engineering.AC1 — Rebrand

- **AC1.1**: All nine plugin directories under `plugins/` have their `ed3d-*` prefix replaced with `rpi-*` (or unprefixed where `ed3d-00-*` conventions existed)
- **AC1.2**: No remaining occurrences of the string `ed3d-` exist in any skill, command, agent, hook, or config file that would be installed into a user's Claude Code environment
- **AC1.3**: `README.md` includes an explicit attribution block crediting `ed3dai/ed3d-plugins` and `obra/superpowers` (Jesse Vincent, MIT) as upstream sources
- **AC1.4**: `CLAUDE.md` and `marketplace.json` reflect the `rpi-*` naming throughout
- **AC1.5 (failure)**: A grep for `ed3d-` across `plugins/` returns results → rebrand is incomplete

### rpi-context-engineering.AC2 — Context Monitor Hook

- **AC2.1**: A `PostToolUse` hook is registered in `plugins/rpi-plan-and-execute/hooks/hooks.json`
- **AC2.2**: The hook script reads or creates `.rpi/context-monitor-count` and increments it on each call
- **AC2.3**: At threshold 1 (default: 40), the hook outputs JSON with `additionalContext` containing a moderate warning prompt
- **AC2.4**: At threshold 2 (default: 70), the hook outputs JSON with `additionalContext` containing an urgent compression prompt
- **AC2.5**: After outputting a warning, the counter resets (debounce) to avoid repeated alerts
- **AC2.6 (failure)**: Counter file is not created or is not incremented → hook is not firing

### rpi-context-engineering.AC3 — Compression Skill & Command

- **AC3.1**: `plugins/rpi-plan-and-execute/skills/compressing-context/SKILL.md` exists and instructs Claude to produce a structured summary with sections: Session Intent, Files Modified, Decisions Made, Current State, Next Steps
- **AC3.2**: The summary is written to `.rpi/CONTEXT.md` in the project working directory
- **AC3.3**: `plugins/rpi-plan-and-execute/commands/compress-context.md` exists and invokes the skill
- **AC3.4**: The `starting-a-design-plan` skill's Phase 6 (Planning Handoff) calls the compression skill before instructing the user to `/clear`
- **AC3.5**: The `starting-an-implementation-plan` skill's final handoff step calls the compression skill before instructing the user to `/clear` for execution
- **AC3.6 (failure)**: `.rpi/CONTEXT.md` is not written after compression → skill did not execute

### rpi-context-engineering.AC4 — CE Memory Tier Templates

- **AC4.1**: The `writing-design-plans` skill includes instructions to write a Memory Tier Index table immediately after the Summary section
- **AC4.2**: The `writing-design-plans` skill annotates each major section heading with its tier emoji (🔴/🟡/🔵) according to a defined mapping
- **AC4.3**: The `writing-implementation-plans` skill includes instructions to add a `Context Budget` line to each phase file header estimating its token weight (small/medium/large) and listing which files an agent must load to execute it
- **AC4.4 (failure)**: A newly generated design doc contains no Memory Tier Index → template upgrade was not applied

---

## 🟡 Architecture

### Feature 1: Context Monitor Hook

**Mechanism:** Claude Code `PostToolUse` hooks receive a JSON payload on stdin describing the tool that fired. The hook script outputs a JSON response; if it includes `hookSpecificOutput.additionalContext`, that string is injected into Claude's visible context before it generates its next response.

Since Claude Code does not currently expose a direct token-count API to hook scripts, we use **tool-call count** as a proxy for context growth. A counter file (`.rpi/context-monitor-count`) is maintained by the hook script and persists between calls within a session.

```
PostToolUse fires
       ↓
context-monitor.sh reads .rpi/context-monitor-count
       ↓
counter < warn_threshold → increment, exit quietly
       ↓
counter >= warn_threshold AND < urgent_threshold
    → output moderate warning additionalContext, reset counter
       ↓
counter >= urgent_threshold
    → output urgent warning additionalContext, reset counter
```

**Configurable via environment variables:**
- `RPI_CONTEXT_WARN_THRESHOLD` (default: 40)
- `RPI_CONTEXT_URGENT_THRESHOLD` (default: 70)

**Why tool-count and not token-count:** Hook scripts are shell processes without direct access to the Claude API context window state. Tool-call count correlates with context growth because each tool call appends tool input + output to the context. A file-read tool call typically adds 500–5000 tokens; an edit adds 200–2000. After 40 calls, accumulated context is typically significant.

### Feature 2: Compression Skill & Command

**Technique:** Anchored Iterative Summarization (from CE `context-compression` skill). Rather than compressing everything, the skill maintains a persistent structured summary file with defined sections. On each invocation it merges new information into the existing file rather than regenerating from scratch — preventing information drift across repeated compressions.

**Output file:** `.rpi/CONTEXT.md` (gitignored by default, session-scoped)

```markdown
## Session Intent
[What the user is trying to accomplish in this session]

## Files Modified
- path/to/file.ts: description of change

## Decisions Made
- [Decision]: [Rationale]

## Current State
[Where we are in the workflow, what's passing/failing]

## Next Steps
1. [Immediate next action]
```

**Integration with RPI phase boundaries:**

The design→plan boundary already tells the user to `/clear`. We insert a mandatory compression step just before that instruction so the summary file exists in the repo when the new session starts and the `starting-an-implementation-plan` skill can read it.

```
Phase 6 of starting-a-design-plan (Planning Handoff):
  1. Call compressing-context skill   ← NEW
  2. Confirm .rpi/CONTEXT.md written  ← NEW
  3. Give user the /clear + command instructions (existing)
```

Same pattern for plan→execute boundary in `starting-an-implementation-plan`.

### Feature 3: CE Memory Tier Templates

**Section tier mapping for design docs:**

| Section | Tier | Rationale |
|---------|------|-----------|
| Memory Tier Index | 🔴 HOT | Meta — tells the reader what to load |
| Definition of Done | 🔴 HOT | Anchor for all decisions |
| Acceptance Criteria | 🔴 HOT | Defines done for each deliverable |
| Architecture | 🟡 WARM | Needed when working on a phase |
| File Map | 🟡 WARM | Needed when navigating the codebase |
| Implementation Phases | 🟡 WARM | Needed when planning tasks |
| Background | 🔵 COLD | Context only; rarely needed mid-session |
| Alternatives Considered | 🔵 COLD | Reference; only if approach is questioned |
| Glossary | 🔵 COLD | Look up terms as needed |

**Context budget line for implementation phase files:**

Each `phase_N.md` file gets a header block:

```
---
phase: N
context-budget: medium        # small / medium / large
files-required:               # files agent MUST load to execute this phase
  - plugins/rpi-plan-and-execute/skills/writing-design-plans/SKILL.md
  - docs/design-plans/YYYY-MM-DD-slug.md
---
```

### Feature 4: Rebrand

**Rename map:**

| Old name | New name |
|----------|----------|
| `ed3d-00-getting-started` | `rpi-getting-started` |
| `ed3d-basic-agents` | `rpi-basic-agents` |
| `ed3d-extending-claude` | `rpi-extending-claude` |
| `ed3d-hook-claudemd-reminder` | `rpi-hook-claudemd-reminder` |
| `ed3d-hook-skill-reinforcement` | `rpi-hook-skill-reinforcement` |
| `ed3d-house-style` | `rpi-house-style` |
| `ed3d-plan-and-execute` | `rpi-plan-and-execute` |
| `ed3d-playwright` | `rpi-playwright` |
| `ed3d-research-agents` | `rpi-research-agents` |

**Attribution block for README.md:**

```markdown
## Attribution

This repository is a fork of [ed3dai/ed3d-plugins](https://github.com/ed3dai/ed3d-plugins).
Core workflow skills (`rpi-plan-and-execute`) are derived from
[obra/superpowers](https://github.com/obra/superpowers) by Jesse Vincent (MIT licence).
Some skills include contributions from the Trail of Bits Skills repository.

This fork diverges from the upstream in: RPI branding, Context Engineering integration,
context monitoring, and compression-aware file templates.
```

---

## 🟡 File Map

Files created (new):
```
plugins/rpi-plan-and-execute/hooks/context-monitor.sh
plugins/rpi-plan-and-execute/skills/compressing-context/SKILL.md
plugins/rpi-plan-and-execute/commands/compress-context.md
docs/design-plans/2026-03-01-rpi-context-engineering.md   ← this file
```

Files modified (significant changes):
```
plugins/rpi-plan-and-execute/hooks/hooks.json              ← add PostToolUse entry
plugins/rpi-plan-and-execute/skills/starting-a-design-plan/SKILL.md     ← add compression step Phase 6
plugins/rpi-plan-and-execute/skills/starting-an-implementation-plan/SKILL.md  ← add compression step
plugins/rpi-plan-and-execute/skills/writing-design-plans/SKILL.md       ← add tier template instructions
plugins/rpi-plan-and-execute/skills/writing-implementation-plans/SKILL.md    ← add context-budget header
README.md                                                   ← full rewrite + attribution block
CLAUDE.md                                                   ← update ed3d→rpi references
.claude-plugin/marketplace.json                             ← rename all plugin entries
CHANGELOG.md                                                ← document breaking changes
```

Files renamed (directories):
```
plugins/ed3d-*/  →  plugins/rpi-*/   (all 9 plugin directories)
```

---

## 🟡 Implementation Phases

### Phase 1: Rebrand — rename directories and update all references

Rename all 9 `plugins/ed3d-*` directories to `plugins/rpi-*`. Then do a global search-and-replace of `ed3d-` → `rpi-` across all files under `plugins/`, `CLAUDE.md`, `marketplace.json`, and `CHANGELOG.md`. Verify with `grep -r "ed3d-" plugins/` returning zero results.

### Phase 2: Update README and attribution

Rewrite `README.md` with: new project name and description, attribution block, updated install instructions using `rpi-*` names, updated command examples, links to upstream repos.

### Phase 3: Context monitor hook

Write `plugins/rpi-plan-and-execute/hooks/context-monitor.sh` (shell script, PostToolUse). Add the PostToolUse hook entry to `plugins/rpi-plan-and-execute/hooks/hooks.json`. The script must create `.rpi/` directory if absent, maintain the counter file, compare against thresholds, output JSON with `additionalContext` at threshold crossings, and reset the counter after each alert.

### Phase 4: Compression skill

Write `plugins/rpi-plan-and-execute/skills/compressing-context/SKILL.md`. The skill instructs Claude to: produce an Anchored Iterative Summary with the five defined sections, merge with existing `.rpi/CONTEXT.md` if present (do not overwrite — merge), write the result back to `.rpi/CONTEXT.md`, and confirm completion.

Write `plugins/rpi-plan-and-execute/commands/compress-context.md` invoking the skill.

### Phase 5: Auto-compression at phase boundaries

Update `starting-a-design-plan` Phase 6 to call `compressing-context` before the `/clear` instruction. Update `starting-an-implementation-plan` final handoff to do the same. In both cases the compression should happen immediately after the phase's primary output is committed to git, and before the `/clear` instruction is given.

### Phase 6: CE memory tier template upgrades

Update `writing-design-plans` skill to: include a Memory Tier Index section template, annotate all standard section headings with their tier emoji, and describe the hot/warm/cold rationale. Update `writing-implementation-plans` skill to: include the `context-budget` YAML frontmatter block in each phase file template, and document how to estimate small/medium/large based on number of files required.

---

## 🔵 Background

This design arises from a comparison of three Claude Code workflow harnesses: `ed3d-plugins` (this repo), `Agent-Skills-for-Context-Engineering`, and `get-shit-done`. The analysis identified three gaps in `ed3d-plugins` relative to the CE skills repo and GSD:

1. No context monitoring — GSD has a PostToolUse hook alerting at 35%/25% context; ed3d has nothing
2. No compression step — the RPI workflow tells users to `/clear` between phases but discards all context with no summary
3. No memory-tier awareness — design docs have no structure indicating to a future agent what is "hot" vs "cold" to read

The rebrand decision arises independently: since this fork introduces breaking changes (new hook, new skill, modified skills), it is a good moment to establish a distinct identity rather than continuing to use the upstream `ed3d-` namespace, which could cause confusion with the original project.

---

## 🔵 Alternatives Considered

**Alternative to tool-count proxy: context percentage from Claude's self-report**
Rather than a hook counting tool calls, the `UserPromptSubmit` hook could ask Claude to self-report context usage. Rejected: more complex, adds latency to every prompt, and Claude's self-reported context fractions are unreliable.

**Alternative to Anchored Iterative Summarization: /compact command**
Claude Code has a built-in `/compact` command that auto-summarises. Rejected: it is destructive (clears the conversation and cannot be undone), gives no structured output, and the resulting summary is not readable as a project file that persists across sessions.

**Alternative to `.rpi/` directory: use `.ed3d/` for backwards compatibility**
Keep the existing `.ed3d/` directory name since users already have project guidance files there. Rejected: the rename is a deliberate clean break; existing `.ed3d/design-plan-guidance.md` files can be copied to `.rpi/` by users, and the guides should document this migration step.

**Alternative to emoji tier prefixes: YAML frontmatter on each section**
Use structured YAML to annotate sections instead of emoji. Rejected: YAML is not valid Markdown section syntax; emoji is rendered clearly in any Markdown viewer and is immediately scannable.

---

## 🔵 Glossary

| Term | Definition |
|------|-----------|
| **RPI** | Research-Plan-Implement — the three-phase workflow at the core of this plugin suite |
| **CE** | Context Engineering — the discipline of structuring information fed to LLMs to maximise quality and minimise degradation |
| **Anchored Iterative Summarization** | A compression technique that maintains a persistent structured summary file, merging new information incrementally rather than regenerating from scratch |
| **Hot/Warm/Cold (memory tiers)** | A three-tier classification of document sections by how frequently an agent needs to read them: hot = always, warm = when relevant, cold = reference only |
| **Context budget** | An estimate of the token cost of loading a document or set of files, used to help agents prioritise what to read when context is limited |
| **PostToolUse hook** | A Claude Code hook type that fires after every tool invocation, receiving tool metadata and optionally injecting content into Claude's context |
| **`ed3d-plugins`** | The upstream repository this project forks from: `github.com/ed3dai/ed3d-plugins` |
| **`obra/superpowers`** | The upstream repository (Jesse Vincent, MIT) from which the core workflow skills derive |
