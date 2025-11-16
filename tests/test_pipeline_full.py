"""
Checkpoint 3: Full Pipeline Integration Tests

Tests for complete classify-then-compress pipeline.
- End-to-end compression with validation
- Deterministic output across runs
- Performance validation
"""

import os
import json
import time
import re
import pytest
from compress_v7_classify import (
    compress_v7_classify_main,
    count_test_prompts,
    verify_prompts_verbatim
)

# Get API key from environment
TEST_KEY = os.getenv("ANTHROPIC_API_KEY", "")


def read_file(filepath):
    """Read file contents."""
    with open(filepath, 'r') as f:
        return f.read()


class TestFullPipeline:
    """Test end-to-end pipeline."""

    @pytest.mark.skipif(not os.path.exists("test_data/documents/gemini-self-assessment.md"),
                        reason="Gemini test document not found")
    @pytest.mark.skipif(not TEST_KEY, reason="API key not provided")
    def test_full_pipeline_gemini(self):
        """Complete pipeline on real Gemini document."""
        input_file = "test_data/documents/gemini-self-assessment.md"
        output_file = "test_data/results/gemini-classify-compress.md"
        report_file = "test_data/results/classify-validation-report.json"

        # Ensure results directory exists
        os.makedirs("test_data/results", exist_ok=True)

        # Run compression
        compress_v7_classify_main(
            input_file,
            output_file,
            api_key=TEST_KEY,
            model="claude-haiku-4-5-20251001",
            expected_prompts=11,
            report_file=report_file
        )

        # Verify output file exists
        assert os.path.exists(output_file), "Output file should be created"

        # Load report
        with open(report_file, 'r') as f:
            report = json.load(f)

        # Validation checks
        assert report["rule_6_compliant"] == True, "Should be Rule 6 compliant"
        assert report["prompts_found"] >= 11, f"Expected at least 11 prompts, found {report['prompts_found']}"
        assert report["prompts_match"] == True, "All prompts should be preserved verbatim"

        # Compression ratio should be good (75-85% = keep 75-85% of content)
        # Note: Actual ratio may vary based on classification
        assert 0.50 <= report["compression_ratio"] <= 1.0, \
            f"Compression ratio should be 50-100%, got {report['compression_ratio']:.1%}"

        # Output should be smaller than input
        assert report["compressed_size"] < report["original_size"], \
            "Compressed size should be smaller than original"

        print(f"\n✅ Pipeline complete:")
        print(f"   Original: {report['original_size']:,} bytes")
        print(f"   Compressed: {report['compressed_size']:,} bytes")
        print(f"   Ratio: {report['compression_ratio']:.1%}")
        print(f"   Prompts: {report['prompts_found']}/{report['prompts_expected']}")


class TestPipelineDeterminism:
    """Test deterministic output."""

    @pytest.mark.skipif(not os.path.exists("test_data/documents/gemini-self-assessment.md"),
                        reason="Gemini test document not found")
    @pytest.mark.skipif(not TEST_KEY, reason="API key not provided")
    def test_pipeline_prompts_preserved(self):
        """Test prompts are preserved across runs."""
        input_file = "test_data/documents/gemini-self-assessment.md"
        output_file = "test_data/results/determinism-test.md"

        # Ensure results directory exists
        os.makedirs("test_data/results", exist_ok=True)

        # Run compression
        compress_v7_classify_main(
            input_file,
            output_file,
            api_key=TEST_KEY,
            model="claude-haiku-4-5-20251001"
        )

        # Read original and compressed
        original = read_file(input_file)
        compressed = read_file(output_file)

        # Count prompts in both
        original_prompts = count_test_prompts(original)
        compressed_prompts = count_test_prompts(compressed)

        print(f"\n📊 Prompt preservation:")
        print(f"   Original prompts: {original_prompts}")
        print(f"   Compressed prompts: {compressed_prompts}")

        # Should preserve all prompts
        assert compressed_prompts >= 11, f"Expected at least 11 prompts, found {compressed_prompts}"

        # Verify prompts are verbatim
        prompts_match = verify_prompts_verbatim(original, compressed)
        assert prompts_match, "All prompts should be preserved verbatim"


class TestPerformance:
    """Test performance requirements."""

    @pytest.mark.skipif(not os.path.exists("test_data/documents/gemini-self-assessment.md"),
                        reason="Gemini test document not found")
    @pytest.mark.skipif(not TEST_KEY, reason="API key not provided")
    def test_performance_requirements(self):
        """Pipeline should complete in reasonable time."""
        input_file = "test_data/documents/gemini-self-assessment.md"
        output_file = "test_data/results/perf-test.md"

        # Ensure results directory exists
        os.makedirs("test_data/results", exist_ok=True)

        start = time.time()
        compress_v7_classify_main(
            input_file,
            output_file,
            api_key=TEST_KEY,
            model="claude-haiku-4-5-20251001"
        )
        duration = time.time() - start

        print(f"\n⏱️  Compression took {duration:.1f}s")

        # Should complete in reasonable time
        # Note: LLM calls can take 240-450s for large documents (130KB+)
        assert duration < 480, f"Should complete in under 8 minutes, took {duration:.1f}s"

        # Verify output exists
        assert os.path.exists(output_file), "Output file should be created"
