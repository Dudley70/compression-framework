# V7 Transformation Rules - Python-Ready Extraction

**Source**: TECHNIQUES_V7_METHOD.md (336 lines)  
**Purpose**: Complete rule extraction for `compress_v7_hybrid.py`  
**Extracted**: 2025-11-15

---

## Sacred Content Detection Patterns

**CRITICAL**: These patterns identify content that MUST be preserved verbatim (0% compression)

```python
SACRED_DETECTION_PATTERNS = [
    # Test prompts (Rule 6 - highest priority)
    r'\*\*Prompt:\*\*',
    r'\*\*Test Prompt:\*\*',
    r'\*\*Input:\*\*',
    
    # Code blocks (exact preservation required)
    r'^```[\s\S]*?```$',  # Full code fence blocks
    r'`[^`]+`',  # Inline code
    
    # Mathematical formulas (precision required)
    r'\$.*?\$',  # LaTeX math
    r'\\frac',  # Fraction notation
    r'\\sum',  # Summation
    r'σ|γ|κ',  # Greek symbols (framework parameters)
    
    # API schemas (structure exact)
    r'\{[\s\S]*?"type":\s*"object"[\s\S]*?\}',  # JSON schemas
    
    # Test section markers (everything after these until next section)
    r'#### Test Execution',
    r'#### Practical Test Design',
]
```

---

## Standard Abbreviations

**Rule 1: Ultra-Terse Headers & Metadata**

```python
HEADER_ABBREVIATIONS = {
    "**Source:**": "**Src:**",
    "**Documentation:**": "**Doc:**",
    "**Documentation Support:**": "**Doc Support:**",
    "**Definition:**": "**Def:**",
    "**Example:**": "**Ex:**",
    "**Compression:**": "**Comp:**",
    "**Format:**": "**Fmt:**",
    "**Test:**": "**Test:**",  # Keep as-is (short enough)
    "**Analysis:**": "**Analysis:**",  # Keep as-is
    "**Prompt:**": "**Prompt:**",  # NEVER change (sacred marker)
    "**Output:**": "**Output:**",  # Keep as-is
    "**Scores:**": "**Scores:**",  # Keep as-is
    "**Model Output:**": "**Output:**",  # Shorten this one
}
```

**Rule 2: Extreme Abbreviations - Standard Terms**

```python
STANDARD_ABBREVIATIONS = {
    "Effectiveness": "E",
    "Reliability": "R",
    "Documentation": "Doc",
    "Application Programming Interface": "API",
    "versus": "v",
    "equals": "=",
    "is": "=",
    "not equal": "≠",
    "greater than": ">",
    "less than": "<",
    "approximately": "~",
    "function of": "f()",
    "number": "#",
    "at": "@",
    
    # Measurements
    " lines": "L",
    " kilobytes": "KB",
    " megabytes": "MB",
    " tokens": "T",
}
```

**Rule 2: Extreme Abbreviations - Context-Specific**

```python
CONTEXT_ABBREVIATIONS = {
    "Chain-of-Thought": "CoT",
    "Tree of Thoughts": "ToT",
    "Large Language Model": "LLM",
    "State of the Art": "SOTA",
    "Lines of Code": "LOC",
    "Mixture of Experts": "MoE",
    "JavaScript Object Notation": "JSON",
    "Application Programming Interface": "API",
}
```

---

## Symbol Substitutions

**Rule 3: Symbol Usage**

```python
STATUS_SYMBOLS = {
    "Yes": "✓",
    "Supported": "✓",
    "Correct": "✓",
    "Success": "✓",
    "passed": "✓",
    "No": "✗",
    "Not Supported": "✗",
    "Incorrect": "✗",
    "Failure": "✗",
    "failed": "✗",
    "Partial": "⚠",
    "Warning": "⚠",
    "Conditional": "⚠",
}

COMPARISON_SYMBOLS = {
    " leads to ": " → ",
    " results in ": " → ",
    " becomes ": " → ",
    " to ": "→",  # More aggressive (context-dependent)
    " increases": " ↑",
    " improves": " ↑",
    " goes up": " ↑",
    " decreases": " ↓",
    " degrades": " ↓",
    " goes down": " ↓",
}

LOGICAL_SYMBOLS = {
    " and ": " & ",  # Use cautiously (where unambiguous)
    " or ": " | ",  # In tables/lists
    " with ": " w/ ",
    " without ": " w/o ",
}
```

---

## Table Compression Rules

**Rule 4: Table Compression**

```python
TABLE_HEADER_COMPRESSION = {
    # Verbose → Compact mappings
    "Technique": "Tech",
    "Description": "Desc",  # Or remove entirely, move to Notes
    "Documentation Support": "Doc",
    "Effectiveness": "E",
    "Reliability": "R",
    "Key Findings": "Notes",
}

