# rpi-extending-claude Context

Knowledge for extending AI coding assistants: creating plugins, commands, agents, skills, hooks, MCP servers, and marketplace management.

## Creating a Plugin

A plugin packages reusable components (commands, agents, skills, hooks, MCP servers) for distribution. Create a plugin when you have components that work across multiple projects.

**Don't create a plugin for:**
- Project-specific configurations
- One-off scripts or commands
- Experimental features still in development

### Directory Structure

```
my-plugin/
   .claude-plugin/
      plugin.json              # Required: plugin manifest
   commands/                    # Optional: slash commands
      my-command.md
   agents/                      # Optional: specialized subagents
      my-agent.md
   skills/                      # Optional: reusable techniques
      my-skill/
          SKILL.md
   hooks/                       # Optional: event handlers
      hooks.json
   .mcp.json                    # Optional: MCP server configs
   README.md                    # Recommended: documentation
```

### plugin.json Format

**Minimal valid manifest:**
```json
{
  "name": "my-plugin"
}
```

**Complete manifest:**
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin does",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "homepage": "https://github.com/yourname/my-plugin",
  "repository": "https://github.com/yourname/my-plugin",
  "license": "MIT",
  "keywords": ["productivity", "automation"]
}
```

### Creating Commands

**File location:** `commands/my-command.md` creates `/my-command` slash command

**Template:**
```markdown
---
description: Brief description of what this command does
allowed-tools: Read, Grep, Glob, Bash
model: sonnet
argument-hint: "[file-path]"
---

# Command Name

Your command prompt goes here. Use $ARGUMENTS for all arguments.
```

### Creating Agents

**File location:** `agents/my-agent.md`

**Template:**
```markdown
---
name: agent-name
description: Use when [specific triggers] - [what agent does]
tools: Read, Grep, Glob, Bash
model: sonnet
---

# Agent Name

[Agent system prompt - who they are, what they do]
```

### Creating Skills

**File location:** `skills/my-skill/SKILL.md`

**Minimal template:**
```markdown
---
name: my-skill-name
description: Use when [specific triggers] - [what it does]
---

# Skill Name

## Overview
Core principle in 1-2 sentences.

## When to Use
- Symptom 1
- Symptom 2

## Implementation
[Code examples, patterns]

## Common Mistakes
[What goes wrong + fixes]
```

**Key principles:**
- `name` uses only letters, numbers, hyphens (no special chars)
- `description` starts with "Use when..." in third person
- Keep token-efficient (<500 words if frequently loaded)
- One excellent example beats many mediocre ones

### Creating Hooks

**File location:** `hooks/hooks.json`

```json
{
  "hooks": [
    {
      "event": "PreToolUse",
      "matcher": "Bash",
      "command": "echo 'About to run bash'"
    },
    {
      "event": "PostToolUse",
      "matcher": "Edit|Write",
      "command": "npx prettier --write \"$CLAUDE_FILE_PATHS\""
    }
  ]
}
```

**Hook events:** `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop`, `SessionStart`, `SessionEnd`

### Component Reference

| Component | Location | When to Use |
|-----------|----------|-------------|
| Commands | `commands/*.md` | Custom slash commands for repetitive tasks |
| Agents | `agents/*.md` | Specialized subagents for complex workflows |
| Skills | `skills/*/SKILL.md` | Reusable techniques and patterns |
| Hooks | `hooks/hooks.json` | Event handlers (format code, validate, etc.) |
| MCP Servers | `.mcp.json` | External tool integrations |

### Naming Conventions

**Use kebab-case everywhere:**
- Plugin names: `my-awesome-plugin`
- Command names: `review-code`
- Agent names: `security-auditor`
- Skill names: `test-driven-development`

### Common Mistakes

| Issue | Fix |
|-------|-----|
| Missing `.claude-plugin/` | Create `.claude-plugin/plugin.json` at root |
| Description too long | Keep under 1024 characters total |
| Not using third person | Use "Use when..." not "I will..." |
| Absolute paths in plugin.json | Use relative paths or `${CLAUDE_PLUGIN_ROOT}` |

---

## Creating an Agent

An **agent** is a specialized AI instance with defined tools, specific responsibilities, and a focused system prompt.

### When to Create an Agent

**Create when:**
- Task requires specialized expertise
- Workflow benefits from tool restrictions
- You want consistent behavior across invocations
- Task is complex enough to warrant context isolation

**Don't create for:**
- Simple, one-off tasks
- Purely conversational interactions

### The Description Field

The `description` field determines when the AI auto-delegates to your agent. **Format:** "Use when [specific triggers/symptoms] - [what the agent does]"

Write in third person.

```yaml
# Bad: vague, no triggers
description: Helps with code

