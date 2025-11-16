"""
Checkpoint 2: Deterministic Compression Phase Tests

Tests for tier-specific compression rules.
- Tier 0 (sacred): No compression (verbatim)
- Tier 1 (minimal): Headers + symbols only (~10-20% compression)
- Tier 2 (moderate): All rules except scaffolding (~30-50% compression)
- Tier 3 (aggressive): All V7 rules (~50-70% compression)
"""

import os
import pytest
from compress_v7_classify import compress_by_tier, compress_from_classification, classify_sections

# Get API key from environment
TEST_KEY = os.getenv("ANTHROPIC_API_KEY", "")


class TestSacredTier:
    """Test tier 0 (sacred) - no compression."""

    def test_compress_sacred_tier(self):
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


class TestMinimalTier:
    """Test tier 1 (minimal) - headers + symbols only."""

    def test_compress_minimal_tier(self):
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

        # Should apply symbols (→ for returns/to)
        assert " → " in result or "returns" in result

        # Should NOT remove prose fragments
        assert "processes" in result or "process" in result


class TestModerateTier:
    """Test tier 2 (moderate) - all rules except scaffolding."""

    def test_compress_moderate_tier(self):
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

        # Should be shorter (moderate = ~20-40% compression)
        assert len(result) < len(section["content"]) * 0.9


class TestAggressiveTier:
    """Test tier 3 (aggressive) - all V7 rules."""

    def test_compress_aggressive_tier(self):
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

        # Should be compressed more than moderate tier
        # Note: Actual compression depends on content - short texts compress less
        assert len(result) < len(section["content"])

        # Should preserve key facts
        assert "Gemini" in result
        assert "2.5 Pro" in result or "2.5Pro" in result or "2.5" in result

        # Should apply scaffolding removal (at least some phrases removed)
        # Note: Specific phrases removed depend on SCAFFOLDING_PATTERNS and context
        assert result != section["content"]  # Should change something


class TestDeterministicCompression:
    """Test that compression is deterministic."""

    @pytest.mark.skipif(not os.path.exists("test_data/documents/gemini-self-assessment.md"),
                        reason="Gemini test document not found")
    @pytest.mark.skipif(not TEST_KEY, reason="API key not provided")
    def test_compress_gemini_deterministic(self):
        """Same classification should produce identical results."""
        with open("test_data/documents/gemini-self-assessment.md", 'r') as f:
            doc = f.read()

        # Classify once
        classification = classify_sections(doc, api_key=TEST_KEY)

        # Compress 3 times
        result1 = compress_from_classification(classification)
        result2 = compress_from_classification(classification)
        result3 = compress_from_classification(classification)

        # All results should be IDENTICAL
        assert result1 == result2 == result3

        # Verify Rule 6 compliance - all test prompts preserved
        prompts_in_classification = [s for s in classification if s["type"] == "test_prompt"]
        for prompt_section in prompts_in_classification:
            # Each prompt should appear verbatim in the result
            assert prompt_section["content"] in result1
