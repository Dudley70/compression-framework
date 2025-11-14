---
name: llm-doc-compression
description: Compress technical docs to max density (85% reduction) while maintaining 95% information retention. Preserves ALL prompts, code, schemas, outputs verbatim - only compresses format. Use for LLM-optimized docs with complete reproducibility.
---

# LLM Documentation Compression

**Version**: 1.0.0 | **Target**: 95%+ information retention at 85% size reduction

## CRITICAL RULES (Read First)

### Rule #1: NEVER COMPRESS CONTENT
**If it's needed for reproduction → keep 100% verbatim**

**NEVER TOUCH**:
- Test prompts (every word exact)
- Code examples (every character exact)
- Command-line examples (exact)
- API calls (exact)
- Schema definitions (exact)
- Model outputs (structure + content preserved)
- Function/variable/parameter names (exact)
- JSON keys (exact)
- Configuration values (exact)

**Example - WRONG**:
```
Original: "Let's think step by step to determine the final number"
Compressed: "Think stepwise for final #" ❌ DESTROYED
```

**Example - CORRECT**:
```
Original: "Let's think step by step to determine the final number"
Compressed: "Let's think step by step to determine the final number" ✓ EXACT
```

### Rule #2: ONLY COMPRESS FORMAT
**Compress prose, headers, transitions, scaffolding - NOT content**

**OK TO COMPRESS**:
- Headers: "**Source**: 1,332 lines" → "**Src**: 1,332L"
- Prose: "The model's performance was excellent" → "Excellent performance"
- Scaffolding: "Now let's examine..." → [delete]
- Meta-commentary: "As we can see..." → [delete]

## Theoretical Foundation

Implements (σ=0.9, γ=1.0, κ=0.1):
- **σ (Structure)**: 0.9 - Max density through format compression
- **γ (Granularity)**: 1.0 - **FULL semantic completeness (95%+ retention)**
- **κ (Scaffolding)**: 0.1 - Minimal explanatory context

**Target**: 95%+ information retention, 85% size reduction

## 10 Compression Rules WITH BOUNDARIES

### 1. Ultra-Terse Headers [↑σ] - FORMAT ONLY
Before: `**Source**: 1,332 lines / 134 kilobytes systematic assessment`
After: `**Src**: 1,332L/134KB systematic assessment`
**DON'T**: Touch any content words (systematic, assessment)

### 2. Extreme Abbreviations [↑σ] - PROSE ONLY
Use in: Prose descriptions, headers, table cells
Standard: E=Effectiveness, R=Reliability, Doc=Documentation, w/=with, w/o=without
**DON'T**: Abbreviate anything in prompts, code, schemas, commands

### 3. Symbols [↑σ] - ANALYSIS ONLY
Use in: Analysis sections, table cells, headers
Symbols: ✓✗⚠→↑↓=≠≥≤
**DON'T**: Use in preserved content (prompts, code, outputs)

### 4. Tables [↑σ] - HEADERS ONLY
Compress: Column headers (`Effectiveness` → `E`)
Preserve: All data in cells (use symbols for status, not content)

### 5. Prose→Fragments [↑σ, ↓κ] - ANALYSIS ONLY
Compress: "The model's performance on this task was excellent. It successfully..."
To: "Excellent performance. Successfully..."
**DON'T**: Apply to test prompts, code comments, output descriptions

### 6. Code/Prompt Preservation [γ=1.0] - SACRED CONTENT
**100% VERBATIM - NO EXCEPTIONS**

What counts as "code/prompt":
- Anything in code blocks (```...```)
- Test prompt instructions
- Command examples
- API calls
- Schema definitions
- Model outputs (keep structure + key content)
- Configuration examples

**If uncertain whether to preserve → PRESERVE IT**

### 7. Section Headers [↓κ] - FORMAT ONLY
Before: `### Definition` [3 lines explaining]
After: `**Def**: [1 terse sentence]`
**DON'T**: Compress the actual definition content

