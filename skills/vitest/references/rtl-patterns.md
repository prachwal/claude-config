# React Testing Library Patterns

## Setup and Queries
```tsx
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

// Always use userEvent over fireEvent
const user = userEvent.setup()

// Render with providers — create a shared helper
function renderWithProviders(ui: ReactElement) {
  return render(
    <QueryClientProvider client={new QueryClient()}>
      <AuthProvider>{ui}</AuthProvider>
    </QueryClientProvider>
  )
}

// Query priority: getByRole > getByLabelText > getByText > getByTestId
screen.getByRole('button', { name: /submit/i })
screen.getByRole('textbox', { name: /email/i })
screen.getByRole('heading', { level: 1 })
screen.getByLabelText('Password')
screen.queryByText('Error')           // returns null if not found
await screen.findByText('Loaded')     // waits for async

// User interactions
await user.click(screen.getByRole('button'))
await user.type(screen.getByRole('textbox'), 'hello')
await user.clear(screen.getByRole('textbox'))
await user.selectOptions(screen.getByRole('combobox'), 'option1')
await user.keyboard('{Enter}')
```

## Coverage Configuration (vite.config.ts)
```ts
test: {
  coverage: {
    provider: 'v8',
    reporter: ['text', 'html'],
    thresholds: {
      lines: 80,
      functions: 80,
      branches: 70,
    },
    exclude: [
      'node_modules/',
      'src/test/',
      'src/main.tsx',
      '**/*.d.ts',
      '**/*.config.*',
    ],
  },
}
```

## Debugging
```bash
npx vitest run --reporter=verbose     # full output without truncation
npx vitest run --silent=false         # show console output
npx vitest run -t "should render"     # by test name
```
```ts
screen.debug()                        // print full DOM
screen.debug(screen.getByRole('button')) // specific element
import { logRoles } from '@testing-library/dom'
logRoles(document.body)               // list all ARIA roles
```
