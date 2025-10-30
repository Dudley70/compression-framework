# Automation Tool Validation Plan

**Created**: 2025-10-30
**Purpose**: Structured validation plan for compression automation tool design questions
**Status**: Planning phase - validation tasks defined
**Context**: Session 7 pivot from white paper to tool development after discovering superior implementation approach

---

## Executive Summary

Session 7 initially planned to develop white paper but pivoted after extensive research revealed a practical implementation path: compression automation tool wrapped as Claude Code skill. Three critical design questions emerged requiring validation before implementation. This plan structures the validation work into testable tasks.

**Core Insight**: Claude already has full project context during sessions. Tool becomes compression execution + validation, not classification. Natural workflow: "Review our docs and suggest compressions."

---

## Design Questions Requiring Validation

### Question 1: Mixed Compression State Handling

**Problem**: Document written → compressed → more uncompressed content added. How to track partial compression state?

**Challenge**:
```markdown
---
compression:
  applied: true
  date: 2025-10-30
  ratio: 0.67
---

# API Reference

## Authentication (COMPRESSED)
- Endpoint: `/auth`
- Methods: POST

## New Section (UNCOMPRESSED - just added)
This is a detailed explanation of the new authentication flow
that was added after compression. It has full prose, examples...
```

Header says "compressed" but document is now mixed state.

**Proposed Solutions**:
- **Option A**: Section-level markers (fine-grained but cluttered)
- **Option B**: Separate source/compressed files (sync problem)
- **Option C**: Header as "last full compression" + content analysis (smart detection)
- **Option D**: Token drift detection (simple metric)
- **Recommended**: C + D hybrid

**Validation Tasks**: See Section "Validation Task 1" below

---

### Question 2: Critical Data Protection

**Problem**: Compressed content is already information-dense. Further compression risks information loss.

**Hypothesis**: Already-compressed content has measurable characteristics:
- High list/table density (σ high)
- Short sentences, minimal prose (γ low)  
- No redundant explanations (κ low)
- Low redundancy, high entropy
- Technical vocabulary concentration

**Proposed Solution**: Compression score (0.0-1.0) measuring current density. Refuse compression when score ≥ 0.8.

**Safety Checks**:
- Entity preservation threshold (≥80%)
- Minimal benefit detection (compression ratio > 0.85 on already-dense content)
- Compression potential calculation

**Validation Tasks**: See Section "Validation Task 2" below

---

### Question 3: Proactive Style Optimization

**Problem**: Current workflow is reactive (write verbose → compress later). Could we write in target style from the start?

**Proposed Workflow**:
```
Declare doc type in header → Write in appropriate style → No compression needed
```

**Implementation Approach**:
- Add `target_style` to document headers
- Add `writing_guide` with style rules
- Claude adapts writing style based on doc type
- Real-time style feedback tool
- Most docs never need compression

**Example**:
```markdown
---
doc_type: API_REFERENCE
audience: LLM-only
target_style: {σ: 0.8, γ: 0.6, κ: 0.2}
writing_guide: |
  ✓ Use lists and tables (high structure)
  ✓ Keep sentences short and direct
  ✗ Avoid prose paragraphs
  ✗ Skip explanatory context
---
```

**Validation Tasks**: See Section "Validation Task 3" below

---

## Validation Task 1: Mixed Compression State Detection

**Objective**: Prove we can detect and handle documents with mixed compression states

### Task 1.1: Build Content Density Analyzer

**What to Build**:
```python
def calculate_compression_score(text_section):
    """
    Score 0.0-1.0 indicating compression level of text section.
    Returns metrics showing why score was assigned.
    """
    pass

def analyze_document_sections(document):
    """
    Split document into sections, score each section.
    Returns: list of (section_name, score, metrics)
    """
    pass
```

**Test Cases**:
1. Fully uncompressed document → all sections score < 0.3
2. Fully compressed document → all sections score > 0.7
3. Mixed document → some sections < 0.3, others > 0.7
4. Incrementally compressed → gradual score increase

**Validation Criteria**:
- ✓ Can distinguish compressed vs uncompressed sections
- ✓ Scores correlate with manual assessment
- ✓ Can identify which specific sections need compression

**Deliverable**: `scripts/analyze_compression_state.py` with test suite

---

### Task 1.2: Test Token Drift Detection