### 8. Scaffolding Removal [↓κ] - NON-CONTENT ONLY
Delete: "Now let's examine...", "As we can see...", "It's important to note..."
Keep: Actual content that follows these phrases
**DON'T**: Remove context needed to understand technical content

### 9. List Compression [↑σ, ↓κ] - ANALYSIS ONLY
Compress: Analysis lists, meta-commentary lists
Preserve: Technical specification lists, step-by-step procedures, test steps

### 10. Standard Test Format [↑σ] - MIXED
Compress: Headers, analysis prose
Preserve: **Prompt (verbatim)**, **Output (complete)**, **Test description (full)**

**Template**:
```
### [N]. [Name]
**Def**: [compress this]
**Doc**: [compress this]
**Test**: [keep description complete]
**Prompt**:
```
[KEEP 100% EXACT - EVERY WORD]
```
**Output**: [keep structure + key results]
```
[PRESERVE STRUCTURE + CONTENT]
```
**Analysis**: [can compress this to fragments]
**Scores**: E=[N]/10 ([keep reasoning]), R=[N]/10 ([keep reasoning])
```

## Quality Verification

Before finalizing, check:

**Information Retention**: 95%+
- [ ] Every test prompt is 100% verbatim
- [ ] Every code example is 100% exact
- [ ] Every schema/API call is 100% exact
- [ ] Model outputs preserve structure + key content
- [ ] Can reproduce any test from compressed version
- [ ] Score justifications are complete (not "good")

**Compression Metrics**: 85%
- [ ] 19-22KB size
- [ ] 400-450 lines
- [ ] Prose → fragments
- [ ] Headers abbreviated
- [ ] Zero scaffolding

**Format Standards**:
- [ ] Tables: single-letter headers
- [ ] Symbols: ✓✗⚠→ in analysis
- [ ] Abbreviations: E/R, CoT in prose only
- [ ] No subjects in analysis fragments

## Red Flags (Stop & Fix)

❌ **If you see any of these, you've gone too far**:
- Prompt phrases shortened ("think step by step" → "think stepwise")
- Code examples abbreviated
- API parameters simplified
- Output structure lost
- "Cannot reproduce test from this" feeling
- Information retention feels <90%

## Process

1. **Identify sacred content** (mark all prompts/code/schemas)
2. **Preserve sacred** (copy verbatim to output)
3. **Compress format** (apply rules 1-5, 7-9 to prose/headers/analysis)
4. **Verify retention** (can you reproduce every test?)
5. **Report**: [original] → [compressed] → [% size] + [% information retained]

## Examples

### ✅ CORRECT Compression

**Original**:
```markdown
**Test Prompt**:
"A logistics manager has to move items between three warehouses: A, B, and C.
- Starting state: Warehouse A has 40 units, B has 30, and C has 20.
Let's think step by step to determine the final number of units."

**Model Output**:
"Certainly. Let's break down the movement step by step.
**Step 1**: Half of A to B means 40/2 = 20 units moved..."
```

**Compressed**:
```markdown
**Prompt**:
```
A logistics manager has to move items between three warehouses: A, B, and C.
- Starting state: Warehouse A has 40 units, B has 30, and C has 20.
Let's think step by step to determine the final number of units.
```

**Output**: Confirmed step-by-step breakdown. Step 1: 40/2=20 moved A→B...
```

✅ **Prompt verbatim**, Output structure preserved, 95%+ retention

### ❌ WRONG Compression

**Original**: [same as above]

**Compressed (BAD)**:
```markdown
**Test**: Logistics problem w/ 3 warehouses, move units
**Output**: Model showed correct step-by-step
```

❌ **Prompt lost**, Output summarized, ~40% retention - **UNUSABLE**

## Claude Notes

- **When uncertain → preserve, don't compress**
- γ=1.0 is NON-NEGOTIABLE (95%+ retention required)
- Only compress FORMAT (headers, prose, scaffolding)
- Prompts/code = completely untouchable
- Target: V7 quality (23KB, 95% retention) not summarization
- If output <90% retention → failed, try again