---
name: howto-code-in-matlab
description: Use when writing or reviewing MATLAB code for scientific analysis - covers argument validation, vectorization, OOP for stateful objects, and toolbox organization
user-invocable: false
---

# MATLAB House Style

## Overview

**Core principle:** Use modern MATLAB features (R2019b+) to ensure type safety, modularity, and high-performance matrix operations. MATLAB is the "lingua franca" of many neuroscience labs; follow these standards to prevent "spaghetti scripts" and ensure reproducible results.

**Why this matters:** MATLAB's loose typing and global-workspace nature can lead to difficult-to-trace bugs. Using `arguments` blocks, namespaces, and OOP patterns makes analysis robust and shareable.

## Modern Function Design

### Use Argument Validation Blocks

**ALWAYS** use `arguments` blocks (R2019b+) for input type, shape, and value checking.

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

### Prefer Functions Over Scripts

Scripts share the base workspace and can cause naming collisions. Use functions to encapsulate variables. Use **Live Scripts (.mlx)** only for interactive exploration and documentation.

## Vectorization and Performance

### Leverage Matrix Operations

Avoid `for` loops where matrix operations are possible. MATLAB is highly optimized for these.

```matlab
% BAD: Manual loop
for i = 1:size(data, 1)
    results(i) = sum(data(i, :));
end

% GOOD: Vectorized sum
results = sum(data, 2);
```

### Preallocation

If you must use a loop, **always** preallocate your arrays to avoid the "growing array" performance penalty.

```matlab
% GOOD: Preallocate with zeros or NaN
n = 1000;
data = zeros(n, 1);
for i = 1:n
    data(i) = computeValue(i);
end
```

## Toolbox and Project Organization

### Use Namespaces (+package)

Avoid cluttering the global path. Use the `+` prefix to create packages.

```
+analysis/
    +signal/
        bandpass.m
    +spike/
        detect.m
```
Call as: `analysis.signal.bandpass(data, 1000)`

### Private Folders

Use `private/` directories for helper functions that should only be accessible within a specific package or folder.

### Avoiding Global State

**Never use `global` variables.** Use classes, structs, or pass data explicitly.

## Object-Oriented Programming (OOP)

### Stateful Analysis Objects

Use **Handle Classes** to represent experimental sessions, hardware interfaces, or processing pipelines where state must be preserved.

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
            % Mutates state in place
            obj.Data = obj.Data * 2;
        end
    end
end
```

### Handle vs. Value Classes

- **Handle Classes:** Mutated in place (like Python objects). Use for things that represent "entities."
- **Value Classes:** Copy-on-write (like structs). Use for pure data containers.

## Property-Based Testing

Use the MATLAB Unit Testing Framework with custom property checks.

```matlab
classdef MyAnalysisTest < matlab.unittest.TestCase
    methods(Test)
        function testSymmetry(testCase)
            data = rand(1, 100);
            result = mySymmetricOp(data);
            testCase.verifyEqual(result, flip(mySymmetricOp(flip(data))));
        end
    end
end
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `clear all` or `close all` inside functions | Never do this; it's disruptive to the user |
| Growing an array inside a loop | Preallocate with `zeros()` or `NaN()` |
| Not using semicolons | End assignments with `;` to avoid console clutter |
| Hardcoded paths with `\` (Windows) | Use `fullfile()` for cross-platform compatibility |
| Putting everything in the base workspace | Use functions and local variables |
| Using `ans` as a variable name | Assign results to descriptive names |

## Red Flags

**Stop and refactor when you see:**
- Functions with more than 5 input arguments without an `arguments` block
- `eval()` or `assignin()` (security and performance risks)
- `global` variables
- Large `.mat` files without a corresponding README or loading script
- Code that uses `pause(X)` instead of checking for conditions
