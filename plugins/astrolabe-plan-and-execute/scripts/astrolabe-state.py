#!/usr/bin/env python3
"""Create and update local Astrolabe project state."""
# pattern: Imperative Shell

import argparse
import contextlib
from datetime import datetime, timezone
import fcntl
from pathlib import Path
import re
import sys

TIERS = ("none", "micro", "quick", "spec", "design")
STATUSES = ("active", "paused", "archived")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PLANNED_STATUS_COMPLETED = re.compile(r"(?m)^- Planned-Status: completed$")
PLANNED_STATUS_STARTED = re.compile(r"(?m)^- Planned-Status: started$")
RESULT_COMPLETED = re.compile(r"(?m)^- Result: completed$")
STRUCTURED_FIELD_LINE = re.compile(r"(?m)^\s*-\s*(Planned-\w+|Tier|Work|Result|Outcome|Artifact):")


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def validate_work(value):
    if value and not SLUG.fullmatch(value):
        raise ValueError("work must be a lowercase hyphenated slug")
    return value


def state_dir(root):
    return root / ".astrolabe"


def atomic_write(path, text):
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


@contextlib.contextmanager
def locked(directory):
    """Serialize read-modify-write sequences against concurrent invocations."""
    lock_path = directory / ".lock"
    with lock_path.open("a") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def status_text(status="active", tier="none", work=None, message="Ready for local work."):
    if tier not in TIERS or status not in STATUSES:
        raise ValueError("invalid status or tier")
    validate_work(work)
    if "\n" in message or "\r" in message:
        raise ValueError("status message must be one line")
    return ("---\n"
            "schema_version: 1\n"
            f"status: {status}\n"
            f"current_tier: {tier}\n"
            f"current_work: {work if work else 'null'}\n"
            f"last_updated: {now()}\n"
            "---\n"
            f"{message}\n")


def initialize(root):
    directory = state_dir(root)
    directory.mkdir(parents=True, exist_ok=True)
    defaults = {
        "PROJECT.md": "# Project\n\nDescribe this project here.\n",
        "STATUS.md": status_text(),
        "HISTORY.md": "# History\n\n",
        "PLANNED.md": "# Planned Work\n\n## Backlog\n\n## Roadmap\n",
    }
    for name, content in defaults.items():
        try:
            with (directory / name).open("x", encoding="utf-8") as stream:
                stream.write(content)
        except FileExistsError:
            pass
    return directory


def write_status(root, *, status="active", tier="none", work=None, message="Ready for local work."):
    directory = initialize(root)
    atomic_write(directory / "STATUS.md", status_text(status, tier, work, message))


def history_value(value):
    value = value.strip()
    if not value:
        raise ValueError("intent and outcome must be nonempty")
    return " ".join(value.splitlines())


def planned_entry(root, item_id):
    if not re.fullmatch(r"[BR][1-9]\d*", item_id):
        raise ValueError("planned ID must be Bn or Rn")
    target = initialize(root) / "PLANNED.md"
    content = target.read_text(encoding="utf-8")
    matches = list(re.finditer(rf"(?m)^- {item_id}: (.+)$", content))
    if len(matches) != 1:
        raise ValueError(f"expected exactly one planned item {item_id}")
    return target, content, matches[0]


def planned_events(root, item_id):
    content = (initialize(root) / "HISTORY.md").read_text(encoding="utf-8")
    return [block for block in re.split(r"(?m)(?=^### )", content)
            if f"- Planned-ID: {item_id}\n" in block]


def start_planned(root, item_id, tier, work):
    validate_work(work)
    if not work:
        raise ValueError("work slug must be nonempty")
    if tier not in TIERS[1:]:
        raise ValueError("invalid tier")
    _, _, match = planned_entry(root, item_id)
    item = match.group(1).strip()
    events = planned_events(root, item_id)
    if any(PLANNED_STATUS_COMPLETED.search(event) for event in events):
        raise ValueError(f"planned item {item_id} is already completed")
    if events:
        work_line = re.compile(rf"(?m)^- Work: {re.escape(work)}$")
        tier_line = re.compile(rf"(?m)^- Tier: {re.escape(tier)}$")
        if not any(PLANNED_STATUS_STARTED.search(event) and
                   work_line.search(event) and tier_line.search(event)
                   for event in events):
            raise ValueError(f"planned item {item_id} is already started with another work or tier")
        return item
    with (state_dir(root) / "HISTORY.md").open("a", encoding="utf-8") as stream:
        stream.write(f"### {now()} — planned — {work}\n\n"
                     f"- Planned-ID: {item_id}\n- Planned-Item: {item}\n"
                     f"- Planned-Status: started\n- Tier: {tier}\n- Work: {work}\n\n")
    write_status(root, tier=tier, work=work, message=f"Working on {item_id}: {item}")
    return item


