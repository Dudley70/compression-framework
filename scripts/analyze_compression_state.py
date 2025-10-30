#!/usr/bin/env python3
"""
Content Density Analyzer (Task 1.1)

Analyzes document compression state at section level.
Detects and handles documents with mixed compression states.
"""
import re
import yaml
import tiktoken
from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path

# Import dependencies from previous tasks
from scripts.compression_score import CompressionScorer
from scripts.detect_token_drift import TokenDriftDetector


@dataclass
class Section:
    """Represents a document section."""
    title: str
    level: int  # 1=H1, 2=H2, 3=H3
    content: str
    start_line: int
    end_line: int


class ContentAnalyzer:
    """
    Analyze document compression state at section level.
    """
    
    def __init__(self, scorer: CompressionScorer):
        """
        Initialize with a compression scorer.
        
        Args:
            scorer: CompressionScorer instance for scoring sections
        """
        self.scorer = scorer
        self.encoding = tiktoken.encoding_for_model("gpt-4")
        
        # Thresholds for state classification
        self.VERBOSE_THRESHOLD = 0.4      # Below this = verbose/uncompressed
        self.COMPRESSED_THRESHOLD = 0.7   # Above this = compressed
        self.MIN_SECTION_TOKENS = 3       # Minimum tokens for section analysis
        
    def split_into_sections(self, document: str) -> List[Dict]:
        """
        Split markdown document into sections based on headers.
        
        Args:
            document: Full document text
            
        Returns:
            List of section dictionaries with title, level, content, line numbers
        """
        if not document.strip():
            return []
            
        lines = document.split('\n')
        sections = []
        current_section = None
        line_num = 0
        
        # Pattern to match headers (H1, H2, H3 only)
        header_pattern = r'^(#{1,3})\s+(.+)$'
        
        for i, line in enumerate(lines):
            line_num = i + 1
            match = re.match(header_pattern, line.strip())
            
            if match:
                level = len(match.group(1))  # Count # characters
                title = match.group(2).strip()
                
                # Only process H1, H2, H3 (ignore H4+)
                if level <= 3:
                    # Save previous section
                    if current_section:
                        current_section['end_line'] = line_num - 1
                        current_section['content'] = current_section['content'].strip()
                        
                        # Only include sections with sufficient content
                        if self._has_sufficient_content(current_section['content']):
                            sections.append(current_section)
                    
                    # Start new section
                    current_section = {
                        'title': title,
                        'level': level,
                        'content': '',
                        'start_line': line_num,
                        'end_line': line_num
                    }
                else:
                    # H4+ headers are treated as content
                    if current_section:
                        current_section['content'] += line + '\n'
            else:
                # Regular content line
                if current_section:
                    current_section['content'] += line + '\n'
                elif line.strip():
                    # Content before first header - create implicit section
                    if not sections:
                        current_section = {
                            'title': 'Introduction',
                            'level': 1,
                            'content': line + '\n',
                            'start_line': line_num,
                            'end_line': line_num
                        }
        
        # Save last section
        if current_section:
            current_section['end_line'] = len(lines)
            current_section['content'] = current_section['content'].strip()
            
            if self._has_sufficient_content(current_section['content']):
                sections.append(current_section)
        
        return sections
    
    def _has_sufficient_content(self, content: str) -> bool:
        """
        Check if section has sufficient content for analysis.
        
        Args:
            content: Section content text
            
        Returns:
            True if section has enough tokens for meaningful analysis
        """
        if not content.strip():
            return False
            
        # Count tokens using tiktoken
        try:
            tokens = len(self.encoding.encode(content))
            return tokens >= self.MIN_SECTION_TOKENS
        except Exception:
            # Fallback to word count
            return len(content.split()) >= self.MIN_SECTION_TOKENS
    
    def analyze_section(self, section_content: str) -> Dict:
        """
        Analyze a single section's compression state.
        
        Args:
            section_content: Text content of the section
            
        Returns:
            Dictionary with score, state, metrics, and compression recommendation
        """
        if not section_content.strip():
            return {
                "score": 0.0,
                "state": "empty",
                "metrics": {},
                "needs_compression": False
            }
        
        # Use compression scorer
        try:
            result = self.scorer.score_text(section_content)
            score = result.compression_score
            metrics = result.metrics.__dict__
        except Exception as e:
            # Fallback scoring if scorer fails
            score = self._fallback_score(section_content)
            metrics = {"error": str(e)}
        
        # Classify state based on score
        if score < self.VERBOSE_THRESHOLD:
            state = "verbose"
            needs_compression = True
        elif score > self.COMPRESSED_THRESHOLD:
            state = "compressed"
            needs_compression = False
        else:
            state = "moderately_compressed"
            needs_compression = False  # Moderate compression is acceptable
        
        return {
            "score": score,
            "state": state,
            "metrics": metrics,
            "needs_compression": needs_compression
        }
    
    def _fallback_score(self, text: str) -> float:
        """
        Simple fallback scoring if main scorer fails.
        
        Args:
            text: Text to score
            
        Returns:
            Rough compression score based on simple heuristics
        """
        if not text.strip():
            return 0.0
        
        # Simple heuristics for compression scoring
        lines = text.split('\n')
        list_lines = sum(1 for line in lines if line.strip().startswith(('-', '*', '•', '1.', '2.')))
        total_lines = len([line for line in lines if line.strip()])
        
        if total_lines == 0:
            return 0.0
        
        list_ratio = list_lines / total_lines
        avg_line_length = sum(len(line) for line in lines) / len(lines)
        
        # Higher list ratio and shorter lines suggest more compression
        score = (list_ratio * 0.7) + (max(0, 1 - avg_line_length / 100) * 0.3)
        return min(1.0, max(0.0, score))
    
    def analyze_document(self, document: str, header_metadata: Dict = None) -> Dict:
        """
        Complete document analysis with section-level detail.
        
        Args:
            document: Full document text
            header_metadata: Optional YAML header data for token drift detection
            
        Returns:
            Complete analysis with overall state, sections, summary, and recommendations
        """
        if not document.strip():
            return {
                "overall_state": "empty",
                "sections": [],
                "summary": {
                    "total_sections": 0,
                    "compressed_sections": 0,
                    "uncompressed_sections": 0,
                    "avg_score": 0.0
                },
                "recommendation": "none"
            }
        
        # Split into sections
        sections = self.split_into_sections(document)
        
        if not sections:
            # No headers found - treat whole document as one section
            analysis = self.analyze_section(document)
            sections = [{
                "title": "Document",
                "level": 1,
                "score": analysis["score"],
                "state": analysis["state"],
                "needs_compression": analysis["needs_compression"]
            }]
        else:
            # Analyze each section
            for i, section in enumerate(sections):
                analysis = self.analyze_section(section['content'])
                section.update({
                    "score": analysis["score"],
                    "state": analysis["state"],
                    "needs_compression": analysis["needs_compression"]
                })
        
        # Calculate summary statistics
        section_scores = [s["score"] for s in sections]
        compressed_count = sum(1 for s in sections if s["score"] > self.COMPRESSED_THRESHOLD)
        uncompressed_count = sum(1 for s in sections if s["score"] < self.VERBOSE_THRESHOLD)
        
        summary = {
            "total_sections": len(sections),
            "compressed_sections": compressed_count,
            "uncompressed_sections": uncompressed_count,
            "avg_score": sum(section_scores) / len(section_scores) if section_scores else 0.0
        }
        
        # Token drift analysis (if header provided)
        token_drift = None
        drift_ratio = None
        if header_metadata:
            try:
                drift_detector = TokenDriftDetector()
                # Create a temporary document with YAML header for drift analysis
                yaml_header = "---\n" + yaml.dump(header_metadata) + "---\n"
                full_document = yaml_header + document
                
                # Use the detector's internal methods
                baseline = drift_detector._extract_baseline(full_document)
                current = drift_detector._count_tokens(full_document)
                drift_result = drift_detector._calculate_drift(baseline, current)
                
                token_drift = {
                    "has_header": drift_result.has_header,
                    "baseline_tokens": drift_result.baseline_tokens,
                    "current_tokens": drift_result.current_tokens,
                    "drift_ratio": drift_result.drift_ratio,
                    "significant_drift": drift_result.drift_ratio and drift_result.drift_ratio > 1.15 if drift_result.drift_ratio else False
                }
                drift_ratio = drift_result.drift_ratio
            except Exception as e:
                token_drift = {"error": str(e)}
        
        # Classify overall state
        overall_state = self.classify_state(section_scores, drift_ratio)
        
        # Generate recommendation
        recommendation = self._generate_recommendation(sections, overall_state, token_drift)
        
        result = {
            "overall_state": overall_state,
            "sections": sections,
            "summary": summary,
            "recommendation": recommendation
        }
        
        if token_drift:
            result["token_drift"] = token_drift
        
        return result
    
    def classify_state(self, section_scores: List[float], token_drift_ratio: Optional[float] = None) -> str:
        """
        Classify overall document state based on section scores.
        
        Args:
            section_scores: List of compression scores for each section
            token_drift_ratio: Optional token drift ratio
            
        Returns:
            Overall state classification
        """
        if not section_scores:
            return "empty"
        
        # Check for token drift first
        if token_drift_ratio and token_drift_ratio > 1.15:
            # Document has grown significantly
            if any(score < self.VERBOSE_THRESHOLD for score in section_scores):
                return "edited"  # Has drift + uncompressed sections
        
        # Check section score distribution
        compressed_count = sum(1 for s in section_scores if s > self.COMPRESSED_THRESHOLD)
        uncompressed_count = sum(1 for s in section_scores if s < self.VERBOSE_THRESHOLD)
        total = len(section_scores)
        
        if compressed_count == total:
            return "compressed"
        elif uncompressed_count == total:
            return "uncompressed"
        elif compressed_count > 0 and uncompressed_count > 0:
            return "mixed"
        else:
            return "moderately_compressed"
    
    def _generate_recommendation(self, sections: List[Dict], overall_state: str, token_drift: Dict = None) -> str:
        """
        Generate actionable recommendation based on analysis.
        
        Args:
            sections: List of analyzed sections
            overall_state: Overall document state
            token_drift: Optional token drift information
            
        Returns:
            Human-readable recommendation
        """
        if overall_state == "empty":
            return "none"
        elif overall_state == "compressed":
            return "none"
        elif overall_state == "uncompressed":
            return "compress_all"
        else:
            # Mixed or edited state - identify specific sections
            sections_to_compress = []
            for i, section in enumerate(sections):
                if section["needs_compression"]:
                    sections_to_compress.append(str(i))
            
            if not sections_to_compress:
                return "none"
            
            recommendation = f"compress_sections: [{', '.join(sections_to_compress)}]"
            
            # Add token drift recommendation if applicable
            if (token_drift and 
                token_drift.get("significant_drift", False) and 
                overall_state == "edited"):
                recommendation += ", update_baseline"
            
            return recommendation


