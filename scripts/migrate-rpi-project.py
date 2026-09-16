#!/usr/bin/env python3
"""Migrate one legacy RPI project to Astrolabe's local file layout."""

import argparse
from pathlib import Path

from migrate_rpi_project import MigrationError, migrate


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path, help="Project directory containing .rpi/")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without writing files")
    args = parser.parse_args()
    try:
        already, actions = migrate(args.project_root, dry_run=args.dry_run)
    except (MigrationError, OSError, UnicodeError) as exc:
        parser.exit(1, f"Migration failed: {exc}\n")
    heading = "Already migrated" if already else "Migration preview" if args.dry_run else "Migration complete"
    print(heading)
    for action in actions:
        print(f"- {action}")


if __name__ == "__main__":
    main()
