---
name: llm-doc-compression
description: Intelligent V7 compression with adaptive strategies - evaluates each section, categorizes content type, applies tiered compression rules. Achieves 85% reduction with 95% retention while protecting critical content.
---

# LLM Documentation Compression (Intelligent)

**Version**: 4.0.0 | **Mode**: Adaptive Compression with Section-Level Intelligence

## How This Works

I evaluate each section individually and apply the right strategy:
1. **Analyze section**: Categorize content type
2. **Determine tier**: Apply appropriate compression level
3. **Compress intelligently**: Adapt to content characteristics
4. **Verify quality**: Ensure preservation requirements met
5. **Self-correct**: Adjust if constraints violated

Sections can be mixed-type - I handle each appropriately.

---

## CONTENT CATEGORIZATION SYSTEM

### Section-Level Evaluation

For each section, I evaluate:

**1. Content Type Distribution**
```
Section Analysis:
- Prose: 40% (compressible)
- Code blocks: 30% (sacred)
- Test prompts: 20% (sacred)
- Data tables: 10% (minimal compression)

Classification: MIXED (sacred-heavy)
Tier: 2 (Moderate compression)
```

**2. Information Density**
- **Dense**: Technical specs, formulas, schemas → Minimal compression
- **Medium**: Analysis, explanations → Moderate compression
- **Sparse**: Scaffolding, transitions, meta-commentary → Aggressive compression

**3. Reproduction Criticality**
- **Critical**: Must reproduce exactly (prompts, code, formulas) → 0% compression
- **Important**: Key insights must remain (analysis) → 30-50% compression
- **Supporting**: Context/scaffolding (transitions) → 70-90% compression

---

## TIERED COMPRESSION RULES

### Tier 0: SACRED (0% compression)
**Applied to**:
- Test prompts (every word matters)
- Code blocks (syntax critical)
- Mathematical formulas (precision required)
- API schemas (structure exact)
- Citations (verification required)
- Persona descriptions in prompts (completeness required)

**Rule**: Preserve byte-for-byte, no exceptions

**Example**:
```
Input: "Let's think step by step to determine the final number"
Output: "Let's think step by step to determine the final number"
         [IDENTICAL - 0% compression]
```

### Tier 1: MINIMAL (10-30% compression)
**Applied to**:
- Technical specifications
- Empirical data/results
- Benchmark tables
- Scoring justifications
- Critical analysis with technical detail

**Rule**: Compress format only, preserve all substance

**Allowed**:
- Header abbreviation: "Definition" → "Def"
- Number formatting: "1,332 lines" → "1,332L"
- Symbol substitution: "passed" → "✓"

**Forbidden**:
- Removing data points
- Simplifying technical explanations
- Omitting qualifications/caveats

**Example**:
```
Input: "The model's effectiveness score is 10/10. The output is perfect. 
        It is accurate, well-structured, and fully adheres to all instructions."
Output: "Effectiveness: 10/10. Output perfect: accurate, well-structured, 
         fully adheres to all instructions."
         [~20% compression - all substance preserved]
```

### Tier 2: MODERATE (30-60% compression)
**Applied to**:
- Analysis sections (mixed substance + scaffolding)
- Methodology explanations
- Test descriptions
- Findings summaries

**Rule**: Remove scaffolding, keep insights in fragments

**Allowed**:
- Subject removal: "The model executed" → "Executed"
- Filler deletion: "As we can see", "It should be noted"
- Transition removal: "Furthermore", "Additionally"
- Fragment conversion: Full sentences → noun phrases

**Forbidden**:
- Removing core insights
- Omitting reasoning steps
- Simplifying technical arguments

**Example**:
```
Input: "The model's performance on this task is excellent. Each agent 
        maintained its distinct persona, tone, and viewpoint throughout 
        all three rounds. This demonstrates strong contextual awareness."
Output: "Performance excellent. Each agent maintained distinct persona/tone/
         viewpoint across rounds. Demonstrates strong contextual awareness."
         [~40% compression - all insights preserved]
```

