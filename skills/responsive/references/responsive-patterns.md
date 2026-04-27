# Responsive Patterns: Typography, Images, Navigation, Testing

## Fluid Typography (clamp)
```css
/* No layout shift between breakpoints */
@theme {
  --text-hero:    clamp(2rem, 5vw + 1rem, 4.5rem);
  --text-heading: clamp(1.5rem, 3vw + 0.5rem, 2.5rem);
  --text-body:    clamp(1rem, 1vw + 0.75rem, 1.125rem);
  --text-small:   0.875rem;
}

p { max-width: 70ch; }   /* ~65-75 chars per line is optimal */
```
```tsx
<h1 className="text-[--text-hero] font-bold leading-tight tracking-tight" />
```

## Images and Media
```tsx
// Responsive image
<img src="photo.jpg" alt="…" className="w-full h-auto object-cover" />

// Aspect ratio container (prevents layout shift before load)
<div className="aspect-video w-full overflow-hidden rounded-lg">
  <img src="…" alt="…" className="w-full h-full object-cover" />
</div>

// Art direction with <picture>
<picture>
  <source media="(min-width: 1024px)" srcSet="hero-desktop.webp" />
  <source media="(min-width: 640px)"  srcSet="hero-tablet.webp" />
  <img src="hero-mobile.webp" alt="…" />
</picture>
```
```css
/* Global image defaults */
img, video { max-width: 100%; height: auto; display: block; }
```

## Mobile Navigation (hamburger)
```tsx
function Navigation() {
  const [open, setOpen] = useState(false)
  return (
    <nav aria-label="Main navigation">
      <ul className="hidden md:flex gap-6">
        <li><a href="/about">About</a></li>
        <li><a href="/work">Work</a></li>
      </ul>

      <button
        className="md:hidden min-h-[44px] min-w-[44px]"
        aria-expanded={open}
        aria-controls="mobile-menu"
        aria-label={open ? 'Close menu' : 'Open menu'}
        onClick={() => setOpen(v => !v)}
      >
        <HamburgerIcon aria-hidden />
      </button>

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

## Responsive Testing Checklist
```
Breakpoints to verify:
  □ 320px  — small phones (iPhone SE)
  □ 375px  — standard phones
  □ 768px  — tablets (portrait)
  □ 1024px — tablets (landscape) / small laptops
  □ 1440px — desktop

Tools:
  □ Chrome DevTools → Toggle device toolbar
  □ Firefox Responsive Design Mode
  □ https://responsively.app

Checks:
  □ No horizontal scrollbar at any width
  □ Text readable without zoom (min 16px base)
  □ Images don't overflow containers
  □ Touch targets ≥ 44×44px on mobile
  □ Navigation usable at 320px
```
