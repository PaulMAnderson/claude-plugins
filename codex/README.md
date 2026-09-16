# Astrolabe skills for Codex

The Codex bundle has 13 skills for local research, tracked tasks, design, phased implementation, review, and validation. It uses the same `.astrolabe/` project files as the Claude Code and Gemini distributions.

## Install

From this checkout, install the complete bundle into a project:

```sh
python3 codex/scripts/install.py --project /path/to/project
```

Use `--user` for your user skill directory, `--skills-dir /path/to/skills` for another discovery location, or `--dry-run` to inspect the changes. The default uses relative symlinks to this checkout. `--copy` makes independent copies that include licenses and runtime scripts. The installer checks every destination before writing and will not replace a different existing skill; review or remove a stale installation yourself before retrying.

This checkout includes `.agents/skills/astrolabe-*` links for work in this repository. Install the bundle separately in another project where you intend to use it.

## Choose a skill

| Skill | Purpose |
| --- | --- |
| `$astrolabe-quick` | One-session analysis or helper, with a short outcome |
| `$astrolabe-spec` | Dated task with numbered steps and notes that can be resumed |
| `$astrolabe-design` | Investigated design, alternatives, Definition of Done, and acceptance criteria |
| `$astrolabe-plan` | Ordered phase files and test requirements |
| `$astrolabe-implement` | Task execution, phase reviews, coverage, and final checks |
| `$astrolabe-review` | Plan/code review, findings, fixes, and acceptance coverage |
| `$astrolabe-workflow` | Full workflow entry point and shared gate contract |
| `$astrolabe-research` | Local code, remote code, and documentation research |
| `$astrolabe-debug` | Root cause analysis and regression verification |
| `$astrolabe-context` | Resume and checkpoint context |
| `$astrolabe-house-style` | Language, architecture, test, and writing conventions |
| `$astrolabe-extend-codex` | Skills, project instructions, and distribution |
| `$astrolabe-fanout` | Corpus analysis with worker, critic, and synthesis roles |

For example:

```text
$astrolabe-spec Track the CSV importer in a dated checklist.
$astrolabe-design Design the CSV importer and its acceptance criteria.
$astrolabe-plan /absolute/path/.astrolabe/docs/design-plans/YYYY-MM-DD-csv-import.md
$astrolabe-implement /absolute/path/.astrolabe/docs/implementation-plans/YYYY-MM-DD-csv-import/
```

A larger task can start with `$astrolabe-workflow`. Design-only and planning-only requests stop at the requested deliverable. Existing unambiguous plans can be resumed without resetting the conversation.

## Local state and planned work

Each tier initializes missing `.astrolabe/` files, reads `PROJECT.md` and `STATUS.md`, and checks Backlog and Roadmap in `PLANNED.md` before work. A matching item is shown for a decision. At exit, the tier updates `STATUS.md` and appends to `HISTORY.md`; deferred ideas are added only after the user chooses a list. The Spec tier writes `.astrolabe/docs/specs/YYYY-MM-DD-<slug>.md` and resumes its checked steps and notes.

The [shared state format](../docs/astrolabe-state-format.md) defines all files and the versioned `STATUS.md` schema. Work is local; registration, credentials, network access, and a running service are unnecessary. The optional [Hypercube dashboard](../README.md#hypercube-dashboard) reads explicitly registered projects.

Use `$astrolabe-workflow Start B1` to work from a specific Backlog or Roadmap ID. The item stays in `PLANNED.md` while active or paused. After its requested outcome is verified, completion removes it and records its original text and result in `HISTORY.md`; its ID is never reused.

Full implementation plans live under `.astrolabe/docs/implementation-plans/`. The gate ledger lives under `.astrolabe/runs/<slug>/state.json`; task and review reports sit alongside it. The `astrolabe_state.py` helper in `astrolabe-workflow/scripts/` manages the ledger, while `project_state.py` manages the tier state files. The ledger checks gate order and recorded evidence hashes. Code and test assertions still require review.

## Customize and verify

Optional project guidance goes in `.astrolabe/design-plan-guidance.md` and `.astrolabe/implementation-plan-guidance.md`. For repository-wide defaults, adapt [AGENTS.example.md](AGENTS.example.md) to your project's `AGENTS.md`; installation does not overwrite it.

Run the current behavior and installer tests with:

```sh
python3 -B -m unittest discover -s codex/tests -v
```

The source-map validator (`python3 codex/scripts/validate.py`) currently reports stale fingerprints and two UI metadata failures after the Astrolabe rename. It needs a separate inventory refresh before it can serve as a passing release check. See [PORTING.md](PORTING.md) for the adaptation map and [VALIDATION.md](VALIDATION.md) for earlier port validation history.