### Tier 3: AGGRESSIVE (60-90% compression)
**Applied to**:
- Executive summaries (overview only)
- Introductions (context setting)
- Meta-commentary (about the document itself)
- Transitional prose
- Scaffolding text

**Rule**: Extract essence only, delete elaboration

**Allowed**:
- Severe condensing: Multi-paragraph → 1-3 sentences
- Telegraphic style: "Assessment of X. Findings: Y. Conclusion: Z."
- Maximum abbreviation and symbols

**Forbidden**:
- Losing key conclusions
- Omitting critical context
- Making content incomprehensible

**Example**:
```
Input: "This report presents a systematic, evidence-based self-assessment 
        of the Gemini 2.5 Pro large language model, with a specific focus 
        on its capacity to execute advanced prompting techniques within a 
        single-shot, non-conversational context. [continues 200 words...]"
Output: "Systematic assessment: Gemini 2.5 Pro advanced prompting in 
         single-shot execution. Exceptional on native API features, strong 
         on emergent capabilities. Optimal for complex single-shot tasks."
         [~85% compression - core message preserved]
```

---

## INTELLIGENT SECTION ANALYSIS

### Mixed-Content Handling

When a section contains multiple content types:

**Example Section**:
```
Title: "Chain-of-Thought Prompting"
- Definition paragraph (Tier 2: 40% compression)
- Documentation citations (Tier 1: 20% compression)
- Test prompt (Tier 0: 0% compression)
- Model output (Tier 2-3: 50-70% compression)
- Analysis (Tier 2: 40% compression)
- Scores with reasoning (Tier 1: 20% compression)
```

**My approach**:
```
Processing: Test Section #1
✓ Definition: Tier 2 applied (40% reduction)
✓ Citations: Tier 1 applied (20% reduction)
✓ Prompt: Tier 0 applied (0% - preserved verbatim)
✓ Output: Tier 3 applied (70% - key results only)
✓ Analysis: Tier 2 applied (40% - fragments, kept insights)
✓ Scores: Tier 1 applied (20% - full reasoning preserved)

Section result: 2.1KB (from 5KB, 58% reduction)
```

### Adaptive Decision-Making

**I evaluate each paragraph**:

```
Paragraph 1: "The model executed the CoT prompt flawlessly..."
- Type: Analysis
- Density: Medium (some scaffolding, some insight)
- Criticality: Important (explains score)
→ TIER 2: Remove subjects, keep insights

Paragraph 2: "**Prompt**: A logistics manager has to move items..."
- Type: Test prompt
- Density: N/A (sacred)
- Criticality: Critical (must reproduce)
→ TIER 0: Preserve 100% verbatim

Paragraph 3: "Certainly. Let's break down the movement..."
- Type: Model output
- Density: Sparse (narration heavy)
- Criticality: Supporting (proof needed, not narration)
→ TIER 3: Extract key results only
```

---

## SAFETY CHECKS & CONSTRAINTS

### Pre-Compression Analysis

**1. Document-Level Check**:
```
📊 Document Analysis:
- Total size: 134KB
- Sacred content: 7KB (5%)
- Compressible: 127KB (95%)
- Target reduction: 84%

✓ Document suitable for compression
```

**2. Section-Level Check**:
```
Section: Test #3
- Prompt: 0.8KB (Tier 0)
- Output: 2.5KB (Tier 3 candidate)
- Analysis: 1.2KB (Tier 2)

✓ Sacred content identified and protected
```

### Post-Compression Verification

**Tier 0 Verification** (Critical):
```
Verifying sacred content:
✓ Prompt #1: Byte-for-byte match
✓ Prompt #2: Byte-for-byte match
✓ Code block #1: Byte-for-byte match
...

Result: All Tier 0 content verified identical
```

**Tier 1 Verification** (Important):
```
Verifying technical content:
✓ All data points preserved
✓ All scores have complete reasoning
✓ All qualifications retained

Result: Minimal compression successful
```

**Tier 2-3 Verification** (Supporting):
```
Verifying insight preservation:
✓ All key insights present
✓ All conclusions readable
✓ Document coherent

Result: Aggressive compression successful
```

