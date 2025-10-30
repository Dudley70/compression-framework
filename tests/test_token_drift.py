#!/usr/bin/env python3
"""
Test suite for token drift detection system.

This test suite follows the TDD approach specified in TASK_1.2_token_drift.md
All tests should FAIL initially since no implementation exists yet.
"""
import pytest
from pathlib import Path
from scripts.detect_token_drift import TokenDriftDetector

@pytest.fixture
def detector():
    """Create a TokenDriftDetector instance for testing."""
    return TokenDriftDetector()

@pytest.fixture
def fixtures_dir():
    """Path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"

class TestTokenDrift:
    """Test cases for token drift detection."""

    def test_no_drift(self, detector, fixtures_dir):
        """Test Case 1: No changes should result in 1.0 drift ratio."""
        result = detector.check_drift(str(fixtures_dir / "no_drift.md"))

        assert result["has_header"] is True
        assert result["drift_ratio"] == pytest.approx(1.0, rel=0.02)
        assert result["recommendation"] == "none"
        assert result["baseline_tokens"] == 1000
        assert result["current_tokens"] == pytest.approx(1000, rel=0.02)
        assert result["drift_percentage"] == pytest.approx(0.0, abs=2.0)
        assert result["absolute_drift"] == pytest.approx(0, abs=20)

    def test_minor_drift(self, detector, fixtures_dir):
        """Test Case 2: 5% growth should not trigger action."""
        result = detector.check_drift(str(fixtures_dir / "minor_drift.md"))

        assert result["has_header"] is True
        assert result["drift_ratio"] == pytest.approx(1.05, rel=0.02)
        assert result["recommendation"] == "none"
        assert result["baseline_tokens"] == 1000
        assert result["current_tokens"] == pytest.approx(1050, rel=0.02)
        assert result["drift_percentage"] == pytest.approx(5.0, abs=2.0)
        assert "Minimal drift" in result["explanation"]

    def test_moderate_drift_flags(self, detector, fixtures_dir):
        """Test Case 3: 25% growth should recommend review."""
        result = detector.check_drift(str(fixtures_dir / "moderate_drift.md"))

        assert result["has_header"] is True
        assert result["drift_ratio"] == pytest.approx(1.25, rel=0.02)
        assert result["recommendation"] == "review"
        assert result["baseline_tokens"] == 1000
        assert result["current_tokens"] == pytest.approx(1250, rel=0.02)
        assert result["drift_percentage"] == pytest.approx(25.0, rel=1.0)
        assert "Review for new content" in result["explanation"]

    def test_substantial_drift_compresses(self, detector, fixtures_dir):
        """Test Case 4: 50% growth should recommend compression."""
        result = detector.check_drift(str(fixtures_dir / "substantial_drift.md"))

        assert result["has_header"] is True
        assert result["drift_ratio"] >= 1.50
        assert result["recommendation"] == "compress"
        assert result["baseline_tokens"] == 1000
        assert result["current_tokens"] >= 1500
        assert result["drift_percentage"] >= 50.0
        assert "re-compression" in result["explanation"]

    def test_no_header_untracked(self, detector, fixtures_dir):
        """Test Case 5: Document without header should be marked untracked."""
        result = detector.check_drift(str(fixtures_dir / "no_header.md"))

        assert result["has_header"] is False
        assert result["baseline_tokens"] is None
        assert result["drift_ratio"] is None
        assert result["drift_percentage"] is None
        assert result["absolute_drift"] is None
        assert result["recommendation"] == "untracked"
        assert result["current_tokens"] > 0  # Still counts current tokens
        assert "no compression baseline" in result["explanation"]

    def test_malformed_header(self, detector, fixtures_dir):
        """Test Case 6: Header missing baseline_tokens should be handled."""
        result = detector.check_drift(str(fixtures_dir / "malformed_header.md"))

        assert result["baseline_tokens"] is None
        assert result["drift_ratio"] is None
        assert result["current_tokens"] > 0
        # Could be either invalid_header or untracked depending on implementation
        assert result["recommendation"] in ["invalid_header", "untracked"]
        assert "baseline" in result["explanation"].lower()

class TestThresholdBoundaries:
    """Test exact threshold boundaries to ensure correct classification."""

    def test_flag_threshold_boundary(self, detector):
        """Test 15% exactly (FLAG_THRESHOLD)."""
        result = detector._calculate_drift(1000, 1150)
        assert result.recommendation == "flag"
        assert result.drift_ratio == 1.15
        assert result.drift_percentage == 15.0
        assert result.absolute_drift == 150

    def test_review_threshold_boundary(self, detector):
        """Test 30% exactly (REVIEW_THRESHOLD)."""
        result = detector._calculate_drift(1000, 1300)
        assert result.recommendation == "review"
        assert result.drift_ratio == 1.30
        assert result.drift_percentage == 30.0
        assert result.absolute_drift == 300

    def test_compress_threshold_boundary(self, detector):
        """Test 50% exactly (COMPRESS_THRESHOLD)."""
        result = detector._calculate_drift(1000, 1500)
        assert result.recommendation == "compress"
        assert result.drift_ratio == 1.50
        assert result.drift_percentage == 50.0
        assert result.absolute_drift == 500

    def test_below_flag_threshold(self, detector):
        """Test just below flag threshold (14% growth)."""
        result = detector._calculate_drift(1000, 1140)
        assert result.recommendation == "none"
        assert result.drift_ratio == 1.14

    def test_between_flag_and_review(self, detector):
        """Test between flag and review thresholds (20% growth)."""
        result = detector._calculate_drift(1000, 1200)
        assert result.recommendation == "flag"
        assert result.drift_ratio == 1.20

    def test_between_review_and_compress(self, detector):
        """Test between review and compress thresholds (40% growth)."""
        result = detector._calculate_drift(1000, 1400)
        assert result.recommendation == "review"
        assert result.drift_ratio == 1.40

class TestTokenCounting:
    """Test token counting functionality."""

    def test_token_counting_excludes_header(self, detector, fixtures_dir):
        """Token count should exclude YAML frontmatter."""
        result = detector.check_drift(str(fixtures_dir / "no_drift.md"))

        # If baseline is 1000, current should also be ~1000 (not including header)
        assert result["current_tokens"] == pytest.approx(
            result["baseline_tokens"], rel=0.02
        )

    def test_content_only_counting(self, detector):
        """Test that _count_tokens method excludes YAML frontmatter."""
        sample_content = """---
