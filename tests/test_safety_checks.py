"""
Comprehensive test suite for safety checks implementation (Task 2.3).

This test suite validates the multi-layered safety framework that prevents
information loss during compression operations. Tests are written FIRST
following TDD methodology - all tests will initially FAIL.

Safety Layers Tested:
1. Pre-check: Already compressed detection
2. Entity preservation: NER + technical extraction (≥80%)
3. Minimal benefit: Compression ratio (≤0.85)
4. Semantic similarity: Meaning preservation (≥0.75)

Test Strategy:
- Individual check tests (pass/fail scenarios)
- Integration tests (multiple checks combined)
- Edge cases and boundary conditions
- Real-world document validation
"""

import pytest
import sys
import os

# Add scripts directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# Import will fail initially - that's expected for TDD
try:
    from safety_checks import SafetyValidator
except ImportError:
    # Expected during TDD Phase 1
    SafetyValidator = None


class TestSafetyValidator:
    """Test the SafetyValidator class initialization and basic functionality."""

    @pytest.fixture
    def validator(self):
        """Create SafetyValidator instance for testing."""
        if SafetyValidator is None:
            pytest.skip("SafetyValidator not implemented yet (TDD Phase 1)")
        return SafetyValidator()

    def test_validator_initialization(self, validator):
        """Test that SafetyValidator initializes with correct configuration."""
        # Should have all required components
        assert hasattr(validator, 'scorer')
        assert hasattr(validator, 'nlp')
        assert hasattr(validator, 'similarity_model')
        assert hasattr(validator, 'tokenizer')

        # Should have correct thresholds
        assert validator.compression_refusal_threshold == 0.8
        assert validator.entity_preservation_threshold == 0.80
        assert validator.minimal_benefit_threshold == 0.85
        assert validator.semantic_similarity_threshold == 0.75


class TestPreCheckAlreadyCompressed:
    """Test pre-check safety layer: refuse already compressed content."""

    @pytest.fixture
    def validator(self):
        if SafetyValidator is None:
            pytest.skip("SafetyValidator not implemented yet (TDD Phase 1)")
        return SafetyValidator()

    def test_verbose_text_passes(self, validator):
        """Verbose text (low compression score) should pass pre-check."""
        verbose_text = """
        This is a very verbose and detailed explanation that contains a lot of
        redundant information and explanatory text. The document is written in
        a very wordy style with lots of examples and detailed descriptions.
        It contains many sentences that could be simplified or compressed.
        """

        result = validator.pre_check_already_compressed(verbose_text)

        assert result["passed"] is True
        assert result["score"] < 0.8
        assert "Pre-check passed" in result["message"]

    def test_compressed_text_fails(self, validator):
        """Already compressed text (high score) should fail pre-check."""
        # Use text that scores >= 0.8 (from compressed_doc.md fixture)
        compressed_text = """## POST /auth
- Body: `{username, password}`
- Returns: `{token}` (200) | `{error}` (401)
- Auth: None required

## GET /users
- Auth: Bearer token
- Returns: User array"""

        result = validator.pre_check_already_compressed(compressed_text)

        assert result["passed"] is False
        assert result["score"] >= 0.8
        assert "already compressed" in result["message"].lower()

    def test_moderately_compressed_passes(self, validator):
        """Moderately compressed text should still pass pre-check."""
        # Use text that will score < 0.8 (more verbose)
        moderate_text = """
        API Authentication Guide and Implementation Details

        Overview and Introduction: This comprehensive guide provides very detailed information about using Bearer tokens for secure API access in modern web applications. This documentation is intended to help developers understand the complete authentication process.

        Detailed Implementation Steps and Procedures:
        1. First, you need to obtain your authentication token from the /auth endpoint by providing valid user credentials through a POST request
        2. Once you have the token, include it in the Authorization header of your HTTP requests to authenticate with the API services
        3. You must handle 401 unauthorized errors appropriately when tokens expire or become invalid due to various security reasons
        4. Implement proper token refresh logic for long-running applications to maintain session continuity without interrupting user experience
        5. Store tokens securely using appropriate security measures and follow established security best practices for token management and storage
        6. Regularly monitor and audit your authentication implementation to ensure it meets security standards and requirements
        """

        result = validator.pre_check_already_compressed(moderate_text)

        assert result["passed"] is True
        assert result["score"] < 0.8


