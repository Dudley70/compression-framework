# Proactive Compression System Specification

**Version**: 1.0
**Date**: 2025-11-01
**Status**: Specification for Phase 2 Implementation

---

## 1. System Overview

### Architecture

The proactive compression system integrates three core components:

1. **Frontmatter Standard**: YAML metadata in document headers specifying (σ,γ,κ) compression parameters
2. **Template Library**: Pre-optimized document structures for common use cases, with compression-efficient layouts
3. **Claude Skill**: AI integration that reads frontmatter parameters and maintains compressed writing style throughout document creation and editing

**System Flow**:
```
User selects template
    ↓
Template provides frontmatter with (σ,γ,κ) parameters
    ↓
Claude Skill reads parameters
    ↓
Claude writes/edits natively in compressed form
    ↓
Document maintains compression throughout lifecycle
    ↓
No post-processing or reactive compression needed
```

### Design Philosophy

**Paradigm Shift**: From reactive post-processing to proactive write-time compression

**Key Principles**:
- **Machine-First**: Compression parameters optimized for LLM comprehension, not human aesthetics
- **Write-Time Efficiency**: Compressed writing feels natural, not forced
- **Automatic Maintenance**: Compression preserved during edits without manual intervention
- **No Post-Processing**: Eliminate reactive compression/verbosity cycle
- **Information Preservation**: Constraint-based optimization ensures minimum comprehension threshold

**Core Insight**: Users don't want to compress existing verbose content (reactive) nearly as much as they want to write efficiently from the start (proactive). Templates + Skill eliminate the need for post-processing while improving writing experience.

### User Workflow

**Scenario 1: New Document Creation**
1. User identifies document type and compression need
2. Selects matching template from library (e.g., "Status Update - High Compression")
3. Template provides frontmatter with (σ,γ,κ) parameters and structural guidance
4. User writes content following template structure
5. Claude Skill automatically maintains compression level based on parameters
6. Document emerges naturally compressed, requires no post-processing

**Scenario 2: Document Editing**
1. User opens existing compressed document
2. Claude Skill reads frontmatter parameters
3. User adds new content or modifies existing sections
4. Skill maintains same compression parameters for new content
5. Skill preserves already-compressed sections (idempotent)
6. Document stays at target compression level without extra effort

**Scenario 3: Compression Level Adjustment**
1. User decides document needs different compression
2. Updates (σ,γ,κ) values in frontmatter
3. Claude Skill adapts writing style for subsequent edits
4. User can request recompression of entire document if needed
5. Reactive tool (compress.py) can handle bulk recompression if desired

---

## 2. Frontmatter Standard

### YAML Schema Definition

```yaml
---
compression:
  sigma: 0.6        # Structure density (0.0-1.0)
  gamma: 0.5        # Granularity/Detail (0.0-1.0)
  kappa: 0.3        # Scaffolding/Context (0.0-1.0)
  audience: dual    # LLM | human | dual
  tier: T2          # T1 (essential) | T2 (valuable) | T3 (enrichment)
  phase: active     # active | complete | archived
  template: status-high-compression  # Template identifier (optional)
  version: 1.0      # Framework version (optional)
  updated: 2025-11-01  # Last update date (optional)
---
```

### Parameter Specifications

**Sigma (σ) - Structure Density**

Ranges from pure prose (0.0) to pure structured data (1.0). Controls how content is formatted.

- **0.0-0.3 (Prose-Heavy)**
  - Format: Flowing paragraphs with minimal structure
  - Use case: Narrative, strategic context, explanations
  - Techniques: Active voice, concise sentences, coherent flow
  - Example: Executive summaries, strategic decisions, vision statements

- **0.4-0.6 (Mixed)**
  - Format: Paragraphs + bullet lists + simple tables
  - Use case: Technical documentation, analysis, specifications
  - Techniques: Key points in bullets, data in tables, prose for explanation
  - Example: Design documents, analysis reports, technical specs

- **0.7-1.0 (Structured)**
  - Format: Tables, YAML, lists, key-value pairs, minimal prose
  - Use case: Status updates, metrics, quick reference, configuration
  - Techniques: Structured lists, tables, hierarchical format, abbreviations
  - Example: Status updates, metrics dashboards, quick reference guides

**Gamma (γ) - Granularity/Detail Level**

Ranges from keywords only (0.0) to complete detail (1.0). Controls how much information is included.

- **0.0-0.3 (Low Granularity)**
  - Content: Keywords, abbreviations, minimal prose
  - Detail: Only core information, omit context
  - Use case: Power users familiar with domain, quick reference
  - Example: "Status: ON TRACK | Risk: MEDIUM | Progress: 60%" 

- **0.4-0.6 (Medium Granularity)**
  - Content: Concise sentences, key facts, essential context
  - Detail: Information sufficient for understanding without full background
  - Use case: Informed readers with domain knowledge
  - Example: "Feature complete. Ready for QA testing. Security review pending."

- **0.7-1.0 (High Granularity)**
  - Content: Complete sentences, full context, detailed explanations
  - Detail: Sufficient for readers unfamiliar with domain
  - Use case: General audience, onboarding, public documentation
  - Example: "The feature has been implemented and is ready for quality assurance testing. Security review of authentication changes is currently pending completion."

**Kappa (κ) - Scaffolding/Contextual Explanation**

