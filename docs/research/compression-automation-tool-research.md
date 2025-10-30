# Compression Automation Tool Research

**Created**: 2025-10-30  
**Purpose**: Research findings for building intelligent document compression automation tool  
**Status**: Research complete, implementation pending

---

## Executive Summary

Research into building a Python-based intelligent document compression automation tool that can be wrapped as a Claude Code skill. Key findings:

**Document Classification**: 95% accuracy achievable with modern models (LayoutLM, spaCy TextCategorizer)
**Text Transformation**: Hybrid approach (extractive + abstractive) outperforms pure methods
**Validation**: Multi-metric framework required (BERTScore + ROUGE + entity preservation + semantic similarity)
**Automation**: Three-tier approach (manual/semi/full) with confidence-based routing
**Claude Code Integration**: Progressive disclosure skill architecture with sub-30 token discovery

---

## Document Classification & Analysis

### Production-Ready Solutions

**Hugging Face LayoutLM family**: 95% accuracy on document classification benchmarks by combining text and visual layout understanding.

**mrkdwn_analysis**: Zero-configuration element extraction identifying headers, code blocks, tables, lists with rule-based precision.

**spaCy TextCategorizer**: Best balance for production deployment—90%+ F1 scores with minimal computational overhead.

**Zero-shot classification with BART**: Immediate results without training data for purpose detection (execution vs reference vs audit).

**Fine-tuned BERT models**: 95% accuracy on domain-specific corpora.

### Recommended Technical Stack

**markdown-it-py**: CommonMark-compliant parsing with token stream access. Google Assured Open Source Software member with 100% CommonMark compliance, plugin architecture, AST-based transformations.

**Sentence Transformers**: Semantic embeddings (all-MiniLM-L6-v2 provides 384-dimensional representations in milliseconds).

**deepdoctection**: Comprehensive document AI pipelines for PDFs or scanned content.

**LlamaIndex MarkdownNodeParser**: Splits documents while preserving hierarchy in metadata, extracting tables and code blocks as separate nodes.

### Custom Classifier Opportunity

No existing specialized tools for lifecycle phase detection. Training data could be generated from:
- Documentation repositories labeled by folder structure (draft/, review/, published/, archived/)
- Git commit metadata

---

## Text Transformation Methods

### Gold Standard Models

**BART (facebook/bart-large-cnn)**: Gold standard for technical document summarization
- ROUGE-L scores: 0.365
- Semantic similarity preservation: 82-89%
- Best for abstractive summarization

**LexRank/LSA**: Extractive methods
- 100% factual accuracy (selects original sentences verbatim)
- Lower compression ratios than abstractive
- No hallucination risk

### Hybrid Approach (Recommended)

**Two-stage pipeline outperforms pure methods**:
1. Extractive selection identifies key content (fast, accurate)
2. Abstractive refinement on selected content (improved fluency, higher compression)

**Benefits**:
- 60% reduction in hallucination risk vs pure abstractive
- Compression ratios: 30-50%
- Maintains accuracy while improving readability

### Markdown Manipulation

**markdown-it-py advantages**:
- Parser/renderer separation allows intercepting token stream
- Apply transformation logic
- Regenerate properly formatted markdown

**AST-based transformation approach**:
1. Parse with markdown-it-py to tokens
2. Identify important nodes (preserve all code blocks, keep H1-H2 headers, rank paragraphs by semantic importance)
3. Prune low-importance subtrees
4. Regenerate

Maintains grammaticality and formatting that pure text-based approaches lose.

---

## Validation Framework

### Multi-Metric Evaluation Pipeline

**Primary: BERTScore F1** using microsoft/deberta-xlarge-mnli
- Threshold: ≥0.85 for automated approval
- 0.93 correlation with human judgments (vs 0.70 for BLEU)
- Captures semantic preservation at token level with contextualized embeddings

**Secondary: ROUGE-L** measuring longest common subsequence
- Threshold: ≥0.70
- Validates structural preservation and content overlap
- Fast to compute, widely understood benchmark

**Tertiary: Entity Preservation** using spaCy NER
- Threshold: ≥0.80 preservation rate
- Critical for technical content (API names, function names, version numbers, dates)
- Track by entity type: PERSON, ORG, GPE, DATE, CARDINAL

**Quality: Semantic Similarity** using Sentence Transformers
- Model: all-mpnet-base-v2 for highest quality
- Threshold: ≥0.75
- Validates overall meaning preservation at document level

### Sentence Transformers Performance

**all-MiniLM-L6-v2**: 
- Processes documents 13,000x faster than BERT
- 0.93 correlation with human judgments
- Recommended threshold: 0.75+ semantic similarity

