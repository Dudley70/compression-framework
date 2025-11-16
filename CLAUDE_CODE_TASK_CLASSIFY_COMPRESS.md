# Claude Code Task: Classify-Then-Compress Architecture

**Date**: 2025-11-16  
**Task Type**: Architecture Refactor + TDD Implementation  
**Complexity**: High  
**Estimated Time**: 3-4 hours

---

## PROBLEM STATEMENT

**Current Issue:**
The hybrid compression tool (compress_v7_hybrid.py) has a critical reliability problem:
- LLM simultaneously classifies AND compresses content
- Non-deterministic behavior: Same doc + same model = different results
- Latest run: 15/22 placeholders preserved (7 formulas lost)
- Session 29 run: 22/22 placeholders preserved
- **Root cause**: LLM can't be trusted to preserve content during compression

**Architecture Flaw:**
```
Current: LLM does classification + compression in one step
→ Unreliable, non-deterministic, violates Rule 6 randomly

Needed: LLM does classification ONLY, Python does compression
→ Reliable, deterministic, Rule 6 guaranteed
```

---

## PROPOSED SOLUTION

### Two-Phase Architecture

**Phase 1: LLM Classification (Non-deterministic, but safe)**
```python
Input: Full document
LLM Task: Scan and tag each section with compression tier
Output: Structured classification map

Example:
[
  {"start": 0, "end": 500, "type": "executive_summary", "tier": "aggressive"},
  {"start": 501, "end": 1200, "type": "test_prompt", "tier": "sacred"},
  {"start": 1201, "end": 2000, "type": "analysis", "tier": "moderate"},
  ...
]
```

**Phase 2: Deterministic Python Compression**
```python
Input: Document + Classification map
Python Task: Apply tier-specific rules to each section
Output: Compressed document (100% deterministic)

Tiers:
- sacred: No compression (preserve verbatim)
- minimal: Apply header abbrev + symbols only
- moderate: Header + abbrev + symbols + prose fragments
- aggressive: All V7 rules
```

---

## IMPLEMENTATION REQUIREMENTS

### New Tool: compress_v7_classify.py

**Architecture:**
1. **extract_sacred()** - Same as current (regex-based, deterministic)
2. **classify_sections()** - NEW: LLM scans doc, returns classification JSON
3. **compress_by_tier()** - NEW: Python applies rules based on tier
4. **restore_sacred()** - Same as current
5. **validate()** - Enhanced validation

---

## TDD SPECIFICATION

### Checkpoint 1: Classification Phase (LLM)

**Test File**: `tests/test_classify.py`

**Test 1.1: Basic Classification**
```python
def test_classify_simple_document():
    """LLM should identify section types correctly."""
    doc = """
# Executive Summary
This document presents a systematic assessment...

## Test 1: Chain-of-Thought

**Prompt:**
A logistics manager has to move items...

## Analysis
The model executed the CoT prompt flawlessly...
"""
    
    result = classify_sections(doc, api_key=TEST_KEY)
    
    # Validate structure
    assert isinstance(result, list)
    assert len(result) == 3
    
    # Validate section 1 (executive summary)
    assert result[0]["type"] == "executive_summary"
    assert result[0]["tier"] == "aggressive"
    assert result[0]["start"] == 0
    assert "systematic assessment" in result[0]["content"]
    
    # Validate section 2 (test prompt)
    assert result[1]["type"] == "test_prompt"
    assert result[1]["tier"] == "sacred"
    assert "**Prompt:**" in result[1]["content"]
    
    # Validate section 3 (analysis)
    assert result[2]["type"] == "analysis"
    assert result[2]["tier"] == "moderate"
```

**Test 1.2: Real Document Classification**
```python
def test_classify_gemini_document():
    """LLM should classify Gemini assessment correctly."""
    doc = read_file("test_data/documents/gemini-self-assessment.md")
    
    result = classify_sections(doc, api_key=TEST_KEY)
    
    # Should identify all 11 test prompts
    prompts = [s for s in result if s["type"] == "test_prompt"]
    assert len(prompts) == 11
    
    # All prompts should be tier "sacred"
    assert all(p["tier"] == "sacred" for p in prompts)
    
    # Should identify executive summary
    summaries = [s for s in result if s["type"] == "executive_summary"]
    assert len(summaries) >= 1
    
    # Should identify analysis sections
    analyses = [s for s in result if s["type"] == "analysis"]
    assert len(analyses) >= 10
```

