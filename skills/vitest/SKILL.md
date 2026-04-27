---
name: vitest
description: Use when writing unit or integration tests with Vitest, including React Testing Library, mocking modules and APIs, testing hooks, and configuring coverage.
---

# SKILL: Vitest Patterns

Reference for writing and running tests with Vitest.
Read this when: writing tests, debugging test failures, setting up coverage.

---

## Running Tests

```bash
npx vitest                  # watch mode (dev)
npx vitest run              # run once (CI)
npx vitest run src/foo.test.ts  # run single file
npx vitest --ui             # browser UI
npx vitest run --coverage   # with coverage report
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
  utils/
    format.ts
    format.test.ts
```

---

## Test Structure

```ts
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'

describe('MyThing', () => {
  // Setup shared between tests
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('when condition X', () => {
    it('does Y', () => {
      // Arrange
      const input = 'test'
      // Act
      const result = myFunction(input)
      // Assert
      expect(result).toBe('expected')
    })
  })

  it('throws when input is null', () => {
    expect(() => myFunction(null as any)).toThrow('Expected string')
  })
})
```

---

## Matchers Cheatsheet

```ts
// Equality
expect(value).toBe(42)              // strict ===
expect(value).toEqual({ a: 1 })    // deep equality
expect(value).toStrictEqual(obj)   // deep + same type

// Truthiness
expect(value).toBeTruthy()
expect(value).toBeFalsy()
expect(value).toBeNull()
expect(value).toBeUndefined()
expect(value).toBeDefined()

// Numbers
expect(n).toBeGreaterThan(0)
expect(n).toBeCloseTo(3.14, 2)     // float precision

// Strings
expect(str).toContain('hello')
expect(str).toMatch(/pattern/)

// Arrays
expect(arr).toHaveLength(3)
expect(arr).toContain('item')
expect(arr).toEqual(expect.arrayContaining(['a', 'b']))

// Objects
expect(obj).toHaveProperty('key', 'value')
expect(obj).toMatchObject({ a: 1 }) // partial match

// Functions / errors
expect(() => fn()).toThrow()
expect(() => fn()).toThrow('message')
expect(() => fn()).toThrow(ErrorClass)

// Promises
await expect(promise).resolves.toBe('value')
await expect(promise).rejects.toThrow('error')

// Mocks
expect(mockFn).toHaveBeenCalled()
expect(mockFn).toHaveBeenCalledOnce()
expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2')
expect(mockFn).toHaveBeenCalledTimes(3)
expect(mockFn).toHaveReturnedWith('value')
```

---

## Mocking Patterns

### Mock a module
```ts
vi.mock('../api/users', () => ({
  fetchUser: vi.fn(),
  createUser: vi.fn(),
}))

import { fetchUser } from '../api/users'

it('loads user on mount', async () => {
  vi.mocked(fetchUser).mockResolvedValue({ id: '1', name: 'Alice' })
  // ... render and assert
})
```

### Mock only some exports
```ts
vi.mock('../utils', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../utils')>()
  return {
    ...actual,          // keep real implementations
    formatDate: vi.fn() // override only this one
  }
})
```

### Mock global fetch
```ts
beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn())
})

afterEach(() => {
  vi.unstubAllGlobals()
})

it('fetches data', async () => {
  vi.mocked(fetch).mockResolvedValue(
    new Response(JSON.stringify({ users: [] }), { status: 200 })
  )
  // ...
})
```

### Fake timers
```ts
beforeEach(() => { vi.useFakeTimers() })
afterEach(() => { vi.useRealTimers() })

it('debounces input', async () => {
  render(<SearchBox />)
  await userEvent.type(screen.getByRole('textbox'), 'hello')
  vi.advanceTimersByTime(300)
  expect(mockSearch).toHaveBeenCalledWith('hello')
})
```

---

## React Testing Library Patterns

```tsx
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

// Always use userEvent over fireEvent
const user = userEvent.setup()

// Render with providers (create a helper)
function renderWithProviders(ui: ReactElement) {
  return render(
    <QueryClientProvider client={new QueryClient()}>
      <AuthProvider>
        {ui}
      </AuthProvider>
    </QueryClientProvider>
  )
}

// Common queries
screen.getByRole('button', { name: /submit/i })
screen.getByRole('textbox', { name: /email/i })
screen.getByRole('heading', { level: 1 })
screen.getByLabelText('Password')
screen.queryByText('Error') // returns null if not found (don't throw)
await screen.findByText('Loaded') // waits for async

// User interactions
await user.click(screen.getByRole('button'))
await user.type(screen.getByRole('textbox'), 'hello')
await user.clear(screen.getByRole('textbox'))
await user.selectOptions(screen.getByRole('combobox'), 'option1')
await user.keyboard('{Enter}')
```

---

## Coverage Configuration (vite.config.ts)

```ts
test: {
  coverage: {
    provider: 'v8',
    reporter: ['text', 'html'],
    thresholds: {
      lines: 80,
      functions: 80,
      branches: 70,
    },
    exclude: [
      'node_modules/',
      'src/test/',
      'src/main.tsx',      // entry point
      '**/*.d.ts',
      '**/*.config.*',
    ],
  },
}
```

---

## Debugging Failing Tests

```bash
# See full output without truncation
npx vitest run --reporter=verbose

# Run with console output visible
npx vitest run --silent=false

# Run specific test by name
npx vitest run -t "should render login form"

# Debug what's in the DOM
screen.debug()                    # prints full DOM
screen.debug(screen.getByRole('button')) # prints specific element

# Check what roles exist
import { logRoles } from '@testing-library/dom'
logRoles(document.body)
```
