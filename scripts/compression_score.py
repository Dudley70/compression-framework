import tiktoken
from markdown_it import MarkdownIt
import nltk
import numpy as np
import re
import math
from collections import Counter
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class CompressionMetrics:
    list_density: float
    prose_ratio: float
    avg_sentence_length: float
    redundancy: float
    explanation_markers: int
    information_entropy: float

class CompressionScorer:
    def __init__(self):
        self.encoding = tiktoken.get_encoding("cl100k_base")
        self.md_parser = MarkdownIt()

        # Explanation markers to look for
        self.explanation_markers = [
            "this means", "in other words", "for example",
            "to illustrate", "that is to say", "specifically"
        ]

        # Download required NLTK data
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('punkt_tab', quiet=True)
        except:
            pass  # In case NLTK is not available

    def calculate_score(self, text: str) -> Dict:
        """Main entry point for scoring."""
        if not text.strip():
            return {
                "overall_score": 0.0,
                "metrics": {
                    "list_density": 0.0,
                    "prose_ratio": 0.0,
                    "avg_sentence_length": 0.0,
                    "redundancy": 0.0,
                    "explanation_markers": 0,
                    "information_entropy": 0.0
                },
                "interpretation": "verbose",
                "safe_to_compress": True
            }

        metrics = self._calculate_metrics(text)
        overall_score = self._compute_overall_score(metrics)

        return {
            "overall_score": overall_score,
            "metrics": {
                "list_density": metrics.list_density,
                "prose_ratio": metrics.prose_ratio,
                "avg_sentence_length": metrics.avg_sentence_length,
                "redundancy": metrics.redundancy,
                "explanation_markers": metrics.explanation_markers,
                "information_entropy": metrics.information_entropy
            },
            "interpretation": self._interpret_score(overall_score),
            "safe_to_compress": overall_score < 0.8
        }

    def _calculate_metrics(self, text: str) -> CompressionMetrics:
        """Calculate all individual metrics."""

        # Count total tokens
        total_tokens = len(self.encoding.encode(text))
        if total_tokens == 0:
            return CompressionMetrics(0.0, 0.0, 0.0, 0.0, 0, 0.0)

        # 1. List density calculation
        list_density = self._calculate_list_density(text, total_tokens)

        # 2. Prose ratio calculation
        prose_ratio = self._calculate_prose_ratio(text, total_tokens)

        # 3. Average sentence length
        avg_sentence_length = self._calculate_avg_sentence_length(text)

        # 4. Redundancy calculation
        redundancy = self._calculate_redundancy(text)

        # 5. Explanation markers count
        explanation_markers = self._count_explanation_markers(text, total_tokens)

        # 6. Information entropy
        information_entropy = self._calculate_information_entropy(text)

        return CompressionMetrics(
            list_density=list_density,
            prose_ratio=prose_ratio,
            avg_sentence_length=avg_sentence_length,
            redundancy=redundancy,
            explanation_markers=explanation_markers,
            information_entropy=information_entropy
        )

    def _calculate_list_density(self, text: str, total_tokens: int) -> float:
        """Calculate ratio of list items to total tokens."""
        # Find list patterns: lines starting with -, *, +, or numbers
        list_patterns = [
            r'^\s*[-*+]\s+.+$',  # Bullet lists
            r'^\s*\d+\.\s+.+$',  # Numbered lists
            r'^\s*[a-zA-Z]\.\s+.+$',  # Letter lists
        ]

        list_content = ""
        lines = text.split('\n')

        for line in lines:
            for pattern in list_patterns:
                if re.match(pattern, line, re.MULTILINE):
                    list_content += line + "\n"
                    break

        if not list_content:
            return 0.0

        list_tokens = len(self.encoding.encode(list_content))
        return min(1.0, list_tokens / total_tokens)

    def _calculate_prose_ratio(self, text: str, total_tokens: int) -> float:
        """Calculate ratio of paragraph tokens to total tokens."""
        # Don't rely on markdown parser as it misclassifies list content
        prose_content = ""

        # Analyze line by line to be more precise
        lines = text.split('\n')
        for line in lines:
            original_line = line
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Skip any markdown structural elements
            if (line.startswith('#') or         # Headers
                line.startswith('-') or         # Bullet lists
                line.startswith('*') or         # Bullet lists
                line.startswith('+') or         # Bullet lists
                re.match(r'^\d+\.', line) or    # Numbered lists
                line.startswith('```') or       # Code blocks
                line.startswith('|') or         # Tables
                line.startswith('**') or        # Bold formatting
                line.endswith(':') or           # Section labels
                re.match(r'^\w+\s*:\s*', line) or  # Key: value pairs
                '`' in line):                   # Code snippets
                continue

            # Must be substantial prose - at least 5 words, multiple meaningful words
            words = line.split()
            if (len(words) > 4 and
                len([word for word in words if len(word) > 3]) > 2 and
                not any(char in line for char in '()[]{}|`')):  # No code-like formatting
                prose_content += line + " "

        if not prose_content.strip():
            return 0.0

        prose_tokens = len(self.encoding.encode(prose_content))
        return min(1.0, prose_tokens / total_tokens)

    def _calculate_avg_sentence_length(self, text: str) -> float:
        """Calculate average sentence length in words."""
        # Remove markdown syntax for sentence analysis
        clean_text = re.sub(r'[#*_`\[\](){}]', '', text)
        clean_text = re.sub(r'^\s*[-+*]\s+', '', clean_text, flags=re.MULTILINE)
        clean_text = re.sub(r'^\s*\d+\.\s+', '', clean_text, flags=re.MULTILINE)

        # Split on multiple delimiters including colons and line breaks
        # This better handles compressed formats with short fragments
        sentences = re.split(r'[.!?:\n]+', clean_text)

        if not sentences:
            return 0.0

        # Filter out very short fragments and empty strings
        real_sentences = []
        for s in sentences:
            s = s.strip()
            words = s.split()
            # Must have at least 2 words and not be just punctuation/markdown
            if len(words) >= 2 and not all(len(word) <= 2 for word in words):
                real_sentences.append(s)

        if not real_sentences:
            # If no "real" sentences found, treat the whole text as short fragments
            # This handles highly compressed content better
            words = clean_text.split()
            if len(words) > 0:
                return min(5.0, len(words) / max(1, text.count('\n') + 1))
            return 0.0

        word_counts = [len(sentence.split()) for sentence in real_sentences]
        return sum(word_counts) / len(word_counts)

    def _calculate_redundancy(self, text: str) -> float:
        """Calculate redundancy based on repeated phrases."""
        # Extract phrases of 3+ words
        words = re.findall(r'\b\w+\b', text.lower())

        if len(words) < 3:
            return 1.0  # No redundancy possible

        # Generate 3-word phrases
        phrases = []
        for i in range(len(words) - 2):
            phrase = ' '.join(words[i:i+3])
            phrases.append(phrase)

        if not phrases:
            return 1.0

        # Count phrase frequencies
        phrase_counts = Counter(phrases)

        # Calculate how many phrases appear more than once
        repeated_phrases = sum(1 for count in phrase_counts.values() if count > 1)
        total_unique_phrases = len(phrase_counts)

        if total_unique_phrases == 0:
            return 1.0

        # More sensitive redundancy calculation
        # If many phrases are repeated, redundancy score drops significantly
        redundancy_score = 1.0 - (repeated_phrases / total_unique_phrases)

        return max(0.0, redundancy_score)

    def _count_explanation_markers(self, text: str, total_tokens: int) -> int:
        """Count explanation/scaffolding phrases."""
        text_lower = text.lower()
        marker_count = 0

        for marker in self.explanation_markers:
            marker_count += text_lower.count(marker)

        return marker_count

    def _calculate_information_entropy(self, text: str) -> float:
        """Calculate Shannon entropy of token distribution."""
        tokens = self.encoding.encode(text)

        if not tokens:
            return 0.0

        # Count token frequencies
        token_counts = Counter(tokens)
        total_tokens = len(tokens)

        # Calculate Shannon entropy
        entropy = 0.0
        for count in token_counts.values():
            probability = count / total_tokens
            if probability > 0:
                entropy -= probability * math.log2(probability)

        return entropy

    def _compute_overall_score(self, metrics: CompressionMetrics) -> float:
        """Weighted combination of metrics."""
        # Normalize sentence length: 5 words = 1.0, 25+ words = 0.0 (adjusted for better range)
        normalized_sentence_length = max(0, min(1, (25 - metrics.avg_sentence_length) / 20))

        # Normalize explanation markers - penalize verbose explanations more
        normalized_explanation = max(0, min(1, 1 - (metrics.explanation_markers / 3)))

        # Normalize entropy: typical range 3.0-6.5 -> 0-1 (adjusted range)
        normalized_entropy = max(0, min(1, (metrics.information_entropy - 3.0) / 3.5))

        # Balanced weighted combination for better range distribution
        overall_score = (
            metrics.list_density * 0.40 +         # Lists are primary compression indicator
            (1 - metrics.prose_ratio) * 0.30 +    # Prose reduction is critical
            normalized_sentence_length * 0.15 +   # Sentence brevity matters
            metrics.redundancy * 0.05 +           # Redundancy less critical
            normalized_explanation * 0.05 +       # Explanation markers less important
            normalized_entropy * 0.05             # Entropy less reliable
        )

        return max(0.0, min(1.0, overall_score))

    def _interpret_score(self, score: float) -> str:
        """Convert score to interpretation."""
        if score < 0.3:
            return "verbose"
        elif score < 0.6:
            return "moderately_compressed"
        elif score < 0.8:
            return "compressed"
        else:
            return "highly_compressed"