**What to Build**:
```python
def check_token_drift(document):
    """
    Compare current token count vs baseline in header.
    Returns drift ratio and recommendation.
    """
    pass
```

**Test Cases**:
1. No changes after compression → drift ratio ≈ 1.0
2. Minor edits (5% growth) → drift ratio 1.05, no action needed
3. New section added (25% growth) → drift ratio 1.25, flag for review
4. Substantial new content (50% growth) → drift ratio 1.50, recommend compression

**Validation Criteria**:
- ✓ Accurately calculates drift
- ✓ Appropriate thresholds (1.15 = flag, 1.30 = recommend)
- ✓ Useful actionable recommendations

**Deliverable**: `scripts/detect_token_drift.py` with test suite

---

### Task 1.3: Integrated Mixed State Handler

**What to Build**:
Integration of 1.1 + 1.2 into comprehensive state detection:

```python
def analyze_compression_state(document):
    """
    Comprehensive analysis combining section scoring + token drift.
    Returns state classification and recommendations.
    """
    pass
```

**Test Cases**:
1. Clean compressed doc → state: 'compressed', action: 'none'
2. Uncompressed doc → state: 'uncompressed', action: 'compress'
3. Mixed doc (2 compressed, 1 new) → state: 'mixed', action: 'compress_sections'
4. Edited compressed doc (<15% drift) → state: 'compressed_edited', action: 'review'

**Validation Criteria**:
- ✓ Correct state classification in all test cases
- ✓ Actionable recommendations
- ✓ No false positives (claiming compressed when not)
- ✓ No false negatives (missing uncompressed content)

**Deliverable**: Comprehensive state detection with test suite demonstrating accuracy

**Decision Point**: If validation succeeds → adopt Option C+D hybrid. If fails → fallback to simpler Option D only.

---

## Validation Task 2: Critical Data Protection

**Objective**: Prove we can detect already-compressed content and refuse further compression

### Task 2.1: Compression Score Algorithm

**What to Build**:
```python
def calculate_compression_score(text):
    """
    Calculate 0.0-1.0 score indicating compression level.
    
    Metrics:
    - list_density: ratio of list items to total tokens
    - prose_ratio: ratio of paragraph tokens to total
    - avg_sentence_length: words per sentence
    - redundancy: repeated phrase detection
    - explanation_markers: count of scaffolding phrases
    - information_entropy: Shannon entropy
    
    Returns score + detailed metrics breakdown
    """
    pass
```

**Test Cases**:
Create test documents with known compression characteristics:

1. **Verbose technical doc** (score should be 0.2-0.3):
   - Long paragraphs with explanations
   - Examples with commentary
   - Repetitive phrasing
   - Low information density

2. **Moderately compressed doc** (score should be 0.5-0.6):
   - Mix of lists and prose
   - Some explanations removed
   - Moderate information density

3. **Highly compressed doc** (score should be 0.8-0.9):
   - Predominantly lists/tables
   - Minimal prose
   - No redundancy
   - High information density
   - Technical vocabulary concentration

**Validation Criteria**:
- ✓ Scores match expected ranges for test documents
- ✓ Metrics correlate with manual compression assessment
- ✓ Can explain score (which metrics contributed)
- ✓ Consistent across multiple runs (deterministic)

**Deliverable**: `scripts/compression_score.py` with test documents and validation report

---

### Task 2.2: Round-Trip Compression Test

**What to Build**:
```python
def test_idempotency():
    """
    Test that compressing already-compressed content is correctly refused.
    """
    pass
```

**Test Procedure**:
1. Take verbose document (score 0.2)
2. Compress to target (σ=0.8, γ=0.6, κ=0.2)
3. Measure result score (should be 0.7-0.8)
4. Attempt second compression with same parameters
5. **Expected**: Tool refuses (score already ≥ 0.8)
6. Attempt third compression with aggressive parameters (σ=0.9, γ=0.4, κ=0.1)
7. **Expected**: Tool warns or refuses (minimal benefit, risk of information loss)

**Validation Criteria**:
- ✓ First compression succeeds with expected score increase
- ✓ Second compression correctly refused
- ✓ Refusal message is clear and actionable
- ✓ No information loss in first compression (entity preservation ≥80%)

**Deliverable**: Test suite demonstrating idempotency with pass/fail report

---

