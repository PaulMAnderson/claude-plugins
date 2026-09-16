# B2: Legacy RPI project migration

## Summary
A standalone Python script previews and copies a legacy project's `.rpi/` state into a new `.astrolabe/` directory. It preserves the source, embeds the old session log in a HISTORY entry, and copies old design and implementation plans. It publishes the new directory only after staging succeeds.

## Memory Tier Index
- Hot: B2 outcome, ACs, source preservation, target conflict rule
- Warm: file mapping, CLI, staged publish
- Cold: old layout evidence and alternatives

## Definition of Done
- Supplied by B2: Build a migration script or skill for other projects with existing `.rpi` state. The prior project-tracking design specifically names PROJECT.md, CONTEXT.md, SESSION.md, guidance, and root plan directories.
- Agent assumption: a repository script is sufficient; no tool-specific skill copy is needed.
- A dry run lists planned copies. A real run yields a valid schema-1 `.astrolabe/`, retains legacy content and old paths, and prints the result.
- The tool refuses an existing `.astrolabe/` target and does not mutate `.rpi/` or root plans. Unknown `.rpi` files remain in a legacy archive.

## Acceptance Criteria
- legacy-rpi-migration.AC1.1: Given a project with legacy core files, the tool creates valid PROJECT.md, CONTEXT.md, STATUS.md, HISTORY.md, and PLANNED.md under `.astrolabe/`.
- legacy-rpi-migration.AC1.2: Legacy SESSION.md content remains byte-for-byte recoverable and appears in the new HISTORY.md as an indented legacy entry.
- legacy-rpi-migration.AC1.3: Guidance and root design/implementation plans are copied to their new paths; other `.rpi` files remain in the legacy archive.
- legacy-rpi-migration.AC2.1: Dry run reports the mapping and makes no changes.
- legacy-rpi-migration.AC2.2: Missing `.rpi/`, existing `.astrolabe/`, or symlinks in copied trees produce a clear error without changing source or destination.
- legacy-rpi-migration.AC2.3: A copy failure removes staging content and leaves no partial `.astrolabe/`.
- legacy-rpi-migration.AC2.4: Repeating a completed migration reports it as already migrated without modifying files.

## Architecture and contracts
`python3 scripts/migrate-rpi-project.py /absolute/project/path [--dry-run]` is the public CLI. It uses Python standard library only. It validates that the root is a directory, `.rpi` is a real directory, and no source tree contains symlinks. It maps `.rpi/PROJECT.md` and `CONTEXT.md` to the same basenames in `.astrolabe/`; guidance files are copied likewise. `.rpi/SESSION.md` is copied verbatim inside `.astrolabe/legacy-rpi/` and its text is indented under a dated `legacy` HISTORY entry. The full `.rpi/` tree is archived at `.astrolabe/legacy-rpi/`, including unknown files. Root `docs/design-plans/` and `docs/implementation-plans/` are copied under `.astrolabe/docs/` if present. Missing optional files use schema-1 defaults. The new STATUS is active, tier none, work null, with a migration summary. PLANNED starts with empty Backlog and Roadmap. A marker `.astrolabe/MIGRATION.md` identifies a completed migration. An existing target without that marker is a conflict; with the marker it is a no-op. Staging uses a temporary directory beside `.astrolabe/` and one final rename. No source is deleted.

## Existing patterns and investigation
The historical `a647a21` tree contains `.rpi/PROJECT.md`, `CONTEXT.md`, and root plan directories. Legacy skills reference optional SESSION.md and guidance files. The current `docs/astrolabe-state-format.md` defines schema 1; `codex/skills/astrolabe-workflow/scripts/project_state.py` initializes new state. Checked 2026-09-16 on branch feature/legacy-rpi-migration at base bf4fd04.

## Alternatives and rationale
In-place moves would risk losing the old workflow's only copy. Merging into an existing `.astrolabe/` needs conflict policy and is outside B2's migration of an unmigrated project. A staged copy keeps the source intact and avoids a partially published target.

## Implementation phases
### Phase 1: Migration engine and behavior tests
Implement preflight, copy/mapping, HISTORY rendering, staging, no-op, and failure behavior. Covers all ACs.
### Phase 2: CLI and documentation
Add argparse entry point, dry-run output, invocation guide, and an end-to-end CLI test. Covers AC2.1–AC2.4 at the user interface.

## Open decisions and risks
Large legacy trees require enough free disk space for a second copy. Historic prose may contain obsolete path references; the tool preserves content without rewriting it.
