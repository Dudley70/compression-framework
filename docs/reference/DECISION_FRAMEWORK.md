---
title: Compression Decision Framework
created: 2025-11-06
updated: 2025-11-06
status: active
category: reference
version: 1.0
compression_level: moderate
audience: technical
purpose: framework_reference
---

# Compression Decision Framework

**Purpose**: Practical guidance for making compression decisions across [Role × Layer × Phase] dimensions with ROI prioritization, anti-patterns, and edge cases.

**Audience**: Technical teams implementing compression framework  
**Scope**: Decision-making guidance, not technique specifications (see TECHNIQUES.md)

---

## Quick Start

**Simple Decision Path**:
1. Check if document is in **Archive** (Layer 5) → Use 95-99% compression
2. Check if phase is **Ideation** → Use 10-30% compression maximum
3. Check if document is **Session** (Layer 4) → Use 60-85% compression
4. Otherwise → Use Base Compression Matrix (Section 6)

**For Multi-Role Documents**: See Section 3 for Union/Intersection/Layered strategies

**For Team-Specific Guidance**: See Section 4 for team size adjustments

**For Edge Cases**: See Section 5 for legal/emergency/external overrides

**For Decision-Support Documents**: See Section 8 for operational guidance preservation

---

## Table of Contents

1. Phase-Based Compression Guidelines
2. ROI-Based Prioritization
3. Multi-Role Document Strategies
4. Team-Size Considerations
5. Edge Cases and Overrides
6. Base Compression Matrix
7. Common Pitfalls
8. Decision-Support Compression Methodology

---

## 1. Phase-Based Compression Guidelines

### Overview

Compression appropriateness varies by project phase. The same document requires different compression at different lifecycle stages - aggressive compression during Build phase can be counterproductive during Ideation.

### Phase Compression Targets

| Phase | Target Range | Rationale | Key Focus |
|-------|-------------|-----------|-----------|
| **Research** | 10-20% | Preserve evidence depth | Organization > reduction |
| **Ideation** | 10-30% | Creativity needs space | Don't kill ideas prematurely |
| **Refinement** | 20-40% | Preserve decision rationale | Keep "why not X" answers |
| **Structure** | 30-50% | Clarity over brevity | Format optimization |
| **Build** | 50-70% | Execution efficiency | High-ROI operational focus |
| **Maintain - Active** | 40-60% | Balance history + efficiency | Ongoing changes |
| **Maintain - Archive** | 95-99% | Ultra-aggressive | Rare access, storage optimization |

### Rationale Preservation Strategy

During **Refinement phase**, preserve decision context with graduated detail:

**Selected Approach** (0% compression):
- Full implementation detail required
- Complete technical specifications
- Comprehensive design rationale

**Seriously Considered Alternatives** (30-50% compression):
- Key rejection rationale preserved
- Main trade-offs documented
- "Why not X" answers clear

**Briefly Evaluated Alternatives** (70-85% compression):
- One-line dismissal sufficient
- Minimal context needed
- Just enough for searchability

**Never Considered**: Don't document

### Phase Transition Rules

As documents move through lifecycle, apply progressive compression:

**Active → Complete** (+15-25% additional compression):
- Summarize outcomes
- Maintain searchability
- Reduce operational detail
- Example: 40% → 55-65% compression

**Complete → Archive** (+30-50% additional compression):
- Total 95-99% compression
- Metadata + searchability only
- Ultra-aggressive reduction
- Example: 65% → 95-99% compression

### Document State Lifecycle

```
┌─────────────┐  Working on it   ┌──────────────┐  Finished     ┌─────────────┐
│   ACTIVE    │ ────────────────> │   COMPLETE   │ ───────────> │   ARCHIVE   │
│ Phase-aware │  Phase targets    │  +15-25%     │  +30-50%     │  95-99%     │
│ compression │                   │  compression │  compression │  total      │
└─────────────┘                   └──────────────┘              └─────────────┘
```

### Application Guidelines

**During Research/Ideation**:
- ✅ Organize and structure information
- ✅ Preserve all findings and ideas
- ❌ Don't aggressively compress
- ❌ Don't eliminate "unnecessary" detail

**During Build/Maintain**:
- ✅ Apply aggressive compression (50-70%)
- ✅ Optimize for execution efficiency
- ✅ Use structured formats (LSC techniques)
- ✅ Prioritize session startup documents

**When Transitioning Phases**:
- Review compression appropriateness
- Adjust targets based on new phase
- Archive completed work aggressively
- Don't compress future work prematurely

---

## 2. ROI-Based Prioritization

### The ROI Formula

```
ROI = (Token Reduction × Access Frequency) / Compression Effort

High ROI = High frequency + Good compression potential + Low effort
Low ROI = Low frequency OR poor compression OR high effort
```

### Session Startup = Highest ROI

**Critical Insight**: Small reductions in high-frequency documents create massive cumulative impact.

**Example - SESSION.md**:
- Baseline: ~2,000 tokens (verbose operational documentation)
- Target: ~300 tokens (85% reduction)
- Frequency: 5-20 loads per day
- **Daily savings**: 7,000-34,000 tokens
- Implementation: One-time template design
- **ROI: HIGHEST POSSIBLE**

### Frequency Impact Analysis

| Frequency | Examples | Cumulative Impact | Priority |
|-----------|----------|-------------------|----------|
| **Every session** | SESSION.md, PROJECT.md | CRITICAL | HIGHEST |
| **Daily** | TASKS.md, build configs | HIGH | HIGH |
| **Weekly** | Sprint docs, status reports | MEDIUM | MEDIUM |
| **Monthly** | Strategic reviews, metrics | LOW-MEDIUM | MEDIUM |
| **Rarely** | Historical decisions, archive | MINIMAL | LOW |

### Priority Scoring System

