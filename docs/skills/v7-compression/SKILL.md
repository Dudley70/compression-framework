---
name: v7-compression
description: Apply V7 Complete LLM-Optimized compression to documentation. Achieves 84% reduction maintaining 100% completeness through aggressive format-only compression. Use when user requests V7 compression, wants to compress documents for LLM-only use, or needs complete technical reference at maximum density (~21KB natural compression limit).
version: 1.0.0
---

# V7 Compression Skill

## Purpose

V7 compression transforms verbose technical documentation into ultra-dense LLM-optimized format while maintaining 100% completeness. Achieves V3 completeness (all test patterns, reproducible prompts, full details) at V5 size (~21KB) through aggressive format-only compression.

## When to Use This Skill

Use V7 compression when:
- User explicitly requests "V7 compression" or "compress using V7"
- Document needs maximum density for LLM consumption (not human reading)
- Complete technical reference required at ~21KB natural compression limit
- All test patterns/code/prompts must be preserved exactly
- Target audience is LLM only (symbols, abbreviations, terse fragments acceptable)

**Do NOT use when**:
- Human readability required
- Quick summaries needed (use V5 instead)
- Document is simple/non-technical
- User wants partial compression only

## Core Principle

**Compress FORMAT only. Never sacrifice CONTENT needed for reproduction.**

Preserve exactly:
- Test prompts (verbatim)
- Code examples (verbatim)
- Model outputs (structure preserved)
- Schema definitions (verbatim)
- API parameters (verbatim)

Compress aggressively:
- Headers & metadata
- Prose descriptions
- Tables
- Lists
- Section structure
- Scaffolding (remove entirely)

## V7 Target Metrics

- **Lines**: ~400-450 (from 1,300+)
- **Size**: ~19-22KB (from 130-140KB)
- **Reduction**: 84-85% byte reduction
- **Completeness**: 100% (no content loss)

## Compression Rules

For complete compression rules, see REFERENCE.md in this skill folder.

### Quick Reference

1. **Ultra-terse headers**: Src, L, KB, pipe-separated
2. **Extreme abbreviations**: E/R, CoT, LLM, w/, w/o, Doc, ✓✗⚠
3. **Symbols**: →↑↓=≠≥≤
4. **Tables**: Single-letter headers (Doc, E, R)
5. **Prose→fragments**: Remove subjects, filler, combine points
6. **Code preservation**: NEVER abbreviate prompts/code/schemas
7. **Section headers**: Inline definitions (Def:, Doc:)
8. **Scaffolding removal**: Remove ALL transitions/meta-commentary
9. **List compression**: Combine related, remove numbering
10. **Standard test format**: See REFERENCE.md

## Quality Checklist

- [ ] Size: 19-22KB
- [ ] Lines: 400-450
- [ ] All test prompts verbatim
- [ ] All code preserved
- [ ] No prose paragraphs
- [ ] Tables: single-letter headers
- [ ] Symbols: ✓✗⚠→
- [ ] Abbreviations consistent
- [ ] No "The model..." starters
- [ ] No scaffolding
- [ ] Completeness: 100%

## Process

When user requests V7 compression:

1. Read REFERENCE.md for complete compression rules
2. Apply all 10 rules systematically to source document
3. Verify quality against checklist
4. Output compressed version
5. Report metrics (original → compressed → %)

## Notes for Claude

- V7 = LLM eyes only (not human-readable)
- Never apologize for terse format
- Completeness > readability
- When unsure about keeping: keep it
- When unsure about abbreviating: abbreviate it
- Prompts/code = sacred (touch nothing)
- Scaffolding = noise (remove all)

## Version History

- v1.0.0 (2025-11-14): Initial release