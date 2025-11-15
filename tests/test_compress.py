"""
test_compress.py - Comprehensive test suite for compress_v7_hybrid.py

Tests organized by checkpoint:
- Checkpoint 1: extract_sacred_content() tests
- Checkpoint 2: restore_sacred() and V7 rules round-trip tests
- Checkpoint 3: Full pipeline with validation
"""

import pytest
import re
from pathlib import Path

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from compress_v7_hybrid import (
    extract_sacred_content,
    restore_sacred,
    apply_abbreviations,
    apply_symbols,
    apply_prose_transforms,
    restore_and_transform,
    validate,
    count_prompts,
    extract_prompts,
)


# ============================================================================
# CHECKPOINT 1: Sacred Content Extraction Tests
# ============================================================================

class TestExtractSacredContent:
    """Tests for extract_sacred_content() function"""

    def test_empty_document(self):
        """Test extraction from empty document"""
        result = extract_sacred_content("")
        assert result['sacred_items'] == []
        assert result['modified_document'] == ""
        assert result['count']['prompts'] == 0
        assert result['count']['code_blocks'] == 0
        assert result['count']['formulas'] == 0

    def test_document_without_prompts(self):
        """Test extraction from document with no prompts"""
        doc = "This is a regular document without any prompts."
        result = extract_sacred_content(doc)
        assert result['sacred_items'] == []
        assert result['modified_document'] == doc
        assert result['count']['prompts'] == 0

    def test_single_prompt_extraction(self):
        """Test extraction of a single prompt"""
        doc = """
**Prompt:**
```
What is machine learning?
```
"""
        result = extract_sacred_content(doc)

        assert len(result['sacred_items']) == 1
        assert result['count']['prompts'] == 1

        item = result['sacred_items'][0]
        assert item['type'] == 'test_prompt'
        assert 'machine learning' in item['content'].lower()
        assert item['placeholder'] == '{{SACRED_TEST_PROMPT_0}}'

    def test_multiple_prompts_extraction(self):
        """Test extraction of multiple prompts"""
        doc = """
First prompt:
**Prompt:**
```
First question?
```

Some text in between.

Second prompt:
**Prompt:**
```
Second question?
```
"""
        result = extract_sacred_content(doc)

        assert len(result['sacred_items']) == 2
        assert result['count']['prompts'] == 2

        assert result['sacred_items'][0]['placeholder'] == '{{SACRED_TEST_PROMPT_0}}'
        assert result['sacred_items'][1]['placeholder'] == '{{SACRED_TEST_PROMPT_1}}'

    def test_prompt_with_multiline_content(self):
        """Test extraction of prompt with multiple lines"""
        doc = """
**Prompt:**
```
Line 1 of prompt
Line 2 of prompt
Line 3 of prompt
```
"""
        result = extract_sacred_content(doc)

        assert len(result['sacred_items']) == 1
        content = result['sacred_items'][0]['content']
        assert 'Line 1' in content
        assert 'Line 2' in content
        assert 'Line 3' in content

    def test_placeholder_replacement_in_document(self):
        """Test that placeholders replace prompts in modified document"""
        doc = """
**Prompt:**
```
Original question
```
"""
        result = extract_sacred_content(doc)

        # Should contain placeholder
        assert '{{SACRED_TEST_PROMPT_0}}' in result['modified_document']
        # Should NOT contain original content
        assert 'Original question' not in result['modified_document']

    def test_extraction_preserves_surrounding_content(self):
        """Test that surrounding content is preserved"""
        doc = """
Before prompt

**Prompt:**
```
Inside prompt
```

After prompt
"""
        result = extract_sacred_content(doc)

        assert 'Before prompt' in result['modified_document']
        assert 'After prompt' in result['modified_document']
        assert 'Inside prompt' not in result['modified_document']

    def test_eleven_prompts_extraction(self):
        """Test extraction of 11 prompts (expected from spec)"""
        # Build document with 11 prompts
        doc = ""
        for i in range(11):
            doc += f"""
**Prompt:**
```
Prompt number {i}
```

"""

        result = extract_sacred_content(doc)
        assert len(result['sacred_items']) == 11
        assert result['count']['prompts'] == 11

        # Verify all have correct placeholders
        for idx, item in enumerate(result['sacred_items']):
            assert item['placeholder'] == f'{{{{SACRED_TEST_PROMPT_{idx}}}}}'

    def test_code_block_extraction(self):
        """Test extraction of code blocks"""
        doc = """
Here is some code:
```python
def hello():
    print("world")
```
Some text after.
"""
        result = extract_sacred_content(doc)

        # Should extract code blocks
        assert len(result['sacred_items']) > 0
        assert result['count']['code_blocks'] > 0

    def test_formula_extraction(self):
        """Test extraction of LaTeX formulas"""
        doc = """
The formula is $E = mc^2$ and another $F = ma$.
"""
        result = extract_sacred_content(doc)

        # Should extract formulas
        assert len(result['sacred_items']) >= 2
        assert result['count']['formulas'] >= 2

    def test_prose_prompt_extraction(self):
        """Test extraction of prose prompts (not code-fenced)"""
        doc = """
Some introduction text.

**Prompt:**

This is a prose prompt that continues
across multiple lines without code fences.

#### Model Output

The output goes here.

**Prompt:**

Second prose prompt here.

**Output:**

Second output.
"""
        result = extract_sacred_content(doc)

        # Should extract 2 prose prompts
        assert result['count']['prompts'] == 2

        # Verify content is captured correctly
        prompt1 = result['sacred_items'][0]['content']
        assert 'This is a prose prompt' in prompt1
        assert 'across multiple lines' in prompt1

        prompt2 = result['sacred_items'][1]['content']
        assert 'Second prose prompt' in prompt2

    def test_mixed_prompt_formats(self):
        """Test extraction of both code-fenced and prose prompts"""
        doc = """
**Prompt:**
```
Code-fenced prompt content
```

Some text.

**Prompt:**

Prose prompt content here.

#### Next Section

More text.
"""
        result = extract_sacred_content(doc)

        # Should extract 2 prompts (one of each format)
        assert result['count']['prompts'] == 2

        # First should be code-fenced
        assert '```' in result['sacred_items'][0]['content']

        # Second should be prose
        assert 'Prose prompt content' in result['sacred_items'][1]['content']


