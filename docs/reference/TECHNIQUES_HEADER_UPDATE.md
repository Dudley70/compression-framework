---
title: Compression Techniques
created: 2025-11-06
updated: 2025-11-14
status: active
category: reference
version: 1.3
compression_level: moderate
audience: technical
purpose: technique_reference
---

# Compression Techniques

**Purpose**: Comprehensive reference for compression techniques including LSC (proactive), decision-support (manual), LLM-optimized (V4 & V5), CCM (retrospective), and archive strategies.

**Audience**: Technical implementers, developers using compress.py, teams adopting compression framework  
**Scope**: Specific techniques and implementations, not decision guidance (see DECISION_FRAMEWORK.md)

---

## Quick Reference

**LSC Techniques** (proactive, 70-85% reduction, automated):
1. Hierarchical Structure - Nested lists to structured data
2. Redundancy Elimination - Remove repeated info
3. Semantic Clustering - Group related concepts
4. Pattern Abstraction - Templates for recurring patterns
5. Contextual Abbreviation - Domain-aware shortening

**Decision-Support Compression** (manual, 70-85% reduction):
- Preserve decision-critical content (scores, patterns, implementations)
- Compress explanations, methodology, background  
- Target: Operational reference for quick decisions

**LLM-Optimized V5** (manual, 65-70% reduction) ⭐ **DEFAULT FOR COMPLEX DOCS**:
- Balanced compression with mini implementation patterns
- Self-contained for 90% of use cases
- Target: 400-450 lines from ~1,300 line originals
- Best for: Multi-technique guides, capability assessments, technical references

**LLM-Optimized V4** (manual, 60-75% reduction):
- Aggressive compression, removes all human scaffolding
- Target: Simple reference lookups
- Best for: Maximum iteration count, known techniques

**CCM** (retrospective, 99.5% reduction):
- Four-tier compression for session logs
- Preserve artifacts, compress dialogue

**Archive Strategies** (95-99% reduction):
- Search-optimized indexing
- Keyword extraction
- Structured summaries

---

## Table of Contents

1. Core LSC Techniques
2. Decision-Support Compression (Manual)
3. LLM-Optimized V4: Aggressive Compression
4. LLM-Optimized V5: Balanced Compression ⭐ **RECOMMENDED DEFAULT**
5. Context Compression Method (CCM)
6. Archive Compression Strategies
7. Compression Anti-Patterns
8. Compression in Practice (Examples)

---

## Choosing the Right Technique

**Quick Decision Tree**:

```
Need automation? → LSC (compress.py)
Manual compression needed:
  ├─ Human-readable? → Decision-Support (70-85%)
  └─ LLM-only?
      ├─ Complex multi-technique work? → V5 (65-70%) ⭐ DEFAULT
      ├─ Simple reference lookups? → V4 (60-75%)
      └─ Session logs? → CCM (99.5%)
Archive/search? → Archive Strategies (95-99%)
```

**Recommendation**: When in doubt, **use V5** for technical reference documents.

---

