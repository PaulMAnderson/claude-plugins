# RPI House Style Context

This extension provides coding standards, patterns, and writing guidelines for RPI projects. It covers architectural patterns (FCIS), language-specific house styles, database conventions, and technical writing guidance.

## Repository context

This extension defines:
- **Coding patterns** — FCIS (Functional Core, Imperative Shell) and other architectural patterns
- **Language styles** — Reference guides for Python, MATLAB, R, and MySQL
- **Writing standards** — Technical writing conventions for documentation and code comments

### What makes good context

- YAML frontmatter is not used in GEMINI.md
- Valid UTF-8 encoding throughout — use ASCII arrows (`->`), ASCII quotes, ASCII apostrophes
- Concise content — every token competes with conversation history
- Descriptions that are concrete and trigger-focused

### Core patterns

The FCIS pattern (Functional Core, Imperative Shell) is mandatory for all application code. See the section below for complete details.

---

## Coding effectively

When writing or refactoring any code, apply these principles. The FCIS and defense-in-depth sections below are always required. Language-specific sections apply when relevant.

### Property-driven design

When designing features, think about properties upfront. This surfaces design gaps early.

| Question | Property type | Example |
|----------|---------------|---------|
| Does it have an inverse operation? | Roundtrip | `decode(encode(x)) == x` |
| Is applying it twice the same as once? | Idempotence | `f(f(x)) == f(x)` |
| What quantities are preserved? | Invariants | Array shape, sum, count unchanged |
| Is order of arguments irrelevant? | Commutativity | `f(a, b) == f(b, a)` |
| Can operations be regrouped? | Associativity | `f(f(a,b), c) == f(a, f(b,c))` |
| Is there a neutral element? | Identity | `f(x, 0) == x` |
| Is there a reference implementation? | Oracle | `new(x) == old(x)` |
| Can output be easily verified? | Easy to verify | `is_sorted(sort(x))` |

Common design questions these reveal:
- "How should we handle NaNs in the signal data?"
- "What happens if the sample rates don't match?"
- "Is the array order [channels, samples] or [samples, channels]?"
- "Stable filter or not? Edge effect handling?"

Surface these during design, not during debugging.

### Core engineering principles

**Correctness over convenience.** Model the full error space. No shortcuts.

- Handle all edge cases: race conditions, timing issues, partial failures
- Use the type system (or schema) to encode correctness constraints
- Prefer explicit validation over implicit assumptions
- When uncertain, explore and iterate rather than assume

Do not simplify error handling to save time. Do not ignore edge cases because "they probably won't happen". Do not use loose types (like `any` in Python type hints) to bypass checks.

**Error handling — two-tier model:**

1. **User-facing errors**: Semantic exit codes, rich diagnostics, actionable messages
2. **Internal errors**: Programming errors that may panic or use internal types

**Error message format:** Lowercase sentence fragments for "failed to {message}".

```
Good: failed to connect to database: connection refused
Bad:  Failed to Connect to Database: Connection Refused

Good: invalid configuration: missing required field 'apiKey'
Bad:  Invalid Configuration: Missing Required Field 'apiKey'
```

Lowercase fragments compose naturally: `"operation failed: " + error.message` reads correctly.

**Pragmatic incrementalism:**

- Prefer specific, composable logic over abstract frameworks
- Evolve design incrementally rather than perfect upfront architecture
- Don't build for hypothetical future requirements
- Document design decisions and trade-offs when making non-obvious choices

The rule of three applies to abstraction: don't abstract until you've seen the pattern three times. Three similar lines of code is better than a premature abstraction.

### File organization

**Descriptive file names over catch-all files.** Name files by what they contain, not by generic categories.

Don't create: `utils.py`, `helpers.m`, `common.R`, `misc.py`

Do create: `signal_processing.py`, `spike_sorting.py`, `data_io.py`, `array_validation.py`

When tempted to create `utils.py`: stop. Ask what the functions have in common. Name the file after that commonality.

Module organization:
- Keep module boundaries strict with restricted visibility
- Platform-specific code in separate files: `unix.py`, `windows.py`
- Use runtime checks for platform branching
- Test helpers in dedicated modules/files, not mixed with production code

### Cross-platform principles

Don't emulate Unix on Windows or vice versa. Use each platform's native patterns. When platform differences are significant, use separate files:

```
process_spawn.py         # Shared interface and logic
process_spawn_unix.py    # Unix-specific implementation
process_spawn_windows.py # Windows-specific implementation
```

Document platform differences in comments when behavior differs. CI should run on all supported platforms.

### Common mistakes

