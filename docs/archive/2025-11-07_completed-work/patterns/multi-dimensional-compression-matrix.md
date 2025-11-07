# Multi-Dimensional Compression Matrix

**Created:** 2025-10-30 AEDT  
**Purpose:** Operationalize [Role × Layer × Phase] compression decision framework  
**Status:** Active refinement (Session 1)  
**Gap Addressed:** Multi-dimensional decision framework (HIGH priority)

---

## Executive Summary

**Problem:** Compression framework addresses dimensions separately (audience categories, purposes, targets), but CC_Projects validated architecture proves multi-dimensional complexity is real: [Role × Layer × Phase × Mode]. Need explicit guidance for compression decisions when multiple dimensions interact.

**Solution:** This matrix provides compression targets for all [Role × Layer × Phase] combinations, decision processes for resolving conflicts, and mode-switching considerations.

**Key Insight:** Cannot compress along single dimension. A Developer (role) accessing Strategic layer (layer) during Build phase (phase) has different needs than same Developer accessing same layer during Maintain phase. Single compression target insufficient.

**Usage:** 
1. Identify role, layer, and phase for document
2. Look up base compression target in matrix
3. Apply conflict resolution if multiple roles/phases
4. Adjust for mode-switching patterns
5. Validate preservation requirements

---

## Section 1: The Three Dimensions

### Dimension 1: Role (WHO accesses)

From CC_Projects H2 validated roles:

**1. Coordinator**
- Function: Project oversight, workflow orchestration, stakeholder communication
- Information Needs: High-level summaries, strategic context, cross-phase view
- Depth: Low depth, high breadth
- Access Pattern: Strategic/Control layer focus, dashboard views
- Technical Literacy: Low-Medium

**2. Analyst**
- Function: Research, investigation, requirements gathering, validation
- Information Needs: Deep research access, evidence trails, gap analysis
- Depth: Deep in research domain, moderate elsewhere
- Access Pattern: Heavy research consumption, creates substantial documentation
- Technical Literacy: Medium-High (domain dependent)

**3. Architect**
- Function: Design decisions, technical structure, system architecture
- Information Needs: Strategic principles, design rationale, constraints
- Depth: Deep technical understanding required
- Access Pattern: Strategic layer read/write, creates foundational documents
- Technical Literacy: High

**4. Developer**
- Function: Implementation, coding, unit testing
- Information Needs: Operational details, specifications, clear requirements
- Depth: High in operational, minimal strategic
- Access Pattern: Operational/Session layer focus, task-focused
- Technical Literacy: High

**5. Maintainer**
- Function: Evolution, optimization, support, technical debt management
- Information Needs: Comprehensive system understanding, historical decisions
- Depth: Requires access to all layers including archive
- Access Pattern: Strategic (why decisions made), Archive (history)
- Technical Literacy: High

**6. Orchestrator** (v2.0 consideration)
- Function: Multi-agent coordination, workflow automation, quality synthesis
- Information Needs: Meta-level project structure, agent configurations
- Depth: Tool-agnostic understanding
- Access Pattern: Control layer, configuration management
- Technical Literacy: System-level

### Dimension 2: Layer (WHAT is documented)

From CC_Projects H3 validated layers:

**Layer 1: Strategic**
- Content: Vision, decisions, principles, high-level architecture
- Purpose: Long-term guidance, design rationale, context
- Examples: PROJECT.md, DECISIONS.md, PRINCIPLES.md
- Lifespan: Permanent, evolves slowly
- Access: All roles (different depths)

**Layer 2: Control**
- Content: Configuration, modes, skills, workflow automation
- Purpose: System behavior control, tool setup
- Examples: CLAUDE.md, settings.json, hooks, commands
- Lifespan: Phase-dependent, configuration changes
- Access: Architect (design), Developer (use), Orchestrator (manage)

**Layer 3: Operational**
- Content: Active work, tasks, implementation details
- Purpose: Current development activities
- Examples: TASKS.md, feature branches, work-in-progress
- Lifespan: Task-specific, archives when complete
- Access: Developer (primary), Maintainer (reference)

**Layer 4: Session**
- Content: Ephemeral state, handovers, context recovery
- Purpose: Cross-session continuity, context management
- Examples: SESSION.md, HANDOVER.md, checkpoints
- Lifespan: Session-specific, regenerated frequently
- Access: All roles (continuity critical)

**Layer 5: Archive**
- Content: Historical records, completed work, lessons learned
- Purpose: Searchability, reference, compliance
- Examples: archive/[date]/[documents], completed session logs
- Lifespan: Permanent, rarely accessed
- Access: Maintainer (primary), Coordinator (reference)

### Dimension 3: Phase (WHEN accessed)

From CC_Projects H1 validated lifecycle:

**Phase 1: Research**
- Activities: Investigation, discovery, feasibility analysis
- Information Pattern: Heavy gathering, evidence accumulation
- Compression Need: Preserve depth, manage volume

**Phase 2: Ideation**
- Activities: Concept development, brainstorming, exploration
- Information Pattern: Divergent thinking, multiple approaches
- Compression Need: LOW - space for creativity essential

**Phase 3: Refinement**
- Activities: Validation, design iteration, specification
- Information Pattern: Convergent thinking, narrowing to solution
- Compression Need: Preserve rationale for eliminated alternatives

**Phase 4: Structure**
- Activities: Architecture, planning, organization setup
- Information Pattern: Formalization, foundation documentation
- Compression Need: Clarity and precision over brevity

