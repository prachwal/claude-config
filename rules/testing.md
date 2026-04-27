---
applyTo: "**/*.test.ts,**/*.test.tsx,**/*.spec.ts,**/*.spec.tsx,tests/**,e2e/**,test/**"
---

# Testing Rules

## Before writing tests

Load the relevant skill:
- Unit / integration tests → `.claude/skills/vitest/SKILL.md`
- E2E / Playwright → `.claude/skills/web-testing/SKILL.md`

## Conventions

- Test file lives next to the source file: `foo.ts` → `foo.test.ts`
- E2E tests go in `e2e/` or `tests/` at project root
- Test names: `describe('ComponentName')` + `it('does X when Y')`
- Never test implementation details — test behavior from the user's perspective
- Prefer `userEvent` over `fireEvent` in RTL tests
- Mock at module boundary, not inside functions
- One `expect` per logical assertion — split large tests into focused cases
- No `any` in test files — type your mocks