def main():
    """
    Command-line interface for content analysis.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze document compression state")
    parser.add_argument("file", help="Markdown file to analyze")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    # Load document
    try:
        with open(args.file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File {args.file} not found")
        return 1
    except Exception as e:
        print(f"Error reading file: {e}")
        return 1
    
    # Extract YAML header if present
    header_metadata = None
    if content.startswith('---\n'):
        try:
            lines = content.split('\n')
            yaml_end = lines.index('---', 1)
            header_text = '\n'.join(lines[1:yaml_end])
            header_metadata = yaml.safe_load(header_text)
            content = '\n'.join(lines[yaml_end + 1:])
        except (ValueError, yaml.YAMLError):
            pass  # No valid YAML header
    
    # Analyze document
    scorer = CompressionScorer()
    analyzer = ContentAnalyzer(scorer)
    result = analyzer.analyze_document(content, header_metadata)
    
    # Output results
    if args.json:
        import json
        print(json.dumps(result, indent=2))
    else:
        print(f"Document: {args.file}")
        print(f"Overall State: {result['overall_state']}")
        print(f"Sections: {result['summary']['total_sections']}")
        print(f"Average Score: {result['summary']['avg_score']:.2f}")
        print(f"Recommendation: {result['recommendation']}")
        
        if args.verbose:
            print("\nSection Details:")
            for i, section in enumerate(result['sections']):
                print(f"  {i}: {section['title']} (L{section['level']}) - "
                      f"Score: {section['score']:.2f}, State: {section['state']}")


if __name__ == "__main__":
    exit(main())