**Phase 5: Build**
- Activities: Implementation with strategic oversight
- Information Pattern: Task-focused, operational details
- Compression Need: HIGH - execution efficiency

**Phase 6: Maintain**
- Activities: Evolution, enhancement, optimization
- Information Pattern: Historical understanding + active changes
- Compression Need: Variable (active: moderate, archive: aggressive)

---

## Section 2: Base Compression Target Matrix

### Matrix Structure

Compression targets expressed as percentage reduction (e.g., 40% = reduce to 60% of original).

| Role | L1: Strategic | L2: Control | L3: Operational | L4: Session | L5: Archive |
|------|--------------|-------------|-----------------|-------------|-------------|
| **Coordinator** | 20-30% | 30-40% | 40-50% | 60-70% | 95-97% |
| **Analyst** | 25-35% | 35-45% | 35-45% | 60-70% | 95-97% |
| **Architect** | 30-40% | 40-50% | 40-50% | 65-75% | 95-97% |
| **Developer** | 40-50% | 40-50% | 40-50% | 70-80% | 95-97% |
| **Maintainer** | 30-40% | 40-50% | 40-50% | 65-75% | 95-99% |
| **Orchestrator** | 60-70% | 50-60% | 60-70% | 75-85% | 97-99% |

**Reading the Matrix:**
- Coordinator accessing Strategic: 20-30% reduction (preserve high-level context)
- Developer accessing Session: 70-80% reduction (execution-focused, structured)
- Maintainer accessing Archive: 95-99% reduction (ultra-aggressive, rare access)

**Key Patterns:**
- Strategic layer: Lower compression (rationale preservation critical)
- Session layer: Higher compression (high frequency, machine-first)
- Archive layer: Ultra-aggressive (rare access, searchability priority)
- Coordinator: Lowest compression (needs context and breadth)
- Orchestrator: Highest compression (machine-first, automation-focused)

### Phase-Adjusted Targets

Base matrix assumes **active phase** for document. Adjust by phase:

**Phase Multipliers:**

| Phase | Description | Adjustment | Rationale |
|-------|-------------|------------|-----------|
| **Research** | Evidence gathering | -10 to -20% | Preserve research depth |
| **Ideation** | Creative exploration | -20 to -30% | Space for divergent thinking |
| **Refinement** | Design iteration | -10 to -15% | Preserve alternative rationale |
| **Structure** | Architecture setup | ±0% | Base targets appropriate |
| **Build** | Active implementation | +10 to +20% | Execution efficiency |
| **Maintain - Active** | Ongoing changes | ±0 to +10% | Balance history + efficiency |
| **Maintain - Archive** | Historical record | +20 to +30% | Ultra-aggressive, move to L5 |

**Example Calculations:**

**Architect accessing Strategic during Ideation:**
- Base: 30-40% compression
- Phase: Ideation (-20 to -30%)
- Result: 10-20% compression (preserve creative space)

**Developer accessing Operational during Build:**
- Base: 40-50% compression  
- Phase: Build (+10 to +20%)
- Result: 50-70% compression (aggressive, task-focused)

**Maintainer accessing Strategic during Maintain (historical):**
- Base: 30-40% compression
- Phase: Maintain-Archive (+20 to +30%)
- Result: Move to L5 Archive, 95-99% compression

### Document State Adjustments

Documents evolve through lifecycle states:

**Active State** (currently working):
- Use base matrix + phase adjustments
- Preserve detail for current work
- Compression: Moderate

**Complete State** (finished, reference):
- Add +15 to +25% compression
- Reference format, summary access
- Move operational details to appendix/archive

**Archive State** (historical, rare access):
- Move to Layer 5
- Apply archive compression (95-99%)
- Preserve searchability over readability

---

## Section 3: Multi-Role Document Handling

### Problem: Many Documents Serve Multiple Roles

**Examples:**
- **DECISIONS.md**: Coordinator (oversight) + Maintainer (historical understanding)
- **PROJECT.md**: All roles (different depths)
- **TASKS.md**: Developer (execution) + Coordinator (status)

### Strategy 1: Union of Requirements (Most Conservative)

**When to Use:** Critical documents, multiple purposes, high preservation needs

**Process:**
1. Identify all roles accessing document
2. Calculate compression target for each role
3. Select LOWEST compression (highest preservation)
4. Apply to entire document

**Example: DECISIONS.md**
- Coordinator + Strategic + Research: 20-30% - 10-20% = 10-20%
- Maintainer + Strategic + Maintain: 30-40% + 0% = 30-40%
- Union: Use 10-20% (lowest, highest preservation)

**Trade-off:** Conservative, may over-preserve, but safe

### Strategy 2: Intersection (Most Aggressive)

**When to Use:** High-frequency documents, clear primary role, secondary roles optional

**Process:**
1. Identify primary role (highest access frequency)
2. Calculate target for primary role
3. Apply aggressive compression
4. Provide alternate representations for secondary roles if needed

**Example: TASKS.md**
- Developer + Operational + Build: 40-50% + 10-20% = 50-70% (PRIMARY)
- Coordinator + Operational + Build: 40-50% + 10-20% = 50-70% (SECONDARY)
- Intersection: Use 50-70% (primary role optimized)
- Secondary: Coordinator gets summary view separately

**Trade-off:** Optimizes for primary, may require multiple representations

### Strategy 3: Layered Representation (Most Flexible)

