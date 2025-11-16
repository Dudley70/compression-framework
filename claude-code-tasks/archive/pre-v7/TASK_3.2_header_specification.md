# Claude Code Task: Document Header Specification (Task 3.2)

**Task ID**: TASK-3.2-HEADER-SPECIFICATION  
**Priority**: MEDIUM (Enhancement)  
**Estimated Time**: 2-3 hours  
**Approach**: TDD with checkpoint system  
**Dependencies**: None (independent)

---

## Project Context

This is part of a compression research project evaluating methods for AI context optimization. We've developed a unified theory where all compression techniques optimize three parameters (σ, γ, κ) subject to comprehension constraints.

**Current Phase**: Validation - testing critical design assumptions before building the full automation tool.

**This Task's Role**: Create formal YAML header specification that provides metadata for documents, enabling Claude to understand document type, compression state, and target style without reading full content.

---

## Objective

Create comprehensive document header specification that:
1. Defines YAML frontmatter structure for all document types
2. Specifies required and optional metadata fields
3. Provides clear examples for 10+ document types
4. Enables machine-readable compression tracking
5. Guides Claude in maintaining appropriate style

**Core Problem**: Tool needs structured metadata to make intelligent decisions about compression without reading entire documents.

**Solution**: Standardized YAML headers with document classification, compression tracking, and style guidance.

---

## TDD Approach

### Phase 1: Define Test Cases (Checkpoint 1)
1. Create example documents with headers for major document types
2. Define validation criteria (required fields, format rules)
3. Write validation test suite
4. **Checkpoint**: Test suite ready (tests will validate specification)

### Phase 2: Write Specification (Checkpoint 2)
1. Document header structure and field definitions
2. Provide examples for all document types
3. Explain usage patterns and best practices
4. Pass validation tests
5. **Checkpoint**: Specification complete and validated

### Phase 3: Apply to Real Documents (Checkpoint 3)
1. Add headers to 5+ real project documents
2. Verify headers provide needed information
3. Test Claude's ability to parse and understand headers
4. **Checkpoint**: Works on real project documentation

---

## Checkpoint System

### Checkpoint 1: Test Cases Defined ✓
**Deliverable**: `tests/test_header_validation.py` (validation suite)  
**Validation**:
```bash
# Tests verify header examples are valid YAML
# Tests check required fields present
# Tests validate field value constraints
pytest tests/test_header_validation.py
```
**Output**: `checkpoints/checkpoint_1_header_tests.md`

### Checkpoint 2: Specification Written ✓
**Deliverable**: `docs/reference/DOCUMENT_HEADER_SPECIFICATION.md`  
**Validation**:
```bash
# Specification examples pass validation tests
# All document types have examples
# Format is clear and unambiguous
pytest tests/test_header_validation.py
```
**Output**: `checkpoints/checkpoint_2_header_spec.md`

### Checkpoint 3: Real-World Application ✓
**Deliverable**: Headers added to 5+ project docs  
**Validation**: Claude can parse and use headers effectively  
**Output**: `checkpoints/checkpoint_3_header_applied.md`

---

## Technical Specifications

### Header Structure

```yaml
---
# Document Classification (REQUIRED)
doc_type: [type]           # See Document Types section
audience: [audience]       # See Audience section
layer: [layer]             # See Information Layer section
phase: [phase]             # See Lifecycle Phase section
purpose: [purpose]         # See Purpose section

# Style Guidance (REQUIRED for compressed docs)
target_style:
  sigma: 0.0-1.0          # Structure density (0=prose, 1=data)
  gamma: 0.0-1.0          # Semantic granularity (0=keywords, 1=full)
  kappa: 0.0-1.0          # Contextual scaffolding (0=none, 1=full)

# Compression Tracking (REQUIRED if compressed)
compression:
  last_full_compression: YYYY-MM-DD HH:MM TZ
  baseline_tokens: [number]
  parameters: {σ: X.X, γ: X.X, κ: X.X}
  validation:
    entity_preservation: 0.0-1.0
    semantic_similarity: 0.0-1.0

# Writing Guidance (OPTIONAL)
writing_guide:
  preferred_patterns: |
    Guidance on what works well for this document type
  anti_patterns: |
    What to avoid when writing/updating this document
---
```

---

## Field Definitions

### Document Type (doc_type)

**Required**: Yes  
**Format**: SCREAMING_SNAKE_CASE  
**Purpose**: Classify document for appropriate compression strategy

**Valid Values**:
- `API_REFERENCE`: API documentation (endpoints, parameters, responses)
- `TUTORIAL`: Step-by-step learning content
- `SESSION_HANDOVER`: Session-to-session context transfer
- `PROJECT_CONTEXT`: Strategic context and decision history
- `TASK_SPECIFICATION`: Autonomous task delegation specs
- `VALIDATION_REPORT`: Test results and validation findings
- `ANALYSIS`: Research findings and detailed analysis
- `PLAN`: Implementation plans and roadmaps
- `REFERENCE`: Quick reference guides and lookup tables
- `PATTERN`: Reusable patterns and best practices
- `METHODOLOGY`: Process documentation and frameworks
- `RESEARCH`: Literature review and external research
- `PROPOSAL`: Design proposals and RFCs

