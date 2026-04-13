---
name: howto-code-in-r
description: Write or review R code for statistical analysis
user-invocable: false
---

# R House Style

## Overview

**Core principle:** Use R's powerful statistical ecosystem to create reproducible, publication-ready analysis pipelines. Focus on clear data manipulation, robust statistical testing, and declarative visualization.

**Why this matters:** R is the tool of choice for statistical validation and data exploration. Using `tidyverse` patterns and `renv` ensures your analysis is both readable and reproducible across environments.

## Data Manipulation: Tidyverse vs. Base R

### Prefer Tidyverse for Readability

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

### Use Base R for Performance-Critical Loops

While `tidyverse` is excellent for data cleaning, Base R can be faster for certain mathematical operations.

```r
# FAST: Base R matrix multiplication
result <- data_matrix %*% weights
```

## Reproducibility and Package Management

### Use `renv`

**ALWAYS** use `renv` to manage package dependencies. This records exact package versions and prevents "it works on my machine" issues.
- `renv::init()`: Initialize a project.
- `renv::snapshot()`: Record current package versions.
- `renv::restore()`: Install versions recorded in the lockfile.

### Avoid `rm(list = ls())`

Never use `rm(list = ls())` inside scripts. It creates a false sense of a clean environment and disrupts the user's workspace. Instead, restart the R session regularly.

## Visualization with `ggplot2`

### Publication-Ready Figures

Use `ggplot2` for all statistical plotting. Follow these conventions for scientific clarity:

```r
library(ggplot2)

plot_evoked <- function(data) {
    ggplot(data, aes(x = time, y = amplitude, color = condition)) +
        geom_line(size = 1) +
        theme_classic() +  # Clean white background
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

### Use `cowplot` or `patchwork`

For multi-panel figures, use `patchwork` for simple composition or `cowplot` for complex alignment.

## Object Systems

### S3 vs. S4 Objects

- **S3 (Simple):** Default for most R packages. Easy to implement, focuses on method dispatch.
- **S4 (Strict):** Use for large projects where data validation is critical (e.g., Bioconductor style). Enforces slot types.

## Reproducible Reports with RMarkdown/Quarto

Use **Quarto (.qmd)** or RMarkdown (.Rmd) to weave together code, results, and text. This is the gold standard for scientific documentation.

- **Knit to HTML** for sharing with collaborators.
- **Knit to PDF** for publication-quality reports.

## Property-Based Testing with `hedgehog`

Use `hedgehog` (or `testthat`) to find edge cases in your statistical functions.

```r
library(hedgehog)

test_that("mean is within bounds", {
  forall(gen.list(gen.element(1:100)), function(xs) {
    if (length(xs) == 0) return(TRUE)
    expect_true(mean(xs) >= min(xs) && mean(xs) <= max(xs))
  })
})
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `setwd()` | Use RStudio Projects (.Rproj) and relative paths |
| `rm(list = ls())` | Restart R session instead |
| Hardcoding indices (`data[, 5]`) | Refer to column names (`data$signal`) |
| Not using `renv` | Always use `renv` for dependency management |
| Loop over data frames | Use `lapply()`, `sapply()`, or `purrr::map()` |
| `library()` calls buried in code | Put all `library()` calls at the top of the file |

## Red Flags

**Stop and refactor when you see:**
- Scripts that require manual `setwd()` to run
- Column indexing by number (`df[, 3]`)
- Global variables being used as function parameters
- `source()` calls to large, undocumented files
- Using `attach(df)` (leads to namespace collisions)
- No `renv.lock` file in the project repository
