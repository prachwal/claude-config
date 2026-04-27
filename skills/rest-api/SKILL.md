---
name: rest-api
description: Use when building or reviewing Node.js REST API endpoints, middleware, input validation, authentication, authorization, database access, and error handling.
---

# SKILL: REST API Patterns

Reference for building Node.js APIs correctly.
Read this when: adding endpoints, handling auth, connecting to DB.

---

## Project Structure

```
src/
  routes/          # route definitions only — no logic here
    auth.ts
    users.ts
  controllers/     # request/response handling
    auth.controller.ts
    users.controller.ts
  services/        # business logic — pure functions, no req/res
    auth.service.ts
    users.service.ts
  middleware/      # express middleware
    auth.middleware.ts
    validate.middleware.ts
    error.middleware.ts
  db/              # database client and queries
    client.ts
    users.queries.ts
  types/           # shared TypeScript types
    index.ts
  app.ts           # express app setup
  server.ts        # listen — separate from app for testing
```

---

## Request Validation Pattern (zod)

```ts
// types/schemas.ts
import { z } from 'zod'

export const CreateUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(100),
  name: z.string().min(1).max(100).trim(),
})

export type CreateUserInput = z.infer<typeof CreateUserSchema>

// middleware/validate.ts
import { Request, Response, NextFunction } from 'express'
import { ZodSchema } from 'zod'

export function validate(schema: ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body)
    if (!result.success) {
      return res.status(400).json({
        error: 'Validation failed',
        details: result.error.flatten().fieldErrors,
      })
    }
    req.body = result.data // use parsed + typed data
    next()
  }
}

// routes/users.ts
router.post('/users', validate(CreateUserSchema), createUser)
```

---

## Auth Middleware (JWT)

```ts
// middleware/auth.ts
import jwt from 'jsonwebtoken'
import { Request, Response, NextFunction } from 'express'

export interface AuthRequest extends Request {
  userId: string
}

export function requireAuth(req: Request, res: Response, next: NextFunction) {
  const header = req.headers.authorization
  if (!header?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Unauthorized' })
  }

  const token = header.slice(7)
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!) as { sub: string }
    ;(req as AuthRequest).userId = payload.sub
    next()
  } catch {
    res.status(401).json({ error: 'Invalid token' })
  }
}
```

---

## Controller Pattern

```ts
// controllers/users.controller.ts
import { Request, Response, NextFunction } from 'express'
import { AuthRequest } from '../middleware/auth'
import { getUserById, updateUser } from '../services/users.service'
import { UpdateUserSchema } from '../types/schemas'

export async function getMe(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const user = await getUserById((req as AuthRequest).userId)
    if (!user) {
      res.status(404).json({ error: 'User not found' })
      return
    }
    res.json({ data: user })
  } catch (error) {
    next(error) // pass to error middleware
  }
}
```

---

## Error Middleware (put LAST in app.ts)

```ts
// middleware/error.ts
import { Request, Response, NextFunction } from 'express'

export function errorHandler(
  error: unknown,
  _req: Request,
  res: Response,
  _next: NextFunction
) {
  console.error(error) // log full error server-side

  if (error instanceof Error) {
    // Known error types
    if (error.name === 'ValidationError') {
      return res.status(400).json({ error: error.message })
    }
    if (error.name === 'UnauthorizedError') {
      return res.status(401).json({ error: 'Unauthorized' })
    }
  }

  // Never expose internals to client
  res.status(500).json({ error: 'Internal server error' })
}
```

---

## Database Pattern (Prisma example)

```ts
// services/users.service.ts
import { prisma } from '../db/client'
import bcrypt from 'bcryptjs'

export async function createUser(input: CreateUserInput) {
  // Check duplicate
  const existing = await prisma.user.findUnique({
    where: { email: input.email }
  })
  if (existing) {
    const err = new Error('Email already registered')
    err.name = 'ConflictError'
    throw err
  }

  const hash = await bcrypt.hash(input.password, 12)

  return prisma.user.create({
    data: {
      email: input.email,
      name: input.name,
      passwordHash: hash,
    },
    select: {
      id: true,
      email: true,
      name: true,
      createdAt: true,
      // passwordHash: false — never return this
    }
  })
}
```

---

## Environment Variables

```ts
// config/env.ts — validate at startup, fail fast
import { z } from 'zod'

const EnvSchema = z.object({
  PORT: z.string().default('3000'),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
})

const result = EnvSchema.safeParse(process.env)
if (!result.success) {
  console.error('Invalid environment:', result.error.flatten())
  process.exit(1)
}

export const env = result.data
```

---

## HTTP Status Codes — Quick Reference

| Code | When |
|------|------|
| 200 | Success (GET, PUT, PATCH) |
| 201 | Created (POST) |
| 204 | Success, no body (DELETE) |
| 400 | Bad request / validation error |
| 401 | Not authenticated |
| 403 | Authenticated but not authorized |
| 404 | Resource not found |
| 409 | Conflict (duplicate) |
| 422 | Unprocessable (valid format, bad data) |
| 429 | Rate limited |
| 500 | Server error (log it, hide details) |
