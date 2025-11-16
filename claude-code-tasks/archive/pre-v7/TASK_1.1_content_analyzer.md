# Claude Code Task: Content Density Analyzer (Task 1.1)

**Task ID**: TASK-1.1-CONTENT-ANALYZER  
**Priority**: HIGH  
**Estimated Time**: 4-6 hours  
**Approach**: TDD with checkpoint system  
**Dependencies**: TASK-2.1 (compression score) + TASK-1.2 (token drift)

---

## Project Context

This is part of a compression research project evaluating methods for AI context optimization. We've developed a unified theory where all compression techniques optimize three parameters (σ, γ, κ) subject to comprehension constraints.

**Current Phase**: Validation - testing critical design assumptions before building the full automation tool.

**This Task's Role**: Detect and handle documents with **mixed compression states** - where some sections are compressed and others are not. This happens when documents are partially compressed or when new content is added after compression.

---

## Objective

Build a content density analyzer that:
1. Splits documents into sections (H1, H2, H3 boundaries)
2. Scores each section using the compression score algorithm
3. Classifies overall document state (uncompressed, compressed, mixed)
4. Identifies which specific sections need compression
5. Integrates with token drift detection for comprehensive analysis

**Core Problem**: Document written → compressed → new section added → header says "compressed" but document has mixed state.

**Solution**: Section-level analysis combined with token drift metrics.

---

## TDD Approach

### Phase 1: Write Tests First (Checkpoint 1)
1. Create test documents with known section states
2. Define expected section scores and classifications
3. Write failing tests
4. **Checkpoint**: All tests FAIL (no implementation)

### Phase 2: Implement Section Analysis (Checkpoint 2)
1. Implement section splitting logic
2. Apply compression score per section
3. Implement state classification
4. Make tests pass
5. **Checkpoint**: All tests PASS

### Phase 3: Validate Real Documents (Checkpoint 3)
1. Test on actual project documentation
2. Validate section boundary detection
3. Verify state classification accuracy
4. **Checkpoint**: Works on real docs

---

## Checkpoint System

### Checkpoint 1: Tests Written ✓
**Deliverable**: `tests/test_content_analyzer.py` (tests fail)  
**Validation**:
```bash
pytest tests/test_content_analyzer.py
# Expected: All tests FAIL
```
**Output**: `checkpoints/checkpoint_1_analyzer_tests.md`

### Checkpoint 2: Implementation Works ✓
**Deliverable**: `scripts/analyze_compression_state.py`  
**Validation**:
```bash
pytest tests/test_content_analyzer.py
# Expected: All tests PASS
```
**Output**: `checkpoints/checkpoint_2_analyzer_impl.md`

### Checkpoint 3: Real-World Validation ✓
**Deliverable**: `validation_report_task_1.1.md`  
**Validation**: Works accurately on project docs  
**Output**: `checkpoints/checkpoint_3_analyzer_validated.md`

---

## Technical Specifications

### Core Functions

```python
from scripts.compression_score import CompressionScorer
from scripts.detect_token_drift import check_token_drift

class ContentAnalyzer:
    """
    Analyze document compression state at section level.
    """
    
    def __init__(self, scorer: CompressionScorer):
        self.scorer = scorer
        
    def split_into_sections(self, document: str) -> list:
        """
        Split markdown document into sections based on headers.
        
        Returns:
            [
                {
                    "title": "Section Name",
                    "level": 1,  # H1, H2, or H3
                    "content": "section text...",
                    "start_line": 10,
                    "end_line": 25
                },
                ...
            ]
        """
        pass
    
    def analyze_section(self, section_content: str) -> dict:
        """
        Analyze a single section's compression state.
        
        Returns:
            {
                "score": 0.65,
                "state": "moderately_compressed",  # verbose|moderate|compressed|highly_compressed
                "metrics": {...},  # from compression_score
                "needs_compression": False
            }
        """
        pass
    
    def analyze_document(self, document: str, header_metadata: dict = None) -> dict:
        """
        Complete document analysis with section-level detail.
        
        Args:
            document: Full document text
            header_metadata: Optional YAML header data (for token drift)
        
        Returns:
            {
                "overall_state": "mixed",  # uncompressed|compressed|mixed|edited
                "sections": [
                    {
                        "title": "Introduction",
                        "score": 0.25,
                        "state": "verbose",
                        "needs_compression": True
                    },
                    {
                        "title": "API Reference",
                        "score": 0.82,
                        "state": "highly_compressed",
                        "needs_compression": False
                    }
                ],
                "summary": {
                    "total_sections": 2,
                    "compressed_sections": 1,
                    "uncompressed_sections": 1,
                    "avg_score": 0.54
                },
                "token_drift": {...},  # from detect_token_drift if header provided
                "recommendation": "compress_sections: [0]"  # actionable guidance
            }
        """
        pass
    
    def classify_state(self, section_scores: list) -> str:
        """
        Classify overall document state based on section scores.
        
        Logic:
        - All sections < 0.4: "uncompressed"
        - All sections > 0.7: "compressed"
        - Mixed scores: "mixed"
        - With token drift: "edited"
        """
        pass
```

