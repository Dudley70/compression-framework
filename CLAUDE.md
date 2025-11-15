# CLAUDE.md - AI Assistant Guide

**Last Updated**: 2025-11-15
**Purpose**: Comprehensive guide for AI assistants working on this codebase
**Audience**: Claude, GitHub Copilot, and other AI coding assistants

---

## 🎯 Project Overview

### What This Project Does

This is a **hybrid compression framework for LLM documentation** that combines deterministic safety with LLM intelligence to compress technical documents while guaranteeing critical content preservation.

**Key Achievement**: 77% compression ratio while maintaining 100% byte-for-byte preservation of test prompts, code blocks, and formulas through architectural separation.

### Core Innovation

**Hybrid 4-Step Pipeline**:
```
1. Extract Sacred Content (Python regex)
   ↓ Physically separates prompts/code before LLM sees them
2. LLM Compression (Claude API)
   ↓ Semantic compression on safe-to-compress content
3. Restore + V7 Rules (Python deterministic)
   ↓ Byte-for-byte restoration + abbreviation rules
4. Validation (Python verification)
   ✓ Programmatic verification, no hallucinated success
```

**Why Hybrid?**: Pure autonomous LLM compression failed 5/5 times. Architectural separation physically prevents rule violations.

---

## 📁 Repository Structure

```
compression-framework/
├── compress_v7_hybrid.py          # Main compression tool (761 lines)
├── compress.py                    # Legacy compression tool
├── compress4llm.py                # Alternative compression approach
├── tests/
│   ├── test_compress.py           # Main test suite (675 lines, 35 tests)
│   └── test_*.py                  # Other test suites
├── docs/
│   ├── README.md                  # Framework documentation entry point
│   ├── THEORY.md                  # (σ,γ,κ) unified compression theory
│   ├── VALIDATION.md              # Empirical validation results
│   ├── EXTERNAL_PROJECT_GUIDE.md  # Adoption guide for external projects
│   ├── guides/
│   │   └── INTEGRATION_GUIDE.md   # Complete adoption patterns
│   ├── reference/                 # Reference documentation
│   ├── skills/                    # Claude Code skills
│   ├── templates/                 # Compression templates
│   └── archive/                   # Archived exploration docs
├── scripts/                       # Utility scripts
├── PROJECT.md                     # Project strategic context & decisions
├── SESSION.md                     # Current session status
├── README.md                      # GitHub-facing README
├── CONTRIBUTING.md                # Contribution guidelines
├── QUICKSTART.md                  # Quick reference for compression methods
├── compress_v7_hybrid_spec.md     # Tool architecture specification
├── v7_rules_extraction.md         # V7 transformation rules
└── requirements.txt               # Python dependencies

Key Directories:
- archive/          - Historical artifacts and session handovers
- checkpoints/      - Test checkpoints and validation data
- convergence_results/ - Convergence testing results
- claude-code-tasks/ - Claude Code task specifications
```

---

## 🧠 Core Concepts

### 1. Unified Compression Theory

All compression optimizes three parameters subject to comprehension constraint:

- **σ (Structure)**: Structural density (0=prose → 1=data format)
- **γ (Granularity)**: Semantic detail level (0=keywords → 1=full explanation)
- **κ (Scaffolding)**: Contextual explanation (0=none → 1=complete background)

**Constraint**: σ + γ + κ ≥ C_min(audience, phase)

### 2. Rule 6 Compliance

**Critical Constraint**: Test prompts, code blocks, and formulas must be preserved byte-for-byte (0% compression).

**How We Guarantee It**: Sacred content is extracted BEFORE LLM sees the document, making violations architecturally impossible.

### 3. Compression Versions

| Version | Size | Reduction | Completeness | Use Case |
|---------|------|-----------|--------------|----------|
| V7 ⭐    | 21KB | 84.4% | High (full patterns) | **DEFAULT - Complex work** |
| V5      | 21KB | 84.5% | Medium (results only) | Quick scan |
| V3      | 25KB | 81.4% | High (full patterns) | Human readable |

**Natural Compression Limit**: ~21KB for complete self-contained technical references

### 4. Session-Based Development

Development follows session-based workflow:
- Each session documented in SESSION.md
- Strategic decisions logged in PROJECT.md
- Major milestones tracked with SESSION##_SUMMARY.md files

---

## 🔧 Development Workflow

### Setting Up Development Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests to verify setup
pytest tests/test_compress.py -v

# Should see: 35/35 tests passing
```

### Running the Main Tool

```bash
# Basic usage
python compress_v7_hybrid.py input.md output.md --api-key sk-ant-...