| Mistake | Reality | Fix |
|---------|---------|-----|
| "Just put it in utils for now" | utils.py becomes 2000 lines of unrelated code | Name files by purpose from the start |
| "Edge cases are rare" | Edge cases cause production incidents | Handle them. Model the full error space. |
| "We might need this abstraction later" | Premature abstraction is harder to remove than add | Wait for the third use case |
| "It works on my Mac" | It may not work on Windows or Linux | Test on target platforms |
| "Array shape is always [time, channels]" | Someone will eventually pass [channels, time] | Validate array shapes explicitly |
| "NaNs won't propagate that far" | NaNs will contaminate your entire analysis pipeline | Check for and handle NaNs early |

### Red flags

Stop and refactor when you see:
- A `utils.py` or `helpers.m` file growing beyond 200 lines
- Error handling that swallows errors or uses generic messages
- Platform-specific code mixed with cross-platform code
- Abstractions created for single use cases
- Hardcoded array dimension indices (e.g., `data[0, :]`) without context
- Code that "works on my machine" but isn't tested cross-platform

---

## Defense-in-depth validation

When invalid data causes failures deep in execution, validate at every layer data passes through to make bugs structurally impossible rather than temporarily fixed.

### Overview

When you fix a bug caused by invalid data (e.g., mismatched array shapes or unexpected NaNs in a signal), adding validation at one place feels sufficient. But that single check can be bypassed by different code paths, refactoring, or intermediate data processing steps.

**Core principle:** Validate at EVERY layer data passes through. Make the bug structurally impossible.

### When to use

Use when:
- Invalid data (mismatched shapes, NaNs, incorrect sampling rate) caused a bug deep in the analysis pipeline
- Data crosses system boundaries (File -> Analysis -> Database)
- Multiple analysis paths can reach the same vulnerable algorithm
- Tests mock data loading (bypassing initial validation)

