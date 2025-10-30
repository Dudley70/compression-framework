# Claude Code Task: Round-Trip Compression Test (Task 2.2)

**Task ID**: TASK-2.2-ROUND-TRIP  
**Priority**: HIGH (MVP requirement)  
**Estimated Time**: 3-5 hours  
**Approach**: TDD with checkpoint system  
**Dependencies**: TASK-2.1 (compression score algorithm)

---

## Project Context

This is part of a compression research project evaluating methods for AI context optimization. We've developed a unified theory where all compression techniques optimize three parameters (σ, γ, κ) subject to comprehension constraints.

**Current Phase**: Validation - testing critical design assumptions before building the full automation tool.

**This Task's Role**: Prove that the compression system is **idempotent** - attempting to compress already-compressed content is correctly refused, preventing information loss through repeated compression.

---

## Objective

Build a test suite that demonstrates compression idempotency:
1. Take verbose document (compression score ~0.2-0.3)
2. Apply compression with target parameters
3. Measure result (compression score should be 0.7-0.8)
4. Attempt to compress the result again
5. **Expected**: System refuses (score already ≥ 0.8)
6. Verify no information was lost in first compression

This proves the safety mechanism works - compressed content is protected from further compression.

---

## TDD Approach

### Phase 1: Write Tests First (Checkpoint 1)
1. Create test procedure structure
2. Define expected behaviors at each step
3. Write failing tests (no compression implementation yet)
4. **Checkpoint**: All tests FAIL with clear expectations

### Phase 2: Implement Test Harness (Checkpoint 2)
1. Build mock compression function for testing
2. Integrate compression_score from Task 2.1
3. Implement refusal logic
4. Make tests pass
5. **Checkpoint**: All tests PASS with mock implementation

### Phase 3: Validate with Real Examples (Checkpoint 3)
1. Test with multiple document types
2. Validate entity preservation
3. Test edge cases
4. **Checkpoint**: Idempotency proven across examples

---

## Checkpoint System

### Checkpoint 1: Test Procedure Defined ✓
**Deliverable**: `tests/test_round_trip.py` (tests fail)  
**Validation**:
```bash
pytest tests/test_round_trip.py
# Expected: All tests FAIL (no implementation)
```
**Output**: `checkpoints/checkpoint_1_round_trip_tests.md`

### Checkpoint 2: Refusal Logic Works ✓
**Deliverable**: Mock compression with refusal logic  
**Validation**:
```bash
pytest tests/test_round_trip.py
# Expected: All tests PASS
```
**Output**: `checkpoints/checkpoint_2_round_trip_impl.md`

### Checkpoint 3: Validation Complete ✓
**Deliverable**: `validation_report_task_2.2.md`  
**Validation**: Idempotency proven with real examples  
**Output**: `checkpoints/checkpoint_3_round_trip_validated.md`

---

## Technical Specifications

### Core Test Procedure

```python
from scripts.compression_score import CompressionScorer

def test_basic_idempotency():
    """
    Basic idempotency test: compress once, refuse second compression.
    """
    # Step 1: Start with verbose document
    verbose_doc = load_test_document("verbose_api_doc.md")
    initial_score = scorer.calculate_score(verbose_doc)
    assert initial_score["overall_score"] < 0.3, "Document should be verbose"
    
    # Step 2: Apply compression
    compressed_doc = mock_compress(verbose_doc, sigma=0.8, gamma=0.6, kappa=0.2)
    compressed_score = scorer.calculate_score(compressed_doc)
    assert 0.7 <= compressed_score["overall_score"] <= 0.8, "Should be compressed"
    
    # Step 3: Attempt second compression (SHOULD REFUSE)
    result = mock_compress(compressed_doc, sigma=0.8, gamma=0.6, kappa=0.2)
    assert result["refused"] == True, "Should refuse compression"
    assert "already compressed" in result["message"].lower()
    
    # Step 4: Verify no information loss
    entities_preserved = check_entity_preservation(verbose_doc, compressed_doc)
    assert entities_preserved >= 0.80, "Must preserve ≥80% of entities"
```

