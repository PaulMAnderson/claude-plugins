# Astrolabe plugins

Astrolabe is a set of local workflows for Claude Code, Codex, and Gemini CLI. It tracks work from a small helper through a full design and implementation plan, using the same `.astrolabe/` project files across all three tools.

This is [Paul Anderson's fork](https://github.com/paulanderson/astrolabe-plugins) of [ed3dai/ed3d-plugins](https://github.com/ed3dai/ed3d-plugins). The Claude plugins are in `plugins/`, Codex skills in `codex/skills/`, and Gemini extensions in `gemini/extensions/`.

## Choose a tier

| Tier | Use it for | Claude command | Main artifact |
| --- | --- | --- | --- |
| Micro | One helper function | `/helper-function` | Short outcome in `HISTORY.md` |
| Quick | One-session analysis | `/quick-analysis` | Short outcome in `HISTORY.md` |
| Spec | A task that needs a resumable checklist | `/start-tracked-task` | Dated spec with numbered steps |
| Full | Architecture, acceptance criteria, phased delivery, and review | `/start-design-plan` → `/start-implementation-plan` → `/execute-implementation-plan` | Design, phase plans, review reports, and human test plan |

Codex offers the equivalent `$astrolabe-quick`, `$astrolabe-spec`, `$astrolabe-design`, `$astrolabe-plan`, and `$astrolabe-implement` skills. Gemini has the corresponding skills and `/start-tracked-task`, `/start-design-plan`, and `/start-implementation-plan` commands. See the [Claude workflow guide](plugins/astrolabe-plan-and-execute/README.md), [Codex guide](codex/README.md), and [Gemini workflow guide](gemini/extensions/astrolabe-plan-and-execute/README.md) for tool-specific steps.

Work can move up a tier without losing its earlier notes. A Spec can become input to a Full design when the task needs architecture or explicit acceptance criteria. The skills preserve context across sessions; clearing the conversation between phases is optional.

## Local project state

On first use, a tier initializes missing files under the project's `.astrolabe/` directory. Repeated initialization preserves existing content. Each tier reads the project description and status, checks planned work, then updates status and appends an outcome when it exits.

Start a planned item by ID with Claude Code `/start-planned B1`, Gemini `/start-planned B1`, or Codex `$astrolabe-workflow Start B1`. The agent chooses a tier and keeps the item in `PLANNED.md` while it is active or paused. After its requested outcome is verified, the state helper removes it from the list and records the ID, original text, outcome, and optional artifact in `HISTORY.md`. Completed IDs are never reused.

| File | Purpose |
| --- | --- |
| `PROJECT.md` | Stable, human-authored project description |
| `STATUS.md` | Current tier, work slug, state, and timestamp in a versioned format |
| `HISTORY.md` | Append-only outcomes |
| `PLANNED.md` | Separate Backlog (`B` IDs) and Roadmap (`R` IDs) |
| `CONTEXT.md` | Optional summary for resuming a session |
| `docs/specs/`, `docs/design-plans/`, `docs/implementation-plans/` | Tier documents |

A matching Backlog or Roadmap item is shown before work begins so you can work on it, extend it, or proceed separately. Deferred ideas are added only after you choose Backlog or Roadmap. The [state format](docs/astrolabe-state-format.md) defines the files and `STATUS.md` schema.

Astrolabe project tracking runs locally without registration, credentials, or a service. The optional [Hypercube dashboard](#hypercube-dashboard) reads `STATUS.md` only for projects explicitly added to its watch list.

## Hypercube dashboard

Create a JSON watch list on the machine running the dashboard:

```json
{"projects":[{"name":"Example","path":"/absolute/path/to/project"}]}
```

Run `python3 -m hypercube --config /path/to/projects.json` from this repository, then open `http://127.0.0.1:8765/`. `--host` and `--port` set the listening address. The page reads each registered project's `.astrolabe/STATUS.md` on every request, so status changes appear without a restart. Editing the watch list requires a restart. Missing or invalid status files show an error for that project. The server binds to localhost by default and has no authentication; use a trusted network or access controls if exposing it elsewhere.

### Run with Docker Compose

1. Copy `deploy/hypercube.env.example` to `.env` and set `HYPERCUBE_PROJECTS_ROOT` to the host directory containing the registered projects. Set `HYPERCUBE_UID` and `HYPERCUBE_GID` to an account that can read their `.astrolabe/STATUS.md` files.
2. Copy `deploy/hypercube/projects.example.json` to `deploy/hypercube/projects.json`. Each `path` in this watch list uses the **container** path under `/projects`, such as `/projects/example` for the host directory `${HYPERCUBE_PROJECTS_ROOT}/example`.
3. Run `docker compose up -d --build`, then open `http://127.0.0.1:8765/` on the server. Use `docker compose logs -f hypercube` to inspect startup or read errors.

Compose mounts the watch list and project directory read-only, runs as the configured UID/GID, and binds the published port to localhost by default. Set `HYPERCUBE_BIND_ADDRESS` only when a trusted reverse proxy or network should reach it; the dashboard has no login. Edit the watch list and run `docker compose restart hypercube` to change registrations. Changes to `STATUS.md` appear on the next page load.

## Install

### Claude Code

Register this checkout as a marketplace, then install the core plugins:

```text
/plugin marketplace add file:///absolute/path/to/claude-plugins
/plugin install astrolabe-basic-agents@astrolabe-plugins
/plugin install astrolabe-research-agents@astrolabe-plugins
/plugin install astrolabe-plan-and-execute@astrolabe-plugins
/plugin install astrolabe-extending-claude@astrolabe-plugins
```

Optional plugins are `astrolabe-house-style`, `astrolabe-getting-started`, `astrolabe-hook-skill-reinforcement`, and `astrolabe-hook-claudemd-reminder`. The [marketplace manifest](.claude-plugin/marketplace.json) lists all eight. Reload or restart Claude Code after updating the checkout.

### Codex

Install the 13-skill bundle for a project:

```sh
python3 codex/scripts/install.py --project /path/to/project
```

Use `--user` for your user skill directory, `--copy` for portable copies, or `--dry-run` to inspect changes. The [Codex guide](codex/README.md) covers collisions and updating installed copies.

### Gemini CLI

Link the extensions you need from `gemini/extensions/`, beginning with `astrolabe-plan-and-execute`:

```sh
gemini extensions link /absolute/path/to/claude-plugins/gemini/extensions/astrolabe-plan-and-execute
```

The [Gemini workflow guide](gemini/extensions/astrolabe-plan-and-execute/README.md) lists its commands, skills, and local state helper. Linking keeps the extension's scripts and references available alongside its skills.

## This repository's planned work

The repository's [planned list](.astrolabe/PLANNED.md) contains remaining Backlog work:

- **B2:** Build a migration script or skill for other projects with existing `.rpi` state.

Other projects maintain their own Backlog and Roadmap in their own `.astrolabe/PLANNED.md`.

## Repository map

- `plugins/`: Claude Code plugins and commands.
- `codex/skills/`: Codex skills; `codex/scripts/install.py` installs the bundle.
- `gemini/extensions/`: Gemini extensions, commands, skills, hooks, and scripts.
- `docs/astrolabe-state-format.md`: Shared local state contract.
- `.astrolabe/docs/`: This repository's design and implementation documents.
- `docs/test-plans/`: Human acceptance steps.
- `CHANGELOG.md`: Releases and the rename history.

## Attribution and license

The Claude workflow and some extension skills derive from [obra/superpowers](https://github.com/obra/superpowers) by Jesse Vincent. Some house-style material derives from [Trail of Bits Skills](https://github.com/trailofbits/skills). See the licenses and notices in each plugin or skill. MIT-derived material retains its MIT license; other content is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
