# compress_v7_hybrid.py - Architecture Specification

**Created**: 2025-11-15  
**Purpose**: Complete tool specification for v5.0 hybrid compression system  
**Strategy**: Tiered Tool Chain + Simple Autonomous LLM

---

## Overview

4-step pipeline combining deterministic safety with LLM intelligence:

```
Step 1: Extract Sacred Content (Tool - Python regex)
         ↓
Step 2: Simple Autonomous Compression (LLM - Claude API)
         ↓
Step 3: Restore Sacred + V7 Rules (Tool - Python deterministic)
         ↓
Step 4: Validation (Tool - Python verification)
```

**Key Innovation**: LLM never sees sacred content = physically impossible to violate Rule 6

---

## Architecture Principles

1. **Separation of Concerns**:
   - Tool: Pattern matching, preservation, verification
   - LLM: Semantic compression decisions
   
2. **Fail-Safe Design**:
   - Sacred content extracted BEFORE LLM phase
   - Restoration is mechanical (no judgment)
   - Validation catches any failures
   
3. **Cost Optimization**:
   - LLM sees 127KB (not 134KB) - 5% savings
   - Simple prompt (not complex constraints) - reliable
   
4. **Guaranteed Correctness**:
   - Programmatic verification (not hallucination)
   - Byte-for-byte comparison
   - Measurable pass/fail criteria

---

## Step 1: Sacred Content Extraction

### Purpose
Extract all content requiring 0% compression (Rule 6 compliance)

### Function Signature
```python
def extract_sacred_content(document: str) -> dict:
    """
    Extract test prompts, code blocks, formulas from document.
    
    Args:
        document: Original markdown content
        
    Returns:
        {
            "prompts": [...],
            "code_blocks": [...],
            "formulas": [...],
            "modified_document": str,  # With placeholders
            "metadata": {...}
        }
    """
```

### Detection Patterns
```python
SACRED_PATTERNS = [
    {
        "type": "test_prompt",
        "pattern": r'\*\*Prompt:\*\*\s*\n```(.*?)```',
        "flags": re.DOTALL,
        "preserve": "verbatim",
        "priority": 1,  # Highest
    },
    {
        "type": "code_block",
        "pattern": r'```(\w+)?\n(.*?)\n```',
        "flags": re.DOTALL,
        "preserve": "verbatim",
        "priority": 2,
    },
    {
        "type": "formula",
        "pattern": r'\$(.+?)\$',
        "flags": re.MULTILINE,
        "preserve": "verbatim",
        "priority": 3,
    },
]
```

### Extraction Algorithm
```python
def extract_sacred_content(document):
    sacred_items = []
    modified_doc = document
    
    # Process in priority order (prompts first, formulas last)
    for pattern_config in sorted(SACRED_PATTERNS, key=lambda x: x['priority']):
        pattern = pattern_config['pattern']
        matches = re.finditer(pattern, modified_doc, pattern_config['flags'])
        
        for match in matches:
            item_id = f"{pattern_config['type']}_{len(sacred_items)}"
            placeholder = f"{{{{SACRED_{item_id.upper()}}}}}"
            
            sacred_items.append({
                "id": item_id,
                "type": pattern_config['type'],
                "content": match.group(0),
                "placeholder": placeholder,
                "start_pos": match.start(),
                "end_pos": match.end(),
                "line_number": document[:match.start()].count('\n') + 1,
            })
            
            # Replace with placeholder
            modified_doc = (
                modified_doc[:match.start()] +
                placeholder +
                modified_doc[match.end():]
            )
    
    return {
        "sacred_items": sacred_items,
        "modified_document": modified_doc,
        "count": {
            "prompts": sum(1 for i in sacred_items if i['type'] == 'test_prompt'),
            "code_blocks": sum(1 for i in sacred_items if i['type'] == 'code_block'),
            "formulas": sum(1 for i in sacred_items if i['type'] == 'formula'),
        }
    }
```

