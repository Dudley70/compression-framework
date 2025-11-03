# Compression Framework Template Library

**Version**: 1.0
**Created**: 2025-11-03
**Purpose**: Pre-optimized document structures for common use cases with compression parameters built-in

---

## Overview

This template library provides 8 pre-optimized document structures that enable proactive compression. Each template includes:

1. **YAML frontmatter** specifying compression parameters (σ, γ, κ)
2. **Template structure** with section guidance
3. **Realistic example** demonstrating the compression style
4. **Clear use cases** for when to use each template

Instead of writing verbose and compressing afterward (reactive), select a template and write naturally in compressed form from the start (proactive). The parameters guide your writing style automatically.

---

## Quick Template Selection

### By Document Type

| Document Type | Template | σ | γ | κ | Best For |
|---|---|---|---|---|---|
| Status updates, progress reports | [high_compression_status.md](high_compression_status.md) | 0.8 | 0.4 | 0.2 | Quick summaries for busy readers |
| Design docs, architecture decisions | [medium_compression_design.md](medium_compression_design.md) | 0.6 | 0.6 | 0.4 | Technical documentation |
| Meeting notes, action items | [high_compression_notes.md](high_compression_notes.md) | 0.8 | 0.5 | 0.2 | Quick summaries of discussions |
| Research analysis, findings | [medium_compression_research.md](medium_compression_research.md) | 0.5 | 0.7 | 0.5 | Analysis and research documentation |
| Architecture decisions, ADRs | [decision_record.md](decision_record.md) | 0.5 | 0.7 | 0.6 | Formal decision documentation |
| API reference, command lookup | [quick_reference.md](quick_reference.md) | 0.9 | 0.3 | 0.1 | Rapid lookup by power users |
| Tutorials, onboarding, getting started | [educational_guide.md](educational_guide.md) | 0.4 | 0.9 | 0.8 | Learning for newcomers |
| Roadmaps, project plans, strategy | [planning_document.md](planning_document.md) | 0.6 | 0.6 | 0.5 | Strategic planning and roadmaps |

### By Compression Level

**High Compression** (σ ≥ 0.7, fast reading):
- [high_compression_status.md](high_compression_status.md) - Status updates
- [high_compression_notes.md](high_compression_notes.md) - Meeting notes

**Medium Compression** (0.4 ≤ σ < 0.7, balanced):
- [medium_compression_design.md](medium_compression_design.md) - Design documents
- [medium_compression_research.md](medium_compression_research.md) - Research findings
- [planning_document.md](planning_document.md) - Planning documents

**Low Compression** (σ < 0.4, narrative focus):
- [educational_guide.md](educational_guide.md) - Tutorials and onboarding

**Ultra-High Compression** (σ ≥ 0.9, power users):
- [quick_reference.md](quick_reference.md) - Quick reference guides

### By Audience

**LLM-Primary** (machine reading first):
- [high_compression_status.md](high_compression_status.md) - σ=0.8, γ=0.4, κ=0.2

**Dual Audience** (both humans and machines):
- [medium_compression_design.md](medium_compression_design.md) - σ=0.6, γ=0.6, κ=0.4
- [medium_compression_research.md](medium_compression_research.md) - σ=0.5, γ=0.7, κ=0.5
- [planning_document.md](planning_document.md) - σ=0.6, γ=0.6, κ=0.5

**Human-Primary** (newcomers):
- [educational_guide.md](educational_guide.md) - σ=0.4, γ=0.9, κ=0.8

**Power Users** (expert readers):
- [quick_reference.md](quick_reference.md) - σ=0.9, γ=0.3, κ=0.1

---

## Understanding Compression Parameters

### σ (Sigma) - Structure Density

Controls **how organized** the content is formatted.

- **Low (0.0-0.3)**: Flowing prose paragraphs, narrative style
- **Medium (0.4-0.6)**: Mix of prose and structure (bullets, lists, some tables)
- **High (0.7-1.0)**: Tables, YAML, lists, hierarchical format, minimal prose

**Example**:
- σ=0.8: "| Task | Status | ETA | \n|---|---|---|\n| Feature | 90% | Nov 15 |"
- σ=0.3: "Feature implementation is 90% complete with expected completion on November 15th..."

### γ (Gamma) - Granularity/Detail Level

