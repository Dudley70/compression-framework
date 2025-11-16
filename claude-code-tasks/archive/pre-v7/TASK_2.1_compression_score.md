# Claude Code Task: Compression Score Algorithm (Task 2.1)

**Task ID**: TASK-2.1-COMPRESSION-SCORE  
**Priority**: CRITICAL (MVP requirement)  
**Estimated Time**: 4-8 hours  
**Approach**: TDD with checkpoint system  

---

## Project Context

This is part of a compression research project evaluating methods for AI context optimization. We've developed a unified theory where all compression techniques optimize three parameters (σ, γ, κ) subject to comprehension constraints.

**Current Phase**: Validation - testing critical design assumptions before building the full automation tool.

**This Task's Role**: Build the foundation algorithm that detects whether content is already compressed, preventing information loss through repeated compression (idempotency protection).

---

## Objective

Build a compression score algorithm that measures how compressed text already is on a 0.0-1.0 scale, where:
- **0.0-0.3**: Verbose, uncompressed (safe to compress)
- **0.4-0.6**: Moderately compressed
- **0.7-0.9**: Highly compressed (refuse further compression)
- **0.9-1.0**: Maximally compressed

---

## TDD Approach

### Phase 1: Write Tests First (Checkpoint 1)
1. Create test documents with known characteristics
2. Define expected score ranges
3. Write failing tests
4. **Checkpoint**: All tests fail as expected (no implementation yet)

### Phase 2: Implement Core Algorithm (Checkpoint 2)
1. Implement basic scoring metrics
2. Make tests pass
3. **Checkpoint**: All tests pass with basic implementation

### Phase 3: Refine & Validate (Checkpoint 3)
1. Add edge cases
2. Tune metric weights
3. Validate score accuracy
4. **Checkpoint**: Scores match manual assessment

---

## Checkpoint System

### Checkpoint 1: Test Suite Complete ✓
**Deliverable**: `tests/test_compression_score.py`  
**Validation**:
```bash
pytest tests/test_compression_score.py
# Expected: All tests FAIL (no implementation)
```
**Output**: `checkpoints/checkpoint_1_tests_written.md` documenting test cases

### Checkpoint 2: Basic Implementation ✓
**Deliverable**: `scripts/compression_score.py`  
**Validation**:
```bash
pytest tests/test_compression_score.py
# Expected: All tests PASS
```
**Output**: `checkpoints/checkpoint_2_basic_impl.md` with test results

### Checkpoint 3: Validation Complete ✓
**Deliverable**: `validation_report_task_2.1.md`  
**Validation**: Scores correlate with manual assessment  
**Output**: `checkpoints/checkpoint_3_validated.md` with full analysis

---

## Technical Specifications

### Algorithm Requirements

Implement `calculate_compression_score(text: str) -> dict`:

**Return Structure**:
```python
{
    "overall_score": 0.65,  # 0.0-1.0
    "metrics": {
        "list_density": 0.45,        # ratio of list items to total tokens
        "prose_ratio": 0.30,          # ratio of paragraph tokens to total
        "avg_sentence_length": 12.5,  # words per sentence (lower = more compressed)
        "redundancy": 0.15,           # repeated phrase detection
        "explanation_markers": 3,     # count of scaffolding phrases
        "information_entropy": 4.2    # Shannon entropy
    },
    "interpretation": "moderately_compressed",  # verbose|moderate|compressed|highly_compressed
    "safe_to_compress": true  # false if score >= 0.8
}
```

### Metric Calculations

#### 1. List Density (weight: 0.25)
```python
list_tokens = count_tokens_in_lists_and_tables(text)
total_tokens = count_total_tokens(text)
list_density = list_tokens / total_tokens
```

#### 2. Prose Ratio (weight: 0.20)
```python
prose_tokens = count_tokens_in_paragraphs(text)
prose_ratio = prose_tokens / total_tokens
# Lower prose_ratio = more compressed
# Score contribution: 1 - prose_ratio
```