### Test Cases

#### Test 1: Basic Idempotency
- Verbose doc (score 0.2) → compress → score 0.75 → attempt re-compress → refused

#### Test 2: Aggressive Re-compression Attempt
- Compressed doc (score 0.75) → attempt with σ=0.9, γ=0.4, κ=0.1 → refused/warned

#### Test 3: Minimal Benefit Detection
- Already dense doc (score 0.6) → compress → only 5% reduction → refused (minimal benefit)

#### Test 4: Entity Preservation Validation
- Technical doc with API names → compress → verify all entities present

#### Test 5: Multiple Document Types
- API reference, tutorial, session notes → all show idempotency

#### Test 6: Edge Case - Just Below Threshold
- Doc at score 0.78 → compression allowed but warned
- Result at score 0.82 → second compression refused

---

## Mock Compression Implementation

For testing purposes, create a mock compression function:

```python
class MockCompressor:
    """
    Mock compression for testing idempotency logic.
    In real tool, this would call actual compression algorithms.
    """
    
    def __init__(self, scorer):
        self.scorer = scorer
        self.refusal_threshold = 0.8
        self.minimal_benefit_threshold = 0.85  # compression ratio
        
    def compress(self, text, sigma, gamma, kappa):
        """
        Mock compression with safety checks.
        """
        # Pre-check: Already compressed?
        current_score = self.scorer.calculate_score(text)
        
        if current_score["overall_score"] >= self.refusal_threshold:
            return {
                "refused": True,
                "reason": "already_compressed",
                "message": f"Document already compressed (score: {current_score['overall_score']:.2f}). Refusing to prevent information loss.",
                "current_score": current_score["overall_score"]
            }
        
        # Mock compression (in reality, apply actual compression algorithms)
        compressed = self._mock_compress_text(text, sigma, gamma, kappa)
        
        # Post-check: Minimal benefit?
        original_tokens = self._count_tokens(text)
        compressed_tokens = self._count_tokens(compressed)
        compression_ratio = compressed_tokens / original_tokens
        
        if compression_ratio > self.minimal_benefit_threshold:
            return {
                "refused": True,
                "reason": "minimal_benefit",
                "message": f"Compression achieves only {(1-compression_ratio)*100:.1f}% reduction. Risk vs benefit too high.",
                "compression_ratio": compression_ratio
            }
        
        # Post-check: Entity preservation
        entities_preserved = self._check_entities(text, compressed)
        
        if entities_preserved < 0.80:
            return {
                "refused": True,
                "reason": "entity_loss",
                "message": f"Compression would lose {(1-entities_preserved)*100:.1f}% of entities. Refusing.",
                "entities_preserved": entities_preserved
            }
        
        return {
            "refused": False,
            "compressed_text": compressed,
            "original_tokens": original_tokens,
            "compressed_tokens": compressed_tokens,
            "compression_ratio": compression_ratio,
            "final_score": self.scorer.calculate_score(compressed)["overall_score"],
            "entities_preserved": entities_preserved
        }
    
    def _mock_compress_text(self, text, sigma, gamma, kappa):
        """
        Simulate compression based on parameters.
        In reality, would apply actual compression algorithms.
        For testing, we can use simple transformations.
        """
        # Simple mock: higher sigma = more lists, lower gamma = shorter
        # This is just for testing the safety logic
        lines = text.split('\n')
        compressed_lines = []
        
        for line in lines:
            if sigma > 0.7 and len(line) > 80:
                # Convert long lines to bullet points
                compressed_lines.append(f"- {line[:60]}...")
            elif gamma < 0.5:
                # Shorten sentences
                words = line.split()[:10]
                compressed_lines.append(" ".join(words))
            else:
                compressed_lines.append(line)
        
        return '\n'.join(compressed_lines)
    
    def _count_tokens(self, text):
        """Use same tokenizer as compression_score."""
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    
    def _check_entities(self, original, compressed):
        """
        Simple entity preservation check.
        In real implementation, use spaCy NER.
        """
        # For testing, check if key technical terms are preserved
        import re
        entities_orig = set(re.findall(r'\b[A-Z][a-z]+\b|\b[A-Z]{2,}\b|/\w+', original))
        entities_comp = set(re.findall(r'\b[A-Z][a-z]+\b|\b[A-Z]{2,}\b|/\w+', compressed))
        
        if len(entities_orig) == 0:
            return 1.0
        
        preserved = len(entities_orig & entities_comp) / len(entities_orig)
        return preserved
```

