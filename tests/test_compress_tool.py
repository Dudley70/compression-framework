#!/usr/bin/env python3
"""
Comprehensive test suite for compression tool MVP (Task 4.1)

This test suite follows TDD methodology with 30+ test cases covering:
- Document analysis and recommendations
- LSC technique applications (5 techniques)
- Safety integration (4 layers)
- Validation and reporting
- CLI interface
- End-to-end workflows

Tests are designed to initially fail (red phase) until implementation is complete.
"""

import pytest
import os
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Import the actual implementation classes (green phase)
from compress import CompressionTool, LSCTechniques, ValidationReport
from compress import AnalysisResult, ValidationResult


def run_cli(command: str):
    """Helper function to run CLI commands for testing"""
    try:
        result = subprocess.run(
            f"python3 compress.py {command}",
            shell=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        return result
    except Exception as e:
        # Return mock result for TDD phase
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = f"CLI execution failed - {e}"
        return mock_result


class TestDocumentAnalysis:
    """Test document analysis and recommendations (8 tests)"""
    
    def test_detect_uncompressed_document(self):
        """Identify verbose prose needing compression"""
        tool = CompressionTool()
        fixture_path = Path(__file__).parent / "fixtures" / "verbose_prose.md"

        result = tool.analyze_document(str(fixture_path))
        assert result.compression_score < 0.4, f"Expected low score for verbose prose, got {result.compression_score}"
        assert "lists_tables" in result.recommended_techniques, "Should recommend lists_tables for enumerated prose"
        assert result.needs_compression is True, "Verbose prose should need compression"
        assert result.analysis_time < 5.0, "Analysis should be fast"
    
    def test_detect_already_compressed(self):
        """Recognize highly structured documents"""
        tool = CompressionTool()
        fixture_path = Path(__file__).parent / "fixtures" / "already_compressed.md"

        result = tool.analyze_document(str(fixture_path))
        assert result.compression_score >= 0.8, f"Expected high score for already compressed, got {result.compression_score}"
        assert len(result.recommended_techniques) == 0, "Should not recommend techniques for already compressed content"
        assert result.needs_compression is False, "Already compressed content should not need compression"
    
    def test_section_level_analysis(self):
        """Analyze each section independently"""
        tool = CompressionTool()
        fixture_path = Path(__file__).parent / "fixtures" / "mixed_state.md"

        result = tool.analyze_document(str(fixture_path))
        assert len(result.sections) > 1, "Should analyze multiple sections independently"
        assert any(s['needs_compression'] for s in result.sections), "Should find at least one section needing compression"
        assert any(not s['needs_compression'] for s in result.sections), "Should find at least one section already compressed"
    
    def test_technique_recommendations(self):
        """Recommend appropriate LSC techniques"""
        tool = CompressionTool()
        fixture_path = Path(__file__).parent / "fixtures" / "verbose_prose.md"

        result = tool.analyze_document(str(fixture_path))
        assert "hierarchical_structure" in result.recommended_techniques, \
            f"Expected 'hierarchical_structure' in recommendations, got {result.recommended_techniques}"
        assert "lists_tables" in result.recommended_techniques, \
            f"Expected 'lists_tables' in recommendations, got {result.recommended_techniques}"
    
    def test_handle_empty_document(self):
        """Handle empty documents gracefully"""
        tool = CompressionTool()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("")
            empty_file = f.name

        try:
            result = tool.analyze_document(empty_file)
            assert result.compression_score == 0.0, \
                f"Expected compression_score of 0.0 for empty document, got {result.compression_score}"
            assert result.recommended_techniques == [], \
                f"Expected no technique recommendations for empty document, got {result.recommended_techniques}"
        finally:
            os.unlink(empty_file)
    
    def test_handle_malformed_markdown(self):
        """Handle malformed markdown gracefully"""
        tool = CompressionTool()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("```python\nunclosed code block\n# Malformed header ```")
            malformed_file = f.name

        try:
            result = tool.analyze_document(malformed_file)
            assert result is not None, "Should return result for malformed markdown, not crash"
            assert hasattr(result, 'compression_score'), "Result should have compression_score attribute"
        finally:
            os.unlink(malformed_file)
    
    def test_detect_code_heavy_document(self):
        """Detect documents with lots of code blocks"""
        tool = CompressionTool()

        code_heavy_content = """# API Examples

```python
def get_user():
    return {"id": 1}
```

```javascript
const user = await fetch('/api/user');
```

```bash
curl -X GET /api/user
```

Short text between code blocks.
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(code_heavy_content)
            code_file = f.name

        try:
            result = tool.analyze_document(code_file)
            assert result.compression_score >= 0.6, \
                f"Expected compression_score >= 0.6 for code-heavy document (already well-structured), got {result.compression_score}"
            assert len(result.recommended_techniques) == 0, \
                f"Expected no compression techniques for code-heavy document, got {result.recommended_techniques}"
        finally:
            os.unlink(code_file)
    
    def test_identify_list_opportunities(self):
        """Identify content suitable for list conversion"""
        tool = CompressionTool()

        list_suitable_content = """# Features

Our platform provides three main features. First, user authentication which handles login and registration. Second, data management which stores and retrieves information. Third, reporting which generates analytics and insights.
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(list_suitable_content)
            list_file = f.name

        try:
            result = tool.analyze_document(list_file)
            assert "lists_tables" in result.recommended_techniques, \
                f"Expected 'lists_tables' in recommendations for enumerated prose, got {result.recommended_techniques}"
        finally:
            os.unlink(list_file)


class TestLSCTechniques:
    """Test individual compression technique application (10 tests)"""
    
    def test_lists_tables_conversion(self):
        """Convert prose to structured lists"""
        lsc = LSCTechniques()
        original = "The API supports three methods: GET for retrieval, POST for creation, DELETE for removal."

        result = lsc.apply_lists_tables(original)
        assert "- GET:" in result or "GET:" in result, \
            f"Expected structured list with 'GET:' in result, got: {result}"
        assert "retrieval" in result.lower(), \
            f"Expected 'retrieval' preserved in result, got: {result}"
        assert len(result) < len(original), \
            f"Expected compression: result length {len(result)} should be < original length {len(original)}"
    
    def test_hierarchical_structure_addition(self):
        """Add headers to flat content"""
        lsc = LSCTechniques()
        original = "First topic content here. This is about authentication. Second topic content here. This covers data storage."

        result = lsc.apply_hierarchical_structure(original)
        assert result.count("#") >= 2, \
            f"Expected at least 2 headers added to flat content, got {result.count('#')} headers in: {result}"
    
    def test_redundancy_removal(self):
        """Eliminate duplicate information"""
        lsc = LSCTechniques()
        original = "OAuth2 is secure. OAuth2 prevents theft. OAuth2 is secure authentication. OAuth2 provides security."

        result = lsc.remove_redundancy(original)
        assert result.count("OAuth2") < original.count("OAuth2"), \
            f"Expected fewer 'OAuth2' mentions: original had {original.count('OAuth2')}, result has {result.count('OAuth2')}"
        assert "secure" in result.lower(), \
            f"Expected 'secure' preserved in result, got: {result}"
        assert "prevents theft" in result.lower() or "theft" in result.lower(), \
            f"Expected 'theft' concept preserved in result, got: {result}"
    
    def test_technical_shorthand(self):
        """Use standard abbreviations"""
        lsc = LSCTechniques()
        original = "HyperText Transfer Protocol Secure (HTTPS) with Transport Layer Security (TLS) encryption"

        result = lsc.apply_technical_shorthand(original)
        assert "HTTPS" in result, \
            f"Expected 'HTTPS' abbreviation in result, got: {result}"
        assert "TLS" in result, \
            f"Expected 'TLS' abbreviation in result, got: {result}"
        assert len(result) < len(original), \
            f"Expected compression: result length {len(result)} should be < original length {len(original)}"
    
    def test_information_density(self):
        """Increase meaning per token"""
        lsc = LSCTechniques()
        original = "When you are making a request to the API, you need to make sure to include the authentication header."

        result = lsc.increase_information_density(original)
        assert "request" in result.lower(), \
            f"Expected 'request' preserved in result, got: {result}"
        assert "header" in result.lower(), \
            f"Expected 'header' preserved in result, got: {result}"
        assert len(result) < len(original), \
            f"Expected increased density (shorter): result length {len(result)} should be < original length {len(original)}"
    
    def test_preserve_code_blocks(self):
        """Never compress code blocks"""
        lsc = LSCTechniques()
        original = "Example code:\n```python\nprint('hello world')\n```\nThis code prints a greeting message."

        result = lsc.apply_lists_tables(original)
        assert "```python" in result, \
            f"Expected code block marker '```python' preserved in result, got: {result}"
        assert "print('hello world')" in result, \
            f"Expected code content 'print('hello world')' preserved in result, got: {result}"
    
    def test_preserve_links(self):
        """Maintain markdown links"""
        lsc = LSCTechniques()
        original = "See the [official documentation](https://example.com/docs) for more detailed information about the system."

        result = lsc.increase_information_density(original)
        assert "[official documentation](https://example.com/docs)" in result, \
            f"Expected markdown link '[official documentation](https://example.com/docs)' preserved in result, got: {result}"
    
    def test_preserve_images(self):
        """Maintain markdown images"""
        lsc = LSCTechniques()
        original = "The architecture diagram ![Architecture](./diagram.png) shows the system components and their relationships."

        result = lsc.increase_information_density(original)
        assert "![Architecture](./diagram.png)" in result, \
            f"Expected markdown image '![Architecture](./diagram.png)' preserved in result, got: {result}"
    
    def test_table_preservation(self):
        """Don't modify existing tables"""
        lsc = LSCTechniques()
        original = """| Method | Purpose | Example |
|--------|---------|---------|
| GET    | Retrieve| /api/users |
| POST   | Create  | /api/users |

This table shows the HTTP methods."""

        result = lsc.apply_lists_tables(original)
        assert "| Method |" in result, \
            f"Expected table header '| Method |' preserved in result, got: {result}"
        assert "|--------|" in result, \
            f"Expected table separator '|--------|' preserved in result, got: {result}"
    
    def test_nested_list_handling(self):
        """Handle nested list structures correctly"""
        lsc = LSCTechniques()
        original = """Authentication has multiple layers. The first layer is user credentials. The second layer includes two-factor authentication with SMS and app-based tokens. The third layer is session management."""

        result = lsc.apply_hierarchical_structure(original)
        assert "##" in result or "- " in result, \
            f"Expected hierarchical structure (headers or lists) in result, got: {result}"


class TestSafetyIntegration:
    """Test safety validation integration (6 tests)"""
    
    def test_precheck_blocks_compressed(self):
        """Pre-check refuses already compressed content"""
        tool = CompressionTool()
        fixture_path = Path(__file__).parent / "fixtures" / "already_compressed.md"

        with open(fixture_path) as f:
            original = f.read()
        compressed = "Even more compressed version"

        result = tool.compress_with_safety(original, compressed)
        assert not result.passed, \
            f"Expected pre-check to block already compressed content, but validation passed"
        assert "pre-check" in result.failure_reason.lower(), \
            f"Expected 'pre-check' in failure reason, got: {result.failure_reason}"
    
    def test_entity_preservation_blocks_loss(self):
        """Entity check refuses dangerous information loss"""
        tool = CompressionTool()
        original = "The API uses OAuth2, JWT, and HTTPS with TLS encryption. Configure via the .env.production file using AWS_ACCESS_KEY_ID."
        compressed = "The system uses security protocols."

        result = tool.compress_with_safety(original, compressed)
        assert not result.passed, \
            f"Expected entity preservation check to block dangerous information loss, but validation passed"
        assert "entity" in result.failure_reason.lower(), \
            f"Expected 'entity' in failure reason, got: {result.failure_reason}"
    
    def test_minimal_benefit_blocks_insufficient(self):
        """Minimal benefit check refuses small compression gains"""
        tool = CompressionTool()
        original = "This is a document that contains quite a bit of text content for testing purposes. " * 50  # ~1000 tokens
        compressed = "This is a document that contains quite a bit of text content for testing. " * 47  # ~940 tokens (6% reduction)

        result = tool.compress_with_safety(original, compressed)
        assert not result.passed, \
            f"Expected minimal benefit check to block insufficient compression (6% reduction), but validation passed"
        assert "minimal benefit" in result.failure_reason.lower(), \
            f"Expected 'minimal benefit' in failure reason, got: {result.failure_reason}"
    
    def test_semantic_similarity_blocks_drift(self):
        """Semantic check catches meaning changes"""
        tool = CompressionTool()
        original = "Authentication is required for all API endpoints to ensure security."
        compressed = "Authentication is optional for API endpoints to improve performance."

        result = tool.compress_with_safety(original, compressed)
        assert not result.passed, \
            f"Expected semantic similarity check to block meaning changes (required->optional), but validation passed"
        assert "semantic" in result.failure_reason.lower(), \
            f"Expected 'semantic' in failure reason, got: {result.failure_reason}"
    
    def test_safe_compression_passes(self):
        """Valid compression passes all safety checks"""
        tool = CompressionTool()
        original = "When making requests to the API endpoints, you need to include authentication headers in every single request that you send."
        compressed = "API requests require authentication headers."

        result = tool.compress_with_safety(original, compressed)
        assert result.passed, \
            f"Expected valid compression to pass safety checks, but got failure: {result.failure_reason if hasattr(result, 'failure_reason') else 'unknown'}"
        assert len(result.warnings) == 0, \
            f"Expected no warnings for valid compression, got {len(result.warnings)} warnings: {result.warnings}"
    
    def test_warning_on_edge_case(self):
        """Generate warnings for edge cases that pass but need review"""
        tool = CompressionTool()
        original = "The system configuration requires careful attention to ensure proper setup and configuration."
        compressed = "System config needs careful setup."

        result = tool.compress_with_safety(original, compressed)
        assert result.passed or len(result.warnings) > 0, \
            f"Expected edge case to either pass with warnings or fail, but got passed={result.passed}, warnings={len(result.warnings) if hasattr(result, 'warnings') else 0}"


class TestValidationReporting:
    """Test validation and report generation (5 tests)"""
    
    def test_compression_score_calculated(self):
        """Compression score uses 6-metric algorithm"""
        tool = CompressionTool()
        original = "This is some verbose prose text that contains multiple sentences with various levels of detail."
        compressed = "Verbose prose with details."

        report = tool.validate_compression(original, compressed)
        assert report.compression_score is not None, \
            "Expected compression_score to be calculated, got None"
        assert 0 <= report.compression_score <= 1, \
            f"Expected compression_score between 0 and 1, got {report.compression_score}"
    
    def test_token_drift_detected(self):
        """Token drift detection identifies growth"""
        tool = CompressionTool()
        original = "Short text"
        compressed = "This is actually much longer text that represents token growth instead of compression"

        report = tool.validate_compression(original, compressed)
        assert report.token_drift.growth_detected, \
            f"Expected token drift detection to identify growth from {len(original)} to {len(compressed)} chars"
    
    def test_report_markdown_generation(self):
        """Markdown report contains all required metrics"""
        tool = CompressionTool()
        original = "test content for report generation"
        compressed = "test content"

        report = tool.validate_compression(original, compressed)
        markdown = report.to_markdown()
        assert "Token Count" in markdown, \
            f"Expected 'Token Count' in markdown report, got: {markdown[:200]}..."
        assert "Compression Ratio" in markdown, \
            f"Expected 'Compression Ratio' in markdown report, got: {markdown[:200]}..."
        assert "Safety Validation" in markdown, \
            f"Expected 'Safety Validation' in markdown report, got: {markdown[:200]}..."
        assert "Compression Score" in markdown, \
            f"Expected 'Compression Score' in markdown report, got: {markdown[:200]}..."
    
    def test_report_json_generation(self):
        """JSON report has structured data for automation"""
        tool = CompressionTool()
        original = "test content for JSON report"
        compressed = "test content"

        report = tool.validate_compression(original, compressed)
        json_data = report.to_json()
        assert "original_tokens" in json_data, \
            f"Expected 'original_tokens' in JSON report, got keys: {list(json_data.keys())}"
        assert "compressed_tokens" in json_data, \
            f"Expected 'compressed_tokens' in JSON report, got keys: {list(json_data.keys())}"
        assert "safety_passed" in json_data, \
            f"Expected 'safety_passed' in JSON report, got keys: {list(json_data.keys())}"
        assert "compression_score" in json_data, \
            f"Expected 'compression_score' in JSON report, got keys: {list(json_data.keys())}"
    
    def test_performance_metrics_included(self):
        """Report includes performance timing metrics"""
        tool = CompressionTool()
        original = "content for performance testing"
        compressed = "performance content"

        report = tool.validate_compression(original, compressed)
        json_data = report.to_json()
        assert "processing_time" in json_data, \
            f"Expected 'processing_time' in JSON report, got keys: {list(json_data.keys())}"
        assert "analysis_time" in json_data, \
            f"Expected 'analysis_time' in JSON report, got keys: {list(json_data.keys())}"


class TestCLIInterface:
    """Test command-line interface (4 tests)"""
    
    def test_analyze_command(self):
        """Analyze command shows recommendations without compression"""
        fixture_path = Path(__file__).parent / "fixtures" / "verbose_prose.md"
        result = run_cli(f"analyze {fixture_path}")

        assert result.returncode == 0, \
            f"Expected analyze command to succeed, got returncode {result.returncode}, stderr: {result.stderr}"
        assert "Recommended Techniques" in result.stdout, \
            f"Expected 'Recommended Techniques' in output, got: {result.stdout[:200]}..."
    
    def test_compress_command(self):
        """Compress command creates compressed output"""
        fixture_path = Path(__file__).parent / "fixtures" / "verbose_prose.md"

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_file = Path(tmp_dir) / "compressed.md"
            result = run_cli(f"compress {fixture_path} --output {output_file}")

            assert result.returncode == 0, \
                f"Expected compress command to succeed, got returncode {result.returncode}, stderr: {result.stderr}"
            assert output_file.exists(), \
                f"Expected output file to be created at {output_file}"
    
    def test_dry_run_flag(self):
        """Dry run shows changes without applying them"""
        fixture_path = Path(__file__).parent / "fixtures" / "verbose_prose.md"
        original_content = fixture_path.read_text()

        result = run_cli(f"compress {fixture_path} --dry-run")

        assert result.returncode == 0, \
            f"Expected dry-run to succeed, got returncode {result.returncode}, stderr: {result.stderr}"
        assert "Would compress" in result.stdout, \
            f"Expected 'Would compress' in dry-run output, got: {result.stdout[:200]}..."
        assert fixture_path.read_text() == original_content, \
            "Expected original file to remain unchanged after dry-run"
    
    def test_report_generation(self):
        """Report flag saves validation report to file"""
        fixture_path = Path(__file__).parent / "fixtures" / "verbose_prose.md"

        with tempfile.TemporaryDirectory() as tmp_dir:
            report_file = Path(tmp_dir) / "report.md"
            result = run_cli(f"compress {fixture_path} --report {report_file}")

            assert report_file.exists(), \
                f"Expected report file to be created at {report_file}"
            report_content = report_file.read_text()
            assert "Compression Score" in report_content, \
                f"Expected 'Compression Score' in report, got: {report_content[:200]}..."


class TestEndToEnd:
    """Test complete workflows (6 tests)"""
    
    def test_full_compression_workflow(self):
        """Complete analysis → compress → validate flow"""
        fixture_path = Path(__file__).parent / "fixtures" / "verbose_prose.md"

        with tempfile.TemporaryDirectory() as tmp_dir:
            test_doc = Path(tmp_dir) / "document.md"
            test_doc.write_text(fixture_path.read_text())

            tool = CompressionTool()

            # Analyze
            analysis = tool.analyze_document(str(test_doc))
            assert len(analysis.recommended_techniques) > 0, \
                f"Expected recommendations for verbose prose, got {len(analysis.recommended_techniques)} techniques"

            # Compress
            compressed = tool.compress_file(str(test_doc))
            assert len(compressed) < len(test_doc.read_text()), \
                f"Expected compression: result {len(compressed)} chars < original {len(test_doc.read_text())} chars"

            # Validate
            report = tool.validate_compression(test_doc.read_text(), compressed)
            assert report.safety_passed, \
                f"Expected compression to pass safety validation, got failure: {report.safety_result.failure_reason}"

            # Save
            output = Path(tmp_dir) / "compressed.md"
            output.write_text(compressed)
            assert output.exists(), \
                f"Expected output file to be saved at {output}"
    
    def test_multi_section_document(self):
        """Handle documents with multiple sections independently"""
        fixture_path = Path(__file__).parent / "fixtures" / "mixed_state.md"

        tool = CompressionTool()

        analysis = tool.analyze_document(str(fixture_path))

        assert len(analysis.sections) >= 3, \
            f"Expected at least 3 sections in mixed document, got {len(analysis.sections)}"
        compressed_sections = [s for s in analysis.sections if not s['needs_compression']]
        needs_compression = [s for s in analysis.sections if s['needs_compression']]
        assert len(compressed_sections) >= 1, \
            f"Expected at least 1 already-compressed section, got {len(compressed_sections)}"
        assert len(needs_compression) >= 1, \
            f"Expected at least 1 section needing compression, got {len(needs_compression)}"
    
    def test_error_handling_malformed(self):
        """Handle malformed documents gracefully"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("```python\nunclosed code block\n### Malformed header in code")
            malformed_file = f.name

        try:
            tool = CompressionTool()

            # Should not crash, should handle gracefully
            result = tool.compress_file(malformed_file)
            assert result is not None, \
                "Expected graceful handling of malformed document (non-None result)"
        finally:
            os.unlink(malformed_file)
    
    def test_large_document_performance(self):
        """Handle large documents within performance requirements"""
        # Create large document (simulating real-world size)
        large_content = """# Large Document

This is a large document section. """ + ("This sentence repeats to create size. " * 100) + """

## Section 2

More content here. """ + ("Additional verbose content for testing. " * 100) + """

## Section 3

Final section. """ + ("More repetitive content for size testing. " * 100)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(large_content)
            large_file = f.name

        try:
            tool = CompressionTool()

            import time
            start_time = time.time()
            result = tool.compress_file(large_file)
            end_time = time.time()

            assert (end_time - start_time) < 30, \
                f"Expected compression to complete in <30 seconds, took {end_time - start_time:.2f} seconds"
        finally:
            os.unlink(large_file)
    
    def test_batch_processing_capability(self):
        """Process multiple documents in sequence"""
        fixtures = [
            "verbose_prose.md",
            "mixed_state.md",
            "entity_heavy.md"
        ]

        tool = CompressionTool()

        results = []
        for fixture in fixtures:
            fixture_path = Path(__file__).parent / "fixtures" / fixture
            result = tool.analyze_document(str(fixture_path))
            results.append(result)

        assert len(results) == len(fixtures), \
            f"Expected {len(fixtures)} results, got {len(results)}"
        for i, result in enumerate(results):
            assert result is not None, \
                f"Expected valid result for fixture {fixtures[i]}, got None"
    
    def test_safety_validation_integration(self):
        """Verify safety system integration in real workflow"""
        # Test with entity-heavy document that should trigger safety checks
        fixture_path = Path(__file__).parent / "fixtures" / "entity_heavy.md"

        tool = CompressionTool()

        with open(fixture_path) as f:
            original = f.read()

        # Simulate aggressive compression that should fail safety
        aggressive_compressed = "Tech stack uses various technologies."

        result = tool.compress_with_safety(original, aggressive_compressed)
        assert not result.passed, \
            "Expected aggressive compression to fail entity preservation check"
        assert "entity" in result.failure_reason.lower(), \
            f"Expected 'entity' in failure reason for entity-heavy compression, got: {result.failure_reason}"


class TestIntegrationWithExistingComponents:
    """Test integration with validated components from previous tasks (4 tests)"""
    
    def test_analyze_compression_state_integration(self):
        """Integration with TASK-1.1 CompressionStateAnalyzer"""
        try:
            from analyze_compression_state import CompressionStateAnalyzer

            tool = CompressionTool()
            fixture_path = Path(__file__).parent / "fixtures" / "verbose_prose.md"

            result = tool.analyze_document(str(fixture_path))
            assert result is not None, \
                "Expected analyzer integration to return structured results"
            assert hasattr(result, 'compression_score'), \
                "Expected result to have compression_score from analyzer"
        except ImportError:
            pytest.skip("analyze_compression_state.py not available - component integration pending")
    
    def test_safety_checks_integration(self):
        """Integration with TASK-2.3 SafetyValidator"""
        try:
            from safety_checks import SafetyValidator

            tool = CompressionTool()
            original = "Test content with authentication and OAuth2 configuration details."
            compressed = "Test content."

            result = tool.compress_with_safety(original, compressed)
            assert result is not None, \
                "Expected SafetyValidator integration to return result"
            assert hasattr(result, 'passed'), \
                "Expected result to have 'passed' attribute from SafetyValidator"
        except ImportError:
            pytest.skip("safety_checks.py not available - component integration pending")
    
    def test_compression_score_integration(self):
        """Integration with TASK-2.1 compression scoring"""
        try:
            from compression_score import calculate_compression_score

            tool = CompressionTool()
            original = "verbose content"
            compressed = "concise"

            report = tool.validate_compression(original, compressed)
            assert report is not None, \
                "Expected compression scoring integration to return report"
            assert hasattr(report, 'compression_score'), \
                "Expected report to include compression_score from scoring module"
        except ImportError:
            pytest.skip("compression_score.py not available - component integration pending")
    
    def test_token_drift_integration(self):
        """Integration with TASK-1.2 token drift detection"""
        try:
            from detect_token_drift import detect_token_drift

            tool = CompressionTool()
            original = "original content"
            compressed = "expanded content that actually grew in size"

            report = tool.validate_compression(original, compressed)
            assert report is not None, \
                "Expected token drift detection integration to return report"
            assert hasattr(report, 'token_drift'), \
                "Expected report to include token_drift from drift detection module"
        except ImportError:
            pytest.skip("detect_token_drift.py not available - component integration pending")


# Test runner helper
if __name__ == "__main__":
    """Run tests with verbose output for TDD development"""
    print("=" * 60)
    print("COMPRESSION TOOL MVP TEST SUITE (TDD Phase)")
    print("=" * 60)
    print()
    print("This test suite contains 30+ comprehensive test cases")
    print("designed to initially FAIL until implementation is complete.")
    print()
    print("Test Categories:")
    print("- Document Analysis: 8 tests")
    print("- LSC Techniques: 10 tests") 
    print("- Safety Integration: 6 tests")
    print("- Validation/Reporting: 5 tests")
    print("- CLI Interface: 4 tests")
    print("- End-to-End: 6 tests")
    print("- Component Integration: 4 tests")
    print()
    print("Total: 43 tests")
    print()
    print("Running pytest...")
    print("=" * 60)
    
    # Run pytest with verbose output
    pytest.main([__file__, "-v", "--tb=short"])