# Good: specific triggers + action
description: Use when reviewing code for security vulnerabilities, analyzing authentication flows, or checking for common security anti-patterns like SQL injection, XSS, or insecure dependencies
```

**Include:** specific symptoms, domain keywords, file types if relevant, actions performed. Max 1024 characters.

### Tool Selection

| Tool | When to Include |
|------|-----------------|
| Read | Reading files, analyzing code |
| Grep | Searching code patterns |
| Glob | Finding files by pattern |
| Edit | Modifying existing files |
| Write | Creating new files |
| Bash | Running commands, git, tests |
| WebFetch/WebSearch | Research tasks |

**Principle:** Include only what the agent needs. Fewer tools = more focused behavior.

### Agent Prompt Structure

1. **Role definition** - who the agent is
2. **Responsibilities** - explicit numbered list
3. **Workflow** - step-by-step process
4. **Output format** - expected structure
5. **Constraints** - what the agent should NOT do

### Model Selection

| Model | Use For |
|-------|---------|
| haiku | Simple tasks, fast iteration, high volume |
| sonnet | Balanced capability/cost, most tasks |
| opus | Complex reasoning, critical decisions, code review |

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| Vague description | Include specific triggers and symptoms |
| Too many tools | Restrict to what's needed |
| No workflow | Add step-by-step process |
| No output format | Define expected structure |
| First-person description | Write in third person |
| Overly broad scope | Narrow to specific responsibility |

---

## Maintaining a Marketplace

A Plugin Marketplace catalogs plugins for discovery and installation. The primary maintenance challenge is **sync drift** — keeping versions consistent across `plugin.json`, `marketplace.json`, and `CHANGELOG.md`.

### marketplace.json Schema

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "my-marketplace",
  "owner": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "metadata": {
    "description": "Brief marketplace description",
    "version": "1.0.0",
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./plugins/my-plugin",
      "description": "What this plugin does",
      "version": "1.0.0"
    }
  ]
}
```

**Fields that DO NOT exist** (do not invent these): `displayName`, `installUrl`, `path`, `marketplace` (as wrapper object)

### Release Checklist

When releasing a new plugin version, update these files **in this order**:

1. `plugins/<name>/.claude-plugin/plugin.json` — Bump `version`
2. `.claude-plugin/marketplace.json` — Update matching plugin entry's `version`
3. `CHANGELOG.md` — Add entry at the top
4. Validate and commit all three together

### Changelog Format

```markdown
## plugin-name X.Y.Z

Brief description of the release.

**New:**
- Specific new features

**Changed:**
- Modifications to existing behavior

**Fixed:**
- Bug fixes
```

### Version Sync Verification

After editing, verify these match:
- `plugins/<name>/.claude-plugin/plugin.json` → `version`
- `.claude-plugin/marketplace.json` → plugin entry's `version`
- `CHANGELOG.md` → entry header `## plugin-name X.Y.Z`

### Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Version drift | Old version installed | Verify both files show same version |
| Skipping validation | JSON errors, plugins not found | Validate before every push |
| Generic changelog entries | Users can't evaluate upgrade value | Describe specific changes |
| Using `owner` as string | Validation error | `owner` must be `{"name": "...", "email": "..."}` |
| Not committing all sync files together | Partial release | Single commit for plugin.json + marketplace.json + CHANGELOG.md |

---

## Maintaining Project Context

Context files (CLAUDE.md or AGENTS.md) document contracts and architectural intent. When code changes contracts, the documentation must update. Stale documentation is worse than no documentation.

**Trigger:** End of development phase, branch completion, or any work that changed contracts, APIs, or domain structure.

### Format Detection (MANDATORY FIRST STEP)

Before any updates, check what format the repository uses:

| Root AGENTS.md? | Format | Action |
|-----------------|--------|--------|
| Yes | AGENTS.md-canonical | Update AGENTS.md files, create companion CLAUDE.md |
| No | CLAUDE.md-canonical | Update CLAUDE.md files directly |

For AGENTS.md-canonical repos, create companion CLAUDE.md files with:
```markdown
Read @./AGENTS.md and treat its contents as if they were in CLAUDE.md
```

### When to Update Context Files

| Change Type | Update Required? |
|-------------|------------------|
| New domain/module | Yes |
| API/interface change | Yes |
| Architectural decision | Yes |
| Bug fix (no contract change) | No |
| Refactor (same behavior) | No |
| Test additions | No |

### The Process

1. **Identify what changed** — diff against base commit, categorize as structural/contract/behavioral/internal
2. **Map changes to context files** — domain changes go in domain files, not root
3. **Verify contracts still hold** — read the code, confirm invariants
4. **Update or create context files** — update freshness date, update affected sections
5. **Commit** — `docs: update project context for <context>`