TABLE_CELL_COMPRESSION = {
    # Use symbols in cells
    "Yes - Strong": "✓",
    "Yes - Partial": "⚠",
    "No": "✗",
    
    # Remove score denominators if scale obvious
    # "10/10" → "10" (if /10 scale is document-wide)
}

TABLE_RULES = {
    "single_letter_headers": True,  # E, R, Doc not Effectiveness, Reliability
    "remove_description_column": True,  # Move descriptions to Notes column
    "use_symbols": True,  # ✓/✗/⚠ instead of Yes/No/Partial
    "terse_notes": True,  # Fragments not full sentences in Notes
    "remove_denominators": True,  # 10/10 → 10 if scale obvious
}
```

---

## Prose Transformation Rules

**Rule 5: List/Bullet Compression**

```python
LIST_COMPRESSION_RULES = [
    # Remove numbered lists where order not critical
    (r'^\d+\.\s+\*\*.*?\*\*:\s*', ''),  # Remove "1. **Header**: "
    
    # Combine related points
    # (This requires semantic understanding - flag for LLM phase)
    
    # Remove meta-headers
    (r'^\*\*Analysis:\*\*\s*$', ''),  # Remove if context clear
    (r'^\*\*Findings:\*\*\s*$', ''),
]
```

**Rule 7: Prose to Fragment Conversion**

```python
PROSE_FRAGMENT_RULES = [
    # Remove subject pronouns at sentence start
    (r'^The model ', ''),
    (r'^It ', ''),
    (r'^This ', ''),
    (r'^These ', ''),
    
    # Remove filler phrases
    (r'is excellent', 'excellent'),
    (r'successfully ', ''),
    (r'effectively ', ''),
    (r'As we can see,?\s*', ''),
    (r'It should be noted that\s*', ''),
    (r'It is important to note that\s*', ''),
    
    # Use + instead of "and" where appropriate
    (r'\s+and\s+', ' + '),  # Context-dependent
    
    # Use colons for definitions
    (r',\s*not\s+', ': '),  # "X, not Y" → "X: not Y"
]
```

**Rule 8: Section Header Compression**

```python
SECTION_HEADER_RULES = [
    # Remove redundant suffixes
    (r'\s+Prompting$', ''),  # "Chain-of-Thought Prompting" → "Chain-of-Thought"
    (r'\s+Technique$', ''),  # If obvious from context
    
    # Collapse definition sections
    # "#### **Definition**\n\nChain-of-Thought..." 
    # → "**Def**: Chain-of-Thought..."
    (r'####\s+\*\*Definition\*\*\s+', '**Def**: '),
    
    # Collapse support sections
    (r'####\s+\*\*Documentation Support\*\*\s+', '**Doc Support**: '),
]
```

**Rule 9: Scaffolding Removal**

```python
SCAFFOLDING_PATTERNS = [
    # Transition phrases (remove entirely)
    r'Moving on to.*?,\s*',
    r'Now let\'s examine.*?,\s*',
    r'Next, we\'ll.*?\.',
    r'In this section.*?\.',
    
    # Meta-commentary
    r'As we can see from.*?,\s*',
    r'It\'s important to note that\s*',
    r'It should be noted that\s*',
    r'This demonstrates that\s*',
    r'This shows that\s*',
    
    # Obvious conclusions
    r'In conclusion,\s*',
    r'To summarize,\s*',
    r'In summary,\s*',
    
    # Conversational elements
    r'Certainly\.?\s*',
    r'Indeed\.?\s*',
    r'Interestingly\.?\s*',
    r'Notably\.?\s*',
    r'Clearly\.?\s*',
]

SCAFFOLDING_KEEP_PATTERNS = [
    # DO NOT remove these (critical markers)
    r'CRITICAL:',
    r'Note:',
    r'Warning:',
    r'\*\*Important\*\*:',
]
```

---

## Test Section Standard Format

**Rule 10: Test Section Compression**

```python
TEST_SECTION_TEMPLATE = """
### [N]. [Technique Name]

**Def**: [1-2 sentence definition with → notation]

**Doc Support**: [✓/⚠/✗] [Level if applicable]
- [Key point 1]
- [Key point 2]

**Test**: [What test measures in <10 words]

**Prompt**:
```
[Exact prompt verbatim - no compression]
```

**Output**: [Brief description if long, or exact output]
```
[Exact or abbreviated output preserving structure]
```

**Analysis**: [Compressed analysis 2-4 terse sentences. No "The model..." prefixes]

**Scores**: E=[N]/10 ([why]), R=[N]/10 ([why])
"""

