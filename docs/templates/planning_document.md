---
compression:
  sigma: 0.6
  gamma: 0.6
  kappa: 0.5
  audience: dual
  tier: T1
  phase: active
  template: planning-document
  version: 1.0
---

# [Project/Initiative] Plan

## Overview
[What are we building/doing? Why does it matter? High-level vision statement]

## Goals
1. **Goal 1**: [Specific, measurable outcome]
2. **Goal 2**: [Specific, measurable outcome]
3. **Goal 3**: [Specific, measurable outcome]

## Key Milestones
| Milestone | Target Date | Owner | Key Deliverables |
|-----------|------------|-------|-----------------|
| Phase 1 | [Date] | [Person] | [What gets completed] |
| Phase 2 | [Date] | [Person] | [What gets completed] |
| Phase 3 | [Date] | [Person] | [What gets completed] |

## Workstreams

### Workstream 1: [Name]
**Owner**: [Name]
**Dependencies**: [What needs to happen first]
**Timeline**: [Duration and key milestones]

**Tasks**:
- Task 1.1 - [Description]
- Task 1.2 - [Description]
- Task 1.3 - [Description]

**Success Criteria**:
- [Measurable outcome 1]
- [Measurable outcome 2]

### Workstream 2: [Name]
[Continue pattern]

## Resource Requirements
| Resource | Current | Needed | Gap |
|----------|---------|--------|-----|
| Engineering FTE | 2 | 3 | +1 |
| Infrastructure | $5K | $8K | +$3K |

## Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| [Risk 1] | High/Med/Low | High/Med/Low | [How we'll prevent/handle] |
| [Risk 2] | High/Med/Low | High/Med/Low | [How we'll prevent/handle] |

## Success Metrics
- [Metric 1]: Target [value]
- [Metric 2]: Target [value]
- [Metric 3]: Target [value]

## Timeline
[Gantt or narrative description of project schedule]

## Next Steps
- [Action 1] - Owner [Person] - Due [Date]
- [Action 2] - Owner [Person] - Due [Date]

---

## Example: Template Library Creation Plan

---
compression:
  sigma: 0.6
  gamma: 0.6
  kappa: 0.5
  audience: dual
  tier: T1
  phase: active
  template: planning-document
  version: 1.0
---

# Template Library Creation Plan (Phase 2B)

## Overview
Create 8-template library from comprehensive compression specifications, enabling users to select pre-optimized document structures for common use cases. Templates provide frontmatter with compression parameters (σ, γ, κ) and structural guidance, allowing users to write efficiently from the start without post-processing. This unblocks Phase 2C (Claude Skill) and Phase 3 (integration guide).

Strategic importance: Templates are centerpiece of proactive compression methodology. Enable write-time compression rather than reactive post-processing. Critical path item for Phase 2 completion.

## Goals
1. **Complete template library**: 8 high-quality templates covering 80% of documentation use cases
2. **Enable template selection**: Provide clear guidance for users to choose correct template
3. **Demonstrate compression style**: Each template includes realistic examples showing target compression level
4. **Establish foundation**: Templates ready for Claude Skill integration and user adoption

## Key Milestones
| Milestone | Target Date | Owner | Key Deliverables |
|-----------|------------|-------|-----------------|
| Template creation | 2025-11-04 | Dudley | 8 template files complete |
| Example documentation | 2025-11-04 | Dudley | Realistic examples in each template |
| README & selection guide | 2025-11-04 | Dudley | Template selection guide + usage instructions |
| Validation & testing | 2025-11-04 | Dudley | Constraint validation, style verification |
| Git commit | 2025-11-04 | Dudley | Clean commit with complete deliverables |

## Workstreams

### Workstream 1: Core Templates (4 templates)
**Owner**: Dudley
**Dependencies**: Specification complete (PROACTIVE_SYSTEM_SPEC.md)
**Timeline**: 2 hours

**Tasks**:
- 1.1: High Compression Status template (σ=0.8, γ=0.4, κ=0.2)
- 1.2: Medium Compression Design template (σ=0.6, γ=0.6, κ=0.4)
- 1.3: High Compression Notes template (σ=0.8, γ=0.5, κ=0.2)
- 1.4: Medium Compression Research template (σ=0.5, γ=0.7, κ=0.5)

**Success Criteria**:
- Each template has complete YAML frontmatter with (σ, γ, κ) parameters
- Template structure matches parameter specifications (high σ = tables, high γ = detail, etc.)
- Realistic example content demonstrates compression style
- Constraint satisfied: σ + γ + κ ≥ C_min for each

### Workstream 2: Specialized Templates (3 templates)
**Owner**: Dudley
**Dependencies**: Core templates complete
**Timeline**: 1.5 hours

**Tasks**:
- 2.1: Decision Record template (σ=0.5, γ=0.7, κ=0.6, ADR format)
- 2.2: Quick Reference template (σ=0.9, γ=0.3, κ=0.1, power-user focused)
- 2.3: Educational Guide template (σ=0.4, γ=0.9, κ=0.8, onboarding focused)

**Success Criteria**:
- Each template serves clear specialized use case
- Examples appropriate to audience (power-users, new-users, decision-makers)
- Constraint satisfied: σ + γ + κ ≥ C_min for each
- Templates feel naturally different (not derivative)

### Workstream 3: Planning & Selection Guide
**Owner**: Dudley
**Dependencies**: All templates complete
**Timeline**: 1 hour

**Tasks**:
- 3.1: Planning Document template (σ=0.6, γ=0.6, κ=0.5)
- 3.2: Create README with selection decision matrix
- 3.3: Add parameter explanation and usage guidelines
- 3.4: Include customization guidance

**Success Criteria**:
- README provides clear template selection guidance
- Decision matrix maps document type → template
- Parameter explanation understandable to new users
- Usage examples show how to customize

### Workstream 4: Validation & Commitment
**Owner**: Dudley
**Dependencies**: All templates, README, examples complete
**Timeline**: 30 minutes

**Tasks**:
- 4.1: Validate constraint equation for all 8 templates
- 4.2: Verify examples demonstrate proper compression for parameters
- 4.3: Check markdown formatting and consistency
- 4.4: Create clean git commit with descriptive message
- 4.5: Verify templates ready for production use

**Success Criteria**:
- All constraints satisfied (σ + γ + κ ≥ C_min)
- Examples show authentic compression style (not just templates)
- Files follow markdown best practices
- Git history clean and well-documented

## Resource Requirements
| Resource | Current | Needed | Status |
|----------|---------|--------|--------|
| Specification (PROACTIVE_SYSTEM_SPEC.md) | ✓ | ✓ | Ready |
| Template examples (from spec section 3) | ✓ | ✓ | Available |
| Claude Code environment | ✓ | ✓ | Ready |
| Git repository | ✓ | ✓ | Ready |

## Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| Templates don't demonstrate compression style clearly | Medium | Medium | Include realistic full examples, not just structure |
| Parameters inconsistent with actual compression philosophy | Low | High | Validate constraint equation, review against spec examples |
| Users can't select appropriate template | Medium | Medium | Provide clear decision matrix, multiple selection criteria |
| Templates too rigid/prescriptive | Medium | Low | Document customization guidelines, note template as starting point |

## Success Metrics
- **Completeness**: 8 templates created + README + examples = 100%
- **Quality**: All constraints satisfied (σ + γ + κ ≥ C_min for all 8)
- **Usability**: Templates can be used immediately without confusion
- **Authenticity**: Examples demonstrate real compression style, not just structure

## Timeline
```
Day 1 (2-3 hours):
├─ Workstream 1: Core templates (Status, Design, Notes, Research)
├─ Workstream 2: Specialized templates (Decision, Reference, Educational)
├─ Workstream 3: Planning template + README
└─ Workstream 4: Validation + git commit

All work sequential (Workstream 2 depends on 1, 3 depends on 2, 4 depends on 3)
Estimated total: 4.5 hours
```

## Dependencies & Blockers
**Blocking**: PROACTIVE_SYSTEM_SPEC.md (complete - section 3 provides all template specifications and examples)
**Enabling**: Templates enable Phase 2C (Claude Skill) and Phase 3 (Integration Guide)
**No external blockers identified**

## Assumptions
- Specification is complete and accurate (Section 3 template designs are final)
- Examples from spec can be adapted for template content
- Templates don't require iterative user testing before delivery
- Constraint validation adequate quality gate (no additional testing)

## Next Steps
1. Create all 8 template files in `/docs/templates/`
2. Validate constraint equation for each (σ + γ + κ ≥ C_min)
3. Create README with selection guide and parameter explanation
4. Commit to git with message: "templates: Create 8-template library from proactive system spec (Phase 2B)"
5. Handoff to Phase 2C: Claude Skill specification and implementation

Constraint validation: σ=0.6 (balanced structure) + γ=0.6 (moderate detail with specific information) + κ=0.5 (moderate scaffolding with planning context) = 1.7 ≥ 1.0 (dual audience) ✓