#### 3. Average Sentence Length (weight: 0.20)
```python
sentences = split_into_sentences(text)
avg_length = mean([count_words(s) for s in sentences])
# Normalize: 5 words = 1.0, 20 words = 0.0
normalized = max(0, (20 - avg_length) / 15)
```

#### 4. Redundancy (weight: 0.15)
```python
# Find repeated phrases (3+ words)
phrases = extract_phrases(text, min_length=3)
repetitions = count_repetitions(phrases)
redundancy_score = 1 - (repetitions / len(phrases))
```

#### 5. Explanation Markers (weight: 0.10)
```python
markers = [
    "this means", "in other words", "for example",
    "to illustrate", "that is to say", "specifically"
]
marker_count = count_occurrences(text, markers)
# Normalize by document length (per 1000 tokens)
normalized = max(0, 1 - (marker_count / (total_tokens / 1000) / 5))
```

#### 6. Information Entropy (weight: 0.10)
```python
# Shannon entropy of token distribution
tokens = tokenize(text)
entropy = calculate_shannon_entropy(tokens)
# Normalize: higher entropy = more compressed
# Typical range: 3.0-6.0, normalize to 0-1
normalized = (entropy - 3.0) / 3.0
```

### Overall Score Calculation
```python
overall_score = (
    list_density * 0.25 +
    (1 - prose_ratio) * 0.20 +
    avg_sentence_normalized * 0.20 +
    redundancy_score * 0.15 +
    explanation_marker_score * 0.10 +
    entropy_normalized * 0.10
)
```

---

## Test Cases (Phase 1)

### Test Document 1: Verbose Technical Doc
**Expected Score**: 0.2-0.3

```markdown
# API Authentication

The authentication endpoint is available at the /auth path and accepts POST requests. 
When you want to authenticate a user, you need to send a JSON body that contains 
both a username field and a password field. The API will validate these credentials 
against the database and return a token if the authentication is successful.

For example, if you wanted to authenticate a user named "john" with password "secret123",
you would send a POST request to /auth with the following JSON body:

{
  "username": "john",
  "password": "secret123"
}

The server will then check if these credentials are valid. In other words, it will
query the database to see if there's a user with that username and if the password
matches. If everything checks out, meaning the credentials are correct, the API
will respond with a JSON object containing an access token that you can use for
subsequent authenticated requests.
```

**Expected Metrics**:
- list_density: ~0.05 (very few lists)
- prose_ratio: ~0.90 (mostly prose)
- avg_sentence_length: ~25 words
- redundancy: ~0.3 (repeated explanations)
- explanation_markers: ~6 markers
- entropy: ~3.5 (lower)

---

### Test Document 2: Moderately Compressed Doc
**Expected Score**: 0.5-0.6

```markdown
# API Authentication

## POST /auth

Authenticates user credentials and returns access token.

**Request**:
- Endpoint: `/auth`
- Method: POST
- Body: `{username: string, password: string}`

**Response**:
- Success (200): `{token: string}`
- Failure (401): `{error: string}`

**Example**:
```json
POST /auth
{
  "username": "john",
  "password": "secret123"
}
```

Returns token for authenticated requests.
```

**Expected Metrics**:
- list_density: ~0.40
- prose_ratio: ~0.35
- avg_sentence_length: ~12 words
- redundancy: ~0.75
- explanation_markers: ~1
- entropy: ~4.5

---

### Test Document 3: Highly Compressed Doc
**Expected Score**: 0.8-0.9

```markdown
## POST /auth
- Body: `{username, password}`
- Returns: `{token}` (200) | `{error}` (401)
- Auth: None required

## GET /users
- Auth: Bearer token
- Returns: User array
- Filters: `?role=admin&status=active`

## PUT /users/:id
- Auth: Bearer + admin role
- Body: User update object
- Returns: Updated user (200) | 403/404
```

**Expected Metrics**:
- list_density: ~0.85
- prose_ratio: ~0.05
- avg_sentence_length: ~6 words
- redundancy: ~0.95
- explanation_markers: 0
- entropy: ~5.2

