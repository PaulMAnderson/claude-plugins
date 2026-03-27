---
name: howto-code-in-typescript
description: Use when writing TypeScript code, reviewing TS implementations, or making decisions about type declarations, function styles, or naming conventions - comprehensive house style covering type vs interface rules, function declarations, FCIS integration, immutability patterns, and type safety enforcement
user-invocable: false
---

# TypeScript House Style

## Overview

Comprehensive TypeScript coding standards emphasizing type safety, immutability, and integration with Functional Core, Imperative Shell (FCIS) pattern.

**Core principles:**
- Types as documentation and constraints
- Immutability by default prevents bugs
- Explicit over implicit (especially in function signatures)
- Functional Core returns Results, Imperative Shell may throw
- Configuration over decoration/magic

## Quick Self-Check (Use Under Pressure)

When under deadline pressure or focused on other concerns (performance, accuracy, features), STOP and verify:

- [ ] Using `Array<T>` not `T[]`
- [ ] Using `type` not `interface` (unless class contract)
- [ ] Using math.js for money/currencies/complex math
- [ ] Parameters are `readonly` or `Readonly<T>`
- [ ] Using `unknown` not `any`
- [ ] Using `null` for absent values (not `undefined`)
- [ ] Using function declarations (not const arrow) for top-level functions
- [ ] Using named exports (not default exports)
- [ ] Using `===` not `==`
- [ ] Using `.sort((a, b) => a - b)` for numeric arrays
- [ ] Using `parseInt(x, 10)` with explicit radix

**Why this matters:** Under pressure, you'll default to muscle memory. These checks catch the most common violations.

## Type Declarations

### Type vs Interface

**Always use `type` except for class contracts.**

Types compose better with unions and intersections, support mapped types, and avoid declaration merging surprises. Interfaces are only for defining what a class must implement.

### Naming Conventions: Boolean

**Use is/has/can/should/will prefixes. Avoid negative names.**

```typescript
// GOOD
const isActive = true;
const hasPermission = checkPermission();
const canEdit = user.role === 'admin';
```

## Functions

### Declaration Style

**Use `function` declarations for top-level functions. Use arrow functions for inline callbacks.**

Function declarations are hoisted and more visible. Arrow functions capture lexical `this` and are concise for callbacks.

### Const Arrow Functions

**Use `const foo = () => {}` declarations only for stable references.**

Store callbacks and memoized function references as const arrow functions. Never use for top-level exported functions.

## Immutability

### Readonly by Default

**Mark function parameters and object properties `readonly` unless mutation is explicit and unavoidable.**

Immutable parameters prevent accidental modifications. The compiler enforces this at the call site.

## Type Safety

### Never Use 'any'

**Use `unknown` instead of `any`. Cast explicitly with type guards.**

```typescript
// GOOD
const data: unknown = getValue();
if (typeof data === 'string') {
  console.log(data.toUpperCase());
}

// BAD
const data: any = getValue();
data.toUpperCase(); // no type checking
```

## When to Read REFERENCE.md

For all rules, patterns, and examples beyond the core rules above, Read the reference file when your task requires them:

**Read `plugins/rpi-house-style/skills/howto-code-in-typescript/REFERENCE.md` when:**
- Task involves classes, generics, utility types, FCIS patterns, or module organisation
- Task involves specific libraries: math.js, neverthrow, typebox, type-fest
- Task involves async patterns, type assertions, type guards, enums, or discriminated unions
- Task requires advanced immutability (deep readonly, arrays)
- You are unsure whether a rule applies — look it up rather than guessing

**Companion references in this directory:**
- `type-fest.md` — type-fest library patterns
- `typebox.md` — TypeBox schema patterns
