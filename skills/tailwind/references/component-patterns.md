# Tailwind CSS v4: Component Variants and Patterns

## Component Variants with cva
```tsx
import { cva, type VariantProps } from 'class-variance-authority'
import { twMerge } from 'tailwind-merge'

const button = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        primary: 'bg-brand text-white hover:bg-brand-hover',
        ghost:   'hover:bg-muted hover:text-muted-foreground',
        danger:  'bg-red-600 text-white hover:bg-red-700',
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4',
        lg: 'h-12 px-6 text-lg',
      },
    },
    defaultVariants: { variant: 'primary', size: 'md' },
  }
)

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof button> {}

export function Button({ variant, size, className, ...props }: ButtonProps) {
  return <button className={twMerge(button({ variant, size }), className)} {...props} />
}
```

## Common Layout Patterns
```tsx
// Card
<div className="rounded-[--radius-card] border border-border bg-card p-6 shadow-sm" />

// Centered container
<div className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8" />

// Flex row, wraps on mobile
<div className="flex flex-wrap gap-3" />

// CSS Grid — auto-fit responsive columns
<div className="grid grid-cols-[repeat(auto-fit,minmax(280px,1fr))] gap-6" />

// Truncate text
<p className="truncate" />           // single line
<p className="line-clamp-3" />      // max 3 lines

// Focus ring (keyboard-accessible)
<button className="focus-visible:ring-2 focus-visible:ring-brand focus-visible:ring-offset-2 focus-visible:outline-none" />
```
