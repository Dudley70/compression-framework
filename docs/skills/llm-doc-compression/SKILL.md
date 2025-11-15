---
name: llm-doc-compression
description: Compress technical docs to max density (85% reduction) while maintaining 95% information retention. Preserves ALL prompts, code, schemas, outputs verbatim - only compresses format. Use for LLM-optimized docs with complete reproducibility.
---

# LLM Documentation Compression

**Version**: 1.0.1 | **Target**: 95%+ information retention at 85% size reduction

## CRITICAL RULES (Read First)

### Rule #1: NEVER COMPRESS CONTENT
**If it's needed for reproduction → keep 100% verbatim**

**SACRED CONTENT (NEVER TOUCH)**:
- Test prompts (every word exact)
- Code examples (every character exact)  
- Command-line examples (exact)
- API calls (exact)
- Schema definitions (exact)
- Model outputs (structure + content preserved)
- Persona descriptions (complete)
- Multi-paragraph analysis (keep complete, just remove filler)

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
**Compress headers, symbols, abbreviations - NOT meaning**

**OK TO COMPRESS**:
- Headers: "**Source**: 1,332 lines" → "**Src**: 1,332L"
- Prose subjects: "The model's performance" → "Performance"
- Symbols: "passed" → "✓", "failed" → "✗"
- Abbreviations: "with" → "w/", "Chain-of-Thought" → "CoT"

**NEVER COMPRESS**:
- Substantive content in analysis paragraphs
- Technical explanations
- Test descriptions
- Reasoning/justifications

## V7 Compression Pattern

V7 = **Format compression** with **content preservation**

**Standard test section template**:
```
### [N]. [Technique Name]

**Def**: [Terse 1-sentence definition - compress this]
**Doc**: [✓ Strong / ✗ None / ⚠ Partial - compress this]  
**Test**: [Keep complete test description]

**Prompt**:
```
[KEEP 100% VERBATIM - EVERY SINGLE WORD]
[Include all persona descriptions, test requirements, structure]
[Do NOT shorten, abbreviate, or "improve" prompts]
```

**Output**: [Keep structure + key findings. Can compress prose but preserve substance]

**Analysis**: [Keep complete. Remove filler ("As we can see") but preserve reasoning]

**Scores**: E=[N]/10 ([keep full reasoning]), R=[N]/10 ([keep full reasoning])
```

## Complete Examples

### Example 1: CORRECT V7 Compression

**BEFORE** (Original):
```markdown
### Chain-of-Thought (CoT) Prompting

#### Definition
Chain-of-Thought (CoT) prompting is a technique designed to improve the reasoning abilities of large language models by encouraging them to break down complex problems into a sequence of intermediate, logical steps.

#### Documentation Support
Official Google AI documentation provides strong support for CoT prompting. One guide explicitly names "Chain of Thought (CoT) Prompts" as a technique.

#### Practical Test Design
**Test Prompt**:
"A logistics manager has to move items between three warehouses: A, B, and C.
- Starting state: Warehouse A has 40 units, B has 30, and C has 20.
- Move operations: First, move half of A to B. Second, move one-third of B to C. Third, move one-quarter of C back to A.
Let's think step by step to determine the final number of units in each warehouse."

**Model Output**:
"Certainly. Let's break down the movement step by step.
**Step 1**: Half of A to B means 40/2 = 20 units moved from A to B..."

**Analysis**:
The model correctly executed multi-step reasoning. It broke down the problem into sequential steps, showed intermediate calculations, and arrived at the correct final state. This demonstrates that the CoT approach is highly effective for this model.

**Scores**:
- **Effectiveness**: 10/10 (Perfect step-by-step breakdown with correct math)
- **Reliability**: 9/10 (Consistently performs well on logical problems)
```

**AFTER** (V7):
```markdown
### 1. Chain-of-Thought (CoT)

**Def**: Improve reasoning by encouraging step-by-step breakdown of complex problems.
**Doc**: ✓ Strong - Explicitly named in guides
**Test**: Logistics problem w/ 3 warehouses, multi-step moves

**Prompt**:
```
A logistics manager has to move items between three warehouses: A, B, and C.
- Starting state: Warehouse A has 40 units, B has 30, and C has 20.
- Move operations: First, move half of A to B. Second, move one-third of B to C. Third, move one-quarter of C back to A.
Let's think step by step to determine the final number of units in each warehouse.
```

**Output**: Perfect step-by-step breakdown. Step 1: 40/2=20 moved A→B. Correct intermediate calc + final state.

**Analysis**: Correctly executed multi-step reasoning. Broke down problem→sequential steps, showed intermediate calc, arrived at correct final state. Demonstrates CoT is highly effective for this model.

**Scores**: E=10/10 (Perfect step-by-step w/ correct math), R=9/10 (Consistently performs well on logical problems)
```

