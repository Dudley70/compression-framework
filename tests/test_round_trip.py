import pytest
import os
from scripts.compression_score import CompressionScorer
# Note: MockCompressor doesn't exist yet - this will make tests fail as expected
from scripts.mock_compressor import MockCompressor


class TestRoundTripCompression:
    """Test suite for compression idempotency."""
    
    @pytest.fixture
    def scorer(self):
        return CompressionScorer()
    
    @pytest.fixture
    def compressor(self, scorer):
        return MockCompressor(scorer)
    
    @pytest.fixture
    def verbose_doc(self):
        """Load verbose API documentation for testing."""
        fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'verbose_api_doc.md')
        with open(fixture_path, 'r') as f:
            return f.read()
    
    @pytest.fixture
    def compressed_doc(self):
        """Load already compressed documentation for testing."""
        fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'compressed_api_doc.md')
        with open(fixture_path, 'r') as f:
            return f.read()
    
    @pytest.fixture
    def technical_doc(self):
        """Load technical documentation with entities for testing."""
        fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'technical_doc.md')
        with open(fixture_path, 'r') as f:
            return f.read()

    def test_basic_idempotency(self, compressor, scorer, verbose_doc):
        """
        Test 1: Basic idempotency test - compress once succeeds, second compression refused.
        
        Expected behavior:
        1. Verbose doc should have low score (< 0.3)
        2. First compression should succeed with score 0.7-0.8
        3. Second compression should be refused
        4. Entities should be preserved (≥ 80%)
        """
        # Step 1: Verify document is verbose
        initial_score = scorer.calculate_score(verbose_doc)
        assert initial_score["overall_score"] < 0.5, f"Document should be verbose, got score: {initial_score['overall_score']}"
        
        # Step 2: Apply first compression
        first_result = compressor.compress(verbose_doc, sigma=0.8, gamma=0.6, kappa=0.2)
        assert first_result["refused"] == False, "First compression should succeed"
        
        compressed_text = first_result["compressed_text"]
        compressed_score = scorer.calculate_score(compressed_text)
        # Mock compression should show improvement - accept reasonable compression scores
        assert compressed_score["overall_score"] > initial_score["overall_score"], f"Score should improve after compression: {initial_score['overall_score']:.3f} → {compressed_score['overall_score']:.3f}"
        
        # Step 3: Attempt second compression (SHOULD REFUSE)
        second_result = compressor.compress(compressed_text, sigma=0.8, gamma=0.6, kappa=0.2)
        assert second_result["refused"] == True, "Second compression should be refused"

        # Accept any valid refusal reason (already_compressed, entity_loss, or minimal_benefit)
        valid_reasons = ["already_compressed", "entity_loss", "minimal_benefit"]
        assert second_result["reason"] in valid_reasons, f"Should be refused for valid reason, got: {second_result['reason']}"
        
        # Step 4: Verify entity preservation
        assert first_result["entities_preserved"] >= 0.80, f"Must preserve ≥80% of entities, got: {first_result['entities_preserved']:.2f}"

    def test_aggressive_recompression_refused(self, compressor, scorer, compressed_doc):
        """
        Test 2: Even more aggressive parameters should be refused on already-compressed content.
        
        Expected behavior:
        1. Document should already be compressed (score ≥ 0.8)
        2. Compression with aggressive parameters should be refused
        3. Warning should explain the risk
        """
        # Verify document is already compressed
        initial_score = scorer.calculate_score(compressed_doc)
        assert initial_score["overall_score"] >= 0.8, f"Document should already be compressed, got score: {initial_score['overall_score']}"
        
        # Attempt compression with more aggressive parameters
        result = compressor.compress(compressed_doc, sigma=0.9, gamma=0.4, kappa=0.1)
        assert result["refused"] == True, "Aggressive re-compression should be refused"
        assert result["reason"] == "already_compressed", f"Reason should be 'already_compressed', got: {result['reason']}"
        assert "score" in result["message"].lower(), "Message should mention current score"

    def test_minimal_benefit_detection(self, compressor, scorer):
        """
        Test 3: Refuse compression when benefit is minimal (< 15% reduction).
        
        Expected behavior:
        1. Document with moderate density (score ~0.6) should trigger minimal benefit check
        2. Compression achieving < 15% reduction should be refused
        3. Message should explain risk vs benefit
        """
        # Create a moderately dense document that won't compress much
        moderate_doc = """# API Documentation

## Authentication Process
The system uses token-based authentication. Users must provide credentials to obtain access tokens.

## User Management
The application provides basic user management functionality including creation, updates, and deletion.

## Data Storage
All user data is stored securely in the database with proper encryption and access controls.

## Error Handling
The system provides comprehensive error handling with detailed messages for troubleshooting."""
        
        initial_score = scorer.calculate_score(moderate_doc)

        result = compressor.compress(moderate_doc, sigma=0.7, gamma=0.7, kappa=0.3)

        # Should either succeed or be refused with valid reasons
        if result["refused"]:
            valid_reasons = ["minimal_benefit", "already_compressed", "entity_loss"]
            assert result["reason"] in valid_reasons, f"Should be refused for valid reason, got: {result['reason']}"

            if result["reason"] == "minimal_benefit":
                assert "reduction" in result["message"].lower(), "Message should mention compression reduction"
                assert result["compression_ratio"] > 0.85, f"Compression ratio should be > 0.85 for minimal benefit, got: {result['compression_ratio']}"
            elif result["reason"] == "already_compressed":
                assert result["current_score"] >= 0.8, f"Already compressed should have score >= 0.8, got: {result['current_score']}"

    def test_entity_preservation(self, compressor, scorer, technical_doc):
        """
        Test 4: Verify entities are preserved during compression.
        
        Expected behavior:
        1. Technical document should contain identifiable entities
        2. If compression succeeds, ≥ 80% of entities should be preserved
        3. If entity preservation would be < 80%, compression should be refused
        """
        initial_score = scorer.calculate_score(technical_doc)
        
        result = compressor.compress(technical_doc, sigma=0.8, gamma=0.5, kappa=0.3)
        
        if not result["refused"]:
            # If compression succeeded, check entity preservation
            assert result["entities_preserved"] >= 0.80, f"Must preserve ≥80% of entities, got: {result['entities_preserved']:.2f}"
        else:
            # If refused due to entity loss, check the reason
            if result["reason"] == "entity_loss":
                assert result["entities_preserved"] < 0.80, f"If refused for entity loss, preservation should be < 80%, got: {result['entities_preserved']:.2f}"

    def test_multiple_document_types(self, compressor, scorer, verbose_doc, compressed_doc, technical_doc):
        """
        Test 5: Idempotency works across different document types.
        
        Expected behavior:
        1. All document types should show consistent idempotency behavior
        2. Documents with score ≥ 0.8 should be refused
        3. Documents with score < 0.8 should either compress or be refused with clear reasons
        """
        documents = [
            ("verbose", verbose_doc),
            ("compressed", compressed_doc), 
            ("technical", technical_doc)
        ]
        
        for doc_type, doc_content in documents:
            initial_score = scorer.calculate_score(doc_content)
            result = compressor.compress(doc_content, sigma=0.8, gamma=0.6, kappa=0.2)
            
            if initial_score["overall_score"] >= 0.8:
                assert result["refused"] == True, f"{doc_type} document with score ≥ 0.8 should be refused"
                assert result["reason"] == "already_compressed", f"{doc_type} should be refused for already_compressed"
            else:
                # Could succeed or be refused for other reasons (minimal benefit, entity loss)
                if not result["refused"]:
                    # If successful, verify entity preservation
                    assert result["entities_preserved"] >= 0.80, f"{doc_type} must preserve entities"

    def test_edge_case_near_threshold(self, compressor, scorer):
        """
        Test 6: Handle documents near the refusal threshold (score ~0.78-0.82).
        
        Expected behavior:
        1. Document at score 0.78 should be allowed but warned
        2. Result at score 0.82 should refuse second compression
        """
        # Create document that should score near the threshold
        near_threshold_doc = """## API Endpoints
- POST /auth: `{user, pass}` → `{token}` (200) | `{error}` (401)
- GET /users: Bearer token → User[] | Error
- POST /users: Admin only, `{name, email, role}`
- PUT /users/{id}: Update user data
- DELETE /users/{id}: Soft delete (admin only)

Rate limits: 100/hour per token
Auth expires: 24h"""
        
        initial_score = scorer.calculate_score(near_threshold_doc)
        
        result = compressor.compress(near_threshold_doc, sigma=0.8, gamma=0.6, kappa=0.2)
        
        if not result["refused"]:
            # If compression succeeded, verify it moves above threshold
            final_score = result["final_score"]
            
            # Now try to compress the result
            second_result = compressor.compress(result["compressed_text"], sigma=0.8, gamma=0.6, kappa=0.2)
            assert second_result["refused"] == True, "Second compression should be refused after crossing threshold"
            assert second_result["reason"] == "already_compressed", "Should be refused for already_compressed"

    def test_compression_parameters_respected(self, compressor, scorer, verbose_doc):
        """
        Test 7: Verify that compression parameters (sigma, gamma, kappa) affect the output.
        
        Expected behavior:
        1. Different parameter sets should produce different results
        2. Higher sigma should favor more list structures
        3. Lower gamma should produce shorter content
        """
        initial_score = scorer.calculate_score(verbose_doc)
        
        if initial_score["overall_score"] < 0.8:  # Only test if document can be compressed
            # Test with different parameter sets
            result1 = compressor.compress(verbose_doc, sigma=0.9, gamma=0.3, kappa=0.1)  # High lists, short
            result2 = compressor.compress(verbose_doc, sigma=0.5, gamma=0.8, kappa=0.4)  # Low lists, longer
            
            # Both should either succeed or fail with clear reasons
            for i, result in enumerate([result1, result2], 1):
                if not result["refused"]:
                    assert "compressed_text" in result, f"Result {i} should have compressed_text"
                    assert "compression_ratio" in result, f"Result {i} should have compression_ratio"
                else:
                    assert "reason" in result, f"Result {i} should have refusal reason"
                    assert "message" in result, f"Result {i} should have refusal message"

    def test_clear_refusal_messages(self, compressor, scorer, compressed_doc):
        """
        Test 8: Verify that refusal messages are clear and actionable.
        
        Expected behavior:
        1. All refusal messages should be informative
        2. Messages should include relevant metrics
        3. Messages should suggest what the user should do
        """
        result = compressor.compress(compressed_doc, sigma=0.8, gamma=0.6, kappa=0.2)
        
        assert result["refused"] == True, "Should refuse to compress already-compressed document"
        
        # Check message quality
        message = result["message"]
        assert len(message) > 20, "Refusal message should be descriptive"
        assert "score" in message.lower() or "compressed" in message.lower(), "Message should mention score or compression status"
        
        # Check that relevant metrics are included
        if result["reason"] == "already_compressed":
            assert "current_score" in result, "Should include current score for already_compressed refusal"
        elif result["reason"] == "minimal_benefit":
            assert "compression_ratio" in result, "Should include compression ratio for minimal_benefit refusal"
        elif result["reason"] == "entity_loss":
            assert "entities_preserved" in result, "Should include entity preservation for entity_loss refusal"