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

## Component Variants Pattern

```tsx
// Use cva (class-variance-authority) for variant-based components
import { cva, type VariantProps } from 'class-variance-authority'
import { twMerge } from 'tailwind-merge'

const button = cva(
  // base classes
  'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        primary: 'bg-brand text-white hover:bg-brand-hover',
        ghost:   'hover:bg-muted hover:text-muted-foreground',
        danger:  'bg-red-600 text-white hover:bg-red-700',
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4',
        lg: 'h-12 px-6 text-lg',
      },
    },
    defaultVariants: { variant: 'primary', size: 'md' },
  }
)

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>,
  VariantProps<typeof button> {}

export function Button({ variant, size, className, ...props }: ButtonProps) {
  return <button className={twMerge(button({ variant, size }), className)} {...props} />
}
```

---

## Common Patterns

```tsx
// ✅ Card
<div className="rounded-[--radius-card] border border-border bg-card p-6 shadow-sm" />

// ✅ Centered container
<div className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8" />

// ✅ Flex row with gap, wraps on mobile
<div className="flex flex-wrap gap-3" />

// ✅ CSS Grid — auto-fit responsive columns
<div className="grid grid-cols-[repeat(auto-fit,minmax(280px,1fr))] gap-6" />

// ✅ Truncate text safely
<p className="truncate" />                    // single line
<p className="line-clamp-3" />               // max 3 lines

// ✅ Focus ring (keyboard-accessible)
<button className="focus-visible:ring-2 focus-visible:ring-brand focus-visible:ring-offset-2 focus-visible:outline-none" />
```

---

## What NOT to do

```tsx
// ❌ Don't use @apply for complex component styles — use cva instead
// ❌ Don't hardcode pixel values — use @theme tokens
// ❌ Don't forget focus-visible styles on interactive elements
// ❌ Don't use hover: without also considering focus-visible:
// ❌ Don't mix Tailwind v3 config patterns (tailwind.config.js) with v4
```