**Test 1.3: Edge Cases**
```python
def test_classify_mixed_content():
    """LLM should handle sections with mixed content types."""
    doc = """
## Test Section
This test is designed to assess the model's ability.

**Prompt:**
Calculate the result of 2 + 2.

**Analysis:**
The model correctly computed the answer as 4.
"""
    
    result = classify_sections(doc, api_key=TEST_KEY)
    
    # Should split into 3 sections
    assert len(result) == 3
    
    # Test description should be moderate tier
    assert result[0]["tier"] == "moderate"
    
    # Prompt should be sacred
    assert result[1]["tier"] == "sacred"
    assert result[1]["type"] == "test_prompt"
    
    # Analysis should be moderate
    assert result[2]["tier"] == "moderate"
```

**Validation Criteria for Checkpoint 1:**
- ✅ All 3 tests passing
- ✅ Classification JSON schema valid
- ✅ LLM correctly identifies section types
- ✅ All test prompts marked as "sacred"
- ✅ No compression happens in this phase

---

### Checkpoint 2: Deterministic Compression Phase (Python)

**Test File**: `tests/test_compress_tiers.py`

**Test 2.1: Tier 0 (Sacred) - No Compression**
```python
def test_compress_sacred_tier():
    """Sacred content should be preserved exactly."""
    section = {
        "type": "test_prompt",
        "tier": "sacred",
        "content": "**Prompt:**\nCalculate 2 + 2.\nShow your work."
    }
    
    result = compress_by_tier(section)
    
    # Should be identical
    assert result == section["content"]
    assert len(result) == len(section["content"])
```

**Test 2.2: Tier 1 (Minimal) - Header + Symbols Only**
```python
def test_compress_minimal_tier():
    """Minimal compression should apply headers + symbols only."""
    section = {
        "type": "technical_spec",
        "tier": "minimal",
        "content": "**Definition:** The system processes requests and returns results."
    }
    
    result = compress_by_tier(section)
    
    # Should abbreviate header
    assert "**Def:**" in result
    assert "**Definition:**" not in result
    
    # Should apply symbols
    assert " → " in result or "returns" in result
    
    # Should NOT remove prose
    assert "processes" in result or "process" in result
```

**Test 2.3: Tier 2 (Moderate) - All Rules Except Scaffolding**
```python
def test_compress_moderate_tier():
    """Moderate compression should apply most rules."""
    section = {
        "type": "analysis",
        "tier": "moderate",
        "content": """
The model executed the prompt successfully. 
The output was accurate and well-structured.
It demonstrated strong reasoning abilities.
"""
    }
    
    result = compress_by_tier(section)
    
    # Should remove prose fragments
    assert "The model" not in result or "Model" in result
    
    # Should compress but preserve meaning
    assert "executed" in result or "exec" in result
    assert "accurate" in result
    assert "reasoning" in result or "reason" in result
    
    # Should be shorter
    assert len(result) < len(section["content"]) * 0.7
```

**Test 2.4: Tier 3 (Aggressive) - All V7 Rules**
```python
def test_compress_aggressive_tier():
    """Aggressive compression should apply all V7 rules."""
    section = {
        "type": "executive_summary",
        "tier": "aggressive",
        "content": """
This report presents a systematic, evidence-based assessment 
of the Gemini 2.5 Pro large language model. The findings indicate 
that the model demonstrates exceptional effectiveness.
"""
    }
    
    result = compress_by_tier(section)
    
    # Should be heavily compressed
    assert len(result) < len(section["content"]) * 0.3
    
    # Should preserve key facts
    assert "Gemini" in result
    assert "2.5 Pro" in result or "2.5Pro" in result
    
    # Should remove scaffolding
    assert "This report presents" not in result
    assert "The findings indicate" not in result
```

