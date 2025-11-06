# Framework Theory Extraction

**Category**: framework-theory  
**Source Documents**: Documents exploring foundational compression theory and decision frameworks  
**Extraction Date**: 2025-11-06 (Session 16)  
**Purpose**: Preserve unique insights from exploratory framework documents

---

## Overview

This file contains key insights extracted from framework exploration documents (14,873 lines total) that are not fully captured in the concise framework documentation. These insights inform the design of DECISION_FRAMEWORK.md and provide practical guidance for compression decisions.

**Extraction Philosophy**: 
- Foundation theory → Already integrated (implicit)
- Practical decision frameworks → Extracted here
- Exploratory content → Archived (full documents preserved)

---

## Source 1: information-preservation-framework.md

**Document**: `docs/analysis/information-preservation-framework.md`  
**Size**: 1,809 lines  
**Created**: 2025-10-29 (Session 2)  
**Status**: PARTIAL SUPERSESSION (~85% integrated, ~15% unique insights)

### Insight 1: Phase-Aware Compression Strategy

**Context**: Compression appropriateness varies by project phase. Same document needs different compression at different lifecycle stages.

**Phase-Specific Compression Targets**:

| Phase | Target Compression | Rationale | Key Focus |
|-------|-------------------|-----------|-----------|
| **Research** | 10-20% | Preserve evidence depth | Organization > reduction |
| **Ideation** | 10-30% | Creativity needs space | Don't kill ideas prematurely |
| **Refinement** | 20-40% | Preserve decision rationale | Keep "why not X" answers |
| **Structure** | 30-50% | Clarity over brevity | Structural format optimization |
| **Build** | 50-70% | Execution efficiency | High-ROI operational focus |
| **Maintain** | 40-60% (active)<br>95-99% (archive) | Variable by activity | Active work vs historical |

**Rationale Preservation Strategy (Refinement Phase)**:
- **Selected approach**: Full detail (0% compression) - needs implementation depth
- **Seriously considered alternatives**: Moderate detail (30-50% compression) - preserve key rejection rationale
- **Briefly evaluated alternatives**: Minimal detail (70-85% compression) - one-line dismissal sufficient
- **Never considered alternatives**: Don't document

**Phase Transition Compression Rules**:
- **Active → Complete**: +15-25% compression (summarize outcomes, keep searchable)
- **Complete → Archive**: +30-50% compression (total 95-99% - metadata + searchability only)

**Document State Lifecycle**:
1. **Active**: Phase-appropriate compression (high detail during work)
2. **Complete**: Moderate compression (+15-25% more aggressive - reference use)
3. **Archive**: Ultra-aggressive (95-99% total - rare access, storage optimization)

**Application**: Use phase context when selecting compression targets. Don't compress Research/Ideation aggressively. Enable aggressive compression during Build/Archive phases.

---

### Insight 2: ROI-Based Prioritization Framework

**Context**: Not all compression opportunities have equal value. High-frequency documents have massive cumulative impact even with small reductions.

**ROI Formula**:
```
ROI = (Token Reduction × Access Frequency) / Compression Effort

High ROI = High frequency + Good compression + Low effort
Low ROI = Low frequency OR poor compression OR high effort
```

**Frequency Impact Analysis**:

| Frequency | Examples | Cumulative Impact | Priority |
|-----------|----------|-------------------|----------|
| **Every session** | SESSION.md, PROJECT.md | CRITICAL | HIGHEST |
| **Daily** | TASKS.md, build configs | HIGH | HIGH |
| **Weekly** | Sprint docs, status reports | MEDIUM | MEDIUM |
| **Monthly** | Strategic reviews, metrics | LOW-MEDIUM | MEDIUM |
| **Rarely** | Historical decisions, archive | MINIMAL | LOW |