**When to Use:** Complex documents, significant role divergence, optimization beneficial

**Process:**
1. Create role-specific views of same content
2. Each view compressed for its role
3. Share common base, generate views

**Example: PROJECT.md**
- Coordinator view: 20-30% compression (strategic summary)
- Developer view: 50-60% compression (operational focus only)
- Architect view: 30-40% compression (design rationale preserved)
- Maintainer view: 30-40% compression + archive links

**Trade-off:** Most flexible, but higher overhead (multiple files)

### Multi-Role Decision Framework

**Step 1: Analyze Access Patterns**
- Who accesses most frequently?
- What's the primary purpose?
- Are role needs similar or divergent?

**Step 2: Calculate Cost/Benefit**
- Union: Safe, simple, may over-preserve
- Intersection: Optimized, may under-serve secondary roles
- Layered: Flexible, higher maintenance overhead

**Step 3: Select Strategy**

| Role Divergence | Access Pattern | Recommendation |
|-----------------|----------------|----------------|
| Low (<20% difference) | Any | Union (simple, adequate) |
| Medium (20-40% difference) | Clear primary | Intersection + summary |
| High (>40% difference) | Balanced | Layered views |
| High (>40% difference) | Clear primary | Intersection + separate docs |

**Step 4: Validate**
- Can all roles accomplish their purposes?
- Is information preservation adequate?
- Is overhead justified by benefits?

---

## Section 4: Conflict Resolution Process

### Common Conflicts

**Conflict Type 1: Role vs Layer Contradiction**
- Example: Coordinator (low compression) accessing Archive (high compression)
- Resolution: Layer wins (archive purpose = aggressive compression)
- Rationale: Layer represents information lifecycle state

**Conflict Type 2: Phase vs Role Contradiction**
- Example: Developer (high compression) during Ideation (low compression)
- Resolution: Phase wins (creative space essential)
- Rationale: Phase represents current work mode, overrides default preferences

**Conflict Type 3: Multiple Roles with Divergent Needs**
- Example: DECISIONS.md (Coordinator 20% vs Maintainer 40%)
- Resolution: Apply multi-role strategy (see Section 3)
- Rationale: Purpose and preservation requirements determine approach

### Conflict Resolution Decision Tree

```
START: Compression target needed for [Role × Layer × Phase]

1. Is document in Archive (L5)?
   YES → Apply archive compression (95-99%), END
   NO → Continue

2. Is phase Ideation?
   YES → Apply low compression (10-30% max), END
   NO → Continue

3. Is document Session layer (L4)?
   YES → Apply aggressive compression (60-85%), END
   NO → Continue

4. Does document serve single role?
   YES → Use base matrix + phase adjustment, END
   NO → Continue to multi-role

5. Multi-role: Calculate divergence
   <20% → Union strategy
   20-40% with clear primary → Intersection + summary
   >40% → Layered views or separate documents
   END
```

### Priority Rules (Highest to Lowest)

1. **Archive Layer (L5):** Always ultra-aggressive (95-99%)
2. **Ideation Phase:** Always low compression (10-30% max)
3. **Session Layer (L4):** Always aggressive (60-85%)
4. **Multi-role Preservation:** Union if critical, else by access pattern
5. **Base Matrix:** Default when no overrides apply

**Rationale:**
- Archive and Session have clear functional requirements (storage vs continuity)
- Ideation phase needs creative space (validated by H1)
- Multi-role preservation ensures no use case breaks
- Base matrix provides sensible defaults

---

## Section 5: Mode-Switching Overhead

### What is Mode-Switching?

From H2 Finding: "Some roles require frequent mode switching (maintenance), others operate in single mode (development)."

**Mode:** The working context a role operates within
- Execution mode: Doing tasks, implementing features
- Analysis mode: Investigating, researching, understanding
- Planning mode: Designing, architecting, strategizing
- Review mode: Auditing, validating, quality checking

**Mode-Switching:** Transitioning between contexts within same document/session

### Roles by Mode-Switching Frequency

**High Frequency (Maintainer, Architect):**
- Maintainer: Execution → Analysis (why bug?) → Review (impact?) → Planning (fix approach)
- Architect: Planning → Analysis (research) → Execution (prototype) → Review (validate)
- Impact: Need quick context switches, prefer unified documents

**Medium Frequency (Analyst, Coordinator):**
- Analyst: Analysis → Planning (structure) → Review (validate)
- Coordinator: Planning → Review (status) → Execution (decisions)
- Impact: Moderate switching, can handle separate documents

**Low Frequency (Developer, Orchestrator):**
- Developer: Primarily execution mode, occasional planning
- Orchestrator: System-level automation, minimal switching
- Impact: Single mode focus, highly compressed acceptable

### Compression Implications

**High Mode-Switching Roles:**
- Prefer: Unified documents with moderate compression
- Avoid: Extreme compression requiring context reconstruction
- Adjustment: -10 to -15% compression (easier transitions)

**Low Mode-Switching Roles:**
- Prefer: Highly compressed, mode-specific documents
- Acceptable: Reconstruction costs (rare transitions)
- Adjustment: +10 to +15% compression (optimization opportunity)

### Mode-Switching Adjustment Formula

**Base target from matrix**
± **Role mode-switching factor**
= **Final target**