Controls **how much information** is included.

- **Low (0.0-0.3)**: Keywords and abbreviations, minimal text
- **Medium (0.4-0.6)**: Concise sentences, key facts, essential context
- **High (0.7-1.0)**: Complete sentences, full detail, comprehensive explanations

**Example**:
- γ=0.4: "Status: ON TRACK | ETA: Nov 15 | Progress: 90%"
- γ=0.8: "The feature has been implemented and is approximately 90% complete. We expect to finish implementation by November 15th and move into quality assurance testing..."

### κ (Kappa) - Scaffolding/Context

Controls **how much explanation and background** is provided.

- **Low (0.0-0.3)**: Minimal headers, no explanations, assumes expertise
- **Medium (0.4-0.6)**: Basic headers, brief context, some reasoning
- **High (0.7-1.0)**: Full hierarchical headers, complete background, rationale explained

**Example**:
- κ=0.2: "Decision: Redis TTL-based caching"
- κ=0.8: "After analyzing database load patterns, we decided to implement Redis caching with TTL-based invalidation. This decision was made because: [full explanation with context]"

### Comprehension Constraint

All templates satisfy the comprehension constraint:

```
σ + γ + κ ≥ C_min(audience, phase)

Where C_min depends on audience type:
- LLM audience: C_min = 0.7 (can infer from less context)
- Human audience: C_min = 1.2 (needs more context)
- Dual audience: C_min = 1.0 (balanced)

And phase adjustments:
- Active: base value
- Complete: +0.1 (more context for future readers)
- Archived: +0.2 (maximum context for historical reference)
```

This ensures that reducing one dimension (e.g., less structure) requires increasing another (e.g., more detail or scaffolding). **Every template in this library satisfies its constraint.** ✓

---

## How to Use Templates

### 1. Select the Right Template
Use the quick selection tables above to find the template matching your document type and audience.

### 2. Copy the Template Structure
Each template file contains:
- A blank version with placeholders [like this]
- A complete example showing how it looks when filled in

Copy the blank version and customize the frontmatter parameters if needed.

### 3. Maintain Compression Throughout
Write content following the compression style indicated by your parameters:

- If σ is high (0.7+): Use tables, lists, minimal prose
- If γ is high (0.7+): Include complete details and explanations
- If κ is high (0.7+): Add section headers, context, rationale

The parameters guide your writing naturally. You're not forcing compression—you're writing in an efficient style that matches your needs.

### 4. Validate Your Document
After writing, check:
1. **Does format match σ?** (High σ should look structured, low σ should be prose)
2. **Does detail match γ?** (High γ should have full sentences, low γ just key facts)
3. **Does context match κ?** (High κ should have many headers and explanations, low κ minimal)

If something feels off, adjust the parameters and continue writing.

---

## Customizing Templates

### Adjusting Parameters
You can adjust parameters slightly to fit your specific needs. Key guidelines:

- **Stay within constraint**: σ + γ + κ ≥ C_min(audience, phase)
- **Keep consistency**: Maintain chosen parameters throughout document
- **Match audience**: Don't reduce context (κ) for human audiences below 0.3

**Example adjustment**:
```yaml
compression:
  sigma: 0.6  # Default: 0.8 (less structured for narrative)
  gamma: 0.6  # Default: 0.4 (more detail)
  kappa: 0.4  # Default: 0.2 (more context for new readers)
  audience: dual
```

### Adding/Removing Sections
Templates are starting points. Adapt structure as needed:

- Add sections that make sense for your content
- Remove sections that don't apply
- Keep the format consistent with your compression parameters

**Good**: Removing a metric column from a table
**Avoid**: Suddenly switching from tables (σ=0.8) to prose (σ=0.3) midway through

### Extending for Custom Needs
Templates can be extended with project-specific fields:

```yaml
compression:
  sigma: 0.6
  gamma: 0.6
  kappa: 0.4
  audience: dual
  tier: T2
  
  # Project-specific extensions
  project_id: COMP-2025
  stakeholders:
    - engineering
    - product
```

This flexibility allows templates to grow with your needs without losing compression benefits.

---

## Example: Selecting a Template

**Scenario**: "I need to write a status update for the team about our current progress"

