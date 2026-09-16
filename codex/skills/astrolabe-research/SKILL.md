---
name: "astrolabe-research"
description: "Investigate local or remote code and external documentation for an Astrolabe design, implementation plan, or technical question, with verified paths, versions, sources, and explicit uncertainties."
---

# Research for a concrete decision

Define the question and deliverable before searching: architecture, behavior, dependency contract, integration pattern, or failure cause. Read the minimum relevant project context and instructions.

**Local code:** use `rg --files` and `rg` to locate entry points, definitions, callers, tests, configuration, and project instructions. Trace actual data/control flow across boundaries. Read representative implementations and test setup. Record exact paths/symbols/line references and distinguish current files from proposed new ones. Do not infer behavior from filenames or comments without checking code.

**Remote code:** inspect the specified repository and version/commit through available repository tools or an authorized temporary checkout. Use the actual source and tests, record the revision, and separate that version's behavior from current local dependencies. Do not modify the user's checkout merely to investigate.

**Internet/dependencies:** identify the installed/pinned version first. Prefer official docs, source, and primary papers. Fetch the actual page/source supporting exact API or behavioral claims; search snippets are leads. Check unstable facts live when tools are available. If access is unavailable, state the limitation and leave unverified contracts unresolved instead of inventing signatures.

**Combined research:** gather local interfaces and external contracts independently where practical, then reconcile differences. Parallel tool calls can serve independent reads. Subagent delegation depends on actual availability and authorization; it is not needed for the research method.

Return a focused report with: question; findings and evidence; current patterns to reuse; exact contracts/paths/versions; alternatives where relevant; uncertainty/conflicts; implications for the next design/plan/task. Include dated source URLs or commit links for external facts. Summarize findings in the plan and link the detailed report instead of flooding the main context with search output.