Always get the actual date with `date +%Y-%m-%d` — never use a hardcoded date.

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| Updating for every change | Only update for contract changes |
| Forgetting freshness date | Always use `date +%Y-%m-%d` |
| Documenting implementation | Document contracts and intent |
| Skipping format detection | Always check for AGENTS.md first |
| Forgetting companion CLAUDE.md | AGENTS.md repos need both files |

---

## Testing Skills With Subagents

Testing skills is TDD applied to process documentation: run scenarios without the skill (RED), write skill addressing failures (GREEN), close loopholes (REFACTOR).

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill prevents the right failures.

### TDD Mapping

| TDD Phase | Skill Testing | What You Do |
|-----------|---------------|-------------|
| RED | Baseline test | Run scenario WITHOUT skill, watch agent fail |
| Verify RED | Capture rationalizations | Document exact failures verbatim |
| GREEN | Write skill | Address specific baseline failures |
| Verify GREEN | Pressure test | Run scenario WITH skill, verify compliance |
| REFACTOR | Plug holes | Find new rationalizations, add counters |

### Writing Pressure Scenarios

Combine 3+ pressures: time, sunk cost, authority, economic consequences, exhaustion, social pressure.

**Good scenario structure:**
- Concrete options (A/B/C choice)
- Real constraints with specific times and consequences
- Make the agent act, not hypothesize
- No easy outs (can't defer to "ask your human partner")

### Pressure Types

| Pressure | Example |
|----------|---------|
| Time | Emergency, deadline, deploy window closing |
| Sunk cost | Hours of work, "waste" to delete |
| Authority | Senior says skip it |
| Economic | Job, promotion at stake |
| Exhaustion | End of day, tired |
| Pragmatic | "Being pragmatic not dogmatic" |

### Plugging Loopholes

For each new rationalization, add:
1. Explicit negation in rules
2. Entry in rationalization table
3. Red flag entry
4. Update description with violation symptoms

### Signs of a Bulletproof Skill

1. Agent chooses correct option under maximum pressure
2. Agent cites skill sections as justification
3. Agent acknowledges temptation but follows rule
4. Meta-testing reveals "skill was clear, I should follow it"

---

## Writing Claude Directives

Guidance for writing instructions that guide AI behavior — skills, context files, agent prompts, system prompts.

### Core Principles

**1. The AI is smart.** Only write what it doesn't already know. Challenge each line: does this justify its token cost?

**2. Positive > Negative framing.** "Don't do X" triggers thinking about X. Say what TO do, not what to avoid.

**3. Context motivates compliance.** Explain WHY, not just WHAT. The AI generalizes from motivation.

**4. Placement matters.** Instructions at prompt start and end receive higher attention. Critical rules go at boundaries.

**5. ~150 instruction limit.** More instructions = uniform degradation across ALL rules. Prune ruthlessly.

### Token Efficiency

- Frequently-loaded directives: <200 words
- Skills/context files: <500 lines total
- Reference other skills instead of repeating content
- Progressive disclosure: main file is overview + links

### Discovery (for Skills)

The `description` field determines if the AI finds your skill.

**Format:** Start with "Use when..." + specific triggers + what it does, third person.

**Keywords:** Include error messages, symptoms, tool names that might be searched for.

### Compliance Techniques

**Primary: Context + Motivation** — Explain WHY the rule exists.

**Secondary: Structural Enforcement** — Use numbered workflow steps, checklists, forced commitment ("Announce: I'm using [skill]").

**Escalation: Imperatives** — Use sparingly for true boundaries only. Aggressive language can cause over-triggering.

### Structure Patterns

**XML for directives:**
```xml
<task>What to accomplish</task>
<constraints>Hard requirements</constraints>
<output_format>Expected structure</output_format>
```

**Workflows:**
```markdown
## Workflow
- [ ] Step 1: Analyze inputs
- [ ] Step 2: Generate plan
- [ ] Step 3: Execute
- [ ] Step 4: Verify output
```

### Overengineering Prevention

Include this when needed:

> Avoid over-engineering. Only make changes that are directly requested or clearly necessary. Keep solutions simple and focused. Don't add features, refactor code, or make "improvements" beyond what was asked.

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| Verbose explanations | AI knows basics — omit |
| Multiple valid approaches | Pick one default, escape hatch for edge cases |
| Vague triggers | Specific symptoms: "tests flaky", "race condition" |
| Deeply nested references | Keep one level deep from main file |
| Aggressive language | Lead with context, reserve imperatives for boundaries |

---

## Writing CLAUDE.md Files

Context files bridge AI statelessness. They preserve context so humans don't re-explain architectural intent every session.

**Key distinction:**
- **Top-level**: HOW to work in this codebase (commands, conventions)
- **Subdirectory**: WHY this piece exists and what it PROMISES (contracts, intent)

### Top-Level Context File

Includes: tech stack, commands, project structure, conventions, edit boundaries.

**Template:**
```markdown
# [Project Name]

Last verified: [DATE]

## Tech Stack
- Language: TypeScript 5.x
- Framework: Next.js 14
- Database: PostgreSQL

## Commands
- `npm run dev` - Start dev server
- `npm run test` - Run tests

## Project Structure
- `src/domains/` - Domain modules
- `src/shared/` - Cross-cutting utilities

## Conventions
- Functional Core / Imperative Shell pattern

## Boundaries
- Safe to edit: `src/`
- Never touch: `migrations/`
```

### Subdirectory Context File (Domain-Level)

Focuses on WHY and CONTRACTS. The code shows WHAT; these files explain intent.

**Template:**
```markdown
# [Domain Name]

Last verified: [DATE]

## Purpose
[1-2 sentences: WHY this domain exists]

## Contracts
- **Exposes**: [public interfaces]
- **Guarantees**: [promises this domain keeps]
- **Expects**: [what callers must provide]

## Dependencies
- **Uses**: [domains/services this depends on]
- **Used by**: [what depends on this domain]
- **Boundary**: [what should NOT be imported here]

## Key Decisions
- [Decision]: [Rationale]

## Invariants
- [Thing that must always be true]

## Gotchas
- [Non-obvious thing that will bite you]
```

### Freshness Dates: Mandatory

Every context file MUST include a "Last verified" date. Always get the actual date with `date +%Y-%m-%d` — never use a hardcoded date.

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| Describing WHAT code does | Focus on WHY it exists, contracts it keeps |
| Missing freshness date | Always include, always use real date |
| Too much detail | Subdirectory files should be <100 lines |
| Duplicating parent content | Subdirectory inherits parent; don't repeat |
| Stale contracts | Update when domain changes |

---

## Writing Skills

Writing skills is Test-Driven Development applied to process documentation.

**Iron Law:** No skill without a failing test first. Same as TDD for code.

### When to Create a Skill

**Create when:**
- Technique wasn't intuitively obvious
- You'd reference this across projects
- Pattern applies broadly

**Don't create for:**
- One-off solutions
- Project-specific conventions (use context files)

### Skill Types

- **Technique:** Concrete method with steps
- **Pattern:** Mental model for problems
- **Reference:** API docs, syntax guides, tool documentation

### SKILL.md Template

```markdown
---
name: Skill-Name-With-Hyphens
description: Use when [triggers/symptoms] - [what it does, third person]
---

# Skill Name

## Overview
Core principle in 1-2 sentences.

## When to Use
Symptoms and use cases. When NOT to use.

## Core Pattern
Before/after comparison or key technique.

## Quick Reference
Table or bullets for scanning.

## Common Mistakes
What goes wrong + fixes.
```

### Anti-Patterns

- **Narrative examples** with session dates (too specific, not reusable)
- **Multi-language examples** (mediocre quality, maintenance burden)
- **Generic labels** like helper1, step3 (labels need semantic meaning)

### Testing Before Deploying

1. Create pressure scenarios (3+ combined pressures for discipline skills)
2. Run WITHOUT skill — document baseline failures verbatim
3. Write skill addressing specific failures
4. Run WITH skill — verify compliance
5. Find new rationalizations → add counters → re-test until bulletproof

---

## Project Claude Librarian (Agent Knowledge)

The project-claude-librarian agent maintains accurate project context documentation. It reviews what changed during a development phase and ensures context files reflect current contracts and architectural decisions.

### Responsibilities

1. Detect what format the repository uses (AGENTS.md or CLAUDE.md)
2. Analyze what changed since phase/branch start
3. Categorize changes: contracts, APIs, structure, or internal-only
4. Determine which context files need updates
5. For AGENTS.md repos: ensure companion CLAUDE.md files exist
6. Verify freshness dates are current
7. Commit documentation updates separately from code changes

### Format Detection Logic

Check for AGENTS.md at root first:
- If found: update AGENTS.md files, create companion CLAUDE.md next to each
- If not found: update CLAUDE.md files directly

### Expected Workflow

1. Detect format
2. Diff against base commit to see what changed
3. Categorize changes (structural, contract, behavioral, internal)
4. Map to affected context files
5. Read existing context files before updating
6. Verify contracts still hold by reading the code
7. Apply updates
8. Commit with message: `docs: update project context for <context>`

### Output Format

```
## Context File Maintenance Report

### Format Detected
- Repository uses: AGENTS.md / CLAUDE.md

### Changes Analyzed
- Files changed: <count>
- Contract changes detected: Yes/No

### Context File Updates
- `path/to/context-file`: <what was updated>

### Human Review Recommended
- <any contracts that need human verification>
```

### Constraints

- Only update context files for contract changes (not internal refactoring)
- Always verify contracts by reading the code
- Always use `date +%Y-%m-%d` for freshness dates — never use a hardcoded date
- Commit documentation changes separately from code changes
