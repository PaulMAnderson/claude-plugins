---
name: defense-in-depth
description: Use when invalid data causes failures deep in execution - validates at every layer data passes through to make bugs structurally impossible rather than temporarily fixed
user-invocable: false
---

# Defense-in-Depth Validation

## Overview

When you fix a bug caused by invalid data (e.g., mismatched array shapes or unexpected NaNs in a signal), adding validation at one place feels sufficient. But that single check can be bypassed by different code paths, refactoring, or intermediate data processing steps.

**Core principle:** Validate at EVERY layer data passes through. Make the bug structurally impossible.

## When to Use

**Use when:**
- Invalid data (mismatched shapes, NaNs, incorrect sampling rate) caused a bug deep in the analysis pipeline
- Data crosses system boundaries (File → Analysis → Database)
- Multiple analysis paths can reach the same vulnerable algorithm
- Tests mock data loading (bypassing initial validation)

**Don't use when:**
- Pure internal function with a single caller (validate at caller)
- Data already validated by a library you trust (e.g., numpy's internal checks)
- Adding validation would duplicate identical checks at immediately adjacent layers

## The Four Layers

### Layer 1: Entry Point Validation
**Purpose:** Reject invalid input at the system boundary (e.g., data loading).

```python
import os
import h5py

def load_signal_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    with h5py.File(file_path, 'r') as f:
        if 'raw_signal' not in f:
            raise KeyError(f"Missing 'raw_signal' dataset in {file_path}")
        
        signal = f['raw_signal'][:]
        
        # Layer 1: Basic shape and type check
        if signal.ndim != 2:
            raise ValueError(f"Expected 2D array [channels, samples], got {signal.ndim}D")
            
    return signal
```

**When needed:** Always. This is your first line of defense.

### Layer 2: Business/Analysis Logic Validation
**Purpose:** Ensure data makes sense for a specific scientific operation.

```python
import numpy as np

def compute_psd(signal, fs):
    # Layer 2: Analysis-specific validation
    if fs <= 0:
        raise ValueError(f"Sampling frequency must be positive, got {fs}")
    
    if np.isnan(signal).any():
        raise ValueError("Signal contains NaNs; clean data before computing PSD")
        
    if signal.shape[0] > signal.shape[1]:
        # Heuristic: usually more samples than channels
        logger.warning(f"Array shape {signal.shape} suggests [samples, channels] orientation")
    
    # ... proceed with FFT
```

**When needed:** When analysis rules differ from entry validation, or when intermediate steps might have corrupted the data.

### Layer 3: Environment/Safety Guards
**Purpose:** Prevent dangerous or nonsensical operations in specific contexts.

```python
def TX_save_analysis_results(db, results, session_id):
    # Layer 3: Environment/Context guard
    # Ensure we aren't overwriting production data during a dry run or test
    if os.getenv('ANALYSIS_MODE') == 'dry-run':
        logger.info(f"DRY RUN: skipping save for session {session_id}")
        return

    # Ensure results aren't empty or nonsensical before database write
    if not results or 'metrics' not in results:
        raise ValueError(f"Refusing to save empty results for session {session_id}")
        
    # ... proceed with DB transaction
```

**When needed:** When an operation is destructive (overwriting files) or irreversible (database writes).

### Layer 4: Debug Instrumentation
**Purpose:** Capture context for forensics when other layers fail.

```python
def align_timestamps(signal_a, signal_b, timestamps_a, timestamps_b):
    # Layer 4: Capture context for debugging misalignment
    logger.debug("Aligning signals", extra={
        "shape_a": signal_a.shape,
        "shape_b": signal_b.shape,
        "ts_range_a": [timestamps_a[0], timestamps_a[-1]],
        "ts_range_b": [timestamps_b[0], timestamps_b[-1]],
    })
    
    # ... alignment logic
```

**When needed:** When debugging is difficult (e.g., jitter or drift issues), or when you need to trace how inconsistent data arrived.

## Decision Heuristic

| Situation | Layers Needed |
|-----------|---------------|
| Loading a single CSV file | 1 only |
| Multi-stage analysis pipeline | 1 + 2 |
| Writing results to a central database | 1 + 2 + 3 |
| Chasing a rare synchronization bug | 1 + 2 + 3 + 4 |
| Analysis functions used in multiple pipelines | At minimum: 2 |

## Applying the Pattern

When you find a bug caused by invalid data:

1. **Trace the data flow** - Where does the bad signal/metadata originate? Where is it used?
2. **Map checkpoints** - List every function/layer the data passes through (Load → Filter → Feature Extract → Save).
3. **Decide which layers** - Use the heuristic above.
4. **Add validation** - Entry → Analysis logic → Environment → Debug.
5. **Test each layer** - Verify Layer 2 catches what bypasses Layer 1 (e.g., if Layer 1 only checks file existence, Layer 2 should check array dimensions).

## Quick Reference

| Layer | Question It Answers | Typical Check |
|-------|---------------------|---------------|
| Entry | Is the file/input valid? | File exists, dataset present, correct type |
| Analysis | Does the data make sense here? | No NaNs, positive FS, correct array shape |
| Environment | Is this safe in this context? | Dry-run check, results not empty, correct DB permissions |
| Debug | How did we get here? | Log array shapes, timestamp ranges, stack trace |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| One validation point, call it done | Add at least entry + analysis layers |
| Identical checks at adjacent layers | Make each layer check something different (e.g., Layer 1: shape, Layer 2: content/NaNs) |
| Environment guards only in prod | Add them in test too (prevent test pollution/overwrites) |
| Hardcoding indices without validation | Validate shape before accessing `data[0, :]` |
| Validation but no useful error message | Include the bad shape/value and the expected format in the error |

## Key Insight

In scientific computing, each layer catches bugs the others miss:
- Different data formats bypass entry validation.
- Intermediate processing (e.g., filtering) can introduce NaNs or change array shapes.
- Edge cases in hardware (e.g., dropped packets) need environment guards.
- Debug logging identifies where in a long pipeline the data went "bad".

**Don't stop at one validation point.** The bug isn't fixed until it's impossible.
