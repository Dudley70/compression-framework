"""
Multi-layered safety validation system for compression operations (Task 2.3).

This module implements comprehensive safety checks to prevent information loss
during compression. It uses a 4-layer architecture:

1. Pre-check: Already compressed detection (uses compression_score.py)
2. Entity preservation: NER + technical extraction (≥80% threshold)
3. Minimal benefit: Compression ratio check (≤0.85 threshold)
4. Semantic similarity: Meaning preservation (≥0.75 threshold)

Safety-First Philosophy: When in doubt, refuse compression.
Better to refuse a safe compression than accept an unsafe one.

Author: Claude (Task 2.3 Implementation)
Date: 2025-10-31
"""

import sys
import os
import re
import time
from typing import Dict, List, Set, Any, Optional

# Add scripts directory to path for imports
sys.path.append(os.path.dirname(__file__))

# Core dependencies
import spacy
from sentence_transformers import SentenceTransformer
import tiktoken
from sklearn.metrics.pairwise import cosine_similarity

# Internal dependencies (from previous tasks)
from compression_score import CompressionScorer


class SafetyValidator:
    """
    Multi-layered safety validation for compression operations.

    Implements 4 independent safety checks:
    1. Pre-check: Already compressed detection
    2. Entity preservation: Technical term and entity preservation
    3. Minimal benefit: Compression ratio validation
    4. Semantic similarity: Meaning preservation

    Integration with previous tasks:
    - Uses compression_score.py (TASK-2.1) for pre-check
    - Compatible with mock_compressor.py (TASK-2.2)
    - Can integrate with analyze_compression_state.py (TASK-1.1)
    """

    def __init__(self):
        """
        Initialize SafetyValidator with all required models and components.

        Loads:
        - Compression scorer (from TASK-2.1)
        - spaCy NLP model for entity recognition
        - Sentence transformer for semantic similarity
        - tiktoken for token counting
        """
        print("Initializing SafetyValidator...")

        # Initialize compression scorer (TASK-2.1 integration)
        self.scorer = CompressionScorer()

        # Initialize spaCy for entity recognition
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise RuntimeError(
                "spaCy English model not found. Please install with:\n"
                "python -m spacy download en_core_web_sm"
            )

        # Initialize sentence transformer for semantic similarity
        print("Loading sentence transformer model...")
        self.similarity_model = SentenceTransformer('all-MiniLM-L6-v2')

        # Initialize tiktoken for accurate token counting
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

        # Safety thresholds (tunable)
        self.compression_refusal_threshold = 0.8   # score >= 0.8 → refuse
        self.entity_preservation_threshold = 0.80  # must preserve ≥80%
        self.minimal_benefit_threshold = 0.85      # compression ratio > 0.85 → refuse
        self.semantic_similarity_threshold = 0.75  # similarity ≥ 0.75

        print("SafetyValidator initialized successfully.")

    def validate_compression(self, original_text: str, compressed_text: str,
                           parameters: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Run all safety checks on a compression operation.

        Args:
            original_text: Pre-compression text
            compressed_text: Post-compression text
            parameters: Optional compression parameters {sigma, gamma, kappa}

        Returns:
            {
                "safe": True/False,
                "checks": {
                    "pre_check": {...},
                    "entity_preservation": {...},
                    "minimal_benefit": {...},
                    "semantic_similarity": {...}
                },
                "failures": [...],  # List of failed checks
                "recommendation": "accept" | "refuse" | "warn",
                "summary": "Human-readable summary"
            }
        """
        if parameters is None:
            parameters = {}

        checks = {}
        failures = []

        # Step 1: Pre-check - refuse if already compressed
        checks["pre_check"] = self.pre_check_already_compressed(original_text)

        if not checks["pre_check"]["passed"]:
            # Pre-check failure stops all processing
            failures.append({
                "check": "pre_check",
                "message": checks["pre_check"]["message"]
            })

            return {
                "safe": False,
                "checks": checks,
                "failures": failures,
                "recommendation": "refuse",
                "summary": "Pre-check failed: content already compressed"
            }

        # Step 2-4: Run remaining safety checks
        checks["entity_preservation"] = self.check_entity_preservation(original_text, compressed_text)
        checks["minimal_benefit"] = self.check_minimal_benefit(original_text, compressed_text)
        checks["semantic_similarity"] = self.check_semantic_similarity(original_text, compressed_text)

        # Collect failures from post-checks
        for check_name, result in checks.items():
            if check_name != "pre_check" and not result["passed"]:
                failures.append({
                    "check": check_name,
                    "message": result["message"]
                })

        # Determine recommendation based on failure pattern
        if len(failures) == 0:
            recommendation = "accept"  # All checks passed
            safe = True
        elif len(failures) == 1:
            recommendation = "warn"   # One check failed, might be acceptable
            safe = False
        else:
            recommendation = "refuse" # Multiple failures
            safe = False

        return {
            "safe": safe,
            "checks": checks,
            "failures": failures,
            "recommendation": recommendation,
            "summary": self._generate_summary(checks, failures)
        }

    def pre_check_already_compressed(self, text: str) -> Dict[str, Any]:
        """
        Pre-check: Is content already compressed?

        Uses compression_score.py (TASK-2.1) to detect already compressed content.
        Refuses compression if score >= 0.8 (already compressed).

        Args:
            text: Text to check for compression

        Returns:
            {
                "passed": True/False,
                "score": 0.82,
                "threshold": 0.8,
                "message": "..."
            }
        """
        try:
            score_result = self.scorer.calculate_score(text)
            score = score_result["overall_score"]

            passed = score < self.compression_refusal_threshold

            if passed:
                message = "Pre-check passed"
            else:
                message = f"Content already compressed (score: {score:.2f})"

            return {
                "passed": passed,
                "score": score,
                "threshold": self.compression_refusal_threshold,
                "message": message
            }

        except Exception as e:
            # Handle errors gracefully
            return {
                "passed": False,
                "score": 1.0,  # Assume compressed on error
                "threshold": self.compression_refusal_threshold,
                "message": f"Pre-check error: {str(e)}"
            }

    def check_entity_preservation(self, original: str, compressed: str) -> Dict[str, Any]:
        """
        Check if entities (names, technical terms, API endpoints) are preserved.

        Uses spaCy NER to extract standard entities plus custom technical extraction
        for API paths, code identifiers, and technical acronyms.

        Args:
            original: Original text
            compressed: Compressed text

        Returns:
            {
                "passed": True/False,
                "original_entities": 25,
                "preserved_entities": 24,
                "preservation_rate": 0.96,
                "threshold": 0.80,
                "lost_entities": ["EntityName"],
                "message": "..."
            }
        """
        try:
            # Extract entities using spaCy NER
            orig_doc = self.nlp(original)
            comp_doc = self.nlp(compressed)

            # Get entity text (unique, case-insensitive)
            orig_entities = set(ent.text.lower() for ent in orig_doc.ents)
            comp_entities = set(ent.text.lower() for ent in comp_doc.ents)

            # Add technical entities not caught by spaCy
            orig_entities.update(self._extract_technical_entities(original))
            comp_entities.update(self._extract_technical_entities(compressed))

            # Handle edge case: no entities to preserve
            if len(orig_entities) == 0:
                return {
                    "passed": True,
                    "original_entities": 0,
                    "preserved_entities": 0,
                    "preservation_rate": 1.0,
                    "threshold": self.entity_preservation_threshold,
                    "lost_entities": [],
                    "message": "No entities to preserve"
                }

            # Calculate preservation metrics
            preserved_entities = orig_entities & comp_entities
            preserved_count = len(preserved_entities)
            rate = preserved_count / len(orig_entities)
            passed = rate >= self.entity_preservation_threshold

            # Identify lost entities (limit to first 5 for readability)
            lost = orig_entities - comp_entities
            lost_list = sorted(list(lost))[:5]

            # Generate message
            if passed:
                message = f"Preserved {rate*100:.1f}% of entities"
            else:
                lost_summary = ", ".join(lost_list)
                if len(lost) > 5:
                    lost_summary += f" (and {len(lost)-5} more)"
                message = f"Only {rate*100:.1f}% entities preserved (lost: {lost_summary})"

            return {
                "passed": passed,
                "original_entities": len(orig_entities),
                "preserved_entities": preserved_count,
                "preservation_rate": rate,
                "threshold": self.entity_preservation_threshold,
                "lost_entities": lost_list,
                "message": message
            }

        except Exception as e:
            # Handle errors gracefully - assume failure for safety
            return {
                "passed": False,
                "original_entities": 0,
                "preserved_entities": 0,
                "preservation_rate": 0.0,
                "threshold": self.entity_preservation_threshold,
                "lost_entities": [],
                "message": f"Entity preservation check error: {str(e)}"
            }

    def _extract_technical_entities(self, text: str) -> Set[str]:
        """
        Extract technical entities not caught by spaCy NER.

        Detects:
        - API paths: /api/users, /auth
        - Code identifiers: camelCase, snake_case
        - Technical acronyms: HTTP, API, JSON (2-5 letters, all caps)
        - File extensions: .py, .js, .md
        - Environment variables: ALL_CAPS_NAMES

        Args:
            text: Text to extract technical entities from

        Returns:
            Set of technical entities (lowercase for consistency)
        """
        entities = set()

        # API paths (e.g., /api/users, /auth/login)
        api_paths = re.findall(r'/[\w/\-]+', text)
        entities.update(path.lower() for path in api_paths)

        # Snake_case identifiers
        snake_case = re.findall(r'\b[a-z]+_[a-z_]+\b', text)
        entities.update(identifier.lower() for identifier in snake_case)

        # camelCase identifiers
        camel_case = re.findall(r'\b[a-z]+[A-Z][a-zA-Z]+\b', text)
        entities.update(identifier.lower() for identifier in camel_case)

        # Technical acronyms (2-5 letters, all caps)
        acronyms = re.findall(r'\b[A-Z]{2,5}\b', text)
        entities.update(acronym.lower() for acronym in acronyms)

        # File extensions
        extensions = re.findall(r'\.[a-z]{2,4}\b', text)
        entities.update(ext.lower() for ext in extensions)

        # Environment variables (ALL_CAPS with underscores)
        env_vars = re.findall(r'\b[A-Z][A-Z_]{2,}\b', text)
        entities.update(var.lower() for var in env_vars)

        # URLs and domains
        urls = re.findall(r'https?://[\w\.-]+', text)
        entities.update(url.lower() for url in urls)

        return entities

    def check_minimal_benefit(self, original: str, compressed: str) -> Dict[str, Any]:
        """
        Check if compression provides sufficient benefit.

        If compression ratio > 0.85 (only 15% reduction), risk vs benefit too high.
        Uses tiktoken for accurate token counting.

        Args:
            original: Original text
            compressed: Compressed text

        Returns:
            {
                "passed": True/False,
                "original_tokens": 1000,
                "compressed_tokens": 900,
                "compression_ratio": 0.90,
                "reduction_pct": 10.0,
                "threshold": 0.85,
                "message": "..."
            }
        """
        try:
            # Count tokens using tiktoken
            orig_tokens = len(self.tokenizer.encode(original))
            comp_tokens = len(self.tokenizer.encode(compressed))

            # Handle edge case: empty text
            if orig_tokens == 0:
                return {
                    "passed": False,
                    "original_tokens": 0,
                    "compressed_tokens": comp_tokens,
                    "compression_ratio": float('inf') if comp_tokens > 0 else 0.0,
                    "reduction_pct": 0.0,
                    "threshold": self.minimal_benefit_threshold,
                    "message": "Cannot compress empty text"
                }

            # Calculate compression metrics
            ratio = comp_tokens / orig_tokens
            reduction = (1 - ratio) * 100

            # Check against threshold
            passed = ratio <= self.minimal_benefit_threshold

            # Generate message
            if passed:
                message = f"Compression achieves {reduction:.1f}% reduction"
            else:
                if ratio > 1.0:
                    message = f"Text expanded by {(ratio - 1) * 100:.1f}% - not compressed"
                else:
                    message = f"Only {reduction:.1f}% reduction - insufficient benefit"

            return {
                "passed": passed,
                "original_tokens": orig_tokens,
                "compressed_tokens": comp_tokens,
                "compression_ratio": ratio,
                "reduction_pct": reduction,
                "threshold": self.minimal_benefit_threshold,
                "message": message
            }

        except Exception as e:
            # Handle errors gracefully - assume failure for safety
            return {
                "passed": False,
                "original_tokens": 0,
                "compressed_tokens": 0,
                "compression_ratio": 1.0,
                "reduction_pct": 0.0,
                "threshold": self.minimal_benefit_threshold,
                "message": f"Minimal benefit check error: {str(e)}"
            }

    def check_semantic_similarity(self, original: str, compressed: str) -> Dict[str, Any]:
        """
        Check if meaning is preserved using sentence embeddings.

        Uses sentence-transformers to compute cosine similarity between
        original and compressed text embeddings.

        Args:
            original: Original text
            compressed: Compressed text

        Returns:
            {
                "passed": True/False,
                "similarity_score": 0.82,
                "threshold": 0.75,
                "message": "..."
            }
        """
        try:
            # Handle edge cases
            if not original.strip() or not compressed.strip():
                return {
                    "passed": False,
                    "similarity_score": 0.0,
                    "threshold": self.semantic_similarity_threshold,
                    "message": "Cannot compare empty text"
                }

            if original.strip() == compressed.strip():
                return {
                    "passed": True,
                    "similarity_score": 1.0,
                    "threshold": self.semantic_similarity_threshold,
                    "message": "Identical text - perfect similarity"
                }

            # Generate embeddings
            orig_embedding = self.similarity_model.encode(original)
            comp_embedding = self.similarity_model.encode(compressed)

            # Compute cosine similarity
            similarity = cosine_similarity([orig_embedding], [comp_embedding])[0][0]

            # Convert to float for JSON serialization
            similarity = float(similarity)

            # Check against threshold
            passed = similarity >= self.semantic_similarity_threshold

            # Generate message
            if passed:
                message = f"Semantic similarity: {similarity:.3f}"
            else:
                message = f"Semantic similarity: {similarity:.3f} - meaning significantly changed"

            return {
                "passed": passed,
                "similarity_score": similarity,
                "threshold": self.semantic_similarity_threshold,
                "message": message
            }

        except Exception as e:
            # Handle errors gracefully - assume failure for safety
            return {
                "passed": False,
                "similarity_score": 0.0,
                "threshold": self.semantic_similarity_threshold,
                "message": f"Semantic similarity check error: {str(e)}"
            }

    def _generate_summary(self, checks: Dict[str, Dict], failures: List[Dict]) -> str:
        """
        Generate human-readable summary of validation results.

        Args:
            checks: All check results
            failures: List of failed checks

        Returns:
            Human-readable summary string
        """
        if len(failures) == 0:
            return "All safety checks passed. Compression is safe."

        if "pre_check" in [f["check"] for f in failures]:
            return "Content already compressed - compression refused."

        failed_checks = [f["check"].replace("_", " ") for f in failures]

        if len(failures) == 1:
            return f"Safety concern: {failed_checks[0]} - review recommended."
        else:
            return f"Multiple safety concerns: {', '.join(failed_checks)} - compression refused."


# Utility functions for external use
def quick_safety_check(original: str, compressed: str) -> bool:
    """
    Quick safety check returning simple True/False.

    Args:
        original: Original text
        compressed: Compressed text

    Returns:
        True if compression is safe, False otherwise
    """
    validator = SafetyValidator()
    result = validator.validate_compression(original, compressed)
    return result["safe"]


def detailed_safety_report(original: str, compressed: str,
                          parameters: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Generate detailed safety report for compression operation.

    Args:
        original: Original text
        compressed: Compressed text
        parameters: Optional compression parameters

    Returns:
        Complete safety validation report
    """
    validator = SafetyValidator()
    return validator.validate_compression(original, compressed, parameters)


if __name__ == "__main__":
    # Example usage and testing
    print("Safety Checks Implementation (Task 2.3)")
    print("=" * 50)

    # Initialize validator
    validator = SafetyValidator()

    # Example 1: Good compression
    original = """
    This is a very verbose document that contains a lot of detailed information
    about user authentication systems. The document explains in great detail
    how the authentication process works, including credential validation,
    token generation, and session management procedures.
    """

    compressed = """
    User authentication system documentation covering credential validation,
    token generation, and session management.
    """

    print("\nExample 1: Good Compression")
    result = validator.validate_compression(original, compressed)
    print(f"Safe: {result['safe']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"Summary: {result['summary']}")

    # Example 2: Already compressed
    already_compressed = "Auth: JWT tokens, validation, session mgmt."
    fake_compressed = "Auth: JWT, validation, sessions."

    print("\nExample 2: Already Compressed")
    result = validator.validate_compression(already_compressed, fake_compressed)
    print(f"Safe: {result['safe']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"Summary: {result['summary']}")

    print("\nSafety Checks Implementation Complete!")