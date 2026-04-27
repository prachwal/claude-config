---
name: vitest
description: Use when writing unit or integration tests with Vitest, including React Testing Library, mocking modules and APIs, testing hooks, and configuring coverage.
---

# SKILL: Vitest Patterns

Read this when: writing tests, debugging test failures, setting up coverage.

---

## Running Tests

```bash
npx vitest                      # watch mode (dev)
npx vitest run                  # run once (CI)
npx vitest run src/foo.test.ts  # run single file
npx vitest --ui                 # browser UI
npx vitest run --coverage       # with coverage report
```

---

## File Naming

```
src/
  components/
    Button.tsx
    Button.test.tsx     # co-located, same folder
  services/
    auth.service.ts
    auth.service.test.ts
```

---

## Test Structure

```ts
import { describe, it, expect, vi, beforeEach } from 'vitest'

describe('MyThing', () => {
  beforeEach(() => { vi.clearAllMocks() })

  it('does Y when condition X', () => {
    // Arrange — Act — Assert
    const result = myFunction('input')
    expect(result).toBe('expected')
  })

  it('throws when input is null', () => {
    expect(() => myFunction(null as unknown)).toThrow('Expected string')
  })
})
```

---

## Key Matchers (quick reference)

```ts
expect(v).toBe(x)              // strict ===
expect(v).toEqual({ a: 1 })   // deep equality
expect(v).toMatchObject({ a }) // partial match
expect(arr).toHaveLength(3)
expect(fn).toHaveBeenCalledWith('arg')
await expect(p).resolves.toBe('v')
await expect(p).rejects.toThrow()
```

→ Full cheatsheet: [references/matchers.md](references/matchers.md)

---

## Debugging

```bash
npx vitest run --reporter=verbose   # full output
npx vitest run -t "test name"       # run by name
```
```ts
screen.debug()        // print DOM
logRoles(document.body) // list ARIA roles
```

---

## References

- [references/matchers.md](references/matchers.md) — full matchers cheatsheet
- [references/mocking.md](references/mocking.md) — module mocks, global fetch, fake timers
- [references/rtl-patterns.md](references/rtl-patterns.md) — RTL queries, coverage config, debugging