**Mode-Switching Factors:**
- Maintainer: -10 to -15% (high switching, preserve context)
- Architect: -5 to -10% (high switching, preserve rationale)
- Analyst: -5 to -10% (medium switching, evidence preservation)
- Coordinator: ±0% (medium switching, base adequate)
- Developer: +5 to +10% (low switching, optimize execution)
- Orchestrator: +10 to +15% (minimal switching, machine-first)

**Example:**

**Maintainer accessing Strategic during Maintain:**
- Base: 30-40%
- Phase: Maintain (±0%)
- Mode-switching: -10 to -15%
- Final: 20-30% compression

**Developer accessing Operational during Build:**
- Base: 40-50%
- Phase: Build (+10 to +20%)
- Mode-switching: +5 to +10%
- Final: 55-80% compression

---

## Section 6: Worked Examples

### Example 1: SESSION.md Compression

**Document:** SESSION.md (session handover)

**Context:**
- Layer: L4 (Session)
- Primary Role: All roles (LLM consumption)
- Phase: Continuous (every session)
- State: Active (regenerated frequently)
- Access: Multiple times daily (CRITICAL frequency)

**Analysis:**
1. Layer L4 → Aggressive compression priority
2. LLM-primary audience → Machine-first design
3. High frequency → Highest ROI opportunity
4. Execution purpose → Precision over prose

**Compression Calculation:**
- Base (Developer + Session): 70-80%
- Phase: Continuous (build-equivalent): +0%
- Mode-switching: Developer +5-10%
- Frequency bonus: +5% (highest ROI)
- **Target: 75-85% compression**

**Method Selection:**
- Structural compression: Prose → YAML/JSON
- Section-based keys: WHERE/ACCOMPLISHED/NEXT/etc.
- Compact notation: Lists, IDs, references
- Eliminate: Redundancy, elaboration, formatting prose

**Validation Requirements:**
- CRITICAL: LLM must resume work without information loss
- Test: Can LLM execute all tasks from compressed version?
- Preserve: State, decisions, blockers, next actions
- Strip: Explanatory prose, redundant context

**Expected Result:**
- Current: ~400-500 lines prose
- Target: ~80-125 lines structured
- Ratio: 75-85% reduction validated

### Example 2: DECISIONS.md Entry Compression

**Document:** DECISIONS.md (strategic decision log)

**Context:**
- Layer: L1 (Strategic)
- Roles: Coordinator (oversight) + Maintainer (historical) + Architect (rationale)
- Phase: Varies (entry-dependent)
- State: Active → Complete → Archive transition
- Access: On-demand, learning/audit purposes

**Multi-Role Analysis:**
- Coordinator: 20-30% compression (context preservation)
- Maintainer: 30-40% compression (understand why)
- Architect: 30-40% compression (design rationale)
- Divergence: <20% (similar needs)
- Strategy: **Union** (most conservative)

**Compression Calculation:**
- Base (Coordinator + Strategic): 20-30%
- Phase: Structure (decision formalization): ±0%
- Multi-role: Union (use lowest = 20-30%)
- **Target: 20-30% compression**

**Method Selection:**
- Structural: Decision template (Context/Decision/Rationale/Impact)
- Summary: Remove redundant elaboration
- Preserve: All rationale, context, implications
- Acceptable: Some prose reduction, consolidation

**Phase Transition Strategy:**
- Active (current decisions): 20-30% compression
- Complete (6 months old): 30-40% compression (add summary)
- Archive (1+ year old): Move to L5, 95-99% compression (keep key metadata)

**Expected Result:**
- Current: ~200-300 lines per decision (detailed prose)
- Compressed: ~140-240 lines (structured, consolidated)
- Ratio: 20-30% reduction with full context preserved

### Example 3: TASKS.md for Active Development

**Document:** TASKS.md (operational work tracking)

**Context:**
- Layer: L3 (Operational)
- Primary Role: Developer (execution)
- Secondary Role: Coordinator (status monitoring)
- Phase: Build (active implementation)
- State: Active (constantly updated)
- Access: Daily (high frequency)

**Multi-Role Analysis:**
- Developer: 40-50% base + 10-20% phase + 5-10% mode = 55-80%
- Coordinator: 40-50% base + 10-20% phase = 50-70%
- Divergence: ~10-15% (acceptable)
- Primary: Developer (highest frequency)
- Strategy: **Intersection** (optimize for primary)

**Compression Calculation:**
- Primary (Developer): 55-80%
- Secondary acceptable: Coordinator gets status summary separately
- **Target: 60-75% compression**

**Method Selection:**
- Structural: Checklist format, compact notation
- Reference: Link to specs, avoid duplication
- Strip: Detailed descriptions (link to specs), prose explanations
- Preserve: Task status, dependencies, blockers, owners

**Dual-View Approach:**
- Developer view: Compressed checklist (60-75% reduction)
- Coordinator view: Separate status summary (generated from checklist)

**Expected Result:**
- Current: ~100 lines per feature (prose descriptions)
- Compressed: ~25-40 lines (structured checklist)
- Coordinator summary: ~5-10 lines per feature (status only)
- Ratio: 60-75% reduction for primary, status view for secondary

### Example 4: Configuration File (Control Layer)

**Document:** .claude/config.yaml (control layer)

**Context:**
- Layer: L2 (Control)
- Roles: Architect (design) + Developer (use) + Orchestrator (automation)
- Phase: Structure (setup) → Build (use) → Maintain (evolve)
- State: Semi-stable (infrequent changes)
- Access: Setup + occasional modification

