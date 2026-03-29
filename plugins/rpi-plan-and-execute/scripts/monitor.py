#!/usr/bin/env python3
"""
Workspace Monitor: Scans /Users/paul/Claude/ to classify projects into lifecycle phases
and generates a central DASHBOARD.md.
"""

import os
import json
from pathlib import Path
from datetime import datetime

# pattern: Imperative Shell

CLAUDE_ROOT = Path("/Users/paul/Claude/")
MONITOR_DIR = CLAUDE_ROOT / ".monitor"
DASHBOARD_FILE = CLAUDE_ROOT / "DASHBOARD.md"

LIFECYCLE_PHASES = {
    "empty": "Empty",
    "scaffold": "Scaffold",
    "static-complete": "Static Complete",
    "design": "Design",
    "design-complete": "Design Complete",
    "implementing": "Implementing",
    "active": "Active",
    "upstream-sync": "Upstream Sync",
    "maintenance": "Maintenance",
    "unknown": "Unknown"
}

def classify_project(project_path: Path):
    """Classifies a project into a lifecycle phase based on its files."""
    try:
        # GATHER: Check for indicators
        has_readme = (project_path / "README.md").exists()
        has_package_json = (project_path / "package.json").exists()
        has_design_plans = list((project_path / "docs" / "design-plans").glob("*.md")) if (project_path / "docs" / "design-plans").exists() else []
        has_implementation_plans = list((project_path / "docs" / "implementation-plans").glob("**/phase_*.md")) if (project_path / "docs" / "implementation-plans").exists() else []
        has_todos = (project_path / ".rpi" / "todos").exists()
        
        # PROCESS: Classification logic
        if not has_readme and not has_package_json:
            return "empty"
        
        if has_implementation_plans:
            return "implementing"
        
        if has_design_plans:
            # Check if all design plans are complete (simplified: any active design)
            return "design"
            
        if has_todos:
            return "active"
            
        if has_readme:
            return "static-complete"
            
        return "unknown"
    except Exception:
        return "unknown"

def scan_workspace():
    """Scans the workspace and updates the dashboard."""
    if not CLAUDE_ROOT.exists():
        return

    MONITOR_DIR.mkdir(exist_ok=True)
    
    projects = []
    
    # GATHER: Scan directories
    for item in CLAUDE_ROOT.iterdir():
        if not item.is_dir():
            continue
        
        # EXCLUDE: Hidden dirs and the monitor dir itself
        if item.name.startswith('.') or item.name == "Monitor":
            continue
        
        phase_key = classify_project(item)
        phase_display = LIFECYCLE_PHASES.get(phase_key, "Unknown")
        
        project_data = {
            "name": item.name,
            "path": str(item),
            "phase": phase_key,
            "last_monitored": datetime.now().isoformat()
        }
        
        # PERSIST: Write project stub
        stub_file = MONITOR_DIR / f"{item.name}.json"
        with open(stub_file, "w") as f:
            json.dump(project_data, f, indent=2)
            
        projects.append(project_data)
        
    # PERSIST: Generate DASHBOARD.md
    projects.sort(key=lambda x: x['name'])
    
    dashboard_content = f"# Claude Workspace Dashboard\n\n"
    dashboard_content += f"_Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n\n"
    dashboard_content += "| Project | Lifecycle Phase | Path |\n"
    dashboard_content += "|---------|-----------------|------|\n"
    
    for p in projects:
        phase = LIFECYCLE_PHASES.get(p['phase'], "Unknown")
        dashboard_content += f"| {p['name']} | {phase} | `{p['path']}` |\n"
        
    with open(DASHBOARD_FILE, "w") as f:
        f.write(dashboard_content)

if __name__ == "__main__":
    scan_workspace()
