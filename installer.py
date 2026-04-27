#!/usr/bin/env python3
"""
Interactive Claude Code config installer.
Usage: python3 installer.py [SOURCE_DIR] [TARGET_DIR]
       bash install.sh gui
"""
from __future__ import annotations
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path


# ── Descriptions shown to the user ───────────────────────────────────────────
DESCRIPTIONS: dict[str, str] = {
    "CLAUDE.md": (
        "Core instruction file loaded by Claude Code at startup.\n"
        "Sets agent routing rules, skill-loading discipline, and coding standards.\n"
        "⚠  Always overwritten — not meant to be edited by the user."
    ),
    "settings.json": (
        "Claude Code settings: API permissions, hook registration, env vars.\n"
        "Your personal keys (effortLevel, theme…) are preserved via deep merge.\n"
        "Only 'permissions' and 'hooks' sections are updated from this package."
    ),
    "commands": (
        "Slash-command markdown files copied to ~/.claude/commands/.\n"
        "Adds: /commit, /explore, /fix, /plan, /review, /test\n"
        "and agent sub-commands: /agent:backend, frontend, setup, taskbreak, tester."
    ),
    "hooks": (
        "Python hook scripts (pre_tool_use, post_tool_use, stop).\n"
        "They run automatically around every Claude tool call to add\n"
        "safety checks, logging, and token-budget enforcement."
    ),
    "skills": (
        "Reference skill files loaded on demand (react, rest-api, typescript, vitest).\n"
        "Each skill is a structured cheat-sheet for a coding domain.\n"
        "Claude reads the relevant SKILL.md before writing code in that domain."
    ),
}


# ── ENV detection & verification ─────────────────────────────────────────────
class EnvStatus:
    """Holds detected environment variable state."""
    def __init__(self) -> None:
        self.anthropic_key: str = os.environ.get("ANTHROPIC_API_KEY", "")
        self.openrouter_key: str = os.environ.get("OPENROUTER_API_KEY", "")
        self.or_verified: bool | None = None   # None = not checked yet
        self.ant_verified: bool | None = None

    @property
    def has_anthropic(self) -> bool:
        return bool(self.anthropic_key)

    @property
    def has_openrouter(self) -> bool:
        return bool(self.openrouter_key)


def _verify_openrouter(key: str) -> tuple[bool, str]:
    """Try a cheap models-list call to OpenRouter. Returns (ok, message)."""
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/models?per_page=1",
        headers={"Authorization": f"Bearer {key}", "HTTP-Referer": "claude-config-installer"},
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            if resp.status == 200:
                return True, "connected"
            return False, f"HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return False, "invalid key (401 Unauthorized)"
        return False, f"HTTP {e.code}"
    except Exception as exc:
        return False, str(exc)


def _verify_anthropic(key: str) -> tuple[bool, str]:
    """Verify Anthropic key via models endpoint."""
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/models",
        headers={"x-api-key": key, "anthropic-version": "2023-06-01"},
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            if resp.status == 200:
                return True, "connected"
            return False, f"HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return False, "invalid key (401 Unauthorized)"
        return False, f"HTTP {e.code}"
    except Exception as exc:
        return False, str(exc)


def check_env(profile: str) -> EnvStatus:
    """Detect and optionally verify relevant ENV vars for the chosen profile."""
    env = EnvStatus()

    print()
    print(hr())
    print("  Environment check")
    print(hr())

    needs_openrouter = profile == "openrouter"
    needs_anthropic = profile != "openrouter"  # default profile uses Anthropic

    # ── ANTHROPIC_API_KEY ──
    if needs_anthropic:
        if env.has_anthropic:
            print(f"  ANTHROPIC_API_KEY  ✓ set ({env.anthropic_key[:8]}…)")
            print("    Verifying… ", end="", flush=True)
            ok, msg = _verify_anthropic(env.anthropic_key)
            env.ant_verified = ok
            if ok:
                print(f"✓ {msg}")
            else:
                print(f"✗ {msg}")
        else:
            print("  ANTHROPIC_API_KEY  ✗ not set")
            print("    ⚠  Required for default profile (direct Anthropic API).")
            print("    Set it: export ANTHROPIC_API_KEY=sk-ant-…")

    # ── OPENROUTER_API_KEY ──
    if needs_openrouter:
        if env.has_openrouter:
            print(f"  OPENROUTER_API_KEY ✓ set ({env.openrouter_key[:8]}…)")
            print("    Verifying… ", end="", flush=True)
            ok, msg = _verify_openrouter(env.openrouter_key)
            env.or_verified = ok
            if ok:
                print(f"✓ {msg}")
            else:
                print(f"✗ {msg}")
        else:
            print("  OPENROUTER_API_KEY ✗ not set")
            print("    ⚠  Required for OpenRouter aliases (cc_gemini_flash, cc_qwen, …).")
            print("    Set it: export OPENROUTER_API_KEY=sk-or-…")

    return env


