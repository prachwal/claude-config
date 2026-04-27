Create a git commit for the current changes.

Steps:
1. Run `git diff --staged` — if empty, run `git diff` and ask user to stage files first
2. Analyze all changes
3. Write a commit message following Conventional Commits:
   - Format: `type(scope): description`
   - Types: feat, fix, refactor, test, docs, chore, perf, style
   - Description: imperative mood, lowercase, no period, max 72 chars
4. If changes span multiple concerns, suggest splitting into multiple commits
5. Show the proposed message and ask for confirmation before committing

Do not auto-commit without user confirmation.