### Task 2.3: Safety Checks Implementation

**What to Build**:
```python
def compress_with_safety_checks(text, sigma, gamma, kappa):
    """
    Compress with multiple safety gates:
    - Pre-check: Refuse if already compressed (score ≥ 0.8)
    - Post-check: Validate entity preservation ≥ 80%
    - Post-check: Validate minimal benefit threshold
    - Post-check: Validate semantic similarity ≥ 0.75
    """
    pass
```

**Test Cases**:
1. **Already compressed**: Pre-check refuses
2. **Entity loss**: Post-check rejects (e.g., compression drops API names)
3. **Minimal benefit**: Compression achieves only 5% reduction → rejected
4. **Semantic drift**: Meaning significantly changed → rejected
5. **Success case**: All checks pass, compression applied

**Validation Criteria**:
- ✓ Each safety check triggers appropriately
- ✓ Clear error messages explain why rejected
- ✓ No false positives (rejecting good compressions)
- ✓ No false negatives (accepting bad compressions)

**Deliverable**: Safety check implementation with comprehensive test suite

**Decision Point**: If validation succeeds → proceed with safety-first architecture. If entity preservation check proves unreliable → investigate alternative validation metrics.

---

## Validation Task 3: Proactive Style Optimization

**Objective**: Prove Claude can write in target style from the start, eliminating need for compression

### Task 3.1: Style Analysis Baseline

**What to Build**:
```python
def calculate_current_style(text):
    """
    Analyze text to extract (σ, γ, κ) characteristics.
    Returns current style parameters.
    """
    pass

def compare_to_target(current_style, target_style):
    """
    Compare current vs target, provide specific feedback.
    """
    pass
```

**Test Documents**:
Create same content in different styles:

1. **API Reference - Verbose**:
   ```markdown
   The authentication endpoint is available at /auth and accepts POST requests.
   When you want to authenticate, you need to send a JSON body that contains
   both a username and password field. The API will validate these credentials
   and return a token if successful...
   ```
   Expected: σ=0.3, γ=0.8, κ=0.7 (needs compression)

2. **API Reference - Target Style**:
   ```markdown
   ## POST /auth
   - Body: `{username: string, password: string}`
   - Returns: `{token: string}` (200) or error (401)
   ```
   Expected: σ=0.8, γ=0.6, κ=0.2 (already optimized)

**Validation Criteria**:
- ✓ Style parameters accurately reflect writing style
- ✓ Verbose version shows clear deviation from target
- ✓ Target-style version matches or exceeds target parameters
- ✓ Comparison provides actionable feedback

**Deliverable**: Style analysis tool with test document examples

---

### Task 3.2: Document Header Specification

**What to Create**:
Formal specification for document headers with all metadata:

```markdown
---
# Document Classification
doc_type: [API_REFERENCE | TUTORIAL | SESSION_HANDOVER | PROJECT_CONTEXT | ...]
audience: [LLM-only | Human-technical | Multi-role | ...]
layer: [Session | Strategic | Control | Operational | Archive]
phase: [Active | Complete | Archived]
purpose: [Execution | Learning | Reference | Audit | ...]

# Style Guidance
target_style:
  sigma: 0.8      # Structure density
  gamma: 0.6      # Semantic granularity
  kappa: 0.2      # Contextual scaffolding

writing_guide: |
  ✓ Preferred patterns for this doc type
  ✗ Anti-patterns to avoid

# Compression Tracking (if applicable)
compression:
  last_full_compression: 2025-10-30 15:30 AEDT
  baseline_tokens: 1400
  parameters: {σ: 0.8, γ: 0.6, κ: 0.2}
  validation:
    entity_preservation: 0.94
    semantic_similarity: 0.82
---
```

**Test Cases**:
1. Create headers for 5+ document types
2. Validate Claude can parse and understand headers
3. Verify headers provide sufficient guidance

**Validation Criteria**:
- ✓ Headers are clear and unambiguous
- ✓ All necessary metadata included
- ✓ Easy to write/maintain
- ✓ Machine-readable and human-readable

**Deliverable**: `docs/reference/DOCUMENT_HEADER_SPECIFICATION.md` with examples for all major document types

---

### Task 3.3: Claude Skill Behavior Test

**What to Test**:
Can Claude naturally adapt writing style based on document headers?

