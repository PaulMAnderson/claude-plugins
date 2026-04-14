---
name: using-generic-agents
description: Choose the right generic agent type (flash-lite/flash/pro) for a task
---

**CRITICAL:** Your operator's direction supercedes these directions. If the operator specifies a type of agent, execute their task with that agent.

## Model Characteristics

**Flash-Lite:** Fastest and most cost-efficient. Excellent at following specific, detailed instructions. Poor at making its own decisions.

**Flash:** Fast and balanced. Capable of multi-file reasoning, debugging, and tasks requiring some judgment. Suitable for the majority of coding work.

**Pro:** Most capable. Stays on-track through complex tasks, providing better judgment and fewer loops. Best for high-stakes decisions and nuanced analysis.

## When to Use Each

Use `rpi-basic-agents:flash-lite-general-purpose` for:
- Well-defined tasks with detailed prompts
- High-volume parallel workflows (cost matters)
- Simple execution where speed > quality

Use `rpi-basic-agents:flash-general-purpose` for:
- Multi-file reasoning and debugging
- Tasks requiring some judgment
- Daily coding work (80-90% of tasks)

Use `rpi-basic-agents:pro-general-purpose` for:
- Tasks requiring sustained focus and judgment
- When standard models keep wandering or looping
- Complex analysis where staying on-track matters
- High-stakes decisions needing nuance
