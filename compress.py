#!/usr/bin/env python3
"""
Compression Tool MVP (Task 4.1)

Production-ready CLI tool for safely compressing markdown documents using LSC techniques.
Integrates all validated components with comprehensive safety validation.

Usage:
    python compress.py analyze <input_file>              # Analysis only
    python compress.py compress <input_file>             # Full compression 
    python compress.py validate <original> <compressed>  # Validation only

Flags:
    --dry-run          # Show what would be compressed
    --force           # Skip safety checks (dangerous, logs warning)
    --output <file>   # Custom output path
    --report <file>   # Save validation report
    --verbose         # Detailed progress logging
"""

import argparse
import json
import sys
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any
from dataclasses import dataclass, asdict
import re
import traceback

# Import validated components from previous tasks
try:
    from scripts.analyze_compression_state import ContentAnalyzer, Section
    from scripts.detect_token_drift import TokenDriftDetector, DriftResult
    from scripts.compression_score import CompressionScorer, CompressionMetrics
    from scripts.safety_checks import SafetyValidator
except ImportError as e:
    print(f"Error importing validated components: {e}")
    print("Please ensure scripts/ directory contains validated components from previous tasks.")
    sys.exit(1)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class AnalysisResult:
    """Results from document analysis"""
    file_path: str
    compression_score: float
    sections: List[Dict[str, Any]]  # ContentAnalyzer returns dicts, not Section objects
    recommended_techniques: List[str]
    needs_compression: bool
    analysis_time: float


@dataclass
class ValidationResult:
    """Results from safety validation"""
    passed: bool
    warnings: List[str]
    failure_reason: str
    safety_details: Dict[str, Any]
    validation_time: float


class ValidationReport:
    """Comprehensive validation report with markdown and JSON output"""
    
    def __init__(self, original: str, compressed: str, 
                 safety_result: ValidationResult, 
                 compression_score: float,
                 token_drift: DriftResult,
                 processing_time: float):
        self.original = original
        self.compressed = compressed
        self.safety_result = safety_result
        self.compression_score = compression_score
        self.token_drift = token_drift
        self.processing_time = processing_time
        
        # Calculate metrics
        self.original_tokens = self._count_tokens(original)
        self.compressed_tokens = self._count_tokens(compressed)
        self.compression_ratio = self.compressed_tokens / self.original_tokens if self.original_tokens > 0 else 1.0
        self.reduction_percentage = (1 - self.compression_ratio) * 100
        
    def _count_tokens(self, text: str) -> int:
        """Count tokens using tiktoken"""
        try:
            import tiktoken
            encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
            return len(encoding.encode(text))
        except Exception:
            # Fallback to rough estimation
            return len(text.split())
    
    def to_markdown(self) -> str:
        """Generate human-readable markdown report"""
        status_emoji = "✅" if self.safety_result.passed else "❌"
        
        report = f"""# Compression Validation Report

## Summary {status_emoji}
- **Status**: {"PASSED" if self.safety_result.passed else "FAILED"}
- **Processing Time**: {self.processing_time:.2f}s
- **Validation Time**: {self.safety_result.validation_time:.2f}s

## Token Analysis
- **Original Tokens**: {self.original_tokens:,}
- **Compressed Tokens**: {self.compressed_tokens:,}
- **Compression Ratio**: {self.compression_ratio:.3f}
- **Reduction**: {self.reduction_percentage:.1f}%

## Compression Score
- **Score**: {self.compression_score:.3f}/1.0
- **Interpretation**: {'High' if self.compression_score >= 0.8 else 'Medium' if self.compression_score >= 0.4 else 'Low'} compression

## Safety Validation
"""
        
        if self.safety_result.passed:
            report += "- **Result**: ✅ All safety checks passed\n"
        else:
            report += f"- **Result**: ❌ Failed - {self.safety_result.failure_reason}\n"
        
        if self.safety_result.warnings:
            report += "\n### Warnings\n"
            for warning in self.safety_result.warnings:
                report += f"- ⚠️ {warning}\n"
        
        # Safety details
        if self.safety_result.safety_details:
            report += "\n### Safety Check Details\n"
            for check, result in self.safety_result.safety_details.items():
                check_emoji = "✅" if result.get('passed', False) else "❌"
                report += f"- **{check}**: {check_emoji} {result.get('summary', 'No details')}\n"
        
        # Token drift analysis
        if hasattr(self.token_drift, 'growth_detected'):
            report += f"\n## Token Drift Analysis\n"
            report += f"- **Growth Detected**: {'Yes' if self.token_drift.growth_detected else 'No'}\n"
            if hasattr(self.token_drift, 'ratio'):
                report += f"- **Growth Ratio**: {self.token_drift.ratio:.3f}\n"
            if hasattr(self.token_drift, 'recommendation'):
                report += f"- **Recommendation**: {self.token_drift.recommendation}\n"
        
        return report
    
    def to_json(self) -> Dict[str, Any]:
        """Generate machine-readable JSON report"""
        return {
            "summary": {
                "passed": self.safety_result.passed,
                "processing_time": self.processing_time,
                "validation_time": self.safety_result.validation_time
            },
            "tokens": {
                "original_tokens": self.original_tokens,
                "compressed_tokens": self.compressed_tokens,
                "compression_ratio": self.compression_ratio,
                "reduction_percentage": self.reduction_percentage
            },
            "compression_score": self.compression_score,
            "safety_validation": {
                "passed": self.safety_result.passed,
                "warnings": self.safety_result.warnings,
                "failure_reason": self.safety_result.failure_reason,
                "details": self.safety_result.safety_details
            },
            "token_drift": asdict(self.token_drift) if hasattr(self.token_drift, '__dict__') else str(self.token_drift),
            "original_content": self.original,
            "compressed_content": self.compressed
        }