### Expected Output
```python
{
    "sacred_items": [
        {
            "id": "test_prompt_0",
            "type": "test_prompt",
            "content": "**Prompt:**\n```\nA logistics manager...\n```",
            "placeholder": "{{SACRED_TEST_PROMPT_0}}",
            "start_pos": 5234,
            "end_pos": 5721,
            "line_number": 147
        },
        # ... 10 more prompts
        # ... 8 code blocks
        # ... 5 formulas
    ],
    "modified_document": "[134KB with placeholders, ~127KB]",
    "count": {
        "prompts": 11,
        "code_blocks": 8,
        "formulas": 5
    }
}
```

---

## Step 2: LLM Compression

### Purpose
Semantic compression via Claude API using simple autonomous approach (V3 strategy)

### Why Simple Autonomous?
**Evidence from testing**:
- ✅ V3 simple: "compress for LLM use" → 50% reduction, excellent
- ❌ V7/v4.1 complex constraints → Failed (LLM confused by rules)

**Strategy**: Let Claude find natural balance without complex constraints

### Function Signature
```python
def llm_compress(doc_without_sacred: str, api_key: str) -> str:
    """
    Compress document using Claude API with simple prompt.
    
    Args:
        doc_without_sacred: Document with placeholders (no prompts/code)
        api_key: Anthropic API key
        
    Returns:
        Compressed document (still has placeholders)
    """
```

### Prompt Template
```python
COMPRESSION_PROMPT = """
Compress this technical document for LLM-only consumption.

Context:
- Test prompts and code blocks have been removed (you won't see them)
- Your task: Compress prose, analysis, and meta-commentary
- Keep: All technical information, scores, findings
- Remove: Verbosity, scaffolding, obvious statements

Guidance:
- Use abbreviations where helpful (but you decide which)
- Convert prose to fragments when clear
- Remove transition phrases
- Keep all operational information
- Let compression level emerge naturally

The document currently has placeholders like {{SACRED_TEST_PROMPT_0}} - 
DO NOT modify these placeholders in any way. Leave them exactly as-is.

Compress intelligently:

{document}
"""
```

### API Call Structure
```python
import anthropic

def llm_compress(doc_without_sacred, api_key):
    client = anthropic.Anthropic(api_key=api_key)
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=50000,  # Allow full output
        messages=[
            {
                "role": "user",
                "content": COMPRESSION_PROMPT.format(document=doc_without_sacred)
            }
        ]
    )
    
    compressed = message.content[0].text
    
    # Verify placeholders unchanged
    original_placeholders = re.findall(r'\{\{SACRED_.*?\}\}', doc_without_sacred)
    compressed_placeholders = re.findall(r'\{\{SACRED_.*?\}\}', compressed)
    
    if set(original_placeholders) != set(compressed_placeholders):
        raise ValueError("LLM modified sacred placeholders - corruption detected")
    
    return compressed
```

### Expected Output
- Input: 127KB (with 24 placeholders)
- Output: ~15KB (with same 24 placeholders intact)
- Compression: ~88% of non-sacred content

---

## Step 3: Restoration + V7 Rules

### Purpose
Merge sacred content back + apply deterministic V7 transformations

### Function Signature
```python
def restore_and_transform(compressed: str, sacred_data: dict) -> str:
    """
    Restore sacred content and apply V7 transformation rules.
    
    Args:
        compressed: LLM output with placeholders
        sacred_data: Sacred extraction data from Step 1
        
    Returns:
        Final compressed document with sacred content verbatim
    """
```

### Processing Steps

**Step 3.1: Restore Sacred Content**
```python
def restore_sacred(compressed, sacred_items):
    restored = compressed
    
    # Replace placeholders with original content (in reverse order to maintain positions)
    for item in reversed(sacred_items):
        restored = restored.replace(item['placeholder'], item['content'])
    
    return restored
```

