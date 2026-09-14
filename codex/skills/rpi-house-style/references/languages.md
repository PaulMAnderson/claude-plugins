# Scientific language conventions

## Python

- Use existing project environments and lock/dependency conventions. Create a project virtual environment when needed; do not install packages globally or replace an existing package manager merely for style.
- Prefer NumPy array operations and broadcasting where readable and efficient. Document dimensions and units with type hints/array annotations; name axes, preserve dimensions intentionally, validate orientation. Handle zero denominators and missing values explicitly according to the scientific contract.
- Keep reusable logic in modules and one-off entry points in scripts/notebooks with explicit inputs. Keep paths/parameters in configuration passed from the shell. Avoid mutable global state.
- Use type hints for public/function interfaces appropriate to the supported Python version. Use Matplotlib's object-oriented API (`fig, ax`), explicit labels/units, and return or save the requested figure; avoid hidden dependence on global plotting state.
- Use an explicit random generator/seed for reproducible analysis, record versions and data provenance, and use Hypothesis/property tests where they verify meaningful invariants.

## MATLAB

- Prefer functions over base-workspace scripts. Use supported `arguments` validation blocks for shape/type/value constraints; respect the project's MATLAB release instead of imposing newer syntax.
- Use vectorization where clear and preallocate loops. Document array orientation and indexing conventions; check NaN/finite and sample-rate assumptions according to the contract.
- Organize namespaces with `+package`, limit helpers with `private`, and use `fullfile` for paths. Avoid `global`, `eval`, `assignin`, `clear all`, and disruptive workspace/figure cleanup.
- Use value classes/structs for data, handle classes when shared mutable entity identity is needed. Keep hardware/file I/O outside numerical logic.
- Use `matlab.unittest`, known signals, regression data, tolerances, and relevant property checks. Use condition-based waits with bounded timeouts for asynchronous hardware.

## R

- Follow the project's tidyverse/base-R style; use readable pipelines for data manipulation and efficient matrix operations for numerical kernels. Prefer named columns to positional indices.
- Use the existing `renv` setup; for a new R project use `renv` to capture/restore dependencies. Avoid changing the user's working directory or clearing their workspace with `rm(list=ls())`.
- Keep data/configuration explicit; avoid `attach`, hidden globals, and undocumented `source` chains. Choose S3 for ordinary dispatch and S4 when formal validated structure serves the domain.
- Use ggplot2 with labeled units/scales and appropriate themes; use patchwork/cowplot for layouts when already appropriate dependencies. Use Quarto/RMarkdown for reproducible reports when requested.
- Use known data, explicit seeds, tolerances, and testthat/property tests (for example hedgehog when appropriate). Record missing-data handling and statistical assumptions.