Don't use when:
- Pure internal function with a single caller (validate at caller)
- Data already validated by a library you trust (e.g., numpy's internal checks)
- Adding validation would duplicate identical checks at immediately adjacent layers

### The four layers

**Layer 1: Entry point validation.** Reject invalid input at the system boundary (e.g., data loading). When needed: always. This is your first line of defense.

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

        if signal.ndim != 2:
            raise ValueError(f"Expected 2D array [channels, samples], got {signal.ndim}D")

    return signal
```

**Layer 2: Business/analysis logic validation.** Ensure data makes sense for a specific scientific operation. When needed: when analysis rules differ from entry validation, or when intermediate steps might have corrupted the data.

```python
import numpy as np

def compute_psd(signal, fs):
    if fs <= 0:
        raise ValueError(f"Sampling frequency must be positive, got {fs}")

    if np.isnan(signal).any():
        raise ValueError("Signal contains NaNs; clean data before computing PSD")

    if signal.shape[0] > signal.shape[1]:
        logger.warning(f"Array shape {signal.shape} suggests [samples, channels] orientation")

    # ... proceed with FFT
```

**Layer 3: Environment/safety guards.** Prevent dangerous or nonsensical operations in specific contexts. When needed: when an operation is destructive (overwriting files) or irreversible (database writes).

```python
def TX_save_analysis_results(db, results, session_id):
    if os.getenv('ANALYSIS_MODE') == 'dry-run':
        logger.info(f"DRY RUN: skipping save for session {session_id}")
        return

    if not results or 'metrics' not in results:
        raise ValueError(f"Refusing to save empty results for session {session_id}")

    # ... proceed with DB transaction
```

**Layer 4: Debug instrumentation.** Capture context for forensics when other layers fail. When needed: when debugging is difficult (e.g., jitter or drift issues), or when you need to trace how inconsistent data arrived.

```python
def align_timestamps(signal_a, signal_b, timestamps_a, timestamps_b):
    logger.debug("Aligning signals", extra={
        "shape_a": signal_a.shape,
        "shape_b": signal_b.shape,
        "ts_range_a": [timestamps_a[0], timestamps_a[-1]],
        "ts_range_b": [timestamps_b[0], timestamps_b[-1]],
    })

    # ... alignment logic
```

### Decision heuristic

| Situation | Layers needed |
|-----------|---------------|
| Loading a single CSV file | 1 only |
| Multi-stage analysis pipeline | 1 + 2 |
| Writing results to a central database | 1 + 2 + 3 |
| Chasing a rare synchronization bug | 1 + 2 + 3 + 4 |
| Analysis functions used in multiple pipelines | At minimum: 2 |

### Applying the pattern

When you find a bug caused by invalid data:

1. **Trace the data flow** — Where does the bad signal/metadata originate? Where is it used?
2. **Map checkpoints** — List every function/layer the data passes through (Load -> Filter -> Feature Extract -> Save).
3. **Decide which layers** — Use the heuristic above.
4. **Add validation** — Entry -> Analysis logic -> Environment -> Debug.
5. **Test each layer** — Verify Layer 2 catches what bypasses Layer 1.

### Common mistakes

| Mistake | Fix |
|---------|-----|
| One validation point, call it done | Add at least entry + analysis layers |
| Identical checks at adjacent layers | Make each layer check something different (e.g., Layer 1: shape, Layer 2: content/NaNs) |
| Environment guards only in prod | Add them in test too (prevent test pollution/overwrites) |
| Hardcoding indices without validation | Validate shape before accessing `data[0, :]` |
| Validation but no useful error message | Include the bad shape/value and the expected format in the error |

**Don't stop at one validation point.** The bug isn't fixed until it's impossible.

---

## Functional core, imperative shell (FCIS)

Separate pure business logic and scientific algorithms (Functional Core) from side effects and I/O (Imperative Shell). Pure functions go in one file, I/O operations (file loading, database queries) in another.

**Why this matters:** Pure functions are trivial to test (no mocks needed) and essential for reproducible science. I/O code is isolated to thin shells. Bugs become structurally impossible when analysis logic has no side effects.

### When to use

Use FCIS when:
- Writing any new code file
- Refactoring existing analysis pipelines
- Reviewing code for architectural decisions
- Deciding where logic belongs

Trigger symptoms:
- "Where should this filter function go?"
- Creating a new file for data processing
- Adding database calls to analysis logic
- Adding file I/O (HDF5/MAT) to calculations
- Writing tests that need complex mocking of the file system

### Mandatory: file classification

Add pattern comment to EVERY file you create or modify:

```
# pattern: Functional Core
# pattern: Imperative Shell
# pattern: Mixed (needs refactoring)
```

If file genuinely cannot be separated (rare), document why:

```
# pattern: Mixed (unavoidable)
# Reason: [specific technical justification]
# Example: Performance-critical path where separating I/O causes unacceptable overhead in a real-time loop
```

No file without classification. If you create code without this comment, you have violated the requirement.

**Do NOT add pattern comments to:** bash/shell scripts, configuration files, markdown documentation, data files. Classification applies ONLY to application code.

### File type definitions

**Functional Core files contain ONLY:**
- Pure functions (same input -> same output, always)
- Analysis logic, signal processing, transformations, statistical tests
- Data structure operations (numpy/pandas manipulations)
- Logging (EXCEPTION: loggers are permitted in Functional Core)

**Functional Core files NEVER contain:**
- File I/O (reading/writing .mat, .h5, .csv files)
- Database operations (queries, updates, connections)
- Network requests
- Environment variable access
- `datetime.now()`, `np.random.rand()`, or other non-deterministic functions
- State mutations outside function scope

**Imperative Shell files contain ONLY:**
- I/O operations: file system (loading datasets), database, environment
- Orchestration: load data -> call Functional Core analysis -> save results
- Error handling for I/O failures (file not found, corrupted data)
- Minimal logic (coordination only)

**Imperative Shell files NEVER contain:**
- Complex analysis algorithms
- Signal processing logic
- Statistical calculations beyond simple aggregation for reporting

### Code flow pattern

```
1. GATHER (Shell):  Load signal data from HDF5/MAT files
2. PROCESS (Core):  Apply filter, detect spikes, calculate metrics (pure)
3. PERSIST (Shell): Save processed results to database or new file
```

Every operation follows this sequence. No exceptions.

### Decision framework

Before writing a function, ask:
- Can this logic run without file system, database, network, or environment?
  - YES -> Functional Core
  - NO -> Does it coordinate I/O or contain analysis logic?
    - I/O coordination -> Imperative Shell
    - Analysis logic + I/O -> STOP. Refactor or escalate.

### Common mistakes and rationalizations

| Excuse/Thought pattern | Reality | What to do |
|------------------------|---------|------------|
| "Just one file read in this calculation" | File I/O = side effect. Not Functional Core. | Extract to Shell. Pass data as parameter. |
| "Database is passed as parameter, so it's pure" | Database operations are I/O. Not pure. | Move to Shell. Core receives data, not DB connection. |
| "This validation needs to check if data file exists" | File system check = I/O. Not Functional Core. | Shell checks file, passes boolean to Core validation. |
| "Need random seed for simulation" | Non-deterministic. Not pure. | Shell passes seed or random generator state as parameter. |
| "Logging is a side effect, should remove" | **WRONG.** Logging is explicitly permitted. | Keep logger. This is the exception. |
| "Performance requires mixing" | Prove it with benchmarks. Usually wrong. | Separate first. Optimize with evidence. Mark Mixed (unavoidable) with justification. |

### Red flags — STOP and refactor

If you catch yourself doing ANY of these, STOP:

- **File I/O in an analysis function** (`h5py.File`, `scipy.io.loadmat`)
- **Database passed as parameter to Functional Core** (queries, updates, connections)
- **Environment variables in calculations** (e.g., setting paths inside a filter)
- **`np.random.seed()` inside a pure algorithm**
- **Creating a file without pattern classification comment**
- **Thinking "just this once" about mixing concerns**

All of these mean: extract I/O to Shell. Pass data to Core. Classify file correctly.

### Implementation patterns

**Functional Core pattern:**

```python
# pattern: Functional Core
import numpy as np

def detect_threshold_crossings(signal, threshold, logger=None):
    """Pure algorithm: same signal and threshold always produce same output."""
    if logger:
        logger.debug(f"Processing signal with shape {signal.shape}")

    crossings = np.where(signal > threshold)[0]

    if logger and len(crossings) > 0:
        logger.info(f"Detected {len(crossings)} crossings")

    return crossings
```

**Imperative Shell pattern:**

```python
# pattern: Imperative Shell
import h5py

def process_session_data(file_path, threshold, db, logger):
    """Orchestrates: gather -> process -> persist."""

    # GATHER: Load data from HDF5 file
    with h5py.File(file_path, 'r') as f:
        signal = f['raw_signal'][:]

    # PROCESS: Call Functional Core (pure logic)
    crossings = detect_threshold_crossings(signal, threshold, logger)

    # PERSIST: Save results to database
    db.save_crossings(file_path, crossings)

    return crossings
```

**FCIS in three rules:**
1. **Functional Core:** Pure functions only. No I/O except logging. Easy to test and reproduce.
2. **Imperative Shell:** I/O coordination only. Minimal logic. Calls Core.
3. **Classify every file.** No exceptions. No files without pattern comments.

---

## MATLAB house style

Use when writing or reviewing MATLAB code for scientific analysis. Covers argument validation, vectorization, OOP for stateful objects, and toolbox organization.

**Core principle:** Use modern MATLAB features (R2019b+) to ensure type safety, modularity, and high-performance matrix operations. MATLAB is the "lingua franca" of many neuroscience labs; follow these standards to prevent "spaghetti scripts" and ensure reproducible results.

### Modern function design

**ALWAYS use `arguments` blocks (R2019b+) for input type, shape, and value checking.**

```matlab
% GOOD: Explicit validation
function filtered = applyFilter(signal, fs, options)
    arguments
        signal (1,:) double {mustBeReal, mustBeFinite}
        fs (1,1) double {mustBePositive}
        options.Type string {mustBeMember(options.Type, ["low", "high", "band"])} = "low"
    end
    % Logic here
end

% BAD: No validation or manual 'nargin' checks
function filtered = applyFilter(signal, fs)
    if nargin < 2, error('Missing fs'); end
    % ...
end
```

Scripts share the base workspace and can cause naming collisions. Use functions to encapsulate variables. Use Live Scripts (.mlx) only for interactive exploration and documentation.

### Vectorization and performance

Avoid `for` loops where matrix operations are possible. MATLAB is highly optimized for these.

```matlab
% BAD: Manual loop
for i = 1:size(data, 1)
    results(i) = sum(data(i, :));
end

% GOOD: Vectorized sum
results = sum(data, 2);
```

If you must use a loop, **always** preallocate your arrays to avoid the "growing array" performance penalty.

```matlab
% GOOD: Preallocate with zeros or NaN
n = 1000;
data = zeros(n, 1);
for i = 1:n
    data(i) = computeValue(i);
end
```

### Toolbox and project organization

Use the `+` prefix to create packages and avoid cluttering the global path:

```
+analysis/
    +signal/
        bandpass.m
    +spike/
        detect.m
```

Call as: `analysis.signal.bandpass(data, 1000)`

Use `private/` directories for helper functions that should only be accessible within a specific package or folder.

**Never use `global` variables.** Use classes, structs, or pass data explicitly.

### Object-oriented programming

Use **Handle Classes** for experimental sessions, hardware interfaces, or processing pipelines where state must be preserved.

```matlab
classdef SessionManager < handle
    properties
        Data
        SamplingRate
    end

    methods
        function obj = SessionManager(filePath)
            obj.Data = load(filePath);
        end

        function process(obj)
            obj.Data = obj.Data * 2;
        end
    end
end
```

- **Handle Classes:** Mutated in place (like Python objects). Use for things that represent "entities."
- **Value Classes:** Copy-on-write (like structs). Use for pure data containers.

### Common mistakes

| Mistake | Fix |
|---------|-----|
| Using `clear all` or `close all` inside functions | Never do this; it's disruptive to the user |
| Growing an array inside a loop | Preallocate with `zeros()` or `NaN()` |
| Not using semicolons | End assignments with `;` to avoid console clutter |
| Hardcoded paths with `\` (Windows) | Use `fullfile()` for cross-platform compatibility |
| Putting everything in the base workspace | Use functions and local variables |
| Using `ans` as a variable name | Assign results to descriptive names |

### Red flags

Stop and refactor when you see:
- Functions with more than 5 input arguments without an `arguments` block
- `eval()` or `assignin()` (security and performance risks)
- `global` variables
- Large `.mat` files without a corresponding README or loading script
- Code that uses `pause(X)` instead of checking for conditions

---

## Python house style

Use when writing or reviewing Python code for data science and neuroscience. Covers NumPy/SciPy/Pandas idioms, type hints, virtual environments, and plotting conventions.

**Core principle:** Prioritize readability, reproducibility, and performant array operations. Python is the primary language for modern data science and neuroscience analysis; follow idiomatic patterns to ensure your code is maintainable by others.

### NumPy and vectorization

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

Always document and validate array shapes. In neuroscience, standard dimensions are often `[channels, time]` or `[trials, channels, time]`.

```python
# GOOD: Using constants for dimension indices
CHANNELS = 0
TIME = 1

def baseline_correct(data, baseline_samples):
    baseline = np.mean(data[:, :baseline_samples], axis=TIME, keepdims=True)
    return data - baseline
```

Understand and use broadcasting to perform operations between arrays of different shapes without explicit tiles/repeats.

### Type hints and annotation

Modern Python (3.9+) supports rich type hints. Use them for all function signatures.

```python
from typing import Annotated
import numpy as np
from numpy.typing import NDArray

SignalArray = Annotated[NDArray[np.float64], "Shape: [channels, samples], Unit: uV"]

def bandpass_filter(
    data: SignalArray,
    low_freq: float,
    high_freq: float,
    fs: int
) -> SignalArray:
    ...
```

### Project structure

**Analysis Scripts (.py):** Linear, figure-focused, uses `if __name__ == "__main__":` blocks. Should reside in a `scripts/` or `notebooks/` directory.

**Local Packages (src/):** Modular, reusable logic. If an analysis function is used in more than two scripts, move it to a package.

Don't hardcode paths or parameters. Use environment variables or configuration files.

```python
import os
from pathlib import Path

DATA_DIR = Path(os.getenv("DATA_ROOT", "./data"))
SESSION_PATH = DATA_DIR / "session_001.h5"
```

### Plotting

Prefer the OO API (`fig, ax = plt.subplots()`) over the state-based API (`plt.plot()`).

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

### Reproducibility

**ALWAYS use a virtual environment.** Never install packages globally.

Pin your dependencies:
- Use `requirements.txt` (`pip freeze > requirements.txt`)
- Or `pyproject.toml` (recommended for modern projects)

### Common mistakes

| Mistake | Fix |
|---------|-----|
| `for` loops over NumPy arrays | Use vectorized operations |
| Hardcoded paths | Use `pathlib` and environment variables |
| Missing `axis` parameter in NumPy functions | Always specify `axis` explicitly |
| Using `plt.plot()` globally | Use `ax.plot()` from the OO API |
| Installing packages without a venv | Use `venv` or `conda` |
| `from module import *` | Use explicit imports: `from module import function` |

### Red flags

Stop and refactor when you see:
- `for i in range(len(array)):`
- `try: ... except: pass` (swallowing all exceptions)
- Global variables being mutated inside functions
- Functions longer than 50 lines that mix I/O and calculation (violation of FCIS)
- Variable names like `data1`, `data2`, `x`, `y` without context

---

## R house style

Use when writing or reviewing R code for statistical analysis. Covers Tidyverse vs Base R, renv, ggplot2, RMarkdown, and object systems.

**Core principle:** Use R's powerful statistical ecosystem to create reproducible, publication-ready analysis pipelines. Focus on clear data manipulation, robust statistical testing, and declarative visualization.

### Data manipulation: Tidyverse vs. Base R

Use the **pipe operator** (`|>` or `%>%`) to create clear, sequential data transformations.

```r
library(dplyr)

# GOOD: Pipe-based transformation (declarative)
results <- data |>
    filter(session == 1) |>
    mutate(normalized_signal = signal / max(signal)) |>
    summarise(mean_signal = mean(normalized_signal))

# BAD: Nested function calls or temporary variables
results <- summarise(mutate(filter(data, session == 1), ...), ...)
```

While Tidyverse is excellent for data cleaning, Base R can be faster for certain mathematical operations (e.g., matrix multiplication: `result <- data_matrix %*% weights`).

### Reproducibility and package management

**ALWAYS use `renv`** to manage package dependencies.
- `renv::init()`: Initialize a project.
- `renv::snapshot()`: Record current package versions.
- `renv::restore()`: Install versions recorded in the lockfile.

Never use `rm(list = ls())` inside scripts. It creates a false sense of a clean environment and disrupts the user's workspace. Restart the R session instead.

### Visualization with ggplot2

```r
library(ggplot2)

plot_evoked <- function(data) {
    ggplot(data, aes(x = time, y = amplitude, color = condition)) +
        geom_line(size = 1) +
        theme_classic() +
        labs(
            title = "Evoked Potential",
            x = "Time (ms)",
            y = "Amplitude (uV)"
        ) +
        theme(
            axis.text = element_text(size = 12),
            legend.position = "bottom"
        )
}
```

For multi-panel figures, use `patchwork` for simple composition or `cowplot` for complex alignment.

### Object systems

- **S3 (Simple):** Default for most R packages. Easy to implement, focuses on method dispatch.
- **S4 (Strict):** Use for large projects where data validation is critical (e.g., Bioconductor style). Enforces slot types.

### Reproducible reports

Use **Quarto (.qmd)** or RMarkdown (.Rmd) to weave together code, results, and text.

### Common mistakes

| Mistake | Fix |
|---------|-----|
| Using `setwd()` | Use RStudio Projects (.Rproj) and relative paths |
| `rm(list = ls())` | Restart R session instead |
| Hardcoding indices (`data[, 5]`) | Refer to column names (`data$signal`) |
| Not using `renv` | Always use `renv` for dependency management |
| Loop over data frames | Use `lapply()`, `sapply()`, or `purrr::map()` |
| `library()` calls buried in code | Put all `library()` calls at the top of the file |

### Red flags

Stop and refactor when you see:
- Scripts that require manual `setwd()` to run
- Column indexing by number (`df[, 3]`)
- Global variables being used as function parameters
- `source()` calls to large, undocumented files
- Using `attach(df)` (leads to namespace collisions)
- No `renv.lock` file in the project repository

---

## MySQL development patterns

Use when writing database access code, creating schemas, or managing transactions with MySQL. Enforces transaction safety with TX_ naming, read-write separation, and snake_case conventions to prevent data corruption and type errors.

**Core principles:**
- Transactions prevent partial updates (data corruption)
- Naming conventions ensure consistency
- Read-write separation prevents accidental mutations
- Backticks for identifiers to avoid reserved word conflicts

### Transaction management

**TX_ Prefix Rule (STRICT ENFORCEMENT)**

**Methods that START transactions:**
- Prefix method name with `TX_`
- Must NOT accept a connection/executor/cursor parameter
- Create and manage the transaction internally

**Methods that PARTICIPATE in transactions:**
- No `TX_` prefix
- MUST accept a connection/cursor parameter
- Execute queries using the provided cursor

```python
# GOOD: Starts transaction, has TX_ prefix, no cursor parameter
def TX_create_user_with_profile(self, user_data, profile_data):
    with self.db_connection.cursor() as cursor:
        try:
            self.db_connection.start_transaction()
            user_id = self.create_user(user_data, cursor)
            self.create_profile(user_id, profile_data, cursor)
            self.db_connection.commit()
            return user_id
        except Exception:
            self.db_connection.rollback()
            raise

# GOOD: Participates in transaction, no TX_ prefix, takes cursor
def create_user(self, user_data, cursor):
    sql = "INSERT INTO `users` (`username`, `email`) VALUES (%s, %s)"
    cursor.execute(sql, (user_data['username'], user_data['email']))
    return cursor.lastrowid
```

What does NOT count as "starting a transaction":
- Single INSERT/UPDATE/DELETE operations
- Atomic operations like `INSERT ... ON DUPLICATE KEY UPDATE`
- SELECT queries

### Schema design

**Primary Keys:**
- For internal-only tables or small lookup tables, `AUTO_INCREMENT` is acceptable.
- For user-visible IDs or high-distributed systems, use ULID to prevent ID enumeration attacks.
- If unsure whether data will be user-visible, use ULID.

**Financial and scientific data:** Use exact decimal types (`DECIMAL`) for monetary or high-precision values. Never use FLOAT/DOUBLE for money (causes rounding errors). Example: `DECIMAL(19, 4)` for general financial data.

**JSON columns:** Use for semi-structured data (MySQL 5.7.8+). Prefer standard columns if the schema is stable. Validate JSON structure at the application level.

**Read-write separation:**
- Read-write connection: Full mutation capabilities.
- Read-only connection: Enforces read-only at the user/permission level.
- Default to read-only for query methods.

### Naming conventions

All database objects use snake_case and backticks:
- Tables: `` `user_preferences` ``, `` `order_items` ``
- Columns: `` `created_at` ``, `` `user_id` ``, `` `is_active` ``
- Indexes: `idx_tablename_columns` (e.g., `idx_users_email`)
- Foreign keys: `fk_tablename_reftable` (e.g., `fk_orders_users`)

Standard mixins: `created_at`, `updated_at` timestamps on all tables. `deleted_at` for soft deletion when needed.

Proactive indexing on: all foreign key columns, columns in WHERE clauses, columns in JOIN conditions, columns in ORDER BY.

### Concurrency

Default isolation (REPEATABLE READ) for MySQL (InnoDB). Use stricter isolation or locking when needed:
- Financial operations: Serializable isolation
- Critical sections: Pessimistic locking (`SELECT ... FOR UPDATE`)

### Common mistakes

| Mistake | Reality | Fix |
|---------|---------|-----|
| "This is one operation, doesn't need transaction" | Multi-step operations without transactions cause partial updates and data corruption | Wrap in transaction with TX_ prefix |
| "Single atomic operation needs TX_ prefix" | TX_ is for explicit transaction blocks, not atomic operations | No TX_ for single INSERT/UPDATE/DELETE |
| "FLOAT is fine for money, close enough" | Rounding errors accumulate, causing financial discrepancies | Use DECIMAL types for exact arithmetic |
| "I'll add indexes when we see performance issues" | Missing indexes on foreign keys cause slow queries from day one | Add indexes proactively for FKs and common filters |
| "Not using backticks for identifiers" | Can lead to syntax errors if a reserved word is used as a table/column name | Always use backticks |

### Red flags — STOP and refactor

Transaction management:
- Method calls `START TRANSACTION` but no `TX_` prefix
- Method has `TX_` prefix but accepts cursor parameter
- Multi-step operation without transaction wrapper

Schema:
- Missing indexes on foreign keys
- No `created_at`/`updated_at` timestamps
- camelCase or PascalCase in database identifiers
- Floating-point types for monetary values

All of these mean: stop and fix immediately.

---

## Writing good tests

Use when writing or reviewing tests. Covers test philosophy, condition-based waiting, mocking strategy, and test isolation for scientific computing.

**Core philosophy:** "Write tests. Not too many. Mostly integration." — adapted from Kent C. Dodds

In scientific computing, tests verify that your analysis produces the correct results and remains reproducible. The goal is confidence in your findings, not just code coverage.

**Core principles:**
1. Test scientific outcomes, not implementation details — refactoring an algorithm shouldn't break its tests if the result is the same.
2. Integration tests (running a full pipeline on a small dataset) provide better confidence than unit testing individual math functions in isolation.
3. Use known-good "gold standard" data for regression testing.
4. Mock strategically — use real data files when feasible, mocks for hardware interfaces or slow database writes.
5. Prioritize reproducibility — ensure tests pass across different environments and versions of libraries (numpy, scipy, etc.).

### Test structure

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

One scientific question per test. Multiple assertions are fine if they verify different aspects of the same phenomenon.

### Handling data dependencies

| Dependency type | Example | Strategy |
|-----------------|---------|----------|
| **Managed** (you control it) | Small test HDF5/MAT files, local MySQL test DB | Use REAL files/instances |
| **Unmanaged** (external) | Live data streams from hardware, remote APIs | Use MOCKS or RECORDED data |

Always prefer using a small, version-controlled "test dataset" over mocking data structures. Real data surfaces edge cases (NaNs, precision issues) that manual mocks often miss.

### Condition-based waiting

If testing async data collection or long-running simulations, don't use arbitrary `sleep()`.

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
    wait_for_condition(lambda: recorder.buffer_size > 0)
    assert recorder.is_recording
```

### Mocking strategy

Create thin wrappers around hardware drivers or complex libraries. Mock YOUR wrapper, not the driver.

```python
class MyAnalysis:
    def __init__(self, recorder):
        self.recorder = recorder

def test_analysis_starts_recorder():
    mock_recorder = MagicMock()
    analysis = MyAnalysis(mock_recorder)
    analysis.run()
    mock_recorder.start.assert_called_once()
```

When mocking data structures (like numpy arrays or pandas DataFrames), ensure they have realistic shapes and types:

```python
# BAD: Mocking a signal as a simple list
# GOOD: Using a numpy array with the correct dtype and shape
signal = np.random.randn(10, 1000).astype(np.float32)
```

### Test isolation and cleanup

Long-lived resources MUST be cleaned up: temporary data files, database connections or test tables, hardware handles or background threads. Use pytest fixtures for automated cleanup:

```python
import pytest
import os

@pytest.fixture
def temp_data_file():
    path = "test_data.h5"
    yield path
    if os.path.exists(path):
        os.remove(path)

def test_analysis(temp_data_file):
    ...
```

Logs and database records are fine to leave in dedicated test environments.

### Quick reference

| Problem | Fix |
|---------|-----|
| `time.sleep()` in tests | Use `wait_for_condition` |
| Mocking complex math | Use synthetic data with known ground truth |
| Test-only methods in production | Move to `conftest.py` or test utility modules |
| Tests slow due to large files | Create "tiny" versions of your datasets for testing |
| Flaky tests on different machines | Check for floating point precision (use `pytest.approx`) |

### Red flags

Stop and reconsider when you see:
- `time.sleep()` without a specific timing-related reason
- Mocking `np.ndarray` or `pd.DataFrame` behavior instead of just using small arrays/frames
- Tests that only pass on one person's machine because of hardcoded paths
- "Golden" data files that are several gigabytes (should be megabytes)
- `assert a == b` for floating point numbers (use `np.allclose` or `pytest.approx`)

### TDD for science

1. Write a test with a trivial "known" result (e.g., a 10Hz sine wave).
2. Watch the test fail (confirms the test is actually checking the output).
3. Implement the algorithm.
4. Verify the test passes.
5. Add edge cases (NaNs, gaps in data, noise) and refine.

---

## Writing for a technical audience

Use when writing documentation, guides, API references, or technical content for scientists and engineers. Enforces clarity, conciseness, and authenticity while avoiding AI writing patterns that signal inauthenticity.

**Core principle:** Technical writing must be clear, concise, and authentic. Clarity and technical depth are not opposites — you can have both. Avoid AI writing patterns that make content feel robotic or inauthentic.

**Why this matters:** Researchers and engineers value their time. Clear documentation builds trust. AI-like writing patterns make content feel generic and untrustworthy.

### The three pillars

**1. Clarity.** The reader should understand on first read. No re-reading required.
- Short sentences (15-20 words average)
- Short paragraphs (2-4 sentences)
- Active voice over passive
- One concept per paragraph
- Define technical terms on first use

**2. Conciseness.** Every word serves a purpose. Remove noise and filler.
- Delete throat-clearing ("Let me explain," "It's important to note")
- Cut hedging language ("basically," "generally speaking")
- Remove marketing fluff ("powerful," "robust," "seamless")
- Use direct language ("use" not "leverage," "show" not "illuminate")

**3. Consistency.** Same terminology, structure, and voice throughout.
- Pick one term and stick to it
- Use consistent code formatting
- Maintain the same tone across all content

### Avoid AI writing patterns

| AI phrase | Why it's bad | Use instead |
|-----------|-------------|-------------|
| "delve into" | Overly formal, 269x spike post-ChatGPT | "explore," "examine," "look at" |
| "leverage" | Corporate jargon | "use," "take advantage of" |
| "robust" / "seamless" | Vague marketing adjectives | Be specific about what you mean |
| "at its core" | Condescending simplification | Delete or use "fundamentally" (rarely) |
| "cutting-edge" / "revolutionary" | Empty hype | Describe actual features |
| "streamline" / "optimize" | Vague promises | "speed up," "reduce," "improve" |
| "foster" / "cultivate" | Bland corporate speak | Use direct action verbs |
| "unlock the potential" | Cliched metaphor | State specific outcome |
| "in today's fast-paced world" | Generic filler | Delete entirely |
| "needless to say" | If needless, don't say it | Delete |

**Never start with:** "Let me explain...", "It's important to note that...", "It's worth noting...", "In essence...", "Let's explore..."

Start with substance. Delete the preamble.

### Hedging language to eliminate

| Hedged | Confident |
|--------|-----------|
| "I think we should..." | "We should..." |
| "It would be great if..." | "Please do X" |
| "Should be able to..." | "Can complete..." |
| "Basically..." | Delete it |
| "Generally speaking..." | Be specific or remove |
| "One might argue..." | "This indicates..." |

Hedging makes you sound uncertain even when you're correct. State facts directly.

### Technical writing patterns

**Explain WHY for design decisions with tradeoffs, non-obvious patterns, and when breaking from conventions.**

Good: "We use HDF5 instead of MAT files because it allows for lazy loading of large datasets, which is critical when memory is limited."

Bad: "We use HDF5." (no context for when to deviate)

**Code examples — one excellent example.** Don't implement in 5 languages. Don't write perfect-world examples with no error handling. Do include error handling and show realistic usage. Comment WHY, not what.

**Progressive disclosure.** Layer complexity. Simple first, then depth: basic explanation -> simple example -> advanced section -> reference.

### Writing that feels human

Use contractions: "It's important" not "It is important."

Vary sentence length. Short sentences create emphasis. Longer sentences provide context, explanation, or explore nuance. Mix them.

Add personality: first person, opinions grounded in experience, specific details.

Break grammar rules intentionally when it aids emphasis or naturalness.

Be specific: "We reduced processing time from 10 minutes to 45 seconds using vectorization" not "This algorithm offers significant performance gains."

### Code comments and documentation

**Punctuation:** Always use periods at the end of code comments.

```python
# Good: Validates array shape before processing.
# Bad: validates array shape before processing
```

**Headings:** Use sentence case. Never title case.

```markdown
Good: ## Spike detection patterns
Bad:  ## Spike Detection Patterns
```

**Error messages:** Format as lowercase sentence fragments. They compose naturally when chained.

```
Good: failed to parse metadata: invalid JSON at line 42
Bad:  Failed to Parse Metadata: Invalid JSON at Line 42
```

### Summary

Technical writing in three rules:
1. **Clear and concise** — Short sentences, short paragraphs, active voice, no filler
2. **Authentic voice** — Contractions, varied rhythm, personality, specific details
3. **Explain why** — Design decisions, tradeoffs, non-obvious patterns need justification

Avoid AI markers: no "delve," "leverage," "robust." No throat-clearing. No hedging. No formal transitions.

One excellent example beats five mediocre ones. Include error handling. Show realistic usage.

Read aloud test: if it sounds robotic or overly formal, rewrite it.