**Test 2.5: Real Document Compression - Deterministic**
```python
def test_compress_gemini_deterministic():
    """Same classification should produce identical results."""
    doc = read_file("test_data/documents/gemini-self-assessment.md")
    
    # Classify once
    classification = classify_sections(doc, api_key=TEST_KEY)
    
    # Compress 3 times
    result1 = compress_from_classification(classification)
    result2 = compress_from_classification(classification)
    result3 = compress_from_classification(classification)
    
    # All results should be IDENTICAL
    assert result1 == result2 == result3
    
    # Verify Rule 6 compliance
    assert count_prompts(doc) == count_prompts(result1)
    assert all_prompts_verbatim(doc, result1)
```

**Validation Criteria for Checkpoint 2:**
- ✅ All 5 tests passing
- ✅ Sacred tier preserves content exactly
- ✅ Each tier applies correct rule subset
- ✅ Compression is 100% deterministic
- ✅ Rule 6 compliance guaranteed

---

### Checkpoint 3: Full Pipeline Integration

**Test File**: `tests/test_pipeline_full.py`

**Test 3.1: End-to-End Pipeline**
```python
def test_full_pipeline_gemini():
    """Complete pipeline on real Gemini document."""
    input_file = "test_data/documents/gemini-self-assessment.md"
    output_file = "test_data/results/gemini-classify-compress.md"
    report_file = "test_data/results/classify-validation-report.json"
    
    # Run compression
    result = compress_v7_classify(
        input_file,
        output_file,
        api_key=TEST_KEY,
        model="claude-haiku-4-5",
        expected_prompts=11,
        report=report_file
    )
    
    # Load report
    report = json.load(open(report_file))
    
    # Validation checks
    assert report["rule_6_compliant"] == True
    assert report["prompts_found"] == 11
    assert report["prompts_expected"] == 11
    assert report["prompts_match"] == True
    
    # Compression ratio should be good
    assert 0.75 <= report["compression_ratio"] <= 0.85
    
    # Output size should be in target range
    assert 19000 <= report["compressed_size"] <= 24000
```

**Test 3.2: Determinism Across Runs**
```python
def test_pipeline_determinism():
    """Multiple runs should produce identical output."""
    input_file = "test_data/documents/gemini-self-assessment.md"
    
    # Run 5 times
    results = []
    for i in range(5):
        output_file = f"test_data/results/run_{i}.md"
        compress_v7_classify(
            input_file,
            output_file,
            api_key=TEST_KEY,
            model="claude-haiku-4-5"
        )
        results.append(read_file(output_file))
    
    # Classification may vary (LLM), but compression should be consistent
    # Allow for small classification differences but check core preservation
    for result in results:
        # All should have exactly 11 prompts
        assert count_prompts(result) == 11
        
        # All prompts should be identical to original
        original = read_file(input_file)
        assert all_prompts_verbatim(original, result)
        
        # Size should be within 5% variance
        sizes = [len(r) for r in results]
        assert max(sizes) - min(sizes) < max(sizes) * 0.05
```

**Test 3.3: Performance Validation**
```python
def test_performance_requirements():
    """Pipeline should meet performance requirements."""
    import time
    
    input_file = "test_data/documents/gemini-self-assessment.md"
    output_file = "test_data/results/perf-test.md"
    
    start = time.time()
    compress_v7_classify(
        input_file,
        output_file,
        api_key=TEST_KEY,
        model="claude-haiku-4-5"
    )
    duration = time.time() - start
    
    # Should complete in under 60 seconds
    assert duration < 60
    
    # Report actual time
    print(f"Compression took {duration:.1f}s")
```

**Validation Criteria for Checkpoint 3:**
- ✅ All 3 tests passing
- ✅ Rule 6 compliance: 11/11 prompts preserved
- ✅ Compression ratio: 75-85%
- ✅ Output size: 19-24KB
- ✅ Performance: <60s
- ✅ Deterministic compression (classification may vary slightly)

---

## IMPLEMENTATION DETAILS

### Classification Prompt