**Multi-Role Analysis:**
- Architect: 40-50% base
- Developer: 40-50% base
- Orchestrator: 50-60% base
- Divergence: <15% (similar technical literacy)
- Strategy: **Union** (single representation adequate)

**Compression Calculation:**
- Base (Architect + Control): 40-50%
- Phase: Structure (±0%)
- Format: Already YAML (optimal)
- **Target: 40-50% compression**

**Method Selection:**
- Already structural (YAML) ✓
- Compression: Comments → separate docs
- Strip: Verbose explanations, examples (link to docs)
- Preserve: All functional settings, required comments
- Format: Compact YAML notation, concise keys

**Expected Result:**
- Current: ~150 lines with inline comments and examples
- Compressed: ~75-90 lines + separate documentation
- Ratio: 40-50% reduction in config file itself
- Documentation: Comprehensive guide separately

### Example 5: Archive Compression (Layer 5)

**Document:** Completed session log from 6 months ago

**Context:**
- Layer: L5 (Archive)
- Primary Role: Maintainer (historical reference)
- Phase: Maintain (archive state)
- State: Archive (completed, rare access)
- Access: Rare, search-driven

**Layer Override:**
- L5 Archive → Ultra-aggressive compression (95-99%)
- Purpose: Searchability, not readability
- Trade-off: Reconstruction cost acceptable

**Compression Calculation:**
- Base: Not applicable (Layer 5 override)
- Layer 5: 95-99% compression
- Method: Context Compression Method (conversational)
- **Target: 97-99% compression**

**Method Selection:**
- Context Compression Method (conversational technique)
- Multi-tier strategy: JSON summary + compressed narrative
- Preserve: Metadata (date, phase, outcomes, key decisions)
- Strip: Detailed execution logs, working notes, redundant state
- Searchable: Keywords, decision IDs, references

**Expected Result:**
- Current: ~500-1000 lines (detailed session log)
- Compressed: ~5-20 lines (structured summary + metadata)
- Ratio: 97-99% reduction
- Access: Searchable, expandable on-demand if reconstruction needed

### Example 6: Research Phase Strategic Document

**Document:** Research findings (Strategic layer, Research phase)

**Context:**
- Layer: L1 (Strategic)
- Primary Role: Analyst (creating) + Architect (consuming)
- Phase: Research (evidence gathering)
- State: Active (ongoing research)
- Access: Frequent during research, reference afterward

**Phase Adjustment Critical:**
- Base: 25-35% (Analyst) or 30-40% (Architect)
- Phase: Research (-10 to -20%) **CRITICAL**
- Result: 5-20% compression (preserve research depth)

**Compression Calculation:**
- Base (Analyst + Strategic): 25-35%
- Phase: Research (-15 to -20%)
- **Target: 10-15% compression (LOW)**

**Rationale:**
- Research phase requires depth preservation
- Evidence trails must remain intact
- H1 validation: Research = heavy information gathering
- Compression premature during active research

**Method Selection:**
- Minimal compression: Remove only clear redundancy
- Structural: Organize findings systematically
- Preserve: All evidence, sources, analysis, gaps
- Strip: Only duplicate information, unnecessary formatting

**Phase Transition:**
- Research (active): 10-15% compression
- → Refinement: 20-30% compression (synthesize findings)
- → Complete: 30-40% compression (summary + detail)
- → Archive: 95-99% compression (metadata + references)

**Expected Result:**
- Current: ~500 lines (detailed research)
- Research phase: ~425-450 lines (minimal compression)
- Post-research: ~300-400 lines (moderate compression)
- Ratio: 10-15% during research (preserve), more aggressive later

---

## Section 7: Edge Cases and Special Scenarios

### Edge Case 1: Rapid Phase Transitions

**Scenario:** Prototype project, rapid iteration through phases

**Challenge:** Compression targets change quickly, overhead of re-compression

**Solution:**
- Keep low compression during rapid iteration (20-30%)
- Apply aggressive compression only at stable milestones
- Use temporal versioning: Keep detailed until stabilized

### Edge Case 2: Cross-Phase Documents

**Scenario:** Document spans multiple phases (e.g., ongoing TASKS.md)

**Challenge:** Different tasks in different phases simultaneously

**Solution:**
- Apply compression per task/section, not document-level
- Active tasks: Phase-appropriate compression
- Completed tasks: Aggressive compression or archive
- Document structure: Separate active from complete

### Edge Case 3: Emergency Access (On-Call Maintainer)

**Scenario:** Critical bug, maintainer needs rapid understanding

**Challenge:** Archived documents too compressed for emergency comprehension

**Solution:**
- Critical documents: Flag "emergency-accessible"
- Apply moderate compression even in archive (70-80%, not 95-99%)
- Include "Quick Start" section always preserved
- Trade-off: Storage efficiency vs emergency accessibility

### Edge Case 4: Compliance/Audit Requirements

**Scenario:** Legal or regulatory requirement for complete records

**Challenge:** Archive compression may violate preservation requirements

**Solution:**
- Compliance documents: Flag "compliance-required"
- Apply minimal compression (20-30%) regardless of layer
- Store compressed + full versions
- Archive strategy: Organize, don't compress

### Edge Case 5: Multi-Project Shared Documents

**Scenario:** Documentation shared across multiple projects/phases

**Challenge:** Different projects in different phases, different compression needs

**Solution:**
- Version per project: Each gets phase-appropriate compression
- Shared base: Keep moderate compression (30-40%)
- Project-specific: Apply full compression strategy
- Trade-off: Duplication vs optimization