---

## Implementation Guidelines

### Required Python Libraries
```bash
pip install tiktoken markdown-it-py nltk numpy --break-system-packages
```

### Project Structure
```
/Users/dudley/Projects/Compression/
├── scripts/
│   └── compression_score.py          # Main implementation
├── tests/
│   ├── test_compression_score.py     # Test suite
│   └── fixtures/
│       ├── verbose_doc.md            # Test document 1
│       ├── moderate_doc.md           # Test document 2
│       └── compressed_doc.md         # Test document 3
├── checkpoints/
│   ├── checkpoint_1_tests_written.md
│   ├── checkpoint_2_basic_impl.md
│   └── checkpoint_3_validated.md
└── validation_report_task_2.1.md     # Final deliverable
```

### Code Structure Template

```python
# scripts/compression_score.py
import tiktoken
from markdown_it import MarkdownIt
import nltk
import numpy as np
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class CompressionMetrics:
    list_density: float
    prose_ratio: float
    avg_sentence_length: float
    redundancy: float
    explanation_markers: int
    information_entropy: float

class CompressionScorer:
    def __init__(self):
        self.encoding = tiktoken.get_encoding("cl100k_base")
        self.md_parser = MarkdownIt()
        # Download required NLTK data
        nltk.download('punkt', quiet=True)
    
    def calculate_score(self, text: str) -> Dict:
        """Main entry point for scoring."""
        metrics = self._calculate_metrics(text)
        overall_score = self._compute_overall_score(metrics)
        
        return {
            "overall_score": overall_score,
            "metrics": {
                "list_density": metrics.list_density,
                "prose_ratio": metrics.prose_ratio,
                "avg_sentence_length": metrics.avg_sentence_length,
                "redundancy": metrics.redundancy,
                "explanation_markers": metrics.explanation_markers,
                "information_entropy": metrics.information_entropy
            },
            "interpretation": self._interpret_score(overall_score),
            "safe_to_compress": overall_score < 0.8
        }
    
    def _calculate_metrics(self, text: str) -> CompressionMetrics:
        """Calculate all individual metrics."""
        # TODO: Implement each metric calculation
        pass
    
    def _compute_overall_score(self, metrics: CompressionMetrics) -> float:
        """Weighted combination of metrics."""
        # TODO: Implement weighted scoring
        pass
    
    def _interpret_score(self, score: float) -> str:
        """Convert score to interpretation."""
        if score < 0.3:
            return "verbose"
        elif score < 0.6:
            return "moderately_compressed"
        elif score < 0.8:
            return "compressed"
        else:
            return "highly_compressed"
```

---

## Test Template

```python
# tests/test_compression_score.py
import pytest
from pathlib import Path
from scripts.compression_score import CompressionScorer

@pytest.fixture
def scorer():
    return CompressionScorer()

@pytest.fixture
def test_docs_dir():
    return Path(__file__).parent / "fixtures"

class TestCompressionScore:
    
    def test_verbose_document_scores_low(self, scorer, test_docs_dir):
        """Verbose document should score 0.2-0.3."""
        text = (test_docs_dir / "verbose_doc.md").read_text()
        result = scorer.calculate_score(text)
        
        assert 0.2 <= result["overall_score"] <= 0.3, \
            f"Expected 0.2-0.3, got {result['overall_score']}"
        assert result["safe_to_compress"] is True
        assert result["interpretation"] == "verbose"
    
    def test_moderate_document_scores_medium(self, scorer, test_docs_dir):
        """Moderately compressed should score 0.5-0.6."""
        text = (test_docs_dir / "moderate_doc.md").read_text()
        result = scorer.calculate_score(text)
        
        assert 0.5 <= result["overall_score"] <= 0.6
        assert result["safe_to_compress"] is True
        assert result["interpretation"] == "moderately_compressed"
    
    def test_compressed_document_scores_high(self, scorer, test_docs_dir):
        """Highly compressed should score 0.8-0.9."""
        text = (test_docs_dir / "compressed_doc.md").read_text()
        result = scorer.calculate_score(text)
        
        assert 0.8 <= result["overall_score"] <= 0.9
        assert result["safe_to_compress"] is False
        assert result["interpretation"] == "highly_compressed"
    
    def test_list_density_metric(self, scorer):
        """Test list density calculation."""
        text = "- Item 1\n- Item 2\n- Item 3"
        result = scorer.calculate_score(text)
        assert result["metrics"]["list_density"] > 0.8
    
    def test_prose_ratio_metric(self, scorer):
        """Test prose ratio calculation."""
        text = "This is a long paragraph with lots of prose. " * 10
        result = scorer.calculate_score(text)
        assert result["metrics"]["prose_ratio"] > 0.8
    
    def test_explanation_markers(self, scorer):
        """Test detection of explanation phrases."""
        text = "For example, this means that in other words, to illustrate"
        result = scorer.calculate_score(text)
        assert result["metrics"]["explanation_markers"] >= 3

# Add more specific metric tests as needed
```