Ranges from no context (0.0) to full explanation (1.0). Controls how much background and reasoning is provided.

- **0.0-0.3 (Minimal Scaffolding)**
  - Headers: None or minimal
  - Context: Assume shared knowledge, no explanation
  - Rationale: Not provided, decisions unexplained
  - Audience: Experts familiar with project context
  - Example: Document uses technical jargon without definition

- **0.4-0.6 (Moderate Scaffolding)**
  - Headers: Section headers provided, brief context
  - Context: Some background, context where needed
  - Rationale: High-level reasoning for decisions
  - Audience: Team members with domain knowledge
  - Example: Clear sections with headers, brief context on complex decisions

- **0.7-1.0 (Full Scaffolding)**
  - Headers: Full hierarchical headers, descriptive titles
  - Context: Complete background and context
  - Rationale: Full explanation of decisions and reasoning
  - Audience: Readers unfamiliar with project (onboarding, external)
  - Example: Every section explained, decisions justified, context provided

**Comprehension Constraint**

```
σ + γ + κ ≥ C_min(audience, phase)

Where C_min values:
- LLM audience: C_min = 0.7 (can infer from less scaffolding)
- Human audience: C_min = 1.2 (needs more context)
- Dual audience: C_min = 1.0 (balanced)
- Active phase: C_min = base value (normal requirements)
- Complete phase: +0.1 added (more context for future readers)
- Archived phase: +0.2 added (full context for historical reference)
```

**Interpretation**: The constraint ensures that reducing one dimension requires increasing another. For example:
- If you reduce σ (less structure), you must increase γ+κ (more detail or scaffolding)
- Highly technical content (low κ) needs higher γ (more granular detail)
- Sparse content (low γ) needs more κ (full scaffolding) to be understandable

### Metadata Fields

**Optional Fields** (for additional organization):

```yaml
compression:
  # ... required fields ...
  
  # Optional identifiers
  template: status-high-compression  # Template used
  version: 1.0                        # Document version
  
  # Optional tracking
  created: 2025-10-29                 # Creation date
  updated: 2025-11-01                 # Last update date
  author: dudley                      # Document owner
  
  # Optional categorization
  domain: engineering                 # Domain (engineering, pm, analysis, etc)
  scope: team                         # Audience scope (team, project, external)
  
  # Optional technique hints (for skill guidance)
  techniques:
    - structured_lists
    - hierarchical_structure
    - abbreviations
```

**Extension Points**: Projects can add custom fields without breaking framework:
```yaml
compression:
  # ... standard fields ...
  project_specific:
    priority: high
    stakeholders:
      - engineering
      - product
```

### Examples with Parameter Combinations

**Example 1: High Compression Status Update**
```yaml
---
compression:
  sigma: 0.8
  gamma: 0.4
  kappa: 0.2
  audience: LLM
  tier: T2
  phase: active
---

# Project Status - 2025-11-01

## Accomplished
- Feature A: QA complete ✓
- Feature B: 80% implementation
- Bug fixes: 12 resolved

## Blockers
- Platform limitation → Architecture Review needed
- Timeline: 3 days to resolution

## Next
- QA remaining features
- Security review
- Documentation update
```

**Constraint Check**: 0.8 + 0.4 + 0.2 = 1.4 ✓ (≥ 0.7 for LLM)

---

**Example 2: Medium Compression Technical Design**
```yaml
---
compression:
  sigma: 0.6
  gamma: 0.6
  kappa: 0.4
  audience: dual
  tier: T2
  phase: active
---

# Cache Layer Architecture

## Overview
Implement Redis caching layer to reduce database load by 60-70%. Targets high-frequency queries with cacheable results.

## Design Decision: Cache Invalidation Strategy

| Strategy | Hit Rate | Complexity | Chosen? |
|----------|----------|-----------|---------|
| TTL-based | 85% | Low | ✓ |
| Event-based | 92% | High | |
| Hybrid | 90% | Medium | Alternative |

**Rationale**: TTL balances 85% hit rate with manageable complexity. Event-based invalidation considered but adds maintenance burden. Team comfort with TTL approach preferred.

## Implementation Plan
...
```

**Constraint Check**: 0.6 + 0.6 + 0.4 = 1.6 ✓ (≥ 1.0 for dual)

---

**Example 3: Low Compression Strategic Narrative**
```yaml
---
compression:
  sigma: 0.3
  gamma: 0.8
  kappa: 0.7
  audience: human
  tier: T1
  phase: complete
---

# 2026 Product Vision and Strategic Direction

## Context: Market Landscape

The market for AI-powered document compression has grown significantly since our initial research began. However, adoption remains limited due to several key barriers:

1. **Integration Complexity**: Existing tools require significant configuration and setup, creating friction for new users.

2. **Unfamiliar Paradigms**: The compression parameters (σ, γ, κ) represent novel concepts requiring education and training.

3. **Limited Practical Patterns**: Users struggle to understand how to apply the framework to their specific domains and use cases.

## Our Response: Proactive Compression Methodology

Rather than continuing to focus exclusively on post-processing optimization (reactive compression), we identified through the CCM project integration that users need tools to write efficiently from the start...

[Full narrative with complete explanations]
```

**Constraint Check**: 0.3 + 0.8 + 0.7 = 1.8 ✓ (≥ 1.3 for human + complete phase)

---

## 3. Template Library Specification

### Template Selection Framework

