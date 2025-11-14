# LLM Doc Compression - Complete Rules

**Src**: TECHNIQUES_V7_METHOD.md | **Target**: 85% reduction, 100% completeness, ~21KB | **Format**: LLM only

---

## Rules Detail

### 1. Ultra-Terse Headers/Metadata

**Pattern**: Pipe-separate, abbreviate units, single-line where possible

Before: `**Source**: 1,332 lines / 134KB...` `**Compression**: V7 Complete...` `**Format**: Aggressive...`
After: `**Src**: 1,332L/134KB | **Goal**: Complete + aggressive | **Aud**: LLM only`

Apply: Source→Src, lines→L, KB, pipe-separate multi-bullets, kill redundancy

### 2. Extreme Abbrevs

**Standard** (always):
E=Effectiveness, R=Reliability, Doc=Documentation, API, vs→v|≠, w/=with, w/o=without, #, @, ~, f()=function, →=leads to, &=and, |=or

**Context** (domain-specific):
CoT, ToT, LLM, SOTA, LOC, MoE, JSON, CSV, YAML, SQL, HTTP, URL, CLI, GUI, API, SDK

### 3. Symbols

**Status**: ✓ ✗ ⚠
**Compare**: → ↑ ↓ = ≠ ≥ ≤ < >
**Math**: + - × ÷ ± ∑

### 4. Table Compression

Before: `| Technique | Description | Documentation Support | Effectiveness | Reliability | Key Findings |`
After: `| Tech | Doc | E | R | Notes |`

Single-letter headers. ✓✗⚠ in cells. Terse fragment notes. Remove /10 denominator.

### 5. Prose→Fragments

Pattern: Kill subjects/filler → terse fragments → combine w/ punctuation

Before: "The model successfully executed the Quality Gate prompt. It correctly analyzed the input review and determined that it met the criterion..."
After: "Correct execution. Input analyzed, criterion met, approved path followed."

Remove: "The model", "It", "successfully", "excellent", "is"
Convert: Full sentences → fragments
Combine: Related points via punctuation
Replace: "and" → +

### 6. Code Preservation

**NEVER TOUCH**:
- Test prompts (100% verbatim)
- Code examples (100% verbatim)
- Model outputs (structure preserved, can abbreviate if >100L)
- Schema defs (100% verbatim)
- API params (100% verbatim)
- Function/variable names
- Commands
- JSON keys

### 7. Section Header Compression

Before: `### **1. Chain-of-Thought (CoT) Prompting**` `#### **Definition**` `[3 lines explaining]` `#### **Documentation Support**` `[2 lines]`
After: `### 1. CoT` `**Def**: [1 terse sentence w/ →]` `**Doc**: ✓ Strong`

Inline definitions. Use symbols. Kill qualifiers unless critical ("albeit", "sometimes").

### 8. Scaffolding Removal

**Delete entirely**:
- Transitions: "Moving on", "Now let's", "Next we'll"
- Meta: "As we can see", "It's important", "Note that"
- Obvious: "This demonstrates", "This shows"
- Summaries: End-of-section recaps
- Conversational: "Certainly", "Indeed", "Interestingly"

**Keep**:
- Section numbers (navigation)
- Critical tags ("CRITICAL:", "WARNING:", "Note:")
- Limitation warnings

### 9. List/Bullet Compression

Before: `Analysis:` `1. **Conditional Logic:** It correctly...` `2. **Path Execution:** Because...` `3. **Schema:** The output is...`
After: `Correct conditional logic. Input passed gate → approved path → extracted product+feedback. Schema perfect.`

Remove: Numbering (if order irrelevant), headers ("Analysis:"), subject prefixes ("The model", "It")
Combine: Related points → flowing fragments
Use: Colons for definitions, not explanatory sentences

### 10. Standard Test Format

