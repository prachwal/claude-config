# Pluralization

Plural rules vary by locale.

- Do not assume singular vs plural is the only distinction.
- Keep message templates translatable.
- Use plural-aware formatting for counts and summary text.

---

## Plural categories

ICU / CLDR defines up to 6 plural categories:
`zero`, `one`, `two`, `few`, `many`, `other`

Examples:
- English: `one` (1 item), `other` (0, 2+ items)
- Polish: `one` (1), `few` (2-4, 22-24…), `many` (5-21, 25…), `other` (fractions)
- Arabic: all 6 categories are used

```ts
// ✅ Use Intl.PluralRules to select the right category
const pr = new Intl.PluralRules('pl')  // Polish
pr.select(1)   // 'one'
pr.select(3)   // 'few'
pr.select(10)  // 'many'
pr.select(0.5) // 'other'
```

## Vanilla TS pattern (no i18n library)

```ts
type PluralForms = {
  one: string
  few?: string
  many?: string
  other: string
}

function pluralize(count: number, locale: string, forms: PluralForms): string {
  const category = new Intl.PluralRules(locale).select(count)
  const template = forms[category as keyof PluralForms] ?? forms.other
  return template.replace('{n}', String(count))
}

// Usage
const en: PluralForms = { one: '{n} item', other: '{n} items' }
const pl: PluralForms = {
  one:   '{n} element',
  few:   '{n} elementy',
  many:  '{n} elementów',
  other: '{n} elementu',
}

pluralizeText(1,  'en', en)  // '1 item'
pluralizeText(3,  'en', en)  // '3 items'
pluralizeText(1,  'pl', pl)  // '1 element'
pluralizeText(3,  'pl', pl)  // '3 elementy'
pluralizeText(10, 'pl', pl)  // '10 elementów'
```

## With i18next

```json
// en.json
{
  "itemCount": "{{count}} item",
  "itemCount_other": "{{count}} items"
}
```

```json
// pl.json
{
  "itemCount_one": "{{count}} element",
  "itemCount_few": "{{count}} elementy",
  "itemCount_many": "{{count}} elementów",
  "itemCount_other": "{{count}} elementu"
}
```

```tsx
import { useTranslation } from 'react-i18next'

function ItemCount({ count }: { count: number }) {
  const { t } = useTranslation()
  return <span>{t('itemCount', { count })}</span>
}
```

## What NOT to do

```ts
// ❌ Hardcoded English pluralization
const label = count === 1 ? 'item' : 'items'

// ❌ String concatenation — untranslatable
const msg = `You have ${count} ` + (count === 1 ? 'message' : 'messages')

// ❌ Assuming only two plural forms exist
```

