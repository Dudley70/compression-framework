# Documentation Index

**Last Updated**: 2025-10-30

## Active Documents

### Research

**[Context Compression Method](research/context-compression-method.md)** - Active - Conversational compression technique for verbose AI responses (99.5%+ compression ratios). Post-session retrospective compression using multi-tier strategy with structured JSON summaries. Source: CC_Projects analysis.

**[LSC Framework Overview](research/lsc/README.md)** - Active - Quick reference for LLM-Shorthand Context (LSC) compression framework. Achieves 70-85% token reduction for documentation through machine-first structured format.

**[LSC Complete Framework](research/lsc/LSC_CONTEXT_EFFICIENCY.md)** - Active - Comprehensive 3,247-line guide to LSC framework. Covers core principles, schema design, file-based implementation (70% reduction), retrieval-augmented future (85% reduction), universal interop, output contracts, migration strategies, and reference implementations.

### Analysis

**[Documentation Types Matrix](analysis/documentation-types-matrix.md)** - Active - Comprehensive taxonomy (1,691 lines, enhanced Session 4) defining six audience categories (LLM-only, hybrid-technical, hybrid-general, human-technical, human-general, archival) with specific compression targets (70-85%, 40-60%, 20-40%, 0-10%, 0%, 95-99%). Includes decision framework, comprehension requirements, and 7 example transformations. **NEW: Team-size scaling considerations** (solo/small/medium/large teams with role overlap analysis, compression target adjustments, ROI calculations showing token savings multiply with team size). **NEW: Edge cases and special scenarios** (5 critical scenarios: compliance/audit requirements with retention limits, emergency access needs requiring human-readable formats, multi-project shared documentation strategies, cross-organizational collaboration constraints, long-term archival with format longevity priorities, includes override priority decision tree).

**[Information Preservation Framework](analysis/information-preservation-framework.md)** - Active - Systematic framework (1,808 lines, enhanced Session 2) for purpose-driven compression. Comprehensive taxonomy of 7 documentation purposes (execution, learning, reference, audit, communication, analysis, maintenance) with essential information mapping, preservation decision matrices, 5 compression methods, validation framework, and systematic analysis process. **NEW: Phase-aware compression strategy** (6 phases from Research to Maintain with specific targets, anti-compression patterns, state lifecycle Active/Complete/Archive, phase transition strategies, "why not" preservation for Refinement). **NEW: ROI prioritization** (frequency-based targeting, session startup = highest impact, validation rigor scaling, decision rationale preservation, empirical tracking). Answers "what can be safely stripped" based on "why we're documenting" and "when in lifecycle."

**[CC_Projects Alignment Review](analysis/cc-projects-alignment-review.md)** - Active - Deep alignment analysis (756 lines) systematically validating Compression framework design against CC_Projects validated architecture. Maps 6 audience categories to H2 roles, validates 7 purposes against documentation needs, confirms compression targets for H3 layers, analyzes method support for H1 phase lifecycle. Identifies 6 critical gaps with HIGH priority refinements needed. Documents integration requirements, 5-session refinement plan, and framework readiness assessment. Result: Strong alignment with operational enhancements needed.

### Plans

**[CC_Projects Compression Tasks](plans/CC_PROJECTS_COMPRESSION_TASKS.md)** - Active - Structured 7-phase roadmap (270 lines) for systematically applying Compression framework to CC_Projects document types. Layer-by-layer approach (Session → Strategic → Control → Operational → Archive) with role-based optimization, phase-aware temporal compression, and framework refinement. Estimated 60-75 hours phased implementation.

### Proposals

### Reference

**[CC_Projects Validated Architecture](reference/CC_PROJECTS_VALIDATED_ARCHITECTURE.md)** - Active - Comprehensive reference (994 lines) documenting CC_Projects Phase 2 validation (H1-H4). Provides evidence-based architectural context grounding Compression framework: 5-phase lifecycle, 6 roles, 5 layers, scalability validation. Includes document type mapping, compression implications, concrete test cases, and integration recommendations.

### Prompts

### Patterns

**[Multi-Dimensional Compression Matrix](patterns/multi-dimensional-compression-matrix.md)** - Active - Comprehensive operationalization (1,343 lines) of [Role × Layer × Phase] compression decision framework. Addresses Gap 1 (HIGH priority) from alignment review. Provides base compression target matrix for all role-layer combinations, phase adjustment guidance, multi-role document strategies (Union/Intersection/Layered), conflict resolution process, mode-switching overhead considerations, 6 worked examples (SESSION.md, DECISIONS.md, TASKS.md, config files, archive, research), edge cases, integration with existing framework, practical application guide, validation approach, and best practices. Enables explicit, repeatable, evidence-based compression decisions.

**[Multi-Role Document Strategies](patterns/multi-role-document-strategies.md)** - Active - Comprehensive guide (1,208 lines) for optimizing documents serving multiple audience roles simultaneously. Addresses Gap 3 (HIGH priority, last HIGH priority gap) from alignment review. Provides systematic strategy selection framework: Union (<20% divergence), Intersection (20-40% divergence, primary role), Layered (>40% divergence, multiple representations). Includes divergence calculation methods, cost/benefit analysis for layered approaches, ROI formulas, break-even analysis, implementation templates (Progressive Detail, Role-Specific Views, Core+Extensions), validation and quality assurance processes, common scenarios (SESSION.md, PROJECT.md, TASKS.md, configs, archives, APIs, runbooks), best practices and anti-patterns, integration with Matrix and Framework. Completes operational foundation for multi-role optimization challenges.

**[Ultra-Aggressive Compression Methods](patterns/ultra-aggressive-compression.md)** - Active - Comprehensive guide (816 lines) for 95-99% compression techniques for archival and rarely-accessed documentation. Addresses Gap 5 (MEDIUM priority) from alignment review. Covers when ultra-aggressive compression appropriate (completed sessions, deprecated specs, old versions, verbose transcripts), conversational compression method (four-tier strategy: artifacts, decisions, milestones, dialogue - achieving 99.5% reduction), search-optimized compression (three-layer architecture, keyword selection strategies), reconstruction trade-offs (acceptable information loss, irreversible vs reversible compression, quality assessment tiers), archive lifecycle and transition strategy (Active → Complete → Archive → Ultra-Compressed), best practices and quality assurance (progressive compression, extract before compressing, maintain searchability, validation checklists). Includes detailed examples, anti-patterns, warnings about compliance requirements, emergency access needs, and long-term preservation considerations.

### Methodology

---

## Archive
Documents moved to `docs/archive/` are listed here with archival date and reason.

---

## Notes
- Documents in `docs/drafts/` are temporary and not tracked in this index
- All permanent documents should be listed above with status and brief description
- Format: `[Title](path) - Status - Description`