# With all options
python compress_v7_hybrid.py \
  input.md output.md \
  --api-key sk-ant-... \
  --model claude-haiku-4-5 \
  --expected-prompts 10 \
  --report validation.json \
  --verbose
```

### Testing

```bash
# Run all tests
pytest tests/test_compress.py -v

# Run specific test checkpoint
pytest tests/test_compress.py::TestExtractSacredContent -v

# Run with coverage
pytest tests/test_compress.py --cov=compress_v7_hybrid

# Run all test suites
pytest tests/ -v
```

**Test Structure** (35 tests total):
- Checkpoint 1 (12 tests): Sacred content extraction
- Checkpoint 2 (5 tests): Round-trip preservation
- V7 Rules (8 tests): Transformation rules
- Validation (5 tests): Validation logic
- Integration (5 tests): Full pipeline

### Git Workflow

**Branch Naming Convention**:
```bash
# Claude Code sessions use special branch naming:
claude/claude-md-<session-id>-<unique-id>

# Feature branches:
feature/your-feature-name

# Bug fixes:
fix/issue-description
```

**Commit Message Format**:
```bash
feat: add new feature
fix: resolve bug
docs: update documentation
test: add/modify tests
refactor: code refactoring
perf: performance improvements
```

**Important**: When pushing Claude Code branches, always use:
```bash
git push -u origin <branch-name>
```

---

## 📝 Key Development Principles

### From PROJECT.md Core Principles

1. **Pragmatic implementation over theoretical perfection**
2. **Measure before optimizing** - empirical validation first
3. **Simple solutions for 95% of cases**
4. **Evidence-based evaluation** - test assumptions rigorously
5. **Maintain information fidelity** - preserve essential content
6. **Optimize for LLM consumption**, not human aesthetics
7. **Parsimony**: Simplest complete model (3D not 6D)
8. **Safety-first**: Idempotency and information preservation critical
9. **Autonomous execution**: Comprehensive specifications enable quality delegation
10. **Purpose-driven**: Match compression strategy to use case
11. **Empirical iteration**: Optimal balance discovered through testing
12. **Hybrid architecture**: Combine tool safety with LLM intelligence when pure autonomous fails

### Code Style Guidelines

```python
# Use type hints
def extract_sacred_content(document: str) -> dict:
    """
    Extract test prompts, code blocks, formulas.

    Args:
        document: Original markdown content

    Returns:
        Dictionary with sacred_items, modified_document, counts
    """
    pass

# Clear variable names
sacred_items = []
modified_document = content
prompt_count = 0

# Keep functions focused and small
# Add docstrings to all public functions
# Comment complex logic
# Maximum line length: 100 characters
```

---

## 🧪 Testing Philosophy

### TDD Approach

This project was built using Test-Driven Development:

1. **Write tests first** - Define expected behavior
2. **Implement to pass tests** - Build minimal working code
3. **Refactor with confidence** - Tests ensure correctness

### Checkpoint-Based Testing

Tests are organized by checkpoints:

```python
class TestExtractSacredContent:
    """Checkpoint 1: Sacred content extraction."""

class TestRoundTrip:
    """Checkpoint 2: Round-trip preservation."""

class TestV7Rules:
    """Checkpoint 3: V7 transformation rules."""

class TestValidation:
    """Checkpoint 4: Validation logic."""

class TestIntegration:
    """Checkpoint 5: Full pipeline."""
```

### Validation Requirements

All changes must:
- ✅ Pass all 35 existing tests
- ✅ Maintain Rule 6 compliance (100% prompt preservation)
- ✅ Include new tests for new features
- ✅ Preserve byte-for-byte sacred content restoration
- ✅ Use programmatic verification (no hallucinated success)

---

## 📚 Documentation Structure

### Core Documentation Files

**Strategic Context**:
- `PROJECT.md` - Project evolution, decisions, strategic context
- `SESSION.md` - Current session status and blockers

**Framework Documentation** (in `docs/`):
- `docs/README.md` - Framework overview and entry point
- `docs/THEORY.md` - Unified compression theory
- `docs/VALIDATION.md` - Empirical validation results
- `docs/EXTERNAL_PROJECT_GUIDE.md` - Adoption guide

**Quick References**:
- `README.md` - GitHub-facing project overview
- `QUICKSTART.md` - Compression method quick reference
- `CONTRIBUTING.md` - Contribution guidelines

**Specifications**:
- `compress_v7_hybrid_spec.md` - Tool architecture (748 lines)
- `v7_rules_extraction.md` - V7 transformation rules (487 lines)

### Reading Order for New AI Assistants

1. **Start Here**: This file (CLAUDE.md)
2. **Context**: PROJECT.md - Understand project evolution and decisions
3. **Current State**: SESSION.md - What's happening now
4. **Architecture**: compress_v7_hybrid_spec.md - Tool design
5. **Framework**: docs/README.md - Compression framework overview

---

## 🔍 Common Tasks Guide

### Adding a New Feature

```bash
# 1. Create feature branch
git checkout -b feature/your-feature-name

