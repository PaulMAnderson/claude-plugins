# Port validation

Validated on 2026-09-14. These are local structural, helper-behavior, and installation checks; no independent model evaluation or live Codex task execution is claimed.

## Executed checks

| Check | Result |
| --- | --- |
| Codex skill-creator `quick_validate.py` on every skill | 12/12 valid |
| `python3 codex/scripts/validate.py` | 12 skills; all metadata, local links, syntax, licenses, and 148 source mappings pass |
| `python3 -B -m unittest discover -s codex/tests -v` | 12 tests pass |
| Project installation dry run, actual links, repeated install | All 12 skills; repeat is a no-op |
| Portable copy in temporary project | All skills/resources/licenses copied; installed state helper runs |
| `git diff --check` plus new-file whitespace scan | Pass |

The system's default Python lacks PyYAML. The official skill validator was run with the already installed Python environment at `~/.local/share/uv/tools/phy/bin/python`, which includes PyYAML 6.0.3. No package installation was required. The shipped helper, installer, bundle validator, and tests use only Python's standard library.

## Merge integration validation

Rechecked after merging the Gemini 1.13.0 updates on 2026-09-14: all 12 workflow/installation tests pass. The changed Gemini task reports, recovery ledger, review packages, and review feedback procedures are covered by the existing Codex execution/review guidance and the deliberate reconciliations in PORTING.md. Refreshed four reviewed source fingerprints and added four mappings for the Gemini helpers and receiving-code-review skill; bundle validation now covers 152 sources.

## Behavioral invariants exercised by the tests

- A gate cannot skip unfinished prerequisites or complete without nonempty evidence.
- A two-phase run progresses through all gates and survives separate CLI processes.
- A Minor issue blocks its gate; the original finding is preserved verbatim, and resolution requires evidence.
- A new finding after final review invalidates final review, coverage, and verification until re-reviewed.
- Changed/deleted evidence prevents a clean check and blocks downstream completion.
- Reopening earlier work invalidates downstream gates and retains historical evidence.
- Blocked status requires a reason and never counts as success.
- Reinitialization cannot erase an existing run.
- Empty/outside-project evidence and run path traversal are rejected.
- Installer dry run writes nothing; repeated symlink installation is safe.
- A name collision prevents partial installation and preserves user content.
- Portable copies include runtime resources and licenses; modified copies cannot be overwritten.

## Local workflow walkthrough

Inspected the written procedures for design-only vs end-to-end scope; task vs phase review cadence; incomplete legacy plan recovery; stale tests after fixes; reviewer timeout; unchanged repeated failures; manual acceptance; existing user edits and untracked implementation; unavailable subagents; and compaction/resume.

Corrections made during validation: three UI descriptions were too short and were rewritten; review-package guidance was given a working relative link; installer symlinks were made relative for repository portability; legacy `.rpi/exec/progress.md` recovery was made explicit.

The automated source inventory proves that every inventoried entry has a maintained target and an unchanged source fingerprint. It does not prove semantic parity. The workflow comparison in PORTING.md records the preserved invariants and deliberate changes. The ledger validates declared evidence integrity; a reviewer still must inspect commands, assertions, requirements, and actual code. Skills and optional AGENTS.md instructions are procedural guidance, not an installed background hook or enforced security boundary.
