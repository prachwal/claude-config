#!/usr/bin/env python3
"""
Post-tool-use hook for Claude Code.
Processes tool results to catch common errors and add helpful context.
"""

import json
import sys
import re


COMMON_ERRORS = {
    r"ModuleNotFoundError: No module named '(.+)'": (
        "Missing Python module. Run: pip install {0}"
    ),
    r"Cannot find module '(.+)'": (
        "Missing Node module. Run: npm install {0}"
    ),
    r"ENOENT: no such file or directory": (
        "File not found. Check the path exists before reading/writing."
    ),
    r"Permission denied": (
        "Permission error. Check file permissions with: ls -la <file>"
    ),
    r"SyntaxError: (.+)": (
        "Syntax error: {0}. Re-read the file and fix the syntax."
    ),
    r"EADDRINUSE": (
        "Port already in use. Find the process: lsof -i :<port>"
    ),
    r"git: command not found": (
        "Git not installed or not in PATH."
    ),
    r"fatal: not a git repository": (
        "Not inside a git repo. Run: git init"
    ),
}


def analyze_output(output: str) -> str | None:
    """Return helpful hint if output contains known error pattern."""
    for pattern, hint in COMMON_ERRORS.items():
        match = re.search(pattern, output)
        if match:
            groups = match.groups()
            return hint.format(*groups) if groups else hint
    return None


def main():
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")
    tool_response = hook_input.get("tool_response", {})

    # Extract output text
    output = ""
    if isinstance(tool_response, dict):
        output = tool_response.get("output", "") or tool_response.get("stderr", "")
    elif isinstance(tool_response, str):
        output = tool_response

    if not output:
        sys.exit(0)

    hint = analyze_output(output)
    if hint:
        print(f"\n💡 Hook hint: {hint}", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