```python
CLASSIFICATION_PROMPT = """
Analyze this technical document and classify each section.

Your task: Identify the TYPE and COMPRESSION TIER for each distinct section.

SECTION TYPES:
- executive_summary: Overview, abstract, introduction
- test_prompt: Prompts for testing (marked with **Prompt:** or in code fences)
- test_output: Model responses to prompts
- analysis: Technical analysis, findings, observations
- methodology: How tests were conducted
- scoring: Scores, ratings, evaluations
- documentation: Citations, references
- code_block: Code examples, schemas, configurations
- formula: Mathematical expressions (σ, γ, κ, equations)
- scaffolding: Transitions, meta-commentary, explanations

COMPRESSION TIERS:
- sacred: MUST preserve verbatim (test_prompt, code_block, formula)
- minimal: Light compression only (scoring, documentation)
- moderate: Medium compression (analysis, methodology)
- aggressive: Heavy compression (executive_summary, scaffolding)

CRITICAL RULES:
1. Anything marked **Prompt:** or **Test Prompt:** = tier "sacred"
2. Code fences (```) = tier "sacred"
3. Formulas (σ, γ, κ, math symbols) = tier "sacred"
4. Analysis with technical detail = tier "moderate"
5. Transitions, explanations = tier "aggressive"

OUTPUT FORMAT (JSON):
[
  {
    "start": <byte offset>,
    "end": <byte offset>,
    "type": "<section type>",
    "tier": "<compression tier>",
    "content": "<section text>"
  },
  ...
]

