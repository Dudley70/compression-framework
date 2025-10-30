# Claude Code Task: Token Drift Detection (Task 1.2)

**Task ID**: TASK-1.2-TOKEN-DRIFT  
**Priority**: HIGH (MVP requirement)  
**Estimated Time**: 2-4 hours  
**Approach**: TDD with checkpoint system  
**Can Run**: Parallel with Task 2.1 (independent)

---

## Project Context

This is part of a compression research project evaluating methods for AI context optimization. We've developed a unified theory where all compression techniques optimize three parameters (σ, γ, κ) subject to comprehension constraints.

**Current Phase**: Validation - testing critical design assumptions before building the full automation tool.

**This Task's Role**: Detect when previously-compressed documents have grown significantly due to new content, triggering a review/re-compression recommendation.

---

## Objective

Build a token drift detection system that compares a document's current token count against the baseline stored in its YAML header, identifying when documents need re-compression.

**Core Problem**: Document compressed → new content added → header says "compressed" but document now has mixed state.

**Solution**: Simple metric tracking token growth from baseline.

---

## TDD Approach

### Phase 1: Write Tests First (Checkpoint 1)
1. Create test documents with headers
2. Define expected drift ratios and recommendations
3. Write failing tests
4. **Checkpoint**: All tests fail as expected

### Phase 2: Implement Detection (Checkpoint 2)
1. Implement YAML header parsing
2. Implement token counting
3. Implement drift calculation
4. Make tests pass
5. **Checkpoint**: All tests pass

### Phase 3: Validate Thresholds (Checkpoint 3)
1. Test with real project documents
2. Validate recommendations are actionable
3. **Checkpoint**: Thresholds work in practice

---

## Checkpoint System

### Checkpoint 1: Test Suite Complete ✓
**Deliverable**: `tests/test_token_drift.py`  
**Validation**:
```bash
pytest tests/test_token_drift.py
# Expected: All tests FAIL (no implementation)
```
**Output**: `checkpoints/checkpoint_1_tests_written.md`

### Checkpoint 2: Basic Implementation ✓
**Deliverable**: `scripts/detect_token_drift.py`  
**Validation**:
```bash
pytest tests/test_token_drift.py
# Expected: All tests PASS
```
**Output**: `checkpoints/checkpoint_2_basic_impl.md`

### Checkpoint 3: Threshold Validation ✓
**Deliverable**: `validation_report_task_1.2.md`  
**Validation**: Test on 5+ real docs, verify recommendations  
**Output**: `checkpoints/checkpoint_3_validated.md`

---

## Technical Specifications

### Algorithm Requirements

Implement `check_token_drift(file_path: str) -> dict`:

**Return Structure**:
```python
{
    "has_header": true,
    "baseline_tokens": 1400,        # From header
    "current_tokens": 1750,         # Current count
    "drift_ratio": 1.25,            # current / baseline
    "drift_percentage": 25.0,       # (current - baseline) / baseline * 100
    "absolute_drift": 350,          # current - baseline
    "recommendation": "review",     # none|flag|review|compress
    "explanation": "Document has grown 25% since compression. Review for new content that needs compression."
}
```

### Drift Thresholds

```python
THRESHOLDS = {
    "flag": 1.15,      # 15% growth → yellow flag
    "review": 1.30,    # 30% growth → recommend review
    "compress": 1.50   # 50% growth → recommend re-compression
}
```

**Recommendation Logic**:
- `drift_ratio < 1.15`: recommendation = "none" (minimal drift, no action)
- `1.15 ≤ drift_ratio < 1.30`: recommendation = "flag" (monitor)
- `1.30 ≤ drift_ratio < 1.50`: recommendation = "review" (check for new content)
- `drift_ratio ≥ 1.50`: recommendation = "compress" (significant growth)

### Header Format

Expected YAML frontmatter in documents:
```yaml
---
compression:
  last_full_compression: 2025-10-30 15:30 AEDT
  baseline_tokens: 1400
  parameters: {σ: 0.8, γ: 0.6, κ: 0.2}
---
```

