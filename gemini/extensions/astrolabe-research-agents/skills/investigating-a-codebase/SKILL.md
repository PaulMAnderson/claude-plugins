---
name: investigating-a-codebase
description: Systematically explore a codebase to find information, patterns, and verify assumptions
---

# Investigating a Codebase

Understand current codebase state to ground planning and design decisions in reality, not assumptions. Find existing patterns, verify design assumptions, and provide definitive answers about what exists and where.

## Core Investigation Workflow

1. **Start with entry points** - main files, index, package.json, config
2. **Use multiple search strategies** - glob patterns, grep keywords, read files
3. **Follow traces** - imports, references, component relationships
4. **Verify don't assume** - confirm file locations and structure
5. **Report definitively** - exact paths or "not found" with search strategy used

## If Verifying Design Assumptions

When given design assumptions to verify:

1. **Extract assumptions** - list what the design expects to exist
2. **Search for each** - file paths, functions, patterns, dependencies
3. **Compare reality vs expectation** - matches, discrepancies, additions, missing
4. **Report explicitly**:
   - Confirmed: "Design assumption correct: auth.ts:42 has login()"
   - Discrepancy: "Design assumes auth.ts, found auth/index.ts instead"
   - Addition: "Found logout() not mentioned in design"
   - Missing: "Design expects resetPassword(), not found"

## Reporting Findings

Lead with direct answer:
- Answer the question first
- Supporting details second
- Evidence with exact file paths and line numbers

Provide actionable intelligence:
- Exact file paths (src/auth/login.ts:42), not vague locations
- Relevant code snippets showing current patterns
- Dependencies and versions when relevant
- Configuration files and current settings
- Naming, structure, and testing conventions

Handle "not found" confidently:
- "Feature X does not exist" is valid and useful
- Explain what you searched and where you looked
- Suggest related code as starting point
- Report negative findings prevents hallucination
