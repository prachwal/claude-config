---
name: tailwind
description: Use when styling with Tailwind CSS v4, including CSS-first @theme configuration, design tokens, dark mode, responsive variants, and component variant patterns with cva.
---

# SKILL: Tailwind CSS v4 Patterns

Reference for working with Tailwind CSS v4 correctly.
Read this when: styling components, theming, dark mode, custom tokens.

---

## v4 Key Changes vs v3

```
v3 → v4 migration notes:
- No more tailwind.config.js by default — config lives in CSS via @theme
- PostCSS plugin: @tailwindcss/postcss (not tailwindcss directly)
- Vite plugin: @tailwindcss/vite (preferred over PostCSS for Vite projects)
- JIT is always on, no purge config needed
- New: CSS-first configuration, native cascade layers
- Deprecated: @apply with multi-word variants (use CSS variables instead)
```

---

## Project Setup (Vite + React)

```bash
npm install tailwindcss @tailwindcss/vite
```

```ts
// vite.config.ts
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [tailwindcss()],
})
```

```css
/* src/index.css — single import, no directives needed */
@import "tailwindcss";

/* Custom design tokens live here */
@theme {
  --color-brand: oklch(55% 0.22 260);
  --color-brand-hover: oklch(48% 0.22 260);
  --font-sans: "Inter", sans-serif;
  --radius-card: 0.75rem;
  --spacing-section: 5rem;
}
```

---

## Design Token Usage

```tsx
// Use CSS variables from @theme directly in JSX
<div className="bg-[--color-brand] text-white rounded-[--radius-card]" />

// Or via generated utility classes (Tailwind auto-generates these from @theme)
<div className="bg-brand text-white" />
```

---

## Dark Mode

```css
/* In index.css — use @variant for dark mode */
@import "tailwindcss";

@theme {
  --color-bg: oklch(98% 0 0);
  --color-text: oklch(15% 0 0);
}

@variant dark {
  --color-bg: oklch(12% 0 0);
  --color-text: oklch(92% 0 0);
}
```

```tsx
// In components — one class, automatically responds to dark mode
<div className="bg-[--color-bg] text-[--color-text]" />
```

```html
<!-- Toggle dark mode by setting class on <html> -->
<html class="dark">
```

---

## Responsive Breakpoints

```
Default breakpoints:
  sm   ≥ 640px
  md   ≥ 768px
  lg   ≥ 1024px
  xl   ≥ 1280px
  2xl  ≥ 1536px

Custom breakpoints in @theme:
  --breakpoint-tablet: 900px;   → use as: tablet:flex
```

```tsx
// Mobile-first approach — always start with base (mobile), then add breakpoints
<div className="flex flex-col sm:flex-row gap-4 md:gap-8" />
```

---

→ Component variants (cva) and layout patterns: [references/component-patterns.md](references/component-patterns.md)

---

## What NOT to do

```tsx
// ❌ Don't use @apply for complex component styles — use cva instead
// ❌ Don't hardcode pixel values — use @theme tokens
// ❌ Don't forget focus-visible styles on interactive elements
// ❌ Don't use hover: without also considering focus-visible:
// ❌ Don't mix Tailwind v3 config patterns (tailwind.config.js) with v4
```
