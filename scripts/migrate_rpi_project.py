"""Copy a legacy RPI project's state into Astrolabe's local format."""

from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import tempfile


class MigrationError(Exception):
    """A project cannot be migrated without risking existing state."""


def _exists(path: Path) -> bool:
    return os.path.lexists(path)


def _check_tree(path: Path) -> None:
    if path.is_symlink() or not path.is_dir():
        raise MigrationError(f"Expected a real directory: {path}")
    for parent, dirs, files in os.walk(path, followlinks=False):
        for name in dirs + files:
            item = Path(parent) / name
            if item.is_symlink() or not (item.is_dir() or item.is_file()):
                raise MigrationError(f"Symlink or special file is not supported: {item}")


def plan(root: Path) -> tuple[bool, list[str]]:
    """Validate a project and describe its migration without writing files."""
    root = root.resolve()
    if not root.is_dir():
        raise MigrationError(f"Project directory does not exist: {root}")
    target = root / ".astrolabe"
    if _exists(target):
        if target.is_dir() and not target.is_symlink() and (target / "MIGRATION.md").is_file():
            if (target / "MIGRATION.md").read_text(encoding="utf-8").startswith("# Legacy RPI migration\n"):
                return True, ["Already migrated; no changes"]
        raise MigrationError(f"Target already exists: {target}")
    source = root / ".rpi"
    if not _exists(source):
        raise MigrationError(f"Legacy state directory does not exist: {source}")
    _check_tree(source)
    mappings = [".rpi/ -> .astrolabe/legacy-rpi/",
                "schema-1 STATUS.md, HISTORY.md, and empty PLANNED.md -> .astrolabe/"]
    if (source / "SESSION.md").is_file():
        mappings.append(".rpi/SESSION.md -> .astrolabe/HISTORY.md (indented import)")
    for name in ("PROJECT.md", "CONTEXT.md", "design-plan-guidance.md", "implementation-plan-guidance.md"):
        if (source / name).is_file():
            mappings.append(f".rpi/{name} -> .astrolabe/{name}")
    for name in ("design-plans", "implementation-plans"):
        path = root / "docs" / name
        if _exists(path):
            _check_tree(path)
            mappings.append(f"docs/{name}/ -> .astrolabe/docs/{name}/")
    return False, mappings


def _history(source: Path, timestamp: str) -> str:
    lines = ["# History", "", f"### {timestamp} — legacy — rpi-migration", "",
             "- Intent: Preserve legacy RPI session history.",
             "- Outcome: Original SESSION.md is also stored at legacy-rpi/SESSION.md.",
             "- Result: completed", ""]
    session = source / "SESSION.md"
    if session.is_file():
        lines.extend(["Legacy session content (indented):", ""])
        content = session.read_bytes().decode("utf-8", errors="replace")
        lines.extend("    " + line for line in content.splitlines())
        if not content:
            lines.append("    (empty)")
        lines.append("")
    return "\n".join(lines) + "\n"


def migrate(root: Path, dry_run: bool = False) -> tuple[bool, list[str]]:
    """Return (already_migrated, actions); publish only a complete target."""
    root = root.resolve()
    already, actions = plan(root)
    if already or dry_run:
        return already, actions
    source = root / ".rpi"
    target = root / ".astrolabe"
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    stage = Path(tempfile.mkdtemp(prefix=".astrolabe-migration-", dir=root))
    try:
        shutil.copytree(source, stage / "legacy-rpi")
        for name in ("PROJECT.md", "CONTEXT.md", "design-plan-guidance.md", "implementation-plan-guidance.md"):
            file = source / name
            if file.is_file():
                shutil.copy2(file, stage / name)
        if not (stage / "PROJECT.md").exists():
            (stage / "PROJECT.md").write_text("# Project\n\nDescribe this project here.\n", encoding="utf-8")
        (stage / "HISTORY.md").write_text(_history(source, timestamp), encoding="utf-8")
        (stage / "STATUS.md").write_text(
            "---\nschema_version: 1\nstatus: active\ncurrent_tier: none\ncurrent_work: null\n"
            f"last_updated: {timestamp}\n---\nMigrated legacy RPI state.\n", encoding="utf-8")
        (stage / "PLANNED.md").write_text("# Planned Work\n\n## Backlog\n\n## Roadmap\n", encoding="utf-8")
        (stage / "MIGRATION.md").write_text(
            f"# Legacy RPI migration\n\nCompleted: {timestamp}\n\n"
            "Original `.rpi/` and root plan directories were retained. "
            "A complete `.rpi/` copy is in `legacy-rpi/`.\n", encoding="utf-8")
        for name in ("design-plans", "implementation-plans"):
            source_plans = root / "docs" / name
            if source_plans.exists():
                (stage / "docs").mkdir(exist_ok=True)
                shutil.copytree(source_plans, stage / "docs" / name)
        if _exists(target):
            raise MigrationError(f"Target appeared during migration: {target}")
        stage.rename(target)
    except Exception:
        shutil.rmtree(stage)
        raise
    return False, actions
