# Contrast, Headings, Motion

## Color and Contrast (WCAG 2.2 AA)
```
Minimum contrast ratios:
  Normal text (< 18pt / < 14pt bold):  4.5 : 1
  Large text  (≥ 18pt / ≥ 14pt bold):  3 : 1
  UI components and focus indicators:  3 : 1

Tools:
  https://webaim.org/resources/contrastchecker/
  Chrome DevTools → Accessibility → Color contrast
  VS Code: axe Accessibility Linter

Rules:
  ✅ Never communicate information with color alone — add text or icon
  ✅ Links distinguishable from body text (underline or 3:1 contrast)
  ✅ Focus indicators: 3:1 against adjacent colors
```

## Headings and Document Structure
```tsx
// ✅ One <h1> per page, never skip levels
<h1>Page title</h1>
  <h2>Section</h2>
    <h3>Subsection</h3>

// ❌ Never use headings for visual styling — use CSS classes
// ❌ Never skip from h1 to h3
// ❌ Never use <b> or <i> for meaning — use <strong>, <em>
```

## Visually Hidden Text (sr-only)
```css
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

## Reduced Motion
```css
/* ✅ Always respect prefers-reduced-motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```
