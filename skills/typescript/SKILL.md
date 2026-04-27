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

---

## Common Patterns

### API Response wrapper
```ts
type ApiResult<T> =
  | { ok: true; data: T }
  | { ok: false; error: string }

async function fetchUser(id: string): Promise<ApiResult<User>> {
  try {
    const res = await fetch(`/api/users/${id}`)
    if (!res.ok) return { ok: false, error: `HTTP ${res.status}` }
    const data = await res.json() as User
    return { ok: true, data }
  } catch (e) {
    return { ok: false, error: String(e) }
  }
}

// Usage — always handle both cases
const result = await fetchUser('123')
if (result.ok) {
  console.log(result.data.name) // typed correctly
} else {
  console.error(result.error)
}
```

### Generic fetch hook
```ts
function useAsync<T>(fn: () => Promise<T>) {
  const [state, setState] = useState<{
    status: 'idle' | 'loading' | 'success' | 'error'
    data: T | null
    error: string | null
  }>({ status: 'idle', data: null, error: null })

  const run = useCallback(async () => {
    setState({ status: 'loading', data: null, error: null })
    try {
      const data = await fn()
      setState({ status: 'success', data, error: null })
    } catch (e) {
      setState({ status: 'error', data: null, error: String(e) })
    }
  }, [fn])

  return { ...state, run }
}
```

### Type narrowing
```ts
// Don't do this:
function process(value: unknown) {
  return (value as string).toUpperCase() // unsafe cast
}

// Do this:
function process(value: unknown) {
  if (typeof value !== 'string') throw new Error('Expected string')
  return value.toUpperCase() // safe — TS knows it's string here
}

// Type guard
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'email' in value
  )
}
```

### Discriminated unions
```ts
type Action =
  | { type: 'increment'; by: number }
  | { type: 'reset' }
  | { type: 'setName'; name: string }

function reduce(state: State, action: Action): State {
  switch (action.type) {
    case 'increment': return { ...state, count: state.count + action.by }
    case 'reset': return initialState
    case 'setName': return { ...state, name: action.name }
    // TS will error if a case is missing — good!
  }
}
```

### Component prop patterns
```ts
// Children
interface CardProps {
  children: React.ReactNode // use ReactNode, not JSX.Element
  className?: string
}

// Event handlers
interface ButtonProps {
  onClick: (event: React.MouseEvent<HTMLButtonElement>) => void
  onChange?: (value: string) => void
}

// Polymorphic (rare — avoid unless needed)
interface BoxProps<T extends React.ElementType = 'div'> {
  as?: T
  children: React.ReactNode
}
```

---

## Fixing Common TS Errors

### "Object is possibly 'undefined'"
```ts
// Bad: user.address.city
// Good:
const city = user.address?.city ?? 'Unknown'
```

### "Type 'string' is not assignable to type 'Status'"
```ts
// Bad: const s = 'loading' as string
// Good:
const s = 'loading' as const satisfies Status
// or just:
const s: Status = 'loading'
```

### "Argument of type 'X | null' is not assignable"
```ts
// Either guard:
if (value === null) return
doSomething(value) // safe here

// Or assert (only when you're 100% sure):
doSomething(value!)
```

### "Property 'x' does not exist on type 'never'"
You have an exhaustive check that's not actually exhaustive.
Add the missing case or add:
```ts
function assertNever(value: never): never {
  throw new Error(`Unhandled case: ${JSON.stringify(value)}`)
}
```

---

## Strict Mode Checklist

With `strict: true` in tsconfig, all these are errors — fix them, don't disable strict:

- [ ] Every function parameter has a type
- [ ] Every function has a return type (or TS can infer it clearly)
- [ ] No `any` — use `unknown` + narrowing
- [ ] No non-null assertions (`!`) without a comment explaining why it's safe
- [ ] No unused variables or parameters (prefix with `_` if intentionally unused)
