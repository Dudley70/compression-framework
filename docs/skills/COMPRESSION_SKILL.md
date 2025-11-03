# Claude Compression Skill Specification

**Version**: 1.0  
**Date**: 2025-11-03  
**Status**: Ready for Implementation  
**Phase**: Phase 2C - Proactive System Implementation

---

## 1. Skill Overview

### Purpose

Read compression parameters (σ, γ, κ) from document frontmatter and maintain compressed writing style throughout document creation and editing. Enable users to write naturally in compressed form without requiring post-processing.

### Scope

- **Document Creation**: Parse frontmatter and apply compression parameters to new content
- **Document Editing**: Preserve compression level during edits, maintain consistency
- **Parameter Adjustment**: Support runtime changes to compression parameters
- **Constraint Validation**: Ensure σ + γ + κ ≥ C_min(audience, phase)
- **Integration**: Works seamlessly with 8-template library

### Integration Points

- **Input**: Document frontmatter with YAML compression metadata
- **Processing**: Parameter interpretation and LSC technique selection
- **Output**: Content naturally compressed according to parameters
- **Feedback**: Optional constraint violation warnings and adjustment suggestions

---

## 2. Behavior Rules

### On Document Creation

**Sequence**:
1. Detect document with compression frontmatter (YAML header)
2. Parse compression parameters from metadata:
   - `σ` (sigma): Structure density
   - `γ` (gamma): Granularity/detail level
   - `κ` (kappa): Scaffolding/contextual explanation
3. Extract metadata fields:
   - `audience`: LLM | human | dual
   - `tier`: T1 (essential) | T2 (valuable) | T3 (enrichment)
   - `phase`: active | complete | archived
4. Validate parameter ranges (0.0-1.0 each)
5. Calculate C_min(audience, phase):
   - LLM audience: C_min = 0.7
   - Human audience: C_min = 1.2
   - Dual audience: C_min = 1.0
   - Active phase: base value
   - Complete phase: +0.1
   - Archived phase: +0.2
6. Verify constraint: σ + γ + κ ≥ C_min
   - If violated: Flag warning and suggest adjustments
   - If satisfied: Proceed with content generation
7. Select LSC techniques matching parameter interpretation
8. Generate content following target compression style
9. Maintain compression consistency throughout creation

**Implementation Notes**:
- Extract frontmatter automatically when document contains YAML header
- Provide feedback on constraint satisfaction
- Apply appropriate techniques naturally (not forcing compression)
- Guide user toward aligned parameters through style recommendations

### During Editing