# 2. Write tests first (TDD)
# Add to tests/test_compress.py or create new test file

# 3. Implement feature
# Follow code style guidelines
# Add type hints and docstrings

# 4. Run tests
pytest tests/test_compress.py -v

# 5. Update documentation
# Update README.md if user-facing
# Update CLAUDE.md if affects development
# Add to CHANGELOG.md

# 6. Commit with clear message
git commit -m "feat: add your feature description"

# 7. Push and create PR
git push origin feature/your-feature-name
```

### Fixing a Bug

```bash
# 1. Add failing test that demonstrates bug
def test_bug_reproduction():
    """Test that reproduces the bug."""
    # Test that currently fails

# 2. Fix the bug
# Minimal change to make test pass

# 3. Verify all tests pass
pytest tests/test_compress.py -v

# 4. Commit
git commit -m "fix: resolve bug description"
```

### Updating Documentation

```bash
# User-facing changes → README.md
# Development workflow → CLAUDE.md
# Strategic decisions → PROJECT.md
# Session work → SESSION.md
# Framework docs → docs/*.md

# Commit documentation separately
git commit -m "docs: update documentation for X"
```

### Running Validation on Real Documents

```bash
# Test on real research paper
python compress_v7_hybrid.py \
  path/to/paper.md \
  output.md \
  --api-key $ANTHROPIC_API_KEY \
  --expected-prompts 10 \
  --report validation.json \
  --verbose

# Check validation report
cat validation.json | python -m json.tool
```

---

## ⚠️ Critical Constraints

### 1. Rule 6 Compliance

**MUST preserve byte-for-byte**:
- Test prompts (both code-fenced and prose formats)
- Code blocks
- Mathematical formulas

**How**: Sacred content is extracted BEFORE LLM processing using regex patterns.

### 2. Sacred Content Patterns

```python
# Code-fenced prompts
r'\*\*Prompt:\*\*\s*\n```(.*?)```'

# Prose prompts (no code fence)
r'\*\*Prompt:\*\*\s*\n(?!```)(.*?)(?=\n#{3,}|\*\*(?:Model Output|Output|Prompt):|$)'

# Code blocks
r'```(\w+)?\n(.*?)\n```'