### Edge Case 6: Learning/Tutorial Documents

**Scenario:** Onboarding documentation, learning resources

**Challenge:** Need detail for learners, efficiency for experienced

**Solution:**
- Layered representation: Beginner (10-20%) + Advanced (50-60%)
- Progressive disclosure: Summary → Detail on-demand
- Audience switch: Learner → Practitioner changes compression
- Primary audience determines base compression

---

## Section 8: Integration with Existing Framework

### Integration Point 1: Documentation Types Matrix

**Connection:** Multi-dimensional matrix operationalizes audience categories

**Mapping:**
- LLM-Only (70-85%) → Orchestrator + Session/Archive
- Technical-Heavy (60-75%) → Developer + Operational/Control  
- Hybrid-Technical (40-60%) → Architect/Developer + Strategic/Control
- Hybrid-General (20-40%) → Coordinator/Analyst + Strategic
- General-Friendly (10-25%) → Coordinator + all layers
- Human-Primary (5-15%) → Learning/Tutorial contexts

**Enhancement:** Matrix adds phase and layer context to audience analysis

### Integration Point 2: Information Preservation Framework

**Connection:** Multi-dimensional matrix informs "what to preserve" decisions

**Process:**
1. Identify purposes from framework (execution, learning, audit, etc.)
2. Map purposes to roles accessing document
3. Calculate compression target using matrix
4. Apply preservation requirements per purpose
5. Validate: Can all purposes still be served?

**Enhancement:** Matrix provides quantitative targets for preservation decisions

### Integration Point 3: Compression Method Selection

**Matrix Informs Method Choice:**

| Compression Range | Recommended Methods |
|-------------------|---------------------|
| **5-20%** (Low) | Summary (light), Organization only |
| **20-40%** (Moderate) | Summary + Structural (selective) |
| **40-60%** (High) | Structural + Reference |
| **60-85%** (Aggressive) | Structural + Temporal + Reference
| **95-99%** (Ultra-aggressive) | Conversational Compression, Metadata-only |

**Method Combinations:**
- Low compression: Minimal changes, organization improvements
- Moderate: Structural where beneficial, preserve prose where needed
- High: Aggressive structural, reference external details
- Ultra-aggressive: Complete transformation, searchability priority

---

## Section 9: Practical Application Guide

### Step-by-Step Process

**Step 1: Identify Dimensions**

Questions to answer:
- WHO will access this document? (Role)
- WHAT layer does it belong to? (Layer)
- WHEN will it be used? (Phase)
- HOW frequently is it accessed? (Frequency)

**Step 2: Calculate Base Target**

1. Look up [Role × Layer] in base matrix
2. Note the compression range (e.g., 40-50%)
3. This is your starting point

**Step 3: Apply Phase Adjustment**

1. Identify current phase (Research/Ideation/Refinement/Structure/Build/Maintain)
2. Apply phase multiplier:
   - Research: -10 to -20%
   - Ideation: -20 to -30%
   - Refinement: -10 to -15%
   - Structure: ±0%
   - Build: +10 to +20%
   - Maintain-Active: ±0 to +10%
   - Maintain-Archive: +20 to +30%

**Step 4: Check for Overrides**

Priority order (highest to lowest):
1. Is it Archive (L5)? → 95-99%, STOP
2. Is it Ideation phase? → Max 30%, STOP
3. Is it Session (L4)? → 60-85%, STOP
4. Is it multi-role with >20% divergence? → Apply multi-role strategy
5. Compliance/emergency flagged? → Apply special handling

**Step 5: Adjust for Mode-Switching**

If applicable:
- Maintainer: -10 to -15%
- Architect: -5 to -10%
- Analyst: -5 to -10%
- Developer: +5 to +10%
- Orchestrator: +10 to +15%

**Step 6: Calculate Final Target**

Formula:
```
Base (from matrix)
± Phase adjustment
± Mode-switching adjustment
± Frequency bonus (high frequency +5%)
= Final compression target
```

**Step 7: Select Methods**

Based on final target:
- 5-20%: Summary (light), organization
- 20-40%: Summary + selective structural
- 40-60%: Structural + reference
- 60-85%: Structural + temporal + reference
- 95-99%: Conversational compression

**Step 8: Validate**

Verify preservation requirements:
- Can all roles accomplish their purposes?
- Are all purposes from framework still served?
- Is information fidelity maintained?
- Are special requirements met (compliance, emergency, etc.)?

**Step 9: Document Decision**

Record:
- Calculation process
- Target selected
- Methods used
- Validation results
- Rationale for choices

### Quick Reference Decision Tool

```
[Role] × [Layer] → Base Target
± [Phase] → Adjusted Target
Check overrides (L5/Ideation/L4) → Final Target (or override)
± Multi-role/Mode-switching → Refined Target
→ Select Methods → Validate → Apply
```

### Common Patterns (Quick Lookup)

**Session Handover (all projects):**
- All roles + L4 + Continuous → 70-85%
- Method: Structural (YAML), highest ROI

**Strategic Decisions (active):**
- Multiple roles + L1 + Structure → 20-30%
- Method: Structural template, preserve rationale

**Implementation Tasks (active):**
- Developer + L3 + Build → 60-75%
- Method: Checklist, reference specs

**Configuration Files:**
- Technical roles + L2 + Structure → 40-50%
- Method: Already YAML, compress comments

**Research Findings (active):**
- Analyst + L1 + Research → 10-15%
- Method: Minimal, preserve evidence

