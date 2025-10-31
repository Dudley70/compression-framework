"""
Tests for convergence testing infrastructure.

This module validates the convergence testing harness before running the full suite.
Following TDD approach: test infrastructure first, then implement to pass tests.
"""

import pytest
import json
import csv
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the convergence tester
import sys
sys.path.append(str(Path(__file__).parent.parent))
from scripts.test_convergence import ConvergenceTester


class TestConvergenceInfrastructure:
    """Validate test harness before running full suite"""
    
    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory for testing"""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def tester(self, temp_output_dir):
        """Create ConvergenceTester with temporary output directory"""
        return ConvergenceTester(output_dir=str(temp_output_dir))
    
    def test_harness_initialization(self, temp_output_dir):
        """Test harness creates output directory and initializes properly"""
        tester = ConvergenceTester(output_dir=str(temp_output_dir))
        
        # Check output directory exists
        assert tester.output_dir.exists()
        assert tester.output_dir.is_dir()
        
        # Check components are initialized
        assert hasattr(tester, 'encoder')
        assert hasattr(tester, 'compression_tool')
        assert hasattr(tester, 'lsc')
        
        # Check tiktoken encoder works
        test_text = "This is a test."
        tokens = tester.encoder.encode(test_text)
        assert isinstance(tokens, list)
        assert len(tokens) > 0
    
    def test_technique_list_complete(self, tester):
        """Test all techniques are available"""
        techniques = tester.get_techniques()
        
        assert len(techniques) == 6
        expected_techniques = [
            "lists_tables",
            "hierarchical_structure", 
            "remove_redundancy",
            "technical_shorthand",
            "information_density",
            "all_combined"
        ]
        
        for expected in expected_techniques:
            assert expected in techniques
    
    def test_document_list_valid(self, tester):
        """Test all test documents exist"""
        docs = tester.get_test_documents()
        
        # Should find at least some test documents
        assert len(docs) > 0
        
        # All returned paths should exist
        for doc in docs:
            assert doc.exists(), f"Missing test document: {doc}"
            assert doc.suffix == '.md', f"Document should be markdown: {doc}"
    
    def test_token_counting_accuracy(self, tester):
        """Test token counting is consistent"""
        test_text = "This is a test document with some content."
        
        tokens1 = len(tester.encoder.encode(test_text))
        tokens2 = len(tester.encoder.encode(test_text))
        
        assert tokens1 == tokens2  # Deterministic
        assert tokens1 > 0
        assert isinstance(tokens1, int)
    
    def test_single_technique_application(self, tester):
        """Test individual technique application works"""
        test_text = "This is a test document. First, we do something. Second, we do another thing."
        
        # Test each technique individually
        techniques = ["lists_tables", "hierarchical_structure", "remove_redundancy", 
                     "technical_shorthand", "information_density"]
        
        for technique in techniques:
            try:
                result = tester.compress_single_technique(test_text, technique, safety_enabled=True)
                assert isinstance(result, str)
                assert len(result) > 0  # Should return some content
            except Exception as e:
                pytest.fail(f"Technique {technique} failed: {e}")
    
    def test_full_pipeline_application(self, tester):
        """Test full pipeline compression works"""
        test_text = "This is a test document with multiple sentences. First, authentication. Second, authorization."
        
        # Test both safety modes
        for safety in [True, False]:
            try:
                result = tester.compress_full_pipeline(test_text, safety_enabled=safety)
                assert isinstance(result, str)
                assert len(result) > 0
            except Exception as e:
                pytest.fail(f"Full pipeline failed with safety={safety}: {e}")


class TestSingleConvergenceTest:
    """Test individual convergence test execution"""
    
    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory for testing"""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def tester(self, temp_output_dir):
        """Create ConvergenceTester with temporary output directory"""
        return ConvergenceTester(output_dir=str(temp_output_dir))
    
    @pytest.fixture
    def sample_document(self, temp_output_dir):
        """Create a sample test document"""
        doc_path = temp_output_dir / "test_doc.md"
        doc_path.write_text("""# Test Document

This is a verbose test document. First, we have authentication which handles user login. 
Second, we have authorization which manages permissions. Third, we have session management.

The API supports multiple methods for user interaction. These methods include GET for retrieval,
POST for creation, and DELETE for removal.
""")
        return doc_path
    
    def test_convergence_test_structure(self, tester, sample_document):
        """Test convergence test returns proper structure"""
        result = tester.test_convergence(sample_document, "lists_tables", safety=True, max_rounds=3)
        
        # Validate result structure
        required_fields = ["document", "technique", "safety_enabled", "rounds", "original_tokens"]
        for field in required_fields:
            assert field in result, f"Missing field: {field}"
        
        assert result["document"] == sample_document.name
        assert result["technique"] == "lists_tables"
        assert result["safety_enabled"] is True
        assert isinstance(result["rounds"], list)
        assert result["original_tokens"] > 0
        
        # Each round should have proper structure
        for round_data in result["rounds"]:
            round_fields = ["round", "tokens", "chars", "ratio_to_original", "ratio_to_previous"]
            for field in round_fields:
                assert field in round_data, f"Missing round field: {field}"
    
    def test_convergence_detection(self, tester, sample_document):
        """Test that convergence detection works"""
        result = tester.test_convergence(sample_document, "lists_tables", safety=True, max_rounds=10)
        
        # Should have convergence status
        assert "converged" in result
        
        if result.get("converged"):
            # If converged, should have convergence round and final tokens
            assert "converged_at_round" in result
            assert "final_tokens" in result
            assert result["converged_at_round"] >= 0
        else:
            # If not converged, should still have final tokens
            assert "final_tokens" in result
    
    def test_round_progression(self, tester, sample_document):
        """Test that rounds progress correctly"""
        result = tester.test_convergence(sample_document, "remove_redundancy", safety=True, max_rounds=5)
        
        rounds = result["rounds"]
        assert len(rounds) <= 5  # Should not exceed max_rounds
        
        # Rounds should be numbered sequentially
        for i, round_data in enumerate(rounds):
            assert round_data["round"] == i
        
        # Token counts should be reasonable
        original_tokens = result["original_tokens"]
        for round_data in rounds:
            assert round_data["tokens"] > 0
            assert round_data["tokens"] <= original_tokens * 2  # Sanity check
    
    def test_safety_mode_differences(self, tester, sample_document):
        """Test that safety modes can be applied"""
        # Test with safety enabled
        result_safe = tester.test_convergence(sample_document, "all_combined", safety=True, max_rounds=3)
        assert result_safe["safety_enabled"] is True
        
        # Test with safety disabled  
        result_unsafe = tester.test_convergence(sample_document, "all_combined", safety=False, max_rounds=3)
        assert result_unsafe["safety_enabled"] is False
        
        # Both should complete without errors
        assert len(result_safe["rounds"]) > 0
        assert len(result_unsafe["rounds"]) > 0