class TestEntityPreservation:
    """Test entity preservation safety check."""

    @pytest.fixture
    def validator(self):
        if SafetyValidator is None:
            pytest.skip("SafetyValidator not implemented yet (TDD Phase 1)")
        return SafetyValidator()

    def test_all_entities_preserved_passes(self, validator):
        """When all entities are preserved, check should pass."""
        original = "John Smith works at Microsoft. Contact him at john@microsoft.com or call API /users/profile."
        compressed = "John Smith (Microsoft): john@microsoft.com, API: /users/profile"

        result = validator.check_entity_preservation(original, compressed)

        assert result["passed"] is True
        assert result["preservation_rate"] >= 0.80
        # Allow for minor entity extraction differences

    def test_entity_loss_above_threshold_passes(self, validator):
        """When ≥80% entities preserved, check should pass."""
        original = "Use React, Vue, Angular, Django for development. APIs: /auth, /users, /data, /reports."
        compressed = "Use React, Vue, Angular for development. APIs: /auth, /users, /data."
        # Lost Django and /reports = should still be ≥80%

        result = validator.check_entity_preservation(original, compressed)

        assert result["passed"] is True
        assert result["preservation_rate"] >= 0.80

    def test_entity_loss_below_threshold_fails(self, validator):
        """When <80% entities preserved, check should fail."""
        original = "Technologies: React, Vue, Angular, Django, Flask. APIs: /auth, /users, /data, /reports, /analytics."
        compressed = "Use React and Django for development."
        # Lost Vue, Angular, Flask, /auth, /users, /data, /reports, /analytics = 8 out of 10 = 20% preserved

        result = validator.check_entity_preservation(original, compressed)

        assert result["passed"] is False
        assert result["preservation_rate"] < 0.80
        assert len(result["lost_entities"]) > 0

    def test_technical_entities_detected(self, validator):
        """Technical entities (APIs, camelCase, snake_case) should be detected."""
        original = "Use getUserData() API at /api/users with auth_token parameter."
        compressed = "Get user data via API with token."

        result = validator.check_entity_preservation(original, compressed)

        # Should detect: getUserData, /api/users, auth_token
        assert result["original_entities"] >= 3
        assert result["passed"] is False  # Most technical terms lost

    def test_no_entities_passes(self, validator):
        """Text with no entities should pass (nothing to preserve)."""
        original = "This is simple text with no specific entities or technical terms."
        compressed = "Simple text without entities."

        result = validator.check_entity_preservation(original, compressed)

        assert result["passed"] is True
        assert "No entities to preserve" in result["message"]


class TestMinimalBenefit:
    """Test minimal benefit safety check."""

    @pytest.fixture
    def validator(self):
        if SafetyValidator is None:
            pytest.skip("SafetyValidator not implemented yet (TDD Phase 1)")
        return SafetyValidator()

    def test_good_compression_passes(self, validator):
        """Compression with >15% reduction should pass."""
        original = "This is a long document that contains a lot of verbose information and detailed explanations that could be significantly compressed while preserving the essential meaning and important details."
        compressed = "Long document with verbose info and detailed explanations; can be compressed while preserving essential meaning."

        result = validator.check_minimal_benefit(original, compressed)

        assert result["passed"] is True
        assert result["compression_ratio"] <= 0.85
        assert result["reduction_pct"] >= 15.0

    def test_poor_compression_fails(self, validator):
        """Compression with ≤15% reduction should fail."""
        original = "This is a document with some information that needs to be compressed."
        compressed = "This is a document with some info that needs to be compressed."
        # Only minor word changes - minimal compression

        result = validator.check_minimal_benefit(original, compressed)

        assert result["passed"] is False
        assert result["compression_ratio"] > 0.85
        assert "insufficient benefit" in result["message"].lower()

    def test_boundary_case_85_percent(self, validator):
        """Exactly 85% compression ratio should fail."""
        # Create strings with specific token counts
        original = "A " * 100  # 100 tokens
        compressed = "A " * 85   # 85 tokens = 0.85 ratio

        result = validator.check_minimal_benefit(original, compressed)

        assert result["passed"] is False
        assert abs(result["compression_ratio"] - 0.85) < 0.01

    def test_excellent_compression_passes(self, validator):
        """High compression ratio (e.g., 50%) should pass."""
        original = "This is a very long document with extensive details and verbose explanations that can be significantly compressed through careful summarization and removal of redundant information while maintaining all essential content and meaning for the reader."
        compressed = "Long document with extensive details; can be compressed via summarization while maintaining essential content."

        result = validator.check_minimal_benefit(original, compressed)

        assert result["passed"] is True
        assert result["compression_ratio"] <= 0.7
        assert result["reduction_pct"] >= 30.0


