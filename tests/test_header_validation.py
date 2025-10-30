"""
Test suite for document header specification validation.

This test suite validates that document headers conform to the specification
defined in TASK_3.2_header_specification.md. It tests YAML parsing, required
fields, field value constraints, parameter ranges, and format requirements.
"""

import pytest
import yaml
import re
from pathlib import Path
from datetime import datetime


class TestHeaderValidation:
    """Validate document header specification."""

    @pytest.fixture
    def examples_dir(self):
        """Path to header example fixtures."""
        return Path(__file__).parent / "fixtures" / "headers"

    @pytest.fixture
    def valid_doc_types(self):
        """Valid document type enum values."""
        return [
            'API_REFERENCE', 'TUTORIAL', 'SESSION_HANDOVER',
            'PROJECT_CONTEXT', 'TASK_SPECIFICATION', 'VALIDATION_REPORT',
            'ANALYSIS', 'PLAN', 'REFERENCE', 'PATTERN', 'METHODOLOGY',
            'RESEARCH', 'PROPOSAL'
        ]

    @pytest.fixture
    def valid_audiences(self):
        """Valid audience enum values."""
        return ['llm-only', 'human-technical', 'human-general', 'multi-role']

    @pytest.fixture
    def valid_layers(self):
        """Valid information layer enum values."""
        return ['Session', 'Strategic', 'Control', 'Operational', 'Archive']

    @pytest.fixture
    def valid_phases(self):
        """Valid lifecycle phase enum values."""
        return ['Active', 'Complete', 'Archived', 'Deprecated']

    @pytest.fixture
    def valid_purposes(self):
        """Valid purpose enum values."""
        return ['Execution', 'Learning', 'Reference', 'Audit', 'Planning', 'Analysis']

    def test_examples_directory_exists(self, examples_dir):
        """Examples directory must exist."""
        assert examples_dir.exists(), f"Examples directory not found: {examples_dir}"

    def test_all_examples_parse_yaml(self, examples_dir):
        """All example headers must be valid YAML."""
        example_files = list(examples_dir.glob("*.md"))
        assert len(example_files) >= 10, f"Need at least 10 examples, found {len(example_files)}"

        for example_file in example_files:
            content = example_file.read_text()
            header = self._extract_yaml_header(content)
            assert header, f"No YAML header found in {example_file.name}"

            # Should parse without error
            try:
                parsed = yaml.safe_load(header)
                assert parsed is not None, f"Empty YAML header in {example_file.name}"
            except yaml.YAMLError as e:
                pytest.fail(f"Invalid YAML in {example_file.name}: {e}")

    def test_required_fields_present(self, examples_dir):
        """All required fields must be present in examples."""
        required_fields = ['doc_type', 'audience', 'layer', 'phase', 'purpose', 'target_style']

        for example_file in examples_dir.glob("*.md"):
            content = example_file.read_text()
            header = self._extract_yaml_header(content)
            parsed = yaml.safe_load(header)

            for field in required_fields:
                assert field in parsed, f"{example_file.name}: missing required field '{field}'"

    def test_target_style_structure(self, examples_dir):
        """target_style must have correct structure with σ, γ, κ parameters."""
        for example_file in examples_dir.glob("*.md"):
            content = example_file.read_text()
            header = self._extract_yaml_header(content)
            parsed = yaml.safe_load(header)

            assert 'target_style' in parsed, f"{example_file.name}: missing target_style"
            style = parsed['target_style']

            # Check required parameters
            required_params = ['sigma', 'gamma', 'kappa']
            for param in required_params:
                assert param in style, f"{example_file.name}: target_style missing '{param}'"

            # Check parameter ranges [0.0, 1.0]
            for param in required_params:
                value = style[param]
                assert isinstance(value, (int, float)), f"{example_file.name}: {param} must be numeric"
                assert 0.0 <= value <= 1.0, f"{example_file.name}: {param}={value} not in [0.0, 1.0]"

    def test_compressed_docs_have_tracking(self, examples_dir):
        """Documents with compression must have complete tracking fields."""
        # Only check files that explicitly indicate they are compressed (not uncompressed)
        compressed_pattern = re.compile(r'.*_compressed\.md$')

        for example_file in examples_dir.glob("*.md"):
            # Check if filename suggests compression
            if compressed_pattern.search(example_file.name):
                content = example_file.read_text()
                header = self._extract_yaml_header(content)
                parsed = yaml.safe_load(header)

                assert 'compression' in parsed, f"{example_file.name}: compressed doc missing compression field"
                comp = parsed['compression']

                required_comp_fields = ['last_full_compression', 'baseline_tokens', 'parameters', 'validation']
                for field in required_comp_fields:
                    assert field in comp, f"{example_file.name}: compression missing '{field}'"

                # Check validation subfields
                validation = comp['validation']
                validation_fields = ['entity_preservation', 'semantic_similarity']
                for field in validation_fields:
                    assert field in validation, f"{example_file.name}: compression.validation missing '{field}'"
                    value = validation[field]
                    assert 0.0 <= value <= 1.0, f"{example_file.name}: validation.{field}={value} not in [0.0, 1.0]"

    def test_datetime_format_valid(self, examples_dir):
        """Compression timestamps must use correct format."""
        # Pattern: YYYY-MM-DD HH:MM TZ
        pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2} [A-Z]+$'

        for example_file in examples_dir.glob("*.md"):
            content = example_file.read_text()
            header = self._extract_yaml_header(content)
            parsed = yaml.safe_load(header)

            if 'compression' not in parsed:
                continue

            timestamp = parsed['compression']['last_full_compression']
            assert re.match(pattern, timestamp), f"{example_file.name}: invalid timestamp format '{timestamp}'"

    def test_doc_type_enum_valid(self, examples_dir, valid_doc_types):
        """doc_type values must match specification enum."""
        for example_file in examples_dir.glob("*.md"):
            content = example_file.read_text()
            header = self._extract_yaml_header(content)
            parsed = yaml.safe_load(header)

            doc_type = parsed['doc_type']
            assert doc_type in valid_doc_types, f"{example_file.name}: invalid doc_type '{doc_type}'"

    def test_audience_enum_valid(self, examples_dir, valid_audiences):
        """audience values must match specification enum."""
        for example_file in examples_dir.glob("*.md"):
            content = example_file.read_text()
            header = self._extract_yaml_header(content)
            parsed = yaml.safe_load(header)

            audience = parsed['audience']
            assert audience in valid_audiences, f"{example_file.name}: invalid audience '{audience}'"

    def test_layer_enum_valid(self, examples_dir, valid_layers):
        """layer values must match specification enum."""
        for example_file in examples_dir.glob("*.md"):
            content = example_file.read_text()
            header = self._extract_yaml_header(content)
            parsed = yaml.safe_load(header)

            layer = parsed['layer']
            assert layer in valid_layers, f"{example_file.name}: invalid layer '{layer}'"

    def test_phase_enum_valid(self, examples_dir, valid_phases):
        """phase values must match specification enum."""
        for example_file in examples_dir.glob("*.md"):
            content = example_file.read_text()
            header = self._extract_yaml_header(content)
            parsed = yaml.safe_load(header)

            phase = parsed['phase']
            assert phase in valid_phases, f"{example_file.name}: invalid phase '{phase}'"

    def test_purpose_enum_valid(self, examples_dir, valid_purposes):
        """purpose values must match specification enum."""
        for example_file in examples_dir.glob("*.md"):
            content = example_file.read_text()
            header = self._extract_yaml_header(content)
            parsed = yaml.safe_load(header)

            purpose = parsed['purpose']
            assert purpose in valid_purposes, f"{example_file.name}: invalid purpose '{purpose}'"

    def test_baseline_tokens_positive(self, examples_dir):
        """baseline_tokens must be positive integer."""
        for example_file in examples_dir.glob("*.md"):
            content = example_file.read_text()
            header = self._extract_yaml_header(content)
            parsed = yaml.safe_load(header)

            if 'compression' not in parsed:
                continue

            tokens = parsed['compression']['baseline_tokens']
            assert isinstance(tokens, int), f"{example_file.name}: baseline_tokens must be integer"
            assert tokens > 0, f"{example_file.name}: baseline_tokens must be positive"

    def test_compression_parameters_valid(self, examples_dir):
        """Compression parameters must match target_style structure."""
        for example_file in examples_dir.glob("*.md"):
            content = example_file.read_text()
            header = self._extract_yaml_header(content)
            parsed = yaml.safe_load(header)

            if 'compression' not in parsed:
                continue

            params = parsed['compression']['parameters']
            # Should have same structure as target_style
            for key in ['σ', 'γ', 'κ']:  # Greek letters used in compression tracking
                if key in params:
                    value = params[key]
                    assert 0.0 <= value <= 1.0, f"{example_file.name}: compression parameter {key}={value} not in [0.0, 1.0]"

    def test_writing_guide_structure(self, examples_dir):
        """writing_guide (if present) must have correct structure."""
        for example_file in examples_dir.glob("*.md"):
            content = example_file.read_text()
            header = self._extract_yaml_header(content)
            parsed = yaml.safe_load(header)

            if 'writing_guide' not in parsed:
                continue

            guide = parsed['writing_guide']
            # Should be object with string fields
            assert isinstance(guide, dict), f"{example_file.name}: writing_guide must be object"

            for key, value in guide.items():
                assert isinstance(value, str), f"{example_file.name}: writing_guide.{key} must be string"

    def _extract_yaml_header(self, content: str) -> str:
        """Extract YAML frontmatter from markdown content."""
        lines = content.split('\n')
        if not lines or lines[0].strip() != '---':
            return ""

        header_lines = []
        for line in lines[1:]:
            if line.strip() == '---':
                break
            header_lines.append(line)

        return '\n'.join(header_lines)


# Utility functions for external use
def extract_yaml_header(content: str) -> str:
    """Extract YAML frontmatter from markdown content."""
    return TestHeaderValidation()._extract_yaml_header(content)


def validate_header(header_yaml: str) -> dict:
    """Validate a header YAML string and return parsed result."""
    try:
        parsed = yaml.safe_load(header_yaml)
        if not parsed:
            raise ValueError("Empty YAML header")
        return parsed
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML: {e}")


def check_required_fields(header: dict) -> list:
    """Check required fields and return list of missing fields."""
    required = ['doc_type', 'audience', 'layer', 'phase', 'purpose', 'target_style']
    missing = []
    for field in required:
        if field not in header:
            missing.append(field)
    return missing