def hr(char: str = "─", width: int = 60) -> str:
    return char * width


def ask(prompt: str, default: str = "y", disabled: bool = False) -> bool:
    if disabled:
        print(f"  {prompt} — skipped (missing ENV var)")
        return False
    hint = "[Y/n]" if default == "y" else "[y/N]"
    try:
        ans = input(f"  {prompt} {hint} ").strip().lower()
    except EOFError:
        return default == "y"
    if ans == "":
        return default == "y"
    return ans in ("y", "yes")


def ask_mode() -> str:
    print(hr())
    print("  Claude Code Config — interactive installer")
    print(hr())
    print()
    print("  Choose mode:")
    print("    1) install   — copy files, skip existing personal settings")
    print("    2) update    — overwrite everything, keep your settings keys")
    print("    3) uninstall — remove all files installed by this package")
    print()
    try:
        choice = input("  Enter 1 / 2 / 3  [default: 1]: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        print("  Aborted.")
        sys.exit(0)
    mapping = {"1": "install", "2": "update", "3": "uninstall", "": "install"}
    return mapping.get(choice, "install")


def ask_profile(src: Path) -> str:
    """Ask user to choose a CLAUDE.md profile. Returns profile name or empty string for default."""
    profiles: list[tuple[str, str]] = [("default", "CLAUDE.md")]
    for f in sorted(src.glob("CLAUDE-*.md")):
        name = f.stem.removeprefix("CLAUDE-")
        profiles.append((name, f.name))

    if len(profiles) <= 1:
        return ""

    print()
    print("  Choose CLAUDE.md profile:")
    for i, (name, fname) in enumerate(profiles, 1):
        marker = "  (recommended for OpenRouter)" if name == "openrouter" else ""
        print(f"    {i}) {name:<12} — {fname}{marker}")
    print()
    try:
        choice = input(f"  Enter 1–{len(profiles)}  [default: 1]: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        print("  Aborted.")
        sys.exit(0)

    try:
        idx = int(choice) - 1 if choice else 0
        if 0 <= idx < len(profiles):
            name = profiles[idx][0]
            return "" if name == "default" else name
    except ValueError:
        pass
    return ""


# ── Merge settings.json (same logic as shell script) ─────────────────────────
def merge_settings(existing_path: Path, new_path: Path) -> None:
    try:
        result = subprocess.run(
            [
                "jq", "-s",
                """
                .[0] as $e | .[1] as $n |
                $e
                | .env         = ($e.env         // {} | . + ($n.env         // {}))
                | .permissions = $n.permissions
                | .hooks       = $n.hooks
                """,
                str(existing_path),
                str(new_path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        existing_path.write_text(result.stdout)
        print("    ✓ Merged (your keys preserved; permissions & hooks updated)")
    except (FileNotFoundError, subprocess.CalledProcessError):
        # jq not available or failed — fall back to full copy
        print("    ⚠ jq not available, falling back to full overwrite")
        shutil.copy2(new_path, existing_path)
        print("    ✓ Overwritten")


# ── Install ────────────────────────────────────────────────────────────────────
def do_install(src: Path, dst: Path, mode: str, profile: str = "", env: "EnvStatus | None" = None) -> None:
    is_update = mode == "update"
    is_openrouter = profile == "openrouter"
    # key_ok: whether the relevant API key is present and verified (or unverified but set)
    if is_openrouter:
        key_ok = bool(env and env.has_openrouter and env.or_verified is not False)
    else:
        key_ok = bool(env and env.has_anthropic and env.ant_verified is not False)

    print()
    print(hr())
    print(f"  {'Updating' if is_update else 'Installing'} to: {dst}")
    if not key_ok:
        print("  ⚠  API key missing or invalid — some steps will be disabled.")
    print(hr())

    # CLAUDE.md
    print()
    print("  [CLAUDE.md]")
    print(f"  {DESCRIPTIONS['CLAUDE.md']}")
    if ask("Install CLAUDE.md?", disabled=not key_ok):
        dst.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src / "CLAUDE.md", dst / "CLAUDE.md")
        print("    ✓ Done")
    else:
        print("    – Skipped")

    # settings.json
    print()
    print("  [settings.json]")
    print(f"  {DESCRIPTIONS['settings.json']}")
    settings_dst = dst / "settings.json"
    if ask("Install/merge settings.json?", disabled=not key_ok):
        dst.mkdir(parents=True, exist_ok=True)
        if not settings_dst.exists():
            shutil.copy2(src / "settings.json", settings_dst)
            print("    ✓ Installed (new)")
        else:
            merge_settings(settings_dst, src / "settings.json")
    else:
        print("    – Skipped")

    # Commands
    print()
    print("  [commands]")
    print(f"  {DESCRIPTIONS['commands']}")
    if ask("Install slash commands?", disabled=not key_ok):
        cmd_dst = dst / "commands"
        cmd_dst.mkdir(parents=True, exist_ok=True)
        agents_dst = cmd_dst / "agents"
        agents_dst.mkdir(exist_ok=True)
        count = 0
        for md in (src / "commands").glob("*.md"):
            target = cmd_dst / md.name
            if not target.exists() or is_update:
                shutil.copy2(md, target)
                print(f"    ✓ /{md.stem}")
                count += 1
            else:
                print(f"    – /{md.stem}  (exists, skipped)")
        for md in (src / "commands" / "agents").glob("*.md"):
            target = agents_dst / md.name
            if not target.exists() or is_update:
                shutil.copy2(md, target)
                print(f"    ✓ /agent:{md.stem}")
                count += 1
            else:
                print(f"    – /agent:{md.stem}  (exists, skipped)")
    else:
        print("    – Skipped")

    # Hooks
    print()
    print("  [hooks]")
    print(f"  {DESCRIPTIONS['hooks']}")
    if ask("Install hooks?", disabled=not key_ok):
        hooks_dst = dst / "hooks"
        hooks_dst.mkdir(parents=True, exist_ok=True)
        for py in (src / "hooks").glob("*.py"):
            target = hooks_dst / py.name
            if not target.exists() or is_update:
                shutil.copy2(py, target)
                target.chmod(target.stat().st_mode | 0o111)
                print(f"    ✓ {py.name}")
            else:
                print(f"    – {py.name}  (exists, skipped)")
    else:
        print("    – Skipped")

    # Skills
    print()
    print("  [skills]")
    print(f"  {DESCRIPTIONS['skills']}")
    if ask("Install skills?", disabled=not key_ok):
        skills_dst = dst / "skills"
        skills_dst.mkdir(parents=True, exist_ok=True)
        for skill_dir in sorted((src / "skills").iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_name = skill_dir.name
            target_dir = skills_dst / skill_name
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue
            if not target_dir.exists() or is_update:
                target_dir.mkdir(exist_ok=True)
                shutil.copy2(skill_md, target_dir / "SKILL.md")
                print(f"    ✓ skill/{skill_name}")
            else:
                print(f"    – skill/{skill_name}  (exists, skipped)")
    else:
        print("    – Skipped")


# ── Uninstall ──────────────────────────────────────────────────────────────────
def do_uninstall(src: Path, dst: Path) -> None:
    print()
    print(hr())
    print(f"  Uninstalling from: {dst}")
    print(hr())

    cmd_mds: list[Path] = []
    if (dst / "commands").exists():
        cmd_mds = list((dst / "commands").glob("*.md"))
    agent_mds: list[Path] = []
    if (dst / "commands" / "agents").exists():
        agent_mds = list((dst / "commands" / "agents").glob("*.md"))
    hook_pys: list[Path] = []
    if (dst / "hooks").exists():
        hook_pys = list((dst / "hooks").glob("*.py"))

    files = [
        dst / "CLAUDE.md",
        *cmd_mds,
        *agent_mds,
        *hook_pys,
    ]
    dirs = [
        dst / "skills" / d.name
        for d in (src / "skills").iterdir()
        if d.is_dir() and (dst / "skills" / d.name).exists()
    ]

    if not files and not dirs:
        print("  Nothing to remove.")
        return

    print()
    print("  Files to remove:")
    for f in files:
        if f.exists():
            print(f"    • {f.relative_to(dst)}")
    for d in dirs:
        print(f"    • skills/{d.name}/")

    print()
    if not ask("Proceed with uninstall?", default="n"):
        print("  Aborted.")
        return

    for f in files:
        if f.exists():
            f.unlink()
            print(f"    ✓ Removed {f.relative_to(dst)}")
    for d in dirs:
        shutil.rmtree(d)
        print(f"    ✓ Removed skills/{d.name}/")

    print()
    print("  settings.json was NOT removed (may contain your personal config).")
    print(f"  Remove manually: rm {dst / 'settings.json'}")


# ── Shell profile hint ─────────────────────────────────────────────────────────
SHELL_SNIPPET = """
# Add to ~/.bashrc or ~/.zshrc
claude_or() {
  local MODEL="${1:-mistralai/devstral-small}"
  shift 2>/dev/null
  ANTHROPIC_BASE_URL="https://openrouter.ai/api" \\
  ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY" \\
  ANTHROPIC_API_KEY="" \\
  ANTHROPIC_DEFAULT_SONNET_MODEL="$MODEL" \\
  CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 \\
  claude "$@"
}

alias claude_devstral='claude_or mistralai/devstral-small'
alias claude_codestral='claude_or mistralai/codestral-2508'
alias claude_deepseek='claude_or deepseek/deepseek-r1-0528'
alias claude_gemini='claude_or google/gemini-2.5-pro'
alias claude_qwen='claude_or qwen/qwen3-235b-a22b'
alias claude_kimi='claude_or moonshotai/kimi-k2'
"""


# ── Entry point ────────────────────────────────────────────────────────────────
def main() -> None:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.home() / ".claude"

    try:
        mode = ask_mode()

        profile = ""
        if mode != "uninstall":
            profile = ask_profile(src)

        env = EnvStatus()
        if mode != "uninstall":
            env = check_env(profile)

        if mode == "uninstall":
            do_uninstall(src, dst)
        else:
            do_install(src, dst, mode, profile=profile, env=env)

            # Apply selected profile
            if profile:
                profile_src = src / f"CLAUDE-{profile}.md"
            else:
                profile_src = src / "CLAUDE.md"
            if profile_src.exists():
                import shutil as _shutil
                _shutil.copy2(profile_src, dst / "CLAUDE.md")
                label = profile if profile else "default"
                print(f"    ✓ CLAUDE.md (profile: {label})")

            if mode == "install":
                print()
                print(hr())
                # Only show alias snippet for openrouter profile
                if profile == "openrouter":
                    if env.has_openrouter:
                        print("  Shell aliases (add to ~/.bashrc or ~/.zshrc):")
                        print(hr())
                        print(SHELL_SNIPPET)
                    else:
                        print("  Shell aliases skipped — OPENROUTER_API_KEY not set.")
                        print("  After setting the key, run: bash install.sh update --profile openrouter")
                        print(hr())
                else:
                    print("  Default profile uses ANTHROPIC_API_KEY directly — no aliases needed.")
                    if not env.has_anthropic:
                        print("  ⚠  Set ANTHROPIC_API_KEY before running claude.")
                    print(hr())

        print()
        print(hr())
        print("  All done.")
        print(hr())

    except KeyboardInterrupt:
        print()
        print()
        print("  Aborted.")
        sys.exit(0)


if __name__ == "__main__":
    main()