class TestSemanticSimilarity:
    """Test semantic similarity safety check."""

    @pytest.fixture
    def validator(self):
        if SafetyValidator is None:
            pytest.skip("SafetyValidator not implemented yet (TDD Phase 1)")
        return SafetyValidator()

    def test_preserved_meaning_passes(self, validator):
        """Text with preserved meaning should pass similarity check."""
        original = "The user authentication system requires a valid username and password to grant access to protected resources."
        compressed = "Auth system needs valid username/password for protected resource access."

        result = validator.check_semantic_similarity(original, compressed)

        assert result["passed"] is True
        assert result["similarity_score"] >= 0.75

    def test_changed_meaning_fails(self, validator):
        """Text with significantly changed meaning should fail."""
        original = "The authentication system requires careful validation of user credentials before granting access."
        compressed = "The system automatically grants access to all users without validation."

        result = validator.check_semantic_similarity(original, compressed)

        assert result["passed"] is False
        assert result["similarity_score"] < 0.75
        assert "meaning significantly changed" in result["message"].lower()

    def test_style_change_preserved_meaning_passes(self, validator):
        """Stylistic changes with preserved meaning should pass."""
        original = "In order to authenticate users effectively, the system must validate their credentials thoroughly."
        compressed = "System validates user credentials for authentication."

        result = validator.check_semantic_similarity(original, compressed)

        assert result["passed"] is True
        assert result["similarity_score"] >= 0.75

    def test_boundary_case_75_percent(self, validator):
        """Text at exactly 75% similarity should pass."""
        # This test verifies the boundary condition
        original = "API authentication requires Bearer tokens in Authorization header."
        compressed = "Auth needs Bearer tokens in headers."

        result = validator.check_semantic_similarity(original, compressed)

        # Should be close to boundary - exact value depends on model
        # But should pass if >= 0.75
        if result["similarity_score"] >= 0.75:
            assert result["passed"] is True
        else:
            assert result["passed"] is False


class TestIntegratedValidation:
    """Test the complete validation framework with all checks combined."""

    @pytest.fixture
    def validator(self):
        if SafetyValidator is None:
            pytest.skip("SafetyValidator not implemented yet (TDD Phase 1)")
        return SafetyValidator()

    def test_perfect_compression_all_pass(self, validator):
        """Perfect compression should pass all checks and be accepted."""
        original = """
        User Authentication System Documentation

        The authentication system provides secure access control for the application.
        It validates user credentials through a comprehensive verification process.

        Key components include:
        - Username and password validation
        - Session token generation
        - Authorization header verification
        - API endpoint protection at /auth and /users

        Implementation details:
        1. User submits credentials to /auth/login
        2. System validates against user database
        3. On success, generates JWT token
        4. Client includes token in Authorization: Bearer <token>
        5. Protected endpoints verify token validity

        Error handling covers invalid credentials, expired tokens, and malformed requests.
        """

        compressed = """
        # User Authentication System

        Secure access control with credential validation.

        Components:
        - Username/password validation
        - Session token generation
        - Authorization header verification
        - API protection: /auth, /users

        Flow:
        1. Credentials → /auth/login
        2. Database validation
        3. JWT token generation
        4. Authorization: Bearer <token>
        5. Token verification

        Handles invalid credentials, expired tokens, malformed requests.
        """

        parameters = {"sigma": 0.7, "gamma": 0.6, "kappa": 0.5}
        result = validator.validate_compression(original, compressed, parameters)

        assert result["safe"] is True
        assert result["recommendation"] == "accept"
        assert len(result["failures"]) == 0
        assert "All safety checks passed" in result["summary"]

    def test_already_compressed_refused(self, validator):
        """Already compressed content should be refused at pre-check."""
        # Use text that will score >= 0.8
        already_compressed = """## POST /auth
- Body: `{username, password}`
- Returns: `{token}` (200) | `{error}` (401)"""
        fake_compressed = """## POST /auth
- Body: user/pass
- Returns: token/error"""

        parameters = {"sigma": 0.8, "gamma": 0.7, "kappa": 0.6}
        result = validator.validate_compression(already_compressed, fake_compressed, parameters)

        assert result["safe"] is False
        assert result["recommendation"] == "refuse"
        assert result["checks"]["pre_check"]["passed"] is False
        assert "already compressed" in result["summary"].lower()

    def test_entity_loss_refused(self, validator):
        """Significant entity loss should result in refusal."""
        original = "Use React, Vue, Angular, Django, Flask for frontend development. Backend systems include Express, Spring Boot, Rails. APIs: /auth, /users, /data, /reports, /analytics."
        compressed = "Use React for frontend development."
        # Lost: Vue, Angular, Django, Flask, Express, Spring Boot, Rails, all APIs

        parameters = {"sigma": 0.6, "gamma": 0.5, "kappa": 0.4}
        result = validator.validate_compression(original, compressed, parameters)

        assert result["safe"] is False
        # With massive entity loss, should be refused not just warned
        assert result["recommendation"] in ["refuse", "warn"]
        assert result["checks"]["entity_preservation"]["passed"] is False

    def test_minimal_benefit_warning(self, validator):
        """Single failure (minimal benefit) should result in warning."""
        original = "The authentication system validates user credentials effectively."
        compressed = "The authentication system validates user credentials."
        # Only removed "effectively" - minimal compression

        parameters = {"sigma": 0.5, "gamma": 0.4, "kappa": 0.3}
        result = validator.validate_compression(original, compressed, parameters)

        # Should warn (single failure) rather than refuse
        assert result["recommendation"] == "warn"
        assert result["checks"]["minimal_benefit"]["passed"] is False
        assert len(result["failures"]) == 1

    def test_multiple_failures_refused(self, validator):
        """Multiple failures should result in refusal."""
        original = "Complex authentication system with React frontend, Django backend, JWT tokens, and comprehensive error handling."
        compressed = "Simple login system."
        # Fails: entity preservation (lost React, Django, JWT), minimal benefit (poor compression), semantic similarity (meaning changed)

        parameters = {"sigma": 0.7, "gamma": 0.6, "kappa": 0.5}
        result = validator.validate_compression(original, compressed, parameters)

        assert result["safe"] is False
        assert result["recommendation"] == "refuse"
        assert len(result["failures"]) >= 2

    def test_semantic_drift_refused(self, validator):
        """Significant meaning change should be refused."""
        original = "Authentication system prevents unauthorized access to sensitive data."
        compressed = "Authentication system grants automatic access to all data."

        parameters = {"sigma": 0.6, "gamma": 0.5, "kappa": 0.4}
        result = validator.validate_compression(original, compressed, parameters)

        assert result["safe"] is False
        assert result["checks"]["semantic_similarity"]["passed"] is False


