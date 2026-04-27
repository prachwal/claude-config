# TypeScript Formatting and Import Discipline

## Prettier Configuration
```json
{
  "printWidth": 100,
  "tabWidth": 2,
  "singleQuote": false,
  "trailingComma": "all",
  "semi": true
}
```

- Double quotes are the TypeScript community default.
- Always include trailing commas in multi-line structures — reduces diff noise.
- Keep imports sorted: use `import type` for type-only imports (`verbatimModuleSyntax` enforces this).

## Import Discipline
```ts
// Type-only import — required with verbatimModuleSyntax
import type { Config, Context } from "@netlify/functions";

// Group and order: external → internal → relative
import { z } from "zod";

import type { Product } from "@/models/product";
import { ProductService } from "@/services/product-service";

import { fail, ok } from "../lib/response";
```

- One import per module. Do not mix type and value imports unless the bundler requires it.
- Avoid re-exporting everything with barrel files — they hurt tree shaking and slow compilers.
- Use path aliases via `tsconfig.paths` instead of `../../..` relative chains.

## Module Organization
```
src/
  models/       ← pure types and domain schemas (no side effects)
  services/     ← business logic; depends on models and ports
  lib/          ← stateless helpers: parsing, formatting, errors
  adapters/     ← implementations of ports (DB, HTTP, storage)
  contracts/    ← API request/response types shared with callers
```

- Keep `models/` free of runtime dependencies.
- Domain logic in `services/`, transport in handlers, types in `models/`.
