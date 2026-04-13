---
name: writing-for-a-technical-audience
description: Write technical documentation, guides, and API references for scientists
user-invocable: false
---

# Writing for a Technical Audience

## Overview

**Core principle:** Technical writing must be clear, concise, and authentic. Clarity and technical depth are not opposites - you can have both. Avoid AI writing patterns that make content feel robotic or inauthentic.

**Why this matters:** Researchers and engineers value their time. Clear documentation builds trust. AI-like writing patterns (identified through research) make content feel generic and untrustworthy. Technical depth without clarity frustrates users. Clarity without depth leaves them stuck.

## When to Use

**Use this skill when:**
- Writing API documentation for analysis libraries
- Creating guides, tutorials, or how-to content for data pipelines
- Documenting code, algorithms, or architecture
- Writing technical reports or documentation for experiments
- Reviewing technical content for clarity

**Trigger symptoms:**
- "Does this sound too robotic?"
- Writing feels formal or stiff
- Using phrases like "delve into" or "leverage"
- Explaining obvious things instead of getting to the point
- Uncertain if content is clear enough

## The Three Pillars

### 1. Clarity

The reader should understand on first read. No re-reading required.

**Techniques:**
- Short sentences (15-20 words average)
- Short paragraphs (2-4 sentences)
- Active voice over passive
- One concept per paragraph
- Define technical terms on first use

### 2. Conciseness

Every word serves a purpose. Remove noise and filler.

**Techniques:**
- Delete throat-clearing ("Let me explain," "It's important to note")
- Cut hedging language ("basically," "generally speaking")
- Remove marketing fluff ("powerful," "robust," "seamless")
- Use direct language ("use" not "leverage," "show" not "illuminate")

### 3. Consistency

Same terminology, structure, and voice throughout.

