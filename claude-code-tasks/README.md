# Claude Code Task System

**Created**: 2025-10-30  
**Purpose**: Structured delegation of validation work to Claude Code with TDD and checkpoints  
**Project**: Compression Framework Validation

---

## Overview

This directory contains autonomous task specifications for Claude Code. Each task is designed to be:
- **Self-contained**: All context, specs, and success criteria included
- **TDD-based**: Tests written first, then implementation
- **Checkpoint-driven**: Incremental validation at each phase
- **Independently executable**: No back-and-forth needed

---

## Task Structure

Each task file contains:
1. **Project Context**: Brief background
2. **Objective**: What to build
3. **TDD Approach**: Test-first methodology
4. **Checkpoint System**: 3 stages with validation
5. **Technical Specifications**: Detailed requirements
6. **Test Cases**: Concrete examples with expected results
7. **Implementation Guidelines**: Code templates and structure
8. **Validation Report Template**: How to document results
9. **Success Criteria**: Pass/fail conditions
10. **Dependencies**: What this enables

---

## Current Tasks

### Phase 1: Foundation (Parallel Execution)

#### ✅ TASK-2.1: Compression Score Algorithm
**File**: `TASK_2.1_compression_score.md`  
**Priority**: CRITICAL (MVP requirement)  
**Estimated**: 4-8 hours  
**Status**: Ready for delegation  
**Dependencies**: None

**What it does**: Build algorithm to detect how compressed text already is (0.0-1.0 scale) to prevent repeated compression and information loss.

**Deliverables**:
- `scripts/compression_score.py`
- `tests/test_compression_score.py`
- Three test documents (verbose, moderate, compressed)
- Three checkpoint reports
- Validation report

**Checkpoints**:
1. Tests written (all fail)
2. Basic implementation (all pass)
3. Validated against manual assessment

---

#### ✅ TASK-1.2: Token Drift Detection
**File**: `TASK_1.2_token_drift.md`  
**Priority**: HIGH (MVP requirement)  
**Estimated**: 2-4 hours  
**Status**: Ready for delegation  
**Dependencies**: None

**What it does**: Detect when previously-compressed documents have grown due to new content, triggering re-compression recommendations.

**Deliverables**:
- `scripts/detect_token_drift.py`
- `tests/test_token_drift.py`
- Six test documents with headers
- Three checkpoint reports
- Validation report

**Checkpoints**:
1. Tests written (all fail)
2. Basic implementation (all pass)
3. Validated on real project docs

---

### Phase 2: Integration (Sequential Execution)

#### ⏳ TASK-2.2: Round-Trip Compression Test
**Status**: Template ready, awaiting Phase 1 completion  
**Depends on**: TASK-2.1 (compression score)  
**Estimated**: 3-5 hours

**What it does**: Prove that attempting to compress already-compressed content is correctly refused (idempotency).

**Create when**: TASK-2.1 validation passes

---

#### ⏳ TASK-1.1: Content Density Analyzer
**Status**: Template ready, awaiting Phase 1 completion  
**Depends on**: TASK-2.1 (compression score) + TASK-1.2 (token drift)  
**Estimated**: 4-6 hours

**What it does**: Split documents into sections, score each section, identify mixed compression states.

**Create when**: Both Phase 1 tasks complete

---

### Phase 3: Safety (Sequential Execution)

#### ⏳ TASK-2.3: Safety Checks Implementation
**Status**: Template ready, awaiting Phase 2 completion  
**Depends on**: TASK-2.1, TASK-2.2, TASK-1.1  
**Estimated**: 6-10 hours

**What it does**: Comprehensive safety gates preventing information loss (entity preservation, semantic similarity, minimal benefit detection).

**Create when**: Phase 2 tasks validated

---

### Phase 4: Enhancement (Optional)

#### ⏳ TASK-3.1: Style Analysis Baseline
**Status**: Specs in validation plan, not yet templated  
**Depends on**: None (independent)  
**Estimated**: 4-6 hours

**What it does**: Analyze text to extract current (σ, γ, κ) parameters for proactive style optimization.

#### ⏳ TASK-3.2: Document Header Specification
**Status**: Specs in validation plan, not yet templated  
**Type**: Documentation work (better done interactively)  
**Estimated**: 2-3 hours

