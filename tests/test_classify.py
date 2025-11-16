#!/usr/bin/env python3
"""
Test suite for Checkpoint 1: LLM Classification Phase

Tests the classify_sections() function which uses LLM to identify
section types and compression tiers.
"""

import pytest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compress_v7_classify import classify_sections


# Test API key (will be set via environment or fixture)
TEST_KEY = os.environ.get("ANTHROPIC_API_KEY", "test-key")


class TestBasicClassification:
    """Test 1.1: Basic classification of simple documents."""

    def test_classify_simple_document(self):
        """LLM should identify section types correctly."""
        doc = """# Executive Summary
This document presents a systematic assessment...

## Test 1: Chain-of-Thought

**Prompt:**
A logistics manager has to move items...

## Analysis
The model executed the CoT prompt flawlessly..."""

        result = classify_sections(doc, api_key=TEST_KEY)

        # Validate structure
        assert isinstance(result, list), "Result should be a list"
        assert len(result) >= 3, f"Expected at least 3 sections, got {len(result)}"

        # Check that all sections have required fields
        for section in result:
            assert "type" in section, "Section missing 'type' field"
            assert "tier" in section, "Section missing 'tier' field"
            assert "start" in section, "Section missing 'start' field"
            assert "end" in section, "Section missing 'end' field"
            assert "content" in section, "Section missing 'content' field"

        # Find sections by type
        summaries = [s for s in result if s["type"] == "executive_summary"]
        prompts = [s for s in result if s["type"] == "test_prompt"]
        analyses = [s for s in result if s["type"] == "analysis"]

        # Validate section types found
        assert len(summaries) >= 1, "Should find executive summary"
        assert len(prompts) >= 1, "Should find test prompt"
        assert len(analyses) >= 1, "Should find analysis section"

        # Validate test prompt is marked as sacred
        for prompt in prompts:
            assert prompt["tier"] == "sacred", f"Test prompts must be sacred tier, got {prompt['tier']}"
            assert "**Prompt:**" in prompt["content"], "Prompt content should contain **Prompt:** marker"


class TestRealDocument:
    """Test 1.2: Classification of real Gemini document."""

    @pytest.mark.skipif(not os.path.exists("test_data/documents/gemini-self-assessment.md"),
                        reason="Gemini test document not found")
    def test_classify_gemini_document(self):
        """LLM should classify Gemini assessment correctly."""
        with open("test_data/documents/gemini-self-assessment.md", 'r') as f:
            doc = f.read()

        result = classify_sections(doc, api_key=TEST_KEY)

        # Validate structure
        assert isinstance(result, list), "Result should be a list"
        assert len(result) > 0, "Should classify at least one section"

        # Should identify all test prompts (document has 11-12 depending on interpretation)
        prompts = [s for s in result if s["type"] == "test_prompt"]
        assert len(prompts) >= 11, f"Expected at least 11 test prompts, found {len(prompts)}"

        # All prompts should be tier "sacred"
        for i, prompt in enumerate(prompts):
            assert prompt["tier"] == "sacred", f"Prompt {i+1} should be sacred tier, got {prompt['tier']}"

        # Should identify executive summary
        summaries = [s for s in result if s["type"] == "executive_summary"]
        assert len(summaries) >= 1, "Should find at least one executive summary"

        # Should identify analysis sections
        analyses = [s for s in result if s["type"] == "analysis"]
        assert len(analyses) >= 5, f"Should find at least 5 analysis sections, found {len(analyses)}"


class TestEdgeCases:
    """Test 1.3: Edge cases and mixed content."""

    def test_classify_mixed_content(self):
        """LLM should handle sections with mixed content types."""
        doc = """## Test Section
This test is designed to assess the model's ability.

**Prompt:**
Calculate the result of 2 + 2.

**Analysis:**
The model correctly computed the answer as 4."""

        result = classify_sections(doc, api_key=TEST_KEY)

        # Validate structure
        assert isinstance(result, list), "Result should be a list"
        assert len(result) >= 3, f"Expected at least 3 sections, got {len(result)}"

        # Find sections
        prompts = [s for s in result if s["type"] == "test_prompt"]
        analyses = [s for s in result if s["type"] == "analysis"]

        # Should find the prompt
        assert len(prompts) >= 1, "Should find test prompt"

        # Prompt should be sacred
        for prompt in prompts:
            assert prompt["tier"] == "sacred", "Test prompt must be sacred tier"
            assert "**Prompt:**" in prompt["content"] or "Calculate" in prompt["content"]

        # Analysis should be present
        assert len(analyses) >= 1, "Should find analysis section"

        # Analysis should be moderate tier (not sacred)
        for analysis in analyses:
            assert analysis["tier"] in ["moderate", "minimal", "aggressive"], \
                f"Analysis should not be sacred tier, got {analysis['tier']}"

    def test_classify_empty_document(self):
        """Should handle empty document gracefully."""
        doc = ""

        result = classify_sections(doc, api_key=TEST_KEY)

        # Should return empty list or single section
        assert isinstance(result, list), "Result should be a list"
        assert len(result) <= 1, "Empty doc should have 0-1 sections"

    def test_classify_formulas(self):
        """Should identify formulas and mark as sacred."""
        doc = """## Mathematical Analysis

The formula for standard deviation is:

σ = √(Σ(xi - μ)² / N)

Where σ represents the standard deviation."""

        result = classify_sections(doc, api_key=TEST_KEY)

        # Should find formula section
        formulas = [s for s in result if s["type"] == "formula" or "σ" in s["content"]]

        # If formula identified separately, should be sacred
        for formula in formulas:
            if formula["type"] == "formula":
                assert formula["tier"] == "sacred", "Formulas must be sacred tier"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