---

## Test Document Templates

### Test Document 1: Verbose API Documentation

```markdown
# API Authentication Documentation

## Overview

The authentication system provides a secure way for clients to verify their identity
with the server. This is accomplished through a token-based authentication mechanism
that follows industry best practices.

## Authentication Endpoint

The authentication endpoint is located at `/auth` and accepts POST requests. When you
want to authenticate with the API, you need to send your credentials to this endpoint.

The endpoint expects a JSON body containing two fields:
- A username field containing the user's username
- A password field containing the user's password

When the server receives this request, it will validate the credentials. If the
credentials are valid, the server will generate an authentication token and return it
to the client. If the credentials are invalid, the server will return an error message
explaining why authentication failed.

The response format is as follows:
- On success, you receive a 200 status code with a JSON body containing the token
- On failure, you receive a 401 status code with an error message

This token should be included in subsequent requests to authenticate yourself with the API.
```

**Expected**:
- Initial score: 0.2-0.3 (verbose)
- After compression: 0.7-0.8
- Second compression: Refused

### Test Document 2: Already Compressed

```markdown
## POST /auth
- Body: `{username: string, password: string}`
- Returns: `{token: string}` (200) | `{error: string}` (401)
- Auth: None required

## GET /users  
- Auth: Bearer token
- Returns: User array
- Filters: `?role=admin&status=active`
```

**Expected**:
- Initial score: 0.85 (already compressed)
- Compression attempt: Refused immediately

---

## Implementation Guidelines

### Required Libraries
```bash
# From Task 2.1
# - tiktoken
# - markdown-it-py
# - nltk
# - numpy

# Additional for this task
pip install pytest --break-system-packages
```

### Project Structure
```
/Users/dudley/Projects/Compression/
├── scripts/
│   ├── compression_score.py         # From Task 2.1
│   └── mock_compressor.py           # New: mock compression for testing
├── tests/
│   ├── test_round_trip.py           # New: idempotency tests
│   └── fixtures/
│       ├── verbose_api_doc.md       # Test document 1
│       ├── compressed_api_doc.md    # Test document 2
│       └── technical_doc.md         # Test document 3
├── checkpoints/
│   ├── checkpoint_1_round_trip_tests.md
│   ├── checkpoint_2_round_trip_impl.md
│   └── checkpoint_3_round_trip_validated.md
└── validation_report_task_2.2.md    # Final deliverable
```

---

## Test Template

```python
import pytest
from scripts.compression_score import CompressionScorer
from scripts.mock_compressor import MockCompressor

class TestRoundTripCompression:
    """Test suite for compression idempotency."""
    
    @pytest.fixture
    def scorer(self):
        return CompressionScorer()
    
    @pytest.fixture
    def compressor(self, scorer):
        return MockCompressor(scorer)
    
    def test_basic_idempotency(self, compressor, scorer):
        """Compress once succeeds, second compression refused."""
        # Test implementation here
        pass
    
    def test_aggressive_recompression_refused(self, compressor, scorer):
        """Even more aggressive parameters refused on already-compressed content."""
        pass
    
    def test_minimal_benefit_detection(self, compressor, scorer):
        """Refuse compression when benefit is minimal."""
        pass
    
    def test_entity_preservation(self, compressor, scorer):
        """Verify entities are preserved during compression."""
        pass
    
    def test_multiple_document_types(self, compressor, scorer):
        """Idempotency works across different document types."""
        pass
    
    def test_edge_case_near_threshold(self, compressor, scorer):
        """Handle documents near the refusal threshold."""
        pass
```

---

## Validation Report Template

