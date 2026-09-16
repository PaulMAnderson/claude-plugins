"""Observable local state behavior shared by Astrolabe tiers."""
from datetime import datetime
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "plugins/astrolabe-plan-and-execute/scripts/astrolabe-state.py"


class ProjectStateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="astrolabe-state-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def run_cli(self, *args):
        result = subprocess.run([sys.executable, str(CLI), "--root", str(self.root), *args],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_init_is_idempotent_and_creates_valid_files(self):
        self.run_cli("init")
        state = self.root / ".astrolabe"
        for name in ("PROJECT.md", "STATUS.md", "HISTORY.md", "PLANNED.md"):
            self.assertTrue((state / name).is_file(), name)
        self.assertIn("schema_version: 1", (state / "STATUS.md").read_text())
        (state / "PROJECT.md").write_text("# My project\n")
        before = (state / "HISTORY.md").read_text()
        self.run_cli("init")
        self.assertEqual((state / "PROJECT.md").read_text(), "# My project\n")
        self.assertEqual((state / "HISTORY.md").read_text(), before)

    def test_spec_creation_resume_steps_notes_and_completion(self):
        self.run_cli("spec-start", "--work", "sample-spec", "--intent", "Build sample",
                     "--step", "Collect input", "--step", "Write output")
        files = list((self.root / ".astrolabe/docs/specs").glob("*-sample-spec.md"))
        self.assertEqual(len(files), 1)
        path = files[0]
        self.assertIn("status: in_progress", path.read_text())
        self.run_cli("spec-step", "--work", "sample-spec", "--number", "1")
        self.run_cli("spec-note", "--work", "sample-spec", "--text", "Keep this note")
        before = path.read_text()
        self.run_cli("spec-start", "--work", "sample-spec", "--intent", "Changed intent",
                     "--step", "New step")
        self.assertEqual(path.read_text(), before)
        self.assertIn("- [x] 1. Collect input", before)
        self.assertIn("Keep this note", before)
        self.run_cli("spec-step", "--work", "sample-spec", "--number", "2")
        self.run_cli("spec-done", "--work", "sample-spec", "--outcome", "Built sample")
        self.assertIn("status: done", path.read_text())
        self.assertIn("Built sample", (self.root / ".astrolabe/HISTORY.md").read_text())
        completed_status = (self.root / ".astrolabe/STATUS.md").read_text()
        self.assertIn("current_tier: none", completed_status)
        self.assertIn("schema_version: 1", completed_status)
        self.assertIn("current_work: null", completed_status)

    def test_spec_cannot_finish_with_open_steps(self):
        self.run_cli("spec-start", "--work", "open-spec", "--intent", "Track work",
                     "--step", "Unfinished")
        result = subprocess.run([sys.executable, str(CLI), "--root", str(self.root),
                                 "spec-done", "--work", "open-spec", "--outcome", "Done"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("status: done", next((self.root / ".astrolabe/docs/specs").glob("*.md")).read_text())

    def test_planned_ids_are_separate_stable_and_repeat_safe(self):
        self.run_cli("init")
        self.run_cli("add-planned", "--list", "backlog", "--text", "Ship feature")
        self.run_cli("add-planned", "--list", "roadmap", "--text", "Explore dashboard")
        self.run_cli("add-planned", "--list", "backlog", "--text", "Fix importer")
        planned = (self.root / ".astrolabe/PLANNED.md").read_text()
        self.assertIn("- B1: Ship feature", planned)
        self.assertIn("- B2: Fix importer", planned)
        self.assertIn("- R1: Explore dashboard", planned)
        self.assertLess(planned.index("- B2:"), planned.index("## Roadmap"))
        self.assertEqual(planned.count("- B1:"), 1)

    def test_planned_rejects_duplicate_existing_ids(self):
        self.run_cli("init")
        (self.root / ".astrolabe/PLANNED.md").write_text(
            "## Backlog\n- B1: one\n- B1: two\n\n## Roadmap\n")
        result = subprocess.run([sys.executable, str(CLI), "--root", str(self.root),
                                 "add-planned", "--list", "backlog", "--text", "three"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("three", (self.root / ".astrolabe/PLANNED.md").read_text())

    def test_planned_lifecycle_preserves_item_until_completion_and_reserves_id(self):
        self.run_cli("add-planned", "--list", "backlog", "--text", "Ship feature")
        self.run_cli("start-planned", "--id", "B1", "--tier", "spec", "--work", "ship-feature")
        planned = self.root / ".astrolabe/PLANNED.md"
        history = self.root / ".astrolabe/HISTORY.md"
        self.assertIn("- B1: Ship feature", planned.read_text())
        self.assertIn("- Planned-ID: B1", history.read_text())
        self.run_cli("finish", "--tier", "spec", "--work", "ship-feature",
                     "--intent", "Ship feature", "--outcome", "Verified release")
        self.run_cli("complete-planned", "--id", "B1", "--outcome", "Verified release",
                     "--artifact", "docs/release.md")
        self.assertNotIn("- B1:", planned.read_text())
        recorded = history.read_text()
        self.assertIn("- Planned-Item: Ship feature", recorded)
        self.assertIn("- Planned-Status: completed", recorded)
        self.assertIn("- Artifact: docs/release.md", recorded)
        self.run_cli("complete-planned", "--id", "B1", "--outcome", "Verified release")
        self.assertEqual(history.read_text(), recorded)
        self.assertEqual(self.run_cli("add-planned", "--list", "backlog", "--text", "Next" ).strip(), "B2")

    def test_planned_completion_requires_start_and_tier_completion(self):
        self.run_cli("add-planned", "--list", "roadmap", "--text", "Explore dashboard")
        def rejected(*args):
            return subprocess.run([sys.executable, str(CLI), "--root", str(self.root), *args],
                                  capture_output=True, text=True)
        self.assertEqual(rejected("complete-planned", "--id", "R1", "--outcome", "Done").returncode, 2)
        self.run_cli("start-planned", "--id", "R1", "--tier", "quick", "--work", "dashboard")
        self.assertEqual(rejected("complete-planned", "--id", "R1", "--outcome", "Done").returncode, 2)
        self.run_cli("finish", "--tier", "quick", "--work", "dashboard", "--intent", "Explore",
                     "--outcome", "Still investigating", "--status", "paused")
        self.assertEqual(rejected("complete-planned", "--id", "R1", "--outcome", "Done").returncode, 2)
        self.assertIn("- R1:", (self.root / ".astrolabe/PLANNED.md").read_text())

    def test_paused_work_keeps_tier_and_slug(self):
        self.run_cli("enter", "--tier", "spec", "--work", "paused-work")
        self.run_cli("finish", "--tier", "spec", "--work", "paused-work",
                     "--intent", "track steps", "--outcome", "two steps remain",
                     "--status", "paused")
        status = (self.root / ".astrolabe/STATUS.md").read_text()
        self.assertIn("status: paused", status)
        self.assertIn("current_tier: spec", status)
        self.assertIn("current_work: paused-work", status)
        self.assertIn("Paused paused-work", status)

    def test_three_distributions_use_same_local_contract(self):
        helpers = (CLI,
                   ROOT / "gemini/extensions/astrolabe-plan-and-execute/scripts/astrolabe-state.py",
                   ROOT / "codex/skills/astrolabe-workflow/scripts/project_state.py")
        for index, helper in enumerate(helpers):
            project = self.root / f"project-{index}"
            project.mkdir()
            for args in (("init",), ("enter", "--tier", "quick", "--work", "portable"),
                         ("finish", "--tier", "quick", "--work", "portable",
                          "--intent", "local only", "--outcome", "works")):
                result = subprocess.run([sys.executable, str(helper), "--root", str(project), *args],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            status = (project / ".astrolabe/STATUS.md").read_text()
            history = (project / ".astrolabe/HISTORY.md").read_text()
            self.assertIn("schema_version: 1", status)
            self.assertIn("current_tier: none", status)
            self.assertIn("local only", history)
            self.assertIn("works", history)

    def test_status_schema_after_each_tier_exit(self):
        expected = {"schema_version", "status", "current_tier", "current_work", "last_updated"}
        for tier in ("micro", "quick", "spec", "design"):
            self.run_cli("enter", "--tier", tier, "--work", "schema-check")
            self.run_cli("finish", "--tier", tier, "--work", "schema-check",
                         "--intent", "check schema", "--outcome", "passed")
            lines = (self.root / ".astrolabe/STATUS.md").read_text().splitlines()
            self.assertEqual(lines[0], "---")
            self.assertEqual(lines[6], "---")
            self.assertEqual(len(lines), 8)
            fields = dict(line.split(": ", 1) for line in lines[1:6])
            self.assertEqual(set(fields), expected)
            self.assertEqual(fields["schema_version"], "1")
            self.assertEqual(fields["status"], "active")
            self.assertEqual(fields["current_tier"], "none")
            self.assertEqual(fields["current_work"], "null")
            self.assertIsNotNone(datetime.fromisoformat(fields["last_updated"]).tzinfo)
            self.assertTrue(lines[7].startswith("Completed schema-check:"))

    def test_each_tier_updates_status_and_appends_history(self):
        for tier in ("micro", "quick", "spec", "design"):
            self.run_cli("enter", "--tier", tier, "--work", "sample")
            status = (self.root / ".astrolabe/STATUS.md").read_text()
            self.assertIn(f"current_tier: {tier}", status)
            self.assertIn("current_work: sample", status)
            self.run_cli("finish", "--tier", tier, "--work", "sample",
                         "--intent", f"intent-{tier}", "--outcome", f"outcome-{tier}")
            status = (self.root / ".astrolabe/STATUS.md").read_text()
            self.assertIn("current_tier: none", status)
            self.assertIn("current_work: null", status)
        history = (self.root / ".astrolabe/HISTORY.md").read_text()
        for tier in ("micro", "quick", "spec", "design"):
            self.assertIn(f"intent-{tier}", history)
            self.assertIn(f"outcome-{tier}", history)
        self.assertEqual(history.count("### "), 4)


if __name__ == "__main__":
    unittest.main()
