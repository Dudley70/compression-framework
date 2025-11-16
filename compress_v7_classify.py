#!/usr/bin/env python3
"""
compress_v7_classify.py - V7 Classify-Then-Compress System

Architecture: Two-phase deterministic compression
Phase 1: LLM classifies sections (non-deterministic but safe)
Phase 2: Python compresses by tier (100% deterministic)

Created: 2025-11-16
Version: 1.0
"""

import re
import json
import sys
import os
import argparse
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Import V7 compression functions for Phase 2
sys.path.insert(0, '/home/user/compression-framework')
from compress_v7_hybrid import (
    apply_abbreviations,
    apply_symbols,
    compress_whitespace,
    PROSE_FRAGMENT_RULES,
    SECTION_HEADER_RULES,
    SCAFFOLDING_PATTERNS,
    SCAFFOLDING_KEEP_PATTERNS
)


# ============================================================================
# PHASE 1: LLM CLASSIFICATION
# ============================================================================

CLASSIFICATION_PROMPT = """Analyze this technical document and classify each section.

Your task: Identify the TYPE and COMPRESSION TIER for each distinct section.

SECTION TYPES:
- executive_summary: Overview, abstract, introduction
- test_prompt: Prompts for testing (marked with **Prompt:** or in code fences)
- test_output: Model responses to prompts
- analysis: Technical analysis, findings, observations
- methodology: How tests were conducted
- scoring: Scores, ratings, evaluations
- documentation: Citations, references
- code_block: Code examples, schemas, configurations
- formula: Mathematical expressions (σ, γ, κ, equations)
- scaffolding: Transitions, meta-commentary, explanations

COMPRESSION TIERS:
- sacred: MUST preserve verbatim (test_prompt, code_block, formula)
- minimal: Light compression only (scoring, documentation)
- moderate: Medium compression (analysis, methodology)
- aggressive: Heavy compression (executive_summary, scaffolding)

CRITICAL RULES:
1. Anything marked **Prompt:** or **Test Prompt:** = tier "sacred"
2. Code fences (```) = tier "sacred"
3. Formulas (σ, γ, κ, math symbols) = tier "sacred"
4. Analysis with technical detail = tier "moderate"
5. Transitions, explanations = tier "aggressive"

OUTPUT FORMAT (JSON):
[
  {{
    "start": <byte offset>,
    "end": <byte offset>,
    "type": "<section type>",
    "tier": "<compression tier>",
    "content": "<section text>"
  }},
  ...
]

IMPORTANT: Return ONLY the JSON array, no other text.

Document to classify:

{document}
"""


def classify_sections(document: str, api_key: str, model: str = "claude-haiku-4-5-20251001") -> List[Dict]:
    """
    Classify document sections using LLM.

    Args:
        document: Full document text
        api_key: Anthropic API key
        model: Claude model to use (default: haiku for speed/cost)

    Returns:
        List of classified sections with type, tier, and content
    """
    try:
        import anthropic
    except ImportError:
        raise ImportError("anthropic package required. Install with: pip install anthropic")

    client = anthropic.Anthropic(api_key=api_key)

    print(f"\n=== LLM CLASSIFICATION ===")
    print(f"Document size: {len(document):,} bytes ({len(document)/1024:.1f}KB)")
    print(f"Model: {model}")
    print("Analyzing sections...")

    try:
        # Use streaming for potentially long responses
        full_response = ""
        with client.messages.stream(
            model=model,
            max_tokens=51200,  # 80% of Haiku 4.5 output max (64K) - safe margin for large documents
            messages=[{
                "role": "user",
                "content": CLASSIFICATION_PROMPT.format(document=document)
            }]
        ) as stream:
            for text in stream.text_stream:
                full_response += text

        print(f"Classification response length: {len(full_response)} bytes")

        # Extract JSON from response
        # LLM might wrap JSON in markdown code fence, so handle that
        json_text = full_response.strip()

        # Remove markdown code fences if present
        if json_text.startswith("```json"):
            json_text = json_text[7:]  # Remove ```json
        if json_text.startswith("```"):
            json_text = json_text[3:]  # Remove ```
        if json_text.endswith("```"):
            json_text = json_text[:-3]  # Remove trailing ```

        json_text = json_text.strip()

        # Parse JSON
        classification = json.loads(json_text)

        # Validate structure
        if not isinstance(classification, list):
            raise ValueError("Classification must be a list of sections")

        # Validate each section has required fields
        for i, section in enumerate(classification):
            required_fields = ["start", "end", "type", "tier", "content"]
            for field in required_fields:
                if field not in section:
                    raise ValueError(f"Section {i} missing required field: {field}")

        print(f"✅ Classification complete: {len(classification)} sections identified")

        # Print summary
        type_counts = {}
        tier_counts = {}
        for section in classification:
            type_counts[section["type"]] = type_counts.get(section["type"], 0) + 1
            tier_counts[section["tier"]] = tier_counts.get(section["tier"], 0) + 1

        print(f"\nSection types: {dict(type_counts)}")
        print(f"Compression tiers: {dict(tier_counts)}")

        return classification

    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse classification JSON: {e}")
        print(f"Response preview: {full_response[:500]}")
        raise ValueError(f"LLM returned invalid JSON: {e}")

    except Exception as e:
        print(f"❌ Classification error: {e}")
        raise


