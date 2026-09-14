# RPI skills for Codex

This port preserves the Claude Code/Gemini RPI process in 12 Codex skills: investigate → design → plan → implement → review/fix → validate. It includes durable phase/task progress, exact acceptance-criterion tracing, context recovery, language guidance, and explicit completion gates.

## Use

The repository's `.agents/skills/` links make these skills discoverable when working in this repository. For another project, install the entire bundle so sibling references remain available:

```sh
python3 /path/to/claude-plugins/codex/scripts/install.py --project /path/to/project
```

For all your projects:

```sh
python3 /path/to/claude-plugins/codex/scripts/install.py --user
```

`--user` writes to `~/.agents/skills`; the installer requires normal filesystem permission for that location. This port does not automatically change user-wide configuration. For a deployment using another supported discovery location, pass `--skills-dir /actual/skills/directory` explicitly.

Default installation creates relative symlinks to the bundle; updates in this checkout are immediately available through them. Use `--copy` for independent portable copies, or `--dry-run` to inspect the destinations. The installer preflights every name, preserves unrelated skills, and refuses differing existing copies. To update a modified copy, review/merge its changes deliberately; there is no force-overwrite option. Keep the source checkout available for symlink installations. Copied bundles include their licenses and all runtime resources.

Codex's current documentation describes `.agents/skills` discovery, symlink support, and `$skill-name` invocation. Restart Codex if new skills do not appear. See [Build skills](https://learn.chatgpt.com/docs/build-skills) and [AGENTS.md guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md), checked 2026-09-14.

```text
$rpi-design Add <feature> to this project.
$rpi-plan /absolute/path/docs/design-plans/YYYY-MM-DD-feature.md
$rpi-implement /absolute/path/docs/implementation-plans/YYYY-MM-DD-feature/
```

Or request the complete workflow:

```text
$rpi-workflow Design, plan, implement, review, and validate <feature>.
```

The stages continue within existing authorization. Design-only and planning-only requests stop at their requested deliverable. Existing unambiguous plans and `.rpi` context can be resumed; no forced conversation reset is needed.

| Skill | Purpose |
| --- | --- |
| `rpi-workflow` | Entry point, process contract, quality gates, customization, progress helper |
| `rpi-design` | Investigated architecture, alternatives, Definition of Done, scoped ACs |
| `rpi-plan` | Detailed ordered phase files, plan review, test requirements |
| `rpi-implement` | Task execution, reports, phase reviews, final validation and handoff |
| `rpi-review` | Plan/code review, incoming feedback, issue fixes, acceptance coverage |
| `rpi-research` | Local code, remote code, internet documentation, combined findings |
| `rpi-debug` | Reproduction, root cause, hypotheses, regression verification |
| `rpi-context` | Merge/recover session and project context across sessions |
| `rpi-quick` | One-off analysis and small helpers with verification/session logging |
| `rpi-house-style` | Python, MATLAB, R, MySQL, architecture, tests, technical writing |
| `rpi-extend-codex` | Skills, directives, project context, role briefs, distribution |
| `rpi-fanout` | Worker/critic/synthesis analysis with coverage and recovery |

## Detailed checks and progress

Plans keep the original locations and markers:

```text
docs/design-plans/YYYY-MM-DD-feature.md
docs/implementation-plans/YYYY-MM-DD-feature/phase_01.md
docs/implementation-plans/YYYY-MM-DD-feature/test-requirements.md
docs/test-plans/YYYY-MM-DD-feature.md
.rpi/runs/feature/state.json
.rpi/runs/feature/reports/
.rpi/CONTEXT.md
.rpi/PROJECT.md
.rpi/SESSION.md
```

The ledger tracks design, plan, each phase's read/execute/review gates, final review, coverage, and verification. Task progress stays in phase files with evidence reports. Findings retain verbatim descriptions and severity. Completing a gate requires completed prerequisites and nonempty evidence files; unresolved findings block their gate. Evidence is hashed so later edits/deletions are detected. Reopening a gate invalidates downstream gates and preserves history.

Example from the repository root (replace project, design, plan, and phase titles):

```sh
python3 codex/skills/rpi-workflow/scripts/rpi_state.py --root /path/to/project --run feature init --design docs/design-plans/YYYY-MM-DD-feature.md --plan docs/implementation-plans/YYYY-MM-DD-feature --phase "Foundation" --phase "Behavior"
python3 codex/skills/rpi-workflow/scripts/rpi_state.py --root /path/to/project --run feature status
python3 codex/skills/rpi-workflow/scripts/rpi_state.py --root /path/to/project --run feature check
```

Run `rpi_state.py --help` or a subcommand's `--help` for all transitions. Evidence must be a nonempty file inside the target project; use immutable report files or snapshots so ongoing edits do not invalidate earlier evidence unintentionally. The controller owns ledger writes. Task/review agents write separate reports.

The helper checks recorded gate/evidence integrity; it cannot establish that a report is truthful or that code implements an AC. The skills require direct inspection of code, tests, output, and current revision. This is explicit checkpoint monitoring, not an automatically installed background watcher or model-enforced security boundary. Pending manual acceptance and unavailable environments remain visibly unverified.

## Customize

Preserved customization files:

- `.rpi/design-plan-guidance.md`: terms, constraints, architecture, scope.
- `.rpi/implementation-plan-guidance.md`: coding, testing, review, commit conventions.

For repository-wide RPI defaults, merge the relevant lines from [AGENTS.example.md](AGENTS.example.md) into the target project's existing `AGENTS.md`. This is optional; the installer does not overwrite project instructions or install hooks. If every substantial task should use RPI automatically, the example provides that explicit project preference. Otherwise skills remain naturally selectable or explicitly invocable.

## Validate the port

Python 3.9+; no third-party runtime dependencies:

```sh
python3 codex/scripts/validate.py
python3 -B -m unittest discover -s codex/tests -v
```

The validator checks metadata, UI metadata, sibling references, licenses, Python syntax, vendor-tool remnants, and the complete fingerprinted source inventory. Source changes deliberately fail validation until their port is reviewed and `source-map.json` updated. The tests exercise gate order, evidence requirements, blockers, review findings, recovery, stale evidence, and safe installation.

See [PORTING.md](PORTING.md) for coverage and adaptation decisions and [VALIDATION.md](VALIDATION.md) for the executed checks and their limits.