Document to classify:
{document}
"""
```

### Compression Functions

```python
def compress_by_tier(section: dict) -> str:
    """Apply tier-specific compression rules."""
    tier = section["tier"]
    content = section["content"]
    
    if tier == "sacred":
        # No compression
        return content
    
    elif tier == "minimal":
        # Header abbreviations + symbols only
        content = apply_abbreviations(content)
        content = apply_symbols(content)
        return content
    
    elif tier == "moderate":
        # Header + abbrev + symbols + prose fragments
        content = apply_abbreviations(content)
        content = apply_symbols(content)
        content = apply_prose_transforms(content)
        return content
    
    elif tier == "aggressive":
        # All V7 rules
        content = apply_abbreviations(content)
        content = apply_symbols(content)
        content = apply_prose_transforms(content)
        content = apply_scaffolding_removal(content)
        content = compress_whitespace(content)
        return content
    
    else:
        raise ValueError(f"Unknown tier: {tier}")
```

---

## VALIDATION ON REAL DOCUMENT

### Test Document

**File**: `test_data/documents/gemini-self-assessment.md`
- Size: 130.9KB
- Lines: 1,332
- Test Prompts: 11 (all must be preserved verbatim)
- Formulas: Multiple (σ, γ, κ symbols)

### Success Criteria

**Rule 6 Compliance (CRITICAL):**
- ✅ All 11 test prompts present
- ✅ All prompts byte-for-byte identical to original
- ✅ All formulas preserved exactly

**Compression Performance:**
- ✅ Target size: 19-24KB (75-85% reduction)
- ✅ All key findings preserved
- ✅ Document remains comprehensible

**Reliability:**
- ✅ Deterministic: Same classification = identical output
- ✅ No placeholder corruption
- ✅ No hallucinated success metrics

### Validation Script

```python
def validate_on_real_doc():
    """Full validation on Gemini document."""
    
    # Run compression
    compress_v7_classify(
        "test_data/documents/gemini-self-assessment.md",
        "test_data/results/gemini-classify-final.md",
        api_key=os.environ["ANTHROPIC_API_KEY"],
        model="claude-haiku-4-5",
        expected_prompts=11,
        report="test_data/results/final-validation.json"
    )
    
    # Load results
    original = read_file("test_data/documents/gemini-self-assessment.md")
    compressed = read_file("test_data/results/gemini-classify-final.md")
    report = json.load(open("test_data/results/final-validation.json"))
    
    # Print validation report
    print("\n" + "="*60)
    print("VALIDATION REPORT")
    print("="*60)
    print(f"Original size:    {len(original):,} bytes ({len(original)/1024:.1f}KB)")
    print(f"Compressed size:  {len(compressed):,} bytes ({len(compressed)/1024:.1f}KB)")
    print(f"Compression:      {report['compression_ratio']*100:.1f}%")
    print(f"\nRule 6 Compliance: {report['rule_6_compliant']}")
    print(f"Prompts expected:  {report['prompts_expected']}")
    print(f"Prompts found:     {report['prompts_found']}")
    print(f"Prompts match:     {report['prompts_match']}")
    print(f"\nTarget size:       19-24KB")
    print(f"Actual size:       {len(compressed)/1024:.1f}KB")
    print(f"Within target:     {19 <= len(compressed)/1024 <= 24}")
    print("="*60)
    
    # Assert all criteria met
    assert report["rule_6_compliant"] == True
    assert report["prompts_found"] == 11
    assert 19000 <= len(compressed) <= 24000
    
    print("\n✅ ALL VALIDATION CRITERIA MET")
```

---

## FILE STRUCTURE

```
/Users/dudley/Projects/Compression/
├── compress_v7_classify.py          # NEW: Main tool (classify-then-compress)
├── compress_v7_hybrid.py            # OLD: Keep for reference
├── tests/
│   ├── test_classify.py             # NEW: Checkpoint 1 tests
│   ├── test_compress_tiers.py       # NEW: Checkpoint 2 tests
│   ├── test_pipeline_full.py        # NEW: Checkpoint 3 tests
│   └── test_compress.py             # OLD: Keep for reference
├── test_data/
│   ├── documents/
│   │   └── gemini-self-assessment.md
│   └── results/                     # Gitignored outputs
└── validation_report.json
```

---

## EXECUTION INSTRUCTIONS FOR CLAUDE CODE

### Phase 1: Setup (5 minutes)

1. Read this entire specification
2. Read `compress_v7_hybrid.py` to understand V7 rules
3. Create test files structure
4. Verify test document exists

### Phase 2: Checkpoint 1 - Classification (1 hour)

1. Create `compress_v7_classify.py` skeleton
2. Implement `classify_sections()` function
3. Write tests in `tests/test_classify.py`
4. Run tests: `pytest tests/test_classify.py -v`
5. **STOP** - Report results before proceeding

### Phase 3: Checkpoint 2 - Compression (1.5 hours)

1. Implement `compress_by_tier()` function
2. Copy V7 rule functions from hybrid tool
3. Write tests in `tests/test_compress_tiers.py`
4. Run tests: `pytest tests/test_compress_tiers.py -v`
5. **STOP** - Report results before proceeding

### Phase 4: Checkpoint 3 - Integration (1 hour)

1. Implement full pipeline
2. Write integration tests in `tests/test_pipeline_full.py`
3. Run full test suite: `pytest tests/ -v`
4. Run validation on real document
5. **STOP** - Report final results

### Phase 5: Documentation (30 minutes)

1. Update tool docstrings
2. Create usage examples
3. Document known limitations
4. Commit all changes

---

## CRITICAL REQUIREMENTS

**DO:**
- ✅ Follow TDD: Write test first, then implementation
- ✅ Stop at each checkpoint for validation
- ✅ Use pytest for all testing
- ✅ Validate on real Gemini document
- ✅ Report all test failures immediately

**DO NOT:**
- ❌ Skip checkpoints
- ❌ Implement without tests
- ❌ Proceed if tests fail
- ❌ Trust LLM self-assessment (use programmatic validation)
- ❌ Modify test document

---

## SUCCESS CRITERIA

**Checkpoint 1:** All classification tests pass ✅  
**Checkpoint 2:** All compression tests pass ✅  
**Checkpoint 3:** All integration tests pass ✅  
**Final:** Real document validation passes ✅

**Overall:**
- 100% test coverage on critical paths
- Rule 6 compliance guaranteed (11/11 prompts)
- Deterministic compression verified
- 75-85% compression ratio achieved
- Production-ready code quality

---

## RECOVERY INSTRUCTIONS

If context is lost, resume by:

1. Read this specification file
2. Check git log to see what was completed
3. Run `pytest tests/ -v` to see current state
4. Continue from the last passing checkpoint

---

**Ready to start?** Begin with Checkpoint 1: Classification Phase.
