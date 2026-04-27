# REST API: Validation, Auth, Controller, DB

## Request Validation (zod)
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
    req.body = result.data
    next()
  }
}
// routes/users.ts
router.post('/users', validate(CreateUserSchema), createUser)
```

## Auth Middleware (JWT)
```ts
import jwt from 'jsonwebtoken'
import { Request, Response, NextFunction } from 'express'

export interface AuthRequest extends Request { userId: string }

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

## Controller Pattern
```ts
export async function getMe(req: Request, res: Response, next: NextFunction): Promise<void> {
  try {
    const user = await getUserById((req as AuthRequest).userId)
    if (!user) { res.status(404).json({ error: 'User not found' }); return }
    res.json({ data: user })
  } catch (error) {
    next(error)  // always pass to error middleware
  }
}
```

## Error Middleware (register LAST in app.ts)
```ts
export function errorHandler(error: unknown, _req: Request, res: Response, _next: NextFunction) {
  console.error(error)
  if (error instanceof Error) {
    if (error.name === 'ValidationError') return res.status(400).json({ error: error.message })
    if (error.name === 'UnauthorizedError') return res.status(401).json({ error: 'Unauthorized' })
  }
  res.status(500).json({ error: 'Internal server error' })
}
```

## Database Pattern (Prisma)
```ts
export async function createUser(input: CreateUserInput) {
  const existing = await prisma.user.findUnique({ where: { email: input.email } })
  if (existing) { const e = new Error('Email already registered'); e.name = 'ConflictError'; throw e }

  const hash = await bcrypt.hash(input.password, 12)
  return prisma.user.create({
    data: { email: input.email, name: input.name, passwordHash: hash },
    select: { id: true, email: true, name: true, createdAt: true },
  })
}
```

## Environment Variables (validate at startup)
```ts
// config/env.ts
import { z } from 'zod'

const EnvSchema = z.object({
  PORT: z.string().default('3000'),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
})

const result = EnvSchema.safeParse(process.env)
if (!result.success) { console.error('Invalid environment:', result.error.flatten()); process.exit(1) }
export const env = result.data
```