**pyAutoSummarizer**: All-in-one solution with extractive (TextRank, LexRank, LSA) and abstractive (BART, T5, PEGASUS) algorithms plus built-in evaluation metrics.

---

## Claude Code Skills Architecture

### Progressive Disclosure Pattern

**Skills launched October 2025**: Breakthrough design
- Only 30-50 tokens consumed until Claude determines relevance
- Then full content loads
- Unbounded context can be packaged without bloating context window

### Three-Tier Skill Architecture

**Tier 1 - Discovery** (always loaded):
```yaml
---
name: doc-compressor
description: Compress technical documentation while preserving meaning. Use when reducing token count, optimizing for LLMs, or creating executive summaries. Works with markdown, analyzes document type/purpose/lifecycle, calculates optimal compression parameters.
allowed-tools: Read, Write, Grep, Bash
---
```

**Tier 2 - Core instructions** (loaded when triggered):
- Step-by-step compression workflow
- Quality thresholds (BERTScore F1 ≥ 0.85, entity preservation ≥ 0.80)
- Parameter explanations (σ, γ, κ)
- Example transformations showing before/after

**Tier 3 - Reference materials** (loaded on demand):
- reference.md: Detailed algorithm explanations
- examples.md: Extensive before/after samples
- scripts/compressor.py: Pre-written compression logic
- templates/: Output format templates

---

## Automation Levels

### Three-Tier Automation Architecture

**Manual Mode** (Human-in-the-loop):
- Skill analyzes document and suggests compression parameters
- Displays preview with side-by-side original/compressed view
- User reviews, adjusts parameters (sliders for σ, γ, κ)
- All decisions require explicit user action
- Confidence display with color coding: green (>85%), yellow (70-85%), red (<70%)

**Semi-Automated Mode** (Confidence-based routing):
- Automatically compresses documents with confidence >90%
- Medium confidence (75-90%) queued for batch review with proposed changes highlighted
- Low confidence (<75%) flagged for manual handling
- Checkpoint pattern pauses at critical workflow stages

**Full Automation** (Monitoring with escalation):
- Executes end-to-end for high-confidence documents
- Real-time dashboard: documents processed, average confidence, compression ratios, quality metrics
- Automatic escalation triggers:
  - Confidence drops below 75%
  - Entity preservation < 80%
  - Semantic similarity < 0.75
  - Repeated errors in document type
- Circuit breaker auto-pauses after error threshold

### Confidence Scoring (Spotify 2024 Research)

**Majority voting with 5-7 models provides most reliable confidence scores**:
- Run 3-5 compression variations (different algorithms, parameters)
- Measure agreement percentage
- 80% agreement = 80% confidence
- Apply Platt scaling to calibrate scores with actual quality metrics

---

## Token Counting & Measurement

### Token Counting Tools

**tiktoken** (OpenAI official):
- Rust-backed speed for GPT models
- Encodings: gpt-4o (o200k_base), gpt-4/gpt-3.5-turbo (cl100k_base)

**tokencost**: Multi-model support
- Counts tokens across 400+ LLMs (Claude, Gemini, LLaMA, Mistral)
- Includes cost calculation

**For Claude specifically**:
- Claude 3+ uses Anthropic's beta token counting API
- Older models approximate with tiktoken cl100k_base
- Rule of thumb: ~3.5 characters per token

**LiteLLM**: Unified interface for production
- Auto-detects model-specific tokenizers
- Best for multi-model compression tools

### Compression Ratio Metrics

Report multiple metrics:
1. Token-based ratio (original_tokens / compressed_tokens)
2. Space savings percentage ((original - compressed) / original × 100)
3. Efficiency score combining compression ratio, semantic preservation, and processing speed

---

## Python Library Stack

### Core Libraries

**Document Analysis**:
- `markdown-it-py`: Parsing and token stream manipulation
- `mrkdwn_analysis`: Structural element extraction
- `spacy`: NER and linguistic analysis
- `transformers`: Zero-shot classification

**Text Transformation**:
- `transformers` (BART/T5): Abstractive summarization
- `sumy` (LexRank/LSA): Extractive selection
- `sentence-transformers`: Semantic embeddings

**Validation**:
- `bert-score`: BERTScore calculation
- `rouge-score`: ROUGE metrics
- `sentence-transformers`: Semantic similarity

**Token Counting**:
- `tiktoken`: OpenAI models
- `tokencost`: Multi-model support

### Installation

```bash
pip install transformers sentence-transformers \
    markdown-it-py spacy tiktoken \
    bert-score rouge-score sumy
    
python -m spacy download en_core_web_sm
```

