import os
import re

files = [
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

    # Rule 3: Replace Task Create logic
    content = re.sub(r'TaskCreate', 'write_todos', content)
    content = re.sub(r'TaskUpdate', 'write_todos', content)
    content = re.sub(r'addBlockedBy', 'write_todos', content)
    content = re.sub(r'TaskList', 'write_todos', content)

    # Let's fix YAML frontmatter correctly
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            pass
        else:
            # Invalid frontmatter?
            pass

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Processed {path}")