```markdown
# Validation Report: Round-Trip Compression Test (Task 2.2)

**Date**: [YYYY-MM-DD]
**Task**: TASK-2.2-ROUND-TRIP
**Status**: [PASS/FAIL]

## Summary

[Brief summary of validation results]

## Test Results

### Test 1: Basic Idempotency
- ✓/✗ Verbose document compressed successfully
- ✓/✗ Compression score increased as expected (0.2 → 0.75)
- ✓/✗ Second compression correctly refused
- ✓/✗ Refusal message was clear

### Test 2: Aggressive Re-compression
- ✓/✗ Already-compressed content refused even with aggressive parameters
- ✓/✗ Warning message explained risk

[Continue for all tests...]

## Entity Preservation Analysis

| Document Type | Original Entities | Preserved | Percentage |
|--------------|-------------------|-----------|------------|
| API Docs     | 25                | 24        | 96%        |
| Tutorial     | 18                | 17        | 94%        |
| Technical    | 32                | 28        | 88%        |

**All documents preserved ≥ 80% of entities ✓**

## Safety Mechanism Effectiveness

- Pre-check (score ≥ 0.8): [X/X] tests passed
- Post-check (minimal benefit): [X/X] tests passed
- Post-check (entity loss): [X/X] tests passed

## Edge Cases

[Document any interesting edge cases discovered]

## Conclusions

- [x] Idempotency proven: System refuses to compress already-compressed content
- [x] Safety checks work: No information loss detected
- [x] Clear messaging: Refusal messages are actionable
- [x] Threshold validated: 0.8 score threshold is appropriate

## Recommendations

[Any recommendations for threshold tuning, additional checks, etc.]

## Success Criteria Met

- [x] First compression succeeds with expected score increase
- [x] Second compression correctly refused  
- [x] Refusal message clear and actionable
- [x] Entity preservation ≥ 80%

**Overall Status**: PASS
```

---

## Success Criteria

### Must Pass (Critical)
- ✓ Basic idempotency test passes
- ✓ Second compression is refused when score ≥ 0.8
- ✓ Entity preservation ≥ 80% in all test cases
- ✓ Refusal messages are clear and actionable

### Should Pass (Important)
- ✓ Minimal benefit detection works
- ✓ Edge cases near threshold handled correctly
- ✓ Multiple document types show idempotency

### Nice to Have (Optional)
- Suggestions for threshold tuning
- Performance metrics
- Additional safety checks identified

---

## Final Deliverables

1. `tests/test_round_trip.py` - Complete test suite
2. `scripts/mock_compressor.py` - Mock compression implementation
3. `tests/fixtures/` - Test documents (3+ examples)
4. `checkpoints/checkpoint_1_round_trip_tests.md` - Tests written
5. `checkpoints/checkpoint_2_round_trip_impl.md` - Implementation complete
6. `checkpoints/checkpoint_3_round_trip_validated.md` - Validation done
7. `validation_report_task_2.2.md` - Final validation report

---

## Sequential Task Dependencies

**This task requires**:
- TASK-2.1: compression_score.py must be complete and working
- CompressionScorer class must be importable
- Scoring algorithm must be validated

**This task enables**:
- TASK-2.3: Safety checks implementation (uses refusal logic)
- Full tool development (idempotency proven)
- Confidence in production deployment

**This proves**:
- Compression is safe (no repeated compression)
- Information fidelity is maintained
- Safety mechanisms work as designed

---

## Notes

### Important Context
- This is a **safety-critical** validation
- Idempotency is essential for production use
- Without this, users could accidentally compress documents multiple times
- Information loss is unacceptable

### Design Decisions
- 0.8 threshold chosen based on research (high compression = unsafe to re-compress)
- 80% entity preservation is minimum acceptable
- Minimal benefit threshold (85% compression ratio) prevents risky compression

### Future Enhancements
- Real compression algorithms (not mock)
- Semantic similarity validation (BERTScore)
- More sophisticated entity recognition (spaCy NER)
- User override option with warnings

---

**Working Directory**: /Users/dudley/Projects/Compression  
**Created**: 2025-10-30  
**Depends on**: Task 2.1 completion
