#!/usr/bin/env python3
"""
Test suite for Content Density Analyzer (Task 1.1)

This test suite follows TDD approach - all tests should FAIL initially
since the ContentAnalyzer class doesn't exist yet.
"""
import pytest
import os
from pathlib import Path

# Import dependencies (these should exist from previous tasks)
from scripts.compression_score import CompressionScorer
# Import the ContentAnalyzer (this will fail initially)
try:
    from scripts.analyze_compression_state import ContentAnalyzer
except ImportError:
    ContentAnalyzer = None


class TestContentAnalyzer:
    """Test suite for section-level compression analysis."""
    
    @pytest.fixture
    def scorer(self):
        """Create a compression scorer instance."""
        return CompressionScorer()
    
    @pytest.fixture
    def analyzer(self, scorer):
        """Create a content analyzer instance."""
        if ContentAnalyzer is None:
            pytest.skip("ContentAnalyzer not implemented yet")
        return ContentAnalyzer(scorer)
    
    @pytest.fixture
    def test_fixtures_dir(self):
        """Path to test fixtures directory."""
        return Path(__file__).parent / "fixtures"
    
    def load_fixture(self, filename):
        """Load a test fixture file."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        with open(fixtures_dir / filename, 'r') as f:
            return f.read()
    
    def test_split_sections_basic(self, analyzer):
        """Test document splitting into sections with basic markdown."""
        document = """# Main Title

Some intro content here.

## Section One

Content for section one with multiple paragraphs.
This is the second paragraph.

## Section Two

Content for section two.

### Subsection

Nested content here."""
        
        sections = analyzer.split_into_sections(document)
        
        # Should identify 3 sections: Main Title, Section One, Section Two > Subsection
        assert len(sections) >= 3
        
        # Check section structure
        assert sections[0]["title"] == "Main Title"
        assert sections[0]["level"] == 1
        assert "intro content" in sections[0]["content"]
        
        assert sections[1]["title"] == "Section One"
        assert sections[1]["level"] == 2
        assert "multiple paragraphs" in sections[1]["content"]
    
    def test_split_sections_empty_sections(self, analyzer):
        """Test handling of very short sections."""
        document = """# Title

## Empty Section

## Another Section

Much longer content here that should definitely be above the minimum
token threshold for section analysis. This section has enough content
to be analyzed properly and should not be filtered out."""
        
        sections = analyzer.split_into_sections(document)
        
        # Should filter out sections below minimum token count
        long_sections = [s for s in sections if len(s["content"].split()) > 20]
        assert len(long_sections) >= 1
    
    def test_analyze_section_verbose(self, analyzer):
        """Test analysis of a verbose section (should score low)."""
        verbose_content = """
        This is a very detailed explanation that goes into great depth about
        the topic at hand. We provide comprehensive information and multiple
        examples to ensure that readers understand every aspect of the subject.
        The explanation includes background context, step-by-step instructions,
        and detailed reasoning for each recommendation that we make.
        """
        
        result = analyzer.analyze_section(verbose_content.strip())
        
        assert "score" in result
        assert "state" in result
        assert "needs_compression" in result
        
        # Verbose content should score low (< 0.4)
        assert result["score"] < 0.4
        assert result["state"] in ["verbose", "uncompressed"]
        assert result["needs_compression"] is True
    
    def test_analyze_section_compressed(self, analyzer):
        """Test analysis of a compressed section (should score high)."""
        compressed_content = """
        - API: POST /users
        - Auth: Bearer token
        - Body: {name, email, role}
        - Returns: User object (201) | Error (400/409)
        """
        
        result = analyzer.analyze_section(compressed_content.strip())
        
        # Compressed content should score high (> 0.7)
        assert result["score"] > 0.7
        assert result["state"] in ["compressed", "highly_compressed"]
        assert result["needs_compression"] is False
    
    def test_fully_uncompressed_document(self, analyzer):
        """Test analysis of fully uncompressed document."""
        document = self.load_fixture("fully_uncompressed.md")
        
        result = analyzer.analyze_document(document)
        
        assert result["overall_state"] == "uncompressed"
        
        # All sections should need compression
        sections = result["sections"]
        assert len(sections) >= 3  # Introduction, Authentication, Getting Started
        
        for section in sections:
            assert section["score"] < 0.4
            assert section["needs_compression"] is True
        
        assert result["recommendation"] == "compress_all"
    
    def test_fully_compressed_document(self, analyzer):
        """Test analysis of fully compressed document."""
        document = self.load_fixture("fully_compressed.md")
        
        result = analyzer.analyze_document(document)
        
        assert result["overall_state"] == "compressed"
        
        # All sections should be compressed
        sections = result["sections"]
        assert len(sections) >= 4  # POST /auth, GET /users, PUT /users/:id, DELETE /users/:id
        
        for section in sections:
            assert section["score"] > 0.7
            assert section["needs_compression"] is False
        
        assert result["recommendation"] == "none"
    
    def test_mixed_state_document(self, analyzer):
        """Test analysis of document with mixed compression states."""
        document = self.load_fixture("mixed_state.md")
        
        result = analyzer.analyze_document(document)
        
        assert result["overall_state"] == "mixed"
        
        sections = result["sections"]
        assert len(sections) >= 3
        
        # Should have both compressed and uncompressed sections
        compressed_sections = [s for s in sections if s["score"] > 0.7]
        uncompressed_sections = [s for s in sections if s["score"] < 0.4]
        
        assert len(compressed_sections) > 0
        assert len(uncompressed_sections) > 0
        
        # Recommendation should identify which sections to compress
        assert "compress_sections" in result["recommendation"]
    
    def test_document_with_token_drift(self, analyzer):
        """Test analysis of document with token drift metadata."""
        document = self.load_fixture("with_token_drift.md")
        
        # Extract YAML header for drift analysis
        lines = document.split('\n')
        yaml_end = lines.index('---', 1) if '---' in lines[1:] else 0
        header_text = '\n'.join(lines[1:yaml_end]) if yaml_end > 0 else ""
        
        import yaml
        header_metadata = yaml.safe_load(header_text) if header_text.strip() else None
        
        result = analyzer.analyze_document(document, header_metadata)
        
        # Should detect drift and mixed state
        assert result["overall_state"] in ["edited", "mixed"]
        
        # Should have token drift information
        assert "token_drift" in result
        
        # Should recommend both compression and baseline update
        assert "compress_sections" in result["recommendation"]
        assert "update" in result["recommendation"]
    
    def test_classify_state_logic(self, analyzer):
        """Test state classification with various score combinations."""
        # All low scores → uncompressed
        assert analyzer.classify_state([0.2, 0.3, 0.1]) == "uncompressed"
        
        # All high scores → compressed
        assert analyzer.classify_state([0.8, 0.9, 0.75]) == "compressed"
        
        # Mixed scores → mixed
        assert analyzer.classify_state([0.2, 0.8, 0.3]) == "mixed"
        
        # With token drift → edited
        assert analyzer.classify_state([0.8, 0.2], token_drift_ratio=1.25) == "edited"
    
    def test_section_recommendations(self, analyzer):
        """Test that recommendations correctly identify which sections to compress."""
        # Mock document analysis result
        sections = [
            {"title": "Section 1", "score": 0.2, "needs_compression": True},
            {"title": "Section 2", "score": 0.8, "needs_compression": False},
            {"title": "Section 3", "score": 0.3, "needs_compression": True}
        ]
        
        # Should recommend compressing sections 0 and 2
        recommendation = analyzer._generate_recommendation(sections, "mixed")
        assert "compress_sections: [0, 2]" in recommendation
    
    def test_minimum_section_length(self, analyzer):
        """Test that tiny sections are skipped."""
        document = """# Title

