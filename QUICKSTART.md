# Compression Framework - Quick Start

**Last Updated**: 2025-11-14  
**Current Standard**: V7 Complete LLM-Optimized

---

## For New Sessions: Current Compression Standards

### LLM-Only Technical References (Complex, Complete)
**Use V7** (Complete LLM-Optimized)
- **Location**: Check project-specific compressed/ folders
- **Target**: 84% byte reduction, maintains full completeness
- **Characteristics**: All test patterns, reproducible prompts, API configs, aggressive LLM formatting
- **Size**: ~21KB (natural compression limit for complete self-contained reference)
- **When**: Complex technical references requiring full reproducibility and implementation patterns

### Quick-Scan References (Results Summary)
**Use V5** (Balanced LLM-Optimized)
- **Alternative** to V7 when need faster scanning
- **Target**: 84.5% byte reduction, results-focused
- **Characteristics**: Results summaries, readable format, decision support
- **Size**: ~21KB
- **When**: Quick lookup, score checking, capability assessment where full patterns not needed

### Human-Readable References
**Use V3** (Decision-Support Compression)
- **Alternative** when human readability important
- **Target**: 81% byte reduction, prose format
- **Characteristics**: Full test patterns with readable prose descriptions
- **Size**: ~25KB
- **When**: Need extra verbosity/readability, human review/validation

---

## Key Discovery: Natural Compression Limit

**~21KB** appears to be natural compression limit for complete self-contained technical reference:
- **Below 21KB**: Sacrifices completeness (V6 at 10KB lost implementation patterns)
- **At 21KB**: Optimal balance - complete AND efficient (V7, V5)
- **Above 21KB**: Adds unnecessary verbosity (V3 at 25KB has prose overhead)

**V7's Achievement**: Pack V3's completeness into V5's space through superior formatting efficiency.

---

## Compression Version Summary

| Version | Size | Reduction | Completeness | Use Case |
|---------|------|-----------|--------------|----------|
| V7 ⭐ | 21KB | 84.4% | High (full patterns) | **DEFAULT - Complex work** |
| V5 | 21KB | 84.5% | Medium (results only) | Alternate - Quick scan |
| V3 | 25KB | 81.4% | High (full patterns) | Alternate - Human readable |
| V6 | 10KB | 92.3% | Low (lost patterns) | Rejected - Too aggressive |
| V4 | 11KB | 91.6% | Low | Archive - Simple lookups only |
| V1-V2 | 12-14KB | 89-90% | Low | Archive - Early iterations |

---

## Quick Decision Tree

```
Need to compress LLM-only technical reference?
├─ Need full test patterns + API configs + reproducibility?
│  ├─ Yes → Use V7 (complete at 21KB limit) ⭐ DEFAULT
│  └─ No, just need scores/results → Use V5 (quick-scan at 21KB)
└─ Need human readability?
   └─ Yes → Use V3 (prose format at 25KB)
```

---

## For External Projects

**Gemini Assessment Example**:
- Original: 1,332 lines, 134KB
- V7 Output: 413 lines, 21KB (84.4% reduction)
- Location: `/Users/dudley/projects/Gemini-Research/docs/reference/compressed/7-Gemini_Prompting_Capability_Assessment_V7.md`

**To Apply V7 to Your Project**:
1. Read TECHNIQUES_V7_METHOD.md (when created) for methodology
2. Preserve: All test patterns, API configs, implementation details
3. Compress: Format only (symbols, abbreviations, terse prose, remove scaffolding)
4. Target: ~21KB for complete reference (natural limit)
5. Validate: Self-contained test (can generate complex prompts without source)

---

## Documentation

- **Strategic Context**: PROJECT.md (read first)
- **Current Session**: SESSION.md
- **V7 Standard**: Search for `7-*_V7.md` files in compressed/ folders
- **Methodology**: TECHNIQUES_V5.md (V5), TECHNIQUES_V6_METHOD.md (V6 concepts)
- **Framework**: docs/README.md

---

**CRITICAL FOR NEW SESSIONS**: V7 is the current standard for LLM-only technical references. Use V7 by default unless specific reason to use V5 (quick-scan) or V3 (human-readable).
