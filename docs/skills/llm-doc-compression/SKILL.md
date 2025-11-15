---
name: llm-doc-compression
description: Intelligent V7 compression with adaptive strategies - evaluates each section, categorizes content type, applies tiered compression rules. Achieves 85% reduction with 95% retention while protecting critical content.
---

# LLM Documentation Compression (Intelligent)

**Version**: 4.1.0 | **Mode**: Adaptive Compression with Enforced Sacred Content Protection

## How This Works

I evaluate each section individually and apply the right strategy:
1. **Analyze section**: Categorize content type
2. **Determine tier**: Apply appropriate compression level
3. **Compress intelligently**: Adapt to content characteristics
4. **Verify quality**: Ensure preservation requirements met
5. **Self-correct**: Adjust if constraints violated

Sections can be mixed-type - I handle each appropriately.

---

## ⚠️ CRITICAL: TIER 0 SACRED CONTENT ENFORCEMENT

### MANDATORY DETECTION TRIGGERS

**STOP COMPRESSION IMMEDIATELY when you encounter ANY of these markers:**

1. **Test Prompt Headers**:
   - `**Prompt**:`
   - `**Test Prompt**:`
   - `**Input**:`
   - `#### Test Execution` followed by `**Prompt**:` or code fence

2. **Code Fences After Test Descriptions**:
   - Three backticks (```) appearing after phrases like:
     - "test is designed to"
     - "practical test"
     - "assess the model's ability"
   - These contain test prompts that MUST be preserved verbatim

3. **Instruction Patterns in Tests**:
   - Text beginning with:
     - "Your task is to..."
     - "Given the following..."
     - "Let's think step by step..."
     - "Analyze the following..."

4. **Code Blocks**:
   - Any ``` fenced code (Python, JavaScript, SQL, etc.)
   - Inline code in technical specs
   - API examples, schemas, configurations

5. **Mathematical Content**:
   - Formulas with symbols (σ, γ, κ, equations)
   - Statistical expressions
   - Algorithmic notation

### SACRED CONTENT PRESERVATION PROTOCOL

**When you detect sacred content:**

```
DETECTED: Test prompt at line 147
ACTION REQUIRED: COPY VERBATIM

DO NOT:
❌ Paraphrase or summarize
❌ Remove "unnecessary" words
❌ Shorten for brevity
❌ Reformat or restructure
❌ Change ANY characters

DO:
✅ Copy EXACTLY character-for-character
✅ Preserve ALL whitespace
✅ Keep ALL formatting
✅ Maintain line breaks
✅ Verify byte-for-byte match

CRITICAL: If you change even ONE character, Rule 6 is violated and the compression has FAILED.
The test cannot be reproduced. This is not a suggestion - it's a hard requirement.
```

### WHY THIS MATTERS

**Test prompts must be reproducible**:
- Researchers need to run the same test
- Results must be verifiable
- Comparison across models requires identical inputs
- Changing "warehouse manager" to "logistics manager" = DIFFERENT TEST

**This is non-negotiable**: Tier 0 preservation is the #1 priority. If in doubt, preserve verbatim.

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

### Tier 0: SACRED (0% compression) ⚠️ ABSOLUTE PRIORITY

**Applied to**:
- ✋ **Test prompts** - DETECTED by headers/fences (see enforcement above)
- ✋ **Code blocks** - ANY ``` fenced content
- ✋ **Mathematical formulas** - Equations, symbols (σ,γ,κ), expressions
- ✋ **API schemas** - JSON/YAML structure definitions
- ✋ **Citations** - Author, year, page numbers (verification required)
- ✋ **Persona descriptions in prompts** - Character definitions in tests

**ENFORCEMENT RULE**:
```
IF content matches ANY Tier 0 trigger:
  → COPY VERBATIM (no processing)
  → MARK as "[SACRED - PRESERVED]" in verification
  → COUNT for post-compression check
ELSE:
  → Proceed with tier evaluation
```

**Example**:
```
✅ CORRECT:
Input:  "Let's think step by step to determine the final number"
Output: "Let's think step by step to determine the final number"
        [SACRED - PRESERVED] ✓

❌ INCORRECT:
Input:  "Let's think step by step to determine the final number"
Output: "Think step-by-step for final number"
        [MODIFIED - RULE 6 VIOLATED] ✗
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
- Test prompt (Tier 0: 0% compression) ⚠️ SACRED
- Model output (Tier 2-3: 50-70% compression)
- Analysis (Tier 2: 40% compression)
- Scores with reasoning (Tier 1: 20% compression)
```

**My approach**:
```
Processing: Test Section #1
✓ Definition: Tier 2 applied (40% reduction)
✓ Citations: Tier 1 applied (20% reduction)
⚠️ PROMPT DETECTED: Tier 0 enforcement activated
  → Prompt: COPIED VERBATIM (0% - preserved byte-for-byte)
  → Marked: [SACRED - PRESERVED] ✓
✓ Output: Tier 3 applied (70% - key results only)
✓ Analysis: Tier 2 applied (40% - fragments, kept insights)
✓ Scores: Tier 1 applied (20% - full reasoning preserved)

Section result: 2.1KB (from 5KB, 58% reduction)
Sacred content: 1 prompt preserved (0.8KB)
```

### Adaptive Decision-Making

**I evaluate each paragraph**:

```
Paragraph 1: "The model executed the CoT prompt flawlessly..."
- Type: Analysis
- Density: Medium (some scaffolding, some insight)
- Criticality: Important (explains score)
- TIER 0 CHECK: No triggers detected ✓
→ TIER 2: Remove subjects, keep insights

Paragraph 2: "**Prompt**: A logistics manager has to move items..."
- TIER 0 TRIGGER DETECTED: "**Prompt**:" header ⚠️
- ACTION: STOP COMPRESSION
- COPY VERBATIM: Starting from "A logistics manager..." until end marker
- VERIFY: Character count matches (487 chars = 487 chars) ✓
→ TIER 0: 0% compression [SACRED - PRESERVED]

Paragraph 3: "Certainly. Let's break down the movement..."
- Type: Model output
- Density: Sparse (narration heavy)
- Criticality: Supporting (proof needed, not narration)
- TIER 0 CHECK: No triggers detected ✓
→ TIER 3: Extract key results only
```

---

## SAFETY CHECKS & VERIFICATION

### Pre-Compression Analysis

**1. Document-Level Check**:
```
📊 Document Analysis:
- Total size: 134KB
- Sacred content detected: 12 test prompts, 8 code blocks (7KB total, 5%)
- Compressible: 127KB (95%)
- Target reduction: 84%

✓ Document suitable for compression
⚠️ Sacred content flagged for 0% compression
```

**2. Section-Level Check**:
```
Section: Test #3
- ⚠️ PROMPT DETECTED at line 147 (0.8KB - Tier 0)
- Output: 2.5KB (Tier 3 candidate)
- Analysis: 1.2KB (Tier 2)

✓ Sacred content identified and protected
Action: Preserve prompt verbatim, compress remainder
```

### POST-COMPRESSION VERIFICATION (MANDATORY)

**Step 1: Count Sacred Elements**
```
VERIFICATION CHECKPOINT 1: Sacred Content Count

Original document scan:
- Test prompts (**Prompt**: headers): 12 found
- Code blocks (``` fences): 8 found
- Formulas (σ,γ,κ symbols): 5 found
- Total Tier 0 elements: 25

Compressed document scan:
- Test prompts (**Prompt**: headers): 12 found ✓
- Code blocks (``` fences): 8 found ✓
- Formulas (σ,γ,κ symbols): 5 found ✓
- Total Tier 0 elements: 25 ✓

STATUS: ✅ PASS - All sacred elements present
```

**Step 2: Byte-for-Byte Verification**
```
VERIFICATION CHECKPOINT 2: Content Integrity

Prompt #1 comparison:
Original:  "A logistics manager has to move..." (487 chars)
Compressed: "A logistics manager has to move..." (487 chars)
Match: ✅ BYTE-FOR-BYTE IDENTICAL

Prompt #2 comparison:
Original:  "You are a creative director..." (623 chars)
Compressed: "You are a creative director..." (623 chars)
Match: ✅ BYTE-FOR-BYTE IDENTICAL

[Repeats for all 12 prompts]

STATUS: ✅ PASS - All prompts verified identical
```

**Step 3: Failure Handling**
```
IF verification fails:
  ABORT compression
  REPORT:
    "❌ VERIFICATION FAILED
    
    Sacred content mismatch detected:
    - Expected: 12 prompts
    - Found: 11 prompts
    - Missing: Prompt #7 (Test 7: Multi-Agent)
    
    This means Rule 6 has been violated.
    The compression cannot be used for test reproduction.
    
    Retry? [Yes/No]"
    
  WAIT for user decision
  IF Yes: Reprocess with stricter Tier 0 enforcement
  IF No: Return original document unchanged
```

---

## COMPRESSION WORKFLOW

### Phase 1: Document Analysis
```
📊 Analyzing: Gemini_Assessment.md (134KB)

Step 1: Scan for Tier 0 triggers
- ⚠️ Found: 12 test prompts (6.2KB)
- ⚠️ Found: 8 code blocks (0.8KB)
- ⚠️ Found: 5 formulas (0.1KB)
- Total sacred: 7.1KB (5.3%)

Step 2: Categorize remaining content
- Technical (Tier 1): 25KB (19%)
- Analysis (Tier 2): 55KB (41%)
- Prose (Tier 3): 47KB (35%)

Compression Strategy:
- Tier 0: 7.1KB → 7.1KB (0% reduction) ⚠️ PROTECTED
- Tier 1: 25KB → 20KB (20% reduction)
- Tier 2: 55KB → 25KB (55% reduction)
- Tier 3: 47KB → 8KB (83% reduction)
- Target: ~22KB (83.5% overall reduction)
```

### Phase 2: Section-by-Section Processing
```
Processing Section 1/15: Executive Summary
- Classification: Tier 3 (meta-commentary)
- Tier 0 scan: No triggers ✓
- Original: 3KB
- Target: ~1KB (67% reduction)
- Result: 0.9KB ✓

Processing Section 2/15: Test #1 (CoT)
- Tier 0 scan: ⚠️ PROMPT DETECTED at line 89
  → Prompt: COPIED VERBATIM → 0.8KB (0%) [SACRED - PRESERVED] ✓
- Output: Tier 3 → 0.4KB (80% reduction) ✓
- Analysis: Tier 2 → 0.6KB (40% reduction) ✓
- Scores: Tier 1 → 0.3KB (20% reduction) ✓
- Total: 2.1KB (sacred: 0.8KB preserved) ✓

Running total: 3.0KB / 22KB (14%)
Sacred elements preserved: 1/12 prompts ✓
```

### Phase 3: Verification & Delivery
```
📊 Compression Complete: VERIFICATION IN PROGRESS

CHECKPOINT 1: Sacred Content Count
✅ All Tier 0 elements present (25/25)

CHECKPOINT 2: Byte-for-Byte Verification
✅ All prompts verified identical (12/12)
✅ All code blocks unchanged (8/8)
✅ All formulas exact (5/5)

CHECKPOINT 3: Quality Metrics
✅ All insights present (manual review)
✅ Document coherent
✅ Conclusions clear

Final: 22.1KB (83.5% reduction) ✓
Information retention: 95%+ ✓
Rule 6 compliance: ✅ VERIFIED

🎯 COMPRESSION SUCCESSFUL - READY FOR DELIVERY
```

---

## ADAPTIVE RULES

### Context-Sensitive Compression

**Rule 1: Sacred Content in Tier 2 Section**
```
If section is Tier 2 BUT contains Tier 0 trigger:
→ Extract sacred content (0%), compress remainder

Example:
Section: Analysis with embedded code
- Tier 0 scan: ⚠️ Code block detected
- Analysis prose: Tier 2 (40% compression)
- Code snippet: Tier 0 (0% compression) [SACRED - PRESERVED]
→ Result: Mixed compression with sacred preservation
```

**Rule 2: High-Density Tier 3 Section**
```
If section is Tier 3 BUT information-dense:
→ Upgrade to Tier 2

Example:
Executive summary with critical technical specs
- Default: Tier 3 (70% compression)
- Detected: High technical density
- Upgrade: Tier 2 (40% compression)
→ Preserve technical accuracy
```

**Rule 3: Ambiguous Content**
```
If uncertain whether content is Tier 0:
→ Default to preservation (Tier 0)

Example:
Unclear if text is test prompt or description
- Uncertain: Could be either
- Safety-first: Treat as Tier 0
→ Preserve verbatim (better safe than sorry)
```

### Budget Adaptation with Sacred Protection

**If section exceeds budget DUE TO sacred content**:
```
Test #5: 2.8KB (target: 2KB) - OVER by 40%

Analyzing composition:
- Prompt (Tier 0): 1.2KB [SACRED - CANNOT COMPRESS]
- Output: 0.8KB (should be 0.4KB)
- Analysis: 0.8KB (appropriate)

Action: Accept overage OR re-compress output more aggressively
Decision: Accept 2.8KB (sacred content takes precedence)
```

**If section exceeds budget WITHOUT sacred content**:
```
Analysis section: 3.2KB (target: 2KB) - OVER by 60%

- No Tier 0 content detected
- All Tier 2 (analysis prose)

Action: Re-compress with stricter Tier 2→3 rules
Result: 2.0KB ✓
```

---

## EXAMPLE: INTELLIGENT PROCESSING WITH ENFORCEMENT

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
```
A logistics manager has to move items between three warehouses: A, B, and C.
- Starting state: Warehouse A has 40 units, B has 30, and C has 20.
- Step 1: Move half of the units from A to B.
- Step 2: Move 10 units from C to A.
- Step 3: Evenly distribute all units currently in B among A and C.
- Step 4: Move 5 units from A to C.

Let's think step by step to determine the final number of units in each warehouse. Show your calculations for each step before providing the final answer.
```

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

### Intelligent Processing with Enforcement
```
SECTION SCAN: Chain-of-Thought Test

Step 1: Tier 0 Detection
⚠️ TRIGGER FOUND: "**Prompt:**" at line 147
⚠️ CODE FENCE DETECTED: ``` after "Practical Test Design"
→ SACRED CONTENT IDENTIFIED: 450 characters
→ ACTION: Mark for 0% compression

Step 2: Component Categorization

1. Definition paragraph (lines 1-15):
   - Tier 0 scan: No triggers ✓
   - Type: Explanatory prose
   - Density: Medium
   - Criticality: Supporting
   → TIER 2: 40% compression

2. Documentation paragraph (lines 16-25):
   - Tier 0 scan: No triggers ✓
   - Type: Citations
   - Density: Medium-High
   - Criticality: Important (evidence)
   → TIER 1: 20% compression

3. Test design paragraph (lines 26-35):
   - Tier 0 scan: No triggers ✓
   - Type: Scaffolding
   - Density: Low
   - Criticality: Supporting
   → TIER 3: 70% compression

4. PROMPT SECTION (lines 36-50):
   - ⚠️ TIER 0 ENFORCEMENT ACTIVATED
   - Detection: "**Prompt:**" header + ``` fence
   - Content: 450 characters
   → TIER 0: COPY VERBATIM [SACRED - PRESERVED]
   → Verification: Character count = 450 ✓

5. Model output (lines 51-120):
   - Tier 0 scan: No triggers (output, not input)
   - Type: Result demonstration
   - Density: Low (heavy narration)
   - Criticality: Supporting (proof needed, not narration)
   → TIER 3: 80% compression (extract key results)

6. Analysis (lines 121-145):
   - Tier 0 scan: No triggers ✓
   - Type: Technical analysis
   - Density: Medium
   - Criticality: Important (justifies score)
   → TIER 2: 40% compression

7. Scores with reasoning (lines 146-160):
   - Tier 0 scan: No triggers ✓
   - Type: Evaluation with justification
   - Density: High
   - Criticality: Important
   → TIER 1: 20% compression

Step 3: Execute Compression
[Processing each component with appropriate tier...]

Step 4: Section Verification
✅ Sacred content check: 1 prompt preserved (450 chars)
✅ Character match: Original 450 = Compressed 450
✅ All insights retained
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
[SACRED - PRESERVED] ✓

**Output**: Perfect step-by-step. S1: 40/2=20 A→B (A=20, B=50). S2: 10 C→A (A=30, C=10). S3: Distribute B to A&C (A=55, B=0, C=35). S4: 5 A→C. Final: A=50, B=0, C=40.

**Analysis**: Flawlessly executed CoT. Correctly interpreted "think step by step," adopted sequential approach. Each step calculated correctly, state tracked accurately. Exceptionally well-structured output. Native Thinking architecture highly attuned to this instruction type.

**Scores**: E=10/10 (Perfect: accurate, well-structured, fully adheres to instructions), R=10/10 (Foundational capability, consistently high-quality on logic puzzles)
```

### Verification Report
```
SECTION VERIFICATION COMPLETE:

Sacred Content:
✅ Prompt preserved verbatim (450 chars = 450 chars)
✅ Byte-for-byte match confirmed
✅ Rule 6 compliance: VERIFIED

Compression Results:
- Definition: 80 chars (from 200, Tier 2: 60% reduction)
- Documentation: 70 chars (from 150, Tier 1: 53% reduction)
- Test design: 60 chars (from 180, Tier 3: 67% reduction)
- Prompt: 450 chars (from 450, Tier 0: 0% reduction) [SACRED] ✓
- Output: 180 chars (from 1200, Tier 3: 85% reduction)
- Analysis: 280 chars (from 500, Tier 2: 44% reduction)
- Scores: 150 chars (from 250, Tier 1: 40% reduction)

Total: 2.1KB (from 5KB, 58% overall reduction)
Sacred preservation: ✅ VERIFIED
Information retention: 95%+ ✓
Status: ✅ READY FOR DELIVERY
```

---

## USAGE

Attach document and say "compress this"

I will:
1. Scan for Tier 0 triggers (prompts, code, formulas)
2. Mark sacred content for 0% compression
3. Categorize remaining sections by content type
4. Apply appropriate tier rules adaptively
5. Preserve all sacred content VERBATIM
6. Verify byte-for-byte preservation
7. Self-correct if verification fails
8. Deliver compressed document with quality report

**Sacred content is ABSOLUTELY PROTECTED** - Rule 6 compliance is mandatory.

---

## START COMPRESSING

Ready? Provide your document and I'll intelligently compress it using tiered, adaptive strategies while GUARANTEEING all sacred content preservation through mandatory verification.