def complete_planned(root, item_id, outcome, artifact=None):
    outcome = history_value(outcome)
    artifact = history_value(artifact) if artifact else None
    if not re.fullmatch(r"[BR][1-9]\d*", item_id):
        raise ValueError("planned ID must be Bn or Rn")
    directory = initialize(root)
    # The entire read -> decide -> write sequence must be serialized against
    # add_planned (and against other complete_planned calls), since both
    # mutate PLANNED.md via read-modify-write: without this lock, a
    # concurrent add-planned can read PLANNED.md before this function's
    # write lands and then overwrite it, silently losing the newly added
    # item (or resurrecting an item this call just removed).
    with locked(directory):
        events = planned_events(root, item_id)
        completed = any(PLANNED_STATUS_COMPLETED.search(event) for event in events)
        target = directory / "PLANNED.md"
        content = target.read_text(encoding="utf-8")
        if completed and not re.search(rf"(?m)^- {item_id}: ", content):
            return
        target, content, match = planned_entry(root, item_id)
        started = [event for event in events if PLANNED_STATUS_STARTED.search(event)]
        if len(started) != 1:
            raise ValueError(f"planned item {item_id} must be started exactly once")
        tier = re.search(r"(?m)^- Tier: (.+)$", started[0]).group(1)
        work = re.search(r"(?m)^- Work: (.+)$", started[0]).group(1)
        history = (directory / "HISTORY.md").read_text(encoding="utf-8")
        status = (directory / "STATUS.md").read_text(encoding="utf-8")
        if re.search(r"(?m)^status: paused$", status) and f"current_work: {work}\n" in status:
            raise ValueError(f"work {work} is paused")
        completed_tier = any(f" — {tier} — {work}\n" in block and RESULT_COMPLETED.search(block)
                             for block in re.split(r"(?m)(?=^### )", history))
        if not completed_tier and not completed:
            raise ValueError(f"finish {tier} work {work} before completing {item_id}")
        if not completed:
            item = match.group(1).strip()
            with (directory / "HISTORY.md").open("a", encoding="utf-8") as stream:
                stream.write(f"### {now()} — planned — {work}\n\n"
                             f"- Planned-ID: {item_id}\n- Planned-Item: {item}\n"
                             f"- Planned-Status: completed\n- Tier: {tier}\n- Work: {work}\n"
                             f"- Outcome: {outcome}\n"
                             + (f"- Artifact: {artifact}\n" if artifact else "") + "\n")
        line_end = match.end() + (content[match.end():].startswith("\n"))
        atomic_write(target, content[:match.start()] + content[line_end:])


def add_planned(root, list_name, text):
    if STRUCTURED_FIELD_LINE.search(text):
        raise ValueError("planned item text must not contain structured field lines")
    text = history_value(text)
    if ":" in text[:3]:
        raise ValueError("planned item text must not begin with an ID")
    prefix, heading = ("B", "Backlog") if list_name == "backlog" else ("R", "Roadmap")
    directory = initialize(root)
    target = directory / "PLANNED.md"
    with locked(directory):
        content = target.read_text(encoding="utf-8")
        lines = content.splitlines(keepends=True)
        ids = re.findall(r"(?m)^- ([BR]\d+):", content)
        if len(ids) != len(set(ids)):
            raise ValueError("PLANNED.md has duplicate IDs")
        past_ids = re.findall(r"(?m)^- Planned-ID: ([BR]\d+)$",
                              (directory / "HISTORY.md").read_text(encoding="utf-8"))
        ids_for_list = [int(value[1:]) for value in ids + past_ids if value.startswith(prefix)]
        next_id = f"{prefix}{max(ids_for_list, default=0) + 1}"
        heading_line = f"## {heading}"
        try:
            start = next(i for i, line in enumerate(lines) if line.strip() == heading_line)
        except StopIteration:
            raise ValueError(f"PLANNED.md is missing {heading_line}") from None
        end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
        while end > start + 1 and not lines[end - 1].strip():
            end -= 1
        lines.insert(end, f"- {next_id}: {text}\n")
        atomic_write(target, "".join(lines))
    return next_id


def spec_path(root, work, create=False):
    validate_work(work)
    directory = state_dir(root) / "docs" / "specs"
    if create:
        directory.mkdir(parents=True, exist_ok=True)
    matches = sorted(directory.glob(f"????-??-??-{work}.md")) if directory.exists() else []
    if matches:
        return matches[-1]
    if not create:
        raise ValueError(f"no spec found for {work}")
    return directory / f"{datetime.now().astimezone().date().isoformat()}-{work}.md"


def spec_start(root, work, intent, steps):
    intent = history_value(intent)
    if not steps:
        raise ValueError("spec needs at least one step")
    path = spec_path(root, work, create=True)
    if path.exists():
        if "status: done" in path.read_text(encoding="utf-8"):
            raise ValueError("spec is already done")
    else:
        clean_steps = [history_value(step) for step in steps]
        body = ("---\nstatus: in_progress\ntier: spec\n---\n\n"
                f"# {work}\n\n## Intent\n\n{intent}\n\n## Steps\n\n"
                + "".join(f"- [ ] {i}. {step}\n" for i, step in enumerate(clean_steps, 1))
                + "\n## Notes\n\n")
        atomic_write(path, body)
    write_status(root, tier="spec", work=work, message=f"Tracking spec {work}.")
    return path


