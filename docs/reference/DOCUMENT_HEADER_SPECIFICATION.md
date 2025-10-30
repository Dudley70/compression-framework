# Document Header Specification

**Version**: 1.0
**Date**: 2025-10-31
**Status**: Complete

## Table of Contents

1. [Overview](#overview)
2. [Quick Start Guide](#quick-start-guide)
3. [Field Reference](#field-reference)
4. [Document Type Guide](#document-type-guide)
5. [Validation Rules](#validation-rules)
6. [Usage Patterns](#usage-patterns)
7. [Migration Guide](#migration-guide)
8. [Examples Library](#examples-library)

---

## Overview

### Purpose

This specification defines a standardized YAML frontmatter structure for documentation that enables intelligent compression decisions without reading full document content. Headers provide structured metadata for document classification, compression tracking, and style guidance.

### Benefits

- **Intelligent Tool Decisions**: Compression tools can make informed choices about (σ, γ, κ) parameters
- **Compression Tracking**: Monitor compression state and detect drift over time
- **Style Consistency**: Maintain appropriate writing style for document type and audience
- **Workflow Optimization**: Skip unnecessary analysis for documents with known state
- **Machine Readability**: Structured format enables programmatic processing

### When to Use Headers

**Required for:**
- Documents that will be compressed
- Documents requiring specific style guidance
- Session handover documents
- Task specifications for Claude Code

**Recommended for:**
- All project documentation
- Reference materials
- Analysis and research documents
- Validation reports

**Optional for:**
- Simple README files
- Temporary working documents
- External documentation (not project-controlled)

---

## Quick Start Guide

### 1. Basic Header (3 minutes)

For most documents, start with this template:

```yaml
---
doc_type: [CHOOSE_TYPE]
audience: [CHOOSE_AUDIENCE]
layer: Operational
phase: Active
purpose: [CHOOSE_PURPOSE]

target_style:
  sigma: 0.5
  gamma: 0.7
  kappa: 0.5
---
```

### 2. Choose Your Values

**doc_type**: What kind of document is this?
- `API_REFERENCE` - API documentation
- `TUTORIAL` - Learning content
- `PROJECT_CONTEXT` - Strategic overview
- `VALIDATION_REPORT` - Test results
- [See full list](#document-type-doc_type)

**audience**: Who will read this?
- `llm-only` - Only for AI/Claude (κ=0.1-0.3)
- `human-technical` - Technical team (κ=0.3-0.5)
- `human-general` - General audience (κ=0.5-0.7)
- `multi-role` - Both humans and AI (κ=0.4-0.6)

**purpose**: Why does this document exist?
- `Execution` - Active instructions
- `Learning` - Educational content
- `Reference` - Quick lookup
- `Planning` - Future work design

### 3. Adjust Target Style

The `target_style` parameters guide compression and writing:

- **sigma (σ)**: Structure density
  - `0.0-0.3` - Narrative prose
  - `0.4-0.6` - Mixed format
  - `0.7-1.0` - Structured lists/data

- **gamma (γ)**: Semantic detail
  - `0.0-0.3` - Keywords only
  - `0.4-0.6` - Moderate detail
  - `0.7-1.0` - Full semantic content

- **kappa (κ)**: Contextual scaffolding
  - `0.0-0.3` - Minimal context
  - `0.4-0.6` - Moderate explanation
  - `0.7-1.0` - Full scaffolding

### 4. Common Patterns

```yaml
# API Reference (structured, minimal context)
target_style: {sigma: 0.8, gamma: 0.6, kappa: 0.2}

# Tutorial (prose, full explanation)
target_style: {sigma: 0.4, gamma: 0.8, kappa: 0.7}

# Session Handover (structured, moderate detail)
target_style: {sigma: 0.7, gamma: 0.7, kappa: 0.3}

# Strategic Context (balanced)
target_style: {sigma: 0.5, gamma: 0.8, kappa: 0.5}
```

---

## Field Reference

### Document Type (doc_type)

**Required**: Yes
**Format**: `SCREAMING_SNAKE_CASE`
**Purpose**: Classify document for appropriate compression strategy

#### Valid Values

| Type | Description | Typical σ,γ,κ |
|------|-------------|---------------|
| `API_REFERENCE` | API endpoints, parameters, responses | 0.8, 0.6, 0.2 |
| `TUTORIAL` | Step-by-step learning content | 0.4, 0.8, 0.7 |
| `SESSION_HANDOVER` | Session-to-session context transfer | 0.7, 0.7, 0.3 |
| `PROJECT_CONTEXT` | Strategic context and decision history | 0.5, 0.8, 0.5 |
| `TASK_SPECIFICATION` | Autonomous task delegation specs | 0.6, 0.9, 0.6 |
| `VALIDATION_REPORT` | Test results and validation findings | 0.6, 0.8, 0.4 |
| `ANALYSIS` | Research findings and detailed analysis | 0.5, 0.8, 0.5 |
| `PLAN` | Implementation plans and roadmaps | 0.6, 0.7, 0.4 |
| `REFERENCE` | Quick reference guides and lookup tables | 0.9, 0.5, 0.1 |
| `PATTERN` | Reusable patterns and best practices | 0.6, 0.8, 0.4 |
| `METHODOLOGY` | Process documentation and frameworks | 0.5, 0.8, 0.6 |
| `RESEARCH` | Literature review and external research | 0.4, 0.9, 0.6 |
| `PROPOSAL` | Design proposals and RFCs | 0.5, 0.8, 0.6 |

---

### Audience (audience)

**Required**: Yes
**Format**: `kebab-case`
**Purpose**: Determine appropriate contextual scaffolding (κ) parameters

#### Valid Values

| Audience | Description | Typical κ | Use Case |
|----------|-------------|-----------|----------|
| `llm-only` | LLM consumption only | 0.1-0.3 | Compressed handovers, internal state |
| `human-technical` | Technical users with domain expertise | 0.3-0.5 | API docs, technical specifications |
| `human-general` | General audience needing explanation | 0.5-0.7 | Tutorials, user documentation |
| `multi-role` | Both LLM and human readers | 0.4-0.6 | Project context, validation reports |

#### Compression Impact

The audience field directly influences compression aggressiveness:

- **llm-only**: Aggressive context removal (κ=0.1-0.3)
  - Remove explanatory text
  - Use technical shorthand
  - Assume background knowledge

- **human-technical**: Moderate context (κ=0.3-0.5)
  - Keep essential explanations
  - Preserve technical accuracy
  - Remove obvious elaborations

- **human-general**: Conservative context (κ=0.5-0.7)
  - Maintain explanatory scaffolding
  - Keep examples and analogies
  - Preserve learning context

- **multi-role**: Balanced approach (κ=0.4-0.6)
  - Optimize for both audiences
  - Keep essential context
  - Remove redundant explanations

---

### Information Layer (layer)

**Required**: Yes
**Format**: `PascalCase`
**Purpose**: Classify information lifecycle and determine compression aggressiveness

#### Valid Values

| Layer | Description | Compression Guidelines | Access Pattern |
|-------|-------------|----------------------|----------------|
| `Session` | Per-session ephemeral context | Aggressive (95-99%) | Temporary, frequent access |
| `Strategic` | Long-term project context | Moderate (70-85%) | Stable, periodic access |
| `Control` | Configuration and instructions | Conservative (minimal) | Critical, infrequent changes |
| `Operational` | Active work and tasks | Moderate (70-85%) | Current, regular access |
| `Archive` | Historical reference | Ultra-aggressive (95-99%) | Rarely accessed |

#### Layer-Specific Guidelines

**Session Layer**
- Files: Session handovers, temporary analyses
- Lifecycle: Hours to days
- Compression: Very aggressive once complete
- Example: `SESSION.md`, daily standup notes

**Strategic Layer**
- Files: Project context, decision logs, vision documents
- Lifecycle: Weeks to months
- Compression: Moderate, preserve decision history
- Example: `PROJECT.md`, architecture decisions

**Control Layer**
- Files: Task specifications, configuration, critical instructions
- Lifecycle: Stable, versioned
- Compression: Minimal or none
- Example: `TASK_*.md`, deployment configs

**Operational Layer**
- Files: Current work, validation reports, active analysis
- Lifecycle: Days to weeks
- Compression: Moderate
- Example: Analysis documents, test reports

**Archive Layer**
- Files: Completed work, historical records
- Lifecycle: Long-term storage
- Compression: Very aggressive
- Example: Old session notes, deprecated documentation

---

### Lifecycle Phase (phase)

**Required**: Yes
**Format**: `PascalCase`
**Purpose**: Track document maturity and update frequency

#### Valid Values

| Phase | Description | Update Frequency | Compression Impact |
|-------|-------------|------------------|-------------------|
| `Active` | Currently being written/updated | Daily to weekly | Conservative compression |
| `Complete` | Finished, infrequent updates | Monthly or less | Moderate compression |
| `Archived` | Historical, rarely accessed | Rarely | Aggressive compression |
| `Deprecated` | Superseded by newer version | Never | Ultra-aggressive compression |

#### Automatic Transitions

The phase should be updated based on activity:

- **Active → Complete**: No updates for 7+ days
- **Complete → Archived**: No updates for 30+ days
- **Archived → Deprecated**: Replaced by new document

#### Phase-Specific Behavior

**Active Phase**
- Preserve full context for ongoing work
- Minimal compression to maintain editability
- Frequent validation of header accuracy

**Complete Phase**
- Moderate compression acceptable
- Stable content, occasional updates
- Focus on accessibility and clarity

**Archived Phase**
- Aggressive compression to save space
- Optimize for occasional reference
- Preserve essential information only

**Deprecated Phase**
- Ultra-aggressive compression
- Minimal metadata preservation
- Consider removal after transition period

---

### Purpose (purpose)

**Required**: Yes
**Format**: `PascalCase`
**Purpose**: Understand document's role in workflow

#### Valid Values

| Purpose | Description | Content Focus | Style Impact |
|---------|-------------|---------------|--------------|
| `Execution` | Active instructions for task completion | Action-oriented, precise | High structure (σ↑) |
| `Learning` | Educational content for understanding | Explanatory, scaffolded | High context (κ↑) |
| `Reference` | Quick lookup information | Concise, searchable | Low context (κ↓) |
| `Audit` | Historical record keeping | Complete, traceable | Moderate detail (γ↑) |
| `Planning` | Future work and design | Forward-looking, strategic | Balanced approach |
| `Analysis` | Research and investigation results | Detailed, evidence-based | High semantic (γ↑) |

#### Purpose-Driven Optimization

**Execution Documents**
- Emphasize actionable steps
- Use structured formats (bullets, numbered lists)
- Minimize explanatory context
- Example: Task specifications, deployment guides

**Learning Documents**
- Provide comprehensive explanations
- Include examples and analogies
- Maintain pedagogical scaffolding
- Example: Tutorials, onboarding guides

**Reference Documents**
- Optimize for quick scanning
- Use consistent formatting
- Minimal contextual overhead
- Example: API references, command cheat sheets

**Audit Documents**
- Preserve complete information
- Maintain traceability
- Include supporting evidence
- Example: Validation reports, decision logs

---

### Target Style (target_style)

**Required**: Yes (for all documents)
**Format**: Object with σ, γ, κ parameters
**Purpose**: Guide compression and writing style

#### Parameter Definitions

```yaml
target_style:
  sigma: 0.0-1.0    # Structure density
  gamma: 0.0-1.0    # Semantic granularity
  kappa: 0.0-1.0    # Contextual scaffolding
```

#### Sigma (σ): Structure Density

Controls the balance between narrative prose and structured data.

| Range | Style | Example |
|-------|-------|---------|
| 0.0-0.3 | Narrative prose | "First, you need to install the dependencies. This involves running npm install, which will read your package.json file and download all required packages." |
| 0.4-0.6 | Mixed format | "## Installation\n\nInstall dependencies:\n```bash\nnpm install\n```\nThis reads package.json and downloads required packages." |
| 0.7-1.0 | Structured data | "- Install: `npm install`\n- Reads: `package.json`\n- Downloads: required packages" |

**When to use high σ (0.7-1.0):**
- API references
- Quick reference guides
- Command cheat sheets
- Data tables and lists

**When to use low σ (0.0-0.3):**
- Tutorials
- Explanatory documentation
- Strategic overviews
- Research papers

#### Gamma (γ): Semantic Granularity

Controls the level of semantic detail preserved.

| Range | Detail Level | Example |
|-------|-------------|---------|
| 0.0-0.3 | Keywords only | "npm install, dependencies, package.json" |
| 0.4-0.6 | Essential meaning | "Run npm install to get dependencies from package.json" |
| 0.7-1.0 | Full semantic content | "Execute npm install command to automatically download and install all project dependencies specified in the package.json configuration file" |

**When to use high γ (0.7-1.0):**
- Educational content
- Complex explanations
- Research documentation
- First-time user guides

**When to use low γ (0.0-0.3):**
- Quick references
- Expert-level documentation
- Compressed session notes
- Keyword summaries

#### Kappa (κ): Contextual Scaffolding

Controls the amount of explanatory context and background information.

| Range | Context Level | Example |
|-------|--------------|---------|
| 0.0-0.3 | Minimal context | "`npm install` - installs deps" |
| 0.4-0.6 | Essential context | "Run `npm install` to install project dependencies listed in package.json" |
| 0.7-1.0 | Full scaffolding | "To set up your development environment, you'll need to install the project dependencies. Run the `npm install` command in your terminal. This reads the package.json file and downloads all required packages to the node_modules directory." |

**When to use high κ (0.7-1.0):**
- General audience documentation
- Learning materials
- Onboarding guides
- Cross-team communication

**When to use low κ (0.0-0.3):**
- Expert-only documentation
- Internal system notes
- LLM-consumed content
- Reference materials

#### Common Parameter Combinations

```yaml
# API Reference: Structured, essential detail, minimal context
target_style: {sigma: 0.8, gamma: 0.6, kappa: 0.2}

# Tutorial: Mixed format, full detail, full context
target_style: {sigma: 0.4, gamma: 0.8, kappa: 0.7}

# Session Handover: Structured, good detail, minimal context
target_style: {sigma: 0.7, gamma: 0.7, kappa: 0.3}

# Strategic Context: Balanced approach
target_style: {sigma: 0.5, gamma: 0.8, kappa: 0.5}

# Quick Reference: Highly structured, minimal detail, no context
target_style: {sigma: 0.9, gamma: 0.5, kappa: 0.1}

# Research Paper: Prose format, full detail, good context
target_style: {sigma: 0.3, gamma: 0.9, kappa: 0.6}
```

---

### Compression Tracking (compression)

**Required**: Only if document has been compressed
**Format**: Object with compression metadata
**Purpose**: Track compression state and enable drift detection

#### Field Structure

```yaml
compression:
  last_full_compression: "YYYY-MM-DD HH:MM TZ"
  baseline_tokens: 1234
  parameters: {σ: 0.8, γ: 0.6, κ: 0.2}
  validation:
    entity_preservation: 0.94
    semantic_similarity: 0.82
```

#### Field Definitions

**last_full_compression**
- Format: ISO datetime with timezone
- Example: `"2025-10-31 14:30 AEDT"`
- Purpose: Track when compression was last applied
- Used for: Drift detection, re-compression scheduling

**baseline_tokens**
- Format: Positive integer
- Example: `1234`
- Purpose: Token count after compression
- Used for: Size tracking, efficiency metrics

**parameters**
- Format: Object with σ, γ, κ values
- Example: `{σ: 0.8, γ: 0.6, κ: 0.2}`
- Purpose: Record actual compression parameters used
- Used for: Consistency checking, re-compression

**validation**
- Format: Object with preservation metrics
- Required fields: `entity_preservation`, `semantic_similarity`
- Range: 0.0-1.0 for both metrics
- Purpose: Quality assessment of compression

#### Validation Metrics

**entity_preservation**
- Measures: Percentage of key entities preserved
- Range: 0.0 (none preserved) to 1.0 (all preserved)
- Typical good value: 0.90+ (90%+ entities preserved)
- Calculation: (entities_after / entities_before)

**semantic_similarity**
- Measures: Semantic similarity between original and compressed
- Range: 0.0 (completely different) to 1.0 (identical meaning)
- Typical good value: 0.80+ (80%+ semantic similarity)
- Calculation: Cosine similarity of embeddings

#### Drift Detection

Compare current document state with compression baseline:

```python
# Example drift detection logic
current_tokens = count_tokens(document)
baseline_tokens = header['compression']['baseline_tokens']
drift_ratio = current_tokens / baseline_tokens

if drift_ratio > 1.20:  # 20% growth
    print("Document has grown significantly, consider re-compression")
```

---

### Writing Guidance (writing_guide)

**Required**: No (optional)
**Format**: Multi-line text object
**Purpose**: Provide context-specific writing advice

#### Field Structure

```yaml
writing_guide:
  preferred_patterns: |
    ✓ Bullet lists for parameters/returns
    ✓ Code examples inline
    ✓ HTTP status codes explicit
  anti_patterns: |
    ✗ Prose explanations
    ✗ Redundant descriptions
    ✗ Excessive scaffolding
```

#### When to Include

**Always include for:**
- New document types
- Documents with specific style requirements
- Documents that will be collaboratively edited
- Template documents

**Consider including for:**
- Documents with unusual (σ, γ, κ) combinations
- Documents targeting specific audiences
- Documents with strict formatting requirements

**Usually skip for:**
- Standard document types with well-known patterns
- Simple documents with obvious formatting
- Personal working documents

#### Content Guidelines

**preferred_patterns**
- List specific techniques that work well
- Include format examples where helpful
- Focus on actionable guidance
- Use ✓ checkmarks for visual clarity

**anti_patterns**
- Identify common mistakes to avoid
- Explain why patterns are problematic
- Provide alternative approaches
- Use ✗ marks for visual clarity

#### Examples by Document Type

**API Reference**
```yaml
writing_guide:
  preferred_patterns: |
    ✓ Consistent endpoint format (METHOD /path)
    ✓ Parameter tables with types
    ✓ HTTP status codes with meanings
    ✓ Request/response examples
  anti_patterns: |
    ✗ Lengthy prose descriptions
    ✗ Mixing reference with tutorial content
    ✗ Inconsistent formatting across endpoints
```

**Tutorial**
```yaml
writing_guide:
  preferred_patterns: |
    ✓ Step-by-step numbered instructions
    ✓ Clear learning objectives
    ✓ Hands-on examples with expected outputs
    ✓ Troubleshooting sections
  anti_patterns: |
    ✗ Assuming prior knowledge without stating
    ✗ Skipping intermediate steps
    ✗ Using jargon without explanation
```

---

## Document Type Guide

This section provides complete examples for all supported document types, showing recommended headers and content patterns.

### API Reference

**Purpose**: Document API endpoints, parameters, and responses
**Audience**: Usually `llm-only` or `human-technical`
**Typical Parameters**: High σ (structured), moderate γ (essential details), low κ (minimal context)

```yaml
---
doc_type: API_REFERENCE
audience: llm-only
layer: Operational
phase: Complete
purpose: Reference

target_style:
  sigma: 0.8
  gamma: 0.6
  kappa: 0.2

compression:
  last_full_compression: 2025-10-31 14:30 AEDT
  baseline_tokens: 450
  parameters: {σ: 0.8, γ: 0.6, κ: 0.2}
  validation:
    entity_preservation: 0.96
    semantic_similarity: 0.89

writing_guide:
  preferred_patterns: |
    ✓ Bullet lists for parameters/returns
    ✓ Code examples inline
    ✓ HTTP status codes explicit
  anti_patterns: |
    ✗ Prose explanations
    ✗ Redundant descriptions
    ✗ Excessive scaffolding
---

# API Reference

## POST /auth
- Body: `{username, password}`
- Returns: `{token}` (200) | `{error}` (401)
- Headers: `Content-Type: application/json`

## GET /users
- Auth: Bearer token required
- Returns: User array
- Filters: `?role=admin&status=active`
```

### Tutorial

**Purpose**: Step-by-step learning content
**Audience**: Usually `human-general` or `human-technical`
**Typical Parameters**: Low σ (prose), high γ (full detail), high κ (full context)

```yaml
---
doc_type: TUTORIAL
audience: human-general
layer: Operational
phase: Active
purpose: Learning

target_style:
  sigma: 0.4
  gamma: 0.8
  kappa: 0.7

writing_guide:
  preferred_patterns: |
    ✓ Step-by-step instructions
    ✓ Explain the "why" behind each step
    ✓ Include troubleshooting tips
  anti_patterns: |
    ✗ Don't skip explanatory context
    ✗ Don't assume prior knowledge
    ✗ Don't use jargon without explanation
---

# Getting Started Tutorial

## Introduction

This tutorial walks you through setting up your first project. We'll cover
installation, configuration, and running your first example. By the end,
you'll understand the basic workflow and be ready to build your own applications.

## Step 1: Installation

First, you'll need to install the CLI tool. This tool provides commands for
creating projects, running tests, and deploying applications...
```

### Session Handover

**Purpose**: Transfer context between Claude sessions
**Audience**: Always `llm-only`
**Typical Parameters**: High σ (structured), high γ (good detail), low κ (minimal context)

```yaml
---
doc_type: SESSION_HANDOVER
audience: llm-only
layer: Session
phase: Active
purpose: Execution

target_style:
  sigma: 0.7
  gamma: 0.7
  kappa: 0.3

compression:
  last_full_compression: 2025-10-31 10:00 AEDT
  baseline_tokens: 350
  parameters: {σ: 0.7, γ: 0.7, κ: 0.3}
  validation:
    entity_preservation: 0.92
    semantic_similarity: 0.85

writing_guide:
  preferred_patterns: |
    ✓ Structured sections (WHERE/ACCOMPLISHED/NEXT)
    ✓ Bullet lists for tasks
    ✓ File paths explicit
  anti_patterns: |
    ✗ Narrative prose
    ✗ Redundant context
    ✗ Unnecessary elaboration
---

## Session Status: 2025-10-31 14:30 AEDT

### WHERE WE ARE
Phase 2 validation: Task 1.1 executing via Claude Code delegation

### ACCOMPLISHED THIS SESSION
- Session initialized, git status clean
- Task 1.1 delegated (content analyzer)
- Task 3.2 spec created

### NEXT ACTIONS
1. Monitor Task 1.1 completion
2. Delegate Task 2.3 when ready
3. Evaluate Phase 3 options

### BLOCKERS
None

### ACTIVE FILES
- SESSION.md (this file)
- claude-code-tasks/TASK_1.1_content_analyzer.md

### GIT STATE
On branch main, clean
```

### Project Context

**Purpose**: Strategic context and decision history
**Audience**: Usually `multi-role`
**Typical Parameters**: Moderate σ (mixed), high γ (full detail), moderate κ (essential context)

```yaml
---
doc_type: PROJECT_CONTEXT
audience: multi-role
layer: Strategic
phase: Active
purpose: Reference

target_style:
  sigma: 0.5
  gamma: 0.8
  kappa: 0.5

compression:
  last_full_compression: 2025-10-31 12:00 AEDT
  baseline_tokens: 2400
  parameters: {σ: 0.5, γ: 0.8, κ: 0.5}
  validation:
    entity_preservation: 0.94
    semantic_similarity: 0.88

writing_guide:
  preferred_patterns: |
    ✓ Strategic Context section (high-level overview)
    ✓ Decision log (chronological, detailed)
    ✓ Clear section headers
  anti_patterns: |
    ✗ Don't delete decision history
    ✗ Don't rewrite past decisions
    ✗ Don't bury key context deep in text
---

# Project Name

**Created**: 2025-10-29
**Last Strategic Update**: 2025-10-31

## Strategic Context

### Overview
Brief project description, current status, and key achievements.

### Current Status
**Phase**: Validation - 60% complete
- MVP validation complete (3/3 tasks)
- Phase 2 in progress (Task 1.1 executing)

### Core Principles
- Principle 1: Explanation
- Principle 2: Explanation
```

### Task Specification

**Purpose**: Autonomous task delegation for Claude Code
**Audience**: Always `llm-only`
**Typical Parameters**: Moderate σ (structured), very high γ (complete detail), moderate κ (essential context)

```yaml
---
doc_type: TASK_SPECIFICATION
audience: llm-only
layer: Operational
phase: Active
purpose: Execution

target_style:
  sigma: 0.6
  gamma: 0.9
  kappa: 0.6

writing_guide:
  preferred_patterns: |
    ✓ Comprehensive context (all details needed)
    ✓ TDD approach (tests first)
    ✓ Checkpoint system (incremental validation)
    ✓ Concrete examples with expected outputs
  anti_patterns: |
    ✗ Don't assume context known
    ✗ Don't leave ambiguity
    ✗ Don't skip edge cases
---

# Claude Code Task: [Task Name]

**Task ID**: TASK-X.X-NAME
**Priority**: HIGH
**Estimated Time**: 4-6 hours
**Dependencies**: [List dependencies]

## Project Context
[Full background needed for autonomous execution]

## Objective
[Clear statement of what to build]

## TDD Approach
[Three phases with checkpoints]

## Test Cases
[Concrete examples with expected results]
```

### Validation Report

**Purpose**: Test results and validation findings
**Audience**: Usually `multi-role`
**Typical Parameters**: Moderate σ (structured), high γ (detailed results), moderate κ (essential context)

```yaml
---
doc_type: VALIDATION_REPORT
audience: multi-role
layer: Operational
phase: Complete
purpose: Audit

target_style:
  sigma: 0.6
  gamma: 0.8
  kappa: 0.4

writing_guide:
  preferred_patterns: |
    ✓ Summary upfront
    ✓ Test results table
    ✓ Metrics with units
    ✓ Clear pass/fail status
  anti_patterns: |
    ✗ Don't bury conclusions
    ✗ Don't skip test numbers
    ✗ Don't omit edge cases
---

# Validation Report: [Task Name]

**Date**: 2025-10-31
**Task**: TASK-X.X
**Status**: PASS

## Summary
[Overview of validation results]

## Test Results

| Test | Expected | Actual | Status |
|------|----------|--------|--------|
| Test 1 | X | X | ✓ PASS |
| Test 2 | Y | Y | ✓ PASS |

## Conclusions
[Key findings and recommendations]
```

### Analysis Document

**Purpose**: Research findings and detailed analysis
**Audience**: Usually `multi-role`
**Typical Parameters**: Moderate σ (mixed), high γ (detailed findings), moderate κ (essential context)

```yaml
---
doc_type: ANALYSIS
audience: multi-role
layer: Operational
phase: Complete
purpose: Reference

target_style:
  sigma: 0.5
  gamma: 0.8
  kappa: 0.5

compression:
  last_full_compression: 2025-10-31 11:00 AEDT
  baseline_tokens: 1800
  parameters: {σ: 0.5, γ: 0.8, κ: 0.5}
  validation:
    entity_preservation: 0.91
    semantic_similarity: 0.84
---

# Analysis: [Topic]

**Created**: 2025-10-31
**Status**: Complete

## Executive Summary
[Key findings in 2-3 sentences]

## Methodology
Research approach and data sources used.

## Findings
Detailed analysis organized by theme.

## Conclusions
Implications and recommendations.
```

### Research Document

**Purpose**: Literature review and external research
**Audience**: Usually `multi-role`
**Typical Parameters**: Low σ (prose), very high γ (comprehensive), moderate κ (good context)

```yaml
---
doc_type: RESEARCH
audience: multi-role
layer: Operational
phase: Complete
purpose: Learning

target_style:
  sigma: 0.4
  gamma: 0.9
  kappa: 0.6
---

# Research: [Topic]

**Created**: 2025-10-31
**Sources**: 40+ academic papers reviewed

## Research Question
What dimensions are necessary for compression parameter model?

## Literature Review
Comprehensive review of information theory, cognitive science, and
software engineering literature relevant to compression.

### Information Theory
[Detailed findings with citations]

### Cognitive Science
[Detailed findings with citations]

## Conclusions
Research supports 3D model completeness for project-scale documentation.
```

### Plan Document

**Purpose**: Implementation plans and roadmaps
**Audience**: Usually `multi-role`
**Typical Parameters**: Moderate σ (structured), high γ (detailed steps), moderate κ (essential context)

```yaml
---
doc_type: PLAN
audience: multi-role
layer: Operational
phase: Active
purpose: Planning

target_style:
  sigma: 0.6
  gamma: 0.7
  kappa: 0.4
---

# Implementation Plan: [Feature]

**Created**: 2025-10-31
**Timeline**: 4 weeks
**Status**: In Progress

## Overview
High-level summary of implementation approach.

## Phases

### Phase 1: Foundation (Week 1)
- Task 1: Description
- Task 2: Description

### Phase 2: Integration (Week 2)
- Task 3: Description
- Task 4: Description

## Dependencies
Critical path and blockers identified.

## Success Metrics
How we'll measure completion.
```

### Reference Guide

**Purpose**: Quick reference guides and lookup tables
**Audience**: Usually `llm-only` or `human-technical`
**Typical Parameters**: Very high σ (data-like), moderate γ (essential info), very low κ (no context)

```yaml
---
doc_type: REFERENCE
audience: llm-only
layer: Operational
phase: Complete
purpose: Reference

target_style:
  sigma: 0.9
  gamma: 0.5
  kappa: 0.1

compression:
  last_full_compression: 2025-10-31 09:00 AEDT
  baseline_tokens: 280
  parameters: {σ: 0.9, γ: 0.5, κ: 0.1}
  validation:
    entity_preservation: 0.98
    semantic_similarity: 0.92
---

# Quick Reference: Git Commands

## Commit
`git add .` → `git commit -m "msg"` → `git push`

## Branch
- Create: `git checkout -b name`
- Switch: `git checkout name`
- Delete: `git branch -d name`

## Status
`git status` → changes
`git log -5` → recent commits
`git diff` → unstaged changes
```

### Pattern Document

**Purpose**: Reusable patterns and best practices
**Audience**: Usually `human-technical`
**Typical Parameters**: Moderate σ (structured), high γ (detailed explanation), moderate κ (good context)

```yaml
---
doc_type: PATTERN
audience: human-technical
layer: Strategic
phase: Complete
purpose: Reference

target_style:
  sigma: 0.6
  gamma: 0.8
  kappa: 0.4

writing_guide:
  preferred_patterns: |
    ✓ Clear problem/solution format
    ✓ Code examples with explanations
    ✓ When to use/avoid guidance
  anti_patterns: |
    ✗ Don't skip context of when to apply
    ✗ Don't provide patterns without examples
---

# Design Pattern: [Pattern Name]

## Problem
Description of the problem this pattern solves.

## Solution
How the pattern addresses the problem.

## Implementation
Code examples and best practices.

## When to Use
Specific scenarios where this pattern is beneficial.

## Alternatives
Other patterns or approaches to consider.
```

### Methodology Document

**Purpose**: Process documentation and frameworks
**Audience**: Usually `multi-role`
**Typical Parameters**: Moderate σ (mixed), high γ (detailed steps), moderate κ (good context)

```yaml
---
doc_type: METHODOLOGY
audience: multi-role
layer: Strategic
phase: Complete
purpose: Reference

target_style:
  sigma: 0.5
  gamma: 0.8
  kappa: 0.6

writing_guide:
  preferred_patterns: |
    ✓ Step-by-step process descriptions
    ✓ Clear roles and responsibilities
    ✓ Decision points and criteria
  anti_patterns: |
    ✗ Don't skip rationale for steps
    ✗ Don't assume process knowledge
---

# Methodology: [Process Name]

## Overview
Purpose and scope of this methodology.

## Process Steps

### Step 1: [Name]
**Objective**: What this step accomplishes
**Activities**: Specific tasks to complete
**Deliverables**: Expected outputs

### Step 2: [Name]
**Objective**: What this step accomplishes
**Activities**: Specific tasks to complete
**Deliverables**: Expected outputs

## Roles and Responsibilities
Who does what throughout the process.

## Quality Gates
How to validate each step was completed successfully.
```

### Proposal Document

**Purpose**: Design proposals and RFCs
**Audience**: Usually `human-technical` or `multi-role`
**Typical Parameters**: Moderate σ (mixed), high γ (detailed explanation), moderate κ (good context)

```yaml
---
doc_type: PROPOSAL
audience: human-technical
layer: Strategic
phase: Active
purpose: Planning

target_style:
  sigma: 0.5
  gamma: 0.8
  kappa: 0.6

writing_guide:
  preferred_patterns: |
    ✓ Executive summary upfront
    ✓ Clear problem statement
    ✓ Detailed technical approach
    ✓ Risk assessment and mitigation
  anti_patterns: |
    ✗ Don't bury the main proposal
    ✗ Don't skip implementation details
    ✗ Don't ignore potential downsides
---

# Proposal: [Feature/Change Name]

## Executive Summary
High-level overview of the proposal and expected impact.

## Problem Statement
What problem are we solving and why it matters.

## Proposed Solution
Detailed technical approach and implementation plan.

## Benefits
Expected positive outcomes and value delivery.

## Risks and Mitigation
Potential issues and how we'll address them.

## Implementation Timeline
Key milestones and resource requirements.

## Success Metrics
How we'll measure success and track progress.
```

---

## Validation Rules

### Required Field Validation

All headers must include these fields:

```yaml
# REQUIRED FIELDS
doc_type: [VALID_ENUM_VALUE]
audience: [VALID_ENUM_VALUE]
layer: [VALID_ENUM_VALUE]
phase: [VALID_ENUM_VALUE]
purpose: [VALID_ENUM_VALUE]
target_style:
  sigma: [0.0-1.0]
  gamma: [0.0-1.0]
  kappa: [0.0-1.0]
```

### Enum Value Validation

**doc_type** must be one of:
- `API_REFERENCE`, `TUTORIAL`, `SESSION_HANDOVER`, `PROJECT_CONTEXT`
- `TASK_SPECIFICATION`, `VALIDATION_REPORT`, `ANALYSIS`, `PLAN`
- `REFERENCE`, `PATTERN`, `METHODOLOGY`, `RESEARCH`, `PROPOSAL`

**audience** must be one of:
- `llm-only`, `human-technical`, `human-general`, `multi-role`

**layer** must be one of:
- `Session`, `Strategic`, `Control`, `Operational`, `Archive`

**phase** must be one of:
- `Active`, `Complete`, `Archived`, `Deprecated`

**purpose** must be one of:
- `Execution`, `Learning`, `Reference`, `Audit`, `Planning`, `Analysis`

### Parameter Range Validation

All target_style parameters must be in range [0.0, 1.0]:

```yaml
target_style:
  sigma: 0.0 <= value <= 1.0
  gamma: 0.0 <= value <= 1.0
  kappa: 0.0 <= value <= 1.0
```

### Compression Field Validation

If `compression` field is present, it must include all required subfields:

```yaml
compression:
  last_full_compression: "YYYY-MM-DD HH:MM TZ"  # Valid datetime with timezone
  baseline_tokens: [positive integer]            # > 0
  parameters: {σ: [0.0-1.0], γ: [0.0-1.0], κ: [0.0-1.0]}
  validation:
    entity_preservation: [0.0-1.0]
    semantic_similarity: [0.0-1.0]
```

### DateTime Format Validation

Compression timestamps must match pattern: `YYYY-MM-DD HH:MM TZ`

**Valid examples:**
- `2025-10-31 14:30 AEDT`
- `2025-12-01 09:15 UTC`
- `2025-06-15 16:45 PST`

**Invalid examples:**
- `2025-10-31` (missing time)
- `Oct 31, 2025 2:30pm` (wrong format)
- `2025-10-31T14:30:00Z` (ISO format not supported)

### YAML Structure Validation

Headers must be valid YAML frontmatter:

1. Start with `---` on first line
2. End with `---` on its own line
3. Valid YAML syntax between delimiters
4. No tabs (use spaces for indentation)
5. Consistent indentation (2 spaces recommended)

### Writing Guide Validation

If `writing_guide` is present, it must be an object with string values:

```yaml
writing_guide:
  preferred_patterns: |
    [Multi-line string content]
  anti_patterns: |
    [Multi-line string content]
```

---

## Usage Patterns

### Pattern 1: New Document Creation

When creating a new document:

1. **Identify Document Type**: Choose from the 13 supported types
2. **Determine Audience**: Who will read this document?
3. **Set Lifecycle Info**: Current phase and information layer
4. **Choose Parameters**: Based on document type and audience
5. **Add Writing Guide**: If document has specific requirements

```yaml
---
doc_type: TUTORIAL           # Step-by-step learning content
audience: human-general      # General audience needs explanation
layer: Operational          # Active work content
phase: Active               # Currently being written
purpose: Learning           # Educational content

target_style:
  sigma: 0.4                # Mixed prose/structure for readability
  gamma: 0.8                # Full detail for learning
  kappa: 0.7                # Full context for general audience
---
```

### Pattern 2: Document Compression Workflow

When compressing an existing document:

1. **Pre-compression**: Document has basic header (no compression field)
2. **Compression**: Apply compression using target_style parameters
3. **Post-compression**: Add compression tracking fields
4. **Validation**: Verify compression quality meets thresholds

```yaml
# Before compression
---
doc_type: SESSION_HANDOVER
audience: llm-only
# ... other fields
target_style: {sigma: 0.7, gamma: 0.7, kappa: 0.3}
---

# After compression (add tracking)
---
doc_type: SESSION_HANDOVER
audience: llm-only
# ... other fields
target_style: {sigma: 0.7, gamma: 0.7, kappa: 0.3}
compression:
  last_full_compression: 2025-10-31 14:30 AEDT
  baseline_tokens: 850
  parameters: {σ: 0.7, γ: 0.7, κ: 0.3}
  validation:
    entity_preservation: 0.95
    semantic_similarity: 0.88
---
```

### Pattern 3: Lifecycle Transitions

Update headers as documents progress through lifecycle:

```yaml
# Active document (being written)
phase: Active
target_style: {sigma: 0.5, gamma: 0.8, kappa: 0.6}  # Conservative compression

# Complete document (finished)
phase: Complete
target_style: {sigma: 0.6, gamma: 0.7, kappa: 0.4}  # Moderate compression

# Archived document (historical)
phase: Archived
target_style: {sigma: 0.7, gamma: 0.6, kappa: 0.3}  # Aggressive compression
```

### Pattern 4: Multi-Audience Documents

For documents serving both humans and LLMs:

```yaml
---
doc_type: PROJECT_CONTEXT
audience: multi-role          # Both humans and LLMs
layer: Strategic
phase: Active
purpose: Reference

target_style:
  sigma: 0.5                 # Balanced structure
  gamma: 0.8                 # Keep semantic detail
  kappa: 0.5                 # Moderate context (compromise)

writing_guide:
  preferred_patterns: |
    ✓ Executive summary for humans
    ✓ Structured data for LLMs
    ✓ Clear section headers
  anti_patterns: |
    ✗ Don't optimize for only one audience
    ✗ Don't use excessive jargon
---
```

### Pattern 5: Template Documents

For documents that serve as templates:

```yaml
---
doc_type: PATTERN
audience: human-technical
layer: Strategic
phase: Complete
purpose: Reference

target_style:
  sigma: 0.6                 # Structured for easy copying
  gamma: 0.8                 # Detailed explanations
  kappa: 0.4                 # Essential context only

writing_guide:
  preferred_patterns: |
    ✓ Copy-paste ready examples
    ✓ Clear placeholder markers
    ✓ Step-by-step instructions
  anti_patterns: |
    ✗ Don't embed project-specific details
    ✗ Don't skip example usage
---
```

### Pattern 6: Drift Detection and Re-compression

Monitor documents for content drift:

```python
# Pseudo-code for drift detection
def check_compression_drift(document_path):
    header = parse_header(document_path)
    if 'compression' not in header:
        return None

    current_tokens = count_tokens(document_path)
    baseline_tokens = header['compression']['baseline_tokens']

    drift_ratio = current_tokens / baseline_tokens

    if drift_ratio > 1.20:  # 20% growth threshold
        return "SIGNIFICANT_DRIFT"
    elif drift_ratio > 1.10:  # 10% growth threshold
        return "MODERATE_DRIFT"
    else:
        return "STABLE"
```

### Pattern 7: Batch Header Updates

For updating multiple documents:

```bash
# Find documents missing headers
find . -name "*.md" -exec grep -L "^---$" {} \;

# Find documents with old header versions
grep -r "doc_type: API" --include="*.md" .

# Validate all headers
python -m pytest tests/test_header_validation.py
```

---

## Migration Guide

### Adding Headers to Existing Documents

#### Step 1: Inventory Existing Documents

```bash
# Find all markdown files
find . -name "*.md" -type f

# Check which have headers
find . -name "*.md" -exec grep -l "^---$" {} \;

# Check which need headers
find . -name "*.md" -exec grep -L "^---$" {} \;
```

#### Step 2: Classify Document Types

For each document, determine:

1. **Content Type**: What kind of information does this contain?
   - API documentation → `API_REFERENCE`
   - Learning content → `TUTORIAL`
   - Project overview → `PROJECT_CONTEXT`
   - [See full type list](#document-type-doc_type)

2. **Target Audience**: Who reads this document?
   - Internal tooling docs → `llm-only`
   - Team technical docs → `human-technical`
   - User documentation → `human-general`
   - Cross-functional docs → `multi-role`

3. **Current Phase**: What's the document's state?
   - Actively updated → `Active`
   - Stable, occasional updates → `Complete`
   - Rarely accessed → `Archived`

#### Step 3: Add Headers Gradually

Start with high-impact documents:

1. **Session handovers** (immediate benefit for Claude)
2. **Task specifications** (critical for Claude Code)
3. **API references** (compression candidates)
4. **Project context** (strategic importance)
5. **Everything else** (comprehensive coverage)

#### Step 4: Use Templates

Create header templates for common types:

```yaml
# Template: api_reference_header.yml
---
doc_type: API_REFERENCE
audience: llm-only
layer: Operational
phase: Complete
purpose: Reference
target_style: {sigma: 0.8, gamma: 0.6, kappa: 0.2}
---

# Template: tutorial_header.yml
---
doc_type: TUTORIAL
audience: human-general
layer: Operational
phase: Active
purpose: Learning
target_style: {sigma: 0.4, gamma: 0.8, kappa: 0.7}
---
```

#### Step 5: Validate Headers

Run validation tests after adding headers:

```bash
# Run full validation suite
python3 -m pytest tests/test_header_validation.py -v

# Check specific document
python3 -c "
import yaml
from tests.test_header_validation import extract_yaml_header
content = open('YOUR_DOCUMENT.md').read()
header = extract_yaml_header(content)
parsed = yaml.safe_load(header)
print('Valid header' if parsed else 'No header found')
"
```

### Migration Strategies

#### Strategy 1: Big Bang Migration

**When to use**: Small projects (<50 documents)

1. Add headers to all documents in one session
2. Use templates for consistency
3. Run validation tests
4. Fix any validation errors

**Pros**: Complete consistency, single effort
**Cons**: Large upfront time investment

#### Strategy 2: Gradual Migration

**When to use**: Large projects (50+ documents)

1. **Week 1**: Add headers to critical documents (sessions, tasks)
2. **Week 2**: Add headers to frequently accessed documents
3. **Week 3**: Add headers to reference materials
4. **Week 4**: Add headers to remaining documents

**Pros**: Manageable effort, immediate benefits
**Cons**: Temporary inconsistency

#### Strategy 3: On-Demand Migration

**When to use**: Very large projects or legacy codebases

1. Add headers when documents are touched
2. Require headers for new documents
3. Gradually increase coverage over time

**Pros**: Minimal overhead, natural adoption
**Cons**: Slow coverage, potential inconsistency

### Common Migration Issues

#### Issue 1: Existing Frontmatter

Some documents already have YAML frontmatter:

```yaml
# Existing frontmatter
---
title: My Document
author: Team Name
---

# Solution: Merge with our fields
---
title: My Document
author: Team Name
doc_type: TUTORIAL
audience: human-general
layer: Operational
phase: Active
purpose: Learning
target_style: {sigma: 0.4, gamma: 0.8, kappa: 0.7}
---
```

#### Issue 2: Very Large Documents

For documents >10,000 tokens:

1. Consider splitting into multiple documents
2. Use more aggressive target_style parameters
3. Add compression tracking if compressing
4. Monitor for drift more frequently

#### Issue 3: Multi-Format Documents

For documents in multiple formats (markdown + PDF):

1. Add headers only to primary format (usually markdown)
2. Include note about format variants in writing_guide
3. Ensure header reflects content in all formats

#### Issue 4: Generated Documents

For auto-generated documentation:

1. Update generation templates to include headers
2. Use consistent headers for same document types
3. Consider `doc_type: API_REFERENCE` for API docs
4. Set `phase: Complete` for stable generated content

### Testing Migration Success

#### Validation Checklist

- [ ] All important documents have headers
- [ ] Headers parse as valid YAML
- [ ] All required fields present
- [ ] Enum values are valid
- [ ] Parameter ranges are correct
- [ ] Compression tracking complete (if applicable)
- [ ] Headers match document content
- [ ] Writing guides are helpful

#### Automated Testing

```bash
# Test all documents with headers
find . -name "*.md" -exec python3 -c "
import sys, yaml
from tests.test_header_validation import extract_yaml_header

content = open(sys.argv[1]).read()
header = extract_yaml_header(content)
if header:
    try:
        parsed = yaml.safe_load(header)
        print(f'{sys.argv[1]}: Valid')
    except Exception as e:
        print(f'{sys.argv[1]}: Error - {e}')
else:
    print(f'{sys.argv[1]}: No header')
" {} \;
```

#### Manual Review

1. **Content Alignment**: Do headers match document content?
2. **Parameter Appropriateness**: Are σ, γ, κ values reasonable?
3. **Audience Accuracy**: Does audience field match actual readers?
4. **Lifecycle Correctness**: Is phase field accurate?

---

## Examples Library

### Copy-Paste Templates

#### Basic Template (Most Documents)

```yaml
---
doc_type: [CHOOSE_TYPE]
audience: [CHOOSE_AUDIENCE]
layer: Operational
phase: Active
purpose: [CHOOSE_PURPOSE]

target_style:
  sigma: 0.5
  gamma: 0.7
  kappa: 0.5
---
```

#### LLM-Only Template

```yaml
---
doc_type: [CHOOSE_TYPE]
audience: llm-only
layer: [CHOOSE_LAYER]
phase: [CHOOSE_PHASE]
purpose: Execution

target_style:
  sigma: 0.7
  gamma: 0.7
  kappa: 0.3
---
```

#### Human Documentation Template

```yaml
---
doc_type: [CHOOSE_TYPE]
audience: human-technical
layer: Operational
phase: Active
purpose: [CHOOSE_PURPOSE]

target_style:
  sigma: 0.4
  gamma: 0.8
  kappa: 0.6
---
```

#### Compressed Document Template

```yaml
---
doc_type: [CHOOSE_TYPE]
audience: [CHOOSE_AUDIENCE]
layer: [CHOOSE_LAYER]
phase: Complete
purpose: [CHOOSE_PURPOSE]

target_style:
  sigma: [0.0-1.0]
  gamma: [0.0-1.0]
  kappa: [0.0-1.0]

compression:
  last_full_compression: [YYYY-MM-DD HH:MM TZ]
  baseline_tokens: [NUMBER]
  parameters: {σ: [VALUE], γ: [VALUE], κ: [VALUE]}
  validation:
    entity_preservation: [0.0-1.0]
    semantic_similarity: [0.0-1.0]
---
```

### Edge Case Examples

#### Multi-Role Strategic Document

```yaml
---
doc_type: PROJECT_CONTEXT
audience: multi-role
layer: Strategic
phase: Active
purpose: Reference

target_style:
  sigma: 0.5   # Balanced structure for both audiences
  gamma: 0.8   # Keep detailed information
  kappa: 0.5   # Moderate context (compromise)

writing_guide:
  preferred_patterns: |
    ✓ Executive summary for quick scanning
    ✓ Detailed sections for deep reading
    ✓ Clear headers for navigation
  anti_patterns: |
    ✗ Don't optimize for only humans or only LLMs
    ✗ Don't bury key information in paragraphs
---
```

#### Transitioning Document (Active → Archive)

```yaml
---
doc_type: ANALYSIS
audience: multi-role
layer: Operational
phase: Archived        # Recently transitioned
purpose: Reference

target_style:
  sigma: 0.7           # More structured after archival
  gamma: 0.6           # Reduced detail for space
  kappa: 0.3           # Less context needed

compression:
  last_full_compression: 2025-10-31 16:00 AEDT
  baseline_tokens: 1200
  parameters: {σ: 0.7, γ: 0.6, κ: 0.3}
  validation:
    entity_preservation: 0.89
    semantic_similarity: 0.81

writing_guide:
  preferred_patterns: |
    ✓ Preserve key findings and conclusions
    ✓ Keep methodology section intact
  anti_patterns: |
    ✗ Don't remove supporting evidence
    ✗ Don't compress executive summary
---
```

#### High-Compression Reference

```yaml
---
doc_type: REFERENCE
audience: llm-only
layer: Operational
phase: Complete
purpose: Reference

target_style:
  sigma: 0.9           # Highly structured (list/table format)
  gamma: 0.4           # Minimal detail (essential only)
  kappa: 0.1           # No explanatory context

compression:
  last_full_compression: 2025-10-31 08:00 AEDT
  baseline_tokens: 180
  parameters: {σ: 0.9, γ: 0.4, κ: 0.1}
  validation:
    entity_preservation: 0.98
    semantic_similarity: 0.94

writing_guide:
  preferred_patterns: |
    ✓ Bullet points and tables only
    ✓ Commands with minimal description
    ✓ No prose explanations
  anti_patterns: |
    ✗ Never add explanatory text
    ✗ Don't use full sentences
---
```

#### Tutorial with Comprehensive Context

```yaml
---
doc_type: TUTORIAL
audience: human-general
layer: Operational
phase: Active
purpose: Learning

target_style:
  sigma: 0.3           # Narrative prose format
  gamma: 0.9           # Maximum semantic detail
  kappa: 0.8           # Full explanatory scaffolding

writing_guide:
  preferred_patterns: |
    ✓ Learning objectives at start
    ✓ Step-by-step with explanations
    ✓ Examples and expected outputs
    ✓ Troubleshooting sections
    ✓ Summary and next steps
  anti_patterns: |
    ✗ Never skip intermediate steps
    ✗ Don't assume prior knowledge
    ✗ Don't use unexplained jargon
    ✗ Don't omit error scenarios
---
```

#### Session Handover with Minimal Context

```yaml
---
doc_type: SESSION_HANDOVER
audience: llm-only
layer: Session
phase: Active
purpose: Execution

target_style:
  sigma: 0.8           # Highly structured sections
  gamma: 0.8           # Complete task information
  kappa: 0.2           # Minimal scaffolding

writing_guide:
  preferred_patterns: |
    ✓ Standard sections: WHERE/ACCOMPLISHED/NEXT/BLOCKERS
    ✓ Bullet lists for all content
    ✓ Explicit file paths and git states
    ✓ Quantified progress where possible
  anti_patterns: |
    ✗ No narrative explanations
    ✗ No redundant context
    ✗ No motivational content
---
```

### Parameter Combinations Guide

#### High Structure (σ = 0.7-1.0)

Best for: References, APIs, checklists, structured data

```yaml
target_style: {sigma: 0.9, gamma: 0.5, kappa: 0.1}  # Pure data
target_style: {sigma: 0.8, gamma: 0.6, kappa: 0.2}  # API reference
target_style: {sigma: 0.7, gamma: 0.7, kappa: 0.3}  # Structured guide
```

#### Balanced Structure (σ = 0.4-0.6)

Best for: Mixed content, project docs, moderate tutorials

```yaml
target_style: {sigma: 0.5, gamma: 0.8, kappa: 0.5}  # Balanced doc
target_style: {sigma: 0.4, gamma: 0.8, kappa: 0.7}  # Tutorial-leaning
target_style: {sigma: 0.6, gamma: 0.7, kappa: 0.4}  # Reference-leaning
```

#### Low Structure (σ = 0.0-0.3)

Best for: Prose, research, comprehensive explanations

```yaml
target_style: {sigma: 0.3, gamma: 0.9, kappa: 0.8}  # Rich tutorial
target_style: {sigma: 0.2, gamma: 0.9, kappa: 0.6}  # Research paper
target_style: {sigma: 0.1, gamma: 0.8, kappa: 0.7}  # Narrative guide
```

---

## Appendix

### Validation Test Suite

The complete validation test suite is available at `tests/test_header_validation.py`. Key tests include:

- **YAML Parsing**: All headers parse as valid YAML
- **Required Fields**: All mandatory fields present
- **Enum Validation**: Field values match specification
- **Range Validation**: Parameters within [0.0, 1.0]
- **Format Validation**: Timestamps match required pattern
- **Structure Validation**: Nested objects have correct format

### Tool Integration

Headers are designed to integrate with:

- **Compression Tools**: Use target_style for parameter selection
- **Claude Code**: Parse headers for document classification
- **Validation Systems**: Monitor compression quality and drift
- **Analytics**: Track document types and compression coverage

### Version History

- **v1.0** (2025-10-31): Initial specification with 13 document types and comprehensive validation

### Contributing

To propose changes to this specification:

1. Update validation tests first (TDD approach)
2. Add examples to fixtures directory
3. Update specification document
4. Run full validation suite
5. Submit for review

---

**End of Document Header Specification v1.0**