**Calculate priority score**:
```
Priority = (Frequency × Compression_Potential × Size) / Implementation_Effort

Frequency points:    Every session=10, Daily=7, Weekly=4, Monthly=2, Rarely=1
Compression points:  High (60-85%)=10, Moderate (40-60%)=6, Low (20-40%)=3
Size points:         Very large (>2000)=10, Large (1000-2000)=6, 
                     Medium (500-1000)=3, Small (<500)=1
Effort points:       Low (template)=10, Medium=6, High=3, Very high=1 (divider)
```

**Example Calculations**:
- **SESSION.md**: (10 × 10 × 6) / 6 = **100** → HIGHEST PRIORITY
- **TASKS.md**: (7 × 10 × 3) / 10 = **21** → HIGH PRIORITY
- **DECISIONS.md**: (2 × 3 × 3) / 6 = **3** → MEDIUM PRIORITY
- **Archive logs**: (1 × 10 × 6) / 3 = **2** → LOW-MEDIUM PRIORITY

### Three-Phase Implementation Strategy

**Phase 1: High-Impact Quick Wins**
- **Target**: Session startup + high-frequency operational
- **Documents**: SESSION.md (score: 100), PROJECT.md (60-80), TASKS.md (21)
- **Why first**: Highest cumulative token impact, immediate ROI, framework validation
- **Timeline**: Week 1-2

**Phase 2: Medium-Impact Systematic**
- **Target**: Strategic and control layer documents
- **Documents**: Configs, decision logs, architecture docs, planning documents
- **Why second**: Moderate frequency, systematic patterns, comprehensive coverage
- **Timeline**: Week 3-6

**Phase 3: Archive Optimization**
- **Target**: Historical and completed documents
- **Documents**: Completed logs, archived decisions, old projects
- **Why last**: Low token impact (rare access), high storage benefit, lower urgency
- **Timeline**: Week 7+

### Validation Rigor by Impact

Scale validation effort to match stakes:

**CRITICAL** (session startup, score >50):
- Functional testing required
- LLM must successfully resume work
- Test with actual workflows
- Monitor for errors closely

**HIGH** (daily operational, score 20-50):
- Task completion testing
- Verify execution success
- Spot-check comprehension
- Weekly monitoring

**MEDIUM** (strategic/reference, score 5-20):
- Purpose-based validation
- Comprehension spot-checks
- Monthly reviews sufficient

**LOW** (archive, score <5):
- Searchability testing only
- Reconstruction acceptable if needed
- Minimal monitoring required

---

## 3. Multi-Role Document Strategies

### The Problem

Many documents serve multiple roles with different compression needs:
- **DECISIONS.md**: Coordinator (oversight) + Maintainer (historical understanding)
- **PROJECT.md**: All roles accessing at different depths
- **TASKS.md**: Developer (execution) + Coordinator (status tracking)

### Strategy 1: Union of Requirements (Most Conservative)

**When to Use**: Critical documents, multiple important purposes, high preservation needs

**Process**:
1. Identify all roles accessing document
2. Calculate compression target for each role
3. Select LOWEST compression (highest preservation)
4. Apply to entire document

**Example - DECISIONS.md**:
- Coordinator + Strategic + Research: 20-30% - 10-20% phase = **10-20%**
- Maintainer + Strategic + Maintain: 30-40% + 0% phase = **30-40%**
- **Union result**: Use **10-20%** (lowest, highest preservation)

**Trade-off**: Conservative, may over-preserve, but safe for critical content

### Strategy 2: Intersection (Most Aggressive)

**When to Use**: High-frequency documents, clear primary role, secondary roles optional

**Process**:
1. Identify primary role (highest access frequency)
2. Calculate target for primary role
3. Apply aggressive compression
4. Provide alternate representations for secondary roles if needed

**Example - TASKS.md**:
- Developer + Operational + Build: 40-50% + 10-20% = **50-70%** (PRIMARY)
- Coordinator + Operational + Build: 40-50% + 10-20% = 50-70% (SECONDARY)
- **Intersection result**: Use **50-70%** (optimized for primary)
- **Secondary accommodation**: Coordinator gets separate summary view

**Trade-off**: Optimizes for primary user, may require multiple representations

### Strategy 3: Layered Representation (Most Flexible)

**When to Use**: Complex documents, significant role divergence (>40% difference), optimization justified by benefits

**Process**:
1. Create role-specific views of same content
2. Compress each view for its target role
3. Share common base, generate views as needed

**Example - PROJECT.md**:
- **Coordinator view**: 20-30% compression (strategic summary + status)
- **Developer view**: 50-60% compression (operational focus only)
- **Architect view**: 30-40% compression (design rationale preserved)
- **Maintainer view**: 30-40% compression + archive links

**Implementation**: 
- Single source document
- View generation via templates or filters
- Each role loads appropriate view

**Trade-off**: Most flexible but higher maintenance overhead (multiple representations)

### Multi-Role Decision Framework

**Step 1: Analyze Access Patterns**
- Who accesses most frequently?
- What's the primary purpose?
- Are role needs similar or divergent?
- Calculate compression difference between roles

**Step 2: Calculate Divergence**
```
Divergence = |Role1_Target - Role2_Target|

Example:
Coordinator (20%) vs Developer (50%) = 30% divergence
```

**Step 3: Select Strategy**

| Role Divergence | Access Pattern | Recommendation |
|-----------------|----------------|----------------|
| Low (<20%) | Any | Union (simple, adequate) |
| Medium (20-40%) | Clear primary | Intersection + summary |
| High (>40%) | Balanced access | Layered views |
| High (>40%) | Clear primary | Intersection + separate docs |

**Step 4: Validate**
- Can all roles accomplish their purposes?
- Is information preservation adequate?
- Is overhead justified by benefits?
- Test with actual workflows

### When to Use Each Strategy