Use this decision matrix to select the appropriate template:

**Primary Decision: Document Type**

| Document Type | Typical σ | Typical γ | Typical κ | Best Template |
|---|---|---|---|---|
| Status updates, metrics | 0.7-0.9 | 0.3-0.5 | 0.1-0.3 | High Compression Status |
| Design docs, technical specs | 0.5-0.7 | 0.5-0.7 | 0.3-0.5 | Medium Compression Technical |
| Analysis, findings, decisions | 0.4-0.6 | 0.6-0.8 | 0.4-0.6 | Analysis & Findings |
| Strategic narratives, vision | 0.2-0.4 | 0.7-0.9 | 0.6-0.8 | Strategic Narrative |
| Onboarding, tutorials | 0.3-0.5 | 0.8-1.0 | 0.7-0.9 | Educational Guide |
| Quick reference, lookup | 0.8-1.0 | 0.2-0.4 | 0.1-0.2 | Quick Reference |
| Meeting notes, summaries | 0.6-0.8 | 0.4-0.6 | 0.2-0.4 | Meeting Notes |
| Decision records, rationale | 0.5-0.7 | 0.6-0.8 | 0.5-0.7 | Decision Record |

---

### Template 1: High Compression Status Update

**Use Case**: Quick status reports, meeting notes, sprint summaries, progress tracking

**Parameters**: 
- σ = 0.8 (highly structured)
- γ = 0.4 (concise facts)
- κ = 0.2 (minimal context)
- audience = LLM-primary
- tier = T2

**Structure**:
```markdown
---
compression: {sigma: 0.8, gamma: 0.4, kappa: 0.2, audience: LLM, tier: T2, template: status-high-compression}
---

# [Project/Team] Status - [Date]

## Accomplished
- [x] Task - outcome (impact if significant)
- [x] Task - outcome
- [x] Task - outcome

## In Progress
- [ ] Task - target (ETA)
- [ ] Task - target (ETA)

## Blocked
- [ ] Task - blocker (resolution ETA)

## Metrics
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Key metric 1 | value | target | ✓ or ✗ |
| Key metric 2 | value | target | ✓ or ✗ |

## Next Sprint
- Task priority 1
- Task priority 2
- Task priority 3
```

**Key Principles**:
- Use checkboxes for task tracking
- Include outcomes, not just activities
- Quantify impact when significant
- Table format for metrics
- No explanatory prose

**Example Content**:
```markdown
---
compression: {sigma: 0.8, gamma: 0.4, kappa: 0.2, audience: LLM, tier: T2, template: status-high-compression}
---

# Compression Framework Status - 2025-11-01

## Accomplished
- [x] Paradigm shift analysis - identified proactive + reactive model
- [x] Strategic planning - 4 decision documents created
- [x] Task specifications - TASK-1B through 1E complete
- [x] Intrinsic stability validation - 96.7% convergence confirmed

## In Progress
- [ ] Implementation planning (TASK-1E in progress)
- [ ] Framework restructuring (deferred)

## Blocked
None

## Metrics
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Documentation | 15.3K lines | 20K lines | 76% |
| Task specifications | 4 complete | 4 complete | ✓ |
| Phase 1 completion | 80% | 100% | On track |

## Next
- Phase 1B-E specification creation
- Phase 2 preparation
- Delegate implementation tasks
```

---

### Template 2: Medium Compression Technical Design

**Use Case**: Architecture decisions, design documents, API specifications, technical proposals

**Parameters**:
- σ = 0.6 (mixed structure)
- γ = 0.6 (detailed facts)
- κ = 0.4 (moderate context)
- audience = dual
- tier = T2

**Structure**:
```markdown
---
compression: {sigma: 0.6, gamma: 0.6, kappa: 0.4, audience: dual, tier: T2, template: technical-design}
---

# [System/Feature] Design Document

## Problem Statement
[What problem does this solve? Why is it important?]

## Design Overview
High-level explanation with architecture diagram if needed.

## Technical Approach

### Option A: [Approach Name]
**Pros**: [list]
**Cons**: [list]
**Complexity**: [low/medium/high]

### Option B: [Approach Name]
**Pros**: [list]
**Cons**: [list]
**Complexity**: [low/medium/high]

**Selected**: Option [X] because [key rationale]

## Implementation Details

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| X | Y | Why chosen |

## Tradeoffs
[What are we giving up? What are we optimizing for?]

## Validation Strategy
[How will we verify this works?]

## Future Considerations
[What might change? How to extend?]
```

**Key Principles**:
- Decision focused (make choice explicit)
- Tradeoff analysis (what are we optimizing)
- Both options presented fairly
- Technical depth justified
- Validation approach clear

---

### Template 3: Analysis & Findings

**Use Case**: Research findings, competitive analysis, metrics analysis, problem analysis

**Parameters**:
- σ = 0.5 (mixed structure)
- γ = 0.7 (detailed findings)
- κ = 0.5 (moderate scaffolding)
- audience = dual
- tier = T2

