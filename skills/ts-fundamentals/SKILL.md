---
name: ts-fundamentals
description: Use when reviewing TypeScript project structure, tsconfig setup, naming conventions, JSDoc documentation, module organization, or enforcing code-level consistency. Applies to both frontend and backend TypeScript projects.
---

# TypeScript Fundamentals Skill

Use when writing, reviewing, or refactoring TypeScript with a focus on correctness and maintainability.

## Core principles

1. Prefer explicit types at module boundaries; let the compiler infer inside function bodies.
2. Model the domain with types before writing logic.
3. Avoid `any`. Use `unknown` for truly unknown values and narrow at the boundary.
4. Keep types small and composable. Prefer intersection and union over large monolithic interfaces.
5. Write code that is easy to delete — avoid deep coupling through concrete classes or global mutable state.
6. Fail fast: validate untrusted input at system entry points and return typed errors instead of throwing broadly.

## tsconfig baseline

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "verbatimModuleSyntax": true,
    "skipLibCheck": false
  }
}
```

## Naming conventions

| Context | Convention | Example |
|---|---|---|
| Variables, functions | `camelCase` | `getUserById`, `pageLimit` |
| Types, interfaces, classes | `PascalCase` | `ProductInput`, `UserService` |
| Constants (module-level) | `SCREAMING_SNAKE` | `MAX_PAGE_SIZE = 100` |
| Files | `kebab-case` | `user-service.ts` |
| Boolean variables | `is/has/can/should` prefix | `isActive`, `hasPermission` |

- Name functions with verbs: `fetchUser`, `createOrder`.
- Name types with nouns: `User`, `OrderSummary`, `ValidationResult`.
- Do not abbreviate unless domain-standard (`id`, `url`, `db`, `req`, `res`).

## Code review checklist

- [ ] No `any`; unknown input narrowed at boundary
- [ ] Strict null checks respected; optional fields accessed safely
- [ ] No unused imports or variables
- [ ] Functions/types named with verbs/nouns consistently
- [ ] Domain logic in `services/`, transport in handlers, types in `models/`
- [ ] JSDoc present for exported public API
- [ ] `import type` used for type-only imports
- [ ] No runtime side effects at module scope except safe initialization

## References

Local reference files:
- [references/types.md](references/types.md) — type design patterns, branded types, generics, utility types
- [references/patterns.md](references/patterns.md) — Result type, dependency injection, Zod validation, module structure
- [references/jsdoc.md](references/jsdoc.md) — JSDoc rules, tags reference, examples
- [references/formatting.md](references/formatting.md) — Prettier config, import discipline, module organization

External docs:
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [tsconfig reference](https://www.typescriptlang.org/tsconfig)
