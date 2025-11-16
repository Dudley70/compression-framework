# Claude Code Task: Safety Checks Implementation (Task 2.3)

**Task ID**: TASK-2.3-SAFETY-CHECKS  
**Priority**: HIGH (Production requirement)  
**Estimated Time**: 6-10 hours  
**Approach**: TDD with checkpoint system  
**Dependencies**: TASK-2.1 (compression score), TASK-2.2 (round-trip test), TASK-1.1 (content analyzer)

---

## Project Context

This is part of a compression research project evaluating methods for AI context optimization. We've developed a unified theory where all compression techniques optimize three parameters (σ, γ, κ) subject to comprehension constraints.

**Current Phase**: Validation - testing critical design assumptions before building the full automation tool.

**This Task's Role**: Implement comprehensive safety checks to prevent information loss during compression. This is the **final validation task** that integrates all previous work into a production-ready safety framework.

---

## Objective

Build a multi-layered safety system that validates compression operations through:
1. **Pre-checks**: Detect already-compressed content (refuse before attempting)
2. **Entity preservation**: Verify technical terms, API names, etc. are maintained (≥80%)
3. **Minimal benefit detection**: Refuse low-value compressions (compression ratio > 0.85)
4. **Semantic similarity**: Ensure meaning is preserved (≥0.75 similarity score)
5. **Integration**: Combine all checks into single validation framework

**Safety-First Philosophy**: When in doubt, refuse compression. Information loss is unacceptable.

---

## TDD Approach

### Phase 1: Write Tests First (Checkpoint 1)
1. Create test cases for each safety check
2. Define expected pass/fail conditions
3. Write failing tests
4. **Checkpoint**: All tests FAIL (no implementation)

### Phase 2: Implement Safety Gates (Checkpoint 2)
1. Implement each safety check independently
2. Integrate checks into single framework
3. Make tests pass
4. **Checkpoint**: All tests PASS

### Phase 3: Validate Integration (Checkpoint 3)
1. Test combined safety system
2. Validate on real documents
3. Test edge cases and false positives/negatives
4. **Checkpoint**: Production-ready safety framework

---

## Checkpoint System

### Checkpoint 1: Safety Tests Written ✓
**Deliverable**: `tests/test_safety_checks.py` (tests fail)  
**Validation**:
```bash
pytest tests/test_safety_checks.py
# Expected: All tests FAIL
```
**Output**: `checkpoints/checkpoint_1_safety_tests.md`

### Checkpoint 2: Safety Checks Implemented ✓
**Deliverable**: `scripts/safety_checks.py`  
**Validation**:
```bash
pytest tests/test_safety_checks.py
# Expected: All tests PASS
```
**Output**: `checkpoints/checkpoint_2_safety_impl.md`

### Checkpoint 3: Integration Validated ✓
**Deliverable**: `validation_report_task_2.3.md`  
**Validation**: Works on real documents, no false positives  
**Output**: `checkpoints/checkpoint_3_safety_validated.md`

---

## Technical Specifications

### Safety Framework Architecture

