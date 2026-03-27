---
name: writing-design-plans
description: Use after brainstorming completes - writes validated designs to docs/design-plans/ with structured format and discrete implementation phases required for creating detailed implementation plans
user-invocable: false

## Overview

Complete the design document by appending validated design from brainstorming to the existing file (created in Phase 3 of starting-a-design-plan) and filling in the Summary and Glossary placeholders.

**Core principle:** Append body to existing document. Generate Summary and Glossary. Commit for permanence.


| Dependencies between components | Step-by-step instructions |
| "Done when" verification criteria | Test code |

**Exception: Contracts get full specification.** When a component exposes an interface that other systems depend on, specify the contract fully:

- API endpoints with request/response shapes
- Inter-service interfaces (types, method signatures)
- Database schemas that other systems read
- Message formats for queues/events

Contracts can include code blocks showing types and interfaces. This is different from implementation code — contracts define boundaries, not behavior.

**Example — Contract specification (OK):**
```typescript
interface TokenService {
  generate(claims: TokenClaims): Promise<string>;
  validate(token: string): Promise<TokenClaims | null>;
}

interface TokenClaims {
  sub: string;      // service identifier
  aud: string[];    // allowed audiences
  exp: number;      // expiration timestamp
}
```

**Example — Implementation code (NOT OK for design plans):**
```typescript
async function generate(claims: TokenClaims): Promise<string> {
  const payload = { ...claims, iat: Date.now() };
  return jwt.sign(payload, config.secret, { algorithm: 'RS256' });
}
```

The first defines what the boundary looks like. The second implements behavior — that belongs in implementation plans.


## File Location and Naming

**File location:** `docs/design-plans/YYYY-MM-DD-<topic>.md`

The file is created by starting-a-design-plan Phase 3. This skill appends to that file.

**Expected naming convention:**
- Good: `docs/design-plans/2025-01-18-oauth2-svc-authn.md`

## Document Structure

**The design document already exists** from Phase 3 of starting-a-design-plan with this structure:

```markdown
# [Feature Name] Design

## Summary
<!-- TO BE GENERATED after body is written -->

## 🔴 Definition of Done
[Already written - confirmed in Phase 3]

## 🔴 Acceptance Criteria
<!-- TO BE GENERATED and validated before glossary -->

## 🔵 Glossary
<!-- TO BE GENERATED after body is written -->
```

**This skill appends the body sections:**

**Note on tier emojis:** Each section heading includes a tier emoji (🔴/🟡/🔵) that signals to future agents how urgently they need to read it. Do not explain the emoji in the document body; the Memory Tier Index (written after Summary) provides the legend.

```markdown

## Implementation Phases: Critical Requirements

**YOU MUST break design into discrete, sequential phases.**

**Each phase should:**
- Achieve one cohesive goal
- Build on previous phases (explicit dependencies)
- End with a working build and clear "done" criteria
- Use exact file paths and component names from codebase investigation


## Detailed Guidance and Process

Read `plugins/rpi-plan-and-execute/skills/writing-design-plans/REFERENCE.md` for:
- Legibility header and Memory Tier Index format
- Phase verification checklist
- Codebase investigation findings guidance
- Writing style details
- Acceptance Criteria generation (coverage, structure, validation)
- Summary and Glossary generation
- Common rationalizations to avoid
