import os
import re

files = [
    "gemini/extensions/rpi-plan-and-execute/skills/writing-design-plans/SKILL.md",
    "gemini/extensions/rpi-plan-and-execute/skills/starting-a-design-plan/SKILL.md",
    "gemini/extensions/rpi-plan-and-execute/skills/brainstorming/SKILL.md",
    "gemini/extensions/rpi-plan-and-execute/skills/executing-an-implementation-plan/SKILL.md",
    "gemini/extensions/rpi-plan-and-execute/skills/using-plan-and-execute/SKILL.md",
    "gemini/extensions/rpi-plan-and-execute/skills/requesting-code-review/SKILL.md",
    "gemini/extensions/rpi-plan-and-execute/skills/finishing-a-development-branch/SKILL.md",
    "gemini/extensions/rpi-extending-claude/skills/writing-skills/SKILL.md",
    "gemini/extensions/rpi-extending-claude/skills/creating-an-agent/SKILL.md",
    "gemini/extensions/rpi-extending-claude/skills/writing-claude-directives/SKILL.md"
]

for path in files:
    if not os.path.exists(path):
        print(f"Skipping {path} (not found)")
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Rule 1: Replace 'Skill tool' with 'activate_skill'
    content = content.replace("Skill tool", "activate_skill tool")

    # Rule 2: Replace 'AskUserQuestion' with 'ask_user'
    content = content.replace("AskUserQuestion", "ask_user")

    # Rule 3: Replace Task logic
    content = re.sub(r'TaskCreate', 'write_todos', content)
    content = re.sub(r'TaskUpdate', 'write_todos', content)
    content = re.sub(r'addBlockedBy', 'write_todos', content)
    content = re.sub(r'TaskList', 'write_todos', content)

    # Rule 4: Update any hardcoded paths to plugins/ to be relative
    content = re.sub(r'plugins/[a-zA-Z0-9_-]+/skills/[a-zA-Z0-9_-]+/REFERENCE\.md', './REFERENCE.md', content)
    content = re.sub(r'plugins/[a-zA-Z0-9_-]+/scripts/monitor\.py', '../../scripts/monitor.py', content)

    # Rule 5: Ensure YAML frontmatter is correctly closed with '---'
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            pass # already has closing ---
        else:
            # Invalid frontmatter?
            # E.g.
            # ---
            # name: my-skill
            # # content
            # Let's fix this by finding the first # or blank line after the first ---
            # Actually, usually they forgot the closing ---
            lines = content.split('\n')
            new_lines = []
            in_frontmatter = True
            for i, line in enumerate(lines):
                if i == 0 and line == '---':
                    new_lines.append(line)
                    continue
                if in_frontmatter and (line.startswith('#') or line.startswith(' ')):
                    if not lines[i-1] == '---' and not '---' in lines[i-1]:
                        # Insert closing ---
                        new_lines.append('---')
                    in_frontmatter = False
                new_lines.append(line)

            # Re-check if we closed it properly
            content = '\n'.join(new_lines)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Processed {path}")
