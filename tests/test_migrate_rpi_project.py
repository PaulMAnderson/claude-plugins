from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from migrate_rpi_project import MigrationError, migrate, plan  # noqa: E402
from hypercube.status import parse_status  # noqa: E402


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
            already, actions = migrate(root)
            self.assertFalse(already)
            self.assertTrue(actions)
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
            snapshot = (target / "HISTORY.md").read_bytes()
            self.assertTrue(migrate(root)[0])
            self.assertEqual((target / "HISTORY.md").read_bytes(), snapshot)

    def test_dry_run_and_errors_do_not_change_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(MigrationError, "does not exist"):
                plan(root)
            self.make_project(root)
            self.assertFalse(migrate(root, dry_run=True)[0])
            self.assertFalse((root / ".astrolabe").exists())
            (root / ".astrolabe").mkdir()
            with self.assertRaisesRegex(MigrationError, "already exists"):
                migrate(root)
            self.assertEqual(list((root / ".astrolabe").iterdir()), [])

    def test_symlink_rejected_without_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_project(root)
            (root / ".rpi" / "link").symlink_to("PROJECT.md")
            with self.assertRaisesRegex(MigrationError, "Symlink"):
                migrate(root)
            self.assertFalse((root / ".astrolabe").exists())

    def test_copy_failure_cleans_stage(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_project(root)
            with patch("migrate_rpi_project.shutil.copytree", side_effect=OSError("disk failure")):
                with self.assertRaisesRegex(OSError, "disk failure"):
                    migrate(root)
            self.assertFalse((root / ".astrolabe").exists())
            self.assertEqual(list(root.glob(".astrolabe-migration-*")), [])
            self.assertTrue((root / ".rpi" / "PROJECT.md").exists())

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