### Section Boundary Detection

**Rules**:
1. Split on H1 (`# Header`) → Top-level sections
2. Split on H2 (`## Header`) → Subsections
3. Split on H3 (`### Header`) → Sub-subsections
4. Minimum section length: 100 tokens (skip tiny sections)
5. Maximum depth: H3 (ignore H4+)

**Example**:
```markdown
# Introduction
Some intro text here.

## Getting Started
Setup instructions.

## API Reference
API documentation.

### Authentication
Auth details.

### Endpoints
Endpoint list.
```

**Sections**:
1. "Introduction" (H1, lines 1-3)
2. "Getting Started" (H2, lines 5-6)
3. "API Reference > Authentication" (H3, lines 10-11)
4. "API Reference > Endpoints" (H3, lines 13-14)

---

## Test Cases

### Test Case 1: Fully Uncompressed Document

```markdown
# User Guide

## Introduction

This comprehensive guide walks you through everything you need to know about
using our API. We've designed this guide to be accessible to developers of
all experience levels, so whether you're just getting started or you're an
experienced developer, you'll find valuable information here.

## Authentication

Authentication is an important part of using our API. When you want to make
requests to the API, you'll need to authenticate yourself first. This is done
through a token-based authentication system that we've implemented to provide
security while maintaining ease of use.

The authentication process works as follows...
```

**Expected**:
- All sections score < 0.3
- Overall state: "uncompressed"
- Recommendation: "compress_all"

---

### Test Case 2: Fully Compressed Document

```markdown
# API Reference

## POST /auth
- Body: `{username, password}`
- Returns: `{token}` (200) | `{error}` (401)

## GET /users
- Auth: Bearer token
- Returns: User array
- Filters: `?role=admin&status=active`

## PUT /users/:id
- Auth: Bearer + admin
- Body: User update
- Returns: Updated (200) | 403/404
```

**Expected**:
- All sections score > 0.7
- Overall state: "compressed"
- Recommendation: "none"

---

### Test Case 3: Mixed State Document

```markdown
# API Documentation

## Authentication (COMPRESSED)
- Endpoint: `/auth`
- Method: POST
- Body: `{username, password}`
- Returns: `{token}` or error

## New Feature - Rate Limiting (VERBOSE)

We've recently added rate limiting to the API to ensure fair usage across
all clients. Rate limiting helps prevent abuse and ensures that the API
remains responsive for everyone.

The rate limiting system works by tracking the number of requests made by
each authenticated user within a time window. If you exceed the limit,
you'll receive a 429 status code and will need to wait before making
additional requests.

Here's how to work with rate limits...
```

**Expected**:
- Section 1 score: 0.82 (compressed)
- Section 2 score: 0.25 (verbose)
- Overall state: "mixed"
- Recommendation: "compress_sections: [1]"

---

### Test Case 4: Document with Token Drift

```markdown
---
compression:
  last_full_compression: 2025-10-30 10:00 AEDT
  baseline_tokens: 1000
  parameters: {σ: 0.8, γ: 0.6, κ: 0.2}
---

# API Reference

## POST /auth
[compressed content - 400 tokens]

## GET /users  
[compressed content - 400 tokens]

## NEW SECTION - Webhooks
[verbose new content - 300 tokens]
```

**Expected**:
- Current tokens: 1100 (drift ratio: 1.10)
- Sections 1-2: compressed (score > 0.7)
- Section 3: uncompressed (score < 0.3)
- Overall state: "edited" (compressed + drifted)
- Recommendation: "compress_sections: [2], update_baseline"

---

## Implementation Guidelines

### Required Libraries
```bash
# From previous tasks
# - tiktoken (token counting)
# - markdown-it-py (markdown parsing)

# Additional for this task
pip install pyyaml --break-system-packages  # for YAML header parsing
```

### Markdown Section Parsing

