import json
from pathlib import Path
import tempfile
import unittest

from hypercube.status import Project, collect, load_watch_list, parse_status
from hypercube.web import render


VALID = """---
schema_version: 1
status: active
current_tier: design
current_work: sample-work
last_updated: 2026-09-16T12:00:00+00:00
---
Working on sample.
"""

# One malformed fixture per distinct `raise ValueError` branch in parse_status.
MALFORMED_STATUS_CASES = {
    "too_short": (
        "---\nschema_version: 1\n",
        "Invalid STATUS.md frontmatter",
    ),
    "missing_opening_delimiter": (
        "===\n"
        "schema_version: 1\n"
        "status: active\n"
        "current_tier: design\n"
        "current_work: sample-work\n"
        "last_updated: 2026-09-16T12:00:00+00:00\n"
        "---\n"
        "Working on sample.\n",
        "Invalid STATUS.md frontmatter",
    ),
    "missing_closing_delimiter": (
        "---\n"
        "schema_version: 1\n"
        "status: active\n"
        "current_tier: design\n"
        "current_work: sample-work\n"
        "last_updated: 2026-09-16T12:00:00+00:00\n"
        "===\n"
        "Working on sample.\n",
        "Invalid STATUS.md frontmatter",
    ),
    "malformed_field_line": (
        "---\n"
        "schema_version: 1\n"
        "status active\n"
        "current_tier: design\n"
        "current_work: sample-work\n"
        "last_updated: 2026-09-16T12:00:00+00:00\n"
        "---\n"
        "Working on sample.\n",
        "Invalid STATUS.md field",
    ),
    "duplicate_field_key": (
        # All five required keys are present exactly once each in the *set*
        # sense (current_tier is repeated with the same value), so if the
        # duplicate-key check were ever removed, the dict would end up with
        # a complete, valid field set and parse_status would raise nothing
        # at all -- the subTest would then correctly fail via assertRaises,
        # rather than silently passing through the wrong-field-set branch.
        "---\n"
        "schema_version: 1\n"
        "status: active\n"
        "current_tier: design\n"
        "current_tier: design\n"
        "current_work: sample-work\n"
        "last_updated: 2026-09-16T12:00:00+00:00\n"
        "---\n"
        "Working on sample.\n",
        "Invalid STATUS.md field",
    ),
    "wrong_field_set": (
        "---\n"
        "schema_version: 1\n"
        "status: active\n"
        "current_tier: design\n"
        "extra_field: sample-work\n"
        "last_updated: 2026-09-16T12:00:00+00:00\n"
        "---\n"
        "Working on sample.\n",
        "Invalid STATUS.md fields",
    ),
    "bad_schema_version": (
        VALID.replace("schema_version: 1", "schema_version: 2"),
        "Unsupported STATUS.md schema version",
    ),
    "bad_status_value": (
        VALID.replace("status: active", "status: bogus"),
        "Invalid status",
    ),
    "bad_tier_value": (
        VALID.replace("current_tier: design", "current_tier: bogus"),
        "Invalid current tier",
    ),
    "bad_work_slug": (
        VALID.replace("current_work: sample-work", "current_work: Not_Valid"),
        "Invalid current work",
    ),
    "naive_timestamp": (
        VALID.replace(
            "last_updated: 2026-09-16T12:00:00+00:00",
            "last_updated: 2026-09-16T12:00:00",
        ),
        "Invalid last updated timestamp",
    ),
    "unparseable_timestamp": (
        VALID.replace(
            "last_updated: 2026-09-16T12:00:00+00:00",
            "last_updated: not-a-timestamp",
        ),
        "Invalid last updated timestamp",
    ),
    "empty_body": (
        "---\n"
        "schema_version: 1\n"
        "status: active\n"
        "current_tier: design\n"
        "current_work: sample-work\n"
        "last_updated: 2026-09-16T12:00:00+00:00\n"
        "---\n"
        "\n",
        "STATUS.md needs one summary line",
    ),
    "multiline_body": (
        VALID.replace("Working on sample.\n", "Working on sample.\nSecond line.\n"),
        "STATUS.md needs one summary line",
    ),
}


class StatusTests(unittest.TestCase):
    def test_watch_list_only_registers_explicit_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            listed_status = root / "listed" / ".astrolabe" / "STATUS.md"
            listed_status.parent.mkdir(parents=True)
            listed_status.write_text(VALID)
            unlisted_status = root / "unlisted" / ".astrolabe" / "STATUS.md"
            unlisted_status.parent.mkdir(parents=True)
            unlisted_status.write_text(VALID)

            config = root / "projects.json"
            config.write_text(json.dumps({"projects": [{"name": "Listed", "path": str(root / "listed")}]}))

            projects = load_watch_list(config)
            self.assertEqual(projects, [Project("Listed", root / "listed")])

            results = collect(projects)
            self.assertEqual(len(results), 1)

            page = render(projects)
            self.assertNotIn("Unlisted", page)
            self.assertNotIn(str(root / "unlisted"), page)

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

    def test_parse_status_rejects_each_malformed_case(self):
        for case_name, (text, expected_message) in MALFORMED_STATUS_CASES.items():
            with self.subTest(case=case_name):
                with self.assertRaises(ValueError) as ctx:
                    parse_status(text)
                # Exact match, not assertIn: "Invalid STATUS.md field" (a
                # malformed/duplicate field line) is a literal string prefix
                # of "Invalid STATUS.md fields" (the wrong-field-set branch),
                # so a substring check could pass even when the exception
                # came from the wrong branch entirely.
                self.assertEqual(str(ctx.exception), expected_message)

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

    def test_unreadable_status_file_is_a_per_project_error(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            good_status = root / "good" / ".astrolabe" / "STATUS.md"
            good_status.parent.mkdir(parents=True)
            good_status.write_text(VALID)

            bad_status = root / "bad" / ".astrolabe" / "STATUS.md"
            bad_status.parent.mkdir(parents=True)
            # Invalid UTF-8: 0xff is never a valid UTF-8 lead byte.
            bad_status.write_bytes(b"\xff\xfe\x00\x01invalid")

            projects = [Project("Bad", root / "bad"), Project("Good", root / "good")]
            results = collect(projects)

            self.assertIsNotNone(results[0].error)
            self.assertIsNone(results[0].fields)
            self.assertEqual(results[1].summary, "Working on sample.")


if __name__ == "__main__":
    unittest.main()