---

## Validation Report Template

Create `validation_report_task_2.1.md` with:

```markdown
# Task 2.1 Validation Report: Compression Score Algorithm

**Date**: [timestamp]
**Status**: PASS/FAIL
**Checkpoint**: 3/3 Complete

## Test Results

### Test Document 1: Verbose
- Expected: 0.2-0.3
- Actual: [score]
- Status: PASS/FAIL
- Metrics: [breakdown]

### Test Document 2: Moderate
- Expected: 0.5-0.6
- Actual: [score]
- Status: PASS/FAIL
- Metrics: [breakdown]

### Test Document 3: Compressed
- Expected: 0.8-0.9
- Actual: [score]
- Status: PASS/FAIL
- Metrics: [breakdown]

## Metric Analysis

### List Density
[Analysis of how well it detects lists vs prose]

### Prose Ratio
[Analysis of prose detection accuracy]

### Sentence Length
[Analysis of sentence length normalization]

### Redundancy
[Analysis of repeated phrase detection]

### Explanation Markers
[Analysis of scaffolding detection]

### Information Entropy
[Analysis of entropy calculation]

## Overall Assessment

- Algorithm accuracy: [%]
- Scores correlate with manual assessment: YES/NO
- Ready for integration: YES/NO

## Recommendations

[Any tuning needed, edge cases discovered, etc.]
```

---

## Success Criteria

### Must Pass
- ✓ All test cases pass with expected score ranges (±0.1)
- ✓ Scores increase monotonically: verbose < moderate < compressed
- ✓ Safe-to-compress flag works correctly (false when score ≥ 0.8)
- ✓ Deterministic (same input → same score)

### Should Pass
- ✓ Scores correlate with manual assessment
- ✓ Metric breakdowns are interpretable
- ✓ Edge cases handled (empty docs, pure code blocks, etc.)

### Nice to Have
- Clear documentation
- Performance: <100ms per document
- Extensible architecture for future metrics

---

## Final Deliverables

1. `scripts/compression_score.py` - Main implementation
2. `tests/test_compression_score.py` - Full test suite
3. `tests/fixtures/` - Three test documents
4. `checkpoints/` - Three checkpoint reports
5. `validation_report_task_2.1.md` - Comprehensive validation
6. `README_task_2.1.md` - Usage guide

---

## Sequential Task Dependencies

**This task enables**:
- Task 2.2: Round-trip compression test (needs scoring)
- Task 1.1: Content density analyzer (needs scoring per section)
- Task 2.3: Safety checks (needs pre-compression scoring)

**After completion**: Report results in main session for review before proceeding to dependent tasks.

---

## Notes

- Use tiktoken for token counting (matches OpenAI/Anthropic)
- Test on real docs from /Users/dudley/Projects/Compression/docs/ after basic validation
- Document any score calibration decisions
- If scores don't match expectations, tune metric weights (document changes)

**Working Directory**: /Users/dudley/Projects/Compression