compression:
  baseline_tokens: 500
---

This is the actual content that should be counted.
The YAML header above should be excluded from token counting.
"""
        # This should count only the content after the YAML header
        token_count = detector._count_tokens(sample_content)

        # Should be much less than counting the entire content with header
        full_count = detector.encoding.encode(sample_content)
        assert token_count < len(full_count)
        assert token_count > 0

class TestHeaderParsing:
    """Test YAML header parsing functionality."""

    def test_extract_baseline_valid_header(self, detector):
        """Test extracting baseline from valid header."""
        content = """---
compression:
  baseline_tokens: 1500
  last_full_compression: 2025-10-30
---

Content here."""

        baseline = detector._extract_baseline(content)
        assert baseline == 1500

    def test_extract_baseline_missing_field(self, detector):
        """Test extracting baseline when field is missing."""
        content = """---
compression:
  last_full_compression: 2025-10-30
---

Content here."""

        baseline = detector._extract_baseline(content)
        assert baseline is None

    def test_extract_baseline_no_header(self, detector):
        """Test extracting baseline when no header exists."""
        content = """# Document Title

Just content, no YAML header."""

        baseline = detector._extract_baseline(content)
        assert baseline is None

    def test_extract_baseline_malformed_yaml(self, detector):
        """Test extracting baseline from malformed YAML."""
        content = """---
compression:
  baseline_tokens: not_a_number
---

Content here."""

        # Should handle malformed YAML gracefully
        baseline = detector._extract_baseline(content)
        assert baseline is None

class TestDriftCalculations:
    """Test drift calculation logic."""

    def test_drift_calculation_no_baseline(self, detector):
        """Test drift calculation when baseline is None."""
        result = detector._calculate_drift(None, 1000)

        assert result.has_header is False
        assert result.baseline_tokens is None
        assert result.current_tokens == 1000
        assert result.drift_ratio is None
        assert result.drift_percentage is None
        assert result.absolute_drift is None
        assert result.recommendation == "untracked"

    def test_drift_calculation_with_baseline(self, detector):
        """Test drift calculation with valid baseline."""
        result = detector._calculate_drift(1000, 1200)

        assert result.has_header is True
        assert result.baseline_tokens == 1000
        assert result.current_tokens == 1200
        assert result.drift_ratio == 1.2
        assert result.drift_percentage == 20.0
        assert result.absolute_drift == 200
        assert result.recommendation == "flag"

    def test_zero_drift(self, detector):
        """Test calculation when current equals baseline."""
        result = detector._calculate_drift(1000, 1000)

        assert result.drift_ratio == 1.0
        assert result.drift_percentage == 0.0
        assert result.absolute_drift == 0
        assert result.recommendation == "none"

    def test_negative_drift(self, detector):
        """Test calculation when current is less than baseline."""
        result = detector._calculate_drift(1000, 800)

        assert result.drift_ratio == 0.8
        assert result.drift_percentage == -20.0
        assert result.absolute_drift == -200
        assert result.recommendation == "none"

class TestResultFormatting:
    """Test result formatting and structure."""

    def test_result_format_structure(self, detector, fixtures_dir):
        """Test that result has all required fields."""
        result = detector.check_drift(str(fixtures_dir / "no_drift.md"))

        required_fields = [
            "has_header", "baseline_tokens", "current_tokens",
            "drift_ratio", "drift_percentage", "absolute_drift",
            "recommendation", "explanation"
        ]

        for field in required_fields:
            assert field in result

    def test_explanation_messages(self, detector):
        """Test that explanation messages are appropriate for each recommendation."""
        test_cases = [
            (1000, 1000, "none", "minimal"),
            (1000, 1180, "flag", "monitor"),
            (1000, 1350, "review", "review"),
            (1000, 1600, "compress", "re-compression")
        ]

        for baseline, current, expected_rec, expected_word in test_cases:
            result = detector._calculate_drift(baseline, current)
            assert result.recommendation == expected_rec
            assert expected_word.lower() in result.explanation.lower()

class TestIntegration:
    """Integration tests using actual files."""

    def test_check_drift_method_exists(self, detector):
        """Test that the main check_drift method exists and is callable."""
        assert hasattr(detector, 'check_drift')
        assert callable(detector.check_drift)

    def test_file_not_found_handling(self, detector):
        """Test handling of non-existent files."""
        with pytest.raises(FileNotFoundError):
            detector.check_drift("/nonexistent/file.md")

    def test_all_fixtures_processable(self, detector, fixtures_dir):
        """Test that all fixture files can be processed without errors."""
        fixture_files = [
            "no_drift.md", "minor_drift.md", "moderate_drift.md",
            "substantial_drift.md", "no_header.md", "malformed_header.md"
        ]

        for fixture in fixture_files:
            file_path = fixtures_dir / fixture
            if file_path.exists():
                # Should not raise exceptions
                result = detector.check_drift(str(file_path))
                assert isinstance(result, dict)
                assert "recommendation" in result