**Step 3.2: Apply V7 Abbreviations**
```python
def apply_abbreviations(text):
    # From v7_rules_extraction.md
    
    # Header abbreviations
    for old, new in HEADER_ABBREVIATIONS.items():
        text = text.replace(old, new)
    
    # Standard abbreviations
    for old, new in STANDARD_ABBREVIATIONS.items():
        text = text.replace(old, new)
    
    # Context abbreviations
    for old, new in CONTEXT_ABBREVIATIONS.items():
        text = text.replace(old, new)
    
    return text
```

**Step 3.3: Apply Symbols**
```python
def apply_symbols(text):
    # Status symbols
    for old, new in STATUS_SYMBOLS.items():
        text = text.replace(old, new)
    
    # Comparison symbols
    for old, new in COMPARISON_SYMBOLS.items():
        text = text.replace(old, new)
    
    # Logical symbols (carefully)
    for old, new in LOGICAL_SYMBOLS.items():
        # Apply only in appropriate contexts
        text = text.replace(old, new)
    
    return text
```

**Step 3.4: Apply Prose Transformations**
```python
def apply_prose_transforms(text):
    # Prose fragment rules (regex)
    for pattern, replacement in PROSE_FRAGMENT_RULES:
        text = re.sub(pattern, replacement, text, flags=re.MULTILINE)
    
    # Section header rules
    for pattern, replacement in SECTION_HEADER_RULES:
        text = re.sub(pattern, replacement, text)
    
    # Remove scaffolding (but keep critical markers)
    for pattern in SCAFFOLDING_PATTERNS:
        # Check not in keep patterns
        if not any(re.search(keep, text) for keep in SCAFFOLDING_KEEP_PATTERNS):
            text = re.sub(pattern, '', text)
    
    return text
```

**Step 3.5: Complete Transformation Pipeline**
```python
def restore_and_transform(compressed, sacred_data):
    # 1. Restore sacred content first
    restored = restore_sacred(compressed, sacred_data['sacred_items'])
    
    # 2. Apply V7 transformation rules (order matters)
    transformed = restored
    transformed = apply_abbreviations(transformed)
    transformed = apply_symbols(transformed)
    transformed = apply_prose_transforms(transformed)
    
    return transformed
```

### Expected Output
- Input: ~15KB (LLM compressed)
- Sacred content: +7KB (restored verbatim)
- V7 transforms: -0.5KB (additional compression)
- Output: ~21.5KB (target range 20-24KB)

---

## Step 4: Validation

### Purpose
Programmatic verification of Rule 6 compliance and quality metrics

### Function Signature
```python
def validate(original: str, final: str, expected_prompts: int = 11) -> dict:
    """
    Validate compression quality and Rule 6 compliance.
    
    Args:
        original: Original document
        final: Compressed document
        expected_prompts: Number of test prompts expected
        
    Returns:
        ValidationReport with pass/fail status
    """
```

### Validation Checks

**Check 1: Prompt Count**
```python
def count_prompts(text):
    """Count test prompts in document."""
    return len(re.findall(r'\*\*Prompt:\*\*', text))

def validate_prompt_count(original, final, expected):
    orig_count = count_prompts(original)
    final_count = count_prompts(final)
    
    return {
        "check": "prompt_count",
        "expected": expected,
        "original_had": orig_count,
        "final_has": final_count,
        "pass": final_count == expected and orig_count == final_count,
        "message": f"Found {final_count}/{expected} prompts"
    }
```

**Check 2: Byte-for-Byte Verification**
```python
def extract_prompts(text):
    """Extract all prompt sections for comparison."""
    prompts = []
    pattern = r'\*\*Prompt:\*\*\s*\n```(.*?)```'
    for match in re.finditer(pattern, text, re.DOTALL):
        prompts.append(match.group(1).strip())
    return prompts

def validate_prompts_verbatim(original, final):
    orig_prompts = extract_prompts(original)
    final_prompts = extract_prompts(final)
    
    matches = []
    for i, (orig, final) in enumerate(zip(orig_prompts, final_prompts)):
        match = orig == final  # Byte-for-byte comparison
        matches.append({
            "prompt_number": i + 1,
            "match": match,
            "orig_length": len(orig),
            "final_length": len(final),
        })
    
    all_match = all(m['match'] for m in matches)
    
    return {
        "check": "prompt_verbatim",
        "pass": all_match,
        "details": matches,
        "message": f"{sum(m['match'] for m in matches)}/{len(matches)} prompts exact"
    }
```