**Use Union when**:
- Document is critical to all roles
- Preservation is more important than optimization
- Simple approach preferred
- Role needs don't diverge significantly (<20%)

**Use Intersection when**:
- Clear primary role exists (>80% of access)
- Secondary roles can use summaries
- High-frequency document justifies optimization
- Medium divergence (20-40%)

**Use Layered when**:
- High divergence (>40%) between roles
- Multiple important roles (no clear primary)
- Optimization benefits justify maintenance cost
- Document accessed frequently enough to matter

---

## 4. Team-Size Considerations

### Team Size Categories

| Team Size | Characteristics | Documentation Priority |
|-----------|----------------|------------------------|
| **Solo / Very Small (1-3)** | High role overlap, wear multiple hats | Readability > optimization |
| **Small (4-8)** | Some specialization, 2-3 devs + coordinator | Balance role needs |
| **Medium (9-15)** | Clear specialization, dedicated roles | Optimize for roles |
| **Large (16+)** | High specialization, minimal overlap | Aggressive role optimization |

### Compression Target Adjustments

**Solo / Very Small Teams (1-3 people)**:
```
Adjustments:
- LLM-only: 60-75% (vs 70-85% standard) - favor readability
- Hybrid-Technical: 30-50% (vs 40-60%) - less aggressive
- Multi-role: Union strategy - single narrative for all roles

Rationale:
- Context switching cost > token savings
- Individual reads all roles
- Personal memory supplements docs
- Minimal handover overhead

Example: Don't create separate strategic/technical/operational sections
```

**Small Teams (4-8 people)**:
```
Adjustments:
- LLM-only: 65-80% (approaching standard)
- Hybrid-Technical: 35-55% (light optimization)
- Multi-role: Intersection strategy (primary + accommodations)
- Layered: SESSION.md and PROJECT.md only (highest frequency)

Rationale:
- Some specialization justifies optimization
- Still need cross-role comprehension
- Coordination overhead increasing

Example: Primary Developer detail, Secondary Coordinator inline status
```

**Medium Teams (9-15 people)**:
```
Adjustments:
- LLM-only: 70-85% (full framework targets)
- Hybrid-Technical: 40-60% (standard optimization)
- Multi-role: Full divergence thresholds (use framework exactly)
- Layered: 3-5 critical documents (justified for high-frequency)

Rationale:
- Role specialization high enough
- Token savings compound across team
- Coordination complexity requires optimization

Example: Layered PROJECT.md: Strategic (70%) → Architect (50%) → Dev (35%)
```

**Large Teams (16+ people)**:
```
Adjustments:
- LLM-only: 75-85% (aggressive end of range)
- Hybrid-Technical: 45-60% (upper range)
- Multi-role: Layered standard (most shared docs)
- Archive: 95-99% critical (volume management)

Rationale:
- High specialization enables aggressive optimization
- Documentation volume high (storage costs)
- Coordination complexity requires role optimization

Example: Separate docs by role: Architecture/ Development/ Operations/
```

### Role Overlap Decision Framework

```
Calculate Role Overlap:
  Single person wearing N roles → High overlap (>70%)
  N people each wearing 1 role → No overlap (<30%)

Apply Strategy:
  If Overlap > 70%:
    - Union strategy (single representation)
    - Lower compression targets (readability priority)
    - Minimize role-specific optimization

  If Overlap 30-70%:
    - Intersection strategy (primary + accommodations)
    - Standard compression targets
    - Moderate role optimization

  If Overlap < 30%:
    - Layered strategy (role-specific views)
    - Aggressive compression targets
    - Full role-specific optimization
```

### Token Savings Scale with Team Size

**Annual impact calculation**:
```
Savings = People × Token_Reduction × Sessions_Per_Year
```

**Example: PROJECT.md optimization (1,000 tokens/session, 50 sessions/year)**:

| Team Size | People | Annual Savings | ROI Assessment |
|-----------|--------|----------------|----------------|
| Solo | 1 | 50K tokens | Low - minimal value |
| Small | 5 | 250K tokens | Moderate - justified |
| Medium | 12 | 600K tokens | Significant - important |
| Large | 25 | 1.25M tokens | Critical - essential |

### Layered Strategy ROI Analysis

**Maintenance overhead**: ~15 hours/year per layered document

**Solo Team**:
- Savings: 50K tokens (minimal value)
- Cost: 15 hours maintenance
- **Result**: NEGATIVE ROI - not justified
- **Recommendation**: Don't use layered strategy

**Medium Team**:
- Savings: 600K tokens (significant value)
- Cost: 15 hours maintenance
- **Result**: POSITIVE ROI - justified
- **Recommendation**: Use for 3-5 critical docs

**Large Team**:
- Savings: 1.25M tokens (critical value)
- Cost: 15 hours maintenance
- **Result**: STRONGLY POSITIVE ROI - essential
- **Recommendation**: Standard for shared docs

### Application Guidelines

**For Solo/Small Teams**:
- Favor simplicity and readability
- Use Union strategy for multi-role docs
- Focus on highest-frequency docs only
- Don't over-engineer role separation

**For Medium Teams**:
- Balance optimization with maintainability
- Use layered strategy for 3-5 critical docs
- Apply standard compression targets
- Justify each optimization decision

**For Large Teams**:
- Aggressive optimization justified
- Layered strategy for most shared docs
- Role-specific documentation encouraged
- Volume management becomes critical

---

## 5. Edge Cases and Overrides

### Overview

Real-world constraints may override standard compression guidance. Legal requirements, emergency access needs, external collaboration, and other edge cases require special handling with systematic framework for deviations.

### Five Edge Case Types

**1. Compliance and Audit Requirements**

**Constraint**: Legal, regulatory, or audit mandates  
**Compression Limit**: 0-40% maximum

