---
name: llm-doc-compression
description: Compress technical documentation to maximum density (~85% reduction) while maintaining 100% completeness. Optimizes for LLM consumption using aggressive abbreviations, symbols, and format compression. Preserves all code/prompts/tests verbatim. Use when user wants LLM-only compressed docs, maximum density at natural limit (~21KB), or requests "compress for LLM" or "dense compression".
---

# LLM Documentation Compression

**Version**: 1.0.0 (2025-11-14)

## Theoretical Foundation

This skill implements the Compression Framework's (σ,γ,κ) parameter optimization model:

**Target Configuration**:
- **σ (Structure)**: 0.9 - Maximum structural density through abbreviations, symbols, format compression
- **γ (Granularity)**: 1.0 - Full semantic completeness (all code/prompts/tests preserved verbatim)
- **κ (Scaffolding)**: 0.1 - Minimal contextual scaffolding (only critical warnings retained)

**Constraint**: σ + γ + κ = 2.0 ≥ C_min(LLM, reference) ✓

**Result**: ~85% reduction while maintaining 100% reproducibility.

## Purpose

Transform verbose technical docs → ultra-dense LLM format. 85% reduction, 100% completeness, ~21KB natural limit.

## When to Use

✓ User requests: "compress for LLM", "dense compression", "optimize for LLM"
✓ Technical reference needs max density
✓ LLM-only audience (not human reading)
✓ Must preserve all code/prompts/tests

✗ Human readability needed
✗ Quick summaries (not full compression)
✗ Simple/non-technical docs

## Core Rule

**Compress FORMAT only. Content = sacred.**

Preserve verbatim: prompts, code, schemas, API params, test patterns (γ=1.0)
Compress aggressive: headers, prose, tables, lists, scaffolding (↑σ, ↓κ)

## Target

- Lines: 400-450 (from 1,300+)
- Size: 19-22KB (from 130KB+)
- Reduction: 84-85%
- Completeness: 100%

## 10 Compression Rules (Parameter Mappings)

### 1. Ultra-Terse Headers [↑σ]
Before: `**Source**: 1,332 lines / 134KB systematic...`
After: `**Src**: 1,332L/134KB | 84%→21KB | LLM only`
Rules: Src, L, KB, pipe-separate, remove redundancy

### 2. Extreme Abbreviations [↑σ]
Standard: E=Effectiveness, R=Reliability, Doc=Documentation, w/=with, w/o=without, #=number, @=at, ~=approximately
Context: CoT, ToT, LLM, API, LOC, JSON

### 3. Symbols [↑σ]
Status: ✓=yes/success, ✗=no/fail, ⚠=partial
Compare: →=leads to, ↑=increases, ↓=decreases, =≠≥≤

### 4. Tables [↑σ]
Single-letter headers (Doc, E, R). Symbols in cells. Terse fragments in notes.
Before: `| Effectiveness | Reliability | Documentation Support |`
After: `| E | R | Doc |`

### 5. Prose→Fragments [↑σ, ↓κ]
Remove subjects ("The model", "It"), filler ("successfully", "excellent"). Start w/ action. Combine points w/ punctuation. Use + for "and".
Before: "The model's performance was excellent. It successfully..."
After: "Excellent performance. Successfully..."

### 6. Code Preservation [γ=1.0]
**CRITICAL**: Never touch prompts, code, schemas, API params, commands, function names, JSON keys. Keep 100% verbatim. This maintains full semantic granularity.

### 7. Section Headers [↓κ]
Inline definitions. Remove redundancy.
Before: `### Definition` (3 lines explaining...)
After: `**Def**: [1 terse sentence]`

### 8. Scaffolding Removal [↓κ]
Delete: transitions ("Now let's"), meta-commentary ("As we see"), obvious conclusions, summaries, conversational elements ("Certainly")
Keep: section numbers, critical distinctions ("CRITICAL:"), limitation warnings

### 9. List Compression [↑σ, ↓κ]
Remove numbering where order irrelevant. Combine related. No "The model..." prefixes. Use colons for definitions.
Before: "1. **X:** The model... 2. **Y:** It also..."
After: "X occurred. Y followed. Z confirmed."

### 10. Standard Test Format [↑σ]
```
### [N]. [Name]
**Def**: [terse w/ →]
**Doc**: [✓/✗/⚠] [level]
**Test**: [<10 words]
**Prompt**: ```[verbatim]```
**Output**: [brief | verbatim]
**Analysis**: [2-4 fragments, no subjects]
**Scores**: E=[N]/10 ([why]), R=[N]/10 ([why])
```

## Quality Checklist

- [ ] 19-22KB size
- [ ] 400-450 lines
- [ ] All prompts/code verbatim (γ=1.0 maintained)
- [ ] No prose paragraphs (σ maximized)
- [ ] Tables: single-letter headers (σ maximized)
- [ ] Symbols: ✓✗⚠→ (σ increased)
- [ ] Abbreviations consistent (σ increased)
- [ ] No subjects in analysis (κ reduced)
- [ ] Zero scaffolding (κ≈0.1)
- [ ] 100% completeness (γ=1.0)

## Process

1. Read source doc
2. Apply 10 rules systematically
3. Verify checklist
4. Output compressed
5. Report: [original] → [compressed] → [%]

## Claude Notes

- LLM eyes only (not human-readable)
- Completeness > readability (γ priority)
- When unsure: keep content (maintain γ), abbreviate format (increase σ)
- Prompts/code = untouchable (γ=1.0)
- Scaffolding = noise (minimize κ)