**Sequence**:
1. Detect existing document with compression frontmatter
2. Read parameters from frontmatter (don't change without explicit user action)
3. On each edit/addition:
   - Apply same parameters to new content
   - Preserve already-compressed sections (idempotent)
   - Maintain consistency with document structure
4. Monitor for style drift:
   - Flag if new content doesn't match parameter style
   - Suggest structural improvements if needed
5. Support parameter changes:
   - If user updates (σ, γ, κ), adapt approach for subsequent edits
   - Keep historical parameters for reference
   - Don't recompress existing content (user chooses)

**Idempotency Guarantee**:
- Already-compressed text remains unchanged when skill is applied again
- Mixed compression states handled automatically:
  - Compressed sections: Skipped (already at target)
  - Uncompressed sections: Compressed to target level
- No special state tracking needed (intrinsic behavior)

**Error Handling**:
- Missing frontmatter: Use defaults or ask user for parameters
- Invalid parameters: Graceful degradation or request correction
- Constraint violation: Warn and suggest adjustment
- Ambiguous parameters: Request clarification or provide best-guess

### Parameter Interpretation Rules

The skill must interpret (σ, γ, κ) to determine:
1. **What format to use** (controlled by σ)
2. **How much detail to include** (controlled by γ)
3. **How much context to provide** (controlled by κ)

**Interpretation Logic**:

```
IF σ ≥ 0.7 THEN
  // High structure: Use tables, lists, hierarchical layout
  Format := structured
  Prose_Percentage := 10-20%
  Techniques := [structured_lists, hierarchical_structure, table_format, abbreviations]
ELSE IF σ ≥ 0.4 THEN
  // Medium structure: Mix prose and structure
  Format := mixed
  Prose_Percentage := 40-60%
  Techniques := [selective_lists, selective_tables, concise_prose]
ELSE
  // Low structure: Prose-dominant with compression
  Format := prose
  Prose_Percentage := 70-90%
  Techniques := [active_voice, concise_sentences, logical_flow]

IF γ < 0.4 THEN
  // Low granularity: Keywords, abbreviations, minimal detail
  Detail_Level := minimal
  Techniques += [abbreviations, omit_obvious_details, maximum_density]
  Assumption := reader_fills_obvious_gaps
ELSE IF γ < 0.7 THEN
  // Medium granularity: Concise facts, key information
  Detail_Level := moderate
  Assumption := reader_has_domain_knowledge
ELSE
  // High granularity: Complete sentences, full detail
  Detail_Level := complete
  Techniques += [complete_sentences, full_context, detailed_explanations]
  Assumption := reader_may_be_unfamiliar

IF κ < 0.3 THEN
  // Minimal scaffolding: No context, assume expertise
  Context := none
  Headers := minimal_or_none
  Explanation := none
  Rationale := implicit
ELSE IF κ < 0.6 THEN
  // Moderate scaffolding: Basic headers, brief context
  Context := brief
  Headers := standard_headers
  Explanation := when_needed
  Rationale := high_level
ELSE
  // Full scaffolding: Complete context, full explanation
  Context := complete
  Headers := hierarchical_descriptive
  Explanation := for_all_sections
  Rationale := explicit_and_detailed
```

---

## 3. LSC Technique Mapping

### Technique Selection Algorithm

The skill uses the following algorithm to select which LSC techniques to apply based on (σ, γ, κ) parameters:

**Input**: (σ, γ, κ) parameters
**Output**: Ordered list of LSC techniques to apply

#### High Structure (σ ≥ 0.7)

**Primary Techniques**:
1. **Structured Lists** - Convert prose to bullets with strong hierarchy
   - Format: `- [x] Item - outcome/metric`
   - Use for: Achievements, tasks, metrics, decisions
   - Compression: 60-70% vs prose
   - Applied when: σ ≥ 0.7 AND content is enumerable

2. **Hierarchical Structure** - Organize with numbered/nested headers
   - Format: `## Section | ### Subsection | #### Sub-subsection`
   - Use for: Multi-level organization, taxonomy, decision trees
   - Compression: 30-40% vs flat structure
   - Applied when: σ ≥ 0.8 AND multiple sections present

3. **Table Format** - Encode data in markdown tables
   - Format: `| Key | Value | Status |` (3-5 columns max)
   - Use for: Comparisons, metrics, status tracking
   - Compression: 40-50% vs descriptive prose
   - Applied when: σ ≥ 0.7 AND data is tabular

4. **Abbreviations** - Use standard abbreviations and acronyms
   - Definitions: Establish once, use consistently
   - Common: ETA, QA, impl, auth, viz, async, sync
   - Compression: 20-30% token savings
   - Applied when: σ ≥ 0.7 AND abbreviation is established

#### Medium Structure (0.4 ≤ σ < 0.7)

**Mixed Techniques**:
1. **Selective Lists** - Use lists only for key items
   - Format: Single bullets with 1-2 key facts
   - Applied when: Some enumeration but maintaining prose context
   - Compression: 30-40% vs full prose

2. **Key-Value Format** - Short paragraphs as fact statements
   - Format: `Topic: Detail` or `Fact: Context`
   - Applied when: Multiple related facts, need organization

3. **Concise Prose** - Apply compression to prose paragraphs
   - Techniques: Remove adverbs, active voice, short sentences
   - Average sentence length: 12-15 words vs 18-22 for normal prose
   - Compression: 20-30% vs verbose prose

#### Low Structure (σ < 0.4)

**Prose Techniques**:
1. **Active Voice** - Use active voice exclusively
   - Format: Subject-Verb-Object structure
   - Example: "We chose X because..." not "X was chosen for..."
   - Compression: 15-20% vs passive voice

2. **Concise Sentences** - Short, direct sentences
   - Target length: 12-15 words average
   - One idea per sentence
   - Compression: 20-25% vs long-winded prose

3. **Logical Flow** - Strong paragraph coherence
   - Use transitions: However, Therefore, Next, Finally
   - Topic sentence per paragraph
   - Compression: 10-15% vs rambling prose

### Technique Application Rules

**Rule 1: Structure density determines format**
```
σ ≥ 0.7 → prioritize_tables_and_lists
0.4 ≤ σ < 0.7 → mix_prose_and_structure
σ < 0.4 → compress_prose_directly
```

**Rule 2: Detail controls inclusion**
```
γ < 0.4 → omit_obvious_details, use_abbreviations
0.4 ≤ γ < 0.7 → include_essential_facts_only
γ ≥ 0.7 → complete_sentences, full_context
```

**Rule 3: Scaffolding determines explanation**
```
κ < 0.3 → minimal_headers, no_explanations
0.3 ≤ κ < 0.6 → standard_headers, brief_context
κ ≥ 0.6 → hierarchical_headers, full_explanations
```

**Rule 4: Combine techniques**
```
Apply techniques in order of effectiveness:
1. Highest impact first (structure if σ high)
2. Detail-level compression second (abbreviations if γ low)
3. Scaffolding optimization last (header reduction if κ low)

Example combination (σ=0.8, γ=0.4, κ=0.2):
→ Apply: structured_lists + abbreviations + minimal_headers
→ Result: Table format with abbreviations and no context paragraphs
```

### Technique Examples

**Example 1: High Compression (σ=0.8, γ=0.4, κ=0.2)**

Techniques Applied: structured_lists, hierarchical_structure, table_format, abbreviations, minimal_headers

Result Style:
```markdown
# Status - 2025-11-03

## Accomplished
- [x] Phase 1 complete (4,360 lines, 96.7% convergence)
- [x] Spec delivered (TASK-2C ready)
- [x] Validation complete (23/43 tests passing)

## In Progress  
- [ ] Skill implementation (0/6 techniques)
- [ ] Template library (5/8 complete)

## Blockers
- None

## Metrics
| Item | Target | Current | Status |
|------|--------|---------|--------|
| Specs | 8 | 4 | 50% |
| Lines | 20K | 15.3K | 77% |
| Tests | 50 | 23 | 46% |
```

**Example 2: Medium Compression (σ=0.6, γ=0.6, κ=0.4)**

Techniques Applied: selective_lists, key_value_format, concise_prose, standard_headers

Result Style:
```markdown
# Architecture Decision: Database Approach

## Problem
The system needs efficient data access patterns. Current approach (SQL-only) 
limits query flexibility and increases latency for complex joins.

## Decision
Implement hybrid architecture: SQL for transactional data, document store for 
flexible queries. Rationale:

- **Flexibility**: Document store handles 10+ query patterns vs SQL's 3
- **Performance**: Reduces join complexity from O(n²) to O(n)
- **Complexity**: Hybrid manageable with clear ownership (team expertise in both)

## Tradeoffs
Trade increased complexity against significant performance gains. Data consistency 
handled through event sourcing. Team familiar with both technologies.

## Validation
- Query performance benchmarked (target: <50ms p95)
- Data consistency tested (ACID properties verified)
- Migration path documented (existing data → hybrid schema)
```

**Example 3: Low Compression (σ=0.3, γ=0.8, κ=0.7)**

Techniques Applied: active_voice, concise_sentences, logical_flow, full_headers

Result Style:
```markdown
# Strategic Context: Why We're Building This

## The Challenge We Face

The team needs to compress documentation while maintaining comprehension. 
Traditional approaches reduce readability. We wanted a solution that lets writers 
compress naturally from the start.

## How We Thought About It

We investigated three approaches: reactive compression (compress after writing), 
proactive templates (write compressed from start), and hybrid (both). Each had 
tradeoffs:

- Reactive: Works with existing docs but requires post-processing
- Proactive: Feels natural but requires adoption of new writing patterns  
- Hybrid: Best of both but more complex

## What We Decided

We chose the proactive approach with reactive tools available. Users select 
templates that provide compression guidance. The Claude Skill maintains compression 
as they write. This approach reduces friction: write naturally, compression 
emerges automatically.

## Why This Matters

Research showed users struggle less with compressed writing (when guided by 
templates and parameters) than with post-processing verbose content. The skill 
reduces the mental load—you write normally, parameters control style automatically.
```

---

## 4. Parameter Interpretation Guide

### Understanding Sigma (σ) - Structure Density

**What it controls**: How organized and formatted the content should be

**Low (0.0-0.3): Prose-Heavy**
- **Format**: Flowing paragraphs, minimal structure
- **Use Cases**: Narratives, strategic explanations, vision statements
- **Reading Mode**: Sequential (start to finish)
- **Example Document**: Strategic context, executive summary
- **Key Principle**: Write coherent narrative, prioritize readability over organization

**Medium (0.4-0.6): Mixed**
- **Format**: Paragraphs + bullets + tables balanced
- **Use Cases**: Technical specs, design documents, analysis
- **Reading Mode**: Both sequential and lookup (find specific sections)
- **Example Document**: Technical design, analysis report
- **Key Principle**: Use structure where it helps clarity, prose for explanation

**High (0.7-1.0): Structured**
- **Format**: Tables, lists, key-value pairs, minimal prose
- **Use Cases**: Status updates, metrics dashboards, reference guides
- **Reading Mode**: Lookup (scan to find specific information)
- **Example Document**: Status update, metrics dashboard, API reference
- **Key Principle**: Maximize scanability, minimize prose overhead

### Understanding Gamma (γ) - Granularity/Detail

**What it controls**: How much information to include

**Low (0.0-0.3): Minimal Detail**
- **Content Style**: Keywords, abbreviations, essential facts only
- **Assumptions**: Reader is expert, familiar with domain
- **Use Cases**: Power user references, internal team notes
- **What to Omit**: Obvious context, basic explanations, supporting details
- **Compression Opportunity**: Remove every non-essential word
- **Example**: "Status: ON TRACK | Risk: MEDIUM | ETA: Nov 15 | Blocker: None"

**Medium (0.4-0.6): Moderate Detail**
- **Content Style**: Concise sentences, key facts, essential context
- **Assumptions**: Reader has domain knowledge, understands domain terminology
- **Use Cases**: Team documentation, informed audience
- **What to Include**: Core information, relevant context, key decisions
- **What to Omit**: Background for obvious knowledge, verbose explanations
- **Example**: "Feature complete and QA-ready. Security review pending. ETA one week."

**High (0.7-1.0): Complete Detail**
- **Content Style**: Complete sentences, full context, detailed explanations
- **Assumptions**: Reader may be unfamiliar with domain/project
- **Use Cases**: Public documentation, onboarding, general audience
- **What to Include**: Complete background, definitions, explanations
- **What to Omit**: Nothing essential (completeness prioritized)
- **Example**: "The feature has been fully implemented and is ready for quality assurance testing. The security review is currently pending completion and is expected to finish within one week."

### Understanding Kappa (κ) - Scaffolding/Context

**What it controls**: How much background and explanation to provide

**Low (0.0-0.3): Minimal Scaffolding**
- **Headers**: Minimal or none
- **Context**: Assume shared knowledge, no explanation needed
- **Rationale**: Not provided (assume reader knows why)
- **Audience**: Experts deeply familiar with project
- **Use Cases**: Internal notes, expert discussions
- **Example**: Document jumps directly to technical details without background

**Medium (0.4-0.6): Moderate Scaffolding**
- **Headers**: Standard section headers
- **Context**: Brief background where helpful
- **Rationale**: High-level reasoning for decisions
- **Audience**: Team members with domain knowledge
- **Use Cases**: Team documentation, design decisions
- **Example**: Clear sections with headers, brief context for complex decisions

**High (0.7-1.0): Full Scaffolding**
- **Headers**: Hierarchical, descriptive headers
- **Context**: Complete background and context
- **Rationale**: Full explanation of decisions
- **Audience**: Readers unfamiliar with project
- **Use Cases**: Onboarding, external documentation, historical records
- **Example**: Every section explained, background provided, decisions justified

### Constraint Validation

**The Constraint Equation**:
```
σ + γ + κ ≥ C_min(audience, phase)

Where C_min = base_value(audience) + phase_adjustment(phase)
```

**Base Values by Audience**:
```
LLM audience: C_min_base = 0.7    (LLMs can infer from sparse scaffolding)
Dual audience: C_min_base = 1.0   (balanced for both LLM and human)
Human audience: C_min_base = 1.2  (humans need more context)
```

**Phase Adjustments**:
```
Active phase: C_min_adjustment = 0.0    (current work, context available elsewhere)
Complete phase: C_min_adjustment = +0.1 (work finished, context less accessible)
Archived phase: C_min_adjustment = +0.2 (historical reference, full context needed)
```

**Examples**:
```
LLM audience, active phase:
  C_min = 0.7 + 0.0 = 0.7
  Example: σ=0.8, γ=0.4, κ=0.2 → Sum=1.4 ✓ Valid

Human audience, complete phase:
  C_min = 1.2 + 0.1 = 1.3
  Example: σ=0.3, γ=0.8, κ=0.7 → Sum=1.8 ✓ Valid

Human audience, archived phase:
  C_min = 1.2 + 0.2 = 1.4
  Example: σ=0.3, γ=0.9, κ=0.8 → Sum=2.0 ✓ Valid
```

**How the Skill Uses This**:
1. Calculate C_min from audience and phase metadata
2. Sum the parameters: σ + γ + κ
3. If Sum < C_min: Warn user and suggest adjustments
4. If Sum ≥ C_min: Proceed with confidence
5. Suggest adjustments by increasing lowest dimension (usually κ for LLM audience)

**Typical Adjustment Suggestions**:
```
Constraint violation: σ=0.9, γ=0.2, κ=0.1 (Sum=1.2 < C_min=1.3 for human+complete)

Suggestion 1: Increase κ to 0.2 (minimal context to brief context)
  → New sum: 1.3 ✓

Suggestion 2: Increase γ to 0.3 (keywords to essential facts)
  → New sum: 1.3 ✓

Suggestion 3: Keep current and change audience to LLM
  → C_min drops to 0.7, current 1.2 > 0.7 ✓

Recommendation: Increase κ to 0.2 (easiest adjustment)
```

---

## 5. Writing Pattern Examples

### Example 1: High Compression Status Update
**Parameters**: σ=0.8, γ=0.4, κ=0.2
**Audience**: LLM
**Constraint**: 0.8+0.4+0.2=1.4 ≥ 0.7 ✓

**Frontmatter**:
```yaml
---
compression:
  sigma: 0.8
  gamma: 0.4
  kappa: 0.2
  audience: LLM
  tier: T2
  phase: active
  template: status-high-compression
---
```

**Expected Content**:
```markdown
# Project Status - 2025-11-03

## Accomplished
- [x] Paradigm analysis → Framework expanded (proactive + reactive)
- [x] Specifications → 4 comprehensive docs (4,360 lines)
- [x] Validation → Task 4.1 FIX complete (23/43 passing)
- [x] Intrinsic stability → 96.7% convergence validated

## In Progress
- [ ] TASK-2C Skill specification (Phase 2C)
- [ ] Template library completion (5/8 done)

## Blocked
- None

## Metrics
| Category | Current | Target | Status |
|----------|---------|--------|--------|
| Phase 1 | 80% | 100% | On track |
| Specs | 4 | 4 | Complete |
| Lines | 15.3K | 20K | 76% |

## Next
- TASK-2C delivery
- Phase 2B template implementation
- CLI integration testing
```

**Style Characteristics**:
- Minimal prose (only section headers)
- Structured lists with outcomes only
- Abbreviations used (etc.)
- No explanatory context
- Table for metrics
- Checkboxes for tasks

### Example 2: Medium Compression Technical Design
**Parameters**: σ=0.6, γ=0.6, κ=0.4
**Audience**: dual
**Constraint**: 0.6+0.6+0.4=1.6 ≥ 1.0 ✓

**Frontmatter**:
```yaml
---
compression:
  sigma: 0.6
  gamma: 0.6
  kappa: 0.4
  audience: dual
  tier: T2
  phase: active
  template: technical-design
---
```

**Expected Content**:
```markdown
# Skill Implementation Architecture

## Overview
The Claude Compression Skill reads YAML frontmatter parameters (σ, γ, κ) and 
maintains compressed writing style throughout document lifecycle. This document 
outlines the design approach.

## Core Challenge: Parameter Interpretation
How do we translate abstract parameters (0.0-1.0 ranges) into concrete writing 
guidance? Three requirements:

1. **Deterministic**: Same parameters → same style (consistency)
2. **Intuitive**: Users understand what to expect
3. **Flexible**: Supports diverse document types

## Design Approach: Technique Mapping

We map parameters to LSC techniques:

| Parameter | Range | Technique | Benefit |
|-----------|-------|-----------|---------|
| σ | ≥0.7 | Structured lists | 60% prose reduction |
| γ | <0.4 | Abbreviations | 20% token savings |
| κ | <0.3 | Minimal headers | 30% scaffolding reduction |

**Rationale**: Each technique targets highest-impact compression in its dimension.

## Implementation Phases

**Phase 1: Parameter Detection** (Week 1)
- Read YAML frontmatter
- Validate ranges and constraint
- Select appropriate techniques

**Phase 2: Content Application** (Week 2)
- Apply techniques during writing
- Maintain consistency through edits
- Flag constraint violations

**Phase 3: Refinement** (Week 3)
- Adjust technique mappings based on feedback
- Optimize for common parameter combinations

## Success Criteria
- ✓ Parameters parsed correctly
- ✓ Style matches parameters (manual review)
- ✓ Consistency maintained through edits
- ✓ Users report natural writing experience
```

**Style Characteristics**:
- Mix of prose and lists
- Some tables for data
- Brief explanations with context
- Standard headers (not excessive)
- Both enumerated and narrative sections
- Rationale provided for decisions

### Example 3: Low Compression Strategic Narrative
**Parameters**: σ=0.3, γ=0.8, κ=0.7
**Audience**: human
**Constraint**: 0.3+0.8+0.7=1.8 ≥ 1.3 (human+complete phase) ✓

**Frontmatter**:
```yaml
---
compression:
  sigma: 0.3
  gamma: 0.8
  kappa: 0.7
  audience: human
  tier: T1
  phase: complete
  template: strategic-narrative
---
```

**Expected Content**:
```markdown
# Why We Built a Compression Framework

## The Problem We Encountered

As our project documentation grew beyond 20,000 lines, we noticed a persistent 
friction point: every session started with loading comprehensive context files. 
The Claude context window would consume 2,000-3,000 tokens just on baseline 
project understanding, leaving less room for actual work.

Initially, we assumed this was inevitable overhead. However, deeper investigation 
revealed a pattern: most of this verbose documentation served the machine (Claude) 
perfectly well in structured form. The verbosity was there for human readers—and 
even then, humans usually wanted just specific pieces, not entire narratives.

## The Insight: Machine-First Design

This led to a fundamental question: What if we optimized documentation for how 
it's actually used during sessions, rather than how it looks in a repository?

The answer was LLM-Shorthand Context (LSC), a structured format that reduces 
context consumption by 70-85%. Instead of prose paragraphs, you get YAML/JSON with 
stable IDs and triples for relationships. The machine understands this immediately; 
the human can request a readable view if needed.

## From Reaction to Proaction

Building on LSC, we discovered a larger opportunity: what if writers could compress 
naturally from the start, guided by simple parameters? This would eliminate the 
reactive compression cycle ("write verbose, then compress") with a proactive 
approach ("write efficiently with guidance").

The result is the Compression Framework: a three-parameter system (σ, γ, κ) that 
lets any document be written at the optimal compression level for its purpose, 
audience, and lifecycle phase.

## Why This Matters

Documentation quality improves when writers have clear guidance. Compression quality 
improves when parameters are explicit, not implicit. Adoption improves when writing 
feels natural, not forced.

This framework provides all three. And by grounding it in rigorous information 
theory and empirical validation, we've built something that works reliably across 
diverse projects and contexts.

## What Comes Next

The skills and templates make this framework practical. Users select a template 
("Status Update"), fill it with content, and the compression emerges naturally. 
Post-processing becomes optional, not mandatory.

For projects already using compression, the reactive tool can still help with 
bulk recompression and validation. But the future is proactive: write compressed 
from the start.
```

**Style Characteristics**:
- Flowing prose paragraphs
- Complete sentences and full explanations
- Hierarchical headers with descriptive titles
- No abbreviations (or first use defined)
- Complete context and background
- Narrative structure maintained
- Explanations for all decisions

### Example 4: High Structure Quick Reference
**Parameters**: σ=0.9, γ=0.3, κ=0.1
**Audience**: power-users
**Constraint**: 0.9+0.3+0.1=1.3 ≥ 0.7 ✓

**Expected Content**:
```markdown
# Compression Parameters Quick Reference

## Parameter Ranges
| Param | Range | Default | Meaning |
|-------|-------|---------|---------|
| σ (sigma) | 0.0-1.0 | 0.5 | Structure density |
| γ (gamma) | 0.0-1.0 | 0.5 | Granularity |
| κ (kappa) | 0.0-1.0 | 0.5 | Scaffolding |

## Quick Selection

**Status Updates**: σ=0.8, γ=0.4, κ=0.2  
**Design Docs**: σ=0.6, γ=0.6, κ=0.4  
**Strategic Docs**: σ=0.3, γ=0.8, κ=0.7  
**Quick Ref**: σ=0.9, γ=0.3, κ=0.1  

## Technique Matrix

| σ Range | Techniques |
|---------|-----------|
| ≥0.7 | lists, tables, hierarchy, abbrev |
| 0.4-0.7 | selective_lists, prose_focus |
| <0.4 | prose, compression |

| γ Range | Detail Level |
|---------|-------------|
| <0.4 | keywords, minimal |
| 0.4-0.7 | essential facts |
| ≥0.7 | complete, detailed |

| κ Range | Scaffolding |
|---------|------------|
| <0.3 | minimal, assume knowledge |
| 0.3-0.6 | standard headers, brief context |
| ≥0.6 | full headers, explanations |

## Constraint Check
```
σ + γ + κ ≥ C_min(audience, phase)

C_min = {LLM: 0.7, dual: 1.0, human: 1.2} + {active: 0, complete: +0.1, archived: +0.2}
```

## Techniques by Name
- **structured_lists**: Bullet lists with metrics
- **hierarchical_structure**: Multi-level headers
- **table_format**: Markdown tables
- **abbreviations**: Standard acronyms
- **selective_lists**: Targeted bullets
- **concise_prose**: Short sentences, active voice
```

**Style Characteristics**:
- Pure structured format (tables, no prose)
- Minimal headers
- Abbreviations throughout
- No explanations
- Direct lookup use

### Example 5: Analysis & Findings (Medium-Low Compression)
**Parameters**: σ=0.5, γ=0.7, κ=0.5
**Audience**: dual
**Constraint**: 0.5+0.7+0.5=1.7 ≥ 1.0 ✓

**Expected Content**:
```markdown
# Compression Framework Adoption Study: Key Findings

## Executive Summary
Analysis of 15 projects using the compression framework reveals three key findings:

1. Adoption increases 40% when templates provided (vs. bare parameters)
2. Writing time decreases 15-20% with parameter guidance (vs. free-form)
3. Compression quality improves 25% when skill actively maintains style (vs. manual)

## Methodology
We tracked compression metrics across three cohorts:

- **Cohort A** (n=5): Manual compression using parameters only
- **Cohort B** (n=5): Template-guided with skill assistance
- **Cohort C** (n=5): Reactive compression (post-writing)

Each cohort wrote identical briefing documents. We measured writing time, 
compression ratio achieved, and author satisfaction.

## Key Finding 1: Templates Drive Adoption

Projects using templates showed:
- 40% higher adoption rate (4/5 vs 2/5 active users)
- 30% faster onboarding (1 week vs 2-3 weeks)
- Better consistency across teams

**Why It Matters**: Adoption is primary constraint, not technical capability.

## Key Finding 2: Skill Maintains Consistency

Documents edited with skill assistance maintained compression level with:
- 95% consistency (compression ratio variation <5%)
- 100% idempotency (re-compression → no changes)
- Natural writing experience (reported by 9/10 users)

**Implication**: Skill reduces mental load—writers don't think about compression.

## Key Finding 3: Parameter Clarity Drives Results

Projects with clear parameter definitions (σ, γ, κ explicit) achieved:
- Better alignment (98% of content matched target parameters)
- Fewer violations (only 2% constraint violations vs 15% without guidance)
- Higher satisfaction (8/10 vs 6/10 satisfaction score)

## Recommendations

**Short-term**: Distribute templates broadly (adopt early wins)  
**Medium-term**: Implement skill in primary authoring tools  
**Long-term**: Build parameter literacy in organization  

## Limitations

Analysis limited to single project type (technical documentation). Results may 
differ for creative writing, strategic narratives, or other formats.
```

**Style Characteristics**:
- Balanced mix of prose and structure
- Findings stated as facts with supporting data
- Some lists but mostly narrative explanation
- Moderate detail (key information + context)
- Standard headers with brief explanations

---

## 6. Skill Implementation Guide

### For Claude (When Using This Skill)

**Before Writing**:
1. Always read frontmatter FIRST
2. Extract and validate (σ, γ, κ) parameters
3. Calculate C_min for audience/phase
4. Verify constraint: σ + γ + κ ≥ C_min
5. If violated: Warn user and suggest adjustments
6. Select appropriate LSC techniques

**During Writing**:
1. Apply selected techniques naturally
2. Maintain consistency throughout
3. Use style matching parameter interpretation
4. Flag style drift if new content doesn't match
5. Support parameter changes fluidly

**After Writing**:
1. Review for idempotency (compressed parts should be stable)
2. Verify consistency with template structure
3. Validate constraint still satisfied
4. Provide feedback on compression effectiveness

**Key Principles**:
- ✓ Always read parameters first
- ✓ Apply techniques consistently
- ✓ Maintain idempotent behavior
- ✓ Warn on constraint violations
- ✓ Respect user changes to parameters
- ✓ Preserve already-compressed sections

### For Users

**How to Activate the Skill**:
1. Create/open document with compression frontmatter
2. Include YAML header with (σ, γ, κ) parameters
3. Skill auto-activates when frontmatter detected
4. Or explicitly invoke: `@compression` or `/compression` (depending on implementation)

**What to Expect**:
- Skill reads parameters and understands your target style
- Content generation follows that style automatically
- Editing maintains compression level
- Feedback on constraint violations (if any)
- Suggestions for parameter adjustment if needed

**Common Issues & Solutions**:

| Issue | Solution |
|-------|----------|
| Skill generates too-verbose content | Lower γ (reduce granularity) |
| Content lacks necessary context | Raise κ (increase scaffolding) |
| Skill uses too many lists | Lower σ (reduce structure) |
| Constraint violation warning | Increase lowest parameter by 0.1 |
| Confusion about parameter meaning | See Section 4 (Parameter Interpretation) |

**Tips for Success**:
1. Start with templates (better than bare parameters)
2. Set C_min first (audience + phase determine requirements)
3. Tune parameters gradually (small adjustments, test results)
4. Don't overthink it (skill handles most details automatically)
5. Use constraint violation warnings as guidance, not blocks

---

## 7. Integration with Template Library

### Template-Skill Integration Flow

**Step 1: Template Selection**
User chooses template from library: "High Compression Status Update"

**Step 2: Frontmatter Provision**
Template provides pre-configured YAML header:
```yaml
---
compression:
  sigma: 0.8
  gamma: 0.4
  kappa: 0.2
  audience: LLM
  tier: T2
  phase: active
  template: status-high-compression
---
```

**Step 3: Skill Activation**
Skill reads frontmatter and loads configuration:
- Parameters: σ=0.8, γ=0.4, κ=0.2
- Techniques: structured_lists, hierarchical_structure, abbreviations
- Style: Tables for metrics, bullets for achievements

**Step 4: Content Generation**
User writes content following template structure. Skill:
- Applies compression techniques automatically
- Maintains parameter consistency
- Preserves already-compressed sections during edits
- Provides feedback on constraint satisfaction

**Step 5: Document Completion**
Result: Document at target compression level, no post-processing needed

### Template-Specific Skill Behavior

**Template: Status Update** (σ=0.8, γ=0.4, κ=0.2)
- Skill generates: Section headers only (minimal prose)
- Uses: Tables for metrics, bullets for achievements
- Expects: Concise facts, no explanations
- Maintains: Checkbox format for tasks

**Template: Technical Design** (σ=0.6, γ=0.6, κ=0.4)
- Skill generates: Balanced prose and structure
- Uses: Lists for options, tables for comparisons
- Expects: Rationale for decisions, context where needed
- Maintains: Consistent decision record structure

**Template: Strategic Narrative** (σ=0.3, γ=0.8, κ=0.7)
- Skill generates: Flowing prose with full explanation
- Uses: Hierarchical headers, complete background
- Expects: Full context, narrative coherence
- Maintains: Coherent story arc through sections

**Template: Quick Reference** (σ=0.9, γ=0.3, κ=0.1)
- Skill generates: Pure structured data (tables, lists)
- Uses: Minimal headers, abbreviations
- Expects: Direct lookup, no context
- Maintains: Format consistency and abbreviation dictionary

### Working with Different Templates

**Switching Templates**:
1. Update compression parameters in frontmatter
2. Skill detects change and adapts to new parameters
3. New content follows new style
4. Old content remains unchanged (idempotent)
5. Result: Mixed compression states handled automatically

**Customizing Parameters Within Template**:
1. Start with template default parameters
2. Adjust (σ, γ, κ) if needed
3. Verify new constraint: σ + γ + κ ≥ C_min
4. Skill applies new parameters to subsequent edits
5. Template structure provides guidance, parameters control compression level

**Mixing Parameters Across Sections**:
1. Advanced: Use different parameters for different sections
2. Add multiple YAML blocks (one per section) or comments
3. Skill adapts when parameters change
4. Useful for: Documents with mixed audiences or purposes

---

## 8. Validation Strategy

### How to Verify Skill is Working Correctly

#### Test 1: Parameter Parsing
**Objective**: Confirm skill correctly reads frontmatter

- **Action**: Create document with various parameter combinations
- **Expected**: Skill reads and confirms understanding
- **Validation**: Check parameters logged/reported correctly

**Test Cases**:
- σ=0.8, γ=0.4, κ=0.2 (high compression)
- σ=0.5, γ=0.5, κ=0.5 (medium compression)
- σ=0.3, γ=0.8, κ=0.7 (low compression)
- σ=0.9, γ=0.2, κ=0.1 (edge case high)

#### Test 2: Parameter Validation
**Objective**: Confirm skill validates ranges and constraints

- **Action**: Test invalid/edge-case parameters
- **Expected**: Appropriate error handling or warnings

**Test Cases**:
- Constraint violation: σ=0.8, γ=0.3, κ=0.1 for human audience
- Out of range: σ=1.5 (too high)
- Edge case valid: σ=0.0, γ=0.7, κ=1.0
- Missing parameters: No frontmatter (use defaults)

#### Test 3: Technique Selection
**Objective**: Confirm skill selects appropriate techniques

- **Action**: Generate content with different parameter sets
- **Expected**: Techniques match parameter interpretation

**Validation**:
- σ ≥ 0.7 → Content uses tables and lists (not prose-heavy)
- γ < 0.4 → Content uses abbreviations and omits obvious details
- κ < 0.3 → Content has minimal headers, no explanations
- Technique combinations applied correctly

#### Test 4: Style Consistency
**Objective**: Verify generated content matches parameters

- **Action**: Generate multiple sections with same parameters
- **Expected**: Consistent compression level across sections

**Validation Criteria**:
- Manual review by human: "Does style match what I'd expect from parameters?"
- Consistency check: All sections follow same compression pattern
- Constraint satisfaction: σ + γ + κ maintained throughout

#### Test 5: Idempotent Behavior
**Objective**: Confirm already-compressed content is stable

- **Action**: Generate document, then apply skill again to same content
- **Expected**: Compressed sections unchanged, no new compression applied

**Validation**:
- Mixed compression state (some sections compressed, some not)
- Reapply skill to entire document
- Result: Uncompressed sections now compressed, previously-compressed sections unchanged
- Verify through token count comparison

#### Test 6: Edit Consistency
**Objective**: Confirm editing maintains compression level

- **Action**: Create document with skill, edit existing section, add new section
- **Expected**: New content at same compression level as original

**Validation**:
- Edit existing compressed section: Check it stays compressed
- Add new uncompressed section: Check it becomes compressed to match
- Edit summary field: Check style consistent with parameters
- Verify through manual review and token counting

#### Test 7: Template Integration
**Objective**: Confirm skill works with all 8 templates

- **Action**: Use skill with each template type
- **Expected**: Generated content appropriate for each template

**Test All Templates**:
- ✓ Status Update (high compression)
- ✓ Technical Design (medium compression)
- ✓ Analysis & Findings (medium-low compression)
- ✓ Meeting Notes (medium-high compression)
- ✓ Decision Record (medium compression)
- ✓ Quick Reference (very high compression)
- ✓ Educational Guide (low compression)
- ✓ Strategic Narrative (low compression)

#### Test 8: Error Handling
**Objective**: Confirm graceful degradation for edge cases

- **Action**: Test error scenarios
- **Expected**: Clear error messages, suggested fixes

**Error Cases**:
- Missing compression frontmatter: Use sensible defaults
- Invalid YAML: Parse error with helpful message
- Constraint violation: Warn and suggest adjustment
- Parameter out of range: Clamp to valid range or error
- Ambiguous user request: Ask for clarification

### Quality Metrics

**Functionality Metrics**:
- ✓ Parameter parsing success rate: 100%
- ✓ Constraint validation accuracy: 100%
- ✓ Technique selection correctness: 95%+ (manual review)
- ✓ Template compatibility: All 8 templates supported

**Style Metrics**:
- ✓ Style consistency: 90%+ (cross-section evaluation)
- ✓ Idempotent behavior: 100% (re-compression produces no changes)
- ✓ User satisfaction: 8+/10 (writing feels natural)
- ✓ Adoption rate: 70%+ (among template users)

**Constraint Metrics**:
- ✓ Constraint satisfaction: 100% of valid documents
- ✓ Violation detection: 100% (when C_min not met)
- ✓ Suggestion quality: 95%+ (adjustments resolve violations)

---

## 9. Conclusion

The Claude Compression Skill completes the proactive compression system by:

1. **Reading Parameters**: Interprets (σ, γ, κ) from frontmatter
2. **Selecting Techniques**: Maps parameters to LSC techniques
3. **Maintaining Compression**: Applies techniques consistently through edits
4. **Preserving Idempotency**: Already-compressed content remains stable
5. **Validating Constraints**: Ensures information preservation through C_min checks

**Result**: Users write naturally in compressed form without post-processing, enabled by clear parameters and skill automation.

**Integration**: Templates provide frontmatter, skill reads and applies parameters, users write naturally, documents emerge compressed.

**Quality**: Framework validated through empirical testing (compress.py), intrinsic stability confirmed (96.7% convergence), ready for practical use.

---

## Appendix A: Quick Reference Tables

### Technique Matrix (σ, γ, κ → Techniques)

| σ | γ | κ | Primary Techniques | Example | Use Case |
|---|---|---|-------------------|---------|----------|
| ≥0.7 | <0.4 | <0.3 | lists, abbrev, minimal_headers | Status | High-density update |
| ≥0.7 | 0.4-0.7 | 0.3-0.6 | lists, tables, standard_headers | Metrics | Structured data |
| 0.4-0.7 | 0.4-0.7 | 0.3-0.6 | selective_lists, concise_prose | Design | Technical doc |
| 0.4-0.7 | 0.6-1.0 | 0.4-0.7 | prose, lists, good_headers | Analysis | Research finding |
| <0.4 | 0.6-1.0 | 0.4-0.7 | active_voice, concise_prose | Narrative | Strategic text |
| <0.4 | 0.8-1.0 | 0.7-1.0 | flowing_prose, full_explanation | Onboarding | Educational |

### Parameter Selection by Document Type

| Document Type | σ | γ | κ | Audience | Template |
|---|---|---|---|---|---|
| Status Update | 0.8 | 0.4 | 0.2 | LLM | status-high-compression |
| Metrics Dashboard | 0.9 | 0.3 | 0.1 | Power-user | quick-reference |
| Design Decision | 0.5 | 0.7 | 0.5 | Dual | decision-record |
| Technical Spec | 0.6 | 0.6 | 0.4 | Dual | technical-design |
| Analysis Report | 0.5 | 0.7 | 0.5 | Dual | analysis |
| Meeting Notes | 0.7 | 0.5 | 0.3 | Team | meeting-notes |
| Strategic Vision | 0.3 | 0.8 | 0.7 | Human | strategic-narrative |
| Onboarding Guide | 0.4 | 0.9 | 0.8 | New-user | educational |

### Constraint Validation Quick Reference

| Audience | Phase | C_min | Example Valid | Example Invalid |
|---|---|---|---|---|
| LLM | Active | 0.7 | 0.8+0.4+0.2 = 1.4 ✓ | 0.5+0.1+0.0 = 0.6 ✗ |
| LLM | Complete | 0.8 | 0.3+0.3+0.3 = 0.9 ✓ | 0.2+0.2+0.2 = 0.6 ✗ |
| LLM | Archived | 0.9 | 0.3+0.3+0.4 = 1.0 ✓ | 0.3+0.3+0.2 = 0.8 ✗ |
| Dual | Active | 1.0 | 0.5+0.5+0.5 = 1.5 ✓ | 0.3+0.3+0.3 = 0.9 ✗ |
| Dual | Complete | 1.1 | 0.4+0.4+0.4 = 1.2 ✓ | 0.3+0.3+0.3 = 0.9 ✗ |
| Dual | Archived | 1.2 | 0.4+0.4+0.4 = 1.2 ✓ | 0.3+0.3+0.3 = 0.9 ✗ |
| Human | Active | 1.2 | 0.3+0.5+0.5 = 1.3 ✓ | 0.3+0.3+0.5 = 1.1 ✗ |
| Human | Complete | 1.3 | 0.3+0.5+0.6 = 1.4 ✓ | 0.3+0.5+0.4 = 1.2 ✗ |
| Human | Archived | 1.4 | 0.3+0.5+0.7 = 1.5 ✓ | 0.3+0.5+0.5 = 1.3 ✗ |

---

**Specification Complete. Ready for Phase 2C Implementation.**

**Success Criteria Met**:
- ✅ Complete skill specification document (750+ lines)
- ✅ Clear behavior rules for creation and editing
- ✅ Comprehensive parameter interpretation guide
- ✅ Deterministic algorithm for technique selection
- ✅ 5 writing pattern examples across parameter range
- ✅ Detailed integration instructions with templates
- ✅ Comprehensive validation strategy and testing checklist
- ✅ Implementation notes for Claude and users
- ✅ Quick reference tables and appendices
- ✅ Ready for practical use with template library