---

### Audience (audience)

**Required**: Yes  
**Format**: kebab-case  
**Purpose**: Determine appropriate (γ, κ) parameters

**Valid Values**:
- `llm-only`: LLM consumption only (minimal scaffolding)
- `human-technical`: Technical users (assume expertise)
- `human-general`: General audience (more explanation)
- `multi-role`: Both LLM and human readers (balanced)

**Compression Impact**:
- `llm-only`: κ can be very low (0.1-0.3)
- `human-technical`: κ moderate (0.3-0.5)
- `human-general`: κ higher (0.5-0.7)
- `multi-role`: κ balanced (0.4-0.6)

---

### Information Layer (layer)

**Required**: Yes  
**Format**: PascalCase  
**Purpose**: Classify information lifecycle and access patterns

**Valid Values**:
- `Session`: Per-session ephemeral context
- `Strategic`: Long-term project context
- `Control`: Configuration and instructions
- `Operational`: Active work and tasks
- `Archive`: Historical reference

**Compression Guidelines**:
- `Session`: Aggressive OK (99%+ for completed sessions)
- `Strategic`: Moderate (70-85%)
- `Control`: Conservative (minimal or none)
- `Operational`: Moderate (70-85%)
- `Archive`: Ultra-aggressive (95-99%)

---

### Lifecycle Phase (phase)

**Required**: Yes  
**Format**: PascalCase  
**Purpose**: Track document maturity and update frequency

**Valid Values**:
- `Active`: Currently being written/updated frequently
- `Complete`: Finished, infrequent updates
- `Archived`: Historical, rarely accessed
- `Deprecated`: Superseded by newer version

**Update Triggers**:
- `Active` → `Complete`: No updates for 7+ days
- `Complete` → `Archived`: No updates for 30+ days
- `Archived` → `Deprecated`: Replaced by new document

---

### Purpose (purpose)

**Required**: Yes  
**Format**: PascalCase  
**Purpose**: Understand document's role in workflow

**Valid Values**:
- `Execution`: Active instructions for task completion
- `Learning`: Educational content for understanding
- `Reference`: Quick lookup information
- `Audit`: Historical record keeping
- `Planning`: Future work and design
- `Analysis`: Research and investigation results

---

### Target Style (target_style)

**Required**: Yes (for all documents)  
**Format**: Object with σ, γ, κ parameters  
**Purpose**: Guide compression and writing style

**Field Definitions**:
```yaml
target_style:
  sigma: 0.0-1.0    # Structure density
  gamma: 0.0-1.0    # Semantic granularity  
  kappa: 0.0-1.0    # Contextual scaffolding
```

**Parameter Meanings**:
- **σ (sigma)**: 0=narrative prose, 1=structured data/lists
- **γ (gamma)**: 0=keyword summary, 1=full semantic detail
- **κ (kappa)**: 0=no context/explanation, 1=full scaffolding

**Common Patterns**:
- API Reference: {σ: 0.8, γ: 0.6, κ: 0.2}
- Tutorial: {σ: 0.4, γ: 0.8, κ: 0.7}
- Session Handover: {σ: 0.7, γ: 0.7, κ: 0.3}
- Strategic Context: {σ: 0.5, γ: 0.8, κ: 0.5}

---

### Compression Tracking (compression)

**Required**: Only if document has been compressed  
**Format**: Object with compression metadata  
**Purpose**: Track compression state and enable drift detection

**Field Definitions**:
```yaml
compression:
  last_full_compression: "YYYY-MM-DD HH:MM TZ"
  baseline_tokens: 1234
  parameters: {σ: 0.8, γ: 0.6, κ: 0.2}
  validation:
    entity_preservation: 0.94
    semantic_similarity: 0.82
```

**Field Details**:
- `last_full_compression`: ISO datetime with timezone
- `baseline_tokens`: Token count after compression
- `parameters`: Actual (σ, γ, κ) values used
- `validation.entity_preservation`: % of key entities preserved
- `validation.semantic_similarity`: Semantic similarity score

---

### Writing Guidance (writing_guide)

**Required**: No (optional)  
**Format**: Multi-line text object  
**Purpose**: Provide context-specific writing advice

**Field Definitions**:
```yaml
writing_guide:
  preferred_patterns: |
    - Use bullet points for API parameters
    - Include code examples for each endpoint
    - Keep descriptions under 2 sentences
  anti_patterns: |
    - Don't write prose paragraphs
    - Avoid lengthy explanations
    - Don't duplicate information from code
```

---

## Document Type Examples

### Example 1: API Reference (Compressed)

```markdown
---
doc_type: API_REFERENCE
audience: llm-only
layer: Operational
phase: Complete
purpose: Reference

target_style:
  sigma: 0.8
  gamma: 0.6
  kappa: 0.2

compression:
  last_full_compression: 2025-10-30 14:30 AEDT
  baseline_tokens: 450
  parameters: {σ: 0.8, γ: 0.6, κ: 0.2}
  validation:
    entity_preservation: 0.96
    semantic_similarity: 0.89

writing_guide:
  preferred_patterns: |
    ✓ Bullet lists for parameters/returns
    ✓ Code examples inline
    ✓ HTTP status codes explicit
  anti_patterns: |
    ✗ Prose explanations
    ✗ Redundant descriptions
    ✗ Excessive scaffolding
---

# API Reference

## POST /auth
- Body: `{username, password}`
- Returns: `{token}` (200) | `{error}` (401)
- Headers: `Content-Type: application/json`

## GET /users
- Auth: Bearer token required
- Returns: User array
- Filters: `?role=admin&status=active`
```

