# Hypercube status dashboard design

## Summary
B1 builds a small, standalone Python service in this repository. An operator registers project directories in a Hypercube-side JSON watch list. The service reads each registered `.astrolabe/STATUS.md` on every dashboard request and renders a single status page. It never discovers projects or writes project state.

## Definition of Done
- B1: Build a Hypercube crawler and minimal web UI that reads registered projects' STATUS.md files. Supplied by the backlog and explicit `Start B1` request.
- User-confirmed: place the standalone app in this repository.
- A configured project appears with its name, status, current tier/work, update time, and summary; unreadable or invalid entries show an error without hiding healthy projects.
- The service runs locally with only Python's standard library and documented commands. No authentication or remote filesystem protocol is specified; deployments should bind it to a trusted interface.

## Acceptance Criteria
### hypercube-status-dashboard.AC1: Explicit registration
- AC1.1: A valid watch list path registers exactly its listed projects; unlisted projects remain invisible.
- AC1.2: Duplicate names or malformed list entries produce a clear configuration error.
### hypercube-status-dashboard.AC2: Status collection
- AC2.1: A valid schema-1 STATUS.md yields all five frontmatter fields and its summary.
- AC2.2: Missing, unreadable, malformed, or unsupported status files yield per-project errors while other projects still load.
- AC2.3: A later file update appears on the next request without restart.
### hypercube-status-dashboard.AC3: Web UI
- AC3.1: GET / displays registered projects and their status or error.
- AC3.2: Project names and summary text are escaped as HTML.
- AC3.3: Unknown paths return 404 and the server binds to the configured address/port.

## Architecture and contracts
The proposed `hypercube/` package contains a pure parser and collector plus a standard-library HTTP server. A JSON watch list has `{"projects":[{"name":"Example","path":"/absolute/project/path"}]}`. The server reads only `<path>/.astrolabe/STATUS.md`; paths must be absolute, names nonempty and unique. Registration changes require editing the watch list and restarting the server; status changes are read per request. Collection returns one success or error record per registered project in watch-list order. The parser accepts exactly schema version 1; status is active, paused, or archived; tier is none, micro, quick, spec, or design; work is null or a lowercase hyphenated slug; update time is ISO 8601 with timezone; the body is one nonempty line. Invalid data is displayed as an error without the file content. The UI uses escaped HTML. The operator starts `python3 -m hypercube --config PATH --host HOST --port PORT`.

## Existing patterns and investigation
`docs/astrolabe-state-format.md` defines schema 1. `codex/skills/astrolabe-workflow/scripts/project_state.py` writes STATUS.md. The previous project-tracking design defers the Hypercube implementation and specifies an explicit server-side watch list and pull-based read. No Hypercube app, manifest, or deployment configuration was found in this checkout or sibling directories checked under `/home/paul/Claude`.

## Alternatives and rationale
A standard-library Python service matches the repository's existing tooling and avoids a dependency stack for one read-only page. A static build would require a separate refresh step; a browser-only reader cannot safely access registered local directories. Per-request reads make updates visible immediately at this scale.

## Implementation phases
### Phase 1: Watch list and collector
Implement configuration validation, STATUS parsing, and per-project collection with behavioral tests. Covers AC1 and AC2.
### Phase 2: Web interface and CLI
Implement escaped HTML rendering, HTTP routing, CLI options, usage documentation, and integration tests. Covers AC3 and verifies AC2.3 through HTTP.

## Open decisions and risks
The deployment target and exact Hypercube host path were not supplied. The HTTP server has no authentication; bind to localhost by default and place behind trusted access controls if deployed elsewhere.