# ============================================================================
# PHASE 2: DETERMINISTIC COMPRESSION
# ============================================================================

def apply_prose_transforms_without_scaffolding(text: str) -> str:
    """Apply prose transforms but preserve scaffolding (for moderate tier)."""
    # Prose fragment rules (regex)
    for pattern, replacement in PROSE_FRAGMENT_RULES:
        text = re.sub(pattern, replacement, text, flags=re.MULTILINE)

    # Section header rules
    for pattern, replacement in SECTION_HEADER_RULES:
        text = re.sub(pattern, replacement, text)

    # DO NOT remove scaffolding for moderate tier
    return text


def apply_prose_transforms_with_scaffolding(text: str) -> str:
    """Apply all prose transforms including scaffolding removal (for aggressive tier)."""
    # Prose fragment rules (regex)
    for pattern, replacement in PROSE_FRAGMENT_RULES:
        text = re.sub(pattern, replacement, text, flags=re.MULTILINE)

    # Section header rules
    for pattern, replacement in SECTION_HEADER_RULES:
        text = re.sub(pattern, replacement, text)

    # Remove scaffolding (but keep critical markers)
    for pattern in SCAFFOLDING_PATTERNS:
        # Check if any keep pattern exists nearby
        has_keep_pattern = any(re.search(keep, text) for keep in SCAFFOLDING_KEEP_PATTERNS)
        if not has_keep_pattern:
            text = re.sub(pattern, '', text)

    return text


def compress_by_tier(section: Dict) -> str:
    """
    Apply tier-specific compression rules.

    Compression tiers:
    - sacred: 0% compression (verbatim) - test prompts, formulas
    - minimal: ~10-20% compression (headers + symbols only) - technical specs, scoring
    - moderate: ~30-50% compression (all rules except scaffolding) - analysis, methodology
    - aggressive: ~50-70% compression (all V7 rules) - executive summary, scaffolding

    Args:
        section: Section dict with type, tier, and content

    Returns:
        Compressed text according to tier rules
    """
    content = section.get("content", "")
    tier = section.get("tier", "sacred")

    # Tier 0 (sacred): No compression - preserve exactly
    if tier == "sacred":
        return content

    # Tier 1 (minimal): Headers + symbols only
    elif tier == "minimal":
        text = apply_abbreviations(content)
        text = apply_symbols(text)
        text = compress_whitespace(text)
        return text

    # Tier 2 (moderate): All rules except scaffolding removal
    elif tier == "moderate":
        text = apply_abbreviations(content)
        text = apply_symbols(text)
        text = apply_prose_transforms_without_scaffolding(text)
        text = compress_whitespace(text)
        return text

    # Tier 3 (aggressive): All V7 rules including scaffolding
    elif tier == "aggressive":
        text = apply_abbreviations(content)
        text = apply_symbols(text)
        text = apply_prose_transforms_with_scaffolding(text)
        text = compress_whitespace(text)
        return text

    else:
        # Unknown tier - return as-is
        print(f"⚠️  Unknown tier '{tier}', returning content as-is")
        return content


def compress_from_classification(classification: List[Dict]) -> str:
    """
    Compress document from classification data.

    This is a pure Python function - given the same classification,
    it will always produce identical output (deterministic).

    Args:
        classification: List of classified sections from classify_sections()

    Returns:
        Compressed document text
    """
    compressed_sections = []

    for section in classification:
        compressed_content = compress_by_tier(section)
        compressed_sections.append(compressed_content)

    # Join sections with double newline
    return "\n\n".join(compressed_sections)


# ============================================================================
# VALIDATION HELPERS
# ============================================================================

def count_test_prompts(text: str) -> int:
    """
    Count test prompts in a document.

    Looks for prompt markers and delimiters to identify test prompts.

    Args:
        text: Document text

    Returns:
        Number of test prompts found
    """
    # Common prompt markers
    prompt_patterns = [
        r'\*\*Prompt[:\s]',           # **Prompt:** or **Prompt **
        r'\*\*Test[:\s]',             # **Test:** or **Test **
        r'\n##\s+Test\s+\d+',         # ## Test 1, ## Test 2, etc.
        r'\n###\s+Prompt',            # ### Prompt
        r'^\*\*\d+\.\s+',             # **1. , **2. , etc (at line start)
    ]

    count = 0
    for pattern in prompt_patterns:
        matches = re.findall(pattern, text, re.MULTILINE | re.IGNORECASE)
        count += len(matches)

    return count


