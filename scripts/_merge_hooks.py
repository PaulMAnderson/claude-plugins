#!/usr/bin/env python3
"""Merge plugin hooks into ~/.claude/settings.json without duplicates.

Usage:
    _merge_hooks.py <hooks.json> <settings.json> <plugin_root>

Substitutes ${CLAUDE_PLUGIN_ROOT} with plugin_root in all command values,
then merges hook entries deduplicating by script basename so that
re-running install (e.g. after moving the repo) updates paths in-place
rather than accumulating duplicate entries.
Writes atomically via a temp file.
"""

import json
import os
import sys
import tempfile


def resolve_plugin_root(obj, plugin_root):
    """Recursively substitute ${CLAUDE_PLUGIN_ROOT} in all string values."""
    if isinstance(obj, str):
        return obj.replace("${CLAUDE_PLUGIN_ROOT}", plugin_root)
    if isinstance(obj, list):
        return [resolve_plugin_root(item, plugin_root) for item in obj]
    if isinstance(obj, dict):
        return {k: resolve_plugin_root(v, plugin_root) for k, v in obj.items()}
    return obj


def get_command(hook_entry):
    """Extract the command value from a hook entry."""
    return hook_entry.get("command", "")


def script_basename(cmd):
    """Return the filename of a command path, used as the dedup key."""
    return os.path.basename(cmd) if cmd else ""


def merge_hooks(plugin_hooks, settings_hooks):
    """Merge plugin hook events into settings hooks.

    Deduplicates by script basename: if an existing entry already has a hook
    with the same filename (e.g. session-start.sh), its command path is updated
    in-place rather than adding a duplicate. This means re-running install after
    moving the repo updates paths cleanly.
    """
    result = dict(settings_hooks)

    for event_type, plugin_entries in plugin_hooks.items():
        if event_type not in result:
            result[event_type] = []

        existing = result[event_type]

        # Build a map of basename -> (group_index, hook_index) for existing hooks
        basename_index = {}
        for gi, group in enumerate(existing):
            for hi, hook in enumerate(group.get("hooks", [])):
                bn = script_basename(get_command(hook))
                if bn:
                    basename_index[bn] = (gi, hi)

        # Merge incoming plugin entries
        for plugin_group in plugin_entries:
            hooks_to_add = []
            for hook in plugin_group.get("hooks", []):
                cmd = get_command(hook)
                bn = script_basename(cmd)
                if bn in basename_index:
                    # Update the path in-place
                    gi, hi = basename_index[bn]
                    existing[gi]["hooks"][hi]["command"] = cmd
                else:
                    hooks_to_add.append(hook)
                    if bn:
                        basename_index[bn] = None  # placeholder, will be set when appended

            if hooks_to_add:
                new_group = dict(plugin_group)
                new_group["hooks"] = hooks_to_add
                existing.append(new_group)

        result[event_type] = existing

    return result


def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <hooks.json> <settings.json> <plugin_root>", file=sys.stderr)
        sys.exit(1)

    hooks_path, settings_path, plugin_root = sys.argv[1], sys.argv[2], sys.argv[3]
    plugin_root = os.path.abspath(plugin_root)

    with open(hooks_path) as f:
        plugin_data = json.load(f)

    plugin_hooks = resolve_plugin_root(plugin_data.get("hooks", {}), plugin_root)

    # Read existing settings.json (or start with empty object)
    if os.path.exists(settings_path):
        with open(settings_path) as f:
            settings = json.load(f)
    else:
        settings = {}

    settings_hooks = settings.get("hooks", {})
    settings["hooks"] = merge_hooks(plugin_hooks, settings_hooks)

    # Atomic write: write to temp file in same directory, then rename
    settings_dir = os.path.dirname(os.path.abspath(settings_path))
    fd, tmp_path = tempfile.mkstemp(dir=settings_dir, suffix=".json.tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(settings, f, indent=2)
            f.write("\n")
        os.replace(tmp_path, settings_path)
    except Exception:
        os.unlink(tmp_path)
        raise

    print(f"  Merged hooks from {os.path.basename(hooks_path)} into {settings_path}")


if __name__ == "__main__":
    main()
