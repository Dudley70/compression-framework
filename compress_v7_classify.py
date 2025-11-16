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
# MAIN CLI (Placeholder for Checkpoint 3)
# ============================================================================

def main():
    """Main CLI entry point."""
    print("compress_v7_classify.py - Checkpoint 1: Classification Phase")
    print("Full implementation in Checkpoints 2-3")


if __name__ == '__main__':
    main()
