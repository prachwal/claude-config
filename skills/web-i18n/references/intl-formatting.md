# Locale-aware formatting

Use `Intl` APIs instead of manual string formatting.

- `Intl.DateTimeFormat` for dates and times.
- `Intl.NumberFormat` for numbers, currencies, and percentages.
- `Intl.PluralRules` for plural-sensitive copy.
- Avoid assumptions about separators, ordering, or number of plural forms.

---

## Dates and times

```ts
// ✅ Locale-aware date — user's locale from browser
const fmt = new Intl.DateTimeFormat('en-GB', { dateStyle: 'long' })
fmt.format(new Date())  // '27 April 2026'

// ✅ Relative time
const rel = new Intl.RelativeTimeFormat('en', { numeric: 'auto' })
rel.format(-1, 'day')   // 'yesterday'
rel.format(-3, 'hour')  // '3 hours ago'

// ✅ Utility: pass locale explicitly — never rely on server locale
function formatDate(date: Date, locale: string): string {
  return new Intl.DateTimeFormat(locale, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(date)
}
```

## Numbers, currencies, units

```ts
// ✅ Currency — never hardcode symbol or separator
const price = new Intl.NumberFormat('pl-PL', {
  style: 'currency',
  currency: 'PLN',
}).format(1234.5)
// '1 234,50 zł'

// ✅ Percentage
const pct = new Intl.NumberFormat('en', { style: 'percent' }).format(0.42)
// '42%'

// ✅ Compact notation (1K, 1M)
const compact = new Intl.NumberFormat('en', { notation: 'compact' }).format(12500)
// '12.5K'

// ✅ Unit
const speed = new Intl.NumberFormat('en', {
  style: 'unit',
  unit: 'kilometer-per-hour',
  unitDisplay: 'short',
}).format(80)
// '80 km/h'
```

## List formatting

```ts
// ✅ Locale-aware list join
const list = new Intl.ListFormat('en', { style: 'long', type: 'conjunction' })
list.format(['React', 'TypeScript', 'Tailwind'])
// 'React, TypeScript, and Tailwind'

const listPl = new Intl.ListFormat('pl', { style: 'long', type: 'conjunction' })
listPl.format(['React', 'TypeScript', 'Tailwind'])
// 'React, TypeScript i Tailwind'
```

## Collation / sorting

```ts
// ✅ Locale-aware sort — never use .sort() on user-visible strings
const items = ['Ångström', 'Zebra', 'apple', 'Banana']
items.sort(new Intl.Collator('en', { sensitivity: 'base' }).compare)
// ['apple', 'Ångström', 'Banana', 'Zebra']
```

## What NOT to do

```ts
// ❌ Manual formatting — breaks for non-Latin locales
const bad = `${amount} ${currencySymbol}`

// ❌ new Date().toLocaleString() without explicit locale — uses server locale
const bad2 = new Date().toLocaleString()

// ❌ Hardcoded separators
const bad3 = amount.toFixed(2).replace('.', ',')
```

