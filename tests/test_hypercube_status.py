import json
from pathlib import Path
import tempfile
import unittest

from hypercube.status import Project, collect, load_watch_list, parse_status


VALID = """---
schema_version: 1
status: active
current_tier: design
current_work: sample-work
last_updated: 2026-09-16T12:00:00+00:00
---
Working on sample.
"""


class StatusTests(unittest.TestCase):
    def test_watch_list_only_registers_explicit_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / "projects.json"
            config.write_text(json.dumps({"projects": [{"name": "One", "path": str(root / "one")}] }))
            self.assertEqual(load_watch_list(config), [Project("One", root / "one")])

    def test_bad_watch_list_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "projects.json"
            for data in ({"projects": [{"name": "x", "path": "/a"}, {"name": "x", "path": "/b"}]},
                         {"projects": [{"name": "x", "path": "relative"}]}, {"projects": "bad"}):
                config.write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    load_watch_list(config)

    def test_schema_fields_and_summary(self):
        fields, summary = parse_status(VALID)
        self.assertEqual(fields, {"schema_version": "1", "status": "active", "current_tier": "design",
                                  "current_work": "sample-work", "last_updated": "2026-09-16T12:00:00+00:00"})
        self.assertEqual(summary, "Working on sample.")

    def test_bad_project_does_not_hide_healthy_project(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            status = root / "good" / ".astrolabe" / "STATUS.md"
            status.parent.mkdir(parents=True)
            status.write_text(VALID)
            projects = [Project("Missing", root / "missing"), Project("Good", root / "good")]
            results = collect(projects)
            self.assertIsNotNone(results[0].error)
            self.assertEqual(results[1].summary, "Working on sample.")
            status.write_text(VALID.replace("schema_version: 1", "schema_version: 2"))
            self.assertIn("Unsupported", collect(projects)[1].error)


if __name__ == "__main__":
    unittest.main()
