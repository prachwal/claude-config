#!/usr/bin/env python3
"""
Stop hook for Claude Code.
Runs before Claude finishes a response to validate task completion quality.
"""

import json
import sys
import re


INCOMPLETE_SIGNALS = [
    r"\bTODO\b",
    r"\bFIXME\b",
    r"\bHACK\b",
    r"\bXXX\b",
    r"pass\s*#\s*implement",
    r"raise NotImplementedError",
    r"console\.log\(['\"]debug",
    r"print\(['\"]debug",
]

GOOD_SIGNALS = [
    "let me know",
    "if you have any questions",
    "feel free to",
]


def check_response(response_text: str) -> list[str]:
    issues = []

    for pattern in INCOMPLETE_SIGNALS:
        if re.search(pattern, response_text, re.IGNORECASE):
            issues.append(f"Response may contain incomplete code: {pattern}")

    return issues


def main():
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # Get the assistant's response text
    response = hook_input.get("response", "")
    if not response:
        sys.exit(0)

    issues = check_response(response)

    if issues:
        for issue in issues:
            print(f"⚠️  {issue}", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
