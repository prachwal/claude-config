---
name: web-accessibility-standards
description: Use when approaching accessibility at the project or workflow level: semantic HTML strategy, WCAG 2.2 criteria mapping, axe-core CI integration, and implementation checklist. For concrete ARIA code examples in React/TSX, use wcag-aria. For audits and QA passes, use a11y-review.
---

# SKILL: Web Accessibility Standards

## Rules (always apply)
- Semantic HTML first — `<button>`, `<input>`, `<label>`, `<nav>`, `<main>` before any ARIA
- All images need `alt` (empty `alt=""` for decorative)
- Every `<input>` must have associated `<label>` via `for`/`id`
- Never `outline:none` without a visible `:focus-visible` replacement
- `lang` on `<html>`, descriptive `<title>`, one `<h1>` per page
- Touch targets ≥ 24×24 CSS px; no hover-only or pointer-only interactions
- Respect `prefers-reduced-motion` — wrap animations in `@media (prefers-reduced-motion: no-preference)`
- Contrast: 4.5:1 normal text, 3:1 large text / UI components
- No `tabindex > 0`; no `user-scalable=no` in viewport meta
- Modals: trap focus inside, return focus to trigger on close

## React patterns
```tsx
// Programmatic focus
const ref = useRef<HTMLHeadingElement>(null)
useEffect(() => { ref.current?.focus() }, [routeChanged])

// Live region (declare at root, not inside unmounting components)
<div aria-live="polite" aria-atomic="true">{statusMessage}</div>

// Dialog focus trap
<dialog aria-labelledby="title-id" ref={dialogRef}>
  <h2 id="title-id">Title</h2>
  ...
</dialog>
```

## New project checklist
- `<html lang="en">`, `<meta viewport>` without `user-scalable=no`
- Skip-nav link: `<a href="#main" class="skip-link">Skip to main</a>`
- Landmarks: `<header>`, `<nav>`, `<main>`, `<footer>`
- axe-core in tests: `npm i -D @axe-core/react` or `jest-axe`

## Anti-patterns
| Wrong | Fix |
|---|---|
| `<div onClick>` | `<button>` |
| `placeholder` as label | real `<label>` |
| `display:none` for focus hiding | `tabindex="-1"` + `aria-hidden="true"` |
| Inject `aria-live` on demand | declare in root from load |