```python
from scripts.compression_score import CompressionScorer
from scripts.mock_compressor import MockCompressor
import spacy
from sentence_transformers import SentenceTransformer
import tiktoken

class SafetyValidator:
    """
    Multi-layered safety validation for compression operations.
    """
    
    def __init__(self):
        self.scorer = CompressionScorer()
        self.nlp = spacy.load("en_core_web_sm")  # For entity recognition
        self.similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
        # Thresholds (tunable)
        self.compression_refusal_threshold = 0.8  # score >= 0.8 → refuse
        self.entity_preservation_threshold = 0.80  # must preserve ≥80%
        self.minimal_benefit_threshold = 0.85  # compression ratio > 0.85 → refuse
        self.semantic_similarity_threshold = 0.75  # similarity ≥ 0.75
    
    def validate_compression(self, original_text: str, compressed_text: str, 
                           parameters: dict) -> dict:
        """
        Run all safety checks on a compression operation.
        
        Args:
            original_text: Pre-compression text
            compressed_text: Post-compression text
            parameters: {sigma, gamma, kappa}
        
        Returns:
            {
                "safe": True/False,
                "checks": {
                    "pre_check": {...},
                    "entity_preservation": {...},
                    "minimal_benefit": {...},
                    "semantic_similarity": {...}
                },
                "failures": [...],  # List of failed checks
                "recommendation": "accept" | "refuse" | "warn"
            }
        """
        pass
    
    def pre_check_already_compressed(self, text: str) -> dict:
        """
        Pre-check: Is content already compressed?
        
        Returns:
            {
                "passed": True/False,
                "score": 0.82,
                "threshold": 0.8,
                "message": "..."
            }
        """
        pass
    
    def check_entity_preservation(self, original: str, compressed: str) -> dict:
        """
        Check if entities (names, technical terms, API endpoints) are preserved.
        
        Uses spaCy NER to extract entities from both texts.
        
        Returns:
            {
                "passed": True/False,
                "original_entities": 25,
                "preserved_entities": 24,
                "preservation_rate": 0.96,
                "threshold": 0.80,
                "lost_entities": ["EntityName"],
                "message": "..."
            }
        """
        pass
    
    def check_minimal_benefit(self, original: str, compressed: str) -> dict:
        """
        Check if compression provides sufficient benefit.
        
        If compression ratio > 0.85 (only 15% reduction), risk vs benefit too high.
        
        Returns:
            {
                "passed": True/False,
                "original_tokens": 1000,
                "compressed_tokens": 900,
                "compression_ratio": 0.90,
                "reduction_pct": 10.0,
                "threshold": 0.85,
                "message": "..."
            }
        """
        pass
    
    def check_semantic_similarity(self, original: str, compressed: str) -> dict:
        """
        Check if meaning is preserved using sentence embeddings.
        
        Uses sentence-transformers to compute cosine similarity.
        
        Returns:
            {
                "passed": True/False,
                "similarity_score": 0.82,
                "threshold": 0.75,
                "message": "..."
            }
        """
        pass
```

---

## Detailed Safety Check Specifications

### 1. Pre-Check: Already Compressed

**Purpose**: Refuse compression if content is already dense (prevents over-compression)

**Implementation**:
```python
def pre_check_already_compressed(self, text):
    score_result = self.scorer.calculate_score(text)
    score = score_result["overall_score"]
    
    passed = score < self.compression_refusal_threshold
    
    return {
        "passed": passed,
        "score": score,
        "threshold": self.compression_refusal_threshold,
        "message": f"Content already compressed (score: {score:.2f})" if not passed else "Pre-check passed"
    }
```

**Test Cases**:
- Verbose text (score 0.25) → PASS
- Moderately compressed (score 0.55) → PASS
- Highly compressed (score 0.82) → FAIL

---

### 2. Entity Preservation Check

**Purpose**: Ensure critical information (names, terms, APIs) isn't lost

**Implementation**:
```python
def check_entity_preservation(self, original, compressed):
    # Extract entities using spaCy
    orig_doc = self.nlp(original)
    comp_doc = self.nlp(compressed)
    
    # Get entity text (unique)
    orig_entities = set(ent.text for ent in orig_doc.ents)
    comp_entities = set(ent.text for ent in comp_doc.ents)
    
    # Custom entity extraction for technical content
    # Add code identifiers, API paths, technical terms
    orig_entities.update(self._extract_technical_entities(original))
    comp_entities.update(self._extract_technical_entities(compressed))
    
    if len(orig_entities) == 0:
        return {"passed": True, "message": "No entities to preserve"}
    
    preserved = len(orig_entities & comp_entities)
    rate = preserved / len(orig_entities)
    passed = rate >= self.entity_preservation_threshold
    
    lost = orig_entities - comp_entities
    
    return {
        "passed": passed,
        "original_entities": len(orig_entities),
        "preserved_entities": preserved,
        "preservation_rate": rate,
        "threshold": self.entity_preservation_threshold,
        "lost_entities": list(lost),
        "message": f"Preserved {rate*100:.1f}% of entities" + 
                   (f" (lost: {', '.join(list(lost)[:5])})" if lost else "")
    }

def _extract_technical_entities(self, text):
    """
    Extract technical entities not caught by spaCy NER.
    - API paths: /api/users, /auth
    - Code identifiers: camelCase, snake_case
    - Technical acronyms: HTTP, API, JSON
    """
    import re
    entities = set()
    
    # API paths
    entities.update(re.findall(r'/[\w/]+', text))
    
    # Identifiers
    entities.update(re.findall(r'\b[a-z]+_[a-z_]+\b', text))  # snake_case
    entities.update(re.findall(r'\b[a-z]+[A-Z][a-zA-Z]+\b', text))  # camelCase
    
    # Technical terms (all caps, 2-5 letters)
    entities.update(re.findall(r'\b[A-Z]{2,5}\b', text))
    
    return entities
```

