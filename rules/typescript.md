---
applyTo: "**/*.ts,**/*.tsx"
---

# TypeScript Rules

## Before writing types or fixing TS errors

Load the relevant skill:
- Type patterns, generics, utility types → `.claude/skills/ts-types/SKILL.md`
- Project structure, naming, tsconfig → `.claude/skills/ts-fundamentals/SKILL.md`

## Conventions

- Strict mode required: `"strict": true` in tsconfig
- `interface` for object shapes; `type` for unions, intersections, mapped types
- No `any` — use `unknown` + narrowing for truly unknown data
- No non-null assertions (`!`) on user input or API responses
- Exports: named exports only (no default exports except pages/routes)
- Prefer `satisfies` over explicit type annotation when possible
- Enums: use `const` enums or plain string unions — avoid regular enums
- After editing shared types, run `npx tsc --noEmit` before marking done