**Requirements**:
- Retain full unmodified originals (required retention period)
- Create compressed working copies only (for daily use)
- Maintain keyword index (for legal discovery)
- Legal review before any compression
- **Never compress legal documents** (0%)
- Audit trails: 0-20% (structured only, lossless)

**Examples**: SOX audit trails, GDPR records, HIPAA logs, security incidents

**2. Emergency Access Scenarios**

**Constraint**: Time-critical access during incidents/outages  
**Compression Limit**: 0-10% maximum

**Requirements**:
- Human-readable format (no LSC)
- Step-by-step instructions (no abbreviation)
- Multiple redundant locations
- Printed backup copies for critical procedures
- Test regularly under stress conditions
- Prioritize accessibility over token efficiency

**Examples**: Runbooks, incident response, disaster recovery, emergency contacts

**Challenge**: Ultra-compressed docs may not be accessible fast enough, LLM may be unavailable

**3. Multi-Project Shared Documentation**

**Constraint**: Documents used across multiple projects with different needs  
**Compression Limit**: 20-40% (lowest common denominator)

**Strategies**:
- **Option A - Single Version**: Optimize for least-compression-tolerant project  
  When: <5 projects, similar audiences
- **Option B - Multi-Version**: Create versions with shared core  
  When: 10+ projects OR very diverse audiences
- **Option C - Layered**: Project-specific sections  
  When: 5-10 projects, diverse audiences

**Examples**: Technical standards, architecture patterns, platform APIs, reusable components

**4. External Collaboration**

**Constraint**: Shared with external partners, contractors, open-source community  
**Compression Limit**: 0-20% maximum

**Requirements**:
- Assume human-readable only (LLM use optional)
- Traditional markdown with examples
- No internal abbreviations or assumptions
- Explain all technical terms
- Step-by-step with screenshots
- Plain language for general audiences

**Examples**: API docs for external devs, integration guides, client specs, open-source documentation

**Challenge**: No control over recipient's tools, no LLM assumption, variable technical literacy

**5. Long-Term Archival (10+ years)**

**Constraint**: Must be preserved for decades beyond normal timeframe  
**Compression Limit**: 40-60% (moderate only)

**Requirements**:
- Plain text or markdown (not LSC or proprietary)
- Standard metadata (JSON/YAML)
- 5-year review cycle (format migration as needed)
- Avoid ultra-aggressive compression (95-99% too risky)
- Favor format longevity over token efficiency

**Examples**: Historical company records, long-term research, legal archives, foundational architecture decisions

**Challenge**: Format longevity, future accessibility, technology evolution uncertain

### Override Priority Framework

**Priorities from highest to lowest**:

```
1. Legal/Compliance Requirements → ALWAYS override token efficiency
   Risk: Regulatory violations, legal penalties
   Cost: >>> storage savings

2. Safety/Emergency Access → Human life or critical systems
   Risk: Delayed response, system failures
   Cost: >> compression benefits

3. External Obligations → Contractual or partnership commitments
   Risk: Partnership damage, contract breach
   Cost: > optimization gains

4. Long-Term Preservation → Format longevity over current optimization
   Risk: Information loss over decades
   Cost: = acceptable trade-off

5. Standard Framework → Default guidance when no overrides apply
   Risk: Minimal (validated approach)
   Cost: Normal compression benefits
```

### Decision Tree for Edge Case Handling

```
For each document, check in order:

1. Is document subject to legal/compliance requirements?
   YES → Follow compliance limits (0-40%)
         Legal review required
         Preserve originals
         STOP (highest priority)
   NO → Continue to 2

2. Is document needed for emergency access?
   YES → Human-readable format (0-10%)
         Multiple locations
         Test under stress
         STOP (safety priority)
   NO → Continue to 3

3. Is document shared externally (partners/clients/open-source)?
   YES → Human-readable, low compression (0-20%)
         Explain everything
         No internal assumptions
         STOP (external obligation)
   NO → Continue to 4

4. Is document for 10+ year archival?
   YES → Format longevity priority (40-60%)
         Plain text/markdown
         5-year review cycle
         STOP (long-term preservation)
   NO → Continue to 5

5. Apply standard framework guidance
   → Use Base Compression Matrix (Section 6)
   → Consider multi-role strategies (Section 3)
   → Apply phase adjustments (Section 1)
```

### Edge Case Compression Limits Summary

| Edge Case | Max Compression | Format | Key Constraint |
|-----------|----------------|--------|----------------|
| Compliance/Audit | 0-40% | Original + copy | Legal requirements |
| Emergency Access | 0-10% | Human-readable | Time-critical, stress |
| Multi-Project | 20-40% | Lowest common denominator | Diverse audiences |
| External | 0-20% | Traditional markdown | Unknown tooling |
| Long-Term (10+ years) | 40-60% | Plain text/markdown | Format longevity |

### Warning Principle

> "When in doubt about edge case applicability, err on side of caution.  
> Legal risk or emergency access failure costs more than token savings."

---

## 6. Base Compression Matrix

### The Three Dimensions

**Dimension 1: Role** (WHO accesses)
- **Coordinator**: Project oversight, workflow orchestration  
  Information needs: High-level summaries, strategic context
- **Analyst**: Research, investigation, requirements  
  Information needs: Deep research access, evidence trails
- **Architect**: Design decisions, technical structure  
  Information needs: Strategic principles, design rationale
- **Developer**: Implementation, coding, unit testing  
  Information needs: Operational details, clear requirements
- **Maintainer**: Evolution, optimization, support  
  Information needs: Comprehensive system understanding, historical decisions
- **Orchestrator**: Multi-agent coordination, workflow automation  
  Information needs: Meta-level structure, agent configurations