**Test Procedure**:
1. Create document with header specifying API_REFERENCE style
2. Ask Claude to "Add a section on user endpoints"
3. Observe if Claude writes in target style (lists, minimal prose)
4. Analyze result (σ, γ, κ parameters)
5. Compare to target specified in header

**Test Cases**:
- API Reference (σ=0.8) → Claude uses lists/tables
- Tutorial (κ=0.7) → Claude includes explanations
- Session Handover (γ=0.7) → Claude uses structured sections

**Validation Criteria**:
- ✓ Claude's additions match target style ≥80% of time
- ✓ Style is maintained without explicit prompting
- ✓ Quality is not sacrificed (still accurate, complete)

**Deliverable**: Test report showing Claude's natural style adaptation across document types

**Decision Point**: If validation succeeds → proactive style is viable, most docs won't need compression. If fails → clarify that explicit style guidance needed in prompts.

---

## Implementation Dependencies

### Prerequisites
None of the validation tasks require implementation of the full tool. Each can be tested independently with simple scripts.

### Validation Order (Recommended)

**Week 1: Critical Data Protection** (Task 2)
- Most important: prevents information loss
- Foundational for all compression operations
- Clear pass/fail criteria

**Week 2: Mixed State Detection** (Task 1)
- Builds on compression score from Task 2
- Needed for practical tool operation
- More complex, depends on score algorithm

**Week 3: Proactive Style** (Task 3)
- Optional enhancement (not blocker)
- High value if successful (eliminates compression need)
- Least risk (doesn't affect core tool)

### Alternative: Parallel Validation

If resources available, Tasks 1-2 can run in parallel:
- Task 2.1 (compression score) required by Task 1.1
- Task 1.2 (token drift) independent
- Task 3 completely independent

---

## Success Criteria

### Minimum Viable Validation (MVP)

To proceed with tool implementation, must have:
- ✓ Task 2.1: Compression score algorithm working
- ✓ Task 2.2: Round-trip test passing
- ✓ Task 1.2: Token drift detection working

These three prove core safety and idempotency.

### Full Validation (Recommended)

For production-ready tool:
- ✓ All Task 2 deliverables (critical data protection)
- ✓ All Task 1 deliverables (mixed state handling)
- ✓ Task 3.2: Header specification

Task 3.1 and 3.3 (proactive style) can be deferred to post-v1.0.

---

## Open Questions for Future Sessions

### Questions Requiring Research

1. **Entity Preservation Reliability**: Is spaCy NER sufficient for technical content, or do we need domain-specific entity recognition?

2. **Semantic Similarity Thresholds**: Are our proposed thresholds (0.75 for similarity, 0.80 for entities) appropriate, or do they need empirical tuning?

3. **Compression Score Calibration**: Do the metric weights in compression_score need tuning based on document type?

4. **Section Boundary Detection**: How reliably can we split documents into sections for mixed-state analysis? Do we need minimum section length?

### Questions for User Decision

1. **Failure Mode Preference**: When compression would lose information, should tool:
   - Refuse compression (safe, may frustrate users)
   - Compress with warning (flexible, may cause issues)
   - Ask user (safest, requires interaction)

2. **Mixed State Resolution**: When document is partially compressed, should tool:
   - Default to "compress only uncompressed sections"
   - Default to "re-compress entire document"
   - Always ask user

3. **Header Management**: Who maintains document headers:
   - User manually writes/updates
   - Tool auto-generates/updates
   - Hybrid (user writes doc_type, tool tracks compression)

---

## Next Steps

### Immediate (This Session)
- [x] Document validation plan (this file)
- [ ] Update SESSION.md with Session 7 summary
- [ ] Update PROJECT.md with Decision #6 (tool development pivot)
- [ ] Create handover document

### Next Session Priority
Choose one path:

**Path A: Begin Validation** (Recommended)
- Start with Task 2.1 (compression score algorithm)
- Build test documents with known characteristics
- Validate score accuracy

**Path B: Finalize Planning**
- Refine validation criteria based on user feedback
- Clarify open questions
- Prioritize validation tasks

**Path C: Prototype Core Script**
- Build minimal compressor.py
- Test basic compression operations
- Defer validation temporarily

---

**Created**: 2025-10-30  
**Status**: Complete - ready for review  
**Next Action**: Update project documentation and create handover