---

### Example 2: Tutorial (Uncompressed)

```markdown
---
doc_type: TUTORIAL
audience: human-general
layer: Operational
phase: Active
purpose: Learning

target_style:
  sigma: 0.4
  gamma: 0.8
  kappa: 0.7

writing_guide:
  preferred_patterns: |
    ✓ Step-by-step instructions
    ✓ Explain the "why" behind each step
    ✓ Include troubleshooting tips
  anti_patterns: |
    ✗ Don't skip explanatory context
    ✗ Don't assume prior knowledge
    ✗ Don't use jargon without explanation
---

# Getting Started Tutorial

## Introduction

This tutorial walks you through setting up your first project. We'll cover
installation, configuration, and running your first example. By the end,
you'll understand the basic workflow and be ready to build your own applications.

## Step 1: Installation

First, you'll need to install the CLI tool. This tool provides commands for
creating projects, running tests, and deploying applications...
```

---

### Example 3: Session Handover (Compressed)

```markdown
---
doc_type: SESSION_HANDOVER
audience: llm-only
layer: Session
phase: Active
purpose: Execution

target_style:
  sigma: 0.7
  gamma: 0.7
  kappa: 0.3

compression:
  last_full_compression: 2025-10-30 10:00 AEDT
  baseline_tokens: 350
  parameters: {σ: 0.7, γ: 0.7, κ: 0.3}
  validation:
    entity_preservation: 0.92
    semantic_similarity: 0.85

writing_guide:
  preferred_patterns: |
    ✓ Structured sections (WHERE/ACCOMPLISHED/NEXT)
    ✓ Bullet lists for tasks
    ✓ File paths explicit
  anti_patterns: |
    ✗ Narrative prose
    ✗ Redundant context
    ✗ Unnecessary elaboration
---

## Session Status: 2025-10-30 14:30 AEDT

### WHERE WE ARE
Phase 2 validation: Task 1.1 executing via Claude Code delegation

### ACCOMPLISHED THIS SESSION
- Session initialized, git status clean
- Task 1.1 delegated (content analyzer)
- Task 3.2 spec created

### NEXT ACTIONS
1. Monitor Task 1.1 completion
2. Delegate Task 2.3 when ready
3. Evaluate Phase 3 options

### BLOCKERS
None

### ACTIVE FILES
- SESSION.md (this file)
- claude-code-tasks/TASK_1.1_content_analyzer.md

### GIT STATE
On branch main, clean
```

---

### Example 4: Project Context (Moderately Compressed)

```markdown
---
doc_type: PROJECT_CONTEXT
audience: multi-role
layer: Strategic
phase: Active
purpose: Reference

target_style:
  sigma: 0.5
  gamma: 0.8
  kappa: 0.5

compression:
  last_full_compression: 2025-10-30 12:00 AEDT
  baseline_tokens: 2400
  parameters: {σ: 0.5, γ: 0.8, κ: 0.5}
  validation:
    entity_preservation: 0.94
    semantic_similarity: 0.88

writing_guide:
  preferred_patterns: |
    ✓ Strategic Context section (high-level overview)
    ✓ Decision log (chronological, detailed)
    ✓ Clear section headers
  anti_patterns: |
    ✗ Don't delete decision history
    ✗ Don't rewrite past decisions
    ✗ Don't bury key context deep in text
---

# Project Name

**Created**: 2025-10-29
**Last Strategic Update**: 2025-10-30

## Strategic Context

### Overview
Brief project description, current status, and key achievements.

### Current Status
**Phase**: Validation - 60% complete
- MVP validation complete (3/3 tasks)
- Phase 2 in progress (Task 1.1 executing)

### Core Principles
- Principle 1: Explanation
- Principle 2: Explanation
```

---

### Example 5: Task Specification (Uncompressed)

```markdown
---
doc_type: TASK_SPECIFICATION
audience: llm-only
layer: Operational
phase: Active
purpose: Execution

target_style:
  sigma: 0.6
  gamma: 0.9
  kappa: 0.6

writing_guide:
  preferred_patterns: |
    ✓ Comprehensive context (all details needed)
    ✓ TDD approach (tests first)
    ✓ Checkpoint system (incremental validation)
    ✓ Concrete examples with expected outputs
  anti_patterns: |
    ✗ Don't assume context known
    ✗ Don't leave ambiguity
    ✗ Don't skip edge cases
---

# Claude Code Task: [Task Name]

**Task ID**: TASK-X.X-NAME
**Priority**: HIGH
**Estimated Time**: 4-6 hours
**Dependencies**: [List dependencies]

## Project Context
[Full background needed for autonomous execution]

## Objective
[Clear statement of what to build]

## TDD Approach
[Three phases with checkpoints]

## Test Cases
[Concrete examples with expected results]
```

