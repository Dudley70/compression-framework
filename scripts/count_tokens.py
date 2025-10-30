#!/usr/bin/env python3
"""
Helper script to count tokens and generate test fixtures with exact token counts.
"""
import tiktoken
import yaml
import re
from pathlib import Path

def count_tokens(text: str) -> int:
    """Count tokens using tiktoken cl100k_base encoding."""
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def remove_yaml_frontmatter(content: str) -> str:
    """Remove YAML frontmatter from content."""
    if content.startswith('---'):
        # Find the end of the frontmatter
        parts = content.split('---', 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content

def generate_content_with_target_tokens(target_tokens: int, base_text: str = None) -> str:
    """Generate content that has approximately the target number of tokens."""
    if base_text is None:
        base_text = """This is a test document for the token drift detection system. It is designed to evaluate how well the system can detect when previously compressed documents have grown significantly due to new content additions.

The compression research project uses a unified theory where all compression techniques optimize three parameters: sigma (σ), gamma (γ), and kappa (κ), subject to comprehension constraints. This approach allows for systematic evaluation of different compression methods.

Token drift detection is a critical component because it identifies when documents that were previously compressed have accumulated enough new content to warrant re-compression. This helps maintain the effectiveness of the compression system over time.

The system works by comparing the current token count against a baseline stored in the document's YAML header. When the drift ratio exceeds certain thresholds, different recommendations are triggered: flag for monitoring, review for manual inspection, or compress for automatic re-compression.

This particular test document is carefully crafted to contain exactly the target number of tokens needed for testing various drift scenarios. The content is meaningful but repetitive enough to allow precise token count control."""

    current_tokens = count_tokens(base_text)

    if current_tokens < target_tokens:
        # Need to add more content
        additional_needed = target_tokens - current_tokens

        # Generate additional sentences
        padding_sentences = [
            " This sentence adds more tokens to reach the target count.",
            " Additional content helps test the token drift detection system.",
            " The algorithm must accurately measure document growth over time.",
            " Compression efficiency depends on maintaining optimal token ratios.",
            " Test documents require precise token counts for validation purposes.",
            " Token counting excludes YAML frontmatter but includes all other text.",
            " The drift detection system provides actionable recommendations.",
            " Threshold values determine when documents need attention.",
            " Automated compression maintains document quality and efficiency.",
            " Validation testing ensures the system works correctly."
        ]

        # Add sentences until we reach the target
        sentence_index = 0
        while count_tokens(base_text) < target_tokens:
            sentence = padding_sentences[sentence_index % len(padding_sentences)]
            base_text += sentence
            sentence_index += 1

            # Safety check to avoid infinite loop
            if sentence_index > 1000:
                break

    elif current_tokens > target_tokens:
        # Need to trim content
        words = base_text.split()
        while count_tokens(' '.join(words)) > target_tokens and len(words) > 10:
            words.pop()
        base_text = ' '.join(words)

    return base_text

def create_test_fixture(filename: str, baseline_tokens: int, target_tokens: int,
                       has_header: bool = True, malformed: bool = False):
    """Create a test fixture file with specific token counts."""

    # Generate content for the target token count
    content_text = generate_content_with_target_tokens(target_tokens)

    # Create the full document
    if not has_header:
        # No header case
        full_content = f"""# Document Without Header

This document has no compression metadata.
It should be marked as "untracked" since we cannot
calculate drift without a baseline.

{content_text}"""
    elif malformed:
        # Malformed header case
        full_content = f"""---
compression:
  last_full_compression: 2025-10-30
  # Missing baseline_tokens field
---

{content_text}"""
    else:
        # Normal header case
        header = {
            'compression': {
                'last_full_compression': '2025-10-30 15:30 AEDT',
                'baseline_tokens': baseline_tokens,
                'parameters': {'σ': 0.8, 'γ': 0.6, 'κ': 0.2}
            }
        }

        yaml_header = yaml.dump(header, default_flow_style=False, sort_keys=False)

        full_content = f"""---
{yaml_header}---

{content_text}"""

    # Verify token count (excluding header)
    content_only = remove_yaml_frontmatter(full_content)
    actual_tokens = count_tokens(content_only)

    print(f"Creating {filename}:")
    print(f"  Target tokens: {target_tokens}")
    print(f"  Actual tokens: {actual_tokens}")
    print(f"  Baseline tokens: {baseline_tokens}")
    if baseline_tokens and actual_tokens:
        drift_ratio = actual_tokens / baseline_tokens
        print(f"  Drift ratio: {drift_ratio:.2f}")
    print()

    # Write the file
    Path(f"tests/fixtures/{filename}").write_text(full_content)

if __name__ == "__main__":
    print("Generating test fixtures with precise token counts...\n")

    # Test Case 1: No drift (1000 tokens baseline, 1000 tokens current)
    create_test_fixture("no_drift.md", 1000, 1000)

    # Test Case 2: Minor drift (1000 tokens baseline, 1050 tokens current = 5% growth)
    create_test_fixture("minor_drift.md", 1000, 1050)

    # Test Case 3: Moderate drift (1000 tokens baseline, 1250 tokens current = 25% growth)
    create_test_fixture("moderate_drift.md", 1000, 1250)

    # Test Case 4: Substantial drift (1000 tokens baseline, 1500 tokens current = 50% growth)
    create_test_fixture("substantial_drift.md", 1000, 1500)

    # Test Case 5: No header (untracked document)
    create_test_fixture("no_header.md", None, 500, has_header=False)

    # Test Case 6: Malformed header (missing baseline_tokens)
    create_test_fixture("malformed_header.md", None, 300, malformed=True)

    print("All test fixtures created successfully!")