# Formulas
r'\$(.+?)\$'
```

### 3. Idempotency

Compression should be idempotent:
```
compress(document) == compress(compress(document))
```

**Why**: Enables "living document" workflow - compress → add content → recompress.

### 4. Validation is Mandatory

Never trust "success" claims without verification:
- ✅ Use programmatic validation
- ✅ Byte-for-byte comparison for sacred content
- ✅ Count validation for expected prompts
- ❌ Don't trust LLM success metrics (hallucination risk)

---

## 🎓 Key Learnings from Development

### From Session 29 (Tool Implementation)

1. **Claude Code Requires Supervision**
   - Initial build: 21/33 tests passing (36% failure rate)
   - Required 3 iterations to fix bugs
   - Always verify programmatically, never trust "Build Complete ✅"

2. **Validation Discipline Catches All Issues**
   - Caught regex bug (double-extraction)
   - Caught placeholder removal (22/22 deleted)
   - Session 28 principle: "Don't trust claims, verify programmatically"

3. **Strong Prompts for Critical Behavior**
   - Weak prompt → LLM removed all placeholders
   - Strong prompt (⚠️ CRITICAL + 10 lines emphasis) → All preserved
   - When behavior is critical, use EXTREME emphasis

4. **Real Documents ≠ Spec Assumptions**
   - Specs assumed code-fenced prompts
   - Real papers use prose prompts
   - Added dual-format support

### From Session 28 (Architecture Design)

1. **Pure Autonomous LLM Fails for Constrained Tasks**
   - 5 attempts, 100% Rule 6 violation rate
   - LLMs optimize "helpful" over "compliant"
   - Hallucinate success metrics

2. **Architectural Separation Guarantees Safety**
   - Not about better prompts or smarter models
   - System design physically prevents violations
   - Extract sacred → LLM never sees it → restore deterministically

---

## 🚀 Current Status & Next Steps

### Current State (Session 29 Complete)

✅ **Tool Built**: compress_v7_hybrid.py (761 lines)
✅ **Tests Passing**: 35/35
✅ **Rule 6 Compliance**: 100% validated on real documents
✅ **Architecture Proven**: Sacred content separation works
⚠️ **Minor Tuning Needed**: Size 27% over target (acceptable for v1.0)

### Known Issues

**Minor (Acceptable for v1.0)**:
- Size 30.5KB vs 19-24KB target (+27%)
- Structure validation false positives

**Medium Priority**:
- Model name validation
- Better progress reporting
- Batch processing support

**Low Priority**:
- Output format options (JSON, HTML)
- Configuration files
- Undo compression

### Next Session Focus

**Session 30: GitHub Migration + Tuning**

Ready for:
1. ✅ Initialize GitHub repository (done)
2. ✅ Create README.md, CONTRIBUTING.md (done)
3. ✅ Set up .gitignore, requirements.txt (done)
4. ⏳ Open issues for size/structure tuning
5. ⏳ Optional: CI/CD with GitHub Actions

---

## 💡 Tips for AI Assistants

### When Starting a New Session

1. **Read SESSION.md first** - Understand current state
2. **Check PROJECT.md Decision Log** - See recent decisions
3. **Review blockers** - Any outstanding issues?
4. **Run tests** - Verify environment setup

### When Making Changes

1. **Write tests first** (TDD approach)
2. **Run tests frequently** during development
3. **Update documentation** alongside code
4. **Verify sacred content preservation** for any compression changes
5. **Use programmatic validation** - never trust claims

### When Debugging

1. **Check test output** - What specific assertion failed?
2. **Review validation reports** - Check validation.json
3. **Verify regex patterns** - Sacred content extraction correct?
4. **Test on real documents** - Not just synthetic test cases

### When Adding Features

1. **Check PROJECT.md principles** - Align with project philosophy
2. **Consider Rule 6 compliance** - Will this affect sacred content?
3. **Write comprehensive tests** - Cover edge cases
4. **Update CLAUDE.md** - Help future AI assistants

---

## 📊 Metrics & Performance

### Tool Performance

**Per Document (130KB example)**:
- Haiku 4.5: ~$0.05, ~20-30s
- Sonnet 4.5: ~$0.16, ~25-35s

**Compression Ratio**: 77% (130.9KB → 30.5KB)

**Rule 6 Compliance**: 100% (validated on multiple documents)

### Test Coverage

- 35 tests across 5 checkpoints
- Coverage: Core extraction, transformation, validation, integration
- All tests must pass for any PR

### Convergence Properties

- **Convergence Rate**: 96.7% (documents self-stabilize)
- **Average Rounds**: 1.0 (typically converges first try)
- **Idempotent Behavior**: compress(compress(x)) == compress(x)

---

## 🔗 External References

### API Documentation
- [Anthropic API Docs](https://docs.anthropic.com)
- [Claude Models Overview](https://docs.anthropic.com/en/docs/about-claude/models/overview)

### Related Projects
- CC_Projects framework (H1/H2/H3 organization)
- Gemini Research (example validation documents)

### Academic Foundation
- Information theory (Shannon entropy)
- Cognitive science (comprehension constraints)
- Software engineering (documentation patterns)

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

**Quick Summary**:
1. Fork repository
2. Create feature branch
3. Write tests
4. Implement feature
5. Run all tests
6. Update documentation
7. Submit PR with clear description

---

## 📞 Getting Help

**For AI Assistants**:
- Read this file (CLAUDE.md)
- Check SESSION.md for current context
- Review PROJECT.md for strategic decisions
- Examine test files for usage examples

**For Humans**:
- Open GitHub issue for bugs/features
- Check existing issues first
- Include reproduction steps and test results

---

## 📜 License

[Add license information]

---

**Last Updated**: 2025-11-15
**Maintained By**: Compression Framework Project
**Version**: 1.0

---

## Appendix: Decision Log Summary

### Recent Major Decisions

**Decision #14 (2025-11-16)**: Tool Implementation Complete
- Session 29 implemented compress_v7_hybrid.py
- Rule 6 compliance validated (100% on real documents)
- Architecture proven through separation of concerns

**Decision #13 (2025-11-15)**: Hybrid Architecture for V7 Tool
- Abandoned pure autonomous LLM after 5 failed attempts
- Adopted hybrid: deterministic extraction + LLM compression + deterministic restoration
- Physical separation prevents Rule 6 violations

**Decision #12 (2025-11-14)**: V5 as Default LLM-Optimized Method
- V5 (65-70% reduction) for complex technical references
- V4 for simple lookups only
- Natural compression limit discovered: ~21KB

**Decision #11 (2025-11-01)**: Intrinsic Stability Validated
- 96.7% convergence rate
- Idempotent behavior confirmed
- "Living document" workflow validated

See PROJECT.md for complete decision history.

---

**End of CLAUDE.md**