**Archive Logs:**
- Any role + L5 + Maintain → 95-99%
- Method: Conversational compression

---

## Section 10: Best Practices

### Practice 1: Start Conservative, Iterate

**Principle:** Easier to compress more later than recover lost information

**Approach:**
- First pass: Use lower end of range
- Validate: Verify all purposes served
- Iterate: Compress more if validation passes
- Monitor: Track information loss carefully

### Practice 2: Document Your Decisions

**Why:** Compression is judgment, not formula

**What to document:**
- Target calculation process
- Rationale for edge cases
- Trade-offs accepted
- Validation approach
- Lessons learned

**Where:** Compression specification file per document type

### Practice 3: Phase Awareness is Critical

**Anti-pattern:** Applying high compression during Ideation/Research

**Good practice:** 
- Recognize phase before compressing
- Apply phase-appropriate targets
- Plan for phase transitions
- Preserve → Compress as phases progress

### Practice 4: Validate with Real Users/LLMs

**Don't assume:** Test actual comprehension

**Validation:**
- LLM: Can it execute tasks from compressed version?
- Humans: Can appropriate audiences understand?
- Purposes: Are all still served?
- Edge cases: Emergency access, compliance, etc.

### Practice 5: Multi-Role Requires Strategy

**Anti-pattern:** Averaging compression targets

**Good practice:**
- Identify access patterns
- Calculate role divergence
- Select appropriate strategy (Union/Intersection/Layered)
- Validate all roles served

### Practice 6: Monitor ROI

**High ROI targets:**
- Session layer (L4) - loaded frequently
- High-frequency access documents
- Large documents with aggressive targets

**Track:**
- Token reduction achieved
- Access frequency
- Actual time savings
- Information loss incidents

### Practice 7: Archive Aggressively, But Safely

**Principle:** Archive = storage optimization, not active use

**Safe approach:**
- Verify truly archived (low access expected)
- Preserve metadata and searchability
- Accept reconstruction costs
- Keep emergency-critical accessible
- Respect compliance requirements

### Practice 8: Beware Premature Compression

**When NOT to compress:**
- Ideation phase (creativity needs space)
- Active research (evidence preservation)
- Rapid iteration (overhead exceeds benefit)
- Uncertain requirements (may need detail later)

**Better:** Wait until stabilized, then compress appropriately

### Practice 9: Layered Compression for Complexity

**When divergence is high:**
- Consider multiple representations
- Role-specific views
- Progressive disclosure
- Cost: Maintenance overhead
- Benefit: Optimal for each audience

### Practice 10: Integrate with Workflow

**Compression as part of lifecycle:**
- Active: Moderate compression
- Complete: Aggressive compression
- Archive: Ultra-aggressive compression
- Emergency: Keep accessible versions

**Automate where possible:**
- Phase transitions trigger compression reviews
- Archive moves apply automatic compression
- Frequency tracking identifies high-ROI targets

---

## Section 11: Validation and Testing

### Validation Dimensions

**1. Functional Validation**
- Can LLM/humans execute intended purposes?
- Test: Actual task completion with compressed version
- Pass: All purposes successfully accomplished
- Fail: Information loss detected, reduce compression

**2. Comprehension Validation**
- Can appropriate audiences understand content?
- Test: Role-specific comprehension assessment
- Pass: Audience understands at required depth
- Fail: Confusion or misunderstanding, clarify or reduce compression

**3. Preservation Validation**
- Is critical information retained?
- Test: Compare compressed to original purpose-by-purpose
- Pass: All essential information present
- Fail: Critical information lost, restore and reduce compression

**4. Performance Validation**
- Does compression achieve target ROI?
- Test: Measure token reduction vs overhead
- Pass: Reduction meets targets, overhead acceptable
- Fail: Insufficient reduction or excessive overhead, adjust approach

### Testing Protocol

**Phase 1: Before Compression**
- Document baseline (tokens, structure, purposes)
- Identify validation criteria
- Define success metrics
- Establish test scenarios

**Phase 2: After Compression**
- Measure token reduction
- Test functional completion
- Assess comprehension
- Verify preservation

**Phase 3: Comparative Analysis**
- Compare to targets
- Identify gaps or issues
- Document lessons learned
- Refine approach if needed

**Phase 4: Production Validation**
- Monitor actual usage
- Track information loss incidents
- Gather user feedback
- Iterate based on evidence

### Success Criteria

**Must Pass:**
- ✓ All intended purposes accomplished
- ✓ Critical information preserved
- ✓ Appropriate audiences comprehend
- ✓ No information loss detected

**Should Pass:**
- ✓ Compression target achieved (within ±10%)
- ✓ ROI meets expectations
- ✓ Validation efficient (low overhead)
- ✓ User satisfaction positive

**Nice to Have:**
- ✓ Exceeds compression targets
- ✓ Exceeds ROI expectations
- ✓ Positive user feedback
- ✓ Reusable patterns identified

---

## Section 12: Summary and Key Takeaways

### Core Principle

**Cannot compress along single dimension.** Must consider [Role × Layer × Phase × Mode] simultaneously. Multi-dimensional matrix operationalizes this complexity with quantitative targets and decision processes.

### Key Insights

**1. Base Matrix Provides Foundation**
- [Role × Layer] gives starting target
- Ranges accommodate variation
- Patterns emerge (Coordinator lowest, Orchestrator highest)

