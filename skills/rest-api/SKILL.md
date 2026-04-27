---
name: rest-api
description: Use when building or reviewing Node.js REST API endpoints, middleware, input validation, authentication, authorization, database access, and error handling.
---

# SKILL: REST API Patterns

Read this when: adding endpoints, handling auth, connecting to DB.

---

## Project Structure

```
src/
  routes/       # route definitions only — no logic here
  controllers/  # request/response handling
  services/     # business logic — pure functions, no req/res
  middleware/   # express middleware (auth, validate, error)
  db/           # database client and queries
  types/        # shared TypeScript types
  app.ts        # express app setup
  server.ts     # listen — separate from app for testing
```

---

## Key Rules

```
1. Validate all input at boundary — use zod, not manual checks
2. Never expose internals in error responses
3. Always call next(error) in async controllers — never swallow
4. Register error middleware LAST in app.ts
5. Validate env vars at startup — fail fast before serving traffic
6. Never return passwordHash or secrets in responses — use select:{}
```

---

## HTTP Status Codes

| Code | When |
|------|------|
| 200  | Success (GET, PUT, PATCH) |
| 201  | Created (POST) |
| 204  | Success, no body (DELETE) |
| 400  | Bad request / validation error |
| 401  | Not authenticated |
| 403  | Authenticated but not authorized |
| 404  | Resource not found |
| 409  | Conflict (duplicate) |
| 422  | Unprocessable (valid format, bad data) |
| 429  | Rate limited |
| 500  | Server error (log it, hide details) |

---

## References

- [references/controller-patterns.md](references/controller-patterns.md) — validation (zod), auth middleware (JWT), controller, error middleware, DB pattern, env vars
