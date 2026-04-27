---
name: web-testing
description: Use when designing or refactoring web UI test strategy, including Playwright-based end-to-end tests, regression coverage, stable locators, visual comparisons, browser compatibility, progressive enhancement, and CI reporting.
---

# SKILL: Web Testing

## Rules
- Test behavior from the user's perspective, not implementation details
- Layer: unit for logic, component for UI, E2E for critical user flows
- Stable locators: `getByRole`, `getByLabelText`, `getByText` — no CSS selectors
- Deterministic: mock network only when real deps make tests slow/unstable
- Flaky test = defect in test design, not a retry problem

## Playwright config
```ts
// playwright.config.ts
import { defineConfig, devices } from "@playwright/test"
export default defineConfig({
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "firefox",  use: { ...devices["Desktop Firefox"] } },
    { name: "webkit",   use: { ...devices["Desktop Safari"] } },
  ],
  use: { baseURL: "http://localhost:5173", trace: "on-first-retry" },
  webServer: { command: "npm run dev", url: "http://localhost:5173" },
})
```

## E2E pattern
```ts
test("user can sign in", async ({ page }) => {
  await page.goto("/login")
  await page.getByLabel("Email").fill("user@example.com")
  await page.getByLabel("Password").fill("secret")
  await page.getByRole("button", { name: "Sign in" }).click()
  await expect(page.getByRole("heading", { name: "Dashboard" })).toBeVisible()
})
```

## Critical flows to cover first
sign-in · sign-up · main CRUD action · navigation · error state · empty state

