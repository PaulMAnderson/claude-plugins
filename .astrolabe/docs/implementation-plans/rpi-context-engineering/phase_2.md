---
phase: 2
title: Update README and documentation with attribution and new identity
context-budget: small
files-required:
  - docs/design-plans/2026-03-01-rpi-context-engineering.md
  - README.md
depends-on: [phase_1]
---

# Phase 2: README and Attribution

## Acceptance Criteria
- rpi-context-engineering.AC1.3 (attribution block)
- rpi-context-engineering.AC1.4 (marketplace/docs reflect rpi-* naming)

## Tasks

### Task 2.1 — Rewrite README.md header and description
Replace the opening section with new project identity:

```markdown
# rpi-plugins

Claude Code plugins for design, implementation, and development workflows,
implementing the Research-Plan-Implement (RPI) methodology.

This is **Paul Anderson's fork** of [ed3dai/ed3d-plugins](https://github.com/ed3dai/ed3d-plugins).
It diverges from upstream in: RPI branding, integrated Context Engineering (CE) features,
context monitoring, and compression-aware file templates.
```

### Task 2.2 — Update all install instructions
Replace every occurrence of `ed3d-*` in install examples with `rpi-*`, e.g.:
```
/plugin install rpi-plan-and-execute@rpi-plugins
```

### Task 2.3 — Add attribution block
Add the following section before the License section:

```markdown
## Attribution

This repository is a fork of [ed3dai/ed3d-plugins](https://github.com/ed3dai/ed3d-plugins).

`rpi-plan-and-execute` and parts of `rpi-extending-claude` are derived from
[`obra/superpowers`](https://github.com/obra/superpowers) by Jesse Vincent (MIT licence).
The original code has been extensively modified. See `plugins/rpi-plan-and-execute/LICENSE.superpowers`.

Some skills in `rpi-house-style` are derived from `obra/superpowers` and others
(notably `property-based-testing`) from the
[Trail of Bits Skills repository](https://github.com/trailofbits/skills).

**Key divergences from upstream `ed3dai/ed3d-plugins`:**
- Renamed from `ed3d-*` to `rpi-*` namespace
- Context Engineering integration (context monitor hook, compression skill)
- CE memory-tier-annotated design and implementation plan templates
```

### Task 2.4 — Update plugins/rpi-plan-and-execute/README.md
Update all references to `ed3d-plan-and-execute` → `rpi-plan-and-execute` and all
cross-plugin dependency names from `ed3d-*` → `rpi-*`. Update the marketplace install
command examples. Update the LICENSE.superpowers path reference.

## Done When
README.md contains the attribution block. No `ed3d-` strings in README.md or the plugin's own README.