```python
import re
from markdown_it import MarkdownIt

def split_into_sections(document):
    """
    Split markdown by headers (H1, H2, H3).
    """
    # Parse markdown
    md = MarkdownIt()
    tokens = md.parse(document)
    
    sections = []
    current_section = None
    
    for token in tokens:
        if token.type == 'heading_open':
            level = int(token.tag[1])  # h1 → 1, h2 → 2, etc.
            if level <= 3:  # Only H1, H2, H3
                if current_section:
                    sections.append(current_section)
                current_section = {
                    "level": level,
                    "title": "",
                    "content": ""
                }
        elif token.type == 'inline' and current_section:
            current_section["title"] = token.content
        elif current_section:
            current_section["content"] += token.content or ""
    
    if current_section:
        sections.append(current_section)
    
    return sections
```

### Alternative: Regex-Based Splitting

```python
def split_by_headers_regex(text):
    """
    Simpler approach: split by header patterns.
    """
    # Split on headers, keeping the header
    sections = []
    pattern = r'^(#{1,3})\s+(.+)$'
    
    current_level = 0
    current_title = ""
    current_content = []
    
    for line in text.split('\n'):
        match = re.match(pattern, line)
        if match:
            # Save previous section
            if current_title:
                sections.append({
                    "level": current_level,
                    "title": current_title,
                    "content": '\n'.join(current_content)
                })
            
            # Start new section
            current_level = len(match.group(1))  # count #'s
            current_title = match.group(2)
            current_content = []
        else:
            current_content.append(line)
    
    # Save last section
    if current_title:
        sections.append({
            "level": current_level,
            "title": current_title,
            "content": '\n'.join(current_content)
        })
    
    return sections
```

---

## State Classification Logic

```python
def classify_state(section_scores, token_drift_ratio=None):
    """
    Determine overall document state.
    """
    if not section_scores:
        return "empty"
    
    # Check for token drift first
    if token_drift_ratio and token_drift_ratio > 1.15:
        # Document has grown significantly
        if any(score < 0.4 for score in section_scores):
            return "edited"  # Has drift + uncompressed sections
    
    # Check section score distribution
    compressed_count = sum(1 for s in section_scores if s > 0.7)
    uncompressed_count = sum(1 for s in section_scores if s < 0.4)
    total = len(section_scores)
    
    if compressed_count == total:
        return "compressed"
    elif uncompressed_count == total:
        return "uncompressed"
    elif compressed_count > 0 and uncompressed_count > 0:
        return "mixed"
    else:
        return "moderately_compressed"
```

---

## Project Structure

```
/Users/dudley/Projects/Compression/
├── scripts/
│   ├── compression_score.py         # From Task 2.1
│   ├── detect_token_drift.py        # From Task 1.2
│   └── analyze_compression_state.py # New: section analysis
├── tests/
│   ├── test_content_analyzer.py     # New: test suite
│   └── fixtures/
│       ├── fully_uncompressed.md
│       ├── fully_compressed.md
│       ├── mixed_state.md
│       └── with_token_drift.md
├── checkpoints/
│   ├── checkpoint_1_analyzer_tests.md
│   ├── checkpoint_2_analyzer_impl.md
│   └── checkpoint_3_analyzer_validated.md
└── validation_report_task_1.1.md
```

---

## Test Template

```python
import pytest
from scripts.compression_score import CompressionScorer
from scripts.analyze_compression_state import ContentAnalyzer

class TestContentAnalyzer:
    """Test suite for section-level compression analysis."""
    
    @pytest.fixture
    def scorer(self):
        return CompressionScorer()
    
    @pytest.fixture
    def analyzer(self, scorer):
        return ContentAnalyzer(scorer)
    
    def test_split_sections(self, analyzer):
        """Test document splitting into sections."""
        pass
    
    def test_fully_uncompressed(self, analyzer):
        """All sections verbose → overall state uncompressed."""
        pass
    
    def test_fully_compressed(self, analyzer):
        """All sections compressed → overall state compressed."""
        pass
    
    def test_mixed_state(self, analyzer):
        """Some compressed, some not → overall state mixed."""
        pass
    
    def test_with_token_drift(self, analyzer):
        """Compressed doc with growth → state edited."""
        pass
    
    def test_section_recommendations(self, analyzer):
        """Verify actionable recommendations for which sections to compress."""
        pass
    
    def test_minimum_section_length(self, analyzer):
        """Tiny sections (< 100 tokens) are skipped."""
        pass
    
    def test_real_project_docs(self, analyzer):
        """Validate on actual Compression project documentation."""
        # Test on SESSION.md, PROJECT.md, etc.
        pass
```

