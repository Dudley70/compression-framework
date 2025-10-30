"""
Mock Compression Implementation for Testing Round-Trip Idempotency

This module provides a MockCompressor class that simulates compression behavior
with comprehensive safety checks to prevent information loss. It's designed for
testing the idempotency logic before implementing actual compression algorithms.

The MockCompressor implements three key safety mechanisms:
1. Pre-check: Refuse compression if content is already compressed (score ≥ 0.8)
2. Post-check: Refuse if compression benefit is minimal (< 15% reduction)  
3. Post-check: Refuse if entity preservation is insufficient (< 80%)
"""

import tiktoken
import re
from typing import Dict, Any, List
from scripts.compression_score import CompressionScorer


class MockCompressor:
    """
    Mock compression for testing idempotency logic.
    In real tool, this would call actual compression algorithms.
    """
    
    def __init__(self, scorer: CompressionScorer):
        """
        Initialize MockCompressor with compression scorer.
        
        Args:
            scorer: CompressionScorer instance for measuring compression levels
        """
        self.scorer = scorer
        self.refusal_threshold = 0.8  # Refuse compression if score ≥ 0.8
        self.minimal_benefit_threshold = 0.85  # Refuse if compression ratio > 0.85
        self.entity_preservation_threshold = 0.80  # Require ≥ 80% entity preservation
        
        # Initialize tokenizer (same as compression_score.py)
        self.encoding = tiktoken.get_encoding("cl100k_base")
        
    def compress(self, text: str, sigma: float, gamma: float, kappa: float) -> Dict[str, Any]:
        """
        Mock compression with comprehensive safety checks.
        
        Args:
            text: Text content to compress
            sigma: List density parameter (0-1, higher = more lists)
            gamma: Prose ratio parameter (0-1, higher = more prose)  
            kappa: Explanation marker parameter (0-1, higher = more explanations)
            
        Returns:
            Dict containing either compression result or refusal with reason
        """
        # Input validation
        if not text or not text.strip():
            return {
                "refused": True,
                "reason": "empty_input",
                "message": "Cannot compress empty or whitespace-only content.",
            }
            
        # Parameter validation
        if not all(0 <= param <= 1 for param in [sigma, gamma, kappa]):
            return {
                "refused": True, 
                "reason": "invalid_parameters",
                "message": f"Parameters must be between 0 and 1. Got: σ={sigma}, γ={gamma}, κ={kappa}",
            }
        
        # PRE-CHECK: Already compressed?
        current_score = self.scorer.calculate_score(text)
        
        if current_score["overall_score"] >= self.refusal_threshold:
            return {
                "refused": True,
                "reason": "already_compressed",
                "message": f"Document already compressed (score: {current_score['overall_score']:.2f}). "
                          f"Refusing to prevent information loss. Threshold: {self.refusal_threshold}",
                "current_score": current_score["overall_score"],
                "threshold": self.refusal_threshold
            }
        
        # Calculate original metrics for comparison
        original_tokens = self._count_tokens(text)
        original_entities = self._extract_entities(text)
        
        # MOCK COMPRESSION: Apply simulated compression based on parameters
        compressed_text = self._mock_compress_text(text, sigma, gamma, kappa)
        compressed_tokens = self._count_tokens(compressed_text)
        compressed_entities = self._extract_entities(compressed_text)
        
        # POST-CHECK 1: Minimal benefit?
        compression_ratio = compressed_tokens / original_tokens if original_tokens > 0 else 1.0
        
        if compression_ratio > self.minimal_benefit_threshold:
            reduction_pct = (1 - compression_ratio) * 100
            return {
                "refused": True,
                "reason": "minimal_benefit", 
                "message": f"Compression achieves only {reduction_pct:.1f}% reduction "
                          f"(ratio: {compression_ratio:.3f}). Risk vs benefit too high. "
                          f"Minimum reduction required: {(1-self.minimal_benefit_threshold)*100:.1f}%",
                "compression_ratio": compression_ratio,
                "reduction_percent": reduction_pct,
                "threshold": self.minimal_benefit_threshold
            }
        
        # POST-CHECK 2: Entity preservation
        entities_preserved_ratio = self._check_entity_preservation(original_entities, compressed_entities)
        
        if entities_preserved_ratio < self.entity_preservation_threshold:
            entities_lost_pct = (1 - entities_preserved_ratio) * 100
            return {
                "refused": True,
                "reason": "entity_loss",
                "message": f"Compression would lose {entities_lost_pct:.1f}% of entities "
                          f"({len(original_entities)} → {len(compressed_entities)} entities). "
                          f"Refusing to prevent information loss. Minimum preservation: "
                          f"{self.entity_preservation_threshold*100:.0f}%",
                "entities_preserved": entities_preserved_ratio,
                "entities_original": len(original_entities),
                "entities_remaining": len(compressed_entities),
                "threshold": self.entity_preservation_threshold
            }
        
        # SUCCESS: Compression completed safely
        final_score = self.scorer.calculate_score(compressed_text)
        
        return {
            "refused": False,
            "compressed_text": compressed_text,
            "original_tokens": original_tokens,
            "compressed_tokens": compressed_tokens,
            "compression_ratio": compression_ratio,
            "reduction_percent": (1 - compression_ratio) * 100,
            "final_score": final_score["overall_score"],
            "original_score": current_score["overall_score"],
            "entities_preserved": entities_preserved_ratio,
            "entities_original": len(original_entities),
            "entities_remaining": len(compressed_entities),
            "parameters": {"sigma": sigma, "gamma": gamma, "kappa": kappa}
        }
    
    def _mock_compress_text(self, text: str, sigma: float, gamma: float, kappa: float) -> str:
        """
        Simulate compression based on parameters.
        Ensures actual compression occurs by removing verbose content.
        
        Args:
            text: Original text content
            sigma: List density (higher = more bullet points)
            gamma: Prose ratio (lower = shorter sentences)
            kappa: Explanation markers (lower = remove verbose explanations)
            
        Returns:
            Compressed text with transformations applied
        """
        lines = text.split('\n')
        compressed_lines = []
        
        # Track if we should compress more aggressively
        target_reduction = 0.3  # Aim for 30% reduction minimum
        
        for line in lines:
            line = line.strip()
            if not line:
                continue  # Skip empty lines entirely
                
            # Apply kappa: Remove verbose explanations first (most effective)
            if kappa < 0.5:
                line = self._remove_verbose_explanations(line)
                if not line:  # If line becomes empty after removing verbose parts
                    continue
            
            # Apply gamma: Shorten sentences
            if gamma < 0.6:
                line = self._shorten_sentence(line, gamma)
            
            # Apply sigma: Convert to structured bullet points
            if sigma > 0.6 and len(line) > 100 and not line.startswith(('- ', '* ', '1. ', '2. ', '#')):
                # Convert long explanatory paragraphs to concise bullet points
                key_points = self._extract_key_points(line)
                for point in key_points:
                    if point.strip():
                        compressed_lines.append(f"- {point.strip()}")
            else:
                # Keep the line if it's already structured or short enough
                if line.strip():
                    compressed_lines.append(line)
        
        # Additional aggressive compression if needed
        result = '\n'.join(compressed_lines)
        
        # Final cleanup - remove redundant content
        result = self._remove_redundancies(result)
        result = re.sub(r'\n\s*\n\s*\n+', '\n\n', result)  # Max 2 consecutive newlines
        
        # If we haven't achieved enough compression, do more aggressive reduction
        original_length = len(text)
        compressed_length = len(result)
        if compressed_length / original_length > 0.7:  # Less than 30% reduction
            result = self._aggressive_compress(result)
        
        return result.strip()
    
    def _remove_verbose_explanations(self, line: str) -> str:
        """Remove verbose explanatory phrases and redundant information."""
        # Remove entire sentences that are just verbose explanations
        verbose_sentence_patterns = [
            r'It is important to (understand|note|remember) that\s.*?[.!?]',
            r'It should be noted that\s.*?[.!?]',
            r'As (mentioned|noted|discussed) (before|above|earlier|previously),?\s.*?[.!?]',
            r'This (means|indicates|shows|demonstrates) that\s.*?[.!?]',
            r'In other words,?\s.*?[.!?]',
            r'To (illustrate|explain|clarify),?\s.*?[.!?]',
            r'(Additionally|Furthermore|Moreover),?\s.*?[.!?]',
            r'You should (also )?(ensure|make sure|remember) that\s.*?[.!?]',
        ]
        
        result = line
        for pattern in verbose_sentence_patterns:
            result = re.sub(pattern, '', result, flags=re.IGNORECASE)
        
        # Remove verbose phrase starters
        verbose_patterns = [
            (r'\s*[Tt]his means that\s*', ' '),
            (r'\s*[Ii]n other words,?\s*', ' '),
            (r'\s*[Ff]or example,?\s*', ' '),
            (r'\s*[Tt]o illustrate,?\s*', ' '),
            (r'\s*[Tt]hat is to say,?\s*', ' '),
            (r'\s*[Ss]pecifically,?\s*', ' '),
            (r'\s*[Ii]t should be noted that\s*', ' '),
            (r'\s*[Ii]t is important to understand that\s*', ' '),
            (r'\s*[Aa]s mentioned (before|above|earlier),?\s*', ' '),
            (r'\s*[Aa]s we have seen,?\s*', ' '),
            (r'\s*[Ii]n this case,?\s*', ' '),
            (r'\s*[Aa]s you can see,?\s*', ' '),
            (r'\s*[Aa]dditionally,?\s*', ' '),
            (r'\s*[Ff]urthermore,?\s*', ' '),
            (r'\s*[Mm]oreover,?\s*', ' '),
        ]
        
        for pattern, replacement in verbose_patterns:
            result = re.sub(pattern, replacement, result)
        
        # Clean up extra spaces
        result = re.sub(r'\s+', ' ', result)
        return result.strip()
    
    def _shorten_sentence(self, sentence: str, gamma: float) -> str:
        """Shorten sentences based on gamma parameter."""
        if len(sentence) < 60:
            return sentence
            
        words = sentence.split()
        
        # More aggressive shortening for lower gamma
        if gamma < 0.3:
            max_words = min(8, len(words) // 4)  # Very aggressive
        elif gamma < 0.5:
            max_words = min(12, len(words) // 2)  # Moderate
        else:
            max_words = min(20, int(len(words) * 0.6))  # Light
        
        if len(words) > max_words:
            return ' '.join(words[:max_words])
        
        return sentence
    
    def _extract_key_points(self, paragraph: str) -> List[str]:
        """Extract key points from a paragraph for bullet point conversion."""
        # Split on sentence endings
        sentences = re.split(r'[.!?]+', paragraph)
        key_points = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:  # Too short to be meaningful
                continue
                
            # Remove verbose starters
            sentence = re.sub(r'^(It is important to|You should|Additionally,?|Furthermore,?|Moreover,?)\s*', '', sentence, flags=re.IGNORECASE)
            sentence = re.sub(r'^(This|That)\s+(means|indicates|shows)\s+that\s+', '', sentence, flags=re.IGNORECASE)
            
            if len(sentence) > 15:
                # Shorten to key essence
                words = sentence.split()
                if len(words) > 10:
                    sentence = ' '.join(words[:10])
                key_points.append(sentence.strip())
                
            if len(key_points) >= 3:  # Limit bullet points
                break
        
        return key_points
    
    def _remove_redundancies(self, text: str) -> str:
        """Remove redundant phrases and repeated information."""
        # Remove common redundant phrases
        redundant_patterns = [
            r'\s*as (mentioned|noted|discussed) (before|above|earlier|previously)\s*',
            r'\s*as we have seen\s*',
            r'\s*it is worth noting that\s*',
            r'\s*it should be emphasized that\s*',
        ]
        
        result = text
        for pattern in redundant_patterns:
            result = re.sub(pattern, ' ', result, flags=re.IGNORECASE)
        
        return re.sub(r'\s+', ' ', result)
    
    def _aggressive_compress(self, text: str) -> str:
        """Apply aggressive compression if initial compression wasn't sufficient."""
        lines = text.split('\n')
        compressed_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Very aggressive word reduction
            words = line.split()
            if len(words) > 8:
                if line.startswith('- '):
                    # Keep bullet format but shorten
                    line = f"- {' '.join(words[1:6])}"
                else:
                    line = ' '.join(words[:8])
            
            compressed_lines.append(line)
        
        return '\n'.join(compressed_lines)
    
    def _count_tokens(self, text: str) -> int:
        """Count tokens using same tokenizer as compression_score."""
        if not text:
            return 0
        return len(self.encoding.encode(text))
    
    def _extract_entities(self, text: str) -> List[str]:
        """
        Extract entities from text for preservation checking.
        Simple implementation - in real system would use spaCy NER.
        
        Extracts:
        - Capitalized words (proper nouns)
        - ALL_CAPS words (constants, acronyms)
        - Technical paths (/api/v1/...)
        - Technical identifiers (snake_case, camelCase)
        - Function/method calls (functionName())
        """
        entities = set()
        
        # Capitalized words (proper nouns, brand names)
        entities.update(re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]*)*\b', text))
        
        # ALL_CAPS words (acronyms, constants)
        entities.update(re.findall(r'\b[A-Z]{2,}\b', text))
        
        # Technical paths and endpoints
        entities.update(re.findall(r'/[a-zA-Z][a-zA-Z0-9_/]*', text))
        
        # Technical identifiers (snake_case, camelCase)
        entities.update(re.findall(r'\b[a-z]+(?:_[a-z]+)+\b', text))  # snake_case
        entities.update(re.findall(r'\b[a-z]+(?:[A-Z][a-z]*)+\b', text))  # camelCase
        
        # Function/method calls
        entities.update(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\(\)', text))
        
        # Database/table names (often have specific patterns)
        entities.update(re.findall(r'\b[A-Z][a-zA-Z]*(?:Table|Model|Schema|DB)\b', text))
        
        # Code-like identifiers in backticks
        entities.update(re.findall(r'`([a-zA-Z_][a-zA-Z0-9_\.]*)`', text))
        
        return list(entities)
    
    def _check_entity_preservation(self, original_entities: List[str], compressed_entities: List[str]) -> float:
        """
        Calculate what percentage of original entities are preserved.
        
        Args:
            original_entities: List of entities from original text
            compressed_entities: List of entities from compressed text
            
        Returns:
            Float between 0.0 and 1.0 representing preservation ratio
        """
        if not original_entities:
            return 1.0  # No entities to lose
        
        original_set = set(original_entities)
        compressed_set = set(compressed_entities)
        
        preserved_count = len(original_set & compressed_set)
        preservation_ratio = preserved_count / len(original_set)
        
        return preservation_ratio
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current configuration and thresholds."""
        return {
            "refusal_threshold": self.refusal_threshold,
            "minimal_benefit_threshold": self.minimal_benefit_threshold, 
            "entity_preservation_threshold": self.entity_preservation_threshold,
            "compression_parameters": ["sigma", "gamma", "kappa"],
            "safety_checks": [
                "pre_check_already_compressed",
                "post_check_minimal_benefit",
                "post_check_entity_preservation"
            ]
        }