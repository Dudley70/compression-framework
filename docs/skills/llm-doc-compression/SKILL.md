---
name: llm-doc-compression
description: Autonomous V7 compression with safety checks - compresses technical docs while preserving sacred content and detecting pre-compressed documents. Achieves 85% reduction (134KB→22KB) with 95% information retention.
---

# LLM Documentation Compression (Autonomous)

**Version**: 3.1.0 | **Mode**: Autonomous Compression with Safety Checks

## How This Works

I'll compress your document automatically with built-in safety:
1. **Safety check**: Verify document needs compression
2. **Analyze**: Document structure and sacred content
3. **Compress**: Section by section with checkpoints
4. **Verify**: Quality and completeness
5. **Deliver**: Final compressed document

---

## CRITICAL SAFETY CHECKS

### Before Starting Compression

I will check for:

**1. Already Compressed Documents**
- Ultra-terse headers (Def:, Doc:, Ex:)
- Heavy symbol use (✓✗⚠→)
- Fragment-style prose (no subjects)
- Size already in target range (19-25KB)

**If detected**: 
```
⚠️ SAFETY CHECK FAILED
This document appears already compressed (V7 format detected).
- Size: 22KB (already in target range)
- Format: Uses V7 conventions (Def:, →, fragments)
- Recommendation: Document does not need compression

Proceed anyway? (This may damage the document)
```

**2. Documents That Shouldn't Be Compressed**
- Pure code files (no prose to compress)
- Already minimal documentation
- Files <10KB (compression overhead not worth it)
- Binary/non-text content

**If detected**:
```
⚠️ SAFETY CHECK FAILED
This document may not be suitable for V7 compression:
- Type: Pure code file / minimal doc
- Size: 8KB (below minimum threshold)
- Recommendation: Document too small to benefit

Proceed anyway?
```

**3. Sacred Content Detection**
I will identify and mark:
- Test prompts (exact preservation required)
- Code blocks (exact preservation required)
- Persona descriptions (complete preservation required)
- API examples (exact preservation required)
- Mathematical formulas (exact preservation required)
- Citations/references (exact preservation required)

**Safety guarantee**:
```
✓ Sacred Content Detected: 15 items (~7KB)
  - 12 test prompts
  - 8 code blocks
  - 3 persona descriptions
  
These will be preserved 100% verbatim.
```

---

## Compression Rules

### SACRED CONTENT (0% compression)
**NEVER modify these**:
- Test prompts: 100% verbatim, every word exact
- Code blocks: 100% exact
- Persona descriptions: Complete
- API examples: Exact
- Mathematical formulas: Exact
- Citations: Exact
- Schema definitions: Exact

**Verification after compression**:
- All prompts byte-for-byte identical ✓
- All code blocks unchanged ✓
- All formulas preserved ✓

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

### PHASE 1: Safety Checks
```
🔍 Safety Analysis:

✓ Document size: 134KB (compression recommended)
✓ Format: Uncompressed (verbose prose detected)
✓ Content type: Technical assessment (suitable)
✓ Sacred content: 15 items identified for preservation

Proceeding with compression...
```

OR if issues detected:
```
⚠️ SAFETY ISSUE DETECTED:
- Document appears pre-compressed (V7 format)
- Size: 22KB (already optimal)
- Symbols: Heavy use of ✓✗⚠→

Recommendation: Skip compression (may damage document)

Options:
1. Cancel (recommended)
2. Proceed anyway (may degrade quality)

Please confirm your choice.
```

### PHASE 2: Structure Analysis
```
📊 Document: 134KB, 1,332L → Target: 22KB (84% reduction)

Structure breakdown:
- Exec summary: 3KB → 1KB
- Methodology: 5KB → 1KB
- 10 tests: 115KB → 18KB
- Conclusion: 5KB → 2KB

Sacred content (PRESERVE 100%):
- 12 test prompts (~6KB)
- 8 code blocks (~1KB)
```

### PHASE 3: Section-by-Section Compression

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

### PHASE 4: Quality Verification

After completing all sections:
```
📊 Compression Complete - Quality Verification:

Size Check:
✓ Final size: 21.8KB (target: 19-22KB)
✓ Reduction: 83.7%

Sacred Content Verification:
✓ All 12 prompts preserved verbatim (byte-for-byte match)
✓ All 8 code blocks unchanged
✓ All formulas exact

Information Retention:
✓ All test reproducible from compressed version
✓ All scores have complete reasoning
✓ All analysis preserves core insights

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

## Error Handling

**If compression would damage document**:
```
❌ COMPRESSION ABORTED

Reason: Sacred content exceeds 30% of document
- Document: 40KB
- Sacred content: 15KB (37%)
- Compressible content: 25KB

Compression would yield minimal benefit (only 10KB reduction possible)
while risking sacred content integrity.

Recommendation: Document not suitable for V7 compression.
```

**If sacred content gets modified**:
```
❌ QUALITY CHECK FAILED

Verification detected sacred content modification:
- Test prompt #3: Changed "step by step" to "stepwise"
- Code block #5: Indentation altered

Reverting to original. Retrying with stronger preservation rules...
```

---

## Usage

**Simple**: Attach document and say "compress this"

I'll:
1. ✓ Run safety checks
2. ✓ Identify sacred content
3. ✓ Compress section by section
4. ✓ Verify all sacred content preserved
5. ✓ Deliver final compressed document

**If safety issues detected**: I'll warn you and ask permission before proceeding.

---

## Example Output (Success)

```
🔍 Safety Check: ✓ Document suitable for compression

📊 Starting compression: 134KB → 22KB target
   Sacred content: 12 prompts, 8 code blocks (preserve 100%)

✅ Executive Summary: 0.9KB ✓ (1/15 sections, 4% complete)
✅ Methodology: 1.0KB ✓ (2/15 sections, 9% complete)
✅ Test 1 (CoT): 2.1KB ✓ (3/15 sections, 19% complete)
   - Prompt preserved: ✓ Byte-for-byte match
...

📊 Quality Verification:
✓ Size: 21.8KB (83.7% reduction)
✓ All sacred content verified identical
✓ Information retention: 95%+

Compression successful!
```

## Example Output (Safety Warning)

```
🔍 Safety Check: ⚠️ Issues detected

Document appears pre-compressed:
- Size: 22KB (already in target range)
- Format: V7 conventions detected (Def:, →, symbols)
- Headers: Already ultra-terse

⚠️ RECOMMENDATION: Skip compression

This document is already optimally compressed. Further compression
may reduce readability without meaningful size benefit.

Options:
1. Cancel (recommended)
2. Proceed anyway (not recommended)

Please confirm your choice.
```

---

## Start Compressing

Ready? Attach your document and I'll:
1. Run safety checks
2. Identify sacred content
3. Compress autonomously if safe
4. Deliver final result with verification
