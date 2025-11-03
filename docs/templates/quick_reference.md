---
compression:
  sigma: 0.9
  gamma: 0.3
  kappa: 0.1
  audience: power-users
  tier: T2
  phase: active
  template: quick-reference
  version: 1.0
---

# [Topic] Quick Reference

## [Category 1]
| Item | Value | Notes |
|------|-------|-------|
| X | Y | Z |

## [Category 2]
```
Code or config format here
Key: value
```

## Commands
- `command args` - description
- `command args` - description

## Common Patterns
```
Pattern with code example
```

---

## Example: Compression Framework Quick Reference

---
compression:
  sigma: 0.9
  gamma: 0.3
  kappa: 0.1
  audience: power-users
  tier: T2
  phase: active
  template: quick-reference
  version: 1.0
---

# Compression Framework Quick Reference

## Parameters
| Parameter | Range | Meaning | Examples |
|-----------|-------|---------|----------|
| σ (sigma) | 0.0-1.0 | Structure density | 0.8=tables, 0.3=prose |
| γ (gamma) | 0.0-1.0 | Detail level | 0.8=full, 0.3=keywords |
| κ (kappa) | 0.0-1.0 | Scaffolding | 0.8=full context, 0.2=minimal |

## Document Types → Templates
| Type | Template | σ | γ | κ | Use |
|------|----------|---|---|---|-----|
| Status | high_compression_status | 0.8 | 0.4 | 0.2 | Progress reports |
| Design | medium_compression_design | 0.6 | 0.6 | 0.4 | Architecture docs |
| Notes | high_compression_notes | 0.8 | 0.5 | 0.2 | Meeting summaries |
| Research | medium_compression_research | 0.5 | 0.7 | 0.5 | Analysis docs |
| Decision | decision_record | 0.5 | 0.7 | 0.6 | ADR format |
| Reference | quick_reference | 0.9 | 0.3 | 0.1 | Lookup tables |
| Education | educational_guide | 0.4 | 0.9 | 0.8 | Onboarding |
| Planning | planning_document | 0.6 | 0.6 | 0.5 | Roadmaps |

## Frontmatter Template
```yaml
---
compression:
  sigma: 0.6
  gamma: 0.6
  kappa: 0.4
  audience: dual
  tier: T2
  phase: active
  template: [template-name]
  version: 1.0
---
```

## Compression Constraint
```
σ + γ + κ ≥ C_min(audience, phase)

LLM:    C_min = 0.7
Human:  C_min = 1.2
Dual:   C_min = 1.0
Active: base
Complete: +0.1
Archived: +0.2
```

## High σ (0.7-1.0) Techniques
- Use tables for data
- Bullet lists for facts
- YAML/JSON structures
- Minimal prose
- Abbreviations OK

## High γ (0.7-1.0) Techniques
- Complete sentences
- Full context included
- Detailed explanations
- No assumed knowledge
- Rich detail on rationale

## High κ (0.7-1.0) Techniques
- Full hierarchical headers
- Section explanations
- Complete background
- Rationale for decisions
- Scaffolding for unfamiliar readers

## Example: Status Update
```markdown
---
compression: {sigma: 0.8, gamma: 0.4, kappa: 0.2, audience: LLM, tier: T2, phase: active}
---

# Status - 2025-11-03

## Accomplished
- [x] Feature A - complete

## Metrics
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Tests | 142/156 | 156/156 | 91% |
```

## Example: Design Doc
```markdown
---
compression: {sigma: 0.6, gamma: 0.6, kappa: 0.4, audience: dual, tier: T2, phase: active}
---

# Cache Layer Design

## Problem
DB load 15% quarterly growth.

## Decision
Redis with TTL (1 hour).

**Rationale**: Simple, team understands, meets 85% hit rate target.
```

## Parameter Adjustment
- ↑ σ: More structure (tables, lists)
- ↓ σ: More prose, narrative flow
- ↑ γ: More detail, complete sentences
- ↓ γ: Keywords, abbreviations, concise
- ↑ κ: More context, headers, explanations
- ↓ κ: Minimal context, assume expertise
