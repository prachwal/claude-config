# Claude Code Configuration — Optimized for Weak Models

## CRITICAL RULES — READ FIRST, EVERY SESSION

1. **Read before write** — never edit a file you haven't read in this session
2. **One change at a time** — make one logical change, verify it works, then continue
3. **Plan before code** — for any task > 10 lines, produce a plan first
4. **Use the right agent** — see AGENT ROUTING below
5. **Load the relevant skill** — see SKILLS below

---

## AGENT ROUTING

When given a task, determine the type and use the correct agent command:

| Task type | Command |
|-----------|---------|
| New feature spanning frontend + backend | `/agent:taskbreak <task>` first |
| React component, UI, styling | `/agent:frontend <task>` |
| API endpoint, middleware, DB query | `/agent:backend <task>` |
| Vite / TS / Vitest / ESLint setup | `/agent:setup <task>` |
| Writing tests for existing code | `/agent:tester <path>` |
| Vague or large task | `/agent:taskbreak <task>` first |

**Rule**: If the task touches more than 3 files or more than one domain, run `/agent:taskbreak` first and get the plan approved before writing any code.

---

## SKILLS — LOAD BEFORE WRITING CODE

Read the relevant skill file before writing code in that domain:

| Domain | Skill file |
|--------|-----------|
| TypeScript types, generics, utility types | `.claude/skills/ts-types/SKILL.md` |
| TypeScript structure, JSDoc, naming, tsconfig | `.claude/skills/ts-fundamentals/SKILL.md` |
| React components, hooks, context | `.claude/skills/react/SKILL.md` |
| REST API, validation, auth, DB | `.claude/skills/rest-api/SKILL.md` |
| Vitest unit/integration tests | `.claude/skills/vitest/SKILL.md` |
| Playwright E2E, browser testing | `.claude/skills/web-testing/SKILL.md` |
| Tailwind CSS v4, dark mode, tokens | `.claude/skills/tailwind/SKILL.md` |
| Accessibility audit (WCAG 2.2 QA) | `.claude/skills/a11y-review/SKILL.md` |
| ARIA code patterns in React/TSX | `.claude/skills/wcag-aria/SKILL.md` |
| Accessibility workflow and standards | `.claude/skills/web-accessibility-standards/SKILL.md` |
| Responsive design, mobile-first | `.claude/skills/responsive/SKILL.md` |
| Web forms (validation, a11y, async) | `.claude/skills/web-forms/SKILL.md` |
| Data fetching, loading/error states | `.claude/skills/web-data-fetching/SKILL.md` |
| Web performance, Core Web Vitals | `.claude/skills/web-performance/SKILL.md` |
| Frontend security (XSS, CSP, tokens) | `.claude/skills/web-security/SKILL.md` |
| ESLint flat config, TypeScript rules | `.claude/skills/eslint-config/SKILL.md` |
| Internationalization (i18n, RTL) | `.claude/skills/web-i18n/SKILL.md` |

**How to load a skill**: Use the `Read` tool on the skill file path at the start of the relevant task.

---

## TASK EXECUTION STRATEGY

### For small tasks (1-2 files, clear requirement):
1. Read target file(s)
2. Load relevant skill
3. Make change
4. Verify (tsc --noEmit, or run test)
5. Report

### For medium tasks (3-5 files):
1. Run `/agent:taskbreak` to get a plan
2. Get plan confirmed
3. Execute task by task, verifying each one
4. Run full test suite at the end

### For large tasks (6+ files, new feature):
1. Run `/agent:taskbreak` to decompose into 4-5 stages
2. Get plan confirmed
3. Execute one stage at a time:
   - Complete the stage
   - Write a handoff file: what was done, blockers, what's next
   - Start a fresh session — read the handoff file, not the full history
4. Execute in order: Setup → Backend types → Backend logic → Frontend types → Frontend UI → Tests
5. Never skip steps

**Why stages?** After ~1 hour of work a session hits 80% context fill. Staged handoffs let you continue without carrying debug noise from earlier steps.

---

## VERIFICATION COMMANDS

Run these to verify work is correct:

```bash
# TypeScript — must show 0 errors
npx tsc --noEmit 2>&1 | head -30

# Tests — must pass
npx vitest run 2>&1 | tail -20

# Lint
npx eslint src 2>&1 | head -20

# Build (before marking feature complete)
npx vite build 2>&1 | tail -10
```

---

## ERROR RECOVERY

When something fails:
1. Read the full error message
2. Identify the root cause (state it in one sentence)
3. Fix the root cause — not the symptom
4. Never apply the same fix twice
5. If stuck after 2 attempts, stop and explain the problem

---

## COMMUNICATION

- No preamble ("Sure!", "Of course!", "Great question!")
- No summary at the end ("I hope this helps!")
- Report blockers immediately and specifically
- When done: list what changed and how to verify

---

## WHAT TO NEVER DO

- Never edit a file without reading it first
- Never use `any` in TypeScript
- Never write `// TODO` in delivered code
- Never add packages without asking
- Never refactor code that wasn't requested to change
- Never skip error handling for async operations
- Never run `rm -rf` anything

---

## TASK DELEGATION

Spawn subagents to isolate context, parallelize independent work, or offload bulk mechanical tasks.
**Critical for weak models**: long context degrades quality — isolate subtasks to keep each context short.

Don't spawn when the parent needs the reasoning, or when synthesis requires holding things together.

Match subagent scope to task complexity:
- **Mechanical**: bulk reformatting, renaming, boilerplate — no judgment needed, one-shot
- **Scoped**: code exploration, in-scope synthesis — default for most subtasks
- **Architectural**: real planning, tradeoffs, cross-domain decisions — spawn a fresh session, give full context

Spawn limits:
- Mechanical subagents do not spawn further. If they need to, the task was wrong-sized — return to parent.
- Maximum spawn depth is 2 (parent → subagent → one further tier).
- Parent owns final output and cross-spawn synthesis.

---

## PREFERRED TOOLS

### Data Fetching

1. **WebFetch** — free, text-only, works on public pages that don't block bots.
2. **Browser tool** — for dynamic pages or auth walls that WebFetch can't handle. Use `snapshot` for AI-friendly DOM state, element refs for interaction.
3. When the same fetch/parse logic comes up more than once, add it to **Dedicated Tools** below.

### PDF Files

Use `pdftotext`, not the `Read` tool. Use `Read` only when the user asks to analyze images or charts inside the PDF.

### MCP vs CLI

Every connected MCP server loads its tool definitions into **every message**, even when unused. If a tool has a CLI (Playwright, GitHub CLI, Supabase CLI, Vercel CLI), **use the CLI** — pay tokens only when called. Build a skill around it so the invocation pattern is consistent.

---

## DEDICATED TOOLS

<!-- List project-specific tools here. For each, link to its skill or script file.
     Example: reddit_fetch — tools/reddit_fetch.py
     The orchestration logic lives in those files, not here. -->

---

## PROJECT-SCOPED RULES

When this file exceeds ~100 lines for a given project, offload domain rules to `.claude/rules/`:

```
.claude/rules/
  frontend.md       # component conventions, styling rules
  testing.md        # test patterns, coverage targets
  supabase.md       # DB access patterns, RLS rules
  voice-of-tone.md  # copy style, i18n tone
```

Each file can declare which paths trigger it:

```markdown
applyTo: "src/tests/**"
```

This keeps CLAUDE.md lean and loads domain context only when relevant.

---
