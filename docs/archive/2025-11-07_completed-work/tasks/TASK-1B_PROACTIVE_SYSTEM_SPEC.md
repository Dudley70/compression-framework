# TASK-1B: Create Proactive System Specification

Create comprehensive specification for proactive compression system (templates + Claude skill).

**File**: docs/plans/PROACTIVE_SYSTEM_SPEC.md (~800-1000 lines)
**Context**: PROJECT.md (Strategic Context), SESSION.md, PARADIGM_SHIFT.md (sections 1-5), PHASE_1_APPROACH.md
**Duration**: 90-120 min

## Deliverable Sections

### 1. Overview (~150 lines)
- System architecture (templates + skill integration)
- Proactive vs reactive comparison
- User workflow (select template → edit → compression maintained)

### 2. Frontmatter Standard (~200 lines)
Complete YAML schema:
```yaml
---
compression:
  sigma: 0.6    # Structure (0-1): prose → data structures
  gamma: 0.5    # Granularity (0-1): keywords → full detail  
  kappa: 0.3    # Scaffolding (0-1): no context → full explanation
  audience: dual
  tier: T2
---
```
- Parameter ranges and meanings
- 3 complete examples (high/medium/low compression)

### 3. Template Library (~250 lines)
5-8 templates, each with:
- Purpose and use case
- (σ,γ,κ) parameters with rationale
- Structure design
- 50-100 line working example

Templates:
1. High compression status (σ=0.8, γ=0.6, κ=0.2)
2. Medium compression tech spec (σ=0.5, γ=0.7, κ=0.4)
3. Low compression strategic doc (σ=0.3, γ=0.8, κ=0.6)
4-8. [Additional templates covering use cases]

### 4. Claude Skill (~200 lines)
Location: /mnt/skills/public/compression/SKILL.md

Behavior:
1. Read frontmatter parameters
2. Apply techniques based on σ,γ,κ
3. Maintain compression during edits

Technique mapping:
- σ ranges → LSC techniques (lists_tables, hierarchical, etc.)
- γ ranges → detail levels
- κ ranges → context amounts

Examples for each parameter range.

### 5. Integration Patterns (~100 lines)
- Template selection decision tree
- Edit workflows (create new, add content, update existing)
- Common scenarios with examples

### 6. Dependencies (~50 lines)
```
Frontmatter Standard (FIRST)
  ↓
  ├→ Templates (parallel)
  └→ Skill (parallel)
      ↓
      Integration Guide (LAST)
```
Context requirements per component.

### 7. Success Criteria (~50 lines)
- Validation tests
- Quality gates
- Acceptance criteria

## Output Format

```markdown
# Proactive Compression System Specification

**Version**: 1.0
**Date**: [Date]
**Status**: Specification for Phase 2 Implementation

## 1. Overview
[content]

## 2. Frontmatter Standard
[content]

[etc...]
```

## Success Criteria
- ✅ 800-1000 lines
- ✅ All 7 sections complete
- ✅ Self-contained (Phase 2 can execute from this)
- ✅ Templates are copy-paste ready
- ✅ Skill specification is implementable

**Create: docs/plans/PROACTIVE_SYSTEM_SPEC.md**
