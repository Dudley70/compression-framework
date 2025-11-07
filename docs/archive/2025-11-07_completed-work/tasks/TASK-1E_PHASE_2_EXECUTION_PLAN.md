# TASK-1E: Create Phase 2 Execution Plan

Create detailed execution roadmap for Phase 2 (building proactive system).

**File**: docs/plans/PHASE_2_EXECUTION_PLAN.md (~600-800 lines)
**Context**: All Phase 1 documents, PROACTIVE_SYSTEM_SPEC.md (once created)
**Duration**: 90-120 min
**Note**: This task should run AFTER TASK-1B completes (needs the system spec)

## Deliverable Structure

### 1. Component Dependencies (~100 lines)

Dependency graph with rationale:
```
Frontmatter Standard (TASK 2.1)
  │ Why first: Templates and skill both read this
  │ Context: PROACTIVE_SYSTEM_SPEC.md section 2
  │ Blocks: All other Phase 2 work
  ↓
  ├──→ Template Library (TASK 2.2)
  │     Parallel with skill
  │     Context: Frontmatter + PROACTIVE_SYSTEM_SPEC section 3
  │
  └──→ Claude Skill (TASK 2.3)
        Parallel with templates
        Context: Frontmatter + PROACTIVE_SYSTEM_SPEC section 4
        ↓
        Integration Guide Content (TASK 2.4)
          Must be last
          Needs: Working templates + skill for examples
          Context: INTEGRATION_GUIDE_OUTLINE + completed system
```

### 2. Task Breakdown (~300 lines)

For each task (2.1, 2.2, 2.3, 2.4):

**TASK 2.1: Frontmatter Standard**
- Effort: 2-3 hours
- Context files: PROACTIVE_SYSTEM_SPEC.md section 2
- Context size: ~5K tokens
- Deliverable: FRONTMATTER_STANDARD.md
- Blocking: Nothing
- Blocks: Tasks 2.2, 2.3
- Can delegate: No (design decisions)
- Work type: Interactive (judgment needed)

**TASK 2.2: Template Library**
- Effort: 8-10 hours (1-1.5 hours per template)
- Context files: FRONTMATTER_STANDARD.md + PROACTIVE_SYSTEM_SPEC section 3
- Context size: ~10K tokens per template
- Deliverable: 5-8 template files + docs/proactive/TEMPLATES.md
- Blocking: Task 2.1
- Blocks: Task 2.4
- Can delegate: Yes (execution against spec)
- Work type: Can be parallel (each template independent)

**TASK 2.3: Claude Skill**
- Effort: 6-8 hours
- Context files: FRONTMATTER_STANDARD.md + PROACTIVE_SYSTEM_SPEC section 4
- Context size: ~15K tokens
- Deliverable: /mnt/skills/public/compression/SKILL.md
- Blocking: Task 2.1
- Blocks: Task 2.4
- Can delegate: Yes (clear specification)
- Work type: Single focused implementation

**TASK 2.4: Integration Guide Content**
- Effort: 8-10 hours
- Context files: INTEGRATION_GUIDE_OUTLINE + all templates + skill + examples
- Context size: ~30K tokens
- Deliverable: docs/INTEGRATION_GUIDE.md
- Blocking: Tasks 2.2, 2.3
- Blocks: Nothing
- Can delegate: No (synthesis and judgment)
- Work type: Interactive (requires examples from working system)

### 3. Session Planning (~150 lines)

**Session 2A: Frontmatter Standard** (2-3 hours, interactive)
- Load: PROACTIVE_SYSTEM_SPEC.md section 2
- Create: FRONTMATTER_STANDARD.md
- Validate: Schema is unambiguous, examples work
- Commit: "feat: Define frontmatter standard for proactive compression"
- Checkpoint: Enables templates + skill work

**Session 2B: Template Library** (Can delegate OR 3-4 hour session)
Option A - Delegate:
- Create task specs for each template
- Delegate all simultaneously
- Review and integrate results

Option B - Interactive:
- Create 3-4 core templates first session
- Remaining templates second session
- Test with examples

- Deliverable: Template files + documentation
- Commit: "feat: Add compression template library"
- Checkpoint: Templates ready for skill integration

**Session 2C: Claude Skill** (Can delegate OR 3-4 hour session)
- Load: FRONTMATTER_STANDARD.md + PROACTIVE_SYSTEM_SPEC section 4
- Create: /mnt/skills/public/compression/SKILL.md
- Test: With existing templates
- Validate: Reads parameters, applies correctly
- Commit: "feat: Add compression skill for proactive writing"
- Checkpoint: Proactive system complete

**Session 2D: Integration Guide** (3-4 hours, interactive)
- Load: All completed components
- Create examples using working system
- Write: docs/INTEGRATION_GUIDE.md
- Validate: Examples work, guide is practical
- Commit: "docs: Add integration guide for framework adoption"
- Checkpoint: v1.0 content complete

