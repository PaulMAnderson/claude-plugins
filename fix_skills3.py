import os
import re
import glob

# Find all SKILL.md files
files = glob.glob("gemini/extensions/*/skills/*/SKILL.md")

for path in files:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content

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
    content = re.sub(r'plugins/[a-zA-Z0-9_-]+/', '../../', content) # general fallback? No, let's be careful.

    # Let's manually replace the known remaining ones:
    content = content.replace('plugins/rpi-plan-and-execute/scripts/monitor.py', '../../scripts/monitor.py')
    content = content.replace('plugins/rpi-extending-claude/.claude-plugin/plugin.json', '../../.claude-plugin/plugin.json')
    content = content.replace('plugins/<name>/.claude-plugin/plugin.json', '../../.claude-plugin/plugin.json')
    content = content.replace('./plugins/my-plugin', './my-plugin')

    # Rule 5: Ensure YAML frontmatter is correctly closed with '---'
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            pass # already has closing ---
        else:
            lines = content.split('\n')
            new_lines = []
            in_frontmatter = True
            for i, line in enumerate(lines):
                if i == 0 and line == '---':
                    new_lines.append(line)
                    continue
                if in_frontmatter and (line.startswith('#') or line.startswith(' ') or line == ''):
                    if not lines[i-1] == '---' and not '---' in lines[i-1]:
                        # Insert closing ---
                        new_lines.append('---')
                    in_frontmatter = False
                new_lines.append(line)
            content = '\n'.join(new_lines)

    if content != original_content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Processed {path}")
    else:
        print(f"No changes {path}")
