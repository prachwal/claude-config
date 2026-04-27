# React Hooks and Context Patterns

## Data Fetching Hook (no library)
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

  const load = useCallback(async () => {
    setState(s => ({ ...s, loading: true, error: null }))
    try {
      const res = await fetch(`/api/users/${userId}`)
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data: User = await res.json()
      setState({ data, loading: false, error: null })
    } catch (e) {
      setState({ data: null, loading: false, error: String(e) })
    }
  }, [userId])

  useEffect(() => { load() }, [load])

  return { ...state, refetch: load }
}

// Usage
function UserProfile({ userId }: { userId: string }) {
  const { data: user, loading, error } = useUser(userId)
  if (loading) return <Spinner />
  if (error) return <ErrorMessage message={error} />
  if (!user) return null
  return <div>{user.name}</div>
}
```

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

// Export typed hook — never export the context itself
export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider')
  return ctx
}
```

## Performance Memos
```ts
// useMemo: expensive computation, recalculate when deps change
const sorted = useMemo(
  () => [...items].sort((a, b) => a.name.localeCompare(b.name)),
  [items]
)

// useCallback: stable function reference for child props / useEffect deps
const handleDelete = useCallback(
  (id: string) => setItems(prev => prev.filter(i => i.id !== id)),
  []
)

// Rule: profile first, optimize second — useMemo/useCallback are not free
```
