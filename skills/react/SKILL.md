---
name: react
description: Use when building React components, managing state, writing hooks, handling async data fetching, context, or forms. Covers TSX patterns, error boundaries, and performance.
---

# SKILL: React Patterns

Reference for writing React components correctly.
Read this when: creating components, managing state, handling async data.

---

## State Management Decision Tree

```
Does state need to be shared across routes? → Zustand / Context
Does state need to survive page refresh? → localStorage + useState
Is it server data (fetch from API)? → custom hook or React Query
Is it UI-only (open/closed, active tab)? → useState
Is it derived from other state? → useMemo, NOT useState
```

---

## Data Fetching Pattern (no library)

```tsx
// hooks/useUser.ts
import { useState, useEffect, useCallback } from 'react'

interface FetchState<T> {
  data: T | null
  loading: boolean
  error: string | null
}

export function useUser(userId: string) {
  const [state, setState] = useState<FetchState<User>>({
    data: null,
    loading: true,
    error: null,
  })

  const fetch = useCallback(async () => {
    setState(s => ({ ...s, loading: true, error: null }))
    try {
      const res = await fetch(`/api/users/${userId}`)
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      setState({ data, loading: false, error: null })
    } catch (e) {
      setState({ data: null, loading: false, error: String(e) })
    }
  }, [userId])

  useEffect(() => { fetch() }, [fetch])

  return { ...state, refetch: fetch }
}

// Component usage
function UserProfile({ userId }: { userId: string }) {
  const { data: user, loading, error } = useUser(userId)

  if (loading) return <Spinner />
  if (error) return <ErrorMessage message={error} />
  if (!user) return null

  return <div>{user.name}</div>
}
```

---

## Forms Pattern (no library)

```tsx
function LoginForm({ onSuccess }: { onSuccess: (token: string) => void }) {
  const [values, setValues] = useState({ email: '', password: '' })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [submitting, setSubmitting] = useState(false)

  function validate(): boolean {
    const next: Record<string, string> = {}
    if (!values.email.includes('@')) next.email = 'Invalid email'
    if (values.password.length < 8) next.password = 'Min 8 characters'
    setErrors(next)
    return Object.keys(next).length === 0
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!validate()) return
    setSubmitting(true)
    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values),
      })
      if (!res.ok) throw new Error('Login failed')
      const { token } = await res.json()
      onSuccess(token)
    } catch (e) {
      setErrors({ form: String(e) })
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={values.email}
          onChange={e => setValues(v => ({ ...v, email: e.target.value }))}
        />
        {errors.email && <span role="alert">{errors.email}</span>}
      </div>
      {errors.form && <p role="alert">{errors.form}</p>}
      <button type="submit" disabled={submitting}>
        {submitting ? 'Logging in...' : 'Log in'}
      </button>
    </form>
  )
}
```

---

## Context Pattern (shared state)

```tsx
// contexts/AuthContext.tsx
import { createContext, useContext, useState, ReactNode } from 'react'

interface AuthContextValue {
  user: User | null
  login: (token: string) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)

  function login(token: string) {
    // decode token, set user
    localStorage.setItem('token', token)
    setUser(decodeToken(token))
  }

  function logout() {
    localStorage.removeItem('token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

// Always export a typed hook, never export the context itself
export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider')
  return ctx
}
```

---

## List Rendering Rules

```tsx
// ✅ Use stable, unique ID as key
{items.map(item => (
  <Item key={item.id} data={item} />
))}

// ❌ Never use index as key when list can reorder/filter
{items.map((item, i) => (
  <Item key={i} data={item} /> // BAD — causes bugs with animations, focus
))}

// ✅ Handle empty state explicitly
{items.length === 0 ? (
  <p>No items found</p>
) : (
  items.map(item => <Item key={item.id} data={item} />)
)}
```

---

## Performance — when to use what

```ts
// useMemo: expensive computation, recalculate when deps change
const sorted = useMemo(
  () => [...items].sort((a, b) => a.name.localeCompare(b.name)),
  [items]
)

// useCallback: stable function reference for child props or useEffect deps
const handleDelete = useCallback(
  (id: string) => setItems(prev => prev.filter(i => i.id !== id)),
  [] // no deps — setItems is stable
)

// DON'T: wrap everything in useMemo/useCallback — it's not free
// DO: profile first, optimize second
```

---

## Error Boundaries

```tsx
// Create once, use everywhere around risky subtrees
import { Component, ReactNode } from 'react'

interface Props { children: ReactNode; fallback?: ReactNode }
interface State { hasError: boolean }

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false }

  static getDerivedStateFromError(): State {
    return { hasError: true }
  }

  componentDidCatch(error: Error) {
    console.error('ErrorBoundary caught:', error)
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? <p>Something went wrong.</p>
    }
    return this.props.children
  }
}

// Usage
<ErrorBoundary fallback={<p>Failed to load dashboard</p>}>
  <Dashboard />
</ErrorBoundary>
```