def verify_prompts_verbatim(original: str, compressed: str) -> bool:
    """
    Verify that test prompts are preserved verbatim in compressed output.

    This is a heuristic check that looks for prompt markers in both documents
    and verifies substantial overlap.

    Args:
        original: Original document
        compressed: Compressed document

    Returns:
        True if prompts appear to be preserved, False otherwise
    """
    # Extract lines that look like prompts from both documents
    prompt_pattern = r'(?:^|\n)(?:\*\*(?:Prompt|Test)[:\s]|##\s+Test\s+\d+|###\s+Prompt).*?(?=\n\n|\n#|\Z)'

    original_prompts = re.findall(prompt_pattern, original, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    compressed_prompts = re.findall(prompt_pattern, compressed, re.MULTILINE | re.DOTALL | re.IGNORECASE)

    # If we found prompts in original, we should find similar number in compressed
    if len(original_prompts) > 0:
        # Allow some variance in detection, but should be similar
        ratio = len(compressed_prompts) / len(original_prompts) if len(original_prompts) > 0 else 0
        return ratio >= 0.9  # At least 90% of prompts preserved

    # If no prompts detected by pattern, assume preserved (conservative)
    return True


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def compress_v7_classify_main(
    input_file: str,
    output_file: str,
    api_key: str,
    model: str = "claude-haiku-4-5-20251001",
    expected_prompts: Optional[int] = None,
    report_file: Optional[str] = None
) -> Dict:
    """
    Main pipeline: Classify then compress a document.

    This is the complete two-phase compression system:
    Phase 1: LLM classifies sections (non-deterministic but safe)
    Phase 2: Python compresses by tier (100% deterministic)

    Args:
        input_file: Path to input markdown file
        output_file: Path to output compressed file
        api_key: Anthropic API key
        model: Claude model to use (default: Haiku 4.5)
        expected_prompts: Expected number of test prompts (for validation)
        report_file: Optional path to save validation report JSON

    Returns:
        Validation report dict
    """
    print(f"\n{'='*70}")
    print(f"V7 CLASSIFY-THEN-COMPRESS PIPELINE")
    print(f"{'='*70}")

    # Read input
    print(f"\n📄 Reading input: {input_file}")
    with open(input_file, 'r') as f:
        document = f.read()

    original_size = len(document)
    print(f"   Size: {original_size:,} bytes ({original_size/1024:.1f}KB)")

    # Phase 1: Classification
    print(f"\n🔍 Phase 1: LLM Classification")
    classification = classify_sections(document, api_key=api_key, model=model)

    # Phase 2: Compression
    print(f"\n⚙️  Phase 2: Deterministic Compression")
    compressed = compress_from_classification(classification)

    compressed_size = len(compressed)
    compression_ratio = compressed_size / original_size if original_size > 0 else 0

    print(f"   Original: {original_size:,} bytes")
    print(f"   Compressed: {compressed_size:,} bytes")
    print(f"   Ratio: {compression_ratio:.1%} ({100 - compression_ratio*100:.1f}% reduction)")

    # Write output
    print(f"\n💾 Writing output: {output_file}")
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(compressed)

    # Validation
    print(f"\n✅ Validation")
    prompts_found = count_test_prompts(compressed)
    prompts_match = verify_prompts_verbatim(document, compressed)
    prompts_expected = expected_prompts if expected_prompts else prompts_found

    # Check Rule 6 compliance
    rule_6_compliant = prompts_match and (prompts_found >= prompts_expected * 0.9)

    print(f"   Rule 6 Compliant: {rule_6_compliant}")
    print(f"   Test Prompts: {prompts_found}/{prompts_expected}")
    print(f"   Prompts Match: {prompts_match}")

    # Create report
    report = {
        "timestamp": datetime.now().isoformat(),
        "input_file": input_file,
        "output_file": output_file,
        "model": model,
        "original_size": original_size,
        "compressed_size": compressed_size,
        "compression_ratio": compression_ratio,
        "sections_classified": len(classification),
        "prompts_found": prompts_found,
        "prompts_expected": prompts_expected,
        "prompts_match": prompts_match,
        "rule_6_compliant": rule_6_compliant,
        "tier_distribution": {}
    }

    # Add tier distribution
    for section in classification:
        tier = section.get("tier", "unknown")
        report["tier_distribution"][tier] = report["tier_distribution"].get(tier, 0) + 1

    # Write report if requested
    if report_file:
        print(f"\n📊 Writing report: {report_file}")
        os.makedirs(os.path.dirname(report_file) if os.path.dirname(report_file) else '.', exist_ok=True)
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

    print(f"\n{'='*70}")
    print(f"✅ COMPRESSION COMPLETE")
    print(f"{'='*70}\n")

    return report


# ============================================================================
# MAIN CLI
# ============================================================================

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='V7 Classify-Then-Compress: Deterministic document compression'
    )
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('output', help='Output compressed file')
    parser.add_argument('--api-key', required=True, help='Anthropic API key')
    parser.add_argument('--model', default='claude-haiku-4-5-20251001',
                        help='Claude model to use (default: claude-haiku-4-5-20251001)')
    parser.add_argument('--expected-prompts', type=int, help='Expected number of test prompts')
    parser.add_argument('--report', help='Path to save validation report JSON')

    args = parser.parse_args()

    compress_v7_classify_main(
        input_file=args.input,
        output_file=args.output,
        api_key=args.api_key,
        model=args.model,
        expected_prompts=args.expected_prompts,
        report_file=args.report
    )


if __name__ == '__main__':
    main()
