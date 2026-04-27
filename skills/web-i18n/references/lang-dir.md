# lang and dir

- `lang` describes the language of an element using a BCP 47 tag.
- Set `lang` on the document root and on inline text that switches language.
- `dir` controls text direction: `ltr`, `rtl`, or `auto`.
- Use `dir` intentionally for RTL content and mixed-direction text.

---

## Setting lang on the document

```html
<!-- ✅ Always set lang on <html> -->
<html lang="en">

<!-- ✅ Region variant when relevant -->
<html lang="en-GB">
<html lang="zh-Hant-TW">  <!-- Traditional Chinese, Taiwan -->
```

```tsx
// React / Vite — set in index.html or via document.documentElement.lang
document.documentElement.lang = locale  // 'pl', 'ar', 'zh-TW' …
```

## Inline language switches

```html
<!-- ✅ Mark inline foreign text so screen readers switch voice -->
<p>The French word <span lang="fr">bonjour</span> means hello.</p>

<!-- ✅ Bidirectional inline quote -->
<p>The Arabic greeting is <span lang="ar" dir="rtl">مرحبا</span>.</p>
```

## RTL layouts

```html
<!-- ✅ Set dir on <html> for full RTL pages -->
<html lang="ar" dir="rtl">

<!-- ✅ Or on individual sections -->
<section dir="rtl" lang="he"> … </section>
```

```css
/* ✅ Use logical properties — flip automatically with dir -->
.card {
  /* instead of margin-left / margin-right */
  margin-inline-start: 1rem;
  margin-inline-end: 1rem;

  /* instead of padding-left */
  padding-inline-start: 1.5rem;

  /* instead of border-left */
  border-inline-start: 2px solid var(--color-border);
}

/* ✅ Text alignment */
.label { text-align: start; }  /* left in LTR, right in RTL */
```

```tsx
// ✅ Tailwind v4 — use logical utilities
<div className="ms-4 ps-6 border-s-2">
  {/* ms = margin-inline-start, ps = padding-inline-start, border-s = border-inline-start */}
</div>
```

## dir="auto"

```html
<!-- ✅ Use auto when content direction is unknown (user input) -->
<input dir="auto" type="text" />
<p dir="auto">{userGeneratedText}</p>

<!-- ❌ Don't use auto on the <html> element — set it explicitly -->
```

## BCP 47 tag reference

```
Language only:     en, pl, ar, zh, ja
Language + region: en-US, en-GB, pt-BR, zh-TW
Language + script: zh-Hant, zh-Hans, sr-Latn
Full:              zh-Hant-TW, sr-Latn-RS
```

Use `navigator.language` to get the user's preferred language from the browser.