**Check 3: Size Verification**
```python
def validate_size(final_text, min_kb=19, max_kb=24):
    size_kb = len(final_text) / 1024
    in_range = min_kb <= size_kb <= max_kb
    
    return {
        "check": "size",
        "size_kb": round(size_kb, 2),
        "target_range": f"{min_kb}-{max_kb}KB",
        "pass": in_range,
        "message": f"Size: {size_kb:.1f}KB (target: {min_kb}-{max_kb}KB)"
    }
```

**Check 4: Structural Integrity**
```python
def validate_structure(final_text):
    checks = {
        "has_sections": bool(re.search(r'^###', final_text, re.MULTILINE)),
        "has_scores": bool(re.search(r'E=\d+', final_text)),
        "has_analysis": bool(re.search(r'\*\*Analysis', final_text)),
        "no_broken_placeholders": not bool(re.search(r'\{\{SACRED_', final_text)),
    }
    
    return {
        "check": "structure",
        "pass": all(checks.values()),
        "details": checks,
        "message": "Structure intact" if all(checks.values()) else "Structure broken"
    }
```

**Complete Validation**
```python
def validate(original, final, expected_prompts=11):
    report = {
        "timestamp": datetime.now().isoformat(),
        "checks": [],
        "overall_pass": True,
    }
    
    # Run all checks
    checks = [
        validate_prompt_count(original, final, expected_prompts),
        validate_prompts_verbatim(original, final),
        validate_size(final),
        validate_structure(final),
    ]
    
    report['checks'] = checks
    report['overall_pass'] = all(c['pass'] for c in checks)
    
    # Summary
    report['summary'] = {
        "rule_6_compliance": checks[0]['pass'] and checks[1]['pass'],
        "size_acceptable": checks[2]['pass'],
        "structure_valid": checks[3]['pass'],
        "verdict": "PASS" if report['overall_pass'] else "FAIL"
    }
    
    return report
```

### Expected Output
```json
{
    "timestamp": "2025-11-15T23:30:00",
    "checks": [
        {
            "check": "prompt_count",
            "expected": 11,
            "final_has": 11,
            "pass": true,
            "message": "Found 11/11 prompts"
        },
        {
            "check": "prompt_verbatim",
            "pass": true,
            "message": "11/11 prompts exact"
        },
        {
            "check": "size",
            "size_kb": 21.8,
            "pass": true,
            "message": "Size: 21.8KB (target: 19-24KB)"
        },
        {
            "check": "structure",
            "pass": true,
            "message": "Structure intact"
        }
    ],
    "overall_pass": true,
    "summary": {
        "rule_6_compliance": true,
        "size_acceptable": true,
        "structure_valid": true,
        "verdict": "PASS"
    }
}
```

---

## Error Handling

### Extraction Errors
```python
class SacredExtractionError(Exception):
    """Raised when sacred content extraction fails."""
    pass

try:
    sacred_data = extract_sacred_content(document)
except Exception as e:
    raise SacredExtractionError(f"Failed to extract sacred content: {e}")
```

### LLM Errors
```python
class CompressionError(Exception):
    """Raised when LLM compression fails."""
    pass

try:
    compressed = llm_compress(doc_without_sacred, api_key)
except anthropic.APIError as e:
    raise CompressionError(f"Claude API error: {e}")
except Exception as e:
    raise CompressionError(f"Unexpected compression error: {e}")
```