# ============================================================================
# CHECKPOINT 2: Round-Trip Preservation Tests
# ============================================================================

class TestRoundTripPreservation:
    """Tests for round-trip preservation: Extract -> Restore"""

    def test_single_prompt_round_trip(self):
        """Test that single prompt survives extraction and restoration"""
        original = """
**Prompt:**
```
What is AI?
```
"""

        # Extract
        extraction = extract_sacred_content(original)

        # Restore
        restored = restore_sacred(extraction['modified_document'], extraction['sacred_items'])

        # Extract prompts from both
        original_prompts = extract_prompts(original)
        restored_prompts = extract_prompts(restored)

        assert original_prompts == restored_prompts

    def test_multiple_prompts_round_trip(self):
        """Test round-trip with multiple prompts"""
        original = """
**Prompt:**
```
First question
```

Text between

**Prompt:**
```
Second question
```
"""

        extraction = extract_sacred_content(original)
        restored = restore_sacred(extraction['modified_document'], extraction['sacred_items'])

        original_prompts = extract_prompts(original)
        restored_prompts = extract_prompts(restored)

        assert original_prompts == restored_prompts
        assert len(original_prompts) == 2

    def test_round_trip_byte_for_byte_preservation(self):
        """Test exact byte-for-byte preservation of prompts"""
        original_prompt = "This is an exact prompt with special chars: !@#$%^&*()"
        doc = f"""
**Prompt:**
```
{original_prompt}
```
"""

        extraction = extract_sacred_content(doc)
        restored = restore_sacred(extraction['modified_document'], extraction['sacred_items'])

        restored_prompts = extract_prompts(restored)

        assert len(restored_prompts) == 1
        assert original_prompt == restored_prompts[0]

    def test_round_trip_with_multiline_content(self):
        """Test round-trip preserves multiline prompt content"""
        multiline_prompt = """Line 1
Line 2
Line 3
Line 4"""

        doc = f"""
**Prompt:**
```
{multiline_prompt}
```
"""

        extraction = extract_sacred_content(doc)
        restored = restore_sacred(extraction['modified_document'], extraction['sacred_items'])

        restored_prompts = extract_prompts(restored)

        restored_content = restored_prompts[0]
        assert 'Line 1' in restored_content
        assert 'Line 4' in restored_content

    def test_eleven_prompts_round_trip(self):
        """Test round-trip with 11 prompts"""
        # Build document with 11 unique prompts
        original_prompts = [f"Prompt number {i} with content" for i in range(11)]
        doc = ""
        for prompt in original_prompts:
            doc += f"""
**Prompt:**
```
{prompt}
```

"""

        extraction = extract_sacred_content(doc)
        restored = restore_sacred(extraction['modified_document'], extraction['sacred_items'])

        restored_prompts = extract_prompts(restored)

        assert len(restored_prompts) == 11
        for original, restored_prompt in zip(original_prompts, restored_prompts):
            assert original == restored_prompt


