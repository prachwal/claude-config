---
applyTo: "src/components/**,src/pages/**,src/app/**,src/features/**,src/ui/**"
---

# Frontend Rules

## Before writing any component or hook

Load the relevant skill:
- React patterns → `.claude/skills/react/SKILL.md`
- Tailwind CSS v4 → `.claude/skills/tailwind/SKILL.md`
- Accessibility → `.claude/skills/wcag-aria/SKILL.md`
- Forms → `.claude/skills/web-forms/SKILL.md`
- Data fetching → `.claude/skills/web-data-fetching/SKILL.md`
- Responsive layout → `.claude/skills/responsive/SKILL.md`

## Conventions

- Components: PascalCase files and exports (`UserCard.tsx`)
- Hooks: `use` prefix, camelCase (`useUserData.ts`)
- State: prefer local state; lift only when 2+ siblings need it
- No `any` — use proper generics or discriminated unions
- All interactive elements need accessible labels (role, aria-label, or visible text)
- Tailwind only — no inline styles, no CSS modules unless explicitly requested
- `clsx` or `cva` for conditional class lists — no string concatenation
