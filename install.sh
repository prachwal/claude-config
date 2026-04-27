#!/usr/bin/env bash
# Install Claude Code config optimized for weak models (devstral, codestral, etc.)
# Usage: bash install.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo "Installing Claude Code config..."

# Create directories
mkdir -p "$CLAUDE_DIR/commands"
mkdir -p "$CLAUDE_DIR/hooks"

# Copy CLAUDE.md — always update (model instructions, not user config)
cp "$SCRIPT_DIR/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"
echo "✓ CLAUDE.md installed"

# Merge settings.json — preserve existing keys (effortLevel, theme, etc.), add new ones
if ! command -v jq &>/dev/null; then
  echo "⚠ jq not found — install it with: sudo apt install jq"
  echo "  Falling back to overwrite of settings.json"
  cp "$SCRIPT_DIR/settings.json" "$CLAUDE_DIR/settings.json"
  echo "✓ settings.json installed (overwrite)"
elif [ ! -f "$CLAUDE_DIR/settings.json" ]; then
  cp "$SCRIPT_DIR/settings.json" "$CLAUDE_DIR/settings.json"
  echo "✓ settings.json installed"
else
  # Deep merge: existing keys win for top-level scalars, new keys are added
  # permissions and hooks are always taken from the new file (not user-defined)
  jq -s '
    .[0] as $existing |
    .[1] as $new |
    $existing
    | .env          = ($existing.env          // {} | . + ($new.env          // {}))
    | .permissions  = $new.permissions
    | .hooks        = $new.hooks
  ' "$CLAUDE_DIR/settings.json" "$SCRIPT_DIR/settings.json" > "$CLAUDE_DIR/settings.json.tmp" \
  && mv "$CLAUDE_DIR/settings.json.tmp" "$CLAUDE_DIR/settings.json"
  echo "✓ settings.json merged (permissions & hooks updated, existing keys preserved)"
fi

# Copy slash commands
for cmd in "$SCRIPT_DIR/commands/"*.md; do
  name=$(basename "$cmd")
  cp "$cmd" "$CLAUDE_DIR/commands/$name"
  echo "✓ Command: /$( echo "$name" | sed 's/\.md//')"
done

# Copy hooks
for hook in "$SCRIPT_DIR/hooks/"*.py; do
  name=$(basename "$hook")
  cp "$hook" "$CLAUDE_DIR/hooks/$name"
  chmod +x "$CLAUDE_DIR/hooks/$name"
  echo "✓ Hook: $name"
done

echo ""
echo "Done. Add to your shell profile (~/.bashrc or ~/.zshrc):"
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
