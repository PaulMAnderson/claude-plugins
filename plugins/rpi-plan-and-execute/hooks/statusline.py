#!/usr/bin/env python3
import sys
import json
import time
from pathlib import Path

# pattern: Imperative Shell

def update_statusline():
    """Reads context usage and outputs a StatusLine text with a visual bar."""
    try:
        # GATHER: Read input from stdin
        input_data = json.load(sys.stdin)
        
        # PROCESS: Extract used percentage
        # input_data structure: {"context_window": {"used_percentage": 52}}
        used_percentage = input_data.get("context_window", {}).get("used_percentage", 0)
        
        # PERSIST: Write percentage to .rpi/context-usage.json for session-monitor.py
        rpi_dir = Path(".rpi")
        rpi_dir.mkdir(exist_ok=True)
        usage_file = rpi_dir / "context-usage.json"
        with open(usage_file, "w") as f:
            json.dump({
                "used_percentage": used_percentage, 
                "timestamp": time.time()
            }, f)

        # PROCESS: Generate visual bar
        bar_length = 20
        filled_length = int(bar_length * used_percentage // 100)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        
        status_line_text = f"Context: [{bar}] {used_percentage}%"
        
        # OUTPUT: StatusLine hook response
        sys.stdout.write(json.dumps({"statusLineText": status_line_text}))

    except Exception as e:
        # Fail gracefully: don't break the CLI if hook fails
        # Output minimal status line if something goes wrong
        sys.stdout.write(json.dumps({"statusLineText": "Context: [Error tracking usage]"}))

if __name__ == "__main__":
    update_statusline()