---

## COMPRESSION WORKFLOW

### Phase 1: Document Analysis
```
📊 Analyzing: Gemini_Assessment.md (134KB)

Content Distribution:
- Sacred (Tier 0): 7KB (5%)
- Technical (Tier 1): 25KB (19%)
- Analysis (Tier 2): 55KB (41%)
- Prose (Tier 3): 47KB (35%)

Compression Strategy:
- Target: 22KB (84% reduction)
- Approach: Tiered (preserve sacred, aggressive on prose)
- Estimated: ~21.5KB ±2KB
```

### Phase 2: Section-by-Section Processing
```
Processing Section 1/15: Executive Summary
- Classification: Tier 3 (meta-commentary)
- Original: 3KB
- Target: ~1KB (67% reduction)
- Result: 0.9KB ✓

Processing Section 2/15: Test #1 (CoT)
- Prompt: Tier 0 → 0.8KB (0% reduction) ✓
- Output: Tier 3 → 0.4KB (80% reduction) ✓
- Analysis: Tier 2 → 0.6KB (40% reduction) ✓
- Scores: Tier 1 → 0.3KB (20% reduction) ✓
- Total: 2.1KB ✓

Running total: 3.0KB / 22KB (14%)
```

### Phase 3: Quality Verification
```
📊 Compression Complete: Quality Check

Tier 0 (Sacred):
✓ 12/12 prompts: Byte-for-byte identical
✓ 8/8 code blocks: Unchanged
✓ 5/5 formulas: Exact

Tier 1 (Technical):
✓ All data preserved
✓ All reasoning complete
✓ All scores justified

Tier 2-3 (Analysis/Prose):
✓ All insights present
✓ Document coherent
✓ Conclusions clear

Final: 21.8KB (83.7% reduction) ✓
Information retention: 95%+ ✓
```

---

## ADAPTIVE RULES

### Context-Sensitive Compression

**Rule 1: Sacred Content in Tier 2 Section**
```
If section is Tier 2 BUT contains Tier 0 element:
→ Extract Tier 0, compress remainder

Example:
Section: Analysis with embedded code
- Analysis prose: Tier 2 (40% compression)
- Code snippet: Tier 0 (0% compression)
→ Compress analysis, preserve code exactly
```

**Rule 2: High-Density Tier 3 Section**
```
If section is Tier 3 BUT information-dense:
→ Upgrade to Tier 2

Example:
Executive summary with critical technical specs
- Usually: Tier 3 (70% compression)
- This case: Tier 2 (40% compression)
→ Preserve technical accuracy
```

**Rule 3: Low-Value Tier 1 Section**
```
If section is Tier 1 BUT redundant/obvious:
→ Downgrade to Tier 2

Example:
Methodology section repeating standard practices
- Usually: Tier 1 (20% compression)
- This case: Tier 2 (40% compression)
→ Remove obviousness, keep novel points
```

### Budget Adaptation

**If section exceeds budget**:
```
Test #5: 2.8KB (target: 2KB) - OVER by 40%

Analyzing composition:
- Output: 1.2KB (should be 0.4KB) → Tier 3 not aggressive enough
- Analysis: 0.8KB (appropriate) → Leave as-is

Action: Re-compress output with stricter Tier 3 rules
Result: 2.0KB ✓
```

---

## EXAMPLE: INTELLIGENT PROCESSING

### Input Section (5KB)
```
### Chain-of-Thought (CoT) Prompting

#### Definition
Chain-of-Thought (CoT) prompting is a technique designed to improve 
the reasoning abilities of large language models by encouraging them 
to break down complex problems into a sequence of intermediate, 
logical steps.

#### Documentation Support
Official Google AI documentation provides strong support for CoT...

#### Practical Test Design
The test is designed to assess the model's ability to perform 
zero-shot CoT reasoning...

**Prompt:**
A logistics manager has to move items between three warehouses...
[full 200-word prompt]

#### Test Execution and Analysis
**Model Output:**
Certainly. Let's break down the movement step by step.
[full 400-word output with calculations]

Analysis:
The model executed the CoT prompt flawlessly. It correctly 
interpreted the instruction and adopted a sequential approach...
[full 150-word analysis]

#### Scoring
- Effectiveness: 10/10. The output is perfect. It is accurate...
- Reliability: 10/10. This is a foundational capability...
```

