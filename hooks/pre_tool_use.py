#!/usr/bin/env python3
"""
Pre-tool-use hook for Claude Code.
Intercepts dangerous bash commands and file operations before execution.
"""

import json
import sys
import re

DANGEROUS_PATTERNS = [
    (r"rm\s+-rf\s+[/~]", "Recursive delete of root/home"),
    (r"rm\s+-rf\s+\*", "Recursive delete all"),
    (r">\s*/etc/", "Overwriting system config"),
    (r"curl.+\|\s*(ba)?sh", "Piping curl to shell"),
    (r"wget.+\|\s*(ba)?sh", "Piping wget to shell"),
    (r"DROP\s+TABLE", "SQL DROP TABLE"),
    (r"DROP\s+DATABASE", "SQL DROP DATABASE"),
    (r"TRUNCATE\s+TABLE", "SQL TRUNCATE"),
    (r"DELETE\s+FROM\s+\w+\s*;", "SQL DELETE without WHERE"),
    (r"chmod\s+777", "chmod 777 (insecure permissions)"),
    (r"sudo\s+rm", "sudo rm"),
    (r":(){:|:&};:", "Fork bomb"),
]

WARN_PATTERNS = [
    (r"npm\s+publish", "Publishing to npm"),
    (r"git\s+push\s+.*--force", "Force push"),
    (r"git\s+reset\s+--hard", "Hard git reset"),
    (r"git\s+clean\s+-fd", "Git clean -fd"),
]


def check_command(command: str) -> tuple[str, str | None]:
    """Returns ('block'|'warn'|'allow', reason)"""
    for pattern, reason in DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return "block", reason
    for pattern, reason in WARN_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return "warn", reason
    return "allow", None


def main():
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)  # If we can't parse, don't block

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    if tool_name == "Bash":
        command = tool_input.get("command", "")
        action, reason = check_command(command)

        if action == "block":
            print(
                json.dumps({
                    "decision": "block",
                    "reason": f"BLOCKED: {reason}\nCommand: {command}\n\nThis command was blocked by the safety hook. Ask the user to run it manually if needed."
                })
            )
            sys.exit(0)

        if action == "warn":
            # Output warning to stderr (visible in Claude's thinking)
            print(f"⚠️  WARNING: {reason}", file=sys.stderr)
            # Still allow, but log it

    sys.exit(0)


if __name__ == "__main__":
    main()