**Dimension 2: Layer** (WHAT is documented)
- **L1 Strategic**: Vision, decisions, principles (PROJECT.md, DECISIONS.md)
- **L2 Control**: Configuration, modes, skills (CLAUDE.md, settings)
- **L3 Operational**: Active work, tasks (TASKS.md, work-in-progress)
- **L4 Session**: Ephemeral state, handovers (SESSION.md)
- **L5 Archive**: Historical records (archive/completed documents)

**Dimension 3: Phase** (WHEN accessed)
- See Section 1 for phase-specific adjustments

### Base Compression Targets

**Compression percentage = how much to reduce (40% = reduce to 60% of original)**

| Role | L1: Strategic | L2: Control | L3: Operational | L4: Session | L5: Archive |
|------|--------------|-------------|-----------------|-------------|-------------|
| **Coordinator** | 20-30% | 30-40% | 40-50% | 60-70% | 95-97% |
| **Analyst** | 25-35% | 35-45% | 35-45% | 60-70% | 95-97% |
| **Architect** | 30-40% | 40-50% | 40-50% | 65-75% | 95-97% |
| **Developer** | 40-50% | 40-50% | 40-50% | 70-80% | 95-97% |
| **Maintainer** | 30-40% | 40-50% | 40-50% | 65-75% | 95-99% |
| **Orchestrator** | 60-70% | 50-60% | 60-70% | 75-85% | 97-99% |

### Key Patterns

**By Layer**:
- **Strategic** (L1): Lower compression - rationale preservation critical
- **Session** (L4): Higher compression - high frequency, machine-first
- **Archive** (L5): Ultra-aggressive - rare access, searchability priority

**By Role**:
- **Coordinator**: Lowest compression - needs context and breadth
- **Developer**: Moderate-high - execution-focused, structured needs
- **Orchestrator**: Highest compression - machine-first, automation-focused

### Phase Adjustments

Apply these multipliers to base matrix targets:

| Phase | Adjustment | Example |
|-------|------------|---------|
| Research | -10 to -20% | 40% → 20-30% |
| Ideation | -20 to -30% | 40% → 10-20% |
| Refinement | -10 to -15% | 40% → 25-30% |
| Structure | ±0% | 40% → 40% |
| Build | +10 to +20% | 40% → 50-60% |
| Maintain - Active | ±0 to +10% | 40% → 40-50% |
| Maintain - Archive | +20 to +30% | Move to L5, 95-99% |

### Example Calculations

**Architect accessing Strategic during Ideation**:
- Base: 30-40% compression
- Phase: Ideation (-20 to -30%)
- **Result**: 10-20% compression (preserve creative space)

**Developer accessing Operational during Build**:
- Base: 40-50% compression
- Phase: Build (+10 to +20%)
- **Result**: 50-70% compression (aggressive, task-focused)

**Maintainer accessing Strategic during Maintain (archive)**:
- Base: 30-40% compression
- Phase: Maintain-Archive (+20 to +30%)
- **Result**: Move to L5 Archive, 95-99% compression

### Conflict Resolution

**Priority rules when dimensions conflict**:

1. **Archive Layer (L5)**: Always 95-99%, overrides all other considerations
2. **Ideation Phase**: Always low (10-30% max), overrides role/layer
3. **Session Layer (L4)**: Always aggressive (60-85%), overrides role
4. **Multi-role preservation**: Apply Section 3 strategies
5. **Base matrix**: Default when no overrides apply

**Decision tree** (from Section 5) applies edge cases before base matrix.

---

## 7. Common Pitfalls

### Overview

Negative guidance prevents common compression mistakes. These seven anti-patterns show what NOT to do and why compression can be counterproductive in certain situations.

### Seven Anti-Compression Patterns

**1. Active Ideation**

❌ **Don't**: Compress during brainstorming or concept development  
✅ **Do**: Organize and structure only, preserve all ideas  
**Why**: Creativity requires space, premature compression kills divergent thinking  
**Indicator**: Team exploring multiple approaches, generating concepts  

**Example**: Don't eliminate "unnecessary" alternative approaches during brainstorming - they provide creative context.

---

**2. Active Research**

❌ **Don't**: Aggressively compress during investigation  
✅ **Do**: Preserve all findings, compress after synthesis  
**Why**: Evidence depth critical, can't predict what's important yet  
**Indicator**: Heavy information gathering, discovery phase  

**Example**: Don't compress research notes to "key findings only" - full evidence trail may be needed later.

---

**3. Rapid Iteration**

❌ **Don't**: Compress during fast pivots or frequent changes  
✅ **Do**: Wait for stabilization, then compress  
**Why**: Overhead of re-compression exceeds benefit  
**Indicator**: Frequent document changes, approach uncertainty  

**Example**: If document changes 5x per day, compression effort wasted - wait for design to stabilize.

---

**4. Uncertain Requirements**

❌ **Don't**: Strip "unnecessary" detail when requirements unclear  
✅ **Do**: Preserve detail until requirements clarify  
**Why**: May need that "unnecessary" detail when requirements change  
**Indicator**: Ambiguous specs, evolving understanding  

**Example**: Don't remove edge case handling details if requirements might expand to cover those cases.

---

**5. Learning-Critical Content**

❌ **Don't**: Strip rationale from onboarding/educational documents  
✅ **Do**: Preserve learning value over brevity  
**Why**: Understanding "why" is the point, not just "what"  
**Indicator**: Onboarding docs, training materials, concept explanations  

**Example**: Tutorial explaining authentication should keep "why JWT over sessions" rationale, not just "use JWT".

---

**6. Emergency-Critical Documents**

❌ **Don't**: Archive so aggressively that emergency access fails  
✅ **Do**: Keep emergency procedures accessible even in archive  
**Why**: Reconstruction time unacceptable in emergency  
**Indicator**: Incident response, disaster recovery, critical procedures  

**Example**: Incident runbook compressed to 99% means team can't respond quickly during outage.

---

**7. Compliance-Required Records**

