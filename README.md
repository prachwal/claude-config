# claude-config

> Claude Code configuration optimized for cost-effective AI models — devstral, codestral, deepseek, gemini, and others available via [OpenRouter](https://openrouter.ai).

## What is this?

A drop-in config package for [Claude Code](https://docs.anthropic.com/claude-code) that makes smaller, cheaper LLMs work reliably on real engineering tasks. It provides:

- **`CLAUDE.md`** — core instruction file: agent routing rules, skill-loading discipline, and coding standards that prevent common weak-model failure modes
- **Slash commands** — `/commit`, `/fix`, `/plan`, `/review`, `/test`, `/explore` and agent sub-commands like `/agent:frontend`, `/agent:backend`, `/agent:taskbreak`
- **Hooks** — Python hook scripts for safety checks, token-budget enforcement, and logging around every tool call
- **Skills** — structured reference files for React, TypeScript, REST API, Vitest, Tailwind 4, accessibility (WCAG/ARIA), and responsive design
- **`installer.py`** — interactive TUI installer with descriptions of each component and per-component install/skip choice

---

## Quick start

```bash
git clone https://github.com/prachwal/claude-config
cd claude-config

# Interactive install (recommended — explains each component)
bash install.sh gui

# Or silent install
bash install.sh

# Update existing install
bash install.sh update

# Uninstall
bash install.sh uninstall
```

> **Requires:** `jq` for settings merge (`sudo apt install jq`). Python 3 for `gui` mode.

---

## Shell aliases

Add to `~/.bashrc` or `~/.zshrc`:

```bash
claude_or() {
  local MODEL="${1:-mistralai/devstral-small}"
  shift 2>/dev/null
  ANTHROPIC_BASE_URL="https://openrouter.ai/api" \
  ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY" \
  ANTHROPIC_API_KEY="" \
  ANTHROPIC_DEFAULT_SONNET_MODEL="$MODEL" \
  CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 \
  claude "$@"
}

alias claude_devstral='claude_or mistralai/devstral-small'
alias claude_codestral='claude_or mistralai/codestral-2508'
alias claude_deepseek='claude_or deepseek/deepseek-r1-0528'
alias claude_gemini='claude_or google/gemini-2.5-pro'
alias claude_qwen='claude_or qwen/qwen3-235b-a22b'
alias claude_kimi='claude_or moonshotai/kimi-k2'
```

Then: `OPENROUTER_API_KEY=sk-or-... claude_devstral`

---

## Switching CLAUDE.md profiles

The installer supports named profiles. Each profile is a `CLAUDE-<name>.md` file in the repo root. The active profile is copied to `~/.claude/CLAUDE.md` at install time.

### Available profiles

| Profile | File | Description |
|---|---|---|
| `default` | `CLAUDE.md` | Full config with Anthropic model selection (Haiku/Sonnet/Opus routing) |
| `openrouter` | `CLAUDE-openrouter.md` | Stripped-down config for OpenRouter — no automatic model switching |

### Install with a specific profile

```bash
# Install with OpenRouter profile
bash install.sh --profile openrouter

# Update and switch to default profile
bash install.sh update --profile default
```

### Switch profile at runtime (without reinstalling)

The `claude_profile` shell function (added by the installer) lets you switch profiles on the fly:

```bash
# Switch to openrouter profile and run with kimi-k2
claude_profile openrouter moonshotai/kimi-k2

# Switch back to default and run with haiku
claude_profile default anthropic/claude-haiku-4-5
```

Or manually:

```bash
# Switch active profile manually
cp ~/.claude/CLAUDE-openrouter.md ~/.claude/CLAUDE.md

# Verify
head -1 ~/.claude/CLAUDE.md
```

### Add your own profile

1. Create `CLAUDE-<name>.md` in the repo root
2. Run `bash install.sh update` — all `CLAUDE-*.md` files are copied automatically
3. Use `bash install.sh --profile <name>` or `claude_profile <name>` to activate it

---

## Project structure

```
claude-config/
├── CLAUDE.md                   # Core agent instruction file
├── install.sh                  # Bash installer (install/update/uninstall/gui)
├── installer.py                # Interactive Python TUI installer
├── settings.json               # Claude Code settings (permissions, hooks, env)
├── commands/
│   ├── commit.md               # /commit
│   ├── explore.md              # /explore
│   ├── fix.md                  # /fix
│   ├── plan.md                 # /plan
│   ├── review.md               # /review
│   ├── test.md                 # /test
│   └── agents/
│       ├── backend.md          # /agent:backend
│       ├── frontend.md         # /agent:frontend
│       ├── setup.md            # /agent:setup
│       ├── taskbreak.md        # /agent:taskbreak
│       └── tester.md           # /agent:tester
├── hooks/
│   ├── pre_tool_use.py         # Runs before every Claude tool call
│   ├── post_tool_use.py        # Runs after every Claude tool call
│   └── stop.py                 # Runs on session stop
└── skills/
    ├── react/SKILL.md          # React components, hooks, context, forms
    ├── rest-api/SKILL.md       # Node.js REST API, auth, validation, DB
    ├── typescript/SKILL.md     # TypeScript types, generics, error handling
    ├── vitest/SKILL.md         # Vitest, mocking, React Testing Library
    ├── tailwind/SKILL.md       # Tailwind CSS v4, design tokens, dark mode
    ├── wcag-aria/SKILL.md      # Accessibility: WCAG 2.2, ARIA roles, keyboard nav
    └── responsive/SKILL.md     # Responsive design, mobile-first, fluid layouts
```

---

## Skills

Skills are structured reference files that Claude loads on demand before writing code. Each skill covers one domain and is stored in `skills/<name>/SKILL.md`.

| Skill | When to load |
|---|---|
| `react` | Creating components, managing state, hooks, context |
| `typescript` | TypeScript types, generics, utility types, error handling |
| `rest-api` | API endpoints, middleware, auth, database queries |
| `vitest` | Unit tests, integration tests, mocking, RTL |
| `tailwind` | Styling with Tailwind CSS v4, design tokens, dark mode |
| `wcag-aria` | Accessible UI, keyboard navigation, ARIA roles, forms |
| `responsive` | Mobile-first layouts, fluid typography, responsive images |

---

## Web application guide

This config includes extended guidance for building production-quality web applications.

### Tailwind CSS v4

Tailwind v4 replaces `tailwind.config.js` with CSS-first configuration via `@theme`. Key setup:

```bash
npm install tailwindcss @tailwindcss/vite
```

```css
/* src/index.css */
@import "tailwindcss";

@theme {
  --color-brand: oklch(55% 0.22 260);
  --font-sans: "Inter", sans-serif;
  --radius-card: 0.75rem;
}
```

See [`skills/tailwind/SKILL.md`](skills/tailwind/SKILL.md) for component variants, dark mode, and responsive breakpoints.

### Accessibility (WCAG 2.2 AA)

All interactive UI must meet WCAG 2.2 Level AA. Critical requirements:

- **Keyboard navigation** — every interactive element reachable via `Tab`; `Escape` closes overlays
- **Focus management** — visible focus ring at all times; move focus to modals when they open
- **Contrast** — 4.5:1 for normal text, 3:1 for large text and UI components
- **ARIA** — use semantic HTML first; add ARIA only when native elements are insufficient
- **Forms** — every `<input>` has an associated `<label>`; errors announced via `role="alert"`
- **Touch targets** — minimum 44×44px for all interactive elements (WCAG 2.5.5)

See [`skills/wcag-aria/SKILL.md`](skills/wcag-aria/SKILL.md) for complete patterns.

### Responsive design

Use a **mobile-first** approach — write base styles for small screens, add breakpoint classes for larger ones:

```tsx
// ✅ Stack on mobile, row on desktop
<div className="flex flex-col sm:flex-row gap-4" />

// ✅ Fluid typography — no layout shifts at breakpoints
<h1 className="text-[clamp(2rem,5vw+1rem,4.5rem)]" />

// ✅ Responsive grid — columns fill available space
<div className="grid grid-cols-[repeat(auto-fit,minmax(280px,1fr))] gap-6" />
```

See [`skills/responsive/SKILL.md`](skills/responsive/SKILL.md) for full layout patterns and testing checklist.

---

## How it works

1. Claude Code loads `~/.claude/CLAUDE.md` at startup
2. When a task comes in, `CLAUDE.md` routes it to the appropriate agent command or skill
3. Before writing code, Claude reads the relevant `SKILL.md` (e.g., `react/SKILL.md` for a component task)
4. Hooks run around every tool call for safety and logging
5. Slash commands (`/commit`, `/fix`, etc.) provide structured, repeatable workflows

---

## License

[MIT](LICENSE)
