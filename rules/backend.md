---
applyTo: "src/api/**,src/server/**,src/routes/**,src/middleware/**,src/lib/**,src/db/**"
---

# Backend Rules

## Before writing API endpoints or DB queries

Load the relevant skill:
- REST API, validation, auth, DB → `.claude/skills/rest-api/SKILL.md`

## Conventions

- Validate all input at the boundary with Zod before touching business logic
- Never trust client-provided IDs for ownership — always verify against auth session
- HTTP status codes: 200 success, 201 created, 400 validation, 401 unauth, 403 forbidden, 404 not found, 409 conflict, 500 server error
- Errors: return `{ error: string }` — never leak stack traces to client
- DB queries: use parameterized queries only — no string interpolation
- Auth: short-lived JWTs (15 min access, 7 day refresh) — never store in localStorage