# ============================================================================
# V7 RULES APPLICATION TESTS
# ============================================================================

class TestV7RulesApplication:
    """Tests for V7 transformation rules"""

    def test_definition_abbreviation(self):
        """Test **Definition:** -> **Def:**"""
        text = "**Definition:** This is a definition"
        result = apply_abbreviations(text)
        assert '**Def:**' in result
        assert '**Definition:**' not in result

    def test_documentation_abbreviation(self):
        """Test **Documentation:** -> **Doc:**"""
        text = "**Documentation:** This is documentation"
        result = apply_abbreviations(text)
        assert '**Doc:**' in result

    def test_effectiveness_abbreviation(self):
        """Test Effectiveness -> E"""
        text = "The Effectiveness of this method is high"
        result = apply_abbreviations(text)
        assert ' E ' in result or 'E of' in result

    def test_reliability_abbreviation(self):
        """Test Reliability -> R"""
        text = "Reliability is important"
        result = apply_abbreviations(text)
        assert ' R ' in result or 'R is' in result

    def test_status_symbols(self):
        """Test status symbol replacements"""
        text = "Test passed successfully but another failed"
        result = apply_symbols(text)
        assert '✓' in result
        assert '✗' in result

    def test_comparison_symbols(self):
        """Test comparison symbol replacements"""
        text = "This leads to better results"
        result = apply_symbols(text)
        assert '→' in result

    def test_multiple_rules_applied(self):
        """Test multiple rules applied in same document"""
        text = """
**Definition:** Something passed the test.
Effectiveness and Reliability are key.
This leads to results.
"""
        result = apply_abbreviations(text)
        result = apply_symbols(result)

        assert '**Def:**' in result
        assert '✓' in result
        assert '→' in result

    def test_prose_fragment_rules(self):
        """Test prose fragment transformations"""
        text = "The model performs well. It successfully completes tasks."
        result = apply_prose_transforms(text)
        # Should remove "The model " and "successfully "
        assert 'The model ' not in result or result.index('performs') < result.index('The model')


# ============================================================================
# VALIDATION TESTS
# ============================================================================