**Structure**:
```markdown
---
compression: {sigma: 0.5, gamma: 0.7, kappa: 0.5, audience: dual, tier: T2, template: analysis}
---

# [Analysis Topic] Analysis & Findings

## Executive Summary
[Key findings in 3-5 bullets]

## Research Question
What are we trying to understand?

## Methodology
[How did we gather data? What's our approach?]

## Findings

### Finding 1: [Concise Finding Title]
**Data**: [Evidence supporting this finding]

| Factor | Value | Significance |
|--------|-------|-------------|
| X | Y | Why matters |

**Implication**: [What does this mean for our decisions?]

### Finding 2: [Concise Finding Title]
[Continue pattern]

## Recommendations
1. [Action] - because [evidence from findings]
2. [Action] - because [evidence from findings]

## Limitations & Caveats
[What might invalidate these findings?]

## Next Steps
[Follow-up research needed]
```

---

### Template 4: Meeting Notes

**Use Case**: Team meetings, standup notes, sync summaries, decision meetings

**Parameters**:
- σ = 0.7 (structured)
- γ = 0.5 (concise facts)
- κ = 0.3 (minimal context)
- audience = team
- tier = T2

**Structure**:
```markdown
---
compression: {sigma: 0.7, gamma: 0.5, kappa: 0.3, audience: team, tier: T2, template: meeting-notes}
---

# [Team/Project] Meeting - [Date] - [Duration]

**Attendees**: [Names]
**Decisions**: [Count of decisions made]
**Actions**: [Count of open actions]

## Decisions Made
- **Decision 1**: [Decision with rationale] → Owner: [Person]
- **Decision 2**: [Decision with rationale] → Owner: [Person]

## Action Items
- [ ] Action - Owner @person (due date)
- [ ] Action - Owner @person (due date)

## Key Discussion Points
- Topic 1: [1-2 sentence summary]
- Topic 2: [1-2 sentence summary]

## Blockers
[If any]

## Next Meeting
[Date, time, agenda preview]
```

---

### Template 5: Decision Record

**Use Case**: Architecture decisions, strategic choices, policy decisions, trade-off analysis

**Parameters**:
- σ = 0.5 (mixed)
- γ = 0.7 (detailed)
- κ = 0.6 (good scaffolding)
- audience = dual
- tier = T1

**Structure**:
```markdown
---
compression: {sigma: 0.5, gamma: 0.7, kappa: 0.6, audience: dual, tier: T1, template: decision-record}
---

# ADR-[Number]: [Decision Title]

**Date**: [When made]
**Status**: [Proposed/Accepted/Superseded]
**Context**: [Decision #N from PROJECT.md] (if applicable)

## Context
[What circumstances led to this decision? What problem are we solving?]

## Decision
[What did we decide to do?]

## Rationale
[Why did we choose this over alternatives?]

## Alternatives Considered

### Option A: [Alternative]
- Pros: [list]
- Cons: [list]

### Option B: [Alternative]
- Pros: [list]
- Cons: [list]

## Consequences
**Positive**: [Benefits of this decision]
**Negative**: [Drawbacks or tradeoffs]
**Risks**: [What could go wrong?]

## Related Decisions
- [Link to related ADR or decision]

## Notes
[Any additional context or implementation notes]
```

---

### Template 6: Quick Reference Guide

**Use Case**: Quick lookup, API reference, command checklists, rapid access

**Parameters**:
- σ = 0.9 (highly structured)
- γ = 0.3 (minimal detail)
- κ = 0.1 (no context)
- audience = power-users
- tier = T2

**Structure**:
```markdown
---
compression: {sigma: 0.9, gamma: 0.3, kappa: 0.1, audience: power-users, tier: T2, template: quick-reference}
---

# [Topic] Quick Reference

## [Category 1]
| Item | Value | Notes |
|------|-------|-------|
| X | Y | Z |

## [Category 2]
```
Code or config format
```

## Commands
- `command args` - description
- `command args` - description

## Common Patterns
```
Pattern with code
```
```

---

### Template 7: Educational Guide

**Use Case**: Onboarding, tutorials, getting started, learning materials

**Parameters**:
- σ = 0.4 (prose + structure)
- γ = 0.9 (detailed)
- κ = 0.8 (full scaffolding)
- audience = new users
- tier = T1

**Structure**:
```markdown
---
compression: {sigma: 0.4, gamma: 0.9, kappa: 0.8, audience: new-users, tier: T1, template: educational}
---

# [Topic] Getting Started

## What is [Topic]?
[Introduction explaining concept clearly for newcomers]

## Why Does This Matter?
[Practical examples of why someone should care]

## Prerequisites
- [What you should know before starting]
- [Tools you need installed]

## Step 1: [First Learning Objective]

[Explain concept clearly with examples]

```
code example
```

[Explain what the example shows and why it matters]

## Step 2: [Next Learning Objective]
[Continue with progressive disclosure]

## Common Questions
**Q**: [Question]
**A**: [Answer with context]

## Next Steps
[What to learn next]

## Troubleshooting
**Issue**: [Symptom]
**Solution**: [How to fix]
```

---

### Template 8: Strategic Narrative

**Use Case**: Vision statements, strategic plans, long-term direction, organizational context

**Parameters**:
- σ = 0.3 (prose-heavy)
- γ = 0.8 (detailed)
- κ = 0.7 (full context)
- audience = human
- tier = T1

**Structure**:
```markdown
---
compression: {sigma: 0.3, gamma: 0.8, kappa: 0.7, audience: human, tier: T1, template: strategic}
---

# [Strategic Topic]: Vision and Direction

## Context: Where We Are Today
[Narrative explaining current state, how we got here, market conditions]

## Challenge: What's Changing
[Forces requiring new direction]

## Opportunity: What We Could Become
[Positive vision for future state]

## Our Approach: How We'll Get There
[Strategy and key initiatives]

## Impact: What Success Looks Like
[Outcomes and metrics for success]

## Commitment: What We're Asking
[Time, resources, effort required from team]
```