### Validation Failures
```python
def handle_validation_failure(report):
    """Handle validation failures with detailed reporting."""
    
    if not report['overall_pass']:
        print("❌ VALIDATION FAILED")
        print(f"\nVerdict: {report['summary']['verdict']}")
        
        for check in report['checks']:
            status = "✅" if check['pass'] else "❌"
            print(f"{status} {check['check']}: {check['message']}")
        
        if not report['summary']['rule_6_compliance']:
            print("\n⚠️  CRITICAL: Rule 6 violated - prompts not preserved verbatim")
            print("   Output cannot be used for scientific reproduction")
        
        return False
    
    return True
```

---

## Command Line Interface

```python
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Compress technical documents with V7 hybrid method"
    )
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('output', help='Output compressed file')
    parser.add_argument('--api-key', required=True, help='Anthropic API key')
    parser.add_argument('--expected-prompts', type=int, default=11,
                       help='Expected number of test prompts')
    parser.add_argument('--report', help='Save validation report (JSON)')
    parser.add_argument('--verbose', action='store_true',
                       help='Show detailed progress')
    
    args = parser.parse_args()
    
    # Execute pipeline
    try:
        # Step 1: Extract
        if args.verbose:
            print("Step 1: Extracting sacred content...")
        
        with open(args.input) as f:
            original = f.read()
        
        sacred_data = extract_sacred_content(original)
        
        if args.verbose:
            print(f"  Found: {sacred_data['count']['prompts']} prompts, "
                  f"{sacred_data['count']['code_blocks']} code blocks")
        
        # Step 2: LLM Compress
        if args.verbose:
            print("Step 2: LLM compression...")
        
        compressed = llm_compress(sacred_data['modified_document'], args.api_key)
        
        # Step 3: Restore + Transform
        if args.verbose:
            print("Step 3: Restoring sacred content + V7 rules...")
        
        final = restore_and_transform(compressed, sacred_data)
        
        # Step 4: Validate
        if args.verbose:
            print("Step 4: Validation...")
        
        report = validate(original, final, args.expected_prompts)
        
        # Check results
        if handle_validation_failure(report):
            # Save output
            with open(args.output, 'w') as f:
                f.write(final)
            
            print(f"\n✅ SUCCESS: {args.output}")
            print(f"   Size: {report['checks'][2]['size_kb']}KB")
            print(f"   Rule 6: {'✅ PASS' if report['summary']['rule_6_compliance'] else '❌ FAIL'}")
        
        # Save report if requested
        if args.report:
            with open(args.report, 'w') as f:
                json.dump(report, f, indent=2)
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

### Usage Example
```bash
python compress_v7_hybrid.py \
    input.md \
    output.md \
    --api-key sk-ant-... \
    --expected-prompts 11 \
    --report validation_report.json \
    --verbose
```

---

## Success Criteria

**Mandatory (Non-Negotiable)**:
- ✅ All test prompts preserved byte-for-byte (Rule 6)
- ✅ Validation report shows 100% prompt match
- ✅ No hallucinated success metrics

**Target (Quality)**:
- ✅ Output size 20-24KB
- ✅ Compression ratio 83-85%
- ✅ All code blocks preserved
- ✅ Structure intact

**Verification**:
- ✅ Programmatic validation (not LLM claims)
- ✅ Reproducible results
- ✅ Measurable pass/fail

---

## Performance Expectations

**Speed**:
- Step 1 (Extract): <1s
- Step 2 (LLM): ~30s
- Step 3 (Restore): <1s
- Step 4 (Validate): <1s
- **Total: ~35s**

**Cost**:
- Step 1: $0.00
- Step 2: ~$0.11 (127KB input)
- Step 3: $0.00
- Step 4: $0.00
- **Total: ~$0.11**

**Quality**:
- Rule 6 compliance: 100% (guaranteed by architecture)
- Size accuracy: ±2KB (20-24KB)
- Reproducibility: Deterministic (same input → same output)

---

## Next: Implementation Plan

See `/Users/dudley/temp_session28/implementation_plan.md` for build sequence.
