Perform a thorough code review of: $ARGUMENTS

Structure your review as follows:

## Bugs & Errors
List any bugs, logic errors, or crashes waiting to happen. Include line numbers.

## Security Issues
Any injection, auth, validation, or data exposure problems.

## Performance
Obvious inefficiencies (N+1 queries, unnecessary loops, missing indexes, etc.)

## Code Quality
- Dead code / unreachable branches
- Missing error handling
- Magic numbers / hardcoded values that should be constants
- Functions doing too many things

## Style & Consistency
Deviations from the surrounding code style.

## Summary
One-paragraph verdict with severity: CRITICAL / MAJOR / MINOR / CLEAN

Do not suggest refactors unrelated to the above categories.
