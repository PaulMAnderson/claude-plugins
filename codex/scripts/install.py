#!/usr/bin/env python3
"""Install the complete Astrolabe Codex skill set without overwriting other skills."""
# pattern: Imperative Shell

import argparse
import hashlib
import os
from pathlib import Path
import shutil
import sys


SOURCE = Path(__file__).resolve().parents[1] / "skills"


def tree_digest(directory):
    return {str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in directory.rglob("*") if p.is_file()}


def install(destination, copy=False, dry_run=False):
    skills = sorted(p for p in SOURCE.iterdir() if (p / "SKILL.md").is_file())
    actions = []
    # Preflight the whole bundle before creating anything, including the directory.
    for source in skills:
        target = destination / source.name
        if target.is_symlink() and target.resolve() == source.resolve():
            continue
        if target.exists() or target.is_symlink():
            if copy and not target.is_symlink() and target.is_dir() and tree_digest(target) == tree_digest(source):
                continue
            raise ValueError(f"refusing to overwrite existing skill: {target}")
        actions.append((source, target))
    for source, target in actions:
        print(f"{'copy' if copy else 'link'} {source.name} -> {target}")
    if not dry_run:
        destination.mkdir(parents=True, exist_ok=True)
        for source, target in actions:
            if copy:
                shutil.copytree(source, target)
            else:
                target.symlink_to(os.path.relpath(source, target.parent), target_is_directory=True)
    print(f"{len(skills)} skills available; {len(actions)} {'planned' if dry_run else 'installed'} at {destination}")


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    scope = cli.add_mutually_exclusive_group(required=True)
    scope.add_argument("--project", type=Path, help="Install under PROJECT/.agents/skills")
    scope.add_argument("--user", action="store_true", help="Install under ~/.agents/skills")
    scope.add_argument("--skills-dir", type=Path, help="Explicit discovery path for another Codex setup")
    cli.add_argument("--copy", action="store_true", help="Portable copies instead of live symlinks")
    cli.add_argument("--dry-run", action="store_true")
    args = cli.parse_args()
    if args.project:
        project = args.project.expanduser().resolve()
        if not project.is_dir():
            cli.error(f"project does not exist: {project}")
        destination = project / ".agents" / "skills"
    elif args.user:
        destination = Path.home() / ".agents" / "skills"
    else:
        destination = args.skills_dir.expanduser().absolute()
    try:
        install(destination, args.copy, args.dry_run)
    except (OSError, ValueError) as error:
        print(f"astrolabe-install: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
