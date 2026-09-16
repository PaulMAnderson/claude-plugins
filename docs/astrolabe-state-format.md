# Astrolabe local project state, schema 1

Every project can use `.astrolabe/` without registration, a network connection, credentials, or a service. Create missing files on first use; never replace existing project content during initialization.

## Files

- `PROJECT.md`: stable, human-authored project description. Initialization writes a heading and a short invitation to describe the project. Do not use it as an event log.
- `STATUS.md`: replaceable live snapshot. Frontmatter has exactly the five fields shown below, followed by one human-readable line.
- `HISTORY.md`: append-only entries. Tier entries have an ISO 8601 timestamp, tier, work slug, intent, outcome, and result (`completed` or `paused`). Planned-item start and completion entries also preserve the planned ID and original text. Preserve prior entries.
- `PLANNED.md`: `## Backlog` and `## Roadmap` sections. Backlog entries use unique `B1`, `B2`, etc.; Roadmap uses unique `R1`, `R2`, etc. IDs never get reused. Match requested work by reading prose, not by keyword matching.
- `CONTEXT.md`: optional resume summary, merged when context is compressed. It is separate from the current `STATUS.md` snapshot and append-only `HISTORY.md`.
- `docs/specs/YYYY-MM-DD-{slug}.md`, `docs/design-plans/`, and `docs/implementation-plans/`: tier documents.

```yaml
---
schema_version: 1
status: active
current_tier: none
current_work: null
last_updated: 2026-09-16T12:00:00+00:00
---
Ready for local work.
```

`status` is `active`, `paused`, or `archived`. `current_tier` is `none`, `micro`, `quick`, `spec`, or `design`. `current_work` is a lowercase hyphenated slug or YAML `null`. `last_updated` is an ISO 8601 timestamp with timezone. A completed tier sets `current_tier: none` and `current_work: null`, with the one-line summary describing its latest outcome. An active or paused work item retains its tier and slug until an actual completion.

History entries use this shape:

```markdown
### 2026-09-16T12:00:00+00:00 — quick — sample-work

- Intent: Analyze the sample.
- Outcome: Created the requested plot and verified its inputs.
- Result: completed
```

Planned entries use one line each under the correct heading:

```markdown
## Backlog
- B1: Add a concrete feature.

## Roadmap
- R1: Explore a broader future direction.
```

## Planned-item lifecycle

Start a specific item with `start-planned --id B1 --tier spec --work feature-slug` (or an `R` ID), then follow the chosen tier. The helper appends a `Planned-Status: started` history entry with the original text. The item remains in `PLANNED.md` while work is active or paused. Keep its ID in the spec, design, or implementation artifact.

After the requested outcome is verified and the tier is finished, run `complete-planned --id B1 --outcome "Verified result" --artifact "path/to/artifact"`. The artifact is optional. This removes the item from `PLANNED.md` and appends a `Planned-Status: completed` entry with the ID, original text, tier, work slug, outcome, and optional artifact to `HISTORY.md`. A completed intermediate design or phase leaves the item in `PLANNED.md` if its requested outcome is still pending. Retrying completion does not duplicate the history entry. `add-planned` checks both files so completed IDs are never reused. Preserve the history if editing the planned list manually.

A future Hypercube service may maintain its own watch-list of project paths and periodically pull registered projects' `.astrolabe/STATUS.md` files. Registration is only a Hypercube-side watch-list change. Projects absent from that list remain invisible to the service and continue to work locally.
