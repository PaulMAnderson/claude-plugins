#!/usr/bin/env python3
"""Durable, single-controller Astrolabe gate and issue ledger (Python standard library)."""
# pattern: Imperative Shell

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from datetime import datetime, timezone


def timestamp():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def evidence(root, value):
    path = Path(value).expanduser()
    path = (root / path).resolve() if not path.is_absolute() else path.resolve()
    if not path.is_relative_to(root):
        raise ValueError("evidence must be inside the project so the run remains portable")
    if not path.is_file() or not path.stat().st_size:
        raise ValueError(f"evidence is missing or empty: {path}")
    return {"path": str(path.relative_to(root)),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def verify_evidence(root, record):
    try:
        return evidence(root, record["path"]) == record
    except (OSError, ValueError, KeyError):
        return False


def save(path, state):
    state["updated_at"] = timestamp()
    # Replace atomically: a failed write must leave the previous ledger readable.
    fd, temporary = tempfile.mkstemp(prefix=".state-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(state, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def gate_index(state, name):
    for index, gate in enumerate(state["gates"]):
        if gate["id"] == name:
            return index
    raise ValueError(f"unknown gate: {name}")


def invalidate(state, index, reason):
    for gate in state["gates"][index:]:
        gate.update(status="pending", evidence=[], reason="")
    state["events"].append({"at": timestamp(), "action": "reopen",
                            "gate": state["gates"][index]["id"], "reason": reason})


def prerequisites(state, root, index):
    for gate in state["gates"][:index]:
        if gate["status"] != "completed":
            raise ValueError(f"prerequisite incomplete: {gate['id']}")
        if not gate["evidence"] or not all(verify_evidence(root, e) for e in gate["evidence"]):
            raise ValueError(f"prerequisite evidence missing or changed: {gate['id']}; reopen it")


def inspect(state, root):
    problems = []
    for gate in state["gates"]:
        if gate["status"] != "completed":
            problems.append(f"{gate['id']}: {gate['status']}" +
                            (f" ({gate['reason']})" if gate["reason"] else ""))
        elif not gate["evidence"] or not all(verify_evidence(root, e) for e in gate["evidence"]):
            problems.append(f"{gate['id']}: missing or changed evidence; reopen gate")
    for issue in state["issues"]:
        if issue["status"] == "open":
            problems.append(f"{issue['id']} [{issue['severity']}]: unresolved")
        elif not verify_evidence(root, issue["resolution_evidence"]):
            problems.append(f"{issue['id']}: resolution evidence missing or changed")
    return problems


def parser():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--root", required=True, type=Path, help="Target project/worktree")
    cli.add_argument("--run", required=True, help="Unique lowercase run slug")
    commands = cli.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="Create a run; never overwrite existing progress")
    init.add_argument("--design", required=True)
    init.add_argument("--plan", required=True, help="Existing implementation plan directory")
    init.add_argument("--phase", action="append", required=True, help="Phase title; repeat in dependency order")
    gate = commands.add_parser("gate", help="Record a gate transition")
    gate.add_argument("name", help="design, plan, phase:N:read/execute/review, final-review, coverage, verification")
    gate.add_argument("status", choices=["in_progress", "completed", "blocked"])
    gate.add_argument("--evidence", action="append", default=[], help="Nonempty immutable report/artifact file")
    gate.add_argument("--reason", default="")
    reopen = commands.add_parser("reopen", help="Invalidate a gate and all downstream gates")
    reopen.add_argument("name")
    reopen.add_argument("--reason", required=True)
    issue = commands.add_parser("issue", help="Register a verbatim finding; reopen its gate if completed")
    issue.add_argument("id")
    issue.add_argument("--gate", required=True)
    issue.add_argument("--severity", required=True, choices=["Critical", "Important", "Minor"])
    issue.add_argument("--text-file", required=True, help="Finding text copied verbatim into the ledger")
    resolve = commands.add_parser("resolve", help="Record explicit re-review evidence for a finding")
    resolve.add_argument("id")
    resolve.add_argument("--disposition", required=True, choices=["fixed", "rejected"])
    resolve.add_argument("--evidence", required=True)
    commands.add_parser("status", help="Show progress without changing it")
    commands.add_parser("check", help="Exit 1 unless all gates and issues have intact evidence")
    return cli


def run(args):
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"project does not exist: {root}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.run):
        raise ValueError("run must be a lowercase alphanumeric/hyphen slug")
    directory = (root / ".astrolabe" / "runs" / args.run).resolve()
    if not directory.is_relative_to(root):
        raise ValueError("run directory must remain inside project (check symlinks)")
    path = directory / "state.json"
    if path.is_symlink():
        raise ValueError("state.json must not be a symlink")

    if args.command == "init":
        if path.exists():
            raise ValueError("run already exists; use status/reopen, or choose a new slug")
        design = evidence(root, args.design)
        plan = (root / args.plan).resolve()
        if not plan.is_dir() or not plan.is_relative_to(root):
            raise ValueError("plan must be an existing directory inside project")
        if any(not title.strip() for title in args.phase):
            raise ValueError("phase titles must not be empty")
        names = ["design", "plan"]
        names += [f"phase:{n}:{step}" for n in range(1, len(args.phase) + 1)
                  for step in ("read", "execute", "review")]
        names += ["final-review", "coverage", "verification"]
        state = {"schema_version": 1, "run": args.run, "created_at": timestamp(),
                 "design": design["path"], "plan": str(plan.relative_to(root)),
                 "phases": args.phase, "issues": [], "events": [],
                 "gates": [{"id": name, "status": "pending", "evidence": [], "reason": ""}
                           for name in names]}
        directory.mkdir(parents=True, exist_ok=True)
    else:
        if not path.is_file():
            raise ValueError(f"run not initialized: {path}")
        state = json.loads(path.read_text(encoding="utf-8"))
        if state.get("schema_version") != 1 or state.get("run") != args.run:
            raise ValueError("unsupported or mismatched ledger; do not overwrite it")

    if args.command in ("status", "check"):
        complete = sum(g["status"] == "completed" for g in state["gates"])
        print(f"{args.run}: {complete}/{len(state['gates'])} gates completed")
        problems = inspect(state, root)
        print("\n".join(problems) if problems else "PASS: all gates and recorded evidence intact")
        return int(bool(problems)) if args.command == "check" else 0

    if args.command == "gate":
        index = gate_index(state, args.name)
        gate = state["gates"][index]
        if gate["status"] == "completed":
            raise ValueError("gate already completed; use reopen to invalidate downstream evidence")
        if args.status != "blocked":
            prerequisites(state, root, index)
        if args.status == "completed":
            if not args.evidence:
                raise ValueError("completion requires --evidence")
            if any(i["status"] == "open" and gate_index(state, i["gate"]) <= index
                   for i in state["issues"]):
                raise ValueError("unresolved issues block this gate")
        if args.status == "blocked" and not args.reason.strip():
            raise ValueError("blocked status requires --reason")
        gate.update(status=args.status, evidence=[evidence(root, e) for e in args.evidence], reason=args.reason)
    elif args.command == "reopen":
        if not args.reason.strip():
            raise ValueError("reopen requires a concrete reason")
        invalidate(state, gate_index(state, args.name), args.reason)
    elif args.command == "issue":
        index = gate_index(state, args.gate)
        if any(i["id"] == args.id for i in state["issues"]):
            raise ValueError("issue ID already exists; use a new ID for a recurrence")
        record = evidence(root, args.text_file)
        state["issues"].append({"id": args.id, "gate": args.gate, "severity": args.severity,
                                "text": (root / record["path"]).read_text(encoding="utf-8"), "status": "open"})
        if state["gates"][index]["status"] == "completed":
            invalidate(state, index, f"new finding: {args.id}")
    elif args.command == "resolve":
        issue = next((i for i in state["issues"] if i["id"] == args.id), None)
        if issue is None or issue["status"] != "open":
            raise ValueError("issue is missing or already resolved")
        issue.update(status=args.disposition, resolution_evidence=evidence(root, args.evidence))

    # Snapshot transitions in event history so reopening never erases prior evidence.
    state["events"].append({"at": timestamp(), "action": args.command,
                            "gates": json.loads(json.dumps(state["gates"])),
                            "issues": json.loads(json.dumps(state["issues"]))})
    save(path, state)
    print(path)
    return 0


def main(argv=None):
    try:
        return run(parser().parse_args(argv))
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"astrolabe-state: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
