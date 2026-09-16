"""Watch-list validation and Astrolabe status collection."""

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re


@dataclass(frozen=True)
class Project:
    name: str
    path: Path


@dataclass(frozen=True)
class Result:
    project: Project
    fields: dict[str, str | None] | None
    summary: str | None
    error: str | None


def load_watch_list(path: Path) -> list[Project]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read watch list: {exc}") from exc
    if not isinstance(data, dict) or set(data) != {"projects"} or not isinstance(data["projects"], list):
        raise ValueError("Watch list must contain a projects array")
    projects = []
    names = set()
    for index, item in enumerate(data["projects"]):
        if not isinstance(item, dict) or set(item) != {"name", "path"}:
            raise ValueError(f"Project {index} must have name and path")
        name, raw_path = item["name"], item["path"]
        if not isinstance(name, str) or not name.strip() or not isinstance(raw_path, str) or not Path(raw_path).is_absolute():
            raise ValueError(f"Project {index} needs a nonempty name and absolute path")
        if name in names:
            raise ValueError(f"Duplicate project name: {name}")
        names.add(name)
        projects.append(Project(name, Path(raw_path)))
    return projects


def parse_status(text: str) -> tuple[dict[str, str | None], str]:
    lines = text.splitlines()
    if len(lines) < 8 or lines[0] != "---":
        raise ValueError("Invalid STATUS.md frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("Invalid STATUS.md frontmatter") from exc
    fields: dict[str, str | None] = {}
    for line in lines[1:end]:
        key, separator, value = line.partition(": ")
        if not separator or key in fields:
            raise ValueError("Invalid STATUS.md field")
        fields[key] = None if value == "null" else value
    if set(fields) != {"schema_version", "status", "current_tier", "current_work", "last_updated"}:
        raise ValueError("Invalid STATUS.md fields")
    if fields["schema_version"] != "1":
        raise ValueError("Unsupported STATUS.md schema version")
    if fields["status"] not in {"active", "paused", "archived"}:
        raise ValueError("Invalid status")
    if fields["current_tier"] not in {"none", "micro", "quick", "spec", "design"}:
        raise ValueError("Invalid current tier")
    work = fields["current_work"]
    if work is not None and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", work):
        raise ValueError("Invalid current work")
    try:
        updated = fields["last_updated"]
        if updated is None or datetime.fromisoformat(updated).tzinfo is None:
            raise ValueError
    except ValueError as exc:
        raise ValueError("Invalid last updated timestamp") from exc
    body = lines[end + 1:]
    if len(body) != 1 or not body[0].strip():
        raise ValueError("STATUS.md needs one summary line")
    return fields, body[0]


def collect(projects: list[Project]) -> list[Result]:
    results = []
    for project in projects:
        try:
            text = (project.path / ".astrolabe" / "STATUS.md").read_text(encoding="utf-8")
            fields, summary = parse_status(text)
            results.append(Result(project, fields, summary, None))
        except (OSError, UnicodeError, ValueError) as exc:
            results.append(Result(project, None, None, f"Cannot read valid status: {exc}"))
    return results