### Intelligent Processing
```
Evaluating section components:

1. Definition paragraph:
   - Type: Explanatory prose
   - Density: Medium
   - Criticality: Supporting
   → TIER 2: 40% compression

2. Documentation paragraph:
   - Type: Citations
   - Density: Medium-High
   - Criticality: Important (evidence)
   → TIER 1: 20% compression

3. Test design paragraph:
   - Type: Scaffolding
   - Density: Low
   - Criticality: Supporting
   → TIER 3: 70% compression

4. Prompt:
   - Type: Test prompt
   - Density: N/A
   - Criticality: CRITICAL
   → TIER 0: 0% compression (PRESERVE VERBATIM)

5. Model output:
   - Type: Result demonstration
   - Density: Low (heavy narration)
   - Criticality: Supporting (proof needed, not narration)
   → TIER 3: 80% compression (extract key results)

6. Analysis:
   - Type: Technical analysis
   - Density: Medium
   - Criticality: Important (justifies score)
   → TIER 2: 40% compression

7. Scores with reasoning:
   - Type: Evaluation with justification
   - Density: High
   - Criticality: Important
   → TIER 1: 20% compression
```

### Output Section (2.1KB)
```
### 1. Chain-of-Thought (CoT)

**Def**: Break complex → intermediate logical steps. Encourage "think step by step."

**Doc**: ✓ Strong - Explicitly named in guides, native Thinking architecture

**Test**: Logic puzzle - warehouse inventory tracking w/ multi-step moves

**Prompt**:
```
A logistics manager has to move items between three warehouses: A, B, and C.
- Starting state: Warehouse A has 40 units, B has 30, and C has 20.
- Step 1: Move half of the units from A to B.
- Step 2: Move 10 units from C to A.
- Step 3: Evenly distribute all units currently in B among A and C.
- Step 4: Move 5 units from A to C.

Let's think step by step to determine the final number of units in each warehouse. Show your calculations for each step before providing the final answer.
```

**Output**: Perfect step-by-step. S1: 40/2=20 A→B (A=20, B=50). S2: 10 C→A (A=30, C=10). S3: Distribute B to A&C (A=55, B=0, C=35). S4: 5 A→C. Final: A=50, B=0, C=40.

**Analysis**: Flawlessly executed CoT. Correctly interpreted "think step by step," adopted sequential approach. Each step calculated correctly, state tracked accurately. Exceptionally well-structured output. Native Thinking architecture highly attuned to this instruction type.

**Scores**: E=10/10 (Perfect: accurate, well-structured, fully adheres to instructions), R=10/10 (Foundational capability, consistently high-quality on logic puzzles)
```

### Compression Breakdown
```
Component breakdown:
- Definition: 80 chars (from 200, Tier 2: 60% reduction)
- Documentation: 70 chars (from 150, Tier 1: 53% reduction)
- Test design: 60 chars (from 180, Tier 3: 67% reduction)
- Prompt: 450 chars (from 450, Tier 0: 0% reduction) ✓
- Output: 180 chars (from 1200, Tier 3: 85% reduction)
- Analysis: 280 chars (from 500, Tier 2: 44% reduction)
- Scores: 150 chars (from 250, Tier 1: 40% reduction)

Total: 2.1KB (from 5KB, 58% reduction)
Sacred content preserved: ✓
Information retention: 95%+ ✓
```

---

## USAGE

Attach document and say "compress this"

I will:
1. Analyze entire document structure
2. Categorize each section by content type
3. Apply appropriate tier rules adaptively
4. Self-correct if constraints violated
5. Verify sacred content preservation
6. Deliver compressed document with quality report

**No manual work required** - fully autonomous with intelligent adaptation.

---

## START COMPRESSING

Ready? Provide your document and I'll intelligently compress it using tiered, adaptive strategies while protecting all critical content.