#### ⏳ TASK-3.3: Claude Skill Behavior Test
**Status**: Specs in validation plan, not yet templated  
**Type**: Qualitative testing (better done interactively)  
**Estimated**: 2-4 hours

---

## How to Delegate to Claude Code

### Step 1: Review Task File
Read the task file to understand:
- What will be built
- Time estimate
- Dependencies (is it ready?)

### Step 2: Start Claude Code
```bash
cd /Users/dudley/Projects/Compression
claude-code
```

### Step 3: Provide Task Specification
```
I need you to complete a validation task for the compression project.

Please read and execute: claude-code-tasks/TASK_2.1_compression_score.md

Follow the TDD approach and checkpoint system exactly as specified.
Work autonomously - only ask questions if specifications are ambiguous.

Start with Checkpoint 1: Write all tests first (they should fail).
```

### Step 4: Monitor Progress
Claude Code will:
1. Read task specifications
2. Create project structure
3. Write tests (Checkpoint 1)
4. Implement code (Checkpoint 2)
5. Validate results (Checkpoint 3)
6. Generate reports

### Step 5: Review Deliverables
After completion, review:
- `checkpoints/checkpoint_X_*.md` - Progress reports
- `tests/test_*.py` - Test suite
- `scripts/*.py` - Implementation
- `validation_report_task_X.X.md` - Final validation

### Step 6: Approve or Request Changes
If validation passes → proceed to dependent tasks  
If validation fails → provide feedback, request refinement

---

## Adding Sequential Tasks

When Phase 1 completes and you want to add Phase 2 tasks:

### For TASK-2.2 (Round-Trip Test):

Create `TASK_2.2_round_trip_test.md` using this structure:

```markdown
# Claude Code Task: Round-Trip Compression Test (Task 2.2)

**Task ID**: TASK-2.2-ROUND-TRIP
**Priority**: HIGH (MVP requirement)
**Estimated Time**: 3-5 hours
**Approach**: TDD with checkpoint system
**Dependencies**: TASK-2.1 (compression score algorithm)

## Project Context
[2-3 sentences about compression project]

## Objective
Build test suite that proves compression is idempotent:
1. Compress verbose document
2. Measure compression score (should be 0.7-0.8)
3. Attempt to compress again
4. Verify tool refuses (score already ≥ 0.8)

## TDD Approach
[Checkpoint 1-3 structure]

## Checkpoint System
[Define 3 checkpoints]

## Technical Specifications
Copy from validation plan lines 235-263

## Test Cases
[Detailed test procedures]

## Implementation Guidelines
```python
# Import compression_score from Task 2.1
from scripts.compression_score import CompressionScorer

# Build test harness
def test_idempotency():
    # Test procedure here
    pass
```

## Success Criteria
- First compression succeeds
- Second compression refused
- Entity preservation ≥ 80%
- Clear refusal message

## Dependencies
Requires: scripts/compression_score.py from Task 2.1
```

**Source Material**: Lines 235-263 of `docs/plans/AUTOMATION_TOOL_VALIDATION_PLAN.md`

---

### For TASK-1.1 (Content Density Analyzer):

Create `TASK_1.1_content_analyzer.md` using similar structure:

**Key Additions**:
- Import `compression_score.py` from Task 2.1
- Import `detect_token_drift.py` from Task 1.2
- Use both to analyze sections
- Return section-level analysis

**Source Material**: Lines 90-133 of validation plan

---

### For TASK-2.3 (Safety Checks):

Create `TASK_2.3_safety_checks.md`:

**Key Additions**:
- Integrate all previous tasks
- Add entity preservation (spaCy NER)
- Add semantic similarity (sentence-transformers or BERTScore)
- Comprehensive safety gate system

**Source Material**: Lines 265-297 of validation plan

---

## Template for New Tasks

When creating a new task file:

```markdown
# Claude Code Task: [Task Name] (Task X.X)

**Task ID**: TASK-X.X-[SLUG]
**Priority**: [CRITICAL|HIGH|MEDIUM|LOW]
**Estimated Time**: X-Y hours
**Approach**: TDD with checkpoint system
**Dependencies**: [List or "None"]

## Project Context
[2-3 sentences]

## Objective
[What to build - 1 paragraph]

## TDD Approach
### Phase 1: Write Tests First (Checkpoint 1)
### Phase 2: Implement (Checkpoint 2)
### Phase 3: Validate (Checkpoint 3)

## Checkpoint System
### Checkpoint 1: [Name] ✓
**Deliverable**: [files]
**Validation**: [how to verify]
**Output**: [report file]

[Repeat for 2 and 3]

## Technical Specifications
[Detailed requirements, function signatures, return types]

## Test Cases
[3-6 test cases with expected results]

## Implementation Guidelines
[Code templates, libraries needed, structure]

## Test Template
[pytest template code]

## Validation Report Template
[Markdown template for final report]

## Success Criteria
### Must Pass
- [Critical requirements]

### Should Pass
- [Important requirements]

### Nice to Have
- [Optional enhancements]

## Final Deliverables
1. [List all expected files]

## Sequential Task Dependencies
**This task enables**: [What becomes possible]
**This task requires**: [What must be done first]

## Notes
[Any important context, decisions, or warnings]

**Working Directory**: /Users/dudley/Projects/Compression
```

---

## Task Execution Guidelines

### For Claude Code

When executing these tasks:

1. **Read entire task file first** - don't start coding immediately
2. **Follow TDD strictly** - tests before implementation
3. **Complete checkpoints sequentially** - validate before proceeding
4. **Document decisions** - if you tune parameters, explain why
5. **Generate reports** - checkpoint reports and final validation
6. **Test on real data** - use actual project docs in Phase 3
7. **Work autonomously** - only ask if specs are ambiguous

### For Human Reviewer

When reviewing completed work:

1. **Check checkpoint reports** - were phases completed in order?
2. **Run tests** - do they all pass?
3. **Review validation report** - does it meet success criteria?
4. **Test on edge cases** - try examples not in test suite
5. **Approve or provide feedback** - clear next steps

---

## Quality Standards

All tasks must meet:

- **Test Coverage**: 100% of specified test cases
- **Code Quality**: Clear, documented, maintainable
- **Performance**: Meets any specified benchmarks
- **Error Handling**: Graceful handling of edge cases
- **Documentation**: README explaining usage
- **Validation**: Comprehensive report with results

---

## Project Structure After Completion

```
/Users/dudley/Projects/Compression/
├── claude-code-tasks/          # This directory
│   ├── README.md               # This file
│   ├── TASK_2.1_compression_score.md
│   ├── TASK_1.2_token_drift.md
│   └── [future tasks]
├── scripts/                    # Implementations
│   ├── compression_score.py
│   ├── detect_token_drift.py
│   └── [future scripts]
├── tests/                      # Test suites
│   ├── test_compression_score.py
│   ├── test_token_drift.py
│   └── fixtures/
│       ├── verbose_doc.md
│       ├── moderate_doc.md
│       └── [more test docs]
├── checkpoints/                # Progress reports
│   ├── checkpoint_1_*.md
│   ├── checkpoint_2_*.md
│   └── checkpoint_3_*.md
├── validation_report_task_*.md # Final validations
└── [existing project structure]
```

---

## Status Tracking

### Completed Tasks
- [ ] TASK-2.1: Compression Score Algorithm
- [ ] TASK-1.2: Token Drift Detection

### In Progress
- [ ] None yet

### Ready to Start
- [x] TASK-2.1 (Phase 1)
- [x] TASK-1.2 (Phase 1)

### Blocked (Awaiting Dependencies)
- [ ] TASK-2.2 (needs 2.1)
- [ ] TASK-1.1 (needs 2.1 + 1.2)
- [ ] TASK-2.3 (needs 2.1, 2.2, 1.1)

---

## Notes

- **Parallel execution recommended** for Phase 1 (tasks are independent)
- **Sequential execution required** for Phases 2-3 (dependencies)
- **Task files are immutable** once delegated (don't edit during execution)
- **Create new task versions** if major changes needed (e.g., TASK_2.1_v2.md)
- **Keep validation reports** even after integration (historical record)

---

## Questions?

If task specifications are unclear:
1. Check `docs/plans/AUTOMATION_TOOL_VALIDATION_PLAN.md` for original specs
2. Review PROJECT.md for project context
3. Ask in main Claude session for clarification

**Working Directory**: /Users/dudley/Projects/Compression  
**Last Updated**: 2025-10-30