**Test Cases**:
- All entities preserved → PASS
- 90% preserved → PASS (≥80%)
- 75% preserved → FAIL (<80%)
- API path /auth lost → FAIL
- Technical term UUID lost → FAIL

---

### 3. Minimal Benefit Check

**Purpose**: Refuse compression when benefit doesn't justify risk

**Implementation**:
```python
def check_minimal_benefit(self, original, compressed):
    orig_tokens = len(self.tokenizer.encode(original))
    comp_tokens = len(self.tokenizer.encode(compressed))
    
    ratio = comp_tokens / orig_tokens
    reduction = (1 - ratio) * 100
    
    passed = ratio <= self.minimal_benefit_threshold
    
    return {
        "passed": passed,
        "original_tokens": orig_tokens,
        "compressed_tokens": comp_tokens,
        "compression_ratio": ratio,
        "reduction_pct": reduction,
        "threshold": self.minimal_benefit_threshold,
        "message": f"Compression achieves {reduction:.1f}% reduction" +
                   (" - insufficient benefit" if not passed else "")
    }
```

**Test Cases**:
- 50% reduction (ratio 0.50) → PASS
- 30% reduction (ratio 0.70) → PASS
- 10% reduction (ratio 0.90) → FAIL (>85%)
- 5% reduction (ratio 0.95) → FAIL

---

### 4. Semantic Similarity Check

**Purpose**: Ensure meaning is preserved despite text changes

**Implementation**:
```python
def check_semantic_similarity(self, original, compressed):
    # Generate embeddings
    orig_embedding = self.similarity_model.encode(original)
    comp_embedding = self.similarity_model.encode(compressed)
    
    # Compute cosine similarity
    from sklearn.metrics.pairwise import cosine_similarity
    similarity = cosine_similarity([orig_embedding], [comp_embedding])[0][0]
    
    passed = similarity >= self.semantic_similarity_threshold
    
    return {
        "passed": passed,
        "similarity_score": float(similarity),
        "threshold": self.semantic_similarity_threshold,
        "message": f"Semantic similarity: {similarity:.3f}" +
                   (" - meaning significantly changed" if not passed else "")
    }
```

**Test Cases**:
- Identical meaning, different wording → PASS (similarity ~0.90)
- Same meaning, compressed style → PASS (similarity ~0.80)
- Meaning slightly changed → PASS (similarity ~0.76)
- Meaning significantly changed → FAIL (similarity ~0.65)

---

## Integration: Complete Validation

```python
def validate_compression(self, original, compressed, parameters):
    """
    Run all checks and aggregate results.
    """
    checks = {}
    failures = []
    
    # Run each check
    checks["pre_check"] = self.pre_check_already_compressed(original)
    checks["entity_preservation"] = self.check_entity_preservation(original, compressed)
    checks["minimal_benefit"] = self.check_minimal_benefit(original, compressed)
    checks["semantic_similarity"] = self.check_semantic_similarity(original, compressed)
    
    # Collect failures
    for check_name, result in checks.items():
        if not result["passed"]:
            failures.append({
                "check": check_name,
                "message": result["message"]
            })
    
    # Determine recommendation
    if not checks["pre_check"]["passed"]:
        recommendation = "refuse"  # Already compressed
    elif len(failures) == 0:
        recommendation = "accept"  # All checks passed
    elif len(failures) <= 1:
        recommendation = "warn"  # One check failed, might be acceptable
    else:
        recommendation = "refuse"  # Multiple failures
    
    safe = (recommendation == "accept")
    
    return {
        "safe": safe,
        "checks": checks,
        "failures": failures,
        "recommendation": recommendation,
        "summary": self._generate_summary(checks, failures)
    }

def _generate_summary(self, checks, failures):
    """Generate human-readable summary."""
    if len(failures) == 0:
        return "All safety checks passed. Compression is safe."
    else:
        failed_checks = [f["check"] for f in failures]
        return f"Safety concerns: {', '.join(failed_checks)}"
```

---

## Test Cases

### Test 1: Perfect Compression (All Checks Pass)

**Input**:
- Original: Verbose documentation (1000 tokens)
- Compressed: Well-compressed (500 tokens, 50% reduction)
- All entities preserved
- Semantic similarity: 0.85

**Expected**:
- All checks PASS
- Recommendation: "accept"
- Safe: True

---

### Test 2: Already Compressed (Pre-check Fails)

**Input**:
- Original: Highly compressed (score 0.82)

**Expected**:
- Pre-check FAIL
- Other checks not run
- Recommendation: "refuse"
- Message: "Content already compressed"