❌ **Don't**: Compress beyond legal/regulatory requirements  
✅ **Do**: Preserve complete audit trail regardless of phase  
**Why**: Compliance violations cost more than storage  
**Indicator**: Regulated industries, audit trails, legal requirements  

**Example**: HIPAA-regulated patient interaction logs must preserve complete details even if rarely accessed.

### General Anti-Compression Principle

> **"When compression overhead exceeds compression benefit, don't compress."**

This applies when:
- Effort to compress > token savings value
- Re-compression frequency too high
- Information loss risk > storage cost
- Access pattern doesn't justify optimization

### Indicators of Premature Compression

**Warning signs that compression was too aggressive or too early**:

- ❌ Frequent decompression requests ("can you show me the full version?")
- ❌ Information loss incidents ("we removed that detail last month")
- ❌ Rework due to missing context ("if only we'd kept that rationale...")
- ❌ Complaints about missing detail ("I can't understand this compressed version")
- ❌ Context recovery attempts ("let me check the git history for what was removed")
- ❌ Team asking "why did we remove X?" repeatedly

**If you see these patterns**: Reduce compression aggressiveness or delay compression until document stabilizes.

### When to Delay Compression

**Delay compression if**:
- Document changes >2x per week
- Requirements still evolving
- Team is in ideation/research phase
- Multiple stakeholders haven't reviewed yet
- Legal/compliance requirements unclear
- Emergency access scenarios possible

**Safe to compress when**:
- Document stable (changes <1x per month)
- Requirements clear and validated
- Team in build/maintain phase
- Stakeholders have approved content
- Legal review complete (if applicable)
- Access patterns established

### Checklist Before Compressing

Use this checklist to avoid anti-patterns:

- [ ] Document is NOT in active ideation phase
- [ ] Document is NOT in active research phase
- [ ] Changes are infrequent (< 2x per week)
- [ ] Requirements are clear and stable
- [ ] Document is NOT learning-critical
- [ ] Document is NOT emergency-critical
- [ ] Compliance requirements verified
- [ ] Access patterns justify optimization
- [ ] Compression effort < expected benefit
- [ ] Stakeholders have reviewed and approved

**If any item fails**: Consider delaying compression or reducing aggressiveness.

---

## Summary and Quick Reference

### Decision Flow

```
1. Check Edge Cases (Section 5)
   → Legal/Emergency/External/Long-term?
   → YES: Use edge case limits, DONE
   → NO: Continue

2. Check Phase (Section 1)
   → Ideation: 10-30% max, DONE
   → Archive: Move to L5, 95-99%, DONE
   → Other: Continue

3. Check Layer (Section 6)
   → Session (L4): 60-85%, DONE
   → Archive (L5): 95-99%, DONE
   → Other: Continue

4. Apply Base Matrix (Section 6)
   → Look up [Role × Layer]
   → Apply phase adjustments
   → Continue if multi-role

5. Handle Multi-Role (Section 3)
   → Calculate divergence
   → Select strategy (Union/Intersection/Layered)
   → Apply team size considerations (Section 4)

6. Validate Against Pitfalls (Section 7)
   → Check anti-patterns
   → Verify checklist
   → Proceed with compression
```

### Key Principles

**1. Phase Awareness** (Section 1)
- Ideation/Research: Low compression (10-30%)
- Build/Maintain: High compression (50-70%)
- Archive: Ultra-aggressive (95-99%)

**2. ROI Prioritization** (Section 2)
- Session startup = highest ROI
- Frequency × Reduction × Size / Effort
- Prioritize high-frequency documents first

**3. Multi-Role Flexibility** (Section 3)
- Low divergence (<20%): Union
- Medium divergence (20-40%): Intersection
- High divergence (>40%): Layered

**4. Team Scaling** (Section 4)
- Solo: Readability > optimization
- Medium: Standard targets
- Large: Aggressive optimization

**5. Edge Case Safety** (Section 5)
- Legal/Compliance: Always override
- Emergency: 0-10% max
- External: 0-20% max

**6. Anti-Pattern Awareness** (Section 7)
- When overhead > benefit, don't compress
- Watch for warning signs
- Use validation checklist

### Common Scenarios

**Scenario: SESSION.md for medium dev team**
- Role: Developer (primary)
- Layer: L4 Session
- Phase: Build
- Calculation: Base 70-80% + Build adjustment = 70-80%
- Multi-role: Developer primary, Coordinator gets summary
- **Result: 70-80% compression** (LSC format, structured)

**Scenario: DECISIONS.md during ideation**
- Role: Multiple (Coordinator + Architect)
- Layer: L1 Strategic
- Phase: Ideation
- Check: Ideation overrides → 10-30% max
- **Result: 10-20% compression** (preserve creative reasoning)

**Scenario: API docs for external partners**
- Edge case: External collaboration
- Limit: 0-20% maximum
- Format: Human-readable markdown
- **Result: 15% compression** (light structure, full explanations)

**Scenario: Completed project archive**
- Layer: L5 Archive
- Phase: Maintain-Archive
- Check: Archive layer overrides all
- **Result: 95-99% compression** (metadata + searchability)

---

## Appendix: Terminology

**Compression Percentage**: Amount reduced (40% compression = reduce to 60% of original)  
**Base Matrix**: Default [Role × Layer] targets before adjustments  
**Phase Adjustment**: Multiplier applied based on project lifecycle phase  
**Multi-Role Strategy**: Approach for documents serving multiple roles  
**Edge Case**: Scenario requiring override of standard framework  
**Anti-Pattern**: Common mistake to avoid in compression decisions  
**ROI**: Return on Investment - benefit relative to effort  
**Divergence**: Difference in compression needs between roles  

---

## Related Documentation

- **TECHNIQUES.md**: Specific compression techniques (LSC, CCM, archive strategies)
- **THEORY.md**: Unified (σ,γ,κ) model and theoretical foundations
- **VALIDATION.md**: Framework validation and empirical evidence
- **Integration Guide**: Practical adoption patterns and templates
- **compress.py**: Automation tool implementing LSC techniques