✅ **What Changed**:
- Headers compressed (Def, Doc, Test not full words)
- Symbols added (✓, →, w/)
- Test description shortened BUT prompt 100% verbatim
- Output condensed BUT key facts preserved
- Analysis complete BUT subjects removed ("The model" → direct statements)
- Score reasoning kept complete

✅ **What Stayed Identical**:
- Every word in the prompt
- All substantive analysis points
- Score justifications (complete reasoning)
- Technical accuracy

### Example 2: WRONG - Over-Compression

**WRONG APPROACH**:
```markdown
### 1. CoT

**Test**: Logistics
**Prompt**: "Warehouse problem, think step by step"
**Output**: Model did well
**Scores**: E=10, R=9
```

❌ **Why This Fails**:
- Prompt destroyed (not reproducible)
- Output summarized (lost technical detail)
- Analysis missing (can't understand why scores given)
- Document now ~40% information retention (FAILED)

## Compression Techniques

### 1. Ultra-Terse Headers
`**Definition**: ` → `**Def**: `
`**Documentation**: ` → `**Doc**: `
`**Example**: ` → `**Ex**: `
`1,332 lines` → `1,332L`
`134 kilobytes` → `134KB`

### 2. Extreme Abbreviations (Prose Only)
`Effectiveness` → `E`
`Reliability` → `R`
`Chain-of-Thought` → `CoT`
`with` → `w/`
`without` → `w/o`
`documentation` → `doc`

**DO NOT use in prompts/code**

### 3. Symbols (Analysis Only)
`passed` → `✓`
`failed` → `✗`
`warning` → `⚠`
`to` → `→`
`increases` → `↑`
`decreases` → `↓`

### 4. Prose→Fragments (Remove Subjects)
`The model's performance was excellent` → `Performance was excellent` or `Excellent perf`
`This approach demonstrates` → `Demonstrates`
`As we can see,` → [delete]
`It should be noted that` → [delete]

**Keep substantive content**

### 5. Table Compression
Headers only: `Effectiveness` → `E`
Keep all data in cells

### 6. Complete Prompts (SACRED)
100% verbatim
Every word exact
No "improvements"
No summaries

### 7. Complete Analysis (FORMAT ONLY)
Keep all reasoning
Remove subjects/filler
Preserve technical substance
Score justifications complete

## Quality Verification

**Information Retention**: 95%+
- [ ] Every test prompt 100% verbatim
- [ ] Every code example 100% exact
- [ ] Model outputs preserve structure + key content
- [ ] Analysis paragraphs complete (format compressed only)
- [ ] Score justifications have full reasoning
- [ ] Can reproduce any test from compressed version

**Compression Metrics**: 85%
- [ ] 19-22KB size  
- [ ] 400-450 lines
- [ ] Headers abbreviated
- [ ] Symbols used (✓✗⚠→)
- [ ] Subjects removed from prose

## Process

1. **Identify sacred content** (mark all prompts/code)
2. **Preserve sacred 100%** (copy verbatim)
3. **Compress format** (headers, symbols, abbreviations)
4. **Keep analysis complete** (remove filler, not substance)
5. **Verify**: Can you reproduce every test? Is reasoning clear?

## Red Flags (Stop & Fix)

❌ **If you see these, you've over-compressed**:
- Prompt phrases changed
- Analysis reduced to bullet points
- Score reasoning missing ("good" instead of "Perfect step-by-step w/ correct math")
- Can't reproduce tests from output
- Feels like <90% retention

## Target Output

- **Size**: 19-22KB (for 130KB original)
- **Lines**: 400-450 (for 1,300L original)
- **Retention**: 95%+ (prompts exact, analysis complete)
- **Format**: Ultra-dense but fully reproducible

Remember: V7 is FORMAT compression, not CONTENT summarization.