class TestValidation:
    """Tests for validate() function"""

    def test_validation_identical_documents(self):
        """Test validation when original and final are identical"""
        doc = """
**Prompt:**
```
Test prompt
```
"""

        report = validate(doc, doc, expected_prompts=1)

        assert report['checks'][1]['pass']  # prompts_verbatim
        assert report['overall_pass']
        assert report['summary']['rule_6_compliance']
        assert 'PASS' in report['summary']['verdict']

    def test_validation_different_prompt_counts(self):
        """Test validation detects missing prompts"""
        original = """
**Prompt:**
```
Prompt 1
```
**Prompt:**
```
Prompt 2
```
"""

        final = """
**Prompt:**
```
Prompt 1
```
"""

        report = validate(original, final, expected_prompts=2)

        assert not report['checks'][0]['pass']  # prompt_count
        assert not report['overall_pass']
        assert report['checks'][0]['original_had'] == 2
        assert report['checks'][0]['final_has'] == 1

    def test_validation_size_reporting(self):
        """Test that validation correctly reports output size"""
        # Create document of specific size
        doc = "x" * 21000  # ~21KB

        report = validate(doc, doc, expected_prompts=0)

        assert report['checks'][2]['size_kb'] > 20

    def test_validation_report_structure(self):
        """Test validation report has correct structure"""
        doc = """
**Prompt:**
```
Test
```
"""

        report = validate(doc, doc, expected_prompts=1)

        # Check all required attributes
        assert 'timestamp' in report
        assert 'checks' in report
        assert 'overall_pass' in report
        assert 'summary' in report

        # Check summary structure
        assert 'rule_6_compliance' in report['summary']
        assert 'size_acceptable' in report['summary']
        assert 'structure_valid' in report['summary']
        assert 'verdict' in report['summary']

    def test_validation_prompt_comparison(self):
        """Test that validation includes detailed prompt comparison"""
        original = """
**Prompt:**
```
Prompt 1
```
**Prompt:**
```
Prompt 2
```
"""

        final = """
**Prompt:**
```
Prompt 1
```
**Prompt:**
```
Prompt 2
```
"""

        report = validate(original, final, expected_prompts=2)

        verbatim_check = report['checks'][1]
        assert verbatim_check['check'] == 'prompt_verbatim'
        assert 'details' in verbatim_check
        assert len(verbatim_check['details']) >= 2


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests for the full pipeline"""

    def test_full_pipeline_without_llm(self):
        """Test full pipeline: Extract -> Restore -> Rules -> Validate"""
        original_doc = """
**Prompt:**
```
What is machine learning?
```

This discusses machine learning concepts with Effectiveness metrics.

**Prompt:**
```
Define deep learning.
```
"""

        # Step 1: Extract
        extraction = extract_sacred_content(original_doc)
        assert extraction['count']['prompts'] == 2

        # Step 3A: Restore (simulating no compression)
        restored = restore_sacred(extraction['modified_document'], extraction['sacred_items'])

        # Step 3B: Apply rules
        final = restore_and_transform(extraction['modified_document'], extraction)

        # Step 4: Validate
        report = validate(original_doc, final, expected_prompts=2)
        assert report['checks'][1]['pass']  # prompts_verbatim
        assert report['overall_pass']

    def test_extraction_modified_document_no_prompts(self):
        """Verify extraction removes prompts from modified document"""
        doc = """
**Prompt:**
```
Original prompt
```
"""

        extraction = extract_sacred_content(doc)

        # Modified document should not contain original prompt
        assert 'Original prompt' not in extraction['modified_document']
        # But should contain placeholder
        assert '{{SACRED_TEST_PROMPT_0}}' in extraction['modified_document']

    def test_restore_and_transform_integration(self):
        """Test restore_and_transform applies both restoration and V7 rules"""
        doc = """
**Definition:** Machine learning
**Prompt:**
```
Test prompt
```
Effectiveness is high. Test passed.
"""

        extraction = extract_sacred_content(doc)
        final = restore_and_transform(extraction['modified_document'], extraction)

        # Should have restored prompt
        assert 'Test prompt' in final

        # Should have applied V7 rules
        assert '**Def:**' in final
        assert 'E is' in final or 'E ' in final  # Effectiveness -> E
        assert '✓' in final  # passed -> ✓

    def test_count_prompts_utility(self):
        """Test count_prompts utility function"""
        doc = """
**Prompt:**
```
First
```
**Prompt:**
```
Second
```
**Prompt:**
```
Third
```
"""
        count = count_prompts(doc)
        assert count == 3

    def test_extract_prompts_utility(self):
        """Test extract_prompts utility function"""
        doc = """
**Prompt:**
```
First prompt
```
**Prompt:**
```
Second prompt
```
"""
        prompts = extract_prompts(doc)
        assert len(prompts) == 2
        assert 'First prompt' == prompts[0]
        assert 'Second prompt' == prompts[1]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
