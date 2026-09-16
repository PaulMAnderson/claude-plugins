"""Black-box tests for evidence gates, recovery, and collision-safe installation."""
# pattern: Imperative Shell

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


BUNDLE = Path(__file__).resolve().parents[1]
STATE = BUNDLE / "skills/astrolabe-workflow/scripts/astrolabe_state.py"
INSTALL = BUNDLE / "scripts/install.py"


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="astrolabe-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "plan").mkdir()
        (self.root / "design.md").write_text("Actual design and acceptance criteria\n")
        (self.root / "report.md").write_text("Check command: fixture; exit 0; tested expected behavior\n")
        (self.root / "finding.md").write_text("Boundary value is rejected incorrectly.\nExact value: 17.\n")
        self.call("init", "--design", "design.md", "--plan", "plan", "--phase", "First", "--phase", "Second")

    def call(self, *args, expected=0):
        result = subprocess.run([sys.executable, str(STATE), "--root", str(self.root),
                                 "--run", "test-run", *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def state(self):
        return json.loads((self.root / ".astrolabe/runs/test-run/state.json").read_text())

    def complete(self, name):
        self.call("gate", name, "completed", "--evidence", "report.md")

    def all_complete(self):
        for gate in self.state()["gates"]:
            self.complete(gate["id"])

    def test_cannot_skip_gates_or_evidence(self):
        self.call("gate", "phase:1:execute", "completed", "--evidence", "report.md", expected=2)
        self.call("gate", "design", "completed", expected=2)
        self.call("gate", "design", "completed", "--evidence", "missing.md", expected=2)
        self.assertTrue(all(g["status"] == "pending" for g in self.state()["gates"]))
        self.call("check", expected=1)

    def test_full_multiphase_run_and_cross_process_resume(self):
        self.complete("design")
        self.call("status")
        self.complete("plan")
        for gate in self.state()["gates"][2:]:
            self.call("gate", gate["id"], "in_progress")
            self.complete(gate["id"])
        self.assertIn("PASS", self.call("check").stdout)

    def test_minor_finding_blocks_and_preserves_verbatim_text(self):
        self.complete("design")
        self.call("issue", "R1", "--gate", "plan", "--severity", "Minor", "--text-file", "finding.md")
        self.assertEqual(self.state()["issues"][0]["text"], (self.root / "finding.md").read_text())
        self.call("gate", "plan", "completed", "--evidence", "report.md", expected=2)
        self.call("resolve", "R1", "--disposition", "fixed", "--evidence", "missing.md", expected=2)
        self.call("resolve", "R1", "--disposition", "fixed", "--evidence", "report.md")
        self.complete("plan")

    def test_new_final_finding_invalidates_downstream(self):
        self.all_complete()
        self.call("issue", "R2", "--gate", "final-review", "--severity", "Important", "--text-file", "finding.md")
        self.assertTrue(all(g["status"] == "pending" for g in self.state()["gates"][-3:]))
        self.call("check", expected=1)
        self.call("resolve", "R2", "--disposition", "rejected", "--evidence", "report.md")
        for gate in self.state()["gates"][-3:]:
            self.complete(gate["id"])
        self.call("check")

    def test_changed_or_deleted_evidence_cannot_pass(self):
        self.all_complete()
        (self.root / "report.md").write_text("Changed evidence after completion\n")
        self.assertIn("changed evidence", self.call("check", expected=1).stdout)
        self.call("reopen", "verification", "--reason", "code changed")
        self.call("gate", "verification", "completed", "--evidence", "report.md", expected=2)
        (self.root / "report.md").unlink()
        self.call("check", expected=1)

    def test_reopen_retains_history_and_invalidates_later_work(self):
        self.all_complete()
        self.call("reopen", "phase:1:execute", "--reason", "new contract requirement")
        gates = self.state()["gates"]
        self.assertEqual(gates[2]["status"], "completed")
        self.assertTrue(all(g["status"] == "pending" for g in gates[3:]))
        self.assertTrue(any(e.get("gates", [{}])[-1].get("status") == "completed"
                            for e in self.state()["events"]))

    def test_blocker_requires_reason_and_is_not_success(self):
        self.call("gate", "design", "blocked", expected=2)
        self.call("gate", "design", "blocked", "--reason", "Missing required schema")
        self.assertIn("Missing required schema", self.call("check", expected=1).stdout)
        self.complete("design")

    def test_reinitialization_does_not_erase_progress(self):
        self.complete("design")
        before = self.state()
        self.call("init", "--design", "design.md", "--plan", "plan", "--phase", "New", expected=2)
        self.assertEqual(self.state(), before)

    def test_invalid_evidence_and_run_escape(self):
        (self.root / "empty.md").touch()
        self.call("gate", "design", "completed", "--evidence", "empty.md", expected=2)
        self.call("gate", "design", "completed", "--evidence", str(STATE), expected=2)
        result = subprocess.run([sys.executable, str(STATE), "--root", str(self.root),
                                 "--run", "../escape", "status"], capture_output=True)
        self.assertEqual(result.returncode, 2)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="astrolabe-install-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def install(self, *args, expected=0):
        result = subprocess.run([sys.executable, str(INSTALL), "--project", str(self.root), *args],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_dry_run_and_repeat_symlink_install(self):
        self.install("--dry-run")
        self.assertFalse((self.root / ".agents").exists())
        self.install()
        self.install()
        installed = list((self.root / ".agents/skills").iterdir())
        self.assertEqual(len(installed), 13)
        self.assertTrue(all(p.is_symlink() and (p / "SKILL.md").is_file() for p in installed))

    def test_collision_preflight_makes_no_partial_install(self):
        target = self.root / ".agents/skills/astrolabe-review"
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("User-owned skill\n")
        self.install(expected=2)
        self.assertEqual(list(target.parent.iterdir()), [target])
        self.assertEqual((target / "SKILL.md").read_text(), "User-owned skill\n")

    def test_portable_copy_and_modified_copy_protection(self):
        self.install("--copy")
        self.install("--copy")
        skills = self.root / ".agents/skills"
        self.assertFalse((skills / "astrolabe-workflow").is_symlink())
        result = subprocess.run([sys.executable, str(skills / "astrolabe-workflow/scripts/astrolabe_state.py"),
                                 "--help"], capture_output=True)
        self.assertEqual(result.returncode, 0)
        for path in skills.iterdir():
            self.assertTrue((path / "LICENSE").is_file())
        (skills / "astrolabe-design/SKILL.md").write_text("User edited copy\n")
        self.install("--copy", expected=2)


if __name__ == "__main__":
    unittest.main()