**Techniques:**
- Pick one term and stick to it (don't use "dataset," "session," and "recording" interchangeably if they mean the same thing)
- Use consistent code formatting (e.g., PEP 8 for Python)
- Maintain the same tone across all content
- Follow established patterns for similar content types

## Avoid AI Writing Patterns

Research shows specific phrases and structures that readers identify as AI-generated. Avoid these to maintain authenticity.

### AI Phrases to Never Use

| AI Phrase | Why It's Bad | Use Instead |
|-----------|-------------|-------------|
| "delve into" | Overly formal, 269x spike post-ChatGPT | "explore," "examine," "look at" |
| "leverage" | Corporate jargon | "use," "take advantage of" |
| "robust" / "seamless" | Vague marketing adjectives | Be specific about what you mean |
| "at its core" | Condescending simplification | "fundamentally" (use rarely) or delete |
| "cutting-edge" / "revolutionary" | Empty hype | Describe actual features |
| "streamline" / "optimize" | Vague promises | "speed up," "reduce," "improve" |
| "foster" / "cultivate" | Bland corporate speak | Use direct action verbs |
| "unlock the potential" | Cliched metaphor | State specific outcome |
| "in today's fast-paced world" | Generic filler | Delete entirely |
| "needless to say" | If needless, don't say it | Delete |

### Throat-Clearing to Delete

**Never start with:**
- "Let me explain..."
- "It's important to note that..."
- "It's worth noting..."
- "In essence..."
- "Let's explore..."

**Fix:** Start with substance. Delete the preamble.

### Hedging Language to Eliminate

| Hedged | Confident |
|--------|-----------|
| "I think we should..." | "We should..." |
| "It would be great if..." | "Please do X" |
| "Should be able to..." | "Can complete..." |
| "Basically..." | Delete it |
| "Generally speaking..." | Be specific or remove |
| "One might argue..." | "This indicates..." |

**Why hedging fails:** Makes you sound uncertain even when you're correct. State facts directly.

## Technical Writing Patterns

### Explain WHY for These Cases

**ALWAYS explain why when:**

1. **Design decisions with tradeoffs**
   - Good: "We use HDF5 instead of MAT files because it allows for lazy loading of large datasets, which is critical when memory is limited."
   - Bad: "We use HDF5." (no context for when to deviate)

2. **Non-obvious patterns**
   - Good: "Always validate array shapes before applying the filter because the underlying C implementation will segfault if dimensions don't match exactly."
   - Bad: "Validate array shapes." (why?)

3. **Breaking from conventions**
   - Good: "This function uses 1-based indexing for channel numbers to match the physical labeling on the hardware, despite Python's 0-based convention."
   - Bad: "Use 1-based indexing for channels." (violates Python conventions without justification)

**When "how" alone suffices:**
- Mechanical steps with no alternatives ("Click Save")
- Standard practices ("Use `pip install`")
- When you genuinely don't know why (document behavior, note uncertainty)

### Code Examples: One Excellent Example

**Don't:**
- Implement in 5 languages
- Create fill-in-the-blank templates
- Write perfect-world examples with no error handling

**Do:**
- One complete, runnable example
- Include error handling (especially for I/O and data validation)
- Show realistic usage
- Comment WHY, not what

**Good Example Pattern:**

```python
# Good: Complete, realistic, explains why
import numpy as np

def apply_bandpass(signal, low, high, fs):
    """Applies a bandpass filter to the signal."""
    try:
        # Validate sampling rate - negative FS causes unstable filters
        if fs <= 0:
            raise ValueError(f"Sampling frequency must be positive, got {fs}")
            
        # Ensure signal is 1D - the filter expects a single channel
        if signal.ndim != 1:
            signal = signal.flatten()
            logger.warning("Flattened multi-dimensional signal for filtering")
            
        return some_filter_impl(signal, low, high, fs)
    except Exception as e:
        logger.error(f"Filtering failed: {e}")
        raise
```

**Bad Example Pattern:**

```python
# Bad: Perfect world, no context, brittle
result = apply_bandpass(signal, 10, 100, 1000)
return result
```

### Progressive Disclosure

Layer complexity. Simple first, then depth.

**Pattern:**
1. **Basic explanation** - what it does, core concept
2. **Simple example** - minimal working code
3. **Advanced section** - edge cases, configuration, tradeoffs
4. **Reference** - complete API surface

**Good:**
```markdown
## Spike Detection

Detect threshold crossings in a 1D signal:

```python
indices = detect_spikes(signal, threshold=5.0)
```

### Advanced: Handling Refractory Periods

To avoid multiple detections of the same spike, use the `refractory_ms` parameter...
```

**Bad:**
```markdown
## Spike Detection

Spike detection can be performed using several methods including threshold crossing, template matching, or wavelets. The choice depends on your signal-to-noise ratio, computational constraints, and the specific neuron type...
```

(Too much upfront. Start simple.)

## Anti-Patterns from Real Documentation

### 1. Assumes Too Much

**Bad:**
> "Simply connect your SpikeOrchestrator to the NiDAQ endpoint. Once a connection is established, instantiate a DataStream by passing your BufferConfiguration."

**Why it fails:** Jargon firehose with no definitions, no links, no onramp for beginners.

**Fix:** Define terms, link to hardware setup guides, provide a "Quick Start" script.

### 2. Perfect World Examples

**Bad:**
```python
data = load_mat_file('session_1.mat')
result = run_analysis(data)
print('Analysis complete!')
```

**Why it fails:** No error handling, ignores edge cases (file missing, file corrupted, data not in expected format).

**Fix:** Use `try-except`, check for dataset existence in the file, handle empty results.

### 3. Vague and Unhelpful

**Bad:**
- `get_channel(id)`: "Gets a channel by its ID."
- `class DataProcessor`: "A class for processing data."
- `process_data(data)`: "Processes the data."

**Why it fails:** Tautological. Says nothing beyond the function name.

**Fix:** Describe behavior, parameters, return values, exceptions. "Fetches raw voltage data for a specific channel index. Returns a 1D numpy array. Throws ValueError if the index is out of bounds for the current recording."

## Writing That Feels Human

### Use Contractions

**AI defaults to:**
- "It is important that you do not..."
- "You will need to..."

**Human writing:**
- "It's important that you don't..."
- "You'll need to..."

### Vary Sentence Length

**AI writes:**
Every paragraph is 3-4 sentences. Every sentence is 15-20 words. Everything feels perfectly balanced and rhythmic in an uncanny way.

**Human writes:**
Short sentences create emphasis. Longer sentences provide context, explanation, or explore nuance that requires more breathing room. Mix them. Create rhythm naturally.

### Add Personality

**AI avoids:**
- First person ("I," "we")
- Opinions
- Personal anecdotes
- Humor

**Human includes:**
- "We tried the standard filter first and found it introduced too much phase lag."
- "I recommend using the HDF5 format for sessions longer than 2 hours."
- Opinions grounded in experience
- Self-aware observations

### Break Grammar Rules Intentionally

**AI never:**
- Starts sentences with "And" or "But"
- Uses sentence fragments
- Ends with prepositions

**Human does:**
- "And that's exactly the point." (emphasis)
- "This is what we're dealing with." (natural)

### Be Specific

**AI writes vaguely:**
- "This algorithm offers significant performance gains."
- "Researchers have seen improved results using this method."

**Human writes specifically:**
- "We reduced processing time from 10 minutes to 45 seconds using vectorization."
- "This method correctly identified 98% of spikes in the benchmark dataset."

## Code Comments and Documentation

### Punctuation

Always use periods at the end of code comments.

```python
# Good: Validates array shape before processing.
# Bad: validates array shape before processing
```

### Headings

Use sentence case in all headings. Never title case.

```markdown
Good: ## Spike detection patterns
Bad:  ## Spike Detection Patterns

Good: ### When to use wavelets
Bad:  ### When To Use Wavelets
```

### Error Messages

Format error messages as lowercase sentence fragments. They compose naturally when chained.

```
Good: failed to parse metadata: invalid JSON at line 42
Bad:  Failed to Parse Metadata: Invalid JSON at Line 42
```

The lowercase format works because errors often chain: `"analysis failed: " + inner_error.message` reads correctly.

## Summary

**Technical writing in three rules:**

1. **Clear and concise** - Short sentences, short paragraphs, active voice, no filler
2. **Authentic voice** - Contractions, varied rhythm, personality, specific details
3. **Explain why** - Design decisions, tradeoffs, non-obvious patterns need justification

**Avoid AI markers:** No "delve," "leverage," "robust." No throat-clearing. No hedging. No formal transitions.

**One excellent example** beats five mediocre ones. Include error handling. Show realistic usage.

**Read aloud test:** If it sounds robotic or overly formal, rewrite it.