## Tiny

Hi.

## Normal Section

This is a normal section with enough content to be analyzed properly.
It has multiple sentences and should definitely be above the minimum
token threshold for section analysis."""
        
        sections = analyzer.split_into_sections(document)
        
        # Should filter out the "Tiny" section due to low token count
        substantial_sections = [s for s in sections if len(s["content"].split()) >= 20]
        assert len(substantial_sections) >= 1
        
        # Tiny section should either be filtered or merged
        assert not any(s["title"] == "Tiny" and len(s["content"].split()) < 5 for s in sections)
    
    def test_real_project_docs(self, analyzer):
        """Test on actual project documentation."""
        # Test SESSION.md
        session_path = Path(__file__).parent.parent / "SESSION.md"
        if session_path.exists():
            with open(session_path, 'r') as f:
                content = f.read()
            
            result = analyzer.analyze_document(content)
            
            # Should successfully analyze without errors
            assert "overall_state" in result
            assert "sections" in result
            assert len(result["sections"]) > 0
            assert "recommendation" in result
            
            # Each section should have required fields
            for section in result["sections"]:
                assert "title" in section
                assert "score" in section
                assert "state" in section
                assert "needs_compression" in section
    
    def test_edge_case_no_headers(self, analyzer):
        """Test document with no headers."""
        document = "This is just plain text with no headers at all."
        
        result = analyzer.analyze_document(document)
        
        # Should handle gracefully, treating whole document as one section
        assert len(result["sections"]) >= 1
        assert result["overall_state"] in ["uncompressed", "compressed"]
    
    def test_edge_case_empty_document(self, analyzer):
        """Test empty document."""
        document = ""
        
        result = analyzer.analyze_document(document)
        
        # Should handle gracefully
        assert result["overall_state"] == "empty"
        assert len(result["sections"]) == 0
    
    def test_nested_headers_depth_limit(self, analyzer):
        """Test that H4+ headers are ignored."""
        document = """# H1 Title

## H2 Section

### H3 Subsection

#### H4 Sub-subsection (should be ignored)

##### H5 (should be ignored)

Content here should be part of H3 section."""
        
        sections = analyzer.split_into_sections(document)
        
        # Should only create sections for H1, H2, H3
        section_levels = [s["level"] for s in sections]
        assert max(section_levels) <= 3
        assert 4 not in section_levels
        assert 5 not in section_levels
    
    def test_performance_large_document(self, analyzer):
        """Test performance with a large document."""
        # Create a large document with many sections
        large_doc_parts = ["# Large Document\n\n"]
        
        for i in range(50):
            large_doc_parts.append(f"## Section {i}\n\n")
            large_doc_parts.append(f"Content for section {i} " * 20 + "\n\n")
        
        large_document = "".join(large_doc_parts)
        
        import time
        start_time = time.time()
        result = analyzer.analyze_document(large_document)
        end_time = time.time()
        
        # Should complete within reasonable time (< 5 seconds)
        assert end_time - start_time < 5.0
        
        # Should analyze all sections
        assert len(result["sections"]) >= 50
        
        # Should have valid overall state
        assert result["overall_state"] in ["uncompressed", "compressed", "mixed"]


# Test runner
if __name__ == "__main__":
    pytest.main([__file__, "-v"])