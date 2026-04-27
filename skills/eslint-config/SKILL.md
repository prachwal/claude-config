---
name: eslint-config
description: Use when setting up, extending, or fixing ESLint configuration for TypeScript projects, including flat config, Preact/React, Node.js, Netlify Functions, and monorepo variants. Covers rule selection, plugin integration, and CI enforcement.
---

# ESLint Config Skill

Use when a project needs ESLint set up from scratch, migrated to flat config, or extended for a specific runtime.

## Core principles

1. Use flat config (`eslint.config.ts`) for all new projects. Legacy `.eslintrc` is deprecated as of ESLint v9.
2. Enable TypeScript-aware rules via `typescript-eslint`. Never configure TS rules without it.
3. Layer configs: base TypeScript → framework → project-specific overrides. Keep each layer small.
4. Treat `warn` as `error` in CI. Use `warn` only for rules in active migration.
5. Never disable rules globally without a comment explaining why.

## Base flat config (TypeScript)

```ts
// eslint.config.ts
import tseslint from "typescript-eslint";

export default tseslint.config(
  {
    ignores: ["dist/", "node_modules/", "coverage/", ".netlify/"],
  },
  tseslint.configs.recommendedTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        project: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
    rules: {
      "@typescript-eslint/no-explicit-any": "error",
      "@typescript-eslint/no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
      "@typescript-eslint/consistent-type-imports": ["error", { prefer: "type-imports" }],
      "@typescript-eslint/no-floating-promises": "error",
      "@typescript-eslint/await-thenable": "error",
      "no-console": "warn",
    },
  },
);
```

## Essential rules

| Rule | Reason |
|---|---|
| `no-explicit-any` | Enforce type safety |
| `no-floating-promises` | Catch unawaited async calls |
| `await-thenable` | Prevent `await` on non-Promises |
| `no-unused-vars` | Keep code clean |
| `consistent-type-imports` | Align with `verbatimModuleSyntax` |
| `react-hooks/exhaustive-deps` | Prevent stale closures |

## CI enforcement

```json
{ "scripts": { "lint": "eslint . --max-warnings 0" } }
```

- Run `lint` (not `lint:fix`) in CI — `--max-warnings 0` treats all warnings as failures.
- Cache `.eslintcache` between CI runs for speed.

## Inline disable (always add reason)
```ts
// eslint-disable-next-line @typescript-eslint/no-explicit-any -- third-party SDK returns any
const result = sdk.call() as any;
```

## References

Local reference files:
- [references/rules.md](references/rules.md) — annotated rule list by category with severity guidance
- [references/presets.md](references/presets.md) — ready-to-copy presets: Preact/React, Node.js, monorepo, migration guide

ESLint docs:
- [Flat config migration guide](https://eslint.org/docs/latest/use/configure/migration-guide)
- [typescript-eslint getting started](https://typescript-eslint.io/getting-started/)
