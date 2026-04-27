# Claude Code — Global Config

## RULES
- Read file before editing. One change at a time. No `any` in TS. No `// TODO`.
- No unrequested refactors. No new packages without asking. No `rm -rf`.
- Brief output: no preamble, no summary. Report blockers immediately.

## MODEL SELECTION
**Default: Haiku** — escalate only when needed.

| Task | Model | Flag |
|------|-------|------|
| Search, grep, read, explore, quick fix, rename, 1-file edit | **haiku** | `--model claude-haiku-4-5` |
| Component, hook, test, API endpoint, multi-file edit | **haiku** first → sonnet if output > 80 lines | _(default)_ |
| Planning, decomposition, architecture, security review | **opus** | `--model claude-opus-4` |
| Complex debug across codebase, cross-domain feature | **sonnet** | _(default)_ |

Decision rule:
1. Start with Haiku. If the response is incomplete or reasoning fails — switch to Sonnet.
2. Opus only for planning tasks (before any code is written) and security reviews.
3. Subagents: Explore → Haiku. Implementation → Haiku or Sonnet. Planning → Opus.
4. Never use Opus for code generation — use Sonnet.

## AGENT ROUTING
| Task | Command |
|------|---------|
| Vague / large / cross-domain | `/agent:taskbreak` first |
| React / UI / styling | `/agent:frontend` |
| API / DB / middleware | `/agent:backend` |
| Tests | `/agent:tester <path>` |

> 3 files or > 1 domain → always run `/agent:taskbreak` first.

## SKILLS
Before coding in any domain: `Read .claude/skills/{domain}/SKILL.md`
Domains: `ts-types` `ts-fundamentals` `react` `rest-api` `vitest` `web-testing` `tailwind` `wcag-aria` `a11y-review` `web-accessibility-standards` `responsive` `web-forms` `web-data-fetching` `web-performance` `web-security` `eslint-config` `web-i18n`

## TASK SIZE
- **Small** (1-2 files): read → skill → change → verify → done.
- **Large** (6+ files): decompose with `/agent:taskbreak` → staged execution → handoff file between stages.

## VERIFY
```
npx tsc --noEmit 2>&1 | head -20
npx vitest run 2>&1 | tail -10
```

## SUBAGENTS
Max depth 2. Mechanical tasks → no further spawning. Parent owns final output.
MCP server with a CLI → use the CLI instead (tools load into every message).

