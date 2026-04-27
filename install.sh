#!/usr/bin/env bash
# Claude Code config installer — optimized for weak models (devstral, codestral, etc.)
# Usage: bash install.sh [install|update|uninstall|gui] [--profile <name>]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

MODE="${1:-install}"
PROFILE=""

# Parse arguments
for arg in "$@"; do
  case "$arg" in
    --profile) PROFILE_NEXT=1 ;;
    *) if [ "${PROFILE_NEXT:-}" = "1" ]; then PROFILE="$arg"; PROFILE_NEXT=0; fi ;;
  esac
done

case "$MODE" in
  -h|--help|help)
    cat <<EOF
Usage: bash install.sh [MODE] [--profile <name>]

Modes:
  install    (default) — copy all files, merge settings, skip existing
  update     — overwrite all files, merge settings with new keys
  uninstall  — remove all files installed by this package
  gui        — interactive Python TUI (requires Python 3)
  help       — show this message

Profiles (--profile <name>):
  (default)    — CLAUDE.md with MODEL SELECTION (Anthropic API)
  openrouter   — CLAUDE-openrouter.md without MODEL SELECTION

Examples:
  bash install.sh
  bash install.sh --profile openrouter
  bash install.sh update --profile openrouter
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

  for rule in "$SCRIPT_DIR/rules/"*.md; do
    [ -f "$rule" ] || continue
    name=$(basename "$rule")
    rm -f "$CLAUDE_DIR/rules/$name"       && echo "✓ Removed rule: $name"
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
mkdir -p "$CLAUDE_DIR/rules"

# CLAUDE profile files — copy all CLAUDE-*.md so aliases can switch at runtime
for profile_file in "$SCRIPT_DIR/CLAUDE-"*.md; do
  [ -f "$profile_file" ] || continue
  pname=$(basename "$profile_file")
  cp "$profile_file" "$CLAUDE_DIR/$pname"
  echo "✓ $pname"
done

# CLAUDE.md — select profile if specified
if [ -n "$PROFILE" ]; then
  CLAUDE_SRC="$SCRIPT_DIR/CLAUDE-${PROFILE}.md"
  if [ ! -f "$CLAUDE_SRC" ]; then
    echo "✗ Profile not found: CLAUDE-${PROFILE}.md"
    exit 1
  fi
  cp "$CLAUDE_SRC" "$CLAUDE_DIR/CLAUDE.md"
  echo "✓ CLAUDE.md (profile: $PROFILE)"
else
  cp "$SCRIPT_DIR/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"
  echo "✓ CLAUDE.md (profile: default)"
fi

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