---

### Test 3: Entity Loss (Post-check Fails)

**Input**:
- Original: API docs with 20 entities
- Compressed: Lost 5 entities (75% preserved)

**Expected**:
- Entity preservation FAIL
- Recommendation: "refuse"
- Lost entities listed

---

### Test 4: Minimal Benefit (Post-check Fails)

**Input**:
- Original: 1000 tokens
- Compressed: 920 tokens (8% reduction)

**Expected**:
- Minimal benefit FAIL
- Recommendation: "refuse"
- Message: "Only 8% reduction - risk vs benefit too high"

---

### Test 5: Semantic Drift (Post-check Fails)

**Input**:
- Original: "Authentication requires username and password"
- Compressed: "Auth needs credentials" (meaning oversimplified)
- Semantic similarity: 0.65

**Expected**:
- Semantic similarity FAIL
- Recommendation: "refuse"
- Message: "Meaning significantly changed"

---

### Test 6: Single Warning (Warn Recommendation)

**Input**:
- Compression ratio: 0.86 (just above threshold)
- All other checks pass

**Expected**:
- Minimal benefit FAIL
- Other checks PASS
- Recommendation: "warn" (not "refuse")
- User can override with caution

---

## Required Libraries

```bash
pip install spacy sentence-transformers scikit-learn --break-system-packages
python -m spacy download en_core_web_sm
```

**Note**: sentence-transformers may take time to download model on first use

---

## Project Structure

```
/Users/dudley/Projects/Compression/
├── scripts/
│   ├── compression_score.py         # From Task 2.1
│   ├── detect_token_drift.py        # From Task 1.2
│   ├── mock_compressor.py           # From Task 2.2
│   ├── analyze_compression_state.py # From Task 1.1
│   └── safety_checks.py             # New: comprehensive safety
├── tests/
│   ├── test_safety_checks.py        # New: safety test suite
│   └── fixtures/
│       ├── perfect_compression.md
│       ├── entity_loss_example.md
│       ├── minimal_benefit_example.md
│       └── semantic_drift_example.md
├── checkpoints/
│   ├── checkpoint_1_safety_tests.md
│   ├── checkpoint_2_safety_impl.md
│   └── checkpoint_3_safety_validated.md
└── validation_report_task_2.3.md
```

---

## Test Template

```python
import pytest
from scripts.safety_checks import SafetyValidator

class TestSafetyChecks:
    """Comprehensive safety validation test suite."""
    
    @pytest.fixture
    def validator(self):
        return SafetyValidator()
    
    def test_pre_check_already_compressed(self, validator):
        """Pre-check refuses already-compressed content."""
        pass
    
    def test_entity_preservation_pass(self, validator):
        """All entities preserved → PASS."""
        pass
    
    def test_entity_preservation_fail(self, validator):
        """< 80% entities preserved → FAIL."""
        pass
    
    def test_minimal_benefit_pass(self, validator):
        """Good compression (>15% reduction) → PASS."""
        pass
    
    def test_minimal_benefit_fail(self, validator):
        """Poor compression (<15% reduction) → FAIL."""
        pass
    
    def test_semantic_similarity_pass(self, validator):
        """Meaning preserved (≥0.75 similarity) → PASS."""
        pass
    
    def test_semantic_similarity_fail(self, validator):
        """Meaning changed (<0.75 similarity) → FAIL."""
        pass
    
    def test_perfect_compression(self, validator):
        """All checks pass → accept."""
        pass
    
    def test_multiple_failures(self, validator):
        """Multiple failures → refuse."""
        pass
    
    def test_single_warning(self, validator):
        """One check fails → warn."""
        pass
    
    def test_integration_with_previous_tasks(self, validator):
        """Verify integration with compression_score, etc."""
        pass
```

---

## Validation Report Template

