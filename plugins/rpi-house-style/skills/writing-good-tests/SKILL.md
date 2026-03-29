---
name: writing-good-tests
description: Use when writing or reviewing tests - covers test philosophy, condition-based waiting, mocking strategy, and test isolation for scientific computing
user-invocable: false
---

# Writing Good Tests

## Philosophy

**"Write tests. Not too many. Mostly integration."** — adapted from Kent C. Dodds

In scientific computing, tests verify that your analysis produces the correct results and remains reproducible. The goal is confidence in your findings, not just code coverage.

**Core principles:**
1. Test scientific outcomes, not implementation details — refactoring an algorithm shouldn't break its tests if the result is the same.
2. Integration tests (running a full pipeline on a small dataset) provide better confidence than unit testing individual math functions in isolation.
3. Use known-good "gold standard" data for regression testing.
4. Mock strategically — use real data files when feasible, mocks for hardware interfaces or slow database writes.
5. Prioritize reproducibility — ensure tests pass across different environments and versions of libraries (numpy, scipy, etc.).

## Test Structure

Use **Arrange-Act-Assert** (or Given-When-Then):

```python
import numpy as np
from my_analysis import detect_spikes

def test_spike_detection_on_synthetic_data():
    # Arrange: Create a synthetic signal with known spikes
    fs = 1000  # 1kHz
    t = np.linspace(0, 1, fs)
    signal = np.sin(2 * np.pi * 10 * t)  # 10Hz sine wave
    signal[500] = 10  # Insert a spike at 500ms
    threshold = 5

    # Act: Run the detection algorithm
    spike_indices = detect_spikes(signal, threshold)

    # Assert: Verify the spike was detected at the correct index
    assert len(spike_indices) == 1
    assert spike_indices[0] == 500
```

**One scientific question per test.** Multiple assertions are fine if they verify different aspects of the same phenomenon (e.g., spike time and spike amplitude).

## Handling Data Dependencies

### Managed vs Unmanaged Dependencies

In data science, your "dependencies" are often data files or external hardware.

| Dependency Type | Example | Strategy |
|-----------------|---------|----------|
| **Managed** (you control it) | Small test HDF5/MAT files, local MySQL test DB | Use REAL files/instances |
| **Unmanaged** (external) | Live data streams from hardware, remote APIs | Use MOCKS or RECORDED data |

**Rule:** Always prefer using a small, version-controlled "test dataset" over mocking data structures. Real data surfaces edge cases (NaNs, precision issues) that manual mocks often miss.

## Condition-Based Waiting (for Real-time/Async)

If testing async data collection or long-running simulations, don't use arbitrary `sleep()`.

**Wait for conditions, not time:**

```python
import time

def wait_for_condition(condition_func, timeout=5, poll_interval=0.1):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if condition_func():
            return True
        time.sleep(poll_interval)
    raise TimeoutError("Condition not met within timeout")

def test_data_acquisition_starts():
    recorder.start()
    # GOOD: Wait for the buffer to fill
    wait_for_condition(lambda: recorder.buffer_size > 0)
    assert recorder.is_recording
```

## Mocking Strategy

### Don't Mock What You Don't Own

Create thin wrappers around hardware drivers or complex libraries. Mock YOUR wrapper, not the driver.

```python
# BAD: Mocking the low-level NiDAQmx driver directly
# GOOD: Mock your own HighLevelRecorder class

class MyAnalysis:
    def __init__(self, recorder):
        self.recorder = recorder

def test_analysis_starts_recorder():
    mock_recorder = MagicMock()
    analysis = MyAnalysis(mock_recorder)
    analysis.run()
    mock_recorder.start.assert_called_once()
```

### Anti-Pattern: Incomplete Data Mocks

When mocking data structures (like numpy arrays or pandas DataFrames), ensure they have realistic shapes and types.

```python
# BAD: Mocking a signal as a simple list
# GOOD: Using a numpy array with the correct dtype and shape
signal = np.random.randn(10, 1000).astype(np.float32) 
```

## Test Isolation and Cleanup

### What to Clean Up

**Long-lived resources MUST be cleaned up:**
- Temporary data files created during the test
- Database connections or test tables
- Hardware handles or background threads

Use `pytest` fixtures for automated cleanup:

```python
import pytest
import os

@pytest.fixture
def temp_data_file():
    path = "test_data.h5"
    # Setup: create file
    yield path
    # Teardown: delete file
    if os.path.exists(path):
        os.remove(path)

def test_analysis(temp_data_file):
    # Run test using temp_data_file
    ...
```

### What's OK to Leave

**Logs and database records are fine to leave in dedicated test environments.**
- Don't spend effort perfectly cleaning a test MySQL database; just ensure each test uses unique IDs or a fresh schema.

## Quick Reference

| Problem | Fix |
|---------|-----|
| `time.sleep()` in tests | Use `wait_for_condition` |
| Mocking complex math | Use synthetic data with known ground truth |
| Test-only methods in production | Move to `conftest.py` or test utility modules |
| Tests slow due to large files | Create "tiny" versions of your datasets for testing |
| Flaky tests on different machines | Check for floating point precision (use `pytest.approx`) |

## Red Flags

**Stop and reconsider when you see:**
- `time.sleep()` without a specific timing-related reason.
- Mocking `np.ndarray` or `pd.DataFrame` behavior instead of just using small arrays/frames.
- Tests that only pass on one person's machine because of hardcoded paths.
- "Golden" data files that are several gigabytes (should be megabytes).
- `assert a == b` for floating point numbers (use `np.allclose` or `pytest.approx`).

## TDD for Science

TDD helps ensure your analysis is correct before you trust its results:
1. Write a test with a trivial "known" result (e.g., a 10Hz sine wave).
2. Watch the test fail (confirms the test is actually checking the output).
3. Implement the algorithm.
4. Verify the test passes.
5. Add edge cases (NaNs, gaps in data, noise) and refine.