---

**Version**: 1.0  
**Last Updated**: 2025-11-06  
**Status**: Active reference  
**Feedback**: Report issues or suggestions via project channels

---

## Document Statistics

**Total Lines**: ~787
**Sections**: 7 major sections + appendix
**Tables**: 12 reference tables
**Examples**: 15+ worked scenarios
**Checklists**: 3 decision checklists

**Estimated Reading Time**: 20-25 minutes for full read, 5 minutes for reference lookup

**Target Audience**: Technical teams implementing compression framework, architects making design decisions, developers applying compression to documentation

**Compression Level**: Moderate (this document) - balance between comprehensiveness and accessibility


---

## 8. Decision-Support Compression Methodology

### Overview

**Problem**: Standard compression preserves *reference information* (facts, scores, data) but often loses *operational guidance* (how to decide, what to avoid, what combinations work). This makes compressed documents excellent for understanding but inadequate for repeated decision-making.

**Solution**: Add a "Decision Inventory" step before compression to identify and preserve decision-support content at higher fidelity than background/explanatory content.

**When Critical**: Documents used for iterative workflows, repeated decisions, or operational guidance (e.g., technique selection, prompt generation, architectural choices).

---

### The Three Content Categories

Traditional compression treats all non-factual content the same. Decision-support compression distinguishes three categories:

**Category A: Reference Data** (100% preservation)
- Scores, parameters, measurements, factual claims
- API specifications, concrete numbers
- Existing treatment: ✅ Already preserved fully

**Category B: Explanatory Context** (20-40% preservation)
- "Why it works" explanations, background theory
- Verbose examples, detailed rationale, test methodology
- Existing treatment: ✅ Already compressed heavily

**Category C: Decision Support** (80-100% preservation) ← **NEW**
- Decision trees, compatibility matrices, technique stacks
- Anti-patterns, quality thresholds, trigger phrases
- Existing treatment: ❌ Currently compressed like Category B

### Common Decision-Support Elements

When reading source documents, identify and preserve these at high fidelity:

**1. Decision Trees / Selection Criteria**
- "If X goal → use Y approach"
- "When conditions A, B, C → choose technique D"
- Flowcharts or conditional logic for choosing options

**Example missed in compression**:
- Original: "For factual queries with structured output needs, combine Evidence-Based + JSON Schema"
- Lost in compression (treated as explanation)
- Should preserve: "Decision: Factual + Structured → Evidence-Based + JSON Schema"

---

**2. Compatibility Matrices**
- What works well together
- What conflicts or causes issues
- Interaction effects between techniques/approaches

**Example missed in compression**:
- Original: "CoT and Socratic Questioning combine excellently; Tree of Thoughts conflicts with CoT"
- Lost in compression (treated as background)
- Should preserve: "Compatible: CoT + Socratic | Conflict: ToT + CoT"

---

**3. Optimal Stacks / Proven Combinations**
- Battle-tested combinations that work
- Recommended technique sets for specific use cases
- "Start with these 4-6 techniques" guidance

**Example missed in compression**:
- Original: "For comprehensive research: CoT + Socratic + Evidence-Based + JSON Schema + Quality Gate + Self-Scoring"
- Lost in compression (treated as example)
- Should preserve: "Research stack: CoT + Socratic + Evidence + Schema + Gate + Scoring (6 techniques)"

---

**4. Anti-Patterns / What NOT to Do**
- Explicit "don't do this" warnings
- Common mistakes and their consequences
- Known failure modes

**Example missed in compression**:
- Original: "Combining more than 6 techniques causes diminishing returns and increased prompt complexity"
- Lost in compression (treated as observation)
- Should preserve: "Anti-pattern: >6 techniques → diminishing returns + complexity"

---

**5. Quality Thresholds / Success Criteria**
- Specific numbers defining "good enough"
- When to iterate vs. when to proceed
- Performance targets or benchmarks

**Example missed in compression**:
- Original: "Target average effectiveness ≥8.5/10; below 8.0 requires critical refinement"
- Lost in compression (treated as detail)
- Should preserve: "Threshold: ≥8.5/10 = good | <8.0 = critical refinement needed"

---

**6. Exact Trigger Phrases / Patterns**
- Specific wording that produces results
- Tested phrases with known effectiveness
- Phrasing patterns that work vs. don't work

**Example missed in compression**:
- Original: "'Let's think step by step' consistently triggers CoT; 'You must complete sections in order' forces adherence"
- Lost in compression (treated as example)
- Should preserve: "Triggers: 'step by step'→CoT | 'must complete in order'→adherence"

---

### The Decision Inventory Process

**New 4-Step Workflow**:

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: Identify Purpose                                     │
│ What will users do with this document?                       │
│ (Already part of existing method ✅)                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: Inventory Decisions (NEW)                            │
│ List 5-10 repeated decisions users will make                │
│ Examples:                                                    │
│  - "Which technique for this task?"                         │
│  - "Is this output good enough?"                            │
│  - "What combinations avoid conflicts?"                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: Map Decision Inputs (NEW)                            │
│ For each decision, identify information needed:             │
│  - Decision trees? Compatibility info? Thresholds?          │
│  - Tag this content as "decision-critical"                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 4: Apply σ,γ,κ Compression                              │
│  - Decision-critical content: 80-100% preservation          │
│  - Reference data: 100% preservation                        │
│  - Explanatory context: 20-40% preservation                 │
└─────────────────────────────────────────────────────────────┘
```

**Time Investment**: Add ~5-10 minutes per document for Steps 2-3  
**Impact**: Dramatically improved operational utility without sacrificing compression ratio

---

### Practical Implementation

#### During Document Analysis (Before Compression)

**Ask for each section/paragraph**:
1. "Does this help users **understand** something?" 
   - → Category B (Explanatory) → Compress to 20-40%

2. "Does this help users **decide** something?"
   - → Category C (Decision Support) → Preserve 80-100%

3. "Is this pure **data/facts**?"
   - → Category A (Reference) → Preserve 100%

#### Example Decision Inventory Template

For each document, fill out:

```markdown
## Decision Inventory: [Document Name]

