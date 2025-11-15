# LLM Documentation Compression Framework

Hybrid compression tool that guarantees test prompt preservation (Rule 6 compliance) through architectural separation of sacred content from LLM processing.

[![Tests](https://img.shields.io/badge/tests-35%2F35%20passing-brightgreen)]()
[![Rule 6](https://img.shields.io/badge/Rule%206-100%25%20compliant-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.9+-blue)]()

---

## 🎯 What It Does

Compresses technical documents (research papers, documentation) while **guaranteeing** that test prompts, code blocks, and formulas are preserved byte-for-byte.

**Example:**
- Input: 130.9KB research paper with 11 test prompts
- Output: 30.5KB (77% reduction) with all 11 prompts preserved exactly

**Key Innovation:** Sacred content is physically separated from LLM processing, making Rule 6 violations architecturally impossible.

---

## ⚡ Quick Start

### Installation

```bash
pip install anthropic pytest
```

### Basic Usage

```bash
python compress_v7_hybrid.py \
  input.md \
  output.md \
  --api-key sk-ant-...
```

### With Options

```bash
python compress_v7_hybrid.py \
  paper.md \
  compressed.md \
  --api-key sk-ant-... \
  --model claude-haiku-4-5 \
  --expected-prompts 10 \
  --report validation.json \
  --verbose
```

---

## 🏗️ Architecture

**4-Step Hybrid Pipeline:**

```
Step 1: Extract Sacred Content (Python regex)
  ↓ Finds: Test prompts, code blocks, formulas
  ↓ Replaces with: {{SACRED_TEST_PROMPT_0}}, etc.
  
Step 2: LLM Compression (Claude API)
  ↓ Compresses non-sacred content
  ↓ Placeholders preserved (verified programmatically)
  
Step 3: Restore + V7 Rules (Python deterministic)
  ↓ Sacred content restored byte-for-byte
  ↓ V7 abbreviations/symbols applied
  
Step 4: Validation (Python verification)
  ✓ Rule 6 compliance checked programmatically
  ✓ Size, structure, prompt preservation verified
```

**Why Hybrid?**  
Pure autonomous LLM compression failed 5/5 times (removed prompts, violated constraints, hallucinated success). Hybrid architecture physically separates sacred content before LLM sees it - architectural guarantee, not prompt engineering.

---

## ✅ Features

- **Guaranteed Rule 6 Compliance** - Sacred content extraction prevents violations
- **Dual Format Support** - Handles both code-fenced and prose prompts
- **Model Selection** - Choose Sonnet 4.5 (~$0.16/doc) or Haiku 4.5 (~$0.05/doc)
- **Streaming** - Handles long documents without timeout
- **Programmatic Validation** - No hallucinated success metrics
- **Comprehensive Tests** - 35/35 tests passing

---

## 📊 Validation Results

Tested on **Gemini Prompting Capability Self-Assessment** (real research paper):

| Metric | Result | Status |
|--------|--------|--------|
| Original Size | 130.9KB | - |
| Final Size | 30.5KB | ⚠️ +27% over 19-24KB target |
| Compression Ratio | 77% | ✅ |
| Rule 6 Compliance | 100% | ✅ |
| Prompts Found | 11/11 | ✅ |
| Prompts Preserved | 11/11 byte-for-byte | ✅ |
| Placeholders Through LLM | 22/22 | ✅ |

**Bottom Line:** Architecture works. Minor size tuning needed.

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/test_compress.py -v

# Run specific checkpoint
pytest tests/test_compress.py::TestExtractSacredContent -v

# With coverage
pytest tests/test_compress.py --cov=compress_v7_hybrid
```

**Test Coverage:**
- Checkpoint 1 (12 tests): Sacred extraction
- Checkpoint 2 (5 tests): Round-trip preservation
- V7 Rules (8 tests): Transformation rules
- Validation (5 tests): Validation logic
- Integration (5 tests): Full pipeline

---

## 💰 Cost

**With $1000 Anthropic Credit:**
- Haiku 4.5: ~20,000 documents
- Sonnet 4.5: ~6,250 documents

**Per Document (130KB example):**
- Haiku 4.5: $0.05
- Sonnet 4.5: $0.16

---

## 📖 Documentation

- **[SESSION29_SUMMARY.md](SESSION29_SUMMARY.md)** - Complete build record
- **[compress_v7_hybrid_spec.md](compress_v7_hybrid_spec.md)** - Architecture specification
- **[v7_rules_extraction.md](v7_rules_extraction.md)** - Transformation rules
- **[SESSION.md](SESSION.md)** - Current project status

---

## 🛠️ Development

### Project Structure

```
compression-framework/
├── compress_v7_hybrid.py      # Main tool (693 lines)
├── tests/
│   └── test_compress.py       # Test suite (612 lines)
├── docs/                      # Documentation
├── SESSION29_SUMMARY.md       # Session 29 record
├── README.md                  # This file
└── requirements.txt           # Dependencies
```

### Requirements

- Python 3.9+
- anthropic
- pytest

---

## 🐛 Known Issues

### Minor (v1.0 acceptable)
- **Size 27% over target** - Output 30.5KB vs 19-24KB target
  - Impact: Low - still 77% compression
  - Fix: Tune V7 abbreviation rules
  
- **Structure validation false positives**
  - Impact: Low - prompts still preserved
  - Fix: Update validation regex patterns

### Future Enhancements
- Batch processing
- Configuration files
- Additional output formats (JSON, HTML)
- Undo compression

---

## 📝 License

[Add your license here]

---

## 🙏 Acknowledgments

**Session 28** (2025-11-15):
- Analyzed 5 failed autonomous attempts
- Designed hybrid architecture
- Created 3,179 lines of specifications

**Session 29** (2025-11-16):
- Implemented tool with Claude Code
- Validated architecture on real documents
- Proved Rule 6 compliance guarantees

**Key Insight:** Architectural separation of sacred content from LLM processing is the critical innovation. Not about better prompts or smarter models - about system design that physically prevents violations.

---

## 🔗 Links

- [Anthropic API Documentation](https://docs.anthropic.com)
- [Claude Models](https://docs.anthropic.com/en/docs/about-claude/models/overview)
- [Project Documentation](docs/)

---

**Status:** Production-ready with minor tuning needed. Rule 6 compliance validated.
