#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GEMINI_DIR="${HOME}/.gemini/config"
AGENTS_DIR="${HOME}/.agents"
DEFAULT_EXTENSIONS=(rpi-basic-agents rpi-research-agents rpi-plan-and-execute rpi-extending-claude rpi-house-style)

EXTENSIONS=("${@:-${DEFAULT_EXTENSIONS[@]}}")

mkdir -p "$GEMINI_DIR/skills" "$AGENTS_DIR/skills" "$AGENTS_DIR/agents"

for ext in "${EXTENSIONS[@]}"; do
  EXT_DIR="$REPO_ROOT/gemini/extensions/$ext"
  [[ -d "$EXT_DIR" ]] || { echo "ERROR: extension '$ext' not found at $EXT_DIR"; exit 1; }

  echo "Installing $ext..."

  # Skills — copy each skill directory
  if [[ -d "$EXT_DIR/skills" ]]; then
    for skill_path in "$EXT_DIR/skills"/*; do
      if [[ -d "$skill_path" ]]; then
        skill_name="$(basename "$skill_path")"
        rm -rf "$GEMINI_DIR/skills/$skill_name" "$AGENTS_DIR/skills/$skill_name"
        cp -r "$skill_path" "$GEMINI_DIR/skills/"
        cp -r "$skill_path" "$AGENTS_DIR/skills/"
      fi
    done
  fi

  # Agents — copy agent .md files
  if [[ -d "$EXT_DIR/agents" ]]; then
    for f in "$EXT_DIR/agents"/*.md; do
      [[ -f "$f" ]] && cp "$f" "$AGENTS_DIR/agents/$(basename "$f")"
    done
  fi

  # Scripts — make sure helpers are executable
  if [[ -d "$EXT_DIR/scripts" ]]; then
    chmod +x "$EXT_DIR/scripts"/* || true
  fi

  echo "  ✓ $ext"
done

# Ensure ~/.gemini/config/skills.json registers the extensions
python3 - << PYEOF
import json, os

config_file = os.path.expanduser("~/.gemini/config/skills.json")
repo_root = "$REPO_ROOT"
extensions = "${EXTENSIONS[*]}".split()

entries = []
for ext in extensions:
    skills_path = f"{repo_root}/gemini/extensions/{ext}/skills"
    if os.path.isdir(skills_path):
        entries.append({"path": skills_path})

data = {"entries": entries}
with open(config_file, "w") as f:
    json.dump(data, f, indent=2)
PYEOF

echo ""
echo "Done. Installed ${#EXTENSIONS[@]} Gemini extensions/skills to ~/.gemini/config/skills and ~/.agents/skills."
