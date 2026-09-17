---
name: migrating-legacy-rpi-projects
description: Convert a project's legacy .rpi/ state directory to the current .astrolabe/ layout, including remaining .rpi references repo-wide
user-invocable: true
---

# Migrating Legacy RPI Projects

Use when a project still has a `.rpi/` directory from before the Astrolabe rename and needs full conversion, not just a side-by-side archive.

## Entry

Follow [the shared project state entry contract](../../references/project-state.md) using tier `spec`, with one substitution: initialization happens via the migration script (Work step 1) instead of `astrolabe-state.py init`, since the target has no `.astrolabe/` yet. Confirm `.rpi/` exists and `.astrolabe/` does not; if `.astrolabe/` already exists, stop and tell the user, since the migration script refuses to overwrite it.

## Work

Start the spec with these steps, then track progress through them with `spec-step`/`spec-note`:

```sh
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/astrolabe-state.py" --root "$PWD" spec-start --work rpi-to-astrolabe-migration \
  --intent "Convert legacy .rpi/ state to .astrolabe/ and remove remaining .rpi references" \
  --step "Preview and run migrate-rpi-project.py" \
  --step "Fold docs/design-plans and docs/implementation-plans fully into .astrolabe/docs" \
  --step "Remove the now-archived .rpi/ directory, including untracked scratch content" \
  --step "Grep the repo for remaining .rpi references and rewrite each to its .astrolabe equivalent" \
  --step "Verify git status/diff and run the project's test suite"
```

1. **Preview, then run the archival script.** Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/migrate-rpi-project.py" "$PWD" --dry-run` and show the mapping. Then run it without `--dry-run`. It creates `.astrolabe/legacy-rpi/` as a byte-for-byte archive of `.rpi/`, generates schema-1 `STATUS.md`/`HISTORY.md`/`PLANNED.md`, copies `PROJECT.md`/`CONTEXT.md`/guidance files, and copies `docs/design-plans/` and `docs/implementation-plans/` into `.astrolabe/docs/` if present. It touches nothing outside the new `.astrolabe/` directory and never deletes `.rpi/` itself — that's deliberate, so the remaining steps here are what turn the archive into a full migration.

2. **Fold the plan directories in.** The script *copies* `docs/design-plans/` and `docs/implementation-plans/` into `.astrolabe/docs/`, so the originals now exist in both places. Remove the top-level `docs/design-plans/` and `docs/implementation-plans/` (`git rm -r` if tracked, `rm -r` if not) — git's rename detection picks up the move on the next `git status`/`diff` even though it happened as a copy-then-delete. Leave `docs/notes/` and anything else under `docs/` alone; only the plan directories belong in the Astrolabe schema.

3. **Remove the archived `.rpi/`.** Its full content already lives at `.astrolabe/legacy-rpi/`. Delete `.rpi/` entirely, including untracked scratch files it contains (e.g. lock files, exec scratch dirs) — those were copied into the archive too, so nothing is lost. Use `git rm -r` for tracked paths and plain `rm -r` for untracked ones.

4. **Sweep for remaining `.rpi` references.** Grep tracked files repo-wide for the literal string `.rpi` (exclude `.astrolabe/legacy-rpi/`, which is meant to preserve the original text verbatim, and `.git/`). Check code (including functional default paths and arguments, not just comments), docs, `CLAUDE.md`/`AGENTS.md`, config and dotfiles (e.g. `.dockerignore`), and tests. Rewrite each to its `.astrolabe` equivalent using judgment: a path reference becomes the matching `.astrolabe` path; a reference to a file the new schema doesn't have (e.g. the old `SESSION.md`) should point instead at its replacement (the dated legacy entry in `HISTORY.md`) or be described as historical. Record what you changed with `spec-note`.

5. **Verify before closing out.** Run `git status`/`git diff` and confirm only the intended renames and reference rewrites appear — no unrelated pre-existing uncommitted work should be touched. Run the project's existing test suite if it has one. If the legacy `PROJECT.md` content is stale or clearly a placeholder, use judgment on whether to refresh it; this is optional and project-specific, not part of the mechanical migration.

## Exit

Run `spec-done --work rpi-to-astrolabe-migration --outcome "OUTCOME"` with the same script/root arguments once all steps are checked and verified. This appends the outcome to `HISTORY.md` and updates `STATUS.md`. Do not commit unless the user asks — leave the result in the working tree for review, same as any other tracked task.
