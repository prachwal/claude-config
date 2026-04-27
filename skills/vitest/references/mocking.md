# Vitest Mocking Patterns

## Mock a module
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

## Mock only some exports
```ts
vi.mock('../utils', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../utils')>()
  return {
    ...actual,          // keep real implementations
    formatDate: vi.fn() // override only this one
  }
})
```

## Mock global fetch
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

## Fake timers
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
