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
# PHASE 2: DETERMINISTIC COMPRESSION (Placeholder for Checkpoint 2)
# ============================================================================

def compress_by_tier(section: Dict) -> str:
    """
    Apply tier-specific compression rules.

    This will be implemented in Checkpoint 2.
    For now, returns content as-is.
    """
    return section.get("content", "")


# ============================================================================
# MAIN CLI (Placeholder for Checkpoint 3)
# ============================================================================

def main():
    """Main CLI entry point."""
    print("compress_v7_classify.py - Checkpoint 1: Classification Phase")
    print("Full implementation in Checkpoints 2-3")


if __name__ == '__main__':
    main()