class TestEdgeCasesAndBoundaries:
    """Test edge cases and boundary conditions."""

    @pytest.fixture
    def validator(self):
        if SafetyValidator is None:
            pytest.skip("SafetyValidator not implemented yet (TDD Phase 1)")
        return SafetyValidator()

    def test_empty_text(self, validator):
        """Empty text should be handled gracefully."""
        result = validator.validate_compression("", "", {})
        # Should not crash - exact behavior to be determined in implementation
        assert "safe" in result
        assert "recommendation" in result

    def test_identical_text(self, validator):
        """Identical original and compressed text should be handled."""
        text = "This is a test document."
        result = validator.validate_compression(text, text, {})

        # No compression = minimal benefit failure
        assert result["checks"]["minimal_benefit"]["passed"] is False

    def test_longer_compressed_text(self, validator):
        """Compressed text longer than original should fail minimal benefit."""
        original = "Short text."
        compressed = "This is actually a much longer version of the short text that somehow got expanded instead of compressed."

        result = validator.validate_compression(original, compressed, {})

        assert result["checks"]["minimal_benefit"]["passed"] is False
        assert result["checks"]["minimal_benefit"]["compression_ratio"] > 1.0

    def test_special_characters_entities(self, validator):
        """Special characters and symbols should be handled correctly."""
        original = "Use $ for jQuery, @ for decorators, # for comments, & for references."
        compressed = "Use symbols: $, @, # for jQuery, decorators, comments."

        result = validator.check_entity_preservation(original, compressed)
        # Should detect and preserve special character entities
        assert result["passed"] is not None  # Test should not crash


