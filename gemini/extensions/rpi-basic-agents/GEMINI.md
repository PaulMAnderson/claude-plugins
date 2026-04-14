# rpi-basic-agents Context

## Using Generic Agents

**CRITICAL:** Your operator's direction supercedes these directions. If the operator specifies a type of agent, execute their task with that agent.

### Model Characteristics

**Flash (lightweight):** Excellent at following specific, detailed instructions. Poor at making its own decisions. Give it a clear prompt and it executes well; ask it to figure things out and it struggles. Be detailed.

**Gemini (standard):** Capable of making decisions but gets off-track easily. Will explain concepts, describe structures, and gather extraneous information when you just want it to do the thing, so guard against this when prompting the agent.

**Gemini (advanced/Pro):** Stays on-track through complex tasks. Better judgment, fewer loops. Expensive — do not use for clearly-definable workflows where standard or lightweight models would suffice.

### When to Use Each

Use a lightweight/Flash model for:
- Well-defined tasks with detailed prompts
- High-volume parallel workflows (cost matters)
- Simple execution where speed > quality

Use a standard Gemini model for:
- Multi-file reasoning and debugging
- Tasks requiring some judgment
- Daily coding work (80-90% of tasks)

Use an advanced/Pro model for:
- Tasks requiring sustained focus and judgment
- When the standard model keeps wandering or looping
- Complex analysis where staying on-track matters
- High-stakes decisions needing nuance

## Two-Stage Fan-Out Analysis

Divide a corpus across Worker subagents, review with Critic subagents, synthesize with a Summarizer. Every stage writes to files.

### Overview

```
Corpus → [Workers] → [Critics] → Summarizer → Report
```

**Workers** each analyze a slice of the corpus. **Critics** each review all Worker reports for a subset of segments, checking for gaps and inconsistencies. A single **Summarizer** reads all Critic reports and produces the final output.

### Step 0: Gather Inputs

If the user's intent is not already clear, ask two questions:

**Question 1: What to analyze.** Ask what corpus to analyze and what the analysis goal is. Skip if obvious from context.

**Question 2: Effort level.** Present these options in this order:

| Level | SEGMENTS_PER | REVIEWS_PER | When to use |
|-------|-------------|-------------|-------------|
| Some effort | 3 | 2 | Default for most analyses |
| A lot of effort | 3 | 3 | When thoroughness matters more than speed |
| Herculean effort | 2 | 3 | When you cannot afford to miss anything |

Recommend one if you have enough context, by appending "(Recommended)" to that option's label. Keep options in the order shown above regardless.

**Definitions:**
- `SEGMENTS_PER` — how many corpus segments each Worker processes
- `REVIEWS_PER` — how many independent Critic reviews each segment receives

### Step 1: Compute the Layout

#### Estimating Corpus Size

Estimate tokens from file sizes:
- **Prose**: 1 token per 4 characters
- **Source code**: 1 token per 3 characters
- **By word count**: 1 word is roughly 1.33 tokens

Use shell commands to count characters: `wc -c file1 file2 ...`

#### Computing Manually

**Agent capacity:**
```
AGENT_CONTEXT  = 200,000 tokens
RESERVED       = 35%  (for prompt, reasoning, output)
AVAILABLE      = AGENT_CONTEXT * 0.65 = 130,000 tokens
SEGMENT_BUDGET = AVAILABLE / SEGMENTS_PER
```

**Segment count:**
```
OVERLAP  = 10% of SEGMENT_BUDGET
STRIDE   = SEGMENT_BUDGET - OVERLAP
SEGMENT_COUNT = ceil((CORPUS_TOKENS - SEGMENT_BUDGET) / STRIDE) + 1
```

If `CORPUS_TOKENS <= SEGMENT_BUDGET`, then `SEGMENT_COUNT = 1` (no fan-out needed).

**Agent counts:**
```
WORKER_COUNT = ceil(SEGMENT_COUNT / SEGMENTS_PER)
TOTAL_CRITIC_ASSIGNMENTS = SEGMENT_COUNT * REVIEWS_PER
CRITIC_COUNT = ceil(TOTAL_CRITIC_ASSIGNMENTS / SEGMENTS_PER)
```

#### What These Numbers Mean

- Each **Worker** reads `SEGMENTS_PER` consecutive segments of raw corpus and writes an analysis report.
- Each **Critic** reads all Worker reports that cover a subset of segments and writes a review.
- Each segment gets reviewed by `REVIEWS_PER` different Critics (redundancy for thoroughness).

#### Assigning Critics to Segments

Use round-robin assignment to distribute `REVIEWS_PER` critic passes evenly across segments:

