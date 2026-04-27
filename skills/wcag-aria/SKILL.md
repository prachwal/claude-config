---
name: wcag-aria
description: Use when implementing ARIA patterns in React/TSX code: roles, labels, keyboard navigation, focus management, accessible forms with error announcements, interactive widgets (modal, accordion, tabs), color contrast, and prefers-reduced-motion. Contains ready-to-use code examples. For project-level accessibility workflow and principles, use web-accessibility-standards.
---

# SKILL: WCAG / ARIA Accessibility Patterns

Reference for building accessible web applications.
Read this when: building interactive UI, forms, navigation, modals, or any custom components.

---

## Core Principles (WCAG 2.2 / ARIA 1.2)

```
POUR principles — every component must be:
  Perceivable   — info must be presentable to all senses (not just sight)
  Operable      — UI must be usable via keyboard, no timing traps
  Understandable — UI and content must be clear and predictable
  Robust        — must work with current and future assistive tech
```

---

## Keyboard Navigation Rules

```tsx
// ✅ All interactive elements reachable via Tab
// ✅ Focus order follows visual order (check DOM order, not CSS order)
// ✅ Focus never trapped (unless intentional: modal, dialog)
// ✅ Escape always closes overlays

// ✅ Skip link — first focusable element on every page
<a href="#main-content" className="sr-only focus:not-sr-only focus:fixed focus:top-2 focus:left-2 z-50 bg-white px-4 py-2 rounded">
  Skip to main content
</a>
<main id="main-content" tabIndex={-1}>...</main>
```

---

## Focus Management

```tsx
// ✅ Move focus to modal when it opens
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

---

## ARIA Roles and Labels

```tsx
// ✅ Landmark roles — one of each per page (except <section>)
<header role="banner" />
<nav aria-label="Main navigation" />         // label required if >1 nav
<main role="main" />
<aside aria-label="Related links" />
<footer role="contentinfo" />

// ✅ aria-label vs aria-labelledby vs aria-describedby
// aria-label       — short, direct label (no visible label)
// aria-labelledby  — points to ID of visible heading
// aria-describedby — points to ID of longer description text

// ✅ Icon buttons must have a text label
<button aria-label="Close dialog">
  <XIcon aria-hidden="true" />
</button>

// ✅ Images
<img src="…" alt="Graph showing revenue growth from €10k to €45k in Q1" />
<img src="decorative-divider.svg" alt="" role="presentation" />  // decorative

// ✅ Live regions for dynamic content
<div aria-live="polite" aria-atomic="true">
  {statusMessage}  {/* screen readers announce changes */}
</div>
<div aria-live="assertive">  {/* urgent: error messages */}
  {errorMessage}
</div>
```

---

## Forms — Accessible Pattern

```tsx
function AccessibleForm() {
  return (
    <form noValidate>
      {/* ✅ Every input has an associated <label> */}
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
          <span id="email-error" role="alert">
            {error}
          </span>
        )}
      </div>

      {/* ✅ Fieldset + legend for grouped inputs */}
      <fieldset>
        <legend>Notification preferences</legend>
        <label><input type="checkbox" /> Email</label>
        <label><input type="checkbox" /> SMS</label>
      </fieldset>

      {/* ✅ Submit state communicated */}
      <button type="submit" aria-busy={submitting} disabled={submitting}>
        {submitting ? 'Saving…' : 'Save'}
      </button>
    </form>
  )
}
```

---

## Color and Contrast

```
Minimum contrast ratios (WCAG 2.2 AA):
  Normal text (< 18pt / < 14pt bold):  4.5 : 1
  Large text  (≥ 18pt / ≥ 14pt bold):  3 : 1
  UI components and focus indicators:  3 : 1

Tools:
  https://webaim.org/resources/contrastchecker/
  VS Code extension: axe Accessibility Linter
  Browser: Chrome DevTools → Accessibility → Color contrast

Rules:
  ✅ Never communicate information with color alone — add text or icon
  ✅ Links must be distinguishable from body text (underline or 3:1 contrast)
  ✅ Focus indicators must meet 3:1 contrast against adjacent colors
```

---

## Headings and Document Structure

```tsx
// ✅ One <h1> per page, do not skip levels
<h1>Page title</h1>
  <h2>Section</h2>
    <h3>Subsection</h3>

// ❌ Never use headings for visual styling — use CSS
// ❌ Never skip from h1 to h3
// ❌ Never use <b> or <i> for semantics — use <strong>, <em>

// ✅ Visually hidden but accessible text
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

---

## Interactive Component Patterns

```tsx
// ✅ Accordion
<div>
  <button
    aria-expanded={isOpen}
    aria-controls="panel-1"
    id="header-1"
  >
    FAQ Question
  </button>
  <div
    id="panel-1"
    role="region"
    aria-labelledby="header-1"
    hidden={!isOpen}
  >
    Answer content
  </div>
</div>

// ✅ Tabs
<div role="tablist" aria-label="Settings sections">
  <button role="tab" aria-selected={active === 0} aria-controls="panel-0" id="tab-0">General</button>
  <button role="tab" aria-selected={active === 1} aria-controls="panel-1" id="tab-1">Security</button>
</div>
<div role="tabpanel" id="panel-0" aria-labelledby="tab-0" hidden={active !== 0}>…</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1" hidden={active !== 1}>…</div>
```

---

## Testing Checklist

```
Automated (catch ~30% of issues):
  □ axe-core / @axe-core/react in tests
  □ eslint-plugin-jsx-a11y in ESLint config

Manual:
  □ Tab through entire page — focus visible at all times?
  □ Screen reader test: VoiceOver (macOS), NVDA (Windows), Orca (Linux)
  □ Zoom to 200% — no horizontal scroll, no text cut off
  □ Color blindness check: browser DevTools → Rendering → Emulate vision deficiency
  □ Motion sensitivity: prefers-reduced-motion honored?
```

```css
/* ✅ Always respect prefers-reduced-motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```