**Session Startup = Highest ROI Insight**:
- Small reductions (70-85%) × High frequency (5-20x/day) = Massive cumulative impact
- Example: SESSION.md
  - Reduction: 1,400-1,700 tokens (70-85% of ~2,000)
  - Frequency: 5-20 loads per day
  - Daily impact: 7,000-34,000 tokens saved
  - Effort: One-time template design
  - **ROI: HIGHEST possible**

**Priority Scoring System**:
```
Priority Score = (Frequency × Compression Potential × Current Size) / Implementation Effort

Frequency points:     Every session=10, Daily=7, Weekly=4, Monthly=2, Rarely=1
Compression points:   High (60-85%)=10, Moderate (40-60%)=6, Low (20-40%)=3, Minimal (<20%)=1
Size points:          Very large (>2000)=10, Large (1000-2000)=6, Medium (500-1000)=3, Small (<500)=1
Effort points:        Low (template)=10, Medium=6, High=3, Very high=1 (divider)
```

**Example Calculations**:
- **SESSION.md**: (10 × 10 × 6) / 6 = **100** → HIGHEST PRIORITY
- **TASKS.md**: (7 × 10 × 3) / 10 = **21** → HIGH PRIORITY  
- **DECISIONS.md**: (2 × 3 × 3) / 6 = **3** → MEDIUM PRIORITY
- **Archive logs**: (1 × 10 × 6) / 3 = **2** → LOW-MEDIUM PRIORITY

**Validation Rigor by Impact**:
- **CRITICAL** (session startup): Functional testing required - LLM must successfully resume work
- **HIGH** (daily operational): Task completion testing - verify execution success
- **MEDIUM** (strategic/reference): Purpose-based validation - comprehension spot-checks
- **LOW** (archive): Searchability testing only - reconstruction acceptable if needed

**Three-Phase Compression Strategy**:

**Phase 1: High-Impact Quick Wins**
- Target: Session startup + high-frequency operational
- Documents: SESSION.md (score: 100), PROJECT.md (score: 60-80), TASKS.md (score: 21)
- Why first: Highest cumulative token impact, immediate ROI, validates framework

**Phase 2: Medium-Impact Systematic**
- Target: Strategic and control layer documents
- Documents: Configs, decision logs, architecture docs, planning
- Why second: Moderate frequency, systematic patterns, comprehensive coverage

**Phase 3: Archive Optimization**
- Target: Historical and completed documents
- Documents: Completed logs, archived decisions, old projects
- Why last: Low token impact (rare access), high storage benefit, lower urgency

**Application**: Prioritize session startup documents FIRST. Small reductions × high frequency = massive cumulative impact. Scale validation rigor to match impact stakes.

---

### Insight 3: "When NOT to Compress" Anti-Patterns

**Context**: Negative guidance prevents common mistakes. Some situations make compression counterproductive.

**Seven Anti-Compression Patterns**:

**1. Active Ideation**
- ❌ **Don't**: Compress during brainstorming or concept development
- ✅ **Do**: Organize and structure only, preserve all ideas
- **Why**: Creativity requires space, premature compression kills divergent thinking
- **Indicator**: Team exploring multiple approaches, generating concepts

**2. Active Research**
- ❌ **Don't**: Aggressively compress during investigation
- ✅ **Do**: Preserve all findings, compress after synthesis
- **Why**: Evidence depth critical, can't predict what's important yet
- **Indicator**: Heavy information gathering, discovery phase

**3. Rapid Iteration**
- ❌ **Don't**: Compress during fast pivots or frequent changes
- ✅ **Do**: Wait for stabilization, then compress
- **Why**: Overhead of re-compression exceeds benefit
- **Indicator**: Frequent document changes, approach uncertainty

**4. Uncertain Requirements**
- ❌ **Don't**: Strip "unnecessary" detail when requirements unclear
- ✅ **Do**: Preserve detail until requirements clarify
- **Why**: May need that "unnecessary" detail when requirements change
- **Indicator**: Ambiguous specs, evolving understanding