### 4. Delegation Strategy (~100 lines)

**CAN Delegate** (Sonnet can execute against spec):
- Template creation (TASK 2.2)
  * Each template follows clear specification
  * Examples provided in spec
  * Independent work per template
  
- Skill implementation (TASK 2.3)
  * Clear behavior specification
  * Technique mapping defined
  * Can validate against spec

**SHOULD NOT Delegate** (requires judgment):
- Frontmatter Standard (TASK 2.1)
  * Design decisions needed
  * Trade-offs to evaluate
  * Foundation for everything else
  
- Integration Guide (TASK 2.4)
  * Synthesis across components
  * Needs working examples
  * Judgment about what to include

**Parallel Opportunities**:
- Templates can be created simultaneously (each independent)
- Templates + Skill can be parallel (both depend on frontmatter only)
- Integration Guide must wait for both

### 5. Context Management (~100 lines)

Per task context requirements and loading strategy:

**Task 2.1** (Frontmatter):
```
Load upfront:
- PROACTIVE_SYSTEM_SPEC.md section 2 (~5K)
Self-contained: Yes
Additional context: None needed
```

**Task 2.2** (Templates):
```
Load upfront:
- FRONTMATTER_STANDARD.md (~2K)
- PROACTIVE_SYSTEM_SPEC.md section 3 (~8K)
Per template: ~10K tokens (can work independently)
Self-contained: Yes per template
```

**Task 2.3** (Skill):
```
Load upfront:
- FRONTMATTER_STANDARD.md (~2K)
- PROACTIVE_SYSTEM_SPEC.md section 4 (~8K)
- LSC techniques reference (~5K)
Total: ~15K tokens
Self-contained: Yes
```

**Task 2.4** (Integration Guide):
```
Load upfront:
- INTEGRATION_GUIDE_OUTLINE.md (~10K)
- All templates (~20K)
- Skill documentation (~5K)
Total: ~35K tokens
Self-contained: No (needs working examples)
Must test system while writing
```

### 6. Validation Criteria (~80 lines)

Per-task success criteria:

**Task 2.1**: Frontmatter Standard
- [ ] YAML schema is complete and unambiguous
- [ ] All parameters defined with ranges
- [ ] 3 examples (high/medium/low) work
- [ ] Can parse programmatically
- [ ] Templates can reference it

**Task 2.2**: Template Library
- [ ] 5-8 templates created
- [ ] Each has frontmatter with valid parameters
- [ ] Structure matches (σ,γ,κ) specification
- [ ] Examples are copy-paste ready
- [ ] Selection guide helps users choose

**Task 2.3**: Claude Skill
- [ ] Skill file in correct location
- [ ] Reads frontmatter correctly
- [ ] Maps (σ,γ,κ) to techniques
- [ ] Examples demonstrate behavior
- [ ] Maintains compression during edits

**Task 2.4**: Integration Guide
- [ ] All sections from outline completed
- [ ] Examples use real templates + skill
- [ ] Workflows are practical
- [ ] CCM case study included
- [ ] 20-30 pages comprehensive

### 7. Risk Mitigation (~70 lines)

**Risk 1**: Frontmatter format issues
- Mitigation: Get standard right first (blocks everything)
- Validate with test documents before templates
- Include extension points for future fields

**Risk 2**: Templates don't work with Skill
- Mitigation: Test integration early (after first template)
- Checkpoint after 2B ensures system works
- Can iterate before creating all templates

**Risk 3**: Integration Guide lacks examples
- Mitigation: Do last (after 2B + 2C complete)
- Can test actual workflows
- Real examples from working system

**Risk 4**: Delegation quality concerns
- Mitigation: Comprehensive task specs
- Review checkpoints
- Can iterate if needed
- Conservative: Do interactive instead

## Output Format

```markdown
# Phase 2 Execution Plan

**Phase**: Core Content Creation
**Duration**: 20-25 hours total
**Deliverable**: Proactive system (templates + skill + guide)

## Component Dependencies
[Graph and rationale]

## Task Breakdown
[Detailed specs for 2.1-2.4]

## Session Planning
[Session-by-session plan]

## Delegation Strategy
[What can/can't be delegated]

## Context Management
[Per-task requirements]

## Validation Criteria
[Success criteria per task]

## Risk Mitigation
[Risks and mitigations]
```

## Success Criteria
- ✅ All 4 tasks (2.1-2.4) specified
- ✅ Dependencies clearly mapped
- ✅ Session plans actionable
- ✅ Delegation strategy defined
- ✅ Context requirements documented
- ✅ 600-800 lines total

**Create: docs/plans/PHASE_2_EXECUTION_PLAN.md**
