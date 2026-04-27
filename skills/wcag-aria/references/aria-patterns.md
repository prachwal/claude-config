# ARIA Patterns: Focus Management, Forms, Live Regions

## Focus Management
```tsx
// Move focus to modal heading when it opens
import { useEffect, useRef } from 'react'

function Modal({ isOpen, onClose, children }: ModalProps) {
  const headingRef = useRef<HTMLHeadingElement>(null)

  useEffect(() => {
    if (isOpen) headingRef.current?.focus()
  }, [isOpen])

  if (!isOpen) return null

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      onKeyDown={e => e.key === 'Escape' && onClose()}
    >
      <h2 id="modal-title" ref={headingRef} tabIndex={-1}>{title}</h2>
      {children}
      <button onClick={onClose}>Close</button>
    </div>
  )
}
```

## Accessible Form Pattern
```tsx
function AccessibleForm() {
  return (
    <form noValidate>
      <div>
        <label htmlFor="email">Email address</label>
        <input
          id="email"
          type="email"
          autoComplete="email"
          aria-required="true"
          aria-describedby="email-hint email-error"
        />
        <span id="email-hint">We'll never share your email.</span>
        {error && (
          <span id="email-error" role="alert">{error}</span>
        )}
      </div>

      <fieldset>
        <legend>Notification preferences</legend>
        <label><input type="checkbox" /> Email</label>
        <label><input type="checkbox" /> SMS</label>
      </fieldset>

      <button type="submit" aria-busy={submitting} disabled={submitting}>
        {submitting ? 'Saving…' : 'Save'}
      </button>
    </form>
  )
}
```

## Live Regions
```tsx
// polite: non-urgent status updates
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

// assertive: urgent errors — use sparingly
<div aria-live="assertive">
  {errorMessage}
</div>
```

## Interactive Component Patterns

### Accordion
```tsx
<div>
  <button aria-expanded={isOpen} aria-controls="panel-1" id="header-1">
    FAQ Question
  </button>
  <div id="panel-1" role="region" aria-labelledby="header-1" hidden={!isOpen}>
    Answer content
  </div>
</div>
```

### Tabs
```tsx
<div role="tablist" aria-label="Settings sections">
  <button role="tab" aria-selected={active === 0} aria-controls="panel-0" id="tab-0">General</button>
  <button role="tab" aria-selected={active === 1} aria-controls="panel-1" id="tab-1">Security</button>
</div>
<div role="tabpanel" id="panel-0" aria-labelledby="tab-0" hidden={active !== 0}>…</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1" hidden={active !== 1}>…</div>
```
