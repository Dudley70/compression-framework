# V7 Compression Directive Prompt

Use this prompt when asking Claude (or another LLM) to compress a document to V7 standards.

---

## The Prompt

```
I need you to compress this technical document to V7 LLM-optimized format. This is NOT summarization - it's aggressive FORMAT compression while preserving 95%+ information.

TARGET: 19-22KB, 400-450 lines (from ~134KB, ~1,300 lines)

CRITICAL RULES:

1. **PROMPTS = SACRED (0% compression)**
   - Every test prompt: 100% verbatim, every single word exact
   - Code blocks: 100% exact
   - Persona descriptions: Complete (these ARE part of prompts)
   - API examples: Exact
   
2. **OUTPUTS = KEY RESULTS ONLY (70% compression)**
   - Extract: Final answer, key numbers, essential structure
   - Delete: "Certainly", "Let me", step-by-step narration, explanations
   - Keep: Technical accuracy, all numbers, conclusions
   
3. **ANALYSIS = FRAGMENTS (67% compression)**
   - Delete subjects: "The model" → start with verb
   - Keep reasoning: "broke down problem→sequential steps" (all substance)
   - Delete filler: "As we can see", "It should be noted"
   - Use symbols: "to" → "→", "with" → "w/", "passed" → "✓"
   
4. **HEADERS = ULTRA-TERSE**
   - **Definition**: → **Def**:
   - **Documentation**: → **Doc**:
   - **Example**: → **Ex**:
   - **Analysis**: → **Anal**:
   - 1,332 lines → 1,332L
   - 134 kilobytes → 134KB

5. **META-SECTIONS = ESSENTIALS ONLY (67% compression)**
   - Executive summary: 3 sentences max
   - Introduction: 2-3 sentences
   - Methodology: Key points only, no elaboration

DECISION-MAKING GUIDE:

For each section, ask yourself:

**Prompts/Code:**
"Would someone need this EXACT text to reproduce the test?" 
- YES → Keep 100% verbatim
- NO → (this shouldn't happen for prompts)

**Outputs:**
"What's the minimum text to prove the model succeeded/failed?"
- Keep: Final answer, key calculations, structure proof
- Delete: Everything else (pleasantries, narration, elaboration)

**Analysis:**
"What's the core insight that justifies the score?"
- Keep: The insight in fragment form
- Delete: Subjects, transitions, obvious statements

**Example showing decision points:**

BEFORE (verbose output):
```
Certainly. Let's break down the movement step by step.
**Step 1**: Half of A to B means 40/2 = 20 units moved from A to B.
This leaves A with 20 units and gives B 30 + 20 = 50 units.
**Step 2**: One-third of B to C means 50/3 ≈ 16.67 units moved from B to C.
This leaves B with approximately 33.33 units and gives C 20 + 16.67 = 36.67 units.
**Step 3**: Now we need to evenly distribute all units in B among A and C.
B has 33.33 units, so each warehouse gets 16.67 units.
A becomes 20 + 16.67 = 36.67 units.
C becomes 36.67 + 16.67 = 53.34 units.
**Final Answer**: A has 36.67 units, B has 0 units, C has 53.34 units.
```

AFTER (key results):
```
Perfect step-by-step. S1: 40/2=20 A→B (A=20, B=50). S2: 50/3≈17 B→C (B=33, C=37). S3: Distribute B to A&C (A=37, C=53, B=0). Final: A=37, B=0, C=53.
```

**What I kept**: All numbers, all steps, final answer, accuracy proof
**What I deleted**: "Certainly", "Let's", "This leaves", "This means", "Now we need to"
**Compression**: ~90% (200 chars → 20 chars) while keeping 100% technical content

YOUR TASK:

Go through the document section by section:
1. Identify prompts/code → copy 100% verbatim
2. Compress outputs → extract key results only
3. Compress analysis → fragments, no subjects, keep reasoning
4. Compress meta-sections → essentials only
5. Apply abbreviations/symbols throughout

SIZE CHECK after each major section:
- After executive summary: ~1KB
- After methodology: ~2KB
- After tests 1-5: ~10KB
- After tests 6-10: ~18KB
- After conclusion: ~20-22KB

If any checkpoint is >50% over → you're under-compressing that section.

BEGIN COMPRESSION:
```

---

## Why This Works Better

**Previous skill issues:**
- ❌ "Compress aggressively" - too vague
- ❌ "70% reduction on outputs" - no decision framework
- ❌ "Keep analysis complete" - conflicting with size target

**This prompt:**
- ✅ Shows EXACT before/after for decision-making
- ✅ Provides decision questions for each component
- ✅ Includes size checkpoints for self-correction
- ✅ Emphasizes the judgment: "minimum text to prove success"

**Key difference from skill:**
The skill tried to teach principles. This prompt **shows the actual decision-making process** you used manually.

---

## How You Can Use This

1. **Paste the prompt** into a Claude conversation
2. **Attach the document** to compress
3. **Claude will compress** following the exact decision framework
4. **Check the size** at each checkpoint
5. **If over-budget**, tell Claude which section to compress more

This gives Claude the **decision-making framework** that was missing from the skill.