---

## Validation Report Template

```markdown
# Validation Report: Content Density Analyzer (Task 1.1)

**Date**: [YYYY-MM-DD]
**Task**: TASK-1.1-CONTENT-ANALYZER
**Status**: [PASS/FAIL]

## Summary

[Overview of validation results]

## Test Results

### Section Splitting
- ✓/✗ Correctly identifies H1, H2, H3 boundaries
- ✓/✗ Handles nested sections appropriately
- ✓/✗ Skips sections below 100 token minimum
- ✓/✗ Works with various markdown styles

### State Classification
- ✓/✗ Fully uncompressed documents → "uncompressed"
- ✓/✗ Fully compressed documents → "compressed"
- ✓/✗ Mixed documents → "mixed"
- ✓/✗ Docs with drift → "edited"

### Section-Level Analysis

| Document Type | Sections | Compressed | Uncompressed | State | Recommendation |
|--------------|----------|------------|--------------|-------|----------------|
| Fully Verbose | 3 | 0 | 3 | uncompressed | compress_all |
| Fully Compressed | 4 | 4 | 0 | compressed | none |
| Mixed State | 5 | 2 | 3 | mixed | compress_sections: [1,3,4] |
| With Drift | 3 | 2 | 1 | edited | compress_sections: [2], update |

### Real-World Testing

Tested on actual project documentation:

- `SESSION.md`: [result]
- `PROJECT.md`: [result]
- `docs/plans/AUTOMATION_TOOL_VALIDATION_PLAN.md`: [result]

**Accuracy**: [X/X] documents correctly analyzed

## Edge Cases

[Document any interesting edge cases]

## Performance

- Average analysis time: [X] seconds per document
- Section parsing: [X] ms per section
- Memory usage: [X] MB for large documents

## Conclusions

- [x] Section splitting works reliably
- [x] State classification is accurate
- [x] Recommendations are actionable
- [x] Integrates well with compression_score and token_drift

## Recommendations

[Suggestions for improvements, threshold tuning, etc.]

## Success Criteria Met

- [x] Can distinguish compressed vs uncompressed sections
- [x] Scores correlate with manual assessment
- [x] Can identify specific sections needing compression
- [x] Works on real project documentation

**Overall Status**: PASS
```

---

## Success Criteria

### Must Pass (Critical)
- ✓ Section splitting works correctly
- ✓ State classification matches expectations for all test cases
- ✓ Identifies which sections need compression
- ✓ Integration with compression_score and token_drift works

### Should Pass (Important)
- ✓ Handles edge cases (empty sections, nested headers)
- ✓ Works on real project documentation
- ✓ Recommendations are actionable

### Nice to Have (Optional)
- Performance metrics
- Visual output formatting
- Export to JSON/CSV for analysis

---

## Final Deliverables

1. `scripts/analyze_compression_state.py` - Content analyzer implementation
2. `tests/test_content_analyzer.py` - Complete test suite
3. `tests/fixtures/` - Test documents (4+ examples)
4. `checkpoints/checkpoint_1_analyzer_tests.md`
5. `checkpoints/checkpoint_2_analyzer_impl.md`
6. `checkpoints/checkpoint_3_analyzer_validated.md`
7. `validation_report_task_1.1.md` - Final validation report

---

## Sequential Task Dependencies

**This task requires**:
- TASK-2.1: compression_score.py (for section scoring)
- TASK-1.2: detect_token_drift.py (for drift analysis)

**This task enables**:
- TASK-2.3: Safety checks (uses mixed state detection)
- Full tool: Intelligent section-level compression
- User workflow: "Which sections need compression?"

**This proves**:
- Mixed state detection works
- Section-level analysis is practical
- Tool can handle partially compressed documents

---

## Notes

### Design Decisions
- H1/H2/H3 only (ignore H4+) for manageable granularity
- 100 token minimum prevents tiny section noise
- State classification uses clear thresholds (0.4 and 0.7)

### Open Questions
- Should section boundaries be configurable?
- Do we need H4+ support for very detailed docs?
- Should tiny sections be merged with parent?

### Future Enhancements
- Visual diff showing compressed vs uncompressed sections
- Batch analysis of multiple documents
- Historical tracking of compression state over time

---

**Working Directory**: /Users/dudley/Projects/Compression  
**Created**: 2025-10-30  
**Depends on**: Task 2.1 + Task 1.2 completion
