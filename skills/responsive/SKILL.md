---
name: responsive
description: Use when implementing mobile-first layouts, fluid typography, responsive images, touch targets, navigation menus, or testing across breakpoints.
---

# SKILL: Responsive Web Design Patterns

Reference for building responsive, mobile-first web applications.
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
// ✅ Page container — full width on mobile, max-width centered on desktop
<div className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">

// ✅ Sidebar layout — stacks on mobile, side-by-side on desktop
<div className="flex flex-col lg:flex-row gap-8">
  <aside className="w-full lg:w-64 shrink-0">Sidebar</aside>
  <main className="min-w-0 flex-1">Content</main>
</div>

// ✅ Auto-fit card grid — columns fill available space
<div className="grid grid-cols-[repeat(auto-fit,minmax(280px,1fr))] gap-6" />

// ✅ Holy grail layout (CSS Grid)
<div className="grid min-h-screen grid-rows-[auto_1fr_auto]">
  <header />
  <main />
  <footer />
</div>
```

---

## Typography Scale

```css
/* ✅ Fluid typography with clamp() — no layout shifts between breakpoints */
@theme {
  --text-hero:    clamp(2rem, 5vw + 1rem, 4.5rem);
  --text-heading: clamp(1.5rem, 3vw + 0.5rem, 2.5rem);
  --text-body:    clamp(1rem, 1vw + 0.75rem, 1.125rem);
  --text-small:   0.875rem;
}

/* ✅ Minimum line length for readability */
p { max-width: 70ch; }   /* ~65-75 chars per line is optimal */
```

```tsx
// ✅ Responsive heading
<h1 className="text-[--text-hero] font-bold leading-tight tracking-tight" />
```

---

## Images and Media

```tsx
// ✅ Responsive image — fills container, maintains aspect ratio
<img
  src="photo.jpg"
  alt="…"
  className="w-full h-auto object-cover"
/>

// ✅ Aspect ratio container (prevents layout shift before load)
<div className="aspect-video w-full overflow-hidden rounded-lg">
  <img src="…" alt="…" className="w-full h-full object-cover" />
</div>

// ✅ Next.js / modern: use <picture> for art direction
<picture>
  <source media="(min-width: 1024px)" srcSet="hero-desktop.webp" />
  <source media="(min-width: 640px)"  srcSet="hero-tablet.webp" />
  <img src="hero-mobile.webp" alt="…" />
</picture>
```

```css
/* ✅ Global image defaults */
img, video {
  max-width: 100%;
  height: auto;
  display: block;
}
```

---

## Touch and Interaction

```css
/* ✅ Touch target size — minimum 44×44px (WCAG 2.5.5) */
button, a, [role="button"] {
  min-height: 44px;
  min-width: 44px;
  /* Use padding to enlarge hit area without changing visual size */
}

/* ✅ Remove 300ms tap delay */
html { touch-action: manipulation; }

/* ✅ Smooth scrolling — respect reduced motion */
@media (prefers-reduced-motion: no-preference) {
  html { scroll-behavior: smooth; }
}
```

```tsx
// ✅ Tailwind touch target
<button className="min-h-[44px] min-w-[44px] px-4" />
```

---

## Navigation Patterns

```tsx
// ✅ Mobile navigation with hamburger menu
function Navigation() {
  const [open, setOpen] = useState(false)

  return (
    <nav aria-label="Main navigation">
      {/* Desktop nav — hidden on mobile */}
      <ul className="hidden md:flex gap-6">
        <li><a href="/about">About</a></li>
        <li><a href="/work">Work</a></li>
      </ul>

      {/* Mobile hamburger */}
      <button
        className="md:hidden min-h-[44px] min-w-[44px]"
        aria-expanded={open}
        aria-controls="mobile-menu"
        aria-label={open ? 'Close menu' : 'Open menu'}
        onClick={() => setOpen(v => !v)}
      >
        <HamburgerIcon aria-hidden />
      </button>

      {/* Mobile menu panel */}
      <div id="mobile-menu" hidden={!open} className="md:hidden">
        <ul className="flex flex-col gap-2 p-4">
          <li><a href="/about" onClick={() => setOpen(false)}>About</a></li>
          <li><a href="/work"  onClick={() => setOpen(false)}>Work</a></li>
        </ul>
      </div>
    </nav>
  )
}
```

---

## Viewport and Meta

```html
<!-- ✅ Required in <head> — prevents mobile zoom issues -->
<meta name="viewport" content="width=device-width, initial-scale=1" />
```

```css
/* ✅ Prevent horizontal overflow — catch layout bugs early */
html, body {
  overflow-x: hidden;
}

/* ✅ Box-sizing reset */
*, *::before, *::after {
  box-sizing: border-box;
}
```

---

## Responsive Testing Checklist

```
Breakpoints to verify:
  □ 320px  — small phones (iPhone SE)
  □ 375px  — standard phones
  □ 768px  — tablets (portrait)
  □ 1024px — tablets (landscape) / small laptops
  □ 1440px — desktop
  □ 1920px — wide desktop

Tools:
  □ Chrome DevTools → Toggle device toolbar
  □ Firefox Responsive Design Mode
  □ https://responsively.app — multi-viewport preview

Checks:
  □ No horizontal scrollbar at any width
  □ Text is readable without zooming (min 16px base)
  □ Images don't overflow their containers
  □ Touch targets ≥ 44×44px on mobile views
  □ Navigation is usable at 320px
```
