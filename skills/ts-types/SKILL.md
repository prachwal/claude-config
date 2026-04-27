---
name: ts-types
description: Use when writing TypeScript types, generics, utility types, narrowing, discriminated unions, or fixing TS type errors. Covers type-level patterns for both frontend and backend code.
---

# SKILL: TypeScript Patterns

Reference for writing correct TypeScript in this project.
Read this when: writing new types, fixing TS errors, unsure about generics.

---

## Type vs Interface — when to use each

```ts
// Use interface for objects that will be extended or implemented
interface User {
  id: string
  email: string
  name: string
}

interface AdminUser extends User {
  role: 'admin'
  permissions: string[]
}

// Use type for unions, intersections, primitives, tuples
type Status = 'idle' | 'loading' | 'success' | 'error'
type Nullable<T> = T | null
type UserOrAdmin = User | AdminUser
```

→ Patterns and common error fixes: [references/patterns.md](references/patterns.md)

---

## Strict Mode Checklist

With `strict: true` in tsconfig, all these are errors — fix them, don't disable strict:

- [ ] Every function parameter has a type
- [ ] Every function has a return type (or TS can infer it clearly)
- [ ] No `any` — use `unknown` + narrowing
- [ ] No non-null assertions (`!`) without a comment explaining why it's safe
- [ ] No unused variables or parameters (prefix with `_` if intentionally unused)