**Every assessment follows**:
```
### [N]. [Technique]

**Def**: [1-2 sentences, use →]

**Doc**: [✓/✗/⚠] [level if applicable]
- [Key point 1]
- [Key point 2]

**Test**: [<10 word description]

**Prompt**:
```
[Exact prompt - NO compression]
```

**Output**: [Brief if long | exact if short]
```
[Output structure preserved]
```

**Analysis**: [2-4 terse sentences, no subjects, fragments]

**Scores**: E=[N]/10 ([terse why]), R=[N]/10 ([terse why])
```

---

## Quality Gates

Before finalizing, verify:

**Size**: 19-22KB (if >25KB → insufficient compression, if <18KB → likely lost content)
**Lines**: 400-450 (if >500 → verbose, if <350 → check completeness)
**Prompts**: All test prompts verbatim (critical for reproducibility)
**Code**: All code/schemas exact (never abbreviate)
**Prose**: Zero paragraphs (all fragments)
**Tables**: Single-letter headers (E, R, Doc not Effectiveness, Reliability)
**Symbols**: ✓✗⚠→ throughout (not spelled out)
**Abbrevs**: Consistent (E/R, CoT, LLM, w/, etc)
**Subjects**: None in analysis ("The model", "It" → removed)
**Scaffolding**: Zero (no transitions, meta, obvious statements)
**Completeness**: 100% (can reproduce all tests from compressed version?)

---

## Common Errors

### ❌ Half-Compress
Wrong: Some sections abbreviated, others verbose
Right: Uniform application throughout

### ❌ Code Touch
Wrong: Abbreviate prompt "Let's think step by step" → "Think stepwise"
Right: Keep 100% exact "Let's think step by step"

### ❌ Content Loss
Wrong: Summarize "tested with logistics problem"
Right: Include full test prompt for reproduction

### ❌ Verbose Tables
Wrong: `| Documentation Support | Effectiveness Score |`
Right: `| Doc | E |`

### ❌ Keep Scaffolding
Wrong: "Now let's examine the next technique. As we can see from the analysis above..."
Right: [jump straight to technique content]

---

## Example Transform

### Before (134 words)
```markdown
**Source**: 1,332 lines / 134 kilobytes
**Compression Method**: Complete LLM-Optimized

## Chain-of-Thought Prompting

### Definition

The model's performance on the Chain-of-Thought test was exceptional. It correctly interpreted the instruction "Let's think step by step" and adopted a sequential, verbose problem-solving approach. Each step was calculated correctly, and the state of each warehouse was accurately tracked from one step to the next. The arithmetic was sound throughout the entire calculation process.
```

### After (31 words, 77% reduction)
```markdown
**Src**: 1,332L/134KB | **Method**: Complete LLM-optimized

## CoT

**Def**: Sequential problem decomposition. "Think step by step" instruction.

Exceptional performance. Correctly interpreted "step by step" → sequential approach. Each step calculated correctly, state tracked accurately. Sound arithmetic throughout.
```

**Preservation**: Exact prompt phrase kept ("Let's think step by step")
**Compression**: Headers, prose, filler removed; fragments used

---

## Process Workflow

**Input**: Verbose technical doc (typically 1,000+ lines, 100+ KB)

**Steps**:
1. **Read complete**: Understand structure, identify prompts/code/tests
2. **Mark sacred**: Flag all prompts, code, schemas (never touch)
3. **Apply rules**: Systematic pass through 10 rules
4. **Verify checklist**: Size, lines, completeness, format
5. **Output**: Compressed version + metrics report

**Output**: Dense LLM doc (400-450 lines, 19-22KB, 84-85% reduction, 100% complete)

**Report Format**: `[Src: XL/YKB] → [Compressed: AL/BKB] → [R%]`

---

## Notes

**Audience**: LLM only. Humans may struggle w/ density.
**Philosophy**: Completeness > readability. Information fidelity critical.
**When uncertain**: Keep content, compress format.
**Sacred content**: Prompts, code, schemas = untouchable.
**Noise**: Scaffolding, transitions, meta = delete all.
**Natural limit**: ~21KB appears to be floor for complete technical reference w/ all patterns/configs/tests.

---

**Version**: v1.0.0 (2025-11-14)