**Required Fields**:
- `compression.baseline_tokens` (int) - token count after last compression

**Optional Fields** (read but not required):
- `compression.last_full_compression` (datetime)
- `compression.parameters` (dict)

---

## Test Cases (Phase 1)

### Test Case 1: No Drift
**Scenario**: Document compressed, no changes

```markdown
---
compression:
  baseline_tokens: 1000
---
[Exactly 1000 tokens of content]
```

**Expected**:
- drift_ratio: 1.0
- recommendation: "none"

---

### Test Case 2: Minor Edit (5% growth)
**Scenario**: Small addition after compression

```markdown
---
compression:
  baseline_tokens: 1000
---
[1050 tokens of content]
```

**Expected**:
- drift_ratio: 1.05
- recommendation: "none"
- explanation: "Minimal drift (5%), no action needed"

---

### Test Case 3: Moderate Growth (25% growth)
**Scenario**: New section added

```markdown
---
compression:
  baseline_tokens: 1000
---
[1250 tokens of content]
```

**Expected**:
- drift_ratio: 1.25
- recommendation: "review"
- explanation: "Document has grown 25% since compression. Review for new content that needs compression."

---

### Test Case 4: Substantial Growth (50% growth)
**Scenario**: Major additions

```markdown
---
compression:
  baseline_tokens: 1000
---
[1500 tokens of content]
```

**Expected**:
- drift_ratio: 1.50
- recommendation: "compress"
- explanation: "Document has grown 50% since compression. Recommend full re-compression."

---

### Test Case 5: No Header
**Scenario**: Document without compression metadata

```markdown
# Document Without Header

This document was never compressed.
```

**Expected**:
- has_header: false
- baseline_tokens: null
- current_tokens: [actual count]
- drift_ratio: null
- recommendation: "untracked"
- explanation: "Document has no compression baseline. Cannot detect drift."

---

### Test Case 6: Malformed Header
**Scenario**: Header missing required field

```markdown
---
compression:
  last_full_compression: 2025-10-30
  # Missing baseline_tokens
---
Content here
```

**Expected**:
- has_header: true (partial)
- baseline_tokens: null
- recommendation: "invalid_header"
- explanation: "Compression header exists but missing baseline_tokens field."

---

## Implementation Guidelines

### Required Python Libraries
```bash
pip install tiktoken pyyaml --break-system-packages
```

### Project Structure
```
/Users/dudley/Projects/Compression/
├── scripts/
│   └── detect_token_drift.py          # Main implementation
├── tests/
│   ├── test_token_drift.py            # Test suite
│   └── fixtures/
│       ├── no_drift.md                # Test case 1
│       ├── minor_drift.md             # Test case 2
│       ├── moderate_drift.md          # Test case 3
│       ├── substantial_drift.md       # Test case 4
│       ├── no_header.md               # Test case 5
│       └── malformed_header.md        # Test case 6
├── checkpoints/
│   ├── checkpoint_1_tests_written.md
│   ├── checkpoint_2_basic_impl.md
│   └── checkpoint_3_validated.md
└── validation_report_task_1.2.md
```

### Code Structure Template