---

### Template Usage Guidelines

**Selecting a Template**:
1. Identify document type from decision matrix above
2. Check parameters match your needs
3. If close but not exact, adjust (σ,γ,κ) slightly
4. Keep within comprehension constraint: σ + γ + κ ≥ C_min

**Customizing Templates**:
- Add or remove sections as needed
- Keep structure, adapt content
- Maintain compression parameters
- Don't drift toward verbosity

**Validation**:
- Does content match parameter style?
- Is structure used effectively?
- Is detail level appropriate?
- Is scaffolding sufficient?

---

## 4. Claude Skill Specification

### Skill Purpose

Read compression parameters from document frontmatter and maintain compressed writing style throughout document creation and editing. Enable users to write natively in compressed form without post-processing.

### Skill Behavior

**On Document Creation**:
1. Detect document with compression frontmatter
2. Read (σ,γ,κ) parameters from YAML metadata
3. Parse audience, tier, and phase metadata
4. Interpret parameters to determine:
   - What format and structure to use (σ)
   - How much detail to include (γ)
   - How much context to provide (κ)
5. Apply LSC techniques matching parameter interpretation
6. Generate content matching target compression level
7. Help user stay within comprehension constraint (σ + γ + κ ≥ C_min)

**During Editing**:
1. On each edit, detect compression parameters in frontmatter
2. Apply same parameters to new content
3. Preserve already-compressed sections (don't recompress)
4. Maintain consistency throughout document
5. Flag if new content drifts from target compression level
6. Suggest structural improvements matching template style

**Parameter Interpretation**:

When parameters change, skill adjusts approach:
```
User changes σ from 0.5 → 0.8:
- More structured format (tables, lists)
- Fewer prose paragraphs
- More hierarchical organization

User changes γ from 0.5 → 0.3:
- More concise
- Abbreviations acceptable
- Less explanatory text

User changes κ from 0.6 → 0.2:
- Fewer headers and explanations
- Assume more shared knowledge
- Skip background context
```

### Technique Mapping

**High Structure (σ ≥ 0.7)**
- Apply LSC techniques: structured_lists, hierarchical_structure, table_format, abbreviations
- Minimize prose paragraphs
- Use key-value format where possible
- Apply YAML/JSON structures where appropriate

**Medium Structure (0.4 ≤ σ < 0.7)**
- Mix prose paragraphs with structured elements
- Apply selective LSC techniques
- Use lists for key information
- Tables for comparative data
- Prose for explanation and context

**Low Structure (σ < 0.4)**
- Prose-heavy with compression principles
- Concise sentences, active voice
- Logical paragraph flow
- Minimal structural formatting
- Readability and narrative coherence prioritized

**High Granularity (γ ≥ 0.7)**
- Complete sentences with full detail
- Maintain information completeness
- Include relevant context
- Explain reasoning and implications

**Medium Granularity (0.4 ≤ γ < 0.7)**
- Concise facts and key information
- Omit obvious details
- Assume some shared knowledge
- Focus on novel or important information

**Low Granularity (γ < 0.4)**
- Keywords, abbreviations, minimal prose
- Maximum information density
- Only essential facts
- Trust reader to fill in obvious details

**High Scaffolding (κ ≥ 0.7)**
- Full hierarchical headers
- Section explanations
- Context before diving into details
- Rationale for decisions provided
- Suitable for readers unfamiliar with project

**Medium Scaffolding (0.4 ≤ κ < 0.7)**
- Basic section headers
- Brief context where needed
- Assume some project familiarity
- High-level reasoning for decisions

**Low Scaffolding (κ < 0.3)**
- Minimal headers or none
- No explanations, assume expertise
- Jump directly to content
- Suitable only for deeply familiar readers

### Writing Pattern Examples

**Example 1: Status Update (σ=0.8, γ=0.4, κ=0.2)**

Style characteristics:
- Format: Bullet points, tables, minimal prose
- Detail: Only outcomes and metrics
- Context: None, assume familiarity

Sample paragraph structure:
```markdown
## Feature Implementation Status

| Feature | Status | ETA | Blocker |
|---------|--------|-----|---------|
| Auth system | 85% | Nov 15 | None |
| API endpoints | 60% | Nov 20 | Testing framework |

## Metrics
- Tests written: 142/156 (91%)
- Coverage: 78% target → 82% current ✓
- Performance: Baseline established
```

Not like this (too verbose for σ=0.8):
```markdown
## Feature Implementation Status

We have been making good progress on feature implementation. 
The authentication system is approximately 85% complete with 
expected completion by November 15th. There are no blockers 
at this time for this work...
```

---

**Example 2: Technical Design (σ=0.6, γ=0.6, κ=0.4)**

Style characteristics:
- Format: Mix of prose and structure
- Detail: Key facts with some context
- Context: Brief explanations of decisions

Sample section:
```markdown
## Architecture Decision: Database Schema

We chose normalized PostgreSQL schema over denormalized approaches 
for three reasons:

1. **Data Integrity**: Enforced constraints prevent inconsistency
2. **Query Flexibility**: Support for complex queries without redesign
3. **Operational Experience**: Team expertise with PostgreSQL

Trade-off: Slightly higher query complexity compared to denormalized 
alternatives, but acceptable given operational benefits.

| Approach | Query Complexity | Maintenance | Chosen? |
|----------|-----------------|------------|---------|
| Normalized | Medium | Low | ✓ |
| Denormalized | Low | High | |
| Hybrid | Medium | Medium | Consider v2 |
```

---

**Example 3: Onboarding Guide (σ=0.3, γ=0.9, κ=0.8)**

Style characteristics:
- Format: Flowing prose with structured sections
- Detail: Complete explanations
- Context: Full background and reasoning

Sample section:
```markdown
## Understanding the Compression Framework

The Compression Framework helps you write documents that are both 
efficient (shorter, faster to read) and effective (still understandable 
and complete). It uses three parameters to define how to write:

**Structure (σ)**: How organized should the content be?
- High structure means using tables, lists, and clear organization
- Low structure means flowing prose paragraphs
- You pick the level based on what you're writing

For example, a status update benefits from high structure (tables 
with metrics), while a strategic vision benefits from lower structure 
(flowing narrative). There's no "correct" answer—it depends on your 
purpose.

**Granularity (γ)**: How much detail should you include?
- High granularity means complete sentences with full information
- Low granularity means just the key facts, assuming readers know context
- Again, it depends on your audience

If you're writing for experts who know the project, low granularity 
works fine. If you're writing onboarding material for new team members, 
high granularity is essential.

[Continue with Kappa and integration...]
```

---

### Skill Implementation Notes

**Location**: `/mnt/skills/public/compression/COMPRESSION.md` (proposed)

**Activation**: 
- Automatically triggered when document contains compression frontmatter
- Can be invoked explicitly with `@compression` or similar reference
- Works in document creation and editing modes

**Validation**:
- Check parameters are within valid ranges (0.0-1.0)
- Verify constraint satisfaction: σ + γ + κ ≥ C_min
- Flag if constraint violated, suggest adjustments
- Warn if parameters seem mismatched to template

**Limitations**:
- Cannot validate content quality objectively
- Requires human judgment for appropriateness
- Works best with clear templates
- May struggle with novel document types

**Integration with Templates**:
- Each template includes example frontmatter
- Skill reads frontmatter and confirms understanding
- User can edit parameters, skill adapts
- Examples demonstrate expected writing style

**Testing Strategy**:
1. Create test documents with different parameter combinations
2. Generate content with skill
3. Verify style matches parameters (manual review)
4. Test with users for naturalness
5. Refine technique mappings based on feedback

---

## 5. Integration Patterns

### End-to-End Workflow

**Workflow: New Document with Proactive Compression**

```
1. User identifies need: "I need to write a status update"
2. User selects template: "High Compression Status Update"
3. Template provides frontmatter:
   ---
   compression:
     sigma: 0.8
     gamma: 0.4
     kappa: 0.2
   ---
4. Claude Skill reads parameters and understands:
   - Use highly structured format (tables, lists)
   - Include only concise facts
   - Minimal context (assumes familiarity)
5. User types status content
6. Skill guides toward compressed style:
   - Suggests table format for metrics
   - Concise bullets for achievements
   - Abbreviations acceptable
7. Content emerges in compressed form
8. User edits as needed, skill maintains compression
9. No post-processing required
10. Document ready to share
```

**Workflow: Editing Existing Compressed Document**

```
1. User opens document with compression frontmatter
2. Skill detects parameters (σ=0.8, γ=0.4, κ=0.2)
3. User adds new section ("Blockers")
4. Skill automatically applies same compression level
5. New content emerges in matching style
6. Already-compressed sections untouched (idempotent)
7. Entire document maintains consistent compression
```

**Workflow: Adjusting Compression Level**

```
1. User realizes document needs more context
2. User updates kappa: 0.2 → 0.5
3. Skill adapts approach:
   - Adds more explanation
   - Includes brief context
   - Keeps structure (σ) unchanged
4. New edits follow updated parameters
5. Old content can be regenerated if needed
```

### Template → Skill → Document Integration

```
Template Selection
    ↓
[User chooses "Medium Compression Technical Design"]
    ↓
Frontmatter Generation
    ↓
[Template provides YAML with σ=0.6, γ=0.6, κ=0.4]
    ↓
Skill Activation
    ↓
[Skill reads parameters, loads technique mappings]
    ↓
Content Generation
    ↓
[User writes, skill maintains compressed style]
    ↓
Constraint Validation
    ↓
[Skill checks σ + γ + κ ≥ C_min(audience, phase)]
    ↓
Document Completion
    ↓
[No post-processing needed, document at target compression]
```

### Validation Strategy

**Pre-Delivery Validation**:
1. Parameters are valid (0.0-1.0 range)
2. Constraint satisfied (σ + γ + κ ≥ C_min)
3. Template matches document type
4. Examples demonstrate expected style

**During Use Validation**:
1. Manual review: Does content match parameters?
2. Style consistency: Is compression maintained through edits?
3. Constraint compliance: No drift beyond bounds
4. User feedback: Does it feel natural?

**Post-Delivery Validation** (with reactive tool):
1. Run compress.py with target parameters
2. Compare compression ratio
3. Verify no information loss
4. Check semantic similarity (should be high)

---

## 6. Implementation Dependencies

### Sequential Dependencies

**Blocking Chain**:

```
1. Frontmatter Standard ← BLOCKS EVERYTHING
   ├─ Cannot create templates without frontmatter spec
   ├─ Cannot implement skill without parameters
   ├─ Cannot validate system without standard
   └─ Must complete before any other work

2. Templates + Skill → Can develop in parallel (after frontmatter)
   ├─ Templates need frontmatter to provide metadata
   ├─ Skill needs frontmatter to read parameters
   ├─ Both need each other for testing
   └─ Should integrate early for validation

3. Integration Guide → Needs working system
   ├─ Requires templates complete
   ├─ Requires skill functional
   ├─ Cannot write guide without examples
   └─ Do last (synthesis work)
```

### Parallel Opportunities

**After Frontmatter Complete**:
```
Can happen simultaneously:
- Create Template 1-8
- Implement Claude Skill
- Build example documents
- Write integration patterns

Benefits:
- Skill team can start immediately
- Template team can work independently
- Examples generated during template creation
- Testing happens in parallel
```

### Context Requirements per Task

**Frontmatter Standard Design** (2-3 hours):
- Context needed: (σ,γ,κ) theory, constraint equation, framework decisions
- Context size: ~10-15K tokens
- Decision-heavy: Design tradeoffs explicit
- Delegable: Yes, with comprehensive spec

**Template Creation** (1 hour per template, 5-8 total):
- Context needed: Frontmatter standard, example content, LSC techniques
- Context size: ~15-20K tokens
- Implementation-heavy: Create working examples
- Delegable: Yes, templates are independent
- Can parallelize: Multiple templates simultaneously

**Claude Skill Implementation** (4-6 hours):
- Context needed: Frontmatter standard, templates, LSC technique mappings
- Context size: ~20-25K tokens
- Integration-heavy: Must work with templates
- Delegable: Yes, with clear technique mappings
- Requires: Tested during template creation

**Integration Guide** (8-12 hours):
- Context needed: All previous work, working system examples
- Context size: ~30-40K tokens
- Synthesis-heavy: Requires judgment and integration
- Delegable: Limited (needs human judgment)
- Requires: Templates + Skill working

---

## 7. Success Criteria

### Frontmatter Standard ✓ Complete When

- ✅ YAML schema defined completely
- ✅ All parameters documented with ranges and meanings
- ✅ Comprehension constraint specified and justified
- ✅ 3-5 examples provided showing different parameter combinations
- ✅ Constraint check performed on examples (σ + γ + κ ≥ C_min)
- ✅ Extension mechanism for custom fields documented
- ✅ Validated against framework theory
- ✅ Design decisions for edge cases made explicit

### Template Library ✓ Complete When

- ✅ 5-8 templates created for common use cases
- ✅ Each template has clear use case description
- ✅ Parameters mapped explicitly to document types
- ✅ Structure provided (not just descriptions)
- ✅ Realistic example content showing compression style
- ✅ Selection decision matrix helps users choose
- ✅ All examples satisfy constraint equation
- ✅ Templates tested with skill (style matches parameters)

### Claude Skill ✓ Complete When

- ✅ Reads frontmatter parameters correctly
- ✅ Generates content matching (σ,γ,κ) parameters
- ✅ Maintains compression during edits (idempotent)
- ✅ Technique mapping validated (σ/γ/κ ranges → LSC techniques)
- ✅ Examples demonstrate capability at different parameter levels
- ✅ Constraint validation working (flags violations)
- ✅ Tested with all templates
- ✅ Writing patterns feel natural (not forced)

### Integrated System ✓ Complete When

- ✅ Template selection works (users can pick correct template)
- ✅ Frontmatter → Skill → Document workflow functional
- ✅ Users can write compressed from start without post-processing
- ✅ Compression quality matches reactive tool output (validate with compress.py)
- ✅ Style consistency maintained across edits
- ✅ No adoption barriers removed (simple enough to start)
- ✅ Integration guide explains patterns clearly
- ✅ Real-world examples demonstrate system working

---

## 8. Design Decisions Needed

### Frontmatter Design

**Q1**: Should audience and tier be separate or combined into single field?
- Separate (current): More flexible, supports mixed scenarios
- Combined: Simpler, predefined pairs
- **Recommendation**: Keep separate (more flexible for future)

**Q2**: How to handle version evolution (v1 → v2 schema)?
- Add version field? (breaks existing docs)
- Backward compatible only? (limits evolution)
- Migration guide? (complex but necessary)
- **Recommendation**: Add optional version field, maintain backward compatibility

**Q3**: Should phase be part of compression or separate metadata?
- Current: Part of compression (affects constraint)
- Alternative: Separate metadata (doesn't affect writing)
- **Recommendation**: Keep as part of compression (affects context needs)

**Q4**: Default values when fields omitted?
- Strict validation (require all)
- Sensible defaults (σ=0.5, γ=0.5, κ=0.5)
- Infer from audience (audience → defaults)
- **Recommendation**: Sensible defaults for core parameters

### Templates Design

**Q5**: How many templates for v1.0? (5-8 recommended)
- Fewer (3-4): Essential templates only
- Standard (5-8): Cover 80% of use cases
- Comprehensive (15-20): Cover everything
- **Recommendation**: 5-8 for v1.0, expand v1.1 (allows iteration)

**Q6**: Should templates be copyable files or example structures?
- Files: Copy to project, customize
- Examples: Show in guide, users create
- Mixed: Core templates as files, others as examples
- **Recommendation**: Mixed (core 5 as files, advanced as examples)

**Q7**: How to organize templates?
- By document type: Status, Design, Analysis, etc.
- By compression level: High, Medium, Low
- By audience: LLM, Human, Dual
- **Recommendation**: By document type (intuitive), include compression level

**Q8**: Customization guidelines?
- Strict: "Don't modify template structure"
- Flexible: "Adapt as needed, keep compression"
- Progressive: "Ensure constraint still satisfied"
- **Recommendation**: Progressive (constraint is law, structure is guidance)

### Skill Design

**Q9**: How explicit should parameter interpretation be?
- Explicit rules: σ ≥ 0.7 means X, Y, Z
- Examples only: Show style for each range
- Adaptive: Learn from user edits
- **Recommendation**: Explicit rules + examples (clearer for consistency)

**Q10**: Should skill explain what it's doing or just do it?
- Silent: Apply compression naturally
- Explanatory: "Based on γ=0.6, I'm including moderate detail"
- Configurable: User chooses verbosity
- **Recommendation**: Silent + optional explain-on-request (natural experience)

**Q11**: How to handle edge cases (invalid parameters)?
- Reject: "Please fix parameters"
- Auto-correct: "Adjusting κ to satisfy constraint"
- Flag: "Warning: constraint not satisfied, proceeding anyway"
- **Recommendation**: Flag + suggest adjustment (user chooses)

**Q12**: Testing strategy for skill behavior?
- Manual review: Check style matches parameters
- Automated: Score generated content against technique rules
- User feedback: Does it feel natural?
- **Recommendation**: All three (comprehensive validation)

### Integration Design

**Q13**: Should templates include skill usage instructions?
- Embedded: Instructions in frontmatter comments
- Separate: Skill guide referenced separately
- Implicit: Templates show expected style
- **Recommendation**: Implicit + front-page reference (self-documenting)

**Q14**: How to onboard users to system?
- README: Theory-first explanation
- Quickstart: "Do this for your first document"
- Progressive: Start simple, reveal advanced features
- **Recommendation**: Progressive (lower barrier to entry)

**Q15**: Migration path from reactive to proactive?
- Separate systems: Reactive and proactive independent
- Bridge: Reactive tool reads/generates frontmatter
- Integrated: Single entry point for both
- **Recommendation**: Separate now, bridge in v1.1 (don't complicate v1.0)

---

## 9. Open Questions for Phase 2

These questions will be answered during Phase 2 implementation:

1. **Parameter Tuning**: Which (σ,γ,κ) combinations get used most often in practice?
2. **User Preference**: Do users prefer explicit parameters or preset templates?
3. **Customization**: How much flexibility do templates need vs. standardization?
4. **Quality Validation**: How to measure if compressed content matches parameters?
5. **Integration Adoption**: What barriers exist to using this methodology?
6. **Skill Naturalness**: Does compressed writing feel natural or forced?
7. **Template Library Size**: What's the right balance of templates (5 vs. 20)?
8. **Maintenance Burden**: How much work to keep templates current?
9. **Reactive Integration**: When do users need compress.py vs. skill?
10. **Performance**: Is skill activation automatic or opt-in?

---

## 10. References

### Framework Documentation
- `/docs/analysis/PARADIGM_SHIFT.md`: Paradigm shift explanation (reactive → proactive)
- `/docs/plans/PHASE_1_APPROACH.md`: Implementation strategy
- `/docs/plans/OPEN_QUESTIONS.md`: Strategic questions for replanning

### Theory Documentation
- `/docs/patterns/multi-dimensional-compression-matrix.md`: (σ,γ,κ) decision framework
- `/docs/reference/DOCUMENT_HEADER_SPECIFICATION.md`: Metadata specifications
- `PROJECT.md`: Decision #11 on intrinsic stability

### Implementation Tools
- `/compress.py`: Reactive compression tool (comparison baseline)
- `/docs/analysis/documentation-types-matrix.md`: Document type guidance
- `/docs/patterns/multi-role-document-strategies.md`: Role-based strategies

### Validation
- Empirical validation data from Task 4.1 FIX (compress.py validation)
- Convergence testing results from Task 5.1 (intrinsic stability)
- CCM project integration insights (paradigm shift validation)

---

## Bottom Line

**What This Spec Defines**: Complete proactive compression system architecture

**Key Components**:
1. Frontmatter Standard: Metadata specification for (σ,γ,κ) parameters
2. Template Library: 5-8 pre-optimized document structures
3. Claude Skill: AI integration maintaining compressed style
4. Integration Framework: How system components work together

**Critical Path**: Frontmatter → Templates + Skill (parallel) → Integration Guide

**MVP Definition**: Frontmatter + 5 core templates + skill with basic technique mappings

**Ready For**: Phase 2 implementation (specification complete, no more decisions needed)

**Expected Outcome**: Users write compressed documents from start, no post-processing needed

**Quality Standard**: System reduces barriers to compressed writing while maintaining information fidelity and constraint satisfaction

---

**Status**: Specification complete and ready for Phase 2 implementation

**Next Steps**: Create TASK-2A specification for Frontmatter Standard design, then delegate Phase 2 execution