---

### Example 6: Validation Report (Uncompressed)

```markdown
---
doc_type: VALIDATION_REPORT
audience: multi-role
layer: Operational
phase: Complete
purpose: Audit

target_style:
  sigma: 0.6
  gamma: 0.8
  kappa: 0.4

writing_guide:
  preferred_patterns: |
    ✓ Summary upfront
    ✓ Test results table
    ✓ Metrics with units
    ✓ Clear pass/fail status
  anti_patterns: |
    ✗ Don't bury conclusions
    ✗ Don't skip test numbers
    ✗ Don't omit edge cases
---

# Validation Report: [Task Name]

**Date**: 2025-10-30
**Task**: TASK-X.X
**Status**: PASS

## Summary
[Overview of validation results]

## Test Results

| Test | Expected | Actual | Status |
|------|----------|--------|--------|
| Test 1 | X | X | ✓ PASS |
| Test 2 | Y | Y | ✓ PASS |

## Conclusions
[Key findings and recommendations]
```

---

### Example 7: Analysis Document (Moderately Compressed)

```markdown
---
doc_type: ANALYSIS
audience: multi-role
layer: Operational
phase: Complete
purpose: Reference

target_style:
  sigma: 0.5
  gamma: 0.8
  kappa: 0.5

compression:
  last_full_compression: 2025-10-30 11:00 AEDT
  baseline_tokens: 1800
  parameters: {σ: 0.5, γ: 0.8, κ: 0.5}
  validation:
    entity_preservation: 0.91
    semantic_similarity: 0.84
---

# Analysis: [Topic]

**Created**: 2025-10-30
**Status**: Complete

## Executive Summary
[Key findings in 2-3 sentences]

## Methodology
Research approach and data sources used.

## Findings
Detailed analysis organized by theme.

## Conclusions
Implications and recommendations.
```

---

### Example 8: Research Document (Uncompressed)

```markdown
---
doc_type: RESEARCH
audience: multi-role
layer: Operational
phase: Complete
purpose: Learning

target_style:
  sigma: 0.4
  gamma: 0.9
  kappa: 0.6
---

# Research: [Topic]

**Created**: 2025-10-30
**Sources**: 40+ academic papers reviewed

## Research Question
What dimensions are necessary for compression parameter model?

## Literature Review
Comprehensive review of information theory, cognitive science, and
software engineering literature relevant to compression.

### Information Theory
[Detailed findings with citations]

### Cognitive Science
[Detailed findings with citations]

## Conclusions
Research supports 3D model completeness for project-scale documentation.
```

---

### Example 9: Plan Document (Moderately Compressed)

```markdown
---
doc_type: PLAN
audience: multi-role
layer: Operational
phase: Active
purpose: Planning

target_style:
  sigma: 0.6
  gamma: 0.7
  kappa: 0.4
---

# Implementation Plan: [Feature]

**Created**: 2025-10-30
**Timeline**: 4 weeks
**Status**: In Progress

## Overview
High-level summary of implementation approach.

## Phases

### Phase 1: Foundation (Week 1)
- Task 1: Description
- Task 2: Description

### Phase 2: Integration (Week 2)
- Task 3: Description
- Task 4: Description

## Dependencies
Critical path and blockers identified.

## Success Metrics
How we'll measure completion.
```

---

### Example 10: Reference Guide (Compressed)

```markdown
---
doc_type: REFERENCE
audience: llm-only
layer: Operational
phase: Complete
purpose: Reference

target_style:
  sigma: 0.9
  gamma: 0.5
  kappa: 0.1

compression:
  last_full_compression: 2025-10-30 09:00 AEDT
  baseline_tokens: 280
  parameters: {σ: 0.9, γ: 0.5, κ: 0.1}
  validation:
    entity_preservation: 0.98
    semantic_similarity: 0.92
---

# Quick Reference: Git Commands

## Commit
`git add .` → `git commit -m "msg"` → `git push`

## Branch
- Create: `git checkout -b name`
- Switch: `git checkout name`
- Delete: `git branch -d name`

## Status
`git status` → changes
`git log -5` → recent commits
`git diff` → unstaged changes
```

---

## Validation Tests

### Test 1: Required Fields Present

```python
def test_required_fields():
    """All headers must have required fields."""
    required = ['doc_type', 'audience', 'layer', 'phase', 'purpose', 'target_style']
    
    for example in header_examples:
        header = parse_yaml_header(example)
        for field in required:
            assert field in header, f"Missing required field: {field}"
```

### Test 2: Valid Field Values

```python
def test_valid_field_values():
    """Field values must be from valid enums."""
    doc_types = ['API_REFERENCE', 'TUTORIAL', 'SESSION_HANDOVER', ...]
    audiences = ['llm-only', 'human-technical', 'human-general', 'multi-role']
    
    for example in header_examples:
        header = parse_yaml_header(example)
        assert header['doc_type'] in doc_types
        assert header['audience'] in audiences
```

### Test 3: Parameter Ranges