**Decision Process**:
1. **Document type?** Status/progress → check Template Selection table
2. **Audience?** Team of engineers → LLM or dual
3. **Format preference?** Concise, structured → high σ
4. **Result**: high_compression_status.md matches perfectly

**Alternative scenario**: "I need to create onboarding documentation for new team members"

1. **Document type?** Onboarding → Getting started / educational
2. **Audience?** New users unfamiliar with domain → needs high κ and γ
3. **Format preference?** Flowing explanation → lower σ
4. **Result**: educational_guide.md matches

---

## Constraint Validation

Every template satisfies its compression constraint. Here's how:

| Template | σ | γ | κ | Sum | Audience | Min | ✓ |
|---|---|---|---|---|---|---|---|
| high_compression_status | 0.8 | 0.4 | 0.2 | 1.4 | LLM | 0.7 | ✓ |
| medium_compression_design | 0.6 | 0.6 | 0.4 | 1.6 | dual | 1.0 | ✓ |
| high_compression_notes | 0.8 | 0.5 | 0.2 | 1.5 | LLM | 0.7 | ✓ |
| medium_compression_research | 0.5 | 0.7 | 0.5 | 1.7 | dual | 1.0 | ✓ |
| decision_record | 0.5 | 0.7 | 0.6 | 1.8 | dual | 1.0 | ✓ |
| quick_reference | 0.9 | 0.3 | 0.1 | 1.3 | power-users | 0.7 | ✓ |
| educational_guide | 0.4 | 0.9 | 0.8 | 2.1 | new-users | 1.3 | ✓ |
| planning_document | 0.6 | 0.6 | 0.5 | 1.7 | dual | 1.0 | ✓ |

All templates satisfy their respective constraints. ✓

---

## Common Questions

**Q: What if I need a compression level not covered by these templates?**
A: These 8 templates cover ~80% of typical documentation needs. For specialized cases:
1. Start with the closest template
2. Adjust (σ, γ, κ) within your constraint
3. Adapt the structure to your needs
4. Validate constraint satisfaction

**Q: Can I mix compression levels within a document?**
A: Keep compression consistent throughout. If you have sections needing different styles, consider splitting into separate documents each with appropriate compression.

**Q: What if my audience is mixed (some experts, some newcomers)?**
A: Use dual audience templates with higher κ (0.5+) to provide context for newcomers while keeping structure efficient for experts. Or create two versions (expert-focused vs. newcomer-friendly).

**Q: Should I always follow the template exactly?**
A: No. Templates are guides showing best practices for each compression style. Adapt them to your content while maintaining:
1. Compression parameters (σ, γ, κ)
2. Frontmatter with metadata
3. Overall structure matching parameters

**Q: How do I know if my compression is working?**
A: Ask: "Is this significantly shorter than it would be if I wrote it naturally?" If yes, it's working. Compare to an uncompressed version. If similar length, increase σ (more structure) or decrease γ (less detail).

---

## Template Files

- **[high_compression_status.md](high_compression_status.md)** - Status updates and progress reports
- **[medium_compression_design.md](medium_compression_design.md)** - Design documents and technical specs
- **[high_compression_notes.md](high_compression_notes.md)** - Meeting notes and action items
- **[medium_compression_research.md](medium_compression_research.md)** - Analysis and research documentation
- **[decision_record.md](decision_record.md)** - Architecture decisions and ADRs
- **[quick_reference.md](quick_reference.md)** - Quick reference and lookup guides
- **[educational_guide.md](educational_guide.md)** - Tutorials and onboarding materials
- **[planning_document.md](planning_document.md)** - Roadmaps and project plans

---

## Next Steps

1. **Choose your first template** from the selection table
2. **Copy the template structure** (use the blank version with placeholders)
3. **Customize frontmatter** (adjust σ, γ, κ if needed, keeping constraint satisfied)
4. **Write your content** following the compression style
5. **Validate** your document matches the parameters

---

## For More Information

- **Compression Framework**: See `/docs/plans/PROACTIVE_SYSTEM_SPEC.md` for complete theory and specification
- **Quick Reference**: See [quick_reference.md](quick_reference.md) for condensed parameter guide and tables
- **Theory Background**: Parameter definitions and comprehension constraint in specification Section 2

---

**Template Library Version**: 1.0
**Last Updated**: 2025-11-03
**Status**: Production-ready