### Repeated Decisions Users Will Make:
1. [Decision 1: e.g., "Which technique to use"]
2. [Decision 2: e.g., "Is quality threshold met"]
3. [Decision 3: e.g., "What combinations work"]
4. [Decision 4: e.g., "What to avoid"]
5. [Decision 5: e.g., "How to structure prompt"]

### Decision-Support Content to Preserve:

**Decision Trees:**
- [Location in doc] → [Preserve as structured list]

**Compatibility Info:**
- [Location in doc] → [Preserve as matrix/table]

**Optimal Stacks:**
- [Location in doc] → [Preserve as labeled sets]

**Anti-Patterns:**
- [Location in doc] → [Preserve as warning list]

**Thresholds:**
- [Location in doc] → [Preserve exact numbers]

**Trigger Phrases:**
- [Location in doc] → [Preserve exact wording]
```

---

### Compression Ratio Impact

**Adding decision-support preservation**:
- **Before**: 70-75% compression (reference + explanatory)
- **After**: 68-72% compression (reference + decision + explanatory)
- **Cost**: 2-5% reduction in compression ratio
- **Benefit**: Document actually usable for operational decisions

**Trade-off is favorable**:
- Slightly less compression (~50 extra lines in 400-line doc)
- Massively improved utility for iterative workflows
- Prevents decision-making overhead that exceeds token savings

---

### Validation Checklist

After compression, verify decision-support is adequate:

**Decision Trees**:
- [ ] Can user quickly determine "if X goal → use Y" without re-deriving?
- [ ] Are selection criteria explicit and actionable?

**Compatibility**:
- [ ] Can user avoid known conflicts without trial-and-error?
- [ ] Are positive combinations explicitly called out?

**Stacks**:
- [ ] Are proven combinations readily available?
- [ ] Can user start with a working baseline rather than from scratch?

**Anti-Patterns**:
- [ ] Are "don't do this" warnings explicit?
- [ ] Can user avoid known mistakes without rediscovering them?

**Thresholds**:
- [ ] Are "good enough" criteria specific (numbers, not vague)?
- [ ] Can user determine when to iterate vs. proceed?

**Triggers**:
- [ ] Are exact effective phrases preserved (not paraphrased)?
- [ ] Can user copy/paste working patterns?

**If any fail**: Review Step 3 (Map Decision Inputs) and add missing content

---

### Use Case: Reference vs. Decision-Support

**Reference-Only Document** (traditional compression):
- User needs: Look up information, understand concept
- Usage pattern: Infrequent lookup, different question each time
- Optimization: Maximize compression, preserve facts only
- Example: API documentation, glossary, historical record

**Decision-Support Document** (enhanced compression):
- User needs: Make repeated similar decisions efficiently
- Usage pattern: Frequent access, same decision types repeatedly
- Optimization: Preserve decision scaffolding, accept slightly lower compression
- Example: Technique selection guide, prompt generation reference, architectural decision framework

**This document** falls into decision-support category because teams make repeated compression decisions across many documents.

---

### Integration with Existing Framework

**No changes to**:
- (σ,γ,κ) theory (still valid, just applying γ and κ differently)
- Compression ratios (minimal 2-5% impact)
- Tools (compress.py still works, this is human analysis step)

**Additions to workflow**:
- Pre-compression decision inventory (Steps 2-3)
- Content categorization (A/B/C instead of just data/non-data)
- Validation checklist (verify decision-support preserved)

**When to use**:
- Documents for iterative workflows ✅
- Operational guidance documents ✅
- Frequently-accessed reference ✅
- One-time use documents ❌
- Pure historical records ❌
- Already compressed with adequate utility ❌

---

### Real-World Example: Gemini Prompting Paper

**Original**: 1,332 lines of self-assessment research  
**Use Case**: Generate optimized Gemini prompts across 6-8 research iterations  
**Usage Pattern**: Repeated technique selection, combination decisions, quality assessment

**Traditional Compression Result** (reference-focused):
- Preserved: Scores (10/10), features (1M context), limitations (single-shot)
- Lost: Technique stacks, compatibility, anti-patterns, decision trees, thresholds, exact triggers
- Compression: 75% (1,332 → 322 lines)
- **Problem**: Can understand techniques but must re-derive optimal combinations each time

**Enhanced Compression Result** (decision-support):
- Preserved: All reference data PLUS stacks, compatibility, anti-patterns, thresholds, triggers
- Added sections: ~80 lines
- Compression: 70% (1,332 → 400 lines)
- **Benefit**: Can make technique decisions quickly without re-analysis

**Cost-Benefit**:
- Cost: 78 extra lines (19% increase in compressed size)
- Benefit: Eliminates 5-10 minutes of decision overhead per prompt generation
- ROI: Pays for itself after 2-3 prompts, used across 6-8 iterations = high value

---

### Summary

**Traditional compression asks**: "What information is here?"  
**Decision-support compression asks**: "What decisions will users make?"

**Key insight**: Information that drives repeated decisions has higher operational value than information that builds understanding, even if both are "non-factual."

**Method addition is simple**:
1. Inventory decisions before compressing
2. Categorize content as Reference / Explanatory / Decision-Support
3. Apply different preservation levels to each category
4. Validate decision-support is adequate

**When to use**: Documents for iterative workflows with repeated similar decisions

**Impact**: 2-5% compression ratio cost, dramatic improvement in operational utility

---