```python
def test_parameter_ranges():
    """σ, γ, κ must be in [0.0, 1.0]."""
    for example in header_examples:
        header = parse_yaml_header(example)
        style = header['target_style']
        
        assert 0.0 <= style['sigma'] <= 1.0
        assert 0.0 <= style['gamma'] <= 1.0
        assert 0.0 <= style['kappa'] <= 1.0
```

### Test 4: Compression Tracking Consistency

```python
def test_compression_tracking():
    """If compressed, must have all compression fields."""
    for example in compressed_examples:
        header = parse_yaml_header(example)
        compression = header.get('compression')
        
        assert compression is not None
        assert 'last_full_compression' in compression
        assert 'baseline_tokens' in compression
        assert 'parameters' in compression
        assert 'validation' in compression
```

### Test 5: DateTime Format

```python
def test_datetime_format():
    """Timestamps must be ISO format with timezone."""
    pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2} [A-Z]+'
    
    for example in compressed_examples:
        header = parse_yaml_header(example)
        timestamp = header['compression']['last_full_compression']
        
        assert re.match(pattern, timestamp)
```

---

## Implementation Guidelines

### Creating the Specification Document

Structure: `/Users/dudley/Projects/Compression/docs/reference/DOCUMENT_HEADER_SPECIFICATION.md`

**Sections**:
1. **Overview**: Purpose and scope
2. **Quick Start**: 3-minute guide with common examples
3. **Field Reference**: Complete field definitions
4. **Document Type Guide**: Examples for all types
5. **Validation Rules**: What makes a valid header
6. **Usage Patterns**: Common scenarios and solutions
7. **Migration Guide**: Adding headers to existing docs

**Writing Style**:
- Clear and concise
- Examples for every concept
- Easy to scan (headers, lists, tables)
- Machine-readable format (YAML)
- Both comprehensive (reference) and quick (guide)

---

## Test Implementation

### File: `tests/test_header_validation.py`

```python
import pytest
import yaml
import re
from pathlib import Path

class TestHeaderValidation:
    """Validate document header specification."""
    
    @pytest.fixture
    def examples_dir(self):
        return Path(__file__).parent / "fixtures" / "headers"
    
    def test_all_examples_parse(self, examples_dir):
        """All example headers are valid YAML."""
        for example_file in examples_dir.glob("*.md"):
            content = example_file.read_text()
            header = extract_yaml_header(content)
            
            # Should parse without error
            parsed = yaml.safe_load(header)
            assert parsed is not None
    
    def test_required_fields_present(self, examples_dir):
        """All required fields present in examples."""
        required = ['doc_type', 'audience', 'layer', 'phase', 'purpose', 'target_style']
        
        for example_file in examples_dir.glob("*.md"):
            content = example_file.read_text()
            header = extract_yaml_header(content)
            parsed = yaml.safe_load(header)
            
            for field in required:
                assert field in parsed, f"{example_file.name}: missing {field}"
    
    def test_target_style_structure(self, examples_dir):
        """target_style has σ, γ, κ parameters."""
        for example_file in examples_dir.glob("*.md"):
            content = example_file.read_text()
            header = extract_yaml_header(content)
            parsed = yaml.safe_load(header)
            
            style = parsed['target_style']
            assert 'sigma' in style
            assert 'gamma' in style
            assert 'kappa' in style
            
            # All in valid range
            assert 0.0 <= style['sigma'] <= 1.0
            assert 0.0 <= style['gamma'] <= 1.0
            assert 0.0 <= style['kappa'] <= 1.0
    
    def test_compressed_docs_have_tracking(self, examples_dir):
        """Documents with compression have tracking fields."""
        compressed_files = [
            "api_reference_compressed.md",
            "session_handover_compressed.md",
            "project_context_compressed.md"
        ]
        
        for filename in compressed_files:
            filepath = examples_dir / filename
            if not filepath.exists():
                continue
                
            content = filepath.read_text()
            header = extract_yaml_header(content)
            parsed = yaml.safe_load(header)
            
            assert 'compression' in parsed
            comp = parsed['compression']
            assert 'last_full_compression' in comp
            assert 'baseline_tokens' in comp
            assert 'parameters' in comp
            assert 'validation' in comp
    
    def test_datetime_format_valid(self, examples_dir):
        """Compression timestamps use correct format."""
        pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2} [A-Z]+$'
        
        for example_file in examples_dir.glob("*.md"):
            content = example_file.read_text()
            header = extract_yaml_header(content)
            parsed = yaml.safe_load(header)
            
            if 'compression' not in parsed:
                continue
            
            timestamp = parsed['compression']['last_full_compression']
            assert re.match(pattern, timestamp), f"Invalid timestamp: {timestamp}"
    
    def test_doc_type_enum_valid(self, examples_dir):
        """doc_type values match specification."""
        valid_types = [
            'API_REFERENCE', 'TUTORIAL', 'SESSION_HANDOVER', 
            'PROJECT_CONTEXT', 'TASK_SPECIFICATION', 'VALIDATION_REPORT',
            'ANALYSIS', 'PLAN', 'REFERENCE', 'PATTERN', 'METHODOLOGY',
            'RESEARCH', 'PROPOSAL'
        ]
        
        for example_file in examples_dir.glob("*.md"):
            content = example_file.read_text()
            header = extract_yaml_header(content)
            parsed = yaml.safe_load(header)
            
            assert parsed['doc_type'] in valid_types


def extract_yaml_header(content: str) -> str:
    """Extract YAML frontmatter from markdown."""
    lines = content.split('\n')
    if not lines[0].strip() == '---':
        return ""
    
    header_lines = []
    for line in lines[1:]:
        if line.strip() == '---':
            break
        header_lines.append(line)
    
    return '\n'.join(header_lines)
```

