---
name: llm-doc-compression
description: Autonomous V7 compression - compresses technical docs step-by-step with checkpoints and self-correction. Achieves 85% reduction (134KB→22KB) with 95% information retention.
---

# LLM Documentation Compression (Autonomous)

**Version**: 3.0.0 | **Mode**: Autonomous Compression with Checkpoints

## How This Works

I'll compress your document automatically, section by section:
1. Analyze document structure
2. Compress each section following V7 rules
3. Check size after each section
4. Self-correct if over budget
5. Show you the final result

You provide the document, I compress it, you review the result.

---

## Compression Rules

### SACRED CONTENT (0% compression)
**NEVER modify these**:
- Test prompts: 100% verbatim, every word exact
- Code blocks: 100% exact
- Persona descriptions in prompts: Complete
- API examples: Exact
- Technical numbers, calculations: Exact

### OUTPUT COMPRESSION (70% reduction)
**Extract key results only**:
- Keep: Final answer, key numbers, proof of success/failure
- Delete: "Certainly", "Let me", narration, step-by-step elaboration
- Decision question: "Minimum text to prove model succeeded?"

**Example**:
❌ Before (200 chars):
```
Certainly. Let's break down the movement step by step.
**Step 1**: Half of A to B means 40/2 = 20 units moved...
This leaves A with 20 units and gives B 30 + 20 = 50 units.
```

✅ After (40 chars):
```
Perfect step-by-step. S1: 40/2=20 A→B (A=20, B=50). Final: A=50, B=0, C=40.
```

### ANALYSIS COMPRESSION (67% reduction)
**Fragments, no subjects, keep reasoning**:
- Delete subjects: "The model" → start with verb
- Keep reasoning: "broke down problem→sequential steps" 
- Delete filler: "As we can see", "It should be noted"
- Use symbols: "to" → "→", "with" → "w/"

**Example**:
❌ Before: "The model correctly executed multi-step reasoning. It broke down the problem..."
✅ After: "Correctly executed multi-step reasoning. Broke down problem→sequential steps..."

### HEADERS (Ultra-terse)
- **Definition**: → **Def**:
- **Documentation**: → **Doc**:
- **Example**: → **Ex**:
- 1,332 lines → 1,332L
- 134 kilobytes → 134KB

### META-SECTIONS (67% compression)
- Executive summary: 3 sentences max
- Introduction: 2-3 sentences
- Methodology: Key points only

---

## Autonomous Compression Process

When you provide a document, I will:

### PHASE 1: Analysis
```
📊 Document: 134KB, 1,332L → Target: 22KB (84% reduction)

Structure breakdown:
- Exec summary: 3KB → 1KB
- Methodology: 5KB → 1KB
- 10 tests: 115KB → 18KB
- Conclusion: 5KB → 2KB

Sacred content: 15 prompts (~6KB) - preserve verbatim
```

### PHASE 2: Section-by-Section Compression

I'll compress each section and show running total:

```
✅ Executive Summary: 0.9KB ✓
   Target: 1KB | Running: 0.9KB / 22KB (4%)

✅ Methodology: 1.1KB ✓
   Target: 1KB | Running: 2.0KB / 22KB (9%)

✅ Test 1 (CoT): 2.1KB ✓
   Prompt: Verbatim ✓ | Output: Key results ✓ | Analysis: Complete ✓
   Target: 2KB | Running: 4.1KB / 22KB (19%)
```

If any section goes over budget:
```
⚠️ Test 2: 3.5KB (target: 2KB) - OVER
   Compressing output more aggressively...
   ✅ Test 2 (revised): 2.0KB ✓
   Running: 6.1KB / 22KB (28%)
```

### PHASE 3: Final Result

After completing all sections:
```
📊 Compression Complete:
- Final size: 21.8KB (target: 19-22KB) ✓
- Reduction: 83.7% ✓
- All prompts verbatim: ✓
- All analysis has reasoning: ✓
- Can reproduce tests: ✓

[Download compressed document]
```

---

## Standard Test Section Format

For each test, I'll use this format:

```
### [N]. [Name]

**Def**: [1 terse sentence]
**Doc**: [✓/✗/⚠ + brief]
**Test**: [Key requirement]

**Prompt**:
```
[100% VERBATIM - EVERY WORD EXACT]
```

**Output**: [Key results only - no narration]
**Analysis**: [Fragments, no subjects, keep reasoning]
**Scores**: E=[N]/10 ([reasoning]), R=[N]/10 ([reasoning])
```

---

## Size Budgets (for 134KB document)

| Component | Original | Target | Compression |
|-----------|----------|--------|-------------|
| Prompts | 6KB | 6KB | 0% (SACRED) |
| Outputs | 10KB | 3KB | 70% |
| Analysis | 12KB | 4KB | 67% |
| Meta-sections | 15KB | 5KB | 67% |
| Structure | 15KB | 4KB | 73% |

---

## Self-Correction Triggers

I'll automatically compress more if:
- Any section >50% over budget
- Running total >10% ahead of pace
- Output section >0.5KB per test
- Analysis section >0.6KB per test

---

## Quality Checks

After each section:
- ✓ Prompts 100% verbatim
- ✓ Output has key results
- ✓ Analysis has complete reasoning
- ✓ Size within budget

Final verification:
- ✓ Total: 19-22KB
- ✓ Information retention: 95%+
- ✓ All tests reproducible
- ✓ All scores justified

---

## Usage

**Simple**: Attach document and say "compress this"

I'll:
1. Analyze structure
2. Compress section by section
3. Show running total
4. Self-correct if over budget
5. Provide final compressed document

**No manual work required** - I handle the entire compression process autonomously.

---

## Example Output

```
📊 Starting compression of Gemini assessment (134KB → 22KB)...

✅ Executive Summary: 0.9KB ✓ (1/15 sections, 4% complete)
✅ Methodology: 1.0KB ✓ (2/15 sections, 9% complete)
✅ Test 1 (CoT): 2.1KB ✓ (3/15 sections, 19% complete)
✅ Test 2 (Structured Output): 1.9KB ✓ (4/15 sections, 27% complete)
...
✅ All sections complete: 21.8KB ✓

Compression successful! 83.7% reduction with 95%+ retention ✓
```

---

## Start Compressing

Ready? Attach your document and I'll begin the autonomous compression process.
