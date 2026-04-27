---
name: react
description: Use when building React components, managing state, writing hooks, handling async data fetching, context, or forms. Covers TSX patterns, error boundaries, and performance.
---

# SKILL: React Patterns

Read this when: creating components, managing state, handling async data.

---

## State Management Decision Tree

```
Does state need to be shared across routes?  → Zustand / Context
Does state need to survive page refresh?     → localStorage + useState
Is it server data (fetch from API)?          → custom hook or React Query
Is it UI-only (open/closed, active tab)?     → useState
Is it derived from other state?              → useMemo, NOT useState
```

---

## List Rendering Rules

```tsx
// ✅ Stable, unique ID as key
{items.map(item => <Item key={item.id} data={item} />)}

// ❌ Never index as key when list can reorder/filter
{items.map((item, i) => <Item key={i} data={item} />)}  // BAD

// ✅ Handle empty state explicitly
{items.length === 0
  ? <p>No items found</p>
  : items.map(item => <Item key={item.id} data={item} />)
}
```

---

## Performance — when to use what

```ts
// useMemo: expensive computation
const sorted = useMemo(
  () => [...items].sort((a, b) => a.name.localeCompare(b.name)),
  [items]
)

// useCallback: stable function reference for child props / useEffect deps
const handleDelete = useCallback(
  (id: string) => setItems(prev => prev.filter(i => i.id !== id)),
  []
)

// Rule: profile first, optimize second — wrapping everything is not free
```

---

## Component Rules

```tsx
// ✅ One component per file
// ✅ Props interface explicitly typed
// ✅ Default exports for page components, named exports for shared components
// ✅ Early returns for loading/error states before main render
// ❌ Never mutate state directly — always create new objects/arrays
// ❌ Never call hooks conditionally
```

---

## References

- [references/hooks-patterns.md](references/hooks-patterns.md) — data fetching hook, context pattern, useMemo/useCallback
- [references/component-patterns.md](references/component-patterns.md) — forms (controlled), error boundaries
