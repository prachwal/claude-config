#!/usr/bin/env bash
# Claude Code config installer — optimized for weak models (devstral, codestral, etc.)
# Usage: bash install.sh [install|update|uninstall|gui]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

MODE="${1:-install}"
case "$MODE" in
  -h|--help|help)
    cat <<EOF
Usage: bash install.sh [MODE]

Modes:
  install    (default) — copy all files, merge settings, skip existing
  update     — overwrite all files, merge settings with new keys
  uninstall  — remove all files installed by this package
  gui        — interactive Python TUI (requires Python 3)
  help       — show this message
EOF
    exit 0
    ;;
  --update)   MODE=update ;;
  --uninstall) MODE=uninstall ;;
  --gui)       MODE=gui ;;
esac

# ── GUI mode ────────────────────────────────────────────────────────────────
if [ "$MODE" = "gui" ]; then
  if ! command -v python3 &>/dev/null; then
    echo "⚠ python3 not found. Falling back to plain install."
    MODE=install
  else
    exec python3 "$SCRIPT_DIR/installer.py" "$SCRIPT_DIR" "$CLAUDE_DIR"
  fi
fi

# ── Uninstall ────────────────────────────────────────────────────────────────
if [ "$MODE" = "uninstall" ]; then
  echo "Uninstalling Claude Code config from $CLAUDE_DIR ..."

  rm -f "$CLAUDE_DIR/CLAUDE.md"           && echo "✓ Removed CLAUDE.md"

  for cmd in "$SCRIPT_DIR/commands/"*.md "$SCRIPT_DIR/commands/agents/"*.md; do
    [ -f "$cmd" ] || continue
    name=$(basename "$cmd")
    rm -f "$CLAUDE_DIR/commands/$name"    && echo "✓ Removed command: $name"
  done

  for hook in "$SCRIPT_DIR/hooks/"*.py; do
    [ -f "$hook" ] || continue
    name=$(basename "$hook")
    rm -f "$CLAUDE_DIR/hooks/$name"       && echo "✓ Removed hook: $name"
  done

  for skill_dir in "$SCRIPT_DIR/skills/"/*/; do
    name=$(basename "$skill_dir")
    rm -rf "$CLAUDE_DIR/skills/$name"     && echo "✓ Removed skill: $name"
  done

  echo ""
  echo "Done. settings.json was NOT removed (may contain your personal config)."
  echo "Remove manually with: rm $CLAUDE_DIR/settings.json"
  exit 0
fi

# ── Install / Update ─────────────────────────────────────────────────────────
if [ "$MODE" = "update" ]; then
  echo "Updating Claude Code config in $CLAUDE_DIR ..."
else
  echo "Installing Claude Code config to $CLAUDE_DIR ..."
fi

# Create directories
mkdir -p "$CLAUDE_DIR/commands/agents"
mkdir -p "$CLAUDE_DIR/hooks"
mkdir -p "$CLAUDE_DIR/skills"

# CLAUDE.md — always overwrite (not user config)
cp "$SCRIPT_DIR/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"
echo "✓ CLAUDE.md"

# Merge settings.json — preserve existing keys, always update permissions & hooks
if ! command -v jq &>/dev/null; then
  echo "⚠ jq not found — install it with: sudo apt install jq"
  echo "  Falling back to overwrite of settings.json"
  cp "$SCRIPT_DIR/settings.json" "$CLAUDE_DIR/settings.json"
  echo "✓ settings.json (overwrite)"
elif [ ! -f "$CLAUDE_DIR/settings.json" ]; then
  cp "$SCRIPT_DIR/settings.json" "$CLAUDE_DIR/settings.json"
  echo "✓ settings.json (new)"
else
  jq -s '
    .[0] as $existing |
    .[1] as $new |
    $existing
    | .env          = ($existing.env          // {} | . + ($new.env          // {}))
    | .permissions  = $new.permissions
    | .hooks        = $new.hooks
  ' "$CLAUDE_DIR/settings.json" "$SCRIPT_DIR/settings.json" > "$CLAUDE_DIR/settings.json.tmp" \
  && mv "$CLAUDE_DIR/settings.json.tmp" "$CLAUDE_DIR/settings.json"
  echo "✓ settings.json (merged — permissions & hooks updated, your keys kept)"
fi

# Slash commands (root + agents subdir)
for cmd in "$SCRIPT_DIR/commands/"*.md; do
  [ -f "$cmd" ] || continue
  name=$(basename "$cmd")
  cp "$cmd" "$CLAUDE_DIR/commands/$name"
  echo "✓ /$(echo "$name" | sed 's/\.md//')"
done

for cmd in "$SCRIPT_DIR/commands/agents/"*.md; do
  [ -f "$cmd" ] || continue
  name=$(basename "$cmd")
  cp "$cmd" "$CLAUDE_DIR/commands/agents/$name"
  echo "✓ /agent:$(echo "$name" | sed 's/\.md//')"
done

# Hooks
for hook in "$SCRIPT_DIR/hooks/"*.py; do
  [ -f "$hook" ] || continue
  name=$(basename "$hook")
  cp "$hook" "$CLAUDE_DIR/hooks/$name"
  chmod +x "$CLAUDE_DIR/hooks/$name"
  echo "✓ Hook: $name"
done

# Skills — each skill lives in its own subdir with SKILL.md
for skill_dir in "$SCRIPT_DIR/skills/"/*/; do
  [ -d "$skill_dir" ] || continue
  name=$(basename "$skill_dir")
  mkdir -p "$CLAUDE_DIR/skills/$name"
  cp "$skill_dir/SKILL.md" "$CLAUDE_DIR/skills/$name/SKILL.md"
  echo "✓ Skill: $name"
done

echo ""
echo "Done."
if [ "$MODE" = "install" ]; then
  echo "Add to your shell profile (~/.bashrc or ~/.zshrc):"
  echo ""
  cat << 'SHELL'
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
SHELL
fi