class LSCTechniques:
    """Implementation of 5 core LSC compression techniques"""
    
    def __init__(self):
        self.preserve_patterns = [
            r'```[\s\S]*?```',  # Code blocks
            r'`[^`]+`',         # Inline code
            r'\[([^\]]+)\]\(([^)]+)\)',  # Links
            r'!\[([^\]]*)\]\(([^)]+)\)', # Images
            r'^\|.*\|$',        # Table rows
            r'^<!--[\s\S]*?-->$', # HTML comments
        ]
    
    def _preserve_special_content(self, text: str) -> Tuple[str, Dict[str, str]]:
        """Extract and preserve special content that shouldn't be compressed"""
        preserved = {}
        preserved_text = text
        
        for i, pattern in enumerate(self.preserve_patterns):
            matches = re.findall(pattern, text, re.MULTILINE)
            for j, match in enumerate(matches):
                if isinstance(match, tuple):
                    match_text = f"[{match[0]}]({match[1]})" if pattern.endswith(r'\)') else match[0]
                else:
                    match_text = match
                
                placeholder = f"__PRESERVE_{i}_{j}__"
                preserved[placeholder] = match_text
                preserved_text = preserved_text.replace(match_text, placeholder, 1)
        
        return preserved_text, preserved
    
    def _restore_preserved_content(self, text: str, preserved: Dict[str, str]) -> str:
        """Restore preserved content"""
        restored = text
        for placeholder, content in preserved.items():
            restored = restored.replace(placeholder, content)
        return restored
    
    def apply_lists_tables(self, text: str) -> str:
        """Convert prose to structured lists/tables (σ↑)"""
        preserved_text, preserved = self._preserve_special_content(text)
        
        # Pattern: sentences describing multiple items/methods/features
        list_patterns = [
            # "First... Second... Third..." patterns
            r'(?:First|The first)[^.]*?\.\s*(?:Second|The second)[^.]*?\.\s*(?:Third|The third)[^.]*?\.',
            # "supports three/multiple methods" patterns  
            r'(?:supports|provides|includes|contains)\s+(?:three|multiple|several|many)\s+(?:methods?|features?|options?|types?)[^.]*?\.',
            # Enumeration patterns
            r'(?:There are|We have)\s+(?:three|multiple|several|many)[^.]*?(?:First[^.]*?\.\s*Second[^.]*?\.\s*Third[^.]*?\.)',
        ]
        
        result = preserved_text
        
        for pattern in list_patterns:
            matches = re.findall(pattern, result, re.IGNORECASE | re.DOTALL)
            for match in matches:
                # Extract items from the verbose description
                items = self._extract_list_items(match)
                if len(items) >= 2:
                    list_text = self._format_as_list(items)
                    result = result.replace(match, list_text)
        
        return self._restore_preserved_content(result, preserved)
    
    def _extract_list_items(self, text: str) -> List[str]:
        """Extract list items from verbose prose"""
        items = []
        
        # Common patterns for list items
        patterns = [
            r'(?:first|1st|①)[^.]*?([A-Z][^.]*?)(?:\.|,|\s+(?:for|which|that))',
            r'(?:second|2nd|②)[^.]*?([A-Z][^.]*?)(?:\.|,|\s+(?:for|which|that))',
            r'(?:third|3rd|③)[^.]*?([A-Z][^.]*?)(?:\.|,|\s+(?:for|which|that))',
            # Method descriptions: "GET for retrieval"
            r'([A-Z]+)\s+(?:for|which|that)\s+([^.,]+)',
            # Feature descriptions: "authentication which handles"
            r'(\w+)\s+(?:which|that)\s+([^.,]+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    item = f"{match[0]}: {match[1].strip()}"
                else:
                    item = match.strip()
                if item and item not in items:
                    items.append(item)
        
        return items[:5]  # Limit to reasonable number
    
    def _format_as_list(self, items: List[str]) -> str:
        """Format items as markdown list"""
        formatted_items = []
        for item in items:
            # Clean up the item
            clean_item = re.sub(r'\s+', ' ', item.strip())
            if not clean_item.endswith('.'):
                clean_item += '.'
            formatted_items.append(f"- {clean_item}")
        
        return '\n'.join(formatted_items)
    
    def apply_hierarchical_structure(self, text: str) -> str:
        """Add/improve document hierarchy (σ↑)"""
        preserved_text, preserved = self._preserve_special_content(text)
        
        # Split into paragraphs
        paragraphs = [p.strip() for p in preserved_text.split('\n\n') if p.strip()]
        
        if len(paragraphs) < 2:
            return self._restore_preserved_content(preserved_text, preserved)
        
        result_parts = []
        
        for i, para in enumerate(paragraphs):
            # Skip if already has header
            if para.startswith('#'):
                result_parts.append(para)
                continue
            
            # Detect topic changes that should get headers
            if self._should_add_header(para, i, paragraphs):
                header = self._generate_header(para)
                if header:
                    result_parts.append(f"## {header}")
            
            result_parts.append(para)
        
        result = '\n\n'.join(result_parts)
        return self._restore_preserved_content(result, preserved)
    
    def _should_add_header(self, paragraph: str, index: int, all_paragraphs: List[str]) -> bool:
        """Determine if paragraph should get a header"""
        # Don't add header to first paragraph
        if index == 0:
            return False
        
        # Look for topic transition indicators
        topic_indicators = [
            r'^(?:The|Our|This)\s+(?:second|next|following)',
            r'^(?:Another|Additional|Further)',
            r'^(?:Implementation|Configuration|Setup|Usage)',
            r'^(?:Authentication|Security|Performance)',
        ]
        
        for pattern in topic_indicators:
            if re.search(pattern, paragraph, re.IGNORECASE):
                return True
        
        return False
    
    def _generate_header(self, paragraph: str) -> str:
        """Generate appropriate header from paragraph content"""
        # Extract key topic from first sentence
        first_sentence = paragraph.split('.')[0]
        
        # Common header patterns
        if 'authentication' in first_sentence.lower():
            return "Authentication"
        elif 'endpoint' in first_sentence.lower() or 'api' in first_sentence.lower():
            return "API Endpoints"
        elif 'configuration' in first_sentence.lower() or 'config' in first_sentence.lower():
            return "Configuration"
        elif 'implementation' in first_sentence.lower():
            return "Implementation"
        elif 'usage' in first_sentence.lower() or 'use' in first_sentence.lower():
            return "Usage"
        
        # Extract from first meaningful noun phrase
        words = first_sentence.split()[:5]
        meaningful_words = [w for w in words if len(w) > 3 and w.isalpha()]
        
        if meaningful_words:
            return meaningful_words[0].title()
        
        return None
    
    def remove_redundancy(self, text: str) -> str:
        """Eliminate duplicate information (γ↓)"""
        preserved_text, preserved = self._preserve_special_content(text)
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', preserved_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Remove semantically similar sentences
        unique_sentences = []
        
        for sentence in sentences:
            is_duplicate = False
            
            for existing in unique_sentences:
                if self._are_semantically_similar(sentence, existing):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_sentences.append(sentence)
        
        # Rejoin sentences
        result = '. '.join(unique_sentences)
        if result and not result.endswith('.'):
            result += '.'
        
        return self._restore_preserved_content(result, preserved)
    
    def _are_semantically_similar(self, sent1: str, sent2: str, threshold: float = 0.7) -> bool:
        """Check if two sentences are semantically similar"""
        # Simple similarity based on word overlap
        words1 = set(sent1.lower().split())
        words2 = set(sent2.lower().split())
        
        if not words1 or not words2:
            return False
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        similarity = len(intersection) / len(union)
        return similarity >= threshold
    
    def apply_technical_shorthand(self, text: str) -> str:
        """Use standard abbreviations (κ↓)"""
        preserved_text, preserved = self._preserve_special_content(text)
        
        # Technical term replacements
        replacements = {
            r'HyperText Transfer Protocol Secure\s*\(HTTPS\)': 'HTTPS',
            r'HyperText Transfer Protocol\s*\(HTTP\)': 'HTTP',
            r'Transport Layer Security\s*\(TLS\)': 'TLS',
            r'Secure Sockets Layer\s*\(SSL\)': 'SSL',
            r'JavaScript Object Notation\s*\(JSON\)': 'JSON',
            r'Application Programming Interface\s*\(API\)': 'API',
            r'Uniform Resource Locator\s*\(URL\)': 'URL',
            r'Structured Query Language\s*\(SQL\)': 'SQL',
            r'Cascading Style Sheets\s*\(CSS\)': 'CSS',
            r'HyperText Markup Language\s*\(HTML\)': 'HTML',
            # OAuth patterns
            r'OAuth\s*2\.0': 'OAuth2',
            r'JSON Web Token\s*\(JWT\)': 'JWT',
            # Common expansions
            r'configuration': 'config',
            r'authentication': 'auth',
            r'authorization': 'authz',
            r'environment': 'env',
            r'development': 'dev',
            r'production': 'prod',
        }
        
        result = preserved_text
        
        for pattern, replacement in replacements.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        return self._restore_preserved_content(result, preserved)
    
    def increase_information_density(self, text: str) -> str:
        """Pack more meaning per token (σ↑ γ↑)"""
        preserved_text, preserved = self._preserve_special_content(text)
        
        # Remove filler words and phrases
        filler_patterns = [
            r'\b(?:When\s+you\s+(?:are\s+)?(?:making|working|dealing)\s+with)\b',
            r'\b(?:In\s+order\s+to)\b',
            r'\b(?:It\s+is\s+important\s+to\s+(?:understand\s+that)?)\b',
            r'\b(?:Please\s+(?:note\s+that|ensure\s+that|make\s+sure))\b',
            r'\b(?:You\s+(?:need\s+to|should|must))\b',
            r'\b(?:that\s+you\s+(?:need\s+to|should|must))\b',
            r'\b(?:make\s+sure\s+(?:that\s+)?(?:you\s+)?)\b',
            r'\b(?:ensure\s+that\s+(?:you\s+)?)\b',
        ]
        
        # Conciseness replacements
        concise_replacements = {
            r'requests to the API': 'API requests',
            r'include.*?in the.*?header': 'include in header',
            r'authentication headers?': 'auth header',
            r'in every (?:single )?request': 'in requests',
            r'all API endpoints': 'endpoints',
            r'making requests to': 'requesting',
            r'for the purpose of': 'for',
            r'in the event that': 'if',
            r'at this point in time': 'now',
            r'due to the fact that': 'because',
        }
        
        result = preserved_text
        
        # Remove filler patterns
        for pattern in filler_patterns:
            result = re.sub(pattern, '', result, flags=re.IGNORECASE)
        
        # Apply conciseness replacements
        for pattern, replacement in concise_replacements.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        # Clean up extra whitespace
        result = re.sub(r'\s+', ' ', result)
        result = re.sub(r'\s*([.!?])', r'\1', result)
        
        return self._restore_preserved_content(result, preserved)


class CompressionTool:
    """Main compression tool integrating all validated components"""
    
    def __init__(self):
        # Initialize validated components
        self.scorer = CompressionScorer()
        self.analyzer = ContentAnalyzer(self.scorer)
        self.safety = SafetyValidator()
        self.drift_detector = TokenDriftDetector()
        self.lsc = LSCTechniques()
        
        # Add score_text method to scorer for compatibility
        if not hasattr(self.scorer, 'score_text'):
            self.scorer.score_text = lambda text: type('obj', (object,), {
                'compression_score': self.scorer.calculate_score(text)['overall_score'],
                'metrics': self.scorer.calculate_score(text)['metrics']
            })()
    
    def analyze_document(self, file_path: str) -> AnalysisResult:
        """Analyze document and recommend compression techniques"""
        start_time = time.time()
        
        try:
            # Read document
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Analyze with ContentAnalyzer
            analysis = self.analyzer.analyze_document(content)
            
            # Determine recommended techniques based on analysis
            recommended_techniques = self._determine_techniques(analysis)
            
            # Calculate overall compression score
            score_result = self.scorer.calculate_score(content)
            compression_score = score_result['overall_score']
            
            analysis_time = time.time() - start_time
            
            return AnalysisResult(
                file_path=file_path,
                compression_score=compression_score,
                sections=analysis.get('sections', []),
                recommended_techniques=recommended_techniques,
                needs_compression=compression_score < 0.6,
                analysis_time=analysis_time
            )
            
        except Exception as e:
            logger.error(f"Error analyzing document {file_path}: {e}")
            raise
    
    def _determine_techniques(self, analysis: Dict) -> List[str]:
        """Determine appropriate LSC techniques based on analysis"""
        techniques = []

        # Check overall compression state
        if analysis.get('overall_state') == 'uncompressed':
            techniques.extend(['lists_tables', 'hierarchical_structure', 'information_density'])

        # Check for specific patterns in sections
        sections = analysis.get('sections', [])
        for section in sections:
            content = section.get('content', '').lower()

            # Lists/tables opportunities
            if any(phrase in content for phrase in ['first', 'second', 'third', 'supports', 'methods']):
                if 'lists_tables' not in techniques:
                    techniques.append('lists_tables')

            # Redundancy opportunities
            if content.count('.') > 5:  # Multiple sentences
                words = content.split()
                if len(words) > 0 and len(set(words)) / len(words) < 0.7:  # High repetition
                    if 'remove_redundancy' not in techniques:
                        techniques.append('remove_redundancy')

            # Technical shorthand opportunities
            if any(term in content for term in ['http', 'api', 'json', 'authentication']):
                if 'technical_shorthand' not in techniques:
                    techniques.append('technical_shorthand')

        return techniques
    
    def compress_file(self, file_path: str, dry_run: bool = False) -> str:
        """Compress a file using appropriate LSC techniques"""
        logger.info(f"{'Dry run: ' if dry_run else ''}Compressing {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            original = f.read()
        
        # Analyze first
        analysis = self.analyze_document(file_path)
        
        if not analysis.needs_compression:
            logger.info("Document doesn't need compression (score >= 0.6)")
            return original
        
        # Apply techniques
        compressed = original
        
        for technique in analysis.recommended_techniques:
            logger.info(f"Applying technique: {technique}")
            
            if technique == 'lists_tables':
                compressed = self.lsc.apply_lists_tables(compressed)
            elif technique == 'hierarchical_structure':
                compressed = self.lsc.apply_hierarchical_structure(compressed)
            elif technique == 'remove_redundancy':
                compressed = self.lsc.remove_redundancy(compressed)
            elif technique == 'technical_shorthand':
                compressed = self.lsc.apply_technical_shorthand(compressed)
            elif technique == 'information_density':
                compressed = self.lsc.increase_information_density(compressed)
        
        if dry_run:
            logger.info(f"Dry run complete. Would reduce from {len(original)} to {len(compressed)} characters")
            return compressed
        
        return compressed
    
    def compress_with_safety(self, original: str, compressed: str) -> ValidationResult:
        """Apply compression with comprehensive safety validation"""
        start_time = time.time()
        
        try:
            # Run safety validation
            safety_result = self.safety.validate_compression(original, compressed)
            
            validation_time = time.time() - start_time
            
            return ValidationResult(
                passed=safety_result['safe'],
                warnings=safety_result.get('warnings', []),
                failure_reason=safety_result.get('summary', ''),
                safety_details=safety_result.get('checks', {}),
                validation_time=validation_time
            )
            
        except Exception as e:
            logger.error(f"Error in safety validation: {e}")
            return ValidationResult(
                passed=False,
                warnings=[],
                failure_reason=f"Validation error: {str(e)}",
                safety_details={},
                validation_time=time.time() - start_time
            )
    
    def validate_compression(self, original: str, compressed: str) -> ValidationReport:
        """Generate comprehensive validation report"""
        start_time = time.time()
        
        # Safety validation
        safety_result = self.compress_with_safety(original, compressed)
        
        # Compression score
        score_result = self.scorer.calculate_score(compressed)
        compression_score = score_result['overall_score']
        
        # Token drift detection
        try:
            # Create temporary file for drift detection
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
                # Add baseline tokens to content for drift detection
                baseline_tokens = len(self.drift_detector.encoding.encode(original))
                content_with_header = f"""---
baseline_tokens: {baseline_tokens}
---
{compressed}"""
                f.write(content_with_header)
                temp_path = f.name
            
            drift_result = self.drift_detector.check_drift(temp_path)
            Path(temp_path).unlink()  # Clean up
            
        except Exception as e:
            logger.warning(f"Token drift detection failed: {e}")
            # Create dummy drift result
            drift_result = type('DriftResult', (), {
                'growth_detected': False,
                'ratio': 1.0,
                'recommendation': 'Unable to calculate drift'
            })()
        
        processing_time = time.time() - start_time
        
        return ValidationReport(
            original=original,
            compressed=compressed,
            safety_result=safety_result,
            compression_score=compression_score,
            token_drift=drift_result,
            processing_time=processing_time
        )


def setup_cli() -> argparse.ArgumentParser:
    """Set up command-line interface"""
    parser = argparse.ArgumentParser(
        description="Compression Tool MVP - Safely compress markdown documents using LSC techniques",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python compress.py analyze document.md
  python compress.py compress document.md --output compressed.md
  python compress.py compress document.md --dry-run --verbose
  python compress.py validate original.md compressed.md --report report.md
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze document compression opportunities')
    analyze_parser.add_argument('input_file', help='Input markdown file')
    analyze_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    # Compress command
    compress_parser = subparsers.add_parser('compress', help='Compress document with safety validation')
    compress_parser.add_argument('input_file', help='Input markdown file')
    compress_parser.add_argument('--output', '-o', help='Output file (default: input_compressed.md)')
    compress_parser.add_argument('--dry-run', action='store_true', help='Show changes without applying')
    compress_parser.add_argument('--force', action='store_true', help='Skip safety checks (dangerous)')
    compress_parser.add_argument('--report', help='Save validation report to file')
    compress_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate compression safety')
    validate_parser.add_argument('original', help='Original markdown file')
    validate_parser.add_argument('compressed', help='Compressed markdown file')
    validate_parser.add_argument('--report', help='Save validation report to file')
    validate_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    return parser


def main():
    """Main CLI entry point"""
    parser = setup_cli()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Set logging level
    if hasattr(args, 'verbose') and args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        tool = CompressionTool()
        
        if args.command == 'analyze':
            # Analyze document
            result = tool.analyze_document(args.input_file)
            
            print(f"\n📊 Analysis Results for {args.input_file}")
            print(f"Compression Score: {result.compression_score:.3f}/1.0")
            print(f"Needs Compression: {'Yes' if result.needs_compression else 'No'}")
            print(f"Analysis Time: {result.analysis_time:.2f}s")
            
            if result.recommended_techniques:
                print(f"\n🛠️ Recommended Techniques:")
                for technique in result.recommended_techniques:
                    print(f"  - {technique}")
            else:
                print(f"\n✅ No compression needed - document is already well-structured")
            
            if args.verbose and result.sections:
                print(f"\n📄 Section Analysis ({len(result.sections)} sections):")
                for i, section in enumerate(result.sections):
                    print(f"  {i+1}. {getattr(section, 'title', f'Section {i+1}')}")
        
        elif args.command == 'compress':
            # Compress document
            start_time = time.time()
            
            # Generate output path
            if args.output:
                output_path = args.output
            else:
                input_path = Path(args.input_file)
                output_path = input_path.parent / f"{input_path.stem}_compressed{input_path.suffix}"
            
            # Read original
            with open(args.input_file, 'r', encoding='utf-8') as f:
                original = f.read()
            
            # Compress
            compressed = tool.compress_file(args.input_file, dry_run=args.dry_run)
            
            # Safety validation (unless forced to skip)
            if not args.force:
                safety_result = tool.compress_with_safety(original, compressed)
                
                if not safety_result.passed:
                    print(f"❌ Compression blocked by safety validation:")
                    print(f"   Reason: {safety_result.failure_reason}")
                    if safety_result.warnings:
                        print(f"   Warnings: {', '.join(safety_result.warnings)}")
                    return
                
                if safety_result.warnings:
                    print(f"⚠️ Compression warnings:")
                    for warning in safety_result.warnings:
                        print(f"   - {warning}")
            else:
                logger.warning("Safety checks skipped with --force flag")
            
            # Generate report if requested
            if args.report:
                report = tool.validate_compression(original, compressed)
                with open(args.report, 'w', encoding='utf-8') as f:
                    f.write(report.to_markdown())
                print(f"📋 Report saved to {args.report}")
            
            if args.dry_run:
                print(f"\n🔍 Dry Run Results:")
                print(f"Would compress {args.input_file}")
                print(f"Original: {len(original)} characters")
                print(f"Compressed: {len(compressed)} characters")
                print(f"Reduction: {(1 - len(compressed)/len(original))*100:.1f}%")
            else:
                # Save compressed file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(compressed)
                
                total_time = time.time() - start_time
                print(f"✅ Compression completed in {total_time:.2f}s")
                print(f"📥 Input: {args.input_file} ({len(original)} chars)")
                print(f"📤 Output: {output_path} ({len(compressed)} chars)")
                print(f"📊 Reduction: {(1 - len(compressed)/len(original))*100:.1f}%")
        
        elif args.command == 'validate':
            # Validate compression
            with open(args.original, 'r', encoding='utf-8') as f:
                original = f.read()
            with open(args.compressed, 'r', encoding='utf-8') as f:
                compressed = f.read()
            
            report = tool.validate_compression(original, compressed)
            
            # Print summary
            status = "✅ PASSED" if report.safety_result.passed else "❌ FAILED"
            print(f"\n🔍 Validation Results: {status}")
            print(f"Compression Ratio: {report.compression_ratio:.3f}")
            print(f"Reduction: {report.reduction_percentage:.1f}%")
            print(f"Compression Score: {report.compression_score:.3f}/1.0")
            
            if not report.safety_result.passed:
                print(f"Failure Reason: {report.safety_result.failure_reason}")
            
            if report.safety_result.warnings:
                print(f"Warnings: {', '.join(report.safety_result.warnings)}")
            
            # Save report if requested
            if args.report:
                with open(args.report, 'w', encoding='utf-8') as f:
                    f.write(report.to_markdown())
                print(f"📋 Full report saved to {args.report}")
    
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        if hasattr(args, 'verbose') and args.verbose:
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())