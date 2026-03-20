#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLAUDE_DIR="${HOME}/.claude"
DEFAULT_PLUGINS=(rpi-basic-agents rpi-research-agents rpi-plan-and-execute rpi-extending-claude)

PLUGINS=("${@:-${DEFAULT_PLUGINS[@]}}")

# Ensure required Claude directories exist
mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/agents" "$CLAUDE_DIR/commands" "$CLAUDE_DIR/plugins"

for plugin in "${PLUGINS[@]}"; do
  PLUGIN_DIR="$REPO_ROOT/plugins/$plugin"
  [[ -d "$PLUGIN_DIR" ]] || { echo "ERROR: plugin '$plugin' not found at $PLUGIN_DIR"; exit 1; }

  echo "Installing $plugin..."

  # Skills — preserve subdirectory structure
  if [[ -d "$PLUGIN_DIR/skills" ]]; then
    rsync -r "$PLUGIN_DIR/skills/" "$CLAUDE_DIR/skills/"
  fi

  # Agents — copy .md files, skip .keep placeholders
  if [[ -d "$PLUGIN_DIR/agents" ]]; then
    for f in "$PLUGIN_DIR/agents"/*.md; do
      [[ -f "$f" ]] && cp "$f" "$CLAUDE_DIR/agents/$(basename "$f")"
    done
  fi

  # Commands — namespace with plugin name prefix
  if [[ -d "$PLUGIN_DIR/commands" ]]; then
    for f in "$PLUGIN_DIR/commands"/*.md; do
      [[ -f "$f" ]] && cp "$f" "$CLAUDE_DIR/commands/${plugin}:$(basename "$f")"
    done
  fi

  # Hooks — copy scripts to stable location, then merge into settings.json
  HOOKS_JSON="$PLUGIN_DIR/hooks/hooks.json"
  if [[ -f "$HOOKS_JSON" ]]; then
    INSTALLED_HOOKS_DIR="$CLAUDE_DIR/plugins/$plugin/hooks"
    mkdir -p "$INSTALLED_HOOKS_DIR"
    for f in "$PLUGIN_DIR/hooks"/*.sh; do
      [[ -f "$f" ]] && cp "$f" "$INSTALLED_HOOKS_DIR/$(basename "$f")" && chmod +x "$INSTALLED_HOOKS_DIR/$(basename "$f")"
    done
    python3 "$REPO_ROOT/scripts/_merge_hooks.py" \
      "$HOOKS_JSON" "$CLAUDE_DIR/settings.json" "$INSTALLED_HOOKS_DIR/.."
  fi

  echo "  ✓ $plugin"
done

echo ""
echo "Done. Restart Claude Code (or /clear) to pick up changes."
