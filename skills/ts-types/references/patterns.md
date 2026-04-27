# TypeScript Patterns: API Result, Generics, Narrowing, Discriminated Unions

## API Response Wrapper
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

// Always handle both cases
const result = await fetchUser('123')
if (result.ok) {
  console.log(result.data.name)
} else {
  console.error(result.error)
}
```

## Generic Async Hook
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

## Type Narrowing
```ts
// ❌ Unsafe cast
function process(value: unknown) {
  return (value as string).toUpperCase()
}

// ✅ Guard first, then use
function process(value: unknown) {
  if (typeof value !== 'string') throw new Error('Expected string')
  return value.toUpperCase()
}

// Type guard function
function isUser(value: unknown): value is User {
  return typeof value === 'object' && value !== null && 'id' in value && 'email' in value
}
```

## Discriminated Unions
```ts
type Action =
  | { type: 'increment'; by: number }
  | { type: 'reset' }
  | { type: 'setName'; name: string }

function reduce(state: State, action: Action): State {
  switch (action.type) {
    case 'increment': return { ...state, count: state.count + action.by }
    case 'reset':     return initialState
    case 'setName':   return { ...state, name: action.name }
    // TS errors if a case is missing
  }
}
```

## Component Prop Patterns
```ts
interface CardProps {
  children: React.ReactNode  // use ReactNode, not JSX.Element
  className?: string
}

interface ButtonProps {
  onClick: (event: React.MouseEvent<HTMLButtonElement>) => void
  onChange?: (value: string) => void
}
```

## Common TS Errors

### "Object is possibly 'undefined'"
```ts
const city = user.address?.city ?? 'Unknown'
```

### "Type 'string' is not assignable to type 'Status'"
```ts
const s: Status = 'loading'
// or:
const s = 'loading' as const satisfies Status
```

### "Argument of type 'X | null' is not assignable"
```ts
if (value === null) return
doSomething(value) // safe here
```

### "Property 'x' does not exist on type 'never'"
Exhaustive check is incomplete. Add the missing case, or:
```ts
function assertNever(value: never): never {
  throw new Error(`Unhandled case: ${JSON.stringify(value)}`)
}
```
