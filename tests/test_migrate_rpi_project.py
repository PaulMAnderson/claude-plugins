import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from migrate_rpi_project import MigrationError, migrate, plan  # noqa: E402
from hypercube.status import parse_status  # noqa: E402


def snapshot(root: Path) -> dict:
    """Fingerprint every file, directory, and symlink under root.

    Returns a dict mapping relative path -> a tuple fingerprint:
      - files: (sha256 of contents, st_mode, st_size)
      - dirs: ("dir", None, None)
      - symlinks: ("symlink", link target, None)

    Directories are included (not just files) so a leaked empty staging
    directory is detected too. Used to assert a tree (or an entire project
    root) is byte-and-metadata-identical before and after an operation that
    must not touch it.
    """
    result: dict = {}
    if not root.exists():
        return result
    for path in sorted(root.rglob("*")):
        rel = str(path.relative_to(root))
        if path.is_symlink():
            result[rel] = ("symlink", os.readlink(path), None)
        elif path.is_dir():
            result[rel] = ("dir", None, None)
        elif path.is_file():
            stat = path.stat()
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            result[rel] = (digest, stat.st_mode, stat.st_size)
    return result


class MigrationTests(unittest.TestCase):
    def make_project(self, root: Path) -> None:
        source = root / ".rpi"
        source.mkdir()
        (source / "PROJECT.md").write_text("# My legacy project\n")
        (source / "CONTEXT.md").write_text("Unfinished research.\n")
        (source / "SESSION.md").write_bytes(b"### Old session\n\nOutcome: done.\n")
        (source / "design-plan-guidance.md").write_text("Domain terms.\n")
        (source / "notes.txt").write_bytes(b"unknown\x00file")
        plans = root / "docs" / "design-plans"
        plans.mkdir(parents=True)
        (plans / "old.md").write_text("Old design.\n")

    def test_migration_preserves_state_history_and_plans(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_project(root)
            before = (root / ".rpi" / "SESSION.md").read_bytes()
            rpi_before = snapshot(root / ".rpi")
            docs_before = snapshot(root / "docs")
            already, actions = migrate(root)
            self.assertFalse(already)
            self.assertTrue(actions)
            # The source trees that must never be touched are unchanged,
            # byte-for-byte and metadata-for-metadata.
            self.assertEqual(snapshot(root / ".rpi"), rpi_before)
            self.assertEqual(snapshot(root / "docs"), docs_before)
            target = root / ".astrolabe"
            self.assertEqual((target / "PROJECT.md").read_text(), "# My legacy project\n")
            self.assertEqual((target / "CONTEXT.md").read_text(), "Unfinished research.\n")
            self.assertEqual((target / "legacy-rpi" / "SESSION.md").read_bytes(), before)
            self.assertEqual((root / ".rpi" / "SESSION.md").read_bytes(), before)
            self.assertIn("    ### Old session", (target / "HISTORY.md").read_text())
            fields, summary = parse_status((target / "STATUS.md").read_text())
            self.assertEqual(fields["schema_version"], "1")
            self.assertEqual(fields["current_tier"], "none")
            self.assertEqual(summary, "Migrated legacy RPI state.")
            self.assertIn("## Roadmap", (target / "PLANNED.md").read_text())
            self.assertEqual((target / "design-plan-guidance.md").read_text(), "Domain terms.\n")
            self.assertEqual((target / "legacy-rpi" / "notes.txt").read_bytes(), b"unknown\x00file")
            self.assertEqual((target / "docs" / "design-plans" / "old.md").read_text(), "Old design.\n")
            self.assertTrue((root / "docs" / "design-plans" / "old.md").exists())
            # The completion marker must exist and carry the expected heading;
            # nothing currently reads or asserts on it otherwise.
            migration_notice = (target / "MIGRATION.md")
            self.assertTrue(migration_notice.is_file())
            self.assertTrue(migration_notice.read_text(encoding="utf-8").startswith("# Legacy RPI migration\n"))
            snapshot_history = (target / "HISTORY.md").read_bytes()
            rpi_before_repeat = snapshot(root / ".rpi")
            docs_before_repeat = snapshot(root / "docs")
            self.assertTrue(migrate(root)[0])
            self.assertEqual((target / "HISTORY.md").read_bytes(), snapshot_history)
            # The already-migrated no-op path must also be non-mutating.
            self.assertEqual(snapshot(root / ".rpi"), rpi_before_repeat)
            self.assertEqual(snapshot(root / "docs"), docs_before_repeat)

    def test_dry_run_and_errors_do_not_change_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(MigrationError, "does not exist"):
                plan(root)
            self.make_project(root)
            # Snapshot the ENTIRE project root, not just ".astrolabe"
            # non-existence, so a leaked ".astrolabe-migration-*" staging
            # directory (or any other stray write) is also caught.
            before = snapshot(root)
            self.assertFalse(migrate(root, dry_run=True)[0])
            self.assertEqual(snapshot(root), before)
            self.assertFalse((root / ".astrolabe").exists())
            self.assertEqual(list(root.glob(".astrolabe-migration-*")), [])
            (root / ".astrolabe").mkdir()
            with self.assertRaisesRegex(MigrationError, "already exists"):
                migrate(root)
            self.assertEqual(list((root / ".astrolabe").iterdir()), [])

    def test_symlink_rejected_without_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_project(root)
            (root / ".rpi" / "link").symlink_to("PROJECT.md")
            before = snapshot(root)
            with self.assertRaisesRegex(MigrationError, "Symlink"):
                migrate(root)
            self.assertFalse((root / ".astrolabe").exists())
            # A leaked staging directory can't be seen by presence/absence
            # of ".astrolabe" alone.
            self.assertEqual(list(root.glob(".astrolabe-migration-*")), [])
            self.assertEqual(snapshot(root), before)

    def test_symlink_in_docs_design_plans_rejected_without_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_project(root)
            (root / "docs" / "design-plans" / "link.md").symlink_to("old.md")
            before = snapshot(root)
            with self.assertRaisesRegex(MigrationError, "Symlink"):
                migrate(root)
            self.assertFalse((root / ".astrolabe").exists())
            self.assertEqual(list(root.glob(".astrolabe-migration-*")), [])
            self.assertEqual(snapshot(root), before)

    def test_symlink_in_docs_implementation_plans_rejected_without_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_project(root)
            implementation_plans = root / "docs" / "implementation-plans"
            implementation_plans.mkdir(parents=True)
            (implementation_plans / "task.md").write_text("Old task.\n")
            (implementation_plans / "link.md").symlink_to("task.md")
            before = snapshot(root)
            with self.assertRaisesRegex(MigrationError, "Symlink"):
                migrate(root)
            self.assertFalse((root / ".astrolabe").exists())
            self.assertEqual(list(root.glob(".astrolabe-migration-*")), [])
            self.assertEqual(snapshot(root), before)

    def test_symlinked_docs_directory_rejected_without_changes(self):
        # A symlink AT "docs/" itself (as opposed to inside it) must also be
        # rejected: the per-subtree symlink check only inspects
        # root/docs/<name>, so it can't see that "docs" itself was replaced.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_project(root)
            real_docs = root / "docs"
            shutil.rmtree(real_docs)
            real_docs.symlink_to(root / ".rpi")
            before = snapshot(root)
            with self.assertRaisesRegex(MigrationError, "Symlink"):
                migrate(root)
            self.assertFalse((root / ".astrolabe").exists())
            self.assertEqual(list(root.glob(".astrolabe-migration-*")), [])
            self.assertEqual(snapshot(root), before)

    def test_copy_failure_cleans_stage(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_project(root)
            before = snapshot(root)
            with patch("migrate_rpi_project.shutil.copytree", side_effect=OSError("disk failure")):
                with self.assertRaisesRegex(OSError, "disk failure"):
                    migrate(root)
            self.assertFalse((root / ".astrolabe").exists())
            self.assertEqual(list(root.glob(".astrolabe-migration-*")), [])
            self.assertTrue((root / ".rpi" / "PROJECT.md").exists())
            self.assertEqual(snapshot(root), before)

    def test_publish_uses_single_atomic_rename(self):
        # The design promises a staged copy plus a single final rename, so
        # ".astrolabe" never exists in a partial state. Force the rename
        # itself to fail partway through and prove nothing was published
        # incrementally (e.g. via mkdir + item-by-item copy instead).
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_project(root)
            rpi_before = snapshot(root / ".rpi")
            docs_before = snapshot(root / "docs")
            with patch.object(Path, "rename", autospec=True,
                               side_effect=OSError("simulated failure mid-publish")) as mock_rename:
                with self.assertRaisesRegex(OSError, "simulated failure mid-publish"):
                    migrate(root)
            mock_rename.assert_called_once()
            called_self, called_target = mock_rename.call_args.args
            self.assertTrue(called_self.name.startswith(".astrolabe-migration-"))
            self.assertEqual(called_target, root / ".astrolabe")
            self.assertFalse((root / ".astrolabe").exists())
            self.assertEqual(list(root.glob(".astrolabe-migration-*")), [])
            self.assertEqual(snapshot(root / ".rpi"), rpi_before)
            self.assertEqual(snapshot(root / "docs"), docs_before)

    def test_existing_nonempty_target_without_marker_is_conflict(self):
        # A pre-existing, non-empty ".astrolabe/" that lacks the marker file
        # must be treated as a real conflict, not a silent no-op.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_project(root)
            target = root / ".astrolabe"
            target.mkdir()
            (target / "PROJECT.md").write_text("Unrelated pre-existing content.\n")
            with self.assertRaisesRegex(MigrationError, "already exists"):
                migrate(root)
            self.assertFalse((target / "MIGRATION.md").exists())
            self.assertEqual((target / "PROJECT.md").read_text(), "Unrelated pre-existing content.\n")

    def test_second_run_with_corrupted_marker_heading_is_conflict(self):
        # If the marker's expected heading is missing or corrupted, a second
        # run must raise a conflict rather than reporting "already migrated".
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_project(root)
            migrate(root)
            target = root / ".astrolabe"
            (target / "MIGRATION.md").write_text("Not the expected heading.\n")
            with self.assertRaisesRegex(MigrationError, "already exists"):
                migrate(root)

    def test_cli_preview_and_repeat(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_project(root)
            script = Path(__file__).resolve().parents[1] / "scripts" / "migrate-rpi-project.py"
            preview = subprocess.run([sys.executable, str(script), str(root), "--dry-run"], capture_output=True, text=True)
            self.assertEqual(preview.returncode, 0, preview.stderr)
            self.assertIn("Migration preview", preview.stdout)
            self.assertFalse((root / ".astrolabe").exists())
            done = subprocess.run([sys.executable, str(script), str(root)], capture_output=True, text=True)
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertIn("Migration complete", done.stdout)
            again = subprocess.run([sys.executable, str(script), str(root)], capture_output=True, text=True)
            self.assertEqual(again.returncode, 0, again.stderr)
            self.assertIn("Already migrated", again.stdout)


if __name__ == "__main__":
    unittest.main()
