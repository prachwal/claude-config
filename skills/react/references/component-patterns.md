# React Component Patterns

## Forms (controlled, no library)
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

## Error Boundaries
```tsx
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