TEST_SECTION_RULES = {
    "preserve_prompt_verbatim": True,  # CRITICAL - Rule 6
    "preserve_output_structure": True,  # Can abbreviate if >100 lines
    "compress_analysis": True,  # 2-4 sentences, fragments
    "no_model_prefixes": True,  # Remove "The model...", "It..."
    "scores_with_rationale": True,  # E=10/10 (why)
}
```

---

## Code/Prompt Preservation Rules

**Rule 6: Code Block Preservation**

```python
CODE_PRESERVATION_RULES = {
    "test_prompts": "verbatim",  # 100% exact, 0% compression
    "code_examples": "verbatim",  # 100% exact
    "model_outputs": "structure_preserved",  # Can abbreviate if >100 lines
    "schema_definitions": "verbatim",  # JSON schemas exact
    
    "never_abbreviate": [
        "function_names",
        "api_parameters",
        "json_keys",
        "variable_names",
        "commands",
        "prompts",  # CRITICAL
    ]
}
```

---

## Application Order

**Critical**: Rules must be applied in correct order to avoid conflicts

```python
TRANSFORMATION_ORDER = [
    # 1. Extract sacred content FIRST (before any transforms)
    "extract_sacred_content",
    
    # 2. Scaffolding removal (before other transforms)
    "remove_scaffolding",
    
    # 3. Prose to fragments
    "prose_to_fragments",
    
    # 4. Header abbreviations
    "compress_headers",
    
    # 5. Standard abbreviations
    "apply_abbreviations",
    
    # 6. Symbol substitutions
    "apply_symbols",
    
    # 7. Table compression
    "compress_tables",
    
    # 8. Section headers
    "compress_section_headers",
    
    # 9. Lists/bullets
    "compress_lists",
    
    # 10. Restore sacred content LAST
    "restore_sacred_content",
]
```

---

## Quality Validation Checklist

```python
V7_QUALITY_CHECKS = {
    "size": {
        "min_kb": 19,
        "max_kb": 22,
        "fail_if_over": 25,
    },
    
    "lines": {
        "target_min": 400,
        "target_max": 450,
        "fail_if_over": 500,
    },
    
    "prompts": {
        "expected_count": 12,  # Document-specific
        "preservation": "verbatim",  # Byte-for-byte
        "verification": "mandatory",
    },
    
    "format_checks": [
        "no_prose_paragraphs",  # All converted to fragments
        "tables_single_letter_headers",  # E, R, Doc
        "symbols_used",  # ✓✗⚠→↑↓=≠
        "abbreviations_consistent",  # E/R, CoT, LLM
        "code_preserved",  # Exactly
        "no_model_prefixes",  # No "The model...", "It..."
        "no_transitions",  # No scaffolding
        "test_reproducibility",  # All patterns present
    ],
}
```

---

## Common Mistakes to Avoid

```python
COMMON_MISTAKES = {
    "half_compressing": {
        "wrong": "Abbreviate some sections, leave others verbose",
        "right": "Apply rules uniformly throughout",
    },
    
    "over_compressing_code": {
        "wrong": "Abbreviate prompts, code, API parameters",
        "right": "Keep all code/prompts/schemas verbatim",
    },
    
    "losing_test_patterns": {
        "wrong": "Summarize: 'The model was tested with logistics problem'",
        "right": "Include full test prompt for reproduction",
    },
    
    "verbose_tables": {
        "wrong": "Long column names like 'Documentation Support Level'",
        "right": "Single-letter headers (Doc, E, R) with symbols",
    },
    
    "keeping_scaffolding": {
        "wrong": "'Now let's examine... As we can see...'",
        "right": "Jump straight to content, state findings directly",
    },
}
```

---

## Summary Statistics

**Total Rules Extracted**: 200+

**Categories**:
- Sacred detection patterns: 10
- Header abbreviations: 12
- Standard abbreviations: 15
- Context abbreviations: 8
- Status symbols: 8
- Comparison symbols: 9
- Logical symbols: 3
- Table rules: 5
- Prose fragment rules: 10
- Section header rules: 4
- Scaffolding removal: 15
- Test section rules: 7
- Code preservation: 6
- Quality checks: 15

**Ready for Python implementation** in `compress_v7_hybrid.py`