```python
# scripts/detect_token_drift.py
import tiktoken
import yaml
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class DriftResult:
    has_header: bool
    baseline_tokens: Optional[int]
    current_tokens: int
    drift_ratio: Optional[float]
    drift_percentage: Optional[float]
    absolute_drift: Optional[int]
    recommendation: str
    explanation: str

class TokenDriftDetector:
    # Thresholds for drift recommendations
    FLAG_THRESHOLD = 1.15      # 15% growth
    REVIEW_THRESHOLD = 1.30    # 30% growth
    COMPRESS_THRESHOLD = 1.50  # 50% growth
    
    def __init__(self):
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def check_drift(self, file_path: str) -> Dict:
        """
        Main entry point: check token drift for a document.
        
        Args:
            file_path: Path to markdown file
            
        Returns:
            Dictionary with drift analysis results
        """
        content = Path(file_path).read_text()
        
        # Parse header
        baseline = self._extract_baseline(content)
        
        # Count current tokens
        current = self._count_tokens(content)
        
        # Calculate drift
        result = self._calculate_drift(baseline, current)
        
        return self._format_result(result)
    
    def _extract_baseline(self, content: str) -> Optional[int]:
        """Extract baseline_tokens from YAML frontmatter."""
        # TODO: Parse YAML header and extract compression.baseline_tokens
        pass
    
    def _count_tokens(self, content: str) -> int:
        """Count tokens in document (excluding YAML header)."""
        # TODO: Remove YAML frontmatter, count remaining tokens
        pass
    
    def _calculate_drift(self, baseline: Optional[int], current: int) -> DriftResult:
        """Calculate drift metrics and recommendation."""
        # Handle no baseline case
        if baseline is None:
            return DriftResult(
                has_header=False,
                baseline_tokens=None,
                current_tokens=current,
                drift_ratio=None,
                drift_percentage=None,
                absolute_drift=None,
                recommendation="untracked",
                explanation="Document has no compression baseline. Cannot detect drift."
            )
        
        # Calculate drift
        drift_ratio = current / baseline
        drift_percentage = ((current - baseline) / baseline) * 100
        absolute_drift = current - baseline
        
        # Determine recommendation
        recommendation, explanation = self._get_recommendation(
            drift_ratio, drift_percentage
        )
        
        return DriftResult(
            has_header=True,
            baseline_tokens=baseline,
            current_tokens=current,
            drift_ratio=drift_ratio,
            drift_percentage=drift_percentage,
            absolute_drift=absolute_drift,
            recommendation=recommendation,
            explanation=explanation
        )
    
    def _get_recommendation(self, ratio: float, percentage: float) -> tuple[str, str]:
        """Determine recommendation based on drift ratio."""
        if ratio < self.FLAG_THRESHOLD:
            return "none", f"Minimal drift ({percentage:.1f}%), no action needed."
        elif ratio < self.REVIEW_THRESHOLD:
            return "flag", f"Document has grown {percentage:.1f}% since compression. Monitor for further growth."
        elif ratio < self.COMPRESS_THRESHOLD:
            return "review", f"Document has grown {percentage:.1f}% since compression. Review for new content that needs compression."
        else:
            return "compress", f"Document has grown {percentage:.1f}% since compression. Recommend full re-compression."
    
    def _format_result(self, result: DriftResult) -> Dict:
        """Convert DriftResult to dictionary."""
        return {
            "has_header": result.has_header,
            "baseline_tokens": result.baseline_tokens,
            "current_tokens": result.current_tokens,
            "drift_ratio": result.drift_ratio,
            "drift_percentage": result.drift_percentage,
            "absolute_drift": result.absolute_drift,
            "recommendation": result.recommendation,
            "explanation": result.explanation
        }

# Convenience function for CLI usage
def check_file(path: str) -> Dict:
    """Check token drift for a file."""
    detector = TokenDriftDetector()
    return detector.check_drift(path)
```

---

## Test Template

