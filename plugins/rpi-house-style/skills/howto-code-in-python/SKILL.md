---
name: howto-code-in-python
description: Use when writing or reviewing Python code for data science and neuroscience - covers NumPy/SciPy/Pandas idioms, type hints, virtual environments, and plotting conventions
user-invocable: false
---

# Python House Style

## Overview

**Core principle:** Prioritize readability, reproducibility, and performant array operations. Python is the primary language for modern data science and neuroscience analysis; follow idiomatic patterns to ensure your code is maintainable by others.

**Why this matters:** Scientific code often suffers from "scripting sprawl." Using modular patterns, type hints, and vectorization makes analysis reproducible and less prone to subtle math errors.

## NumPy and Vectorization

### Prefer Vectorization Over Loops

**NumPy's power comes from vectorization.** Avoid `for` loops when operating on arrays.

```python
import numpy as np

# BAD: Explicit loop (slow)
def threshold_loop(signal, threshold):
    results = []
    for x in signal:
        if x > threshold:
            results.append(x)
    return np.array(results)

# GOOD: Vectorized operation (fast)
def threshold_vectorized(signal, threshold):
    return signal[signal > threshold]
```

### Explicit Array Shape Handling

Always document and validate array shapes. In neuroscience, standard dimensions are often `[channels, time]` or `[trials, channels, time]`.

**Technique: Named Dimension Indices**

```python
# GOOD: Using constants for dimension indices
CHANNELS = 0
TIME = 1

def baseline_correct(data, baseline_samples):
    baseline = np.mean(data[:, :baseline_samples], axis=TIME, keepdims=True)
    return data - baseline
```

### Broadcasting Rules

Understand and use broadcasting to perform operations between arrays of different shapes without explicit tiles/repeats.

```python
# Example: Normalize each channel by its own max
# data: [channels, time]
# maxes: [channels, 1]
maxes = np.max(data, axis=1, keepdims=True)
normalized = data / maxes  # Broadcasting handles the expansion
```

## Type Hints and Annotation

### Use Type Hints for Clarity

Modern Python (3.9+) supports rich type hints. Use them for all function signatures.

```python
from typing import Annotated, Literal
import numpy as np
from numpy.typing import NDArray

# Using Annotated to specify units or expected shapes
SignalArray = Annotated[NDArray[np.float64], "Shape: [channels, samples], Unit: uV"]

def bandpass_filter(
    data: SignalArray, 
    low_freq: float, 
    high_freq: float, 
    fs: int
) -> SignalArray:
    ...
```

## Project Structure

### Analysis Scripts vs. Local Packages

**Analysis Scripts (.py):** Linear, figure-focused, uses `if __name__ == "__main__":` blocks. Should reside in a `scripts/` or `notebooks/` directory.

**Local Packages (src/):** Modular, reusable logic. If an analysis function is used in more than two scripts, move it to a package.

### Configuration Management

Don't hardcode paths or parameters. Use environment variables or configuration files (YAML/JSON).

```python
import os
from pathlib import Path

DATA_DIR = Path(os.getenv("DATA_ROOT", "./data"))
SESSION_PATH = DATA_DIR / "session_001.h5"
```

## Plotting and Visualization

### Matplotlib Object-Oriented API

Prefer the OO API (`fig, ax = plt.subplots()`) over the state-based API (`plt.plot()`). It's more robust for complex subplots and figure customization.

```python
import matplotlib.pyplot as plt

def plot_evoked_response(time, signal, title):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(time, signal, color='navy', linewidth=1.5)
    ax.set_title(title)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude (uV)")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return fig
```

## Reproducibility

### Virtual Environments

**ALWAYS use a virtual environment.** Never install packages globally.
- `python -m venv .venv`
- `conda create -n my-env python=3.11`

**Pin your dependencies:**
- Use `requirements.txt` (`pip freeze > requirements.txt`)
- Or `pyproject.toml` (recommended for modern projects)

## Property-Based Testing with Hypothesis

Use the `hypothesis` library to find edge cases in your math and data processing logic.

```python
from hypothesis import given, strategies as st
import numpy as np

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_mean_within_bounds(data_list):
    data = np.array(data_list)
    result = np.mean(data)
    assert np.min(data) <= result <= np.max(data)
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `for` loops over NumPy arrays | Use vectorized operations |
| Hardcoded paths | Use `pathlib` and environment variables |
| Missing `axis` parameter in NumPy functions | Always specify `axis` explicitly |
| Using `plt.plot()` globally | Use `ax.plot()` from the OO API |
| Installing packages with `pip install` without a venv | Use `venv` or `conda` |
| `from module import *` | Use explicit imports: `from module import function` |

## Red Flags

**Stop and refactor when you see:**
- `for i in range(len(array)):`
- `try: ... except: pass` (swallowing all exceptions)
- Global variables being mutated inside functions
- Functions longer than 50 lines that mix I/O and calculation (violation of FCIS)
- Variable names like `data1`, `data2`, `x`, `y` without context