# Skills — each skill lives in its own subdir with SKILL.md + optional references/
for skill_dir in "$SCRIPT_DIR/skills/"/*/; do
  [ -d "$skill_dir" ] || continue
  name=$(basename "$skill_dir")
  mkdir -p "$CLAUDE_DIR/skills/$name"
  cp "$skill_dir/SKILL.md" "$CLAUDE_DIR/skills/$name/SKILL.md"
  if [ -d "$skill_dir/references" ]; then
    mkdir -p "$CLAUDE_DIR/skills/$name/references"
    cp "$skill_dir/references/"*.md "$CLAUDE_DIR/skills/$name/references/" 2>/dev/null || true
  fi
  echo "✓ Skill: $name"
done

# Rules — scoped context files loaded by path pattern
for rule in "$SCRIPT_DIR/rules/"*.md; do
  [ -f "$rule" ] || continue
  name=$(basename "$rule")
  cp "$rule" "$CLAUDE_DIR/rules/$name"
  echo "✓ Rule: $name"
done

# Aliases — write to dedicated file and ensure .bashrc sources it
cat > "$CLAUDE_DIR/aliases.sh" << 'ALIASES'
claude_or() {
  local MODEL="${1:-anthropic/claude-haiku-4-5}"
  shift 2>/dev/null
  ANTHROPIC_BASE_URL="https://openrouter.ai/api" \
  ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY" \
  ANTHROPIC_API_KEY="" \
  ANTHROPIC_DEFAULT_SONNET_MODEL="$MODEL" \
  CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 \
  claude "$@"
}

# Switch CLAUDE.md profile and run claude_or
# Usage: claude_profile <profile> [model] [claude args...]
# Example: claude_profile openrouter mistralai/devstral-small
claude_profile() {
  local PROFILE="${1:-openrouter}"
  local CLAUDE_DIR="$HOME/.claude"
  local SRC="$CLAUDE_DIR/CLAUDE-${PROFILE}.md"
  if [ ! -f "$SRC" ]; then
    echo "Profile not found: $SRC" >&2
    return 1
  fi
  cp "$SRC" "$CLAUDE_DIR/CLAUDE.md"
  echo "Switched to profile: $PROFILE"
  shift
  claude_or "$@"
}

# Verified compatible models (tool-call sequence tested)
# Free models
alias cc_gemini_flash='claude_or google/gemini-2.0-flash-001'      # ✓ tested
alias cc_qwen='claude_or qwen/qwen3-235b-a22b:free'               # ✓ tested
alias cc_qwen32='claude_or qwen/qwen3-32b:free'                   # ✓ tested

# Paid models
alias cc_qwen_p='claude_or qwen/qwen3-235b-a22b'                  # ✓ tested
alias cc_gpt_mini='claude_or openai/gpt-4o-mini'                  # ✓ tested
alias cc_gpt41_mini='claude_or openai/gpt-4.1-mini'               # ✓ tested
alias cc_gpt41_nano='claude_or openai/gpt-4.1-nano'               # ✓ tested
alias cc_gpt5_nano='claude_or openai/gpt-5-nano'                  # $0.05/$0.40 per M
alias cc_gpt54_nano='claude_or openai/gpt-5.4-nano'               # $0.20/$1.25 per M
alias cc_gpt5_mini='claude_or openai/gpt-5-mini'                  # $0.25/$2.00 per M
alias cc_gpt54_mini='claude_or openai/gpt-5.4-mini'               # $0.75/$4.50 per M
alias cc_haiku='claude_or anthropic/claude-haiku-4-5'             # ✓ tested
alias cc_sonnet='claude_or anthropic/claude-sonnet-4-5'           # ✓ tested
alias cc_opus='claude_or anthropic/claude-opus-4'
alias cc_devstral='claude_or mistralai/devstral-small'            # ✓ tested
alias cc_codestral='claude_or mistralai/codestral-2508'           # ✓ tested
alias cc_mistral_small='claude_or mistralai/mistral-small-3.2-24b-instruct' # ✓ tested
alias cc_deepseek='claude_or deepseek/deepseek-chat-v3-0324'      # ✓ tested
alias cc_grok='claude_or x-ai/grok-3-mini-beta'                   # ✓ tested
alias cc_kimi='claude_or moonshotai/kimi-k2'

# Compatibility shorthands
alias claude_devstral='claude_or mistralai/devstral-small'
alias claude_codestral='claude_or mistralai/codestral-2508'
alias claude_deepseek='claude_or deepseek/deepseek-chat-v3-0324'
alias claude_gemini='claude_or google/gemini-2.0-flash-001'
alias claude_qwen='claude_or qwen/qwen3-235b-a22b'
alias claude_kimi='claude_or moonshotai/kimi-k2'
ALIASES
echo "✓ aliases.sh"

BASHRC="$HOME/.bashrc"
if ! grep -qF '.claude/aliases.sh' "$BASHRC" 2>/dev/null; then
  printf '\n# Claude Code — shell aliases\n[ -f "$HOME/.claude/aliases.sh" ] && source "$HOME/.claude/aliases.sh"\n' >> "$BASHRC"
  echo "✓ Added source line to $BASHRC"
else
  echo "✓ $BASHRC already sources aliases.sh"
fi

echo ""
echo "Done. Reload your shell: source ~/.bashrc"