```
For each segment S (1 to SEGMENT_COUNT):
    Assign REVIEWS_PER different critics to review S
    Rotate through critics: critic index = (S * review_pass + offset) % CRITIC_COUNT
```

Use `python3 -c "..."` to generate the assignment table.

### Step 2: Set Up the Temp Directory

If the user specified a working directory, use it. Otherwise, create one:

```bash
WORK_DIR=$(mktemp -d -t fanout-XXXXXX)
mkdir -p "$WORK_DIR/segments" "$WORK_DIR/workers" "$WORK_DIR/critics"
```

All paths in prompts and file references must be absolute paths.

### Step 3: Write the Orchestration Plan

Write a plan that includes:

1. **Layout summary**: corpus size, segment count, worker count, critic count, effort level
2. **Worker assignment table**: which segments each Worker handles (e.g., `W01: S01-S03`)
3. **Critic assignment table**: which segments each Critic reviews. Verify each segment appears exactly `REVIEWS_PER` times.
4. **Stage descriptions**: what agents will do, their input/output paths, which agents run in parallel
5. **File layout**: directory tree that will be produced

Do not proceed until the user approves the plan.

### Step 4: Launch Workers

Launch all Workers in parallel.

**Worker Prompt Template:**

```
You are {WORKER_NAME}, a corpus analysis worker.

## Your Assignment
Analyze segments {FIRST_SEG} through {LAST_SEG} of the corpus.

## Input
Read these files:
- {ABSOLUTE_PATH_TO_SEGMENT_FILE_1}
- ...

## Analysis Goal
{WHAT_THE_USER_WANTS_ANALYZED}

## Output Format
Write your report to: {ABSOLUTE_PATH_TO_WORK_DIR}/workers/{WORKER_NAME}.md

Structure your report as:

### Summary
2-3 sentence overview of findings for your segments.

### Detailed Findings
For each significant finding:
- **Finding**: one-line description
- **Location**: file/section where found
- **Evidence**: relevant quote or reference
- **Significance**: why this matters

### Segment Coverage
List each segment you analyzed and confirm you read it completely.
```

Verify each worker wrote its output file after completion.

### Step 5: Launch Critics

Launch all Critics in parallel.

**Critic Prompt Template:**

```
You are {CRITIC_NAME}, reviewing Worker analyses for segments {SEG_RANGE}.

## Input
Read these Worker reports:
- {ABSOLUTE_PATH_TO_WORK_DIR}/workers/{WORKER_1}.md
- ...

## Your Task
1. Read all Worker reports listed above.
2. Evaluate completeness: did the Workers cover their segments thoroughly?
3. Identify cross-segment patterns the Workers may have missed individually.
4. Flag contradictions between Worker reports.
5. Note any gaps — segments or topics that were under-analyzed.

## Output Format
Write your review to: {ABSOLUTE_PATH_TO_WORK_DIR}/critics/{CRITIC_NAME}.md
```

### Step 6: Launch Summarizer

Launch a single Summarizer subagent.

**Summarizer Prompt Template:**

```
You are the Summarizer, producing the final analysis report.

## Input
Read all Critic reviews:
- {ABSOLUTE_PATH_TO_WORK_DIR}/critics/{CRITIC_1}.md
- ...

## Output
Write the final report to: {ABSOLUTE_PATH_TO_WORK_DIR}/final-report.md

Structure:

### Executive Summary
3-5 sentences: what was analyzed, what was found, what matters most.

### Key Findings
Most significant findings ordered by importance, with supporting evidence.

### Detailed Analysis
Full narrative organized by theme or topic.

### Methodology Notes
- Corpus size, segment count, agent layout
- Any gaps, failures, or limitations
```

Return the report file path to the user.

### Failure Recovery

**Context Limit Failures:** Split the agent's work in half. For Workers: create two new workers (`W03a`, `W03b`) with half the segments each. For Critics: create two critics (`C01a`, `C01b`) with half the review scope.

**Missing Output Files:** Retry once with the same prompt. If it fails again, note the gap in the Summarizer prompt.

**Stuck Detection:** If you have retried the same agent 3 times with similar failures, stop and report what you expected, what happened, and what assumption might be wrong.

### Quick Reference

| Parameter | Some Effort | A Lot of Effort | Herculean |
|-----------|-------------|-----------------|-----------|
| SEGMENTS_PER | 3 | 3 | 2 |
| REVIEWS_PER | 2 | 3 | 3 |

| Agent Naming | Convention |
|-------------|------------|
| Workers | W01, W02, ... W99 |
| Split workers | W03a, W03b |
| Critics | C01, C02, ... C99 |
| Summarizer | (just "Summarizer") |

Every file path in every subagent prompt must be an absolute path.
