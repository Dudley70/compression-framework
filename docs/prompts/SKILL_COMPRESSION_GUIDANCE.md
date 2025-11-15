# Guidance for LLM Doc Compression Skill

## Core Issue Identified

**Problem**: 58KB output when target is 22KB (2.6x over target)

**Status**:
- ✅ Rule 6 compliance: All prompts preserved 100% verbatim (CORRECT)
- ✅ γ=1.0 achieved: Full semantic granularity maintained (CORRECT)
- ❌ Size: 58KB vs 22KB target (2.6x too large)
- ❌ Lines: 607 vs 400-450 target (35% over)
- ❌ Reduction: 56.7% vs ~85% target (far below)

## What's Right

The compression correctly preserved all prompts verbatim as Rule 6 requires. This is the foundation - **don't change this**.

## What's Wrong

Everything EXCEPT prompts was not compressed aggressively enough. The skill requires:
- σ=0.9 (maximum structural compression)
- κ=0.1 (minimal scaffolding)

But the 58KB version has too much:
- Verbose outputs (~10KB should be ~3KB)
- Full sentence analysis (~12KB should be ~4KB)  
- Extensive meta-sections (~15KB should be ~5KB)
- Heavy scaffolding/structure (~15KB should be ~4KB)

## The Fix

**Keep prompts verbatim (Rule 6), compress everything else aggressively**:

| Component | Original | Target | Compression | Action |
|-----------|----------|--------|-------------|--------|
| Prompts | ~6KB | ~6KB | **0%** | KEEP VERBATIM |
| Outputs | ~10KB | ~3KB | **70%** | Key results only |
| Analysis | ~12KB | ~4KB | **67%** | Fragments, no subjects |
| Meta-sections | ~15KB | ~5KB | **67%** | Terse summaries |
| Structure/Headers | ~15KB | ~4KB | **73%** | Symbols, abbreviations |

**Target Result**: 22KB with γ=1.0 maintained

## Key Insight

**Prompts are only ~5% of the document**. The other **95% needs aggressive compression**.

The 58KB output suggests compression was applied too conservatively to non-prompt content.

## Examples of Aggressive Compression

### Outputs (10KB → 3KB)

❌ **WRONG (preserves too much)**:
```
"Certainly. Let's break down the movement step by step.
**Step 1**: Half of A to B means 40/2 = 20 units moved from A to B.
This leaves A with 20 units and gives B 30 + 20 = 50 units.
**Step 2**: One-third of B to C means 50/3 ≈ 16.67 units..."
```

✅ **CORRECT (key results only)**:
```
"Perfect step-by-step breakdown. Step 1: 40/2=20 moved A→B. Step 2: 50/3≈17 moved B→C. Final: A=25, B=33, C=37."
```

### Analysis (12KB → 4KB)

❌ **WRONG (full sentences)**:
```
"The model correctly executed multi-step reasoning. It broke down the problem into sequential steps, showed intermediate calculations, and arrived at the correct final state. This demonstrates that the Chain-of-Thought approach is highly effective for this model when dealing with logical problems."
```

✅ **CORRECT (fragments, no subjects)**:
```
"Correctly executed multi-step reasoning. Broke down problem→sequential steps, showed intermediate calc, arrived at correct final state. Demonstrates CoT is highly effective for this model on logical problems."
```

### Meta-sections (15KB → 5KB)

❌ **WRONG (verbose)**:
```
"This report presents a systematic, evidence-based self-assessment of the Gemini 2.5 Pro large language model, with a specific focus on its capacity to execute advanced prompting techniques within a single-shot, non-conversational context."
```

✅ **CORRECT (terse)**:
```
"Systematic self-assessment of Gemini 2.5 Pro's advanced prompting capabilities in single-shot execution."
```

## Summary for Implementation

**The compression correctly preserves prompts verbatim (Rule 6 ✓) but fails to aggressively compress non-prompt elements.**

**Action Required**: Apply rules 1-5 and 7-10 much more heavily to:
- Outputs (extract key results only)
- Analysis (use fragments, remove subjects)
- Meta-sections (compress to essentials)
- Structure (symbols, abbreviations, remove scaffolding)

**While keeping Rule 6 (prompt preservation) exactly as is.**

**Current**: 58KB  
**Target**: 22KB  
**Gap**: Need 62% more compression on non-prompt content

## Size Checkpoints

After compressing, verify each component:
- [ ] Prompts: ~6KB (unchanged from original)
- [ ] Outputs: ~3KB (70% reduction applied)
- [ ] Analysis: ~4KB (67% reduction applied)
- [ ] Meta: ~5KB (67% reduction applied)
- [ ] Structure: ~4KB (73% reduction applied)
- [ ] **Total: 19-22KB**

If any component is >50% over budget → not compressed aggressively enough.
