#!/usr/bin/env python3
"""Validate the bundle's portable metadata, references, and source coverage."""
# pattern: Imperative Shell

import ast
import hashlib
import json
from pathlib import Path
import re
import sys


def validate(bundle):
    errors = []
    skills = bundle / "skills"
    names = set()
    # Metadata uses a deliberately small YAML subset: JSON-quoted scalar strings.
    # General-purpose YAML authoring can also use the official skill validator.
    for folder in sorted(skills.iterdir()):
        path = folder / "SKILL.md"
        if not path.is_file():
            errors.append(f"missing skill entrypoint: {folder}")
            continue
        text = path.read_text()
        try:
            header = text.split("---\n", 2)[1]
            fields = {k: json.loads(v) for k, v in
                      (line.split(": ", 1) for line in header.strip().splitlines())}
            assert set(fields) == {"name", "description"}
            assert fields["name"] == folder.name and fields["name"] not in names
            assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", fields["name"])
            assert len(fields["name"]) <= 64 and 1 <= len(fields["description"]) <= 1024
            names.add(fields["name"])
        except (ValueError, IndexError, AssertionError):
            errors.append(f"invalid skill metadata: {path}")
        metadata = folder / "agents/openai.yaml"
        try:
            values = {k.strip(): json.loads(v) for k, v in
                      (line.strip().split(": ", 1) for line in metadata.read_text().splitlines()[1:])}
            assert 25 <= len(values["short_description"]) <= 64
            assert "$" + folder.name in values["default_prompt"]
        except (OSError, ValueError, KeyError, AssertionError):
            errors.append(f"invalid UI metadata: {metadata}")
        for required in ("LICENSE", "LICENSE.superpowers", "NOTICE.md"):
            if not (folder / required).is_file():
                errors.append(f"missing attribution: {folder / required}")
        for document in folder.rglob("*.md"):
            content = document.read_text()
            for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
                if re.match(r"https?://|#", link):
                    continue
                target = (document.parent / link.split("#")[0]).resolve()
                if not target.exists() or not target.is_relative_to(skills.resolve()):
                    errors.append(f"broken/nonportable link in {document}: {link}")
            if document.name != "NOTICE.md" and re.search(
                    r"TaskCreate|TaskUpdate|AskUserQuestion|activate_skill|write_todos|CLAUDE_PLUGIN_ROOT|\$\{extensionPath\}|<invoke", content):
                errors.append(f"unported runtime instruction: {document}")
    for script in bundle.rglob("*.py"):
        try:
            ast.parse(script.read_text(), filename=str(script))
        except SyntaxError as error:
            errors.append(str(error))
    manifest = json.loads((bundle / "source-map.json").read_text())
    repo = bundle.parent
    expected = {str(p.relative_to(repo)) for tree in ("plugins", "gemini/extensions")
                for p in (repo / tree).rglob("*") if p.is_file() and
                (p.name == "SKILL.md" or p.parent.name in ("commands", "agents", "hooks", "scripts"))}
    recorded = {entry["source"] for entry in manifest["entries"]}
    if expected != recorded:
        errors.append(f"source inventory changed: missing={sorted(expected-recorded)}, stale={sorted(recorded-expected)}")
    for entry in manifest["entries"]:
        source = repo / entry["source"]
        if source.is_file() and hashlib.sha256(source.read_bytes()).hexdigest() != entry["sha256"]:
            errors.append(f"source changed; inspect/update its port: {entry['source']}")
        if entry["target"] not in names:
            errors.append(f"missing target for {entry['source']}: {entry['target']}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"PASS: {len(names)} skills; metadata, local links, Python syntax, licenses, and {len(recorded)} source mappings")
    return 0


if __name__ == "__main__":
    sys.exit(validate(Path(__file__).resolve().parents[1]))