**2. Phase Adjustments are Critical**
- Ideation needs space (-20 to -30%)
- Build enables efficiency (+10 to +20%)
- Archive transitions aggressive (+20 to +30%)
- Phase awareness prevents premature compression

**3. Multi-Role Documents are Common**
- Union: Safe, conservative (divergence <20%)
- Intersection: Optimized (clear primary)
- Layered: Flexible (divergence >40%)
- Strategy selection matters

**4. Overrides Exist for Good Reasons**
- Archive (L5): Always 95-99%
- Ideation: Always low (max 30%)
- Session (L4): Always aggressive (60-85%)
- Compliance: Always preserved (20-30%)

**5. Mode-Switching Affects Compression**
- High switching (Maintainer): Lower compression
- Low switching (Developer): Higher compression
- Unified vs separate documents trade-off

**6. Validation is Essential**
- Test with real users/LLMs
- Verify all purposes served
- Monitor information loss
- Iterate based on evidence

### Usage Summary

**For any compression decision:**

1. Identify [Role × Layer × Phase]
2. Look up base target in matrix
3. Apply phase adjustment
4. Check for overrides (L5/Ideation/L4)
5. Handle multi-role if applicable
6. Adjust for mode-switching
7. Select appropriate methods
8. Validate comprehensively
9. Document and monitor

### Integration with Framework

**This matrix operationalizes:**
- Documentation Types Matrix (WHO) → Roles
- Information Preservation Framework (WHY) → Purposes to preserve
- CC_Projects Validated Architecture (WHAT/WHEN) → Layers and Phases

**Together they provide:**
- Quantitative targets (matrix)
- Preservation requirements (framework)
- Evidence-based validation (architecture)
- Practical application (this guide)

### What This Enables

**Before matrix:** "Compress based on audience... somehow"

**After matrix:** "Developer accessing Operational during Build with high-frequency access = 60-75% compression using structural methods"

**Value:** Explicit, repeatable, evidence-based compression decisions

---

## Section 13: Next Steps and Future Work

### Immediate Applications

**1. Apply to CC_Projects Documents (when ready)**
- SESSION.md compression (70-85% target validated)
- PROJECT.md multi-role handling (20-40% with role views)
- TASKS.md optimization (60-75% for developer focus)
- Archive strategy (95-99% for completed sessions)

**2. Validate Empirically**
- Test targets against real documents
- Measure actual compression achieved
- Assess information preservation
- Refine matrix based on evidence

**3. Create Document Specifications**
- Apply matrix to each CC_Projects document type
- Document role-specific requirements
- Establish compression standards
- Provide implementation guidance

### Framework Enhancements Still Needed

**From Alignment Review remaining gaps:**

1. **Phase-Aware Guidance** (Session 2)
   - Expand Information Preservation Framework
   - Add phase-specific recommendations
   - Document phase transitions
   - Anti-compression patterns

2. **Multi-Role Patterns Detail** (Session 3)
   - Expand multi-role strategies
   - More worked examples
   - Cost/benefit analysis
   - Implementation templates

3. **Archive Compression Methods** (Session 4)
   - Ultra-aggressive techniques (95-99%)
   - Conversational compression details
   - Search optimization
   - Reconstruction trade-offs

4. **Tool Integration** (Session 5)
   - Format compatibility
   - Git workflows
   - Automation opportunities
   - Human-in-the-loop processes

### Research Questions

**To answer empirically:**
- Are matrix targets achievable in practice?
- Where are practical limits?
- What patterns emerge from testing?
- Do adjustments need refinement?

**To explore:**
- Automated compression based on matrix?
- Dynamic adjustment based on access patterns?
- Machine learning for target optimization?
- Real-time compression/decompression?

---

## References

### Source Documents

**1. CC_Projects Validated Architecture**
- H1: 5-phase lifecycle (100% clear transitions)
- H2: 6 roles with distinct needs
- H3: 5-layer architecture (90% clear assignment)
- H4: Scalability validation (sweet spot: Small-Medium projects)

**2. Documentation Types Matrix**
- 6 audience categories with compression targets
- Technical literacy distinctions
- Comprehension requirements

**3. Information Preservation Framework**
- 7 documentation purposes
- Essential information mapping
- Preservation decision matrices

**4. CC_Projects Alignment Review**
- Systematic validation of framework
- 6 critical gaps identified
- Integration requirements documented

### Related Patterns (To Be Created)

- Multi-Role Document Strategies (Session 3)
- Phase-Aware Compression Guide (Session 2)
- Archive Compression Methods (Session 4)
- Tool Integration Guide (Session 5)

---

## Document Status

**Created:** 2025-10-30 AEDT  
**Status:** Session 1 refinement complete  
**Purpose:** Operationalize multi-dimensional compression decisions  
**Gap Addressed:** Multi-dimensional decision framework (HIGH priority) ✓

**Coverage:**
- ✓ Three dimensions explained (Role, Layer, Phase)
- ✓ Base compression target matrix [Role × Layer]
- ✓ Phase adjustment guidance
- ✓ Multi-role document strategies
- ✓ Conflict resolution process
- ✓ Mode-switching overhead
- ✓ 6 worked examples
- ✓ Edge cases addressed
- ✓ Integration with framework
- ✓ Practical application guide
- ✓ Best practices
- ✓ Validation approach

**Total Length:** ~880 lines

**Next:** Session 2 - Phase-Aware Enhancement to Information Preservation Framework

---

**Multi-Dimensional Compression Matrix: Complete**