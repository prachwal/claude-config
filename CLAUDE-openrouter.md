# Claude Code — OpenRouter Profile

## RULES
- Read file before editing. One change at a time. No `any` in TS. No `// TODO`.
- No unrequested refactors. No new packages without asking. No `rm -rf`.
- Brief output: no preamble, no summary. Report blockers immediately.

## MODEL NOTE
Running via OpenRouter. Use the model configured by the alias/env — do NOT switch models automatically.

1. **Never switch models automatically** — use the model set by the alias/env.
2. **Never spawn Opus as a subagent automatically** — Opus only when user explicitly uses `cc_opus`.
3. **Subagents: always Haiku unless current task clearly requires Sonnet reasoning.**

## KNOWN OPENROUTER ISSUES
| Error | Cause | Fix |
|-------|-------|-----|
| `maximum context length` (131072) | Model has smaller window than Claude; tool messages inflate token count | Switch to a model with ≥200k context or enable `context-compression` plugin |
| `Unexpected role 'tool' after role 'user'` (Mistral code 3230) | Mistral-backed models reject OpenAI tool-call message ordering | Avoid `mistral/*` and Mistral-routed models (e.g. `qwen/qwen3-235b-a22b`) when tools are active; use Anthropic/OpenAI/Google providers instead |
| `invalid request error` (Novita 400) | `moonshotai/kimi-k2` via Novita rejects tool-call message format used by Claude Code | Use `--no-tools` for simple prompts, or switch to a different provider/model for agentic use |

**Safe models for agentic (tool-heavy) use:** `anthropic/claude-*`, `openai/gpt-4*`, `google/gemini-2.5-pro`

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