def spec_step(root, work, number):
    path = spec_path(root, work)
    content = path.read_text(encoding="utf-8")
    if "status: done" in content:
        raise ValueError("spec is already done")
    pattern = re.compile(rf"(?m)^- \[ \] {number}\. ")
    updated, count = pattern.subn(f"- [x] {number}. ", content)
    if count != 1:
        raise ValueError(f"open step {number} not found")
    atomic_write(path, updated)
    return path


def spec_note(root, work, note):
    path = spec_path(root, work)
    content = path.read_text(encoding="utf-8")
    if "status: done" in content:
        raise ValueError("spec is already done")
    with path.open("a", encoding="utf-8") as stream:
        stream.write(f"- {history_value(note)}\n")
    return path


def record_outcome(root, tier, work, intent, outcome, status="active"):
    directory = initialize(root)
    intent = history_value(intent)
    outcome = history_value(outcome)
    validate_work(work)
    with (directory / "HISTORY.md").open("a", encoding="utf-8") as stream:
        stream.write(f"### {now()} — {tier} — {work}\n\n"
                     f"- Intent: {intent}\n- Outcome: {outcome}\n"
                     f"- Result: {'paused' if status == 'paused' else 'completed'}\n\n")
    write_status(root, status=status, tier=tier if status == "paused" else "none",
                 work=work if status == "paused" else None,
                 message=f"{'Paused' if status == 'paused' else 'Completed'} {work}: {outcome}")


def spec_done(root, work, outcome):
    path = spec_path(root, work)
    content = path.read_text(encoding="utf-8")
    if "status: done" in content:
        raise ValueError("spec is already done")
    if re.search(r"(?m)^- \[ \] \d+\. ", content):
        raise ValueError("spec has open steps")
    match = re.search(r"(?s)## Intent\n\n(.*?)\n\n## Steps", content)
    if not match:
        raise ValueError("spec intent is missing")
    outcome = history_value(outcome)
    atomic_write(path, content.replace("status: in_progress", "status: done", 1))
    record_outcome(root, "spec", work, match.group(1), outcome)
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init")
    enter = commands.add_parser("enter")
    enter.add_argument("--tier", choices=TIERS[1:], required=True)
    enter.add_argument("--work", required=True)
    spec_start_parser = commands.add_parser("spec-start")
    spec_start_parser.add_argument("--work", required=True)
    spec_start_parser.add_argument("--intent", required=True)
    spec_start_parser.add_argument("--step", action="append", required=True)
    spec_step_parser = commands.add_parser("spec-step")
    spec_step_parser.add_argument("--work", required=True)
    spec_step_parser.add_argument("--number", type=int, required=True)
    spec_note_parser = commands.add_parser("spec-note")
    spec_note_parser.add_argument("--work", required=True)
    spec_note_parser.add_argument("--text", required=True)
    spec_done_parser = commands.add_parser("spec-done")
    spec_done_parser.add_argument("--work", required=True)
    spec_done_parser.add_argument("--outcome", required=True)
    planned = commands.add_parser("add-planned")
    planned.add_argument("--list", choices=("backlog", "roadmap"), required=True)
    planned.add_argument("--text", required=True)
    start = commands.add_parser("start-planned")
    start.add_argument("--id", required=True)
    start.add_argument("--tier", choices=TIERS[1:], required=True)
    start.add_argument("--work", required=True)
    complete = commands.add_parser("complete-planned")
    complete.add_argument("--id", required=True)
    complete.add_argument("--outcome", required=True)
    complete.add_argument("--artifact")
    finish = commands.add_parser("finish")
    finish.add_argument("--tier", choices=TIERS[1:], required=True)
    finish.add_argument("--work", required=True)
    finish.add_argument("--intent", required=True)
    finish.add_argument("--outcome", required=True)
    finish.add_argument("--status", choices=STATUSES, default="active")
    args = parser.parse_args()
    try:
        directory = initialize(args.root.expanduser().resolve())
        if args.command == "spec-start":
            print(spec_start(args.root.expanduser().resolve(), args.work, args.intent, args.step))
        elif args.command == "spec-step":
            print(spec_step(args.root.expanduser().resolve(), args.work, args.number))
        elif args.command == "spec-note":
            print(spec_note(args.root.expanduser().resolve(), args.work, args.text))
        elif args.command == "spec-done":
            print(spec_done(args.root.expanduser().resolve(), args.work, args.outcome))
        elif args.command == "add-planned":
            print(add_planned(args.root.expanduser().resolve(), args.list, args.text))
        elif args.command == "start-planned":
            print(start_planned(args.root.expanduser().resolve(), args.id, args.tier, args.work))
        elif args.command == "complete-planned":
            complete_planned(args.root.expanduser().resolve(), args.id, args.outcome, args.artifact)
        elif args.command == "enter":
            validate_work(args.work)
            write_status(args.root.expanduser().resolve(), tier=args.tier, work=args.work,
                         message=f"Working on {args.work}.")
        elif args.command == "finish":
            validate_work(args.work)
            record_outcome(args.root.expanduser().resolve(), args.tier, args.work,
                           args.intent, args.outcome, args.status)
        return 0
    except (OSError, ValueError) as error:
        print(f"astrolabe-state: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