---

## Project Structure

```
/Users/dudley/Projects/Compression/
├── docs/
│   └── reference/
│       └── DOCUMENT_HEADER_SPECIFICATION.md  # Main deliverable
├── tests/
│   ├── test_header_validation.py             # Validation suite
│   └── fixtures/
│       └── headers/
│           ├── api_reference_compressed.md
│           ├── tutorial_uncompressed.md
│           ├── session_handover_compressed.md
│           ├── project_context_compressed.md
│           ├── task_specification.md
│           ├── validation_report.md
│           ├── analysis_compressed.md
│           ├── research_uncompressed.md
│           ├── plan_document.md
│           └── reference_compressed.md
├── checkpoints/
│   ├── checkpoint_1_header_tests.md
│   ├── checkpoint_2_header_spec.md
│   └── checkpoint_3_header_applied.md
└── validation_report_task_3.2.md
```

---

## Checkpoint Reports

### Checkpoint 1 Report Template

```markdown
# Checkpoint 1: Header Validation Tests

**Date**: [YYYY-MM-DD]
**Status**: [PASS/FAIL]

## Test Suite Created

### Files Created
- `tests/test_header_validation.py` (validation suite)
- `tests/fixtures/headers/*.md` (10+ example files)

### Test Coverage
- ✓ YAML parsing validation
- ✓ Required fields present
- ✓ target_style structure correct
- ✓ Compression tracking complete
- ✓ DateTime format valid
- ✓ doc_type enum valid

### Test Execution
```bash
pytest tests/test_header_validation.py -v
# Expected: Tests run, specification not yet written
```

## Next Steps
Write specification document that passes these tests.
```

---

### Checkpoint 2 Report Template

```markdown
# Checkpoint 2: Specification Document Complete

**Date**: [YYYY-MM-DD]
**Status**: [PASS/FAIL]

## Specification Created

**File**: `docs/reference/DOCUMENT_HEADER_SPECIFICATION.md`
**Size**: [X] lines
**Coverage**: 10+ document type examples

### Sections Included
- ✓ Overview and quick start
- ✓ Complete field reference
- ✓ Document type examples (10+)
- ✓ Validation rules
- ✓ Usage patterns
- ✓ Migration guide

### Test Validation
```bash
pytest tests/test_header_validation.py -v
# Expected: All tests PASS
```

**Result**: [X/X] tests passing

## Quality Check
- ✓ Clear and unambiguous
- ✓ Examples for all document types
- ✓ Machine-readable format
- ✓ Easy to scan and reference
- ✓ Comprehensive coverage

## Next Steps
Apply headers to real project documents.
```

---

### Checkpoint 3 Report Template

```markdown
# Checkpoint 3: Applied to Real Documents

**Date**: [YYYY-MM-DD]
**Status**: [PASS/FAIL]

## Headers Added

Applied specification to project documentation:

| Document | Type | Status | Notes |
|----------|------|--------|-------|
| SESSION.md | SESSION_HANDOVER | ✓ Added | Works well |
| PROJECT.md | PROJECT_CONTEXT | ✓ Added | Clear metadata |
| TASK_1.1_*.md | TASK_SPECIFICATION | ✓ Added | Helpful for Claude Code |
| validation_report_*.md | VALIDATION_REPORT | ✓ Added | Good structure |
| docs/plans/*.md | PLAN | ✓ Added | Makes type clear |

## Claude Comprehension Test

Asked Claude to:
1. Parse header from SESSION.md
2. Explain document type and target style
3. Determine if compression is appropriate

**Result**: Claude correctly understood all metadata and made appropriate recommendations.

## Issues Found
[Any issues or edge cases discovered]

## Recommendations
[Suggestions for improvements]

## Success Criteria Met
- ✓ Headers added to 5+ documents
- ✓ Claude can parse and understand headers
- ✓ Metadata provides needed information
- ✓ Format is maintainable

**Overall Status**: PASS
```

---

## Validation Report Template

```markdown
# Validation Report: Document Header Specification (Task 3.2)

**Date**: [YYYY-MM-DD]
**Task**: TASK-3.2-HEADER-SPECIFICATION
**Status**: [PASS/FAIL]

## Summary

Created comprehensive YAML header specification for project documentation
with 10+ document type examples, validation test suite, and real-world
application to project files.

## Deliverables

1. ✓ `/docs/reference/DOCUMENT_HEADER_SPECIFICATION.md` ([X] lines)
2. ✓ `tests/test_header_validation.py` (validation suite)
3. ✓ `tests/fixtures/headers/*.md` (10+ examples)
4. ✓ Headers applied to 5+ project documents
5. ✓ Three checkpoint reports

## Test Results

### Validation Suite
```bash
pytest tests/test_header_validation.py -v
```

**Results**: [X/X] tests passing

- ✓ All examples parse as valid YAML
- ✓ Required fields present in all examples
- ✓ target_style structure correct (σ, γ, κ)
- ✓ Compression tracking complete where applicable
- ✓ DateTime formats valid
- ✓ doc_type enum values correct

### Real-World Application

| Document | Header Added | Claude Parse | Metadata Useful |
|----------|-------------|--------------|-----------------|
| SESSION.md | ✓ | ✓ | ✓ |
| PROJECT.md | ✓ | ✓ | ✓ |
| Task specs | ✓ | ✓ | ✓ |
| Validation reports | ✓ | ✓ | ✓ |
| Plan documents | ✓ | ✓ | ✓ |

**Success Rate**: 100% (5/5 documents)

## Specification Quality

### Completeness
- ✓ All required fields documented
- ✓ 10+ document type examples
- ✓ Clear field definitions
- ✓ Validation rules specified
- ✓ Usage patterns explained

### Usability
- ✓ Quick start guide (3 minutes to first header)
- ✓ Easy to scan (headers, lists, tables)
- ✓ Machine-readable (valid YAML)
- ✓ Human-readable (clear explanations)
- ✓ Comprehensive reference

### Maintainability
- ✓ Examples can be copy/pasted
- ✓ Format is consistent
- ✓ Clear field purpose explanations
- ✓ Validation tests catch errors

## Claude Comprehension

Tested Claude's ability to parse and use headers:

**Test 1**: Parse SESSION.md header
- ✓ Correctly identified doc_type: SESSION_HANDOVER
- ✓ Understood target_style: {σ: 0.7, γ: 0.7, κ: 0.3}
- ✓ Recognized compression state

**Test 2**: Recommend compression
- ✓ Used header metadata to assess compression need
- ✓ Made appropriate recommendation
- ✓ Respected current compression state

**Test 3**: Write new section
- ✓ Maintained style consistent with target_style
- ✓ Used appropriate (σ, γ, κ) parameters

## Edge Cases

### Handled Successfully
- Documents without compression tracking
- Optional fields (writing_guide)
- Various audience types
- Mixed document types

### Potential Issues
[Document any edge cases that need attention]

## Recommendations

### Immediate
- [Any urgent fixes needed]

### Future Enhancements
- Add more document type examples as needed
- Consider tool to auto-generate headers
- Track header usage statistics

## Success Criteria Met

### Must Pass (Critical)
- ✓ Headers are clear and unambiguous
- ✓ All necessary metadata included
- ✓ Easy to write and maintain
- ✓ Machine-readable and human-readable
- ✓ Claude can parse and understand

### Should Pass (Important)
- ✓ 10+ document type examples
- ✓ Validation test suite
- ✓ Works on real project docs
- ✓ Format is maintainable

### Nice to Have (Optional)
- ✓ Migration guide for existing docs
- ✓ Usage patterns documented
- ✓ Quick start guide

**Overall Status**: PASS

## Conclusions

Document header specification successfully created and validated. Headers
provide structured metadata enabling intelligent tool decisions about
compression without reading full documents. Format is maintainable, examples
are comprehensive, and Claude demonstrates excellent comprehension.

Ready for integration into compression automation tool.
```

---

## Success Criteria

### Must Pass (Critical)
- ✓ Specification is clear and unambiguous
- ✓ All required fields documented with examples
- ✓ YAML format is valid and parseable
- ✓ Claude can parse and understand headers
- ✓ Headers provide sufficient metadata for tool decisions

### Should Pass (Important)
- ✓ 10+ document type examples provided
- ✓ Validation test suite passes
- ✓ Applied successfully to real project documents
- ✓ Format is easy to maintain

### Nice to Have (Optional)
- Quick start guide (under 3 minutes)
- Migration guide for existing documents
- Usage pattern documentation
- Visual examples

---

## Final Deliverables

1. **Main Specification**: `docs/reference/DOCUMENT_HEADER_SPECIFICATION.md`
   - Complete field reference
   - 10+ document type examples
   - Validation rules
   - Usage patterns
   - Quick start guide
   - Migration guide

2. **Validation Suite**: `tests/test_header_validation.py`
   - YAML parsing validation
   - Required fields checking
   - Field value validation
   - Parameter range checking
   - DateTime format validation

3. **Example Headers**: `tests/fixtures/headers/`
   - api_reference_compressed.md
   - tutorial_uncompressed.md
   - session_handover_compressed.md
   - project_context_compressed.md
   - task_specification.md
   - validation_report.md
   - analysis_compressed.md
   - research_uncompressed.md
   - plan_document.md
   - reference_compressed.md

4. **Checkpoint Reports**:
   - `checkpoints/checkpoint_1_header_tests.md`
   - `checkpoints/checkpoint_2_header_spec.md`
   - `checkpoints/checkpoint_3_header_applied.md`

5. **Validation Report**: `validation_report_task_3.2.md`

6. **Real Document Updates**: Headers added to 5+ project documents
   - SESSION.md
   - PROJECT.md
   - Task specifications
   - Validation reports
   - Plan documents

---

## Task Dependencies

### Prerequisites
- None (independent task)
- Does not require any previous validation tasks

### Enables
- Task 2.3: Safety checks (header parsing for validation)
- Full tool: Document classification and compression decisions
- User workflow: Quick document type identification

### Proves
- Headers provide sufficient metadata
- Format is maintainable
- Claude can parse and use headers effectively

---

## Notes

### Design Decisions

**Why YAML frontmatter?**
- Standard markdown convention
- Machine-readable and human-readable
- Parseable by most markdown tools
- Easy to validate programmatically

**Why these specific fields?**
- `doc_type`: Essential for compression strategy selection
- `audience`: Determines appropriate (γ, κ) parameters
- `layer`: Guides compression aggressiveness
- `phase`: Enables lifecycle-based compression
- `target_style`: Direct (σ, γ, κ) specification
- `compression`: Tracks state and enables drift detection

**Why separate writing_guide?**
- Optional (not all docs need it)
- Provides context-specific advice
- Reduces ambiguity in edge cases
- Helps maintain consistency

### Open Questions

**Should headers be required?**
- Initially: Optional (allow gradual adoption)
- Eventually: Required for compressed documents
- Tool can work without headers (just less intelligent)

**Should we auto-generate headers?**
- Possible future enhancement
- Tool could suggest headers based on content analysis
- Manual review still recommended

**Should headers track compression history?**
- Current spec: Only last compression
- Future: Could track full history
- Trade-off: More metadata vs. header bloat

### Future Enhancements

**Header Generation Tool**
- Analyze document content
- Suggest appropriate doc_type
- Calculate current (σ, γ, κ) parameters
- Generate complete header

**Header Validation Tool**
- Check all project documents have headers
- Validate header consistency
- Flag outdated compression tracking

**Migration Assistant**
- Batch add headers to existing documents
- Interactive header builder
- Header template generator

**Analytics Dashboard**
- Document type distribution
- Compression coverage
- Style parameter trends
- Drift detection summary

---

## Specification Outline

The main deliverable (`docs/reference/DOCUMENT_HEADER_SPECIFICATION.md`) should include:

### 1. Overview (1-2 pages)
- Purpose and benefits
- When to use headers
- Quick start guide

### 2. Field Reference (3-4 pages)
- Complete field definitions
- Required vs. optional
- Valid values and formats
- Parameter meanings

### 3. Document Type Guide (5-6 pages)
- 10+ complete examples
- Each with full header
- Explanation of choices
- Compression guidance

### 4. Validation Rules (1-2 pages)
- What makes a valid header
- Common mistakes
- Validation test suite

### 5. Usage Patterns (2-3 pages)
- Common scenarios
- How to choose doc_type
- When to add compression tracking
- How to update headers

### 6. Migration Guide (1-2 pages)
- Adding headers to existing docs
- Batch update strategy
- Testing headers

### 7. Examples Library (2-3 pages)
- Copy-paste templates
- Edge case examples
- Multi-role documents

**Total**: ~15-20 pages of comprehensive documentation

---

## Working Directory

**Base**: `/Users/dudley/Projects/Compression`

**Key Paths**:
- Specification: `docs/reference/DOCUMENT_HEADER_SPECIFICATION.md`
- Tests: `tests/test_header_validation.py`
- Fixtures: `tests/fixtures/headers/`
- Checkpoints: `checkpoints/checkpoint_*_header_*.md`
- Report: `validation_report_task_3.2.md`

---

## Estimated Timeline

### Checkpoint 1: Test Suite (30-45 minutes)
- Create validation test suite
- Write 10+ example headers
- Verify tests run

### Checkpoint 2: Specification (60-90 minutes)
- Write comprehensive specification document
- Ensure all examples pass tests
- Document validation rules

### Checkpoint 3: Real-World Application (30-45 minutes)
- Add headers to 5+ project documents
- Test Claude comprehension
- Document findings

**Total**: 2-3 hours (consistent with estimate)

---

## Integration with Other Tasks

### Task 1.1 (Content Analyzer)
- Will use headers to skip analysis for known-compressed docs
- Can extract target_style from headers
- Uses compression tracking for drift detection

### Task 2.3 (Safety Checks)
- Parses headers to understand compression state
- Uses baseline_tokens for drift calculation
- Validates against target_style parameters

### Full Tool
- Headers enable intelligent compression decisions
- Reduce need for full document analysis
- Provide metadata for reporting and analytics

---

## Success Measures

### Quantitative
- ✓ 10+ document type examples created
- ✓ 100% validation test pass rate
- ✓ 5+ real documents with headers
- ✓ 0 parsing errors in headers

### Qualitative
- ✓ Specification is clear to humans
- ✓ Headers are easy to write
- ✓ Claude understands headers correctly
- ✓ Format is maintainable long-term

### Adoption
- ✓ Team members can add headers without help
- ✓ Headers become standard practice
- ✓ Tool provides value through header usage

---

**Created**: 2025-10-30  
**Dependencies**: None (independent task)  
**Enables**: Task 2.3, Full compression tool  
**Estimated Effort**: 2-3 hours with TDD + checkpoints