---
name: wcag-aria
description: Use when implementing ARIA patterns in React/TSX code: roles, labels, keyboard navigation, focus management, accessible forms with error announcements, interactive widgets (modal, accordion, tabs), color contrast, and prefers-reduced-motion. Contains ready-to-use code examples. For project-level accessibility workflow and principles, use web-accessibility-standards.
---

# SKILL: WCAG / ARIA Accessibility Patterns

Read this when: building interactive UI, forms, navigation, modals, or any custom components.

---

## Core Principles (WCAG 2.2 / ARIA 1.2)

```
POUR — every component must be:
  Perceivable   — info presentable to all senses (not just sight)
  Operable      — usable via keyboard, no timing traps
  Understandable — UI clear and predictable
  Robust        — works with current and future assistive tech
```

---

## Keyboard Navigation Rules

```tsx
// ✅ All interactive elements reachable via Tab
// ✅ Focus order follows visual DOM order (not CSS order)
// ✅ Focus never trapped unless intentional (modal/dialog)
// ✅ Escape always closes overlays

// ✅ Skip link — first focusable element on every page
<a href="#main-content" className="sr-only focus:not-sr-only focus:fixed focus:top-2 focus:left-2 z-50 bg-white px-4 py-2 rounded">
  Skip to main content
</a>
<main id="main-content" tabIndex={-1}>…</main>
```

---

## ARIA Roles and Labels

```tsx
// ✅ Landmark roles — one of each per page (except <section>)
<header role="banner" />
<nav aria-label="Main navigation" />   // label required if >1 nav
<main role="main" />
<footer role="contentinfo" />

// ✅ aria-label vs aria-labelledby vs aria-describedby
// aria-label       — short, direct label (no visible label)
// aria-labelledby  — points to ID of visible heading
// aria-describedby — points to ID of longer description

// ✅ Icon buttons must have a text label
<button aria-label="Close dialog">
  <XIcon aria-hidden="true" />
</button>

// ✅ Images
<img src="…" alt="Descriptive text" />
<img src="decorative.svg" alt="" role="presentation" />  // decorative
```

---

## Testing Checklist

```
Automated (catch ~30% of issues):
  □ axe-core / @axe-core/react in tests
  □ eslint-plugin-jsx-a11y in ESLint config

Manual:
  □ Tab through entire page — focus visible at all times?
  □ Screen reader: VoiceOver (macOS), NVDA (Windows), Orca (Linux)
  □ Zoom to 200% — no horizontal scroll, no text cut off
  □ Color blindness check: DevTools → Rendering → Emulate vision deficiency
  □ prefers-reduced-motion honored?
```

---

## References

- [references/aria-patterns.md](references/aria-patterns.md) — focus management, accessible forms, live regions, accordion/tabs
- [references/contrast-headings.md](references/contrast-headings.md) — contrast ratios, heading structure, sr-only, reduced-motion
