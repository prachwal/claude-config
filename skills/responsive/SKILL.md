---
name: responsive
description: Use when implementing mobile-first layouts, fluid typography, responsive images, touch targets, navigation menus, or testing across breakpoints.
---

# SKILL: Responsive Web Design Patterns

Read this when: implementing layouts, handling images/media, building navigation, or targeting multiple screen sizes.

---

## Mobile-First Principle

```
Always design and code for small screens first.
Add breakpoint classes to handle larger screens — not the other way around.

Why:
  - Forces content prioritization
  - Smaller CSS shipped to mobile devices
  - Easier to add complexity than remove it
```

```tsx
// ✅ Mobile-first — base style is mobile, md: adds desktop
<div className="flex flex-col gap-4 md:flex-row md:gap-8" />

// ❌ Desktop-first anti-pattern
<div className="flex flex-row gap-8 md:flex-col md:gap-4" />
```

---

## Layout Patterns

```tsx
// ✅ Page container
<div className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">

// ✅ Sidebar layout — stacks on mobile, side-by-side on desktop
<div className="flex flex-col lg:flex-row gap-8">
  <aside className="w-full lg:w-64 shrink-0">Sidebar</aside>
  <main className="min-w-0 flex-1">Content</main>
</div>

// ✅ Auto-fit card grid
<div className="grid grid-cols-[repeat(auto-fit,minmax(280px,1fr))] gap-6" />

// ✅ Holy grail layout (full page with sticky footer)
<div className="grid min-h-screen grid-rows-[auto_1fr_auto]">
  <header /><main /><footer />
</div>
```

---

## Touch and Interaction

```css
/* ✅ Touch target size — minimum 44×44px (WCAG 2.5.5) */
button, a, [role="button"] {
  min-height: 44px;
  min-width: 44px;
}

/* ✅ Remove 300ms tap delay */
html { touch-action: manipulation; }

/* ✅ Smooth scrolling — respect reduced motion */
@media (prefers-reduced-motion: no-preference) {
  html { scroll-behavior: smooth; }
}
```

---

## Viewport and Meta

```html
<!-- Required in <head> — prevents mobile zoom issues -->
<meta name="viewport" content="width=device-width, initial-scale=1" />
```
```css
/* Prevent horizontal overflow */
html, body { overflow-x: hidden; }
*, *::before, *::after { box-sizing: border-box; }
```

---

## References

- [references/responsive-patterns.md](references/responsive-patterns.md) — fluid typography, images/media, hamburger navigation, testing checklist