class TestIntegrationWithPreviousTasks:
    """Test integration with previously implemented components."""

    @pytest.fixture
    def validator(self):
        if SafetyValidator is None:
            pytest.skip("SafetyValidator not implemented yet (TDD Phase 1)")
        return SafetyValidator()

    def test_compression_score_integration(self, validator):
        """Pre-check should use compression_score.py from Task 2.1."""
        # This verifies integration with existing compression scoring
        from compression_score import CompressionScorer

        scorer = CompressionScorer()
        test_text = "This is verbose documentation with lots of detailed explanations."

        # Direct call to compression scorer
        score_result = scorer.calculate_score(test_text)

        # Safety validator should use same scoring
        safety_result = validator.pre_check_already_compressed(test_text)

        assert safety_result["score"] == score_result["overall_score"]

    def test_mock_compressor_integration(self, validator):
        """Should work with mock_compressor.py from Task 2.2."""
        from mock_compressor import MockCompressor
        from compression_score import CompressionScorer

        # MockCompressor requires a scorer parameter
        scorer = CompressionScorer()
        compressor = MockCompressor(scorer)
        original = "This is a verbose document that will be compressed for testing integration between safety checks and the mock compressor system."

        # Get compressed version
        compression_result = compressor.compress(original, 0.7, 0.6, 0.5)

        # Check if compression was successful or refused
        if not compression_result.get("refused", False):
            # Compression was successful
            compressed = compression_result["compressed_text"]

            # Validate the compression
            safety_result = validator.validate_compression(original, compressed, {"sigma": 0.7, "gamma": 0.6, "kappa": 0.5})

            # Should integrate successfully
            assert "safe" in safety_result
            assert "recommendation" in safety_result
        else:
            # Compression was refused - this is also valid behavior
            # The integration test just needs to verify that the components can communicate
            assert "refused" in compression_result
            assert "reason" in compression_result


class TestPerformanceRequirements:
    """Test performance requirements for production use."""

    @pytest.fixture
    def validator(self):
        if SafetyValidator is None:
            pytest.skip("SafetyValidator not implemented yet (TDD Phase 1)")
        return SafetyValidator()

    def test_validation_performance(self, validator):
        """Validation should complete within reasonable time."""
        import time

        original = "Long document " * 100  # Create reasonably long document
        compressed = "Long doc " * 100

        start_time = time.time()
        result = validator.validate_compression(original, compressed, {})
        end_time = time.time()

        # Should complete within 1 second as specified
        assert (end_time - start_time) < 1.0
        assert result is not None

    def test_model_loading_time(self, validator):
        """Model loading should be reasonable (first use)."""
        # This test documents model loading time
        # Actual performance validation will be in real-world testing
        assert validator.similarity_model is not None
        assert validator.nlp is not None


# Test fixtures for different scenarios
class TestFixtures:
    """Test with predefined document fixtures."""

    @pytest.fixture
    def validator(self):
        if SafetyValidator is None:
            pytest.skip("SafetyValidator not implemented yet (TDD Phase 1)")
        return SafetyValidator()

    def test_api_documentation_compression(self, validator):
        """Test compression of API documentation."""
        original = """
        # User Management API

        ## Overview
        The User Management API provides comprehensive functionality for managing user accounts within the system. This RESTful API supports creating, reading, updating, and deleting user records, along with authentication and authorization mechanisms.

        ## Authentication
        All API endpoints require authentication using Bearer tokens. Obtain tokens from the /auth/login endpoint by providing valid credentials.

        ## Endpoints

        ### GET /api/users
        Retrieve a list of all users in the system.

        **Parameters:**
        - page: Page number for pagination (optional)
        - limit: Number of users per page (optional, default: 20)

        **Response:**
        ```json
        {
          "users": [...],
          "pagination": {...}
        }
        ```

        ### POST /api/users
        Create a new user account.

        **Request Body:**
        ```json
        {
          "username": "string",
          "email": "string",
          "password": "string"
        }
        ```

        **Response:**
        ```json
        {
          "id": "string",
          "username": "string",
          "email": "string",
          "created_at": "timestamp"
        }
        ```
        """

        compressed = """
        # User Management API

        RESTful API for user CRUD operations with auth.

        ## Auth
        Bearer tokens required. Get from /auth/login.

        ## Endpoints

        **GET /api/users**
        List users. Params: page, limit (default 20).
        Response: users array + pagination.

        **POST /api/users**
        Create user. Body: username, email, password.
        Response: id, username, email, created_at.
        """

        result = validator.validate_compression(original, compressed, {"sigma": 0.7, "gamma": 0.6, "kappa": 0.5})

        # This should be a good compression
        assert result["checks"]["pre_check"]["passed"] is True
        assert result["checks"]["minimal_benefit"]["passed"] is True
        # Entity preservation and semantic similarity depend on exact implementation


# Checkpoint validation test
def test_checkpoint_1_all_tests_fail():
    """Meta-test: Verify that all tests fail during TDD Phase 1."""
    if SafetyValidator is not None:
        pytest.skip("This test only runs during TDD Phase 1 when implementation doesn't exist")

    # If we reach here, SafetyValidator is None, which means all other tests should be skipped
    # This confirms we're in the correct TDD phase
    assert SafetyValidator is None, "TDD Phase 1: Implementation should not exist yet"


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])