```python
# tests/test_token_drift.py
import pytest
from pathlib import Path
from scripts.detect_token_drift import TokenDriftDetector

@pytest.fixture
def detector():
    return TokenDriftDetector()

@pytest.fixture
def fixtures_dir():
    return Path(__file__).parent / "fixtures"

class TestTokenDrift:
    
    def test_no_drift(self, detector, fixtures_dir):
        """No changes should result in 1.0 drift ratio."""
        result = detector.check_drift(str(fixtures_dir / "no_drift.md"))
        
        assert result["has_header"] is True
        assert result["drift_ratio"] == pytest.approx(1.0, rel=0.01)
        assert result["recommendation"] == "none"
    
    def test_minor_drift(self, detector, fixtures_dir):
        """5% growth should not trigger action."""
        result = detector.check_drift(str(fixtures_dir / "minor_drift.md"))
        
        assert result["drift_ratio"] == pytest.approx(1.05, rel=0.02)
        assert result["recommendation"] == "none"
    
    def test_moderate_drift_flags(self, detector, fixtures_dir):
        """25% growth should recommend review."""
        result = detector.check_drift(str(fixtures_dir / "moderate_drift.md"))
        
        assert result["drift_ratio"] == pytest.approx(1.25, rel=0.02)
        assert result["recommendation"] == "review"
        assert result["drift_percentage"] == pytest.approx(25.0, rel=1.0)
    
    def test_substantial_drift_compresses(self, detector, fixtures_dir):
        """50% growth should recommend compression."""
        result = detector.check_drift(str(fixtures_dir / "substantial_drift.md"))
        
        assert result["drift_ratio"] >= 1.50
        assert result["recommendation"] == "compress"
    
    def test_no_header_untracked(self, detector, fixtures_dir):
        """Document without header should be marked untracked."""
        result = detector.check_drift(str(fixtures_dir / "no_header.md"))
        
        assert result["has_header"] is False
        assert result["baseline_tokens"] is None
        assert result["drift_ratio"] is None
        assert result["recommendation"] == "untracked"
        assert result["current_tokens"] > 0  # Still counts current
    
    def test_malformed_header(self, detector, fixtures_dir):
        """Header missing baseline_tokens should be handled."""
        result = detector.check_drift(str(fixtures_dir / "malformed_header.md"))
        
        assert result["recommendation"] in ["invalid_header", "untracked"]
        assert result["baseline_tokens"] is None
    
    def test_threshold_boundaries(self, detector):
        """Test exact threshold boundaries."""
        # 15% exactly (FLAG_THRESHOLD)
        result = detector._calculate_drift(1000, 1150)
        assert result.recommendation == "flag"
        
        # 30% exactly (REVIEW_THRESHOLD)
        result = detector._calculate_drift(1000, 1300)
        assert result.recommendation == "review"
        
        # 50% exactly (COMPRESS_THRESHOLD)
        result = detector._calculate_drift(1000, 1500)
        assert result.recommendation == "compress"
    
    def test_token_counting_excludes_header(self, detector, fixtures_dir):
        """Token count should exclude YAML frontmatter."""
        result = detector.check_drift(str(fixtures_dir / "no_drift.md"))
        
        # If baseline is 1000, current should also be ~1000 (not including header)
        assert result["current_tokens"] == pytest.approx(
            result["baseline_tokens"], rel=0.02
        )
```

---

## Test Fixtures

Create test files with specific token counts:

### fixtures/no_drift.md
```markdown
---
compression:
  baseline_tokens: 1000
---

[Generate exactly 1000 tokens of content]
```

### fixtures/minor_drift.md
```markdown
---
compression:
  baseline_tokens: 1000
---

[Generate 1050 tokens of content (5% growth)]
```

### fixtures/moderate_drift.md
```markdown
---
compression:
  baseline_tokens: 1000
---

[Generate 1250 tokens of content (25% growth)]
```

### fixtures/substantial_drift.md
```markdown
---
compression:
  baseline_tokens: 1000
---

[Generate 1500 tokens of content (50% growth)]
```

### fixtures/no_header.md
```markdown
# Document Without Header

This document has no compression metadata.
It should be marked as "untracked" since we cannot
calculate drift without a baseline.
```

### fixtures/malformed_header.md
```markdown
---
compression:
  last_full_compression: 2025-10-30
  # Missing baseline_tokens field
---

Content here that cannot have drift calculated.
```

---

## Validation Report Template

Create `validation_report_task_1.2.md`:

```markdown
# Task 1.2 Validation Report: Token Drift Detection

**Date**: [timestamp]
**Status**: PASS/FAIL
**Checkpoint**: 3/3 Complete

## Test Results

### Test Case 1: No Drift
- Expected: ratio ≈ 1.0, recommendation = "none"
- Actual: ratio = [X], recommendation = [Y]
- Status: PASS/FAIL

### Test Case 2: Minor Drift (5%)
- Expected: ratio ≈ 1.05, recommendation = "none"
- Actual: ratio = [X], recommendation = [Y]
- Status: PASS/FAIL

### Test Case 3: Moderate Drift (25%)
- Expected: ratio ≈ 1.25, recommendation = "review"
- Actual: ratio = [X], recommendation = [Y]
- Status: PASS/FAIL

### Test Case 4: Substantial Drift (50%)
- Expected: ratio ≥ 1.50, recommendation = "compress"
- Actual: ratio = [X], recommendation = [Y]
- Status: PASS/FAIL

### Test Case 5: No Header
- Expected: has_header = false, recommendation = "untracked"
- Actual: [results]
- Status: PASS/FAIL

### Test Case 6: Malformed Header
- Expected: baseline = null, recommendation = "invalid_header"
- Actual: [results]
- Status: PASS/FAIL

## Real Document Testing

Tested on 5 documents from /Users/dudley/Projects/Compression/docs/:

1. [Document name]: [results and recommendation]
2. [Document name]: [results and recommendation]
3. [Document name]: [results and recommendation]
4. [Document name]: [results and recommendation]
5. [Document name]: [results and recommendation]

## Threshold Analysis

### 15% Threshold (Flag)
- Appropriate: YES/NO
- Rationale: [explain]

### 30% Threshold (Review)
- Appropriate: YES/NO
- Rationale: [explain]

### 50% Threshold (Compress)
- Appropriate: YES/NO
- Rationale: [explain]

## Recommendations

[Any threshold adjustments, edge cases discovered, etc.]

## Overall Assessment

- Algorithm works correctly: YES/NO
- Thresholds are practical: YES/NO
- Ready for integration: YES/NO
```

---

## Success Criteria

### Must Pass
- ✓ All 6 test cases pass
- ✓ Token counting excludes YAML frontmatter
- ✓ Drift ratio calculated correctly
- ✓ Recommendations match thresholds
- ✓ Handles missing/malformed headers gracefully

### Should Pass
- ✓ Tested on 5+ real project documents
- ✓ Thresholds produce actionable recommendations
- ✓ Performance: <10ms per document

### Nice to Have
- Clear error messages for edge cases
- Batch processing capability
- CLI tool for manual checking

---

## Final Deliverables

1. `scripts/detect_token_drift.py` - Main implementation
2. `tests/test_token_drift.py` - Full test suite
3. `tests/fixtures/` - Six test documents
4. `checkpoints/` - Three checkpoint reports
5. `validation_report_task_1.2.md` - Validation with real docs
6. `README_task_1.2.md` - Usage guide

---

## Sequential Task Dependencies

**This task enables**:
- Task 1.3: Integrated mixed state handler (combines drift + compression score)

**Independent of**:
- Task 2.1: Compression score (can run in parallel)

**After completion**: Report results in main session for review.

---

## CLI Usage Example

After implementation, should be usable as:

```bash
# Check single file
python scripts/detect_token_drift.py docs/reference/INTEGRATION_GUIDE_CC_PROJECTS.md

# Output:
# Drift Analysis: INTEGRATION_GUIDE_CC_PROJECTS.md
# Baseline: 5,200 tokens
# Current: 6,630 tokens
# Drift: +1,430 tokens (+27.5%)
# Recommendation: REVIEW
# Explanation: Document has grown 27.5% since compression. Review for new content.

# Check all docs (optional enhancement)
python scripts/detect_token_drift.py docs/**/*.md --summary
```

---

## Notes

- Use tiktoken cl100k_base encoding (matches Anthropic Claude)
- YAML parsing should be robust (handle missing keys gracefully)
- Token count should exclude frontmatter but include everything else
- Consider adding batch mode for scanning entire directories (optional)

**Working Directory**: /Users/dudley/Projects/Compression