**5. Learning-Critical Content**
- ❌ **Don't**: Strip rationale from onboarding/educational documents
- ✅ **Do**: Preserve learning value over brevity
- **Why**: Understanding "why" is the point, not just "what"
- **Indicator**: Onboarding docs, training materials, concept explanations

**6. Emergency-Critical Documents**
- ❌ **Don't**: Archive so aggressively that emergency access fails
- ✅ **Do**: Keep emergency procedures accessible even in archive
- **Why**: Reconstruction time unacceptable in emergency
- **Indicator**: Incident response, disaster recovery, critical procedures

**7. Compliance-Required Records**
- ❌ **Don't**: Compress beyond legal/regulatory requirements
- ✅ **Do**: Preserve complete audit trail regardless of phase
- **Why**: Compliance violations cost more than storage
- **Indicator**: Regulated industries, audit trails, legal requirements

**General Anti-Compression Principle**:
> "When compression overhead exceeds compression benefit, don't compress."

**Indicators of Premature Compression** (warning signs):
- Frequent decompression requests
- Information loss incidents
- Rework due to missing context
- Complaints about missing detail
- Context recovery attempts
- Team asking "why did we remove X?"

**Application**: Use as checklist before compressing. If document matches any anti-pattern, delay compression or reduce aggressiveness. Recognize when preservation > optimization.

---

## Integration Plan

### For DECISION_FRAMEWORK.md (Phase 2)

**Section 1: Phase-Based Compression Guidelines** (~100-120 lines)
- Phase compression targets table
- Rationale preservation strategy (Refinement focus)
- Phase transition rules
- Document state lifecycle

**Section 2: ROI-Based Prioritization** (~120-150 lines)
- ROI formula and frequency impact
- Session startup = highest ROI principle
- Priority scoring system with examples
- Three-phase compression strategy
- Validation rigor scaling

**Section 3: Common Pitfalls** (~80-100 lines)
- Seven anti-compression patterns
- General principle (overhead vs benefit)
- Indicators of premature compression
- When to delay or reduce compression

**Total Estimated Addition**: ~300-370 lines

### For Integration Guide (Optional Enhancement)

Consider adding to existing sections:
- Part 2 (Template Selection): ROI prioritization guidance
- Part 4 (Project Integration): Phase-awareness context
- Part 5 (Advanced Patterns): Anti-patterns as edge cases

**Estimated Addition**: ~100-150 lines if integrated

---

## Additional Sources

*To be added as more documents are audited*

---

**Extraction Status**: In Progress (1 of 10 documents audited)  
**Next**: Continue with multi-dimensional-compression-matrix.md## Source 2: multi-dimensional-compression-matrix.md

**Document**: `docs/patterns/multi-dimensional-compression-matrix.md`  
**Size**: 1,340 lines  
**Created**: 2025-10-30 (Session 3)  
**Status**: REFINE INTO DECISION_FRAMEWORK.md (not extraction)

### Special Note: Core Decision Framework Content

**This document is different** from others being audited. It's not historical exploration to extract from - it IS the decision framework that becomes DECISION_FRAMEWORK.md in Phase 2.

**Disposition**: REFINE (not archive and extract)
- ~70% is core decision-making content (matrix, strategies, examples)
- ~30% is superseded definitions and integration discussion
- Result: 600-700 line DECISION_FRAMEWORK.md

**Content Breakdown**:
- Base Compression Matrix: [Role × Layer] targets → KEEP
- Phase Adjustments: Multipliers for each phase → KEEP
- Multi-Role Strategies: Union/Intersection/Layered → KEEP
- Conflict Resolution: Priority rules and decision tree → KEEP
- Worked Examples: 6 detailed examples → KEEP 4-6 best
- Application Guide: 8-step process → KEEP
- Edge Cases & Practices: Streamline to key points → REDUCE 50%
- Dimension Definitions: Role/Layer/Phase → REMOVE (superseded)
- Integration Discussion: How pieces connect → REMOVE (implicit)

**Not Extracted Here**: See full audit report (AUDIT_multi-dimensional-compression-matrix.md) for refinement plan

---