---

## Existing Tools & Market Gaps

### Documentation Linters

**Vale**: 10k+ GitHub stars, used by GitHub, Microsoft, Google, Red Hat
- Extensible YAML-based rule architecture
- Flags issues but doesn't transform content
- Demonstrates how to codify writing standards

**Acrolinx**: Enterprise AI-powered content governance
- Style guide enforcement
- Terminology management
- Real-time content scoring
- Shows market for intelligent documentation tools

### Critical Gap Identified

**No existing tools perform semantic compression specifically for technical documentation**.

General summarization tools (Sumy, BART) lack:
- Exact reproduction of code snippets and commands
- Preservation of version numbers, API names, technical terms
- Maintaining prerequisite chains and dependency information
- Keeping warnings and safety-critical information
- Understanding documentation structure (tutorials vs reference vs how-to)

### Opportunity

Build domain-specific compression that:
- Understands technical documentation schemas (DITA, DocBook)
- Detects and preserves code blocks
- Validates technical terminology preservation
- Implements structure-aware compression
- Includes domain-specific quality metrics

---

## Implementation Recommendations

### Phased Approach

**Phase 1 (Weeks 1-2)**: Document classification
- Build using spaCy + zero-shot classification
- Establish evaluation framework
- Collect representative documents

**Phase 2 (Weeks 3-4)**: Basic extractive compression
- Implement LexRank/LSA
- Set baseline compression ratios

**Phase 3 (Weeks 5-6)**: Validation pipeline
- Add BERTScore + Sentence Transformers
- Entity preservation tracking

**Phase 4 (Weeks 7-8)**: Abstractive refinement
- Integrate BART for hybrid approach
- Tune compression parameters

**Phase 5 (Weeks 9-10)**: Claude Code skill (manual mode)
- Package as skill with progressive disclosure
- Manual review workflow

**Phase 6 (Weeks 11-12)**: Automation
- Add semi-auto and full-auto modes
- Confidence-based routing

### Technical Debt to Avoid

1. **Don't over-engineer automation initially** - Start with manual mode, validate quality, then add automation
2. **Don't skip entity preservation tracking** - Catches most quality issues in technical content
3. **Don't use single metric for validation** - False confidence from high ROUGE but low semantic similarity is common
4. **Don't forget audit trails** - Log all compressions, parameters, quality scores

### Hardware Requirements

**Development/Testing**:
- 8-core CPU
- 16GB RAM
- No GPU required for extractive methods

**Production with BART/T5**:
- NVIDIA T4+ GPU with 6GB+ VRAM
- 32GB system RAM
- Fast SSD for model caching

**Alternative**:
- 8-bit quantization (50% memory reduction)
- Distilled models (30x fewer parameters, 90%+ performance)

---

## Key Research Sources

**Document Classification**:
- Hugging Face Document AI (2024)
- spaCy TextCategorizer production implementations
- mrkdwn_analysis library

**Text Transformation**:
- BART/T5/PEGASUS transformer models
- Hybrid extractive-abstractive approaches (ACL 2019)
- pyAutoSummarizer comprehensive library

**Validation Metrics**:
- BERTScore paper and implementations
- Sentence Transformers documentation
- ROUGE and BLEU evaluation frameworks

**Claude Code Skills**:
- Anthropic Skills documentation (Oct 2025)
- Progressive disclosure patterns
- Best practices guide

**Human-in-the-Loop**:
- LangGraph HITL patterns (2025)
- Stanford HAI interactive AI systems research (2024)
- Spotify confidence scoring methodology (2024)

**Automation Maturity**:
- MIT CISR AI Maturity Model (2024)
- Carbon Design System AI patterns
- Enterprise automation case studies

---

## Next Steps

### Immediate Actions

1. **Establish evaluation framework**:
   - Collect representative documents
   - Define gold standard compressions
   - Measure baseline: existing tools performance

2. **Set quality thresholds**:
   - BERTScore: ≥0.85
   - ROUGE-L: ≥0.70
   - Entity preservation: ≥0.80
   - Semantic similarity: ≥0.75

3. **Prototype core compression**:
   - Start with extractive (LexRank)
   - Add basic validation
   - Test on sample corpus

### Integration with Compression Framework

This tool would complement our theoretical framework:
- **Framework provides** (σ, γ, κ) parameter targets
- **Tool implements** actual compression transformations
- **Validation ensures** framework predictions match results
- **Feedback loop** refines framework based on empirical data

---

**Document Status**: Research complete  
**Last Updated**: 2025-10-30  
**Next Phase**: Prototype implementation planning  
**Reference**: Extended research artifact from Session 7