```markdown
# Validation Report: Safety Checks Implementation (Task 2.3)

**Date**: [YYYY-MM-DD]
**Task**: TASK-2.3-SAFETY-CHECKS
**Status**: [PASS/FAIL]

## Summary

[Overview of validation results]

## Individual Check Results

### Pre-Check (Already Compressed)
- Test cases: [X/X] passed
- False positives: [count]
- False negatives: [count]

### Entity Preservation
- Test cases: [X/X] passed
- Entity detection accuracy: [percentage]
- Technical entity recognition: [evaluation]

### Minimal Benefit Detection
- Test cases: [X/X] passed
- Threshold appropriateness: [evaluation]

### Semantic Similarity
- Test cases: [X/X] passed
- Model performance: [evaluation]
- Similarity threshold: [evaluation]

## Integration Testing

| Scenario | Pre-check | Entity | Benefit | Semantic | Recommendation | Expected | Result |
|----------|-----------|--------|---------|----------|----------------|----------|--------|
| Perfect | PASS | PASS | PASS | PASS | accept | accept | ✓ |
| Already compressed | FAIL | - | - | - | refuse | refuse | ✓ |
| Entity loss | PASS | FAIL | PASS | PASS | refuse | refuse | ✓ |
| Minimal benefit | PASS | PASS | FAIL | PASS | warn | warn | ✓ |
| Semantic drift | PASS | PASS | PASS | FAIL | refuse | refuse | ✓ |

## Real-World Testing

Tested on actual compression scenarios:

- API documentation compression: [result]
- Tutorial simplification: [result]
- Technical reference compression: [result]

## Performance

- Average validation time: [X] ms per document
- Memory usage: [X] MB
- Model load time: [X] seconds (first use)

## False Positive/Negative Analysis

**False Positives** (incorrectly refused safe compressions):
- [Count and examples]

**False Negatives** (incorrectly accepted unsafe compressions):
- [Count and examples]

## Threshold Tuning Recommendations

[Suggestions for adjusting thresholds based on results]

## Conclusions

- [x] All safety checks implemented and working
- [x] Integration framework operates correctly
- [x] No false negatives detected (critical)
- [x] False positive rate acceptable
- [x] Production-ready safety system

## Success Criteria Met

- [x] Each safety check triggers appropriately
- [x] Clear error messages explain failures
- [x] No false positives rejecting good compressions
- [x] No false negatives accepting bad compressions

**Overall Status**: PASS
```

---

## Success Criteria

### Must Pass (Critical)
- ✓ All four safety checks implemented and working
- ✓ Integration framework operates correctly
- ✓ Zero false negatives (never accept unsafe compression)
- ✓ Clear, actionable error messages

### Should Pass (Important)
- ✓ False positive rate < 5%
- ✓ Performance acceptable (< 1 second per validation)
- ✓ Works on real project documentation

### Nice to Have (Optional)
- Configurable thresholds
- Detailed logging
- Visual reports
- Performance optimization

---

## Final Deliverables

1. `scripts/safety_checks.py` - Complete safety framework
2. `tests/test_safety_checks.py` - Comprehensive test suite
3. `tests/fixtures/` - Test documents (4+ examples)
4. `checkpoints/checkpoint_1_safety_tests.md`
5. `checkpoints/checkpoint_2_safety_impl.md`
6. `checkpoints/checkpoint_3_safety_validated.md`
7. `validation_report_task_2.3.md` - Final validation report

---

## Sequential Task Dependencies

**This task requires**:
- TASK-2.1: compression_score.py (for pre-check)
- TASK-2.2: mock_compressor.py (for integration testing)
- TASK-1.1: analyze_compression_state.py (optional, for section-level safety)

**This task completes**:
- MVP validation (all critical safety proven)
- Production-ready safety framework
- Foundation for full tool development

**This enables**:
- Confidence in production deployment
- Full automation tool implementation
- Real-world compression operations

---

## Notes

### Critical Importance

This is the **most important validation task**. Without comprehensive safety checks:
- Information could be lost
- Users lose trust
- Tool becomes liability rather than asset

**Safety-first philosophy**: Better to refuse a safe compression than accept an unsafe one.

### Design Decisions

- **0.80 entity preservation**: Industry standard for information fidelity
- **0.85 compression ratio**: Below 15% reduction, risk exceeds benefit
- **0.75 semantic similarity**: Allows stylistic changes while preserving meaning
- **Warn vs Refuse**: Single failure = warn (user can override), multiple = refuse

### Open Questions

**Will be answered through validation**:
- Are thresholds appropriate across document types?
- Is spaCy NER sufficient for technical content?
- Does sentence-transformers perform well on technical docs?
- Should thresholds be configurable per document type?

### Future Enhancements

- Per-document-type threshold configuration
- More sophisticated entity recognition (domain-specific)
- Better semantic similarity models (technical domain)
- User override system with warnings
- Detailed logging and audit trail

---

**Working Directory**: /Users/dudley/Projects/Compression  
**Created**: 2025-10-30  
**Depends on**: Task 2.1, Task 2.2, Task 1.1 completion  
**Final Phase 3 task**: Completes MVP validation
