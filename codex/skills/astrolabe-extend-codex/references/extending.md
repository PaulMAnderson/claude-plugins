# Codex extension modes

## Skill and directive authoring

Create a lowercase, hyphenated folder with `SKILL.md` containing `name` and a discriminating `description` in YAML frontmatter. Put the essential decisions/workflow in the body; route optional detail to references and repeated deterministic operations to scripts. Resolve resources relative to the skill, not the user's cwd. Use `$skill-name` for user invocation and direct reads for internal references; no invented activation tool.

Explain when to apply a procedure, its inputs/outputs, meaningful gates, and stopping conditions. Keep constraints proportional to real fragility. Avoid model-specific persuasion folklore, generic reminders, and arbitrary approval demands. User intent and current authorization take precedence. Optional `agents/openai.yaml` metadata must match current supported schema; role prompt files are not automatically registered agents.

Test scripts by executing them in an isolated workspace. Validate skill metadata and every reference. For workflow behavior use realistic scenarios: insufficient context, a failed check despite a DONE report, stale evidence after a fix, compaction with unresolved issues, an unavailable tool, and a plan/requirement conflict. Where independent delegation is available and authorized, run bounded fresh-agent cases with raw inputs and assess produced artifacts. Otherwise record a local walkthrough and its limitations; do not claim independent testing.

## AGENTS.md and project librarian

Read actual instruction discovery rules and existing files before editing. Root instructions describe how to work here (commands, structure, conventions); nested context describes why a domain exists, what it exposes/expects/guarantees, dependencies, invariants, decisions, and non-obvious traps. Verify each changed claim against code and tests. Record a real last-verified date when performing a contract review; do not refresh a whole document's date without checking it.

At implementation/final-review boundaries inspect the baseline-to-current changes for APIs, commands, layout, or architectural contracts that need documentation. Update only affected content and remove demonstrably stale claims. Do not add a file to every trivial folder or duplicate parent guidance. Link source files as references, not force-loaded copies. Preserve independent instructions and ongoing user edits.

If migrating existing project instructions, use their actual intent with correct Codex discovery semantics. Do not assume another agent's filename is read automatically or change global fallback configuration without scope to do so. `.astrolabe/CONTEXT.md` holds resume progress, while `.astrolabe/PROJECT.md` holds the stable project description; avoid putting transient task logs into `AGENTS.md`.

## Agent roles

A role brief names one bounded objective, permitted workspace/files, exact requirements/interfaces, input paths, output path/schema, checks, and escalation conditions. Workers implement, reviewers inspect, analysts trace AC coverage, and librarians update durable contracts. Use separate reports and controller-owned state. Model choice comes from the user's preference or actual available configuration, not a hardcoded Claude/Gemini tier mapping. A fresh reviewer is useful when supported but is not simulated by claiming local rereading was independent.

## Distribution and maintenance

For local/repository authoring use supported discoverable skill directories (verify current Codex documentation). Keep sibling dependencies installed together. Validate a copy in a temporary project before distributing; detect name collisions and refuse to overwrite unrelated skills.

For a reusable Codex plugin, use the installed plugin authoring skill/current official schema to create its manifest and any marketplace entry, check names/versions/paths, and preserve licenses. Validate registration using available supported tools. A skills-only bundle can be installed without a plugin manifest. Do not present a Claude marketplace or Gemini extension manifest as Codex-compatible.

For updates, inspect the final diff, rerun affected validation, synchronize distribution metadata/version/changelog when those files exist, and record source mappings. Publish/push/install globally only within the user's authorization and execution permissions.