class TestDataExport:
    """Test data export functionality"""
    
    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory for testing"""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def tester(self, temp_output_dir):
        """Create ConvergenceTester with temporary output directory"""
        return ConvergenceTester(output_dir=str(temp_output_dir))
    
    @pytest.fixture
    def sample_results(self):
        """Create sample test results for export testing"""
        return {
            "metadata": {
                "timestamp": "2025-01-01T12:00:00",
                "total_tests": 2,
                "mode": "test"
            },
            "tests": [
                {
                    "document": "test1.md",
                    "technique": "lists_tables",
                    "safety_enabled": True,
                    "original_tokens": 100,
                    "converged": True,
                    "converged_at_round": 2,
                    "final_tokens": 80,
                    "rounds": [
                        {"round": 0, "tokens": 90, "chars": 400, "ratio_to_original": 0.9, "ratio_to_previous": 0.9},
                        {"round": 1, "tokens": 85, "chars": 380, "ratio_to_original": 0.85, "ratio_to_previous": 0.94},
                        {"round": 2, "tokens": 80, "chars": 360, "ratio_to_original": 0.8, "ratio_to_previous": 0.94}
                    ]
                },
                {
                    "document": "test2.md",
                    "technique": "remove_redundancy",
                    "safety_enabled": False,
                    "original_tokens": 120,
                    "converged": False,
                    "final_tokens": 100,
                    "rounds": [
                        {"round": 0, "tokens": 110, "chars": 500, "ratio_to_original": 0.92, "ratio_to_previous": 0.92},
                        {"round": 1, "tokens": 100, "chars": 450, "ratio_to_original": 0.83, "ratio_to_previous": 0.91}
                    ]
                }
            ]
        }
    
    def test_json_export(self, tester, sample_results, temp_output_dir):
        """Test JSON export functionality"""
        file_paths = tester.save_results(sample_results, timestamp="test")
        
        # Check JSON file was created
        assert 'json' in file_paths
        json_path = Path(file_paths['json'])
        assert json_path.exists()
        
        # Validate JSON content
        with open(json_path, 'r') as f:
            exported_data = json.load(f)
        
        assert exported_data["metadata"]["total_tests"] == 2
        assert len(exported_data["tests"]) == 2
        assert exported_data["tests"][0]["document"] == "test1.md"
    
    def test_csv_export(self, tester, sample_results, temp_output_dir):
        """Test CSV export functionality"""
        csv_path = temp_output_dir / "test_export.csv"
        tester.save_csv(sample_results, csv_path)
        
        assert csv_path.exists()
        
        # Validate CSV content
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            rows = list(reader)
        
        # Check headers
        expected_headers = ["document", "technique", "safety", "round", "tokens", "chars", 
                          "ratio_to_original", "ratio_to_previous", "converged", "converged_at_round"]
        assert headers == expected_headers
        
        # Should have rows for each round of each test
        assert len(rows) == 5  # 3 rounds from test1 + 2 rounds from test2
        
        # Check first row data
        assert rows[0][0] == "test1.md"  # document
        assert rows[0][1] == "lists_tables"  # technique
        assert rows[0][2] == "True"  # safety
    
    def test_markdown_summary(self, tester, sample_results, temp_output_dir):
        """Test markdown summary generation"""
        md_path = temp_output_dir / "test_summary.md"
        tester.generate_summary(sample_results, md_path)
        
        assert md_path.exists()
        
        # Validate markdown content
        content = md_path.read_text()
        
        assert "# Convergence Testing Summary" in content
        assert "Total Tests" in content
        assert "Converged" in content
        assert "Results by Technique" in content
        assert "Safety Mode Comparison" in content
        assert len(content) > 500  # Should have substantial content


class TestQuickMode:
    """Test quick mode functionality for rapid testing"""
    
    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory for testing"""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def tester(self, temp_output_dir):
        """Create ConvergenceTester with temporary output directory"""
        return ConvergenceTester(output_dir=str(temp_output_dir))
    
    def test_quick_mode_execution(self, tester):
        """Test that quick mode runs with reduced test set"""
        with patch.object(tester, 'get_test_documents') as mock_docs:
            # Mock to return a smaller set
            mock_docs.return_value = [Path("tests/fixtures/verbose_prose.md")]
            
            results = tester.run_test_matrix(quick_mode=True)
            
            # Quick mode should limit total tests
            assert len(results["tests"]) <= 60
            assert results["metadata"]["mode"] == "quick"
            assert results["metadata"]["max_rounds"] == 5  # Reduced rounds in quick mode


if __name__ == "__main__":
    pytest.main([__file__, "-v"])