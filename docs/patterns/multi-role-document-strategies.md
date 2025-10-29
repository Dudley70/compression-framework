# Multi-Role Document Strategies

**Created:** 2025-10-30 10:15 AEDT  
**Status:** Active - Session 3 deliverable  
**Related:** multi-dimensional-compression-matrix.md, information-preservation-framework.md

---

## Purpose

Documents often serve multiple audience roles simultaneously. This guide provides systematic strategies for optimizing multi-role documents, balancing the competing needs of different consumers while managing complexity and maintenance overhead.

**Key Question:** When a document serves multiple roles with different compression targets, how do you optimize effectively?

**Answer:** Strategy selection based on role divergence, with explicit trade-off analysis.

---

## Overview

### The Multi-Role Challenge

From the Multi-Dimensional Compression Matrix, we have base compression targets per role:

| Role | Base Target | Purpose |
|------|-------------|---------|
| Architect | 40-60% | High-level system understanding |
| Coordinator | 50-70% | Task orchestration, status tracking |
| Developer | 30-50% | Implementation detail, technical depth |
| Maintainer | 30-50% | Evolution context, "why" decisions |
| Orchestrator | 60-80% | Workflow execution, automation |
| Strategic | 60-80% | Direction, decisions, outcomes |

**Problem:** A document like DECISIONS.md might need to serve:
- Coordinator: 50-70% compression (status, dependencies)
- Maintainer: 30-50% compression (rationale, evolution)
- Architect: 40-60% compression (system implications)

**Challenge:** These roles want different information depths from the same document.

### Three Core Strategies

1. **Union Strategy** (<20% divergence): Optimize for least compression (most detail)
2. **Intersection Strategy** (20-40% divergence): Primary role optimization
3. **Layered Strategy** (>40% divergence): Multiple representations

**Selection depends on:**
- Role divergence magnitude
- Document frequency of access
- Maintenance capacity
- Information criticality

---

## Part 1: Strategy Selection Framework

### 1.1 Divergence Calculation

**Formula:**
```
Divergence = |Target_A - Target_B| where A is highest detail, B is lowest detail
```

**Example 1: DECISIONS.md**
```
Roles: Coordinator (50-70%), Maintainer (30-50%), Architect (40-60%)

Most detail needed: Maintainer = 30-50%
Least detail needed: Coordinator = 50-70%

Divergence = |30% - 70%| = 40% divergence
Strategy: Layered (>40%)
```

**Example 2: TASKS.md**
```
Roles: Developer (30-50%), Coordinator (50-70%)

Most detail: Developer = 30-50%
Least detail: Coordinator = 50-70%

Divergence = |30% - 70%| = 40% divergence
Strategy: Intersection (20-40% range) or Layered (at threshold)
Decision: Depends on access frequency and primary role clarity
```

**Example 3: README.md**
```
Roles: Developer (30-50%), Architect (40-60%)

Most detail: Developer = 30-50%
Least detail: Architect = 40-60%

Divergence = |30% - 60%| = 30% divergence
Strategy: Intersection (clear middle ground)
```

### 1.2 Decision Tree

```
Calculate role divergence
    ↓
Is divergence < 20%?
    YES → Union Strategy
    NO → Continue
    ↓
Is divergence 20-40%?
    YES → Intersection Strategy (if primary role clear)
    NO → Continue
    ↓
Is divergence > 40%?
    YES → Consider Layered Strategy
    NO → Edge case, analyze manually
    ↓
Layered Strategy: Evaluate cost/benefit
    High frequency + critical? → Implement layered
    Low frequency + non-critical? → Use intersection with primary role
    Medium cases? → ROI analysis required
```

### 1.3 Strategy Characteristics

**Union Strategy (<20% divergence)**
- **Approach:** Optimize for most detail-needing role
- **Trade-off:** Slightly more verbose for some roles, but manageable
- **When:** Role needs are similar enough that single representation works
- **Example:** Developer (30-50%) + Maintainer (30-50%) = 0-20% divergence

**Intersection Strategy (20-40% divergence)**
- **Approach:** Identify primary role, optimize for that with acceptable compromises
- **Trade-off:** Some roles get more/less detail than ideal
- **When:** Clear primary consumer, secondary roles acceptable with compromise
- **Example:** TASKS.md primarily for Developers, Coordinator can work with detail

**Layered Strategy (>40% divergence)**
- **Approach:** Multiple representations or progressive detail sections
- **Trade-off:** Increased maintenance overhead, potential duplication
- **When:** High-frequency documents, critical information, unacceptable compromise
- **Example:** PROJECT.md with summary section + detailed sections

---

## Part 2: Union Strategy

### 2.1 When to Use Union Strategy

**Ideal Conditions:**
- Role divergence < 20%
- Roles have overlapping information needs
- Single representation serves all roles adequately
- Maintenance simplicity priority

**Example Scenarios:**

**Scenario A: Developer + Maintainer Documentation**
```
Developer target: 30-50% compression
Maintainer target: 30-50% compression
Divergence: 0-20%

Both need:
- Implementation rationale
- Technical decisions
- "Why" context
- Code structure understanding

Union approach: Optimize at 30-40% compression (detailed end)
Result: Both roles well-served
```

**Scenario B: Architect + Strategic Planning Docs**
```
Architect target: 40-60% compression
Strategic target: 60-80% compression
Divergence: 0-40% (borderline)

If content focus is system design:
- Strategic role can handle more detail
- Architect needs that detail
- Union at 40-50% compression works

If content is pure strategic direction:
- Use Intersection strategy instead
- Strategic role is primary
```

### 2.2 Union Strategy Implementation

**Process:**
1. Identify all role targets for document
2. Calculate divergence (confirm <20%)
3. Choose most detail-needing role's target
4. Apply compression targeting that level
5. Validate all roles can accomplish their purposes

**Optimization Guidelines:**

**Preserve shared information needs:**
- Rationale and "why" context
- Decisions and trade-offs
- Technical implications
- Evolution history (where relevant)

**Compress role-specific tangents:**
- Details only one role needs: Consider separating
- Process steps only relevant to one role: Link out
- Deep technical dives: Separate document if only Developer needs

**Conservative approach:**
- When in doubt, preserve detail
- Union strategy favors completeness
- Better slightly verbose than missing critical info

### 2.3 Union Strategy Examples

**Example 1: Technical Design Document**

**Roles:** Developer (30-50%), Maintainer (30-50%), Architect (40-60%)

**Divergence:** Maintainer vs Architect = 10-30% (borderline)

**Decision:** Union at 30-40% compression

**Structure:**
```markdown
# Component X Design

## Overview (all roles)
Purpose, scope, integration points - 40% compression

## Technical Approach (Dev + Maint primary)
Implementation strategy, patterns used - 30% compression
Why this approach vs alternatives - preserved fully
Technology choices and rationale - preserved fully

## Architecture Integration (Arch + Dev)
System-level implications - 35% compression
Dependencies and interfaces - preserved fully

## Maintenance Considerations (Maint + Dev)
Evolution patterns, extension points - 30% compression
Known limitations and future work - preserved fully

## Implementation Notes (Dev primary, others optional)
Code organization, key classes - 40% compression
Setup and configuration - linked externally if lengthy
```

**Why this works:**
- All roles get sufficient detail for their purposes
- Shared sections optimized for most-detail-needing role
- Developer-specific details moderately compressed (still accessible)
- Total document: 35% average compression (within all role ranges)

**Example 2: API Documentation**

**Roles:** Developer (30-50%), Orchestrator (60-80%)

**Divergence:** 10-50% (spans union and intersection range)

**Decision:** If Orchestrator is automation/scripting focus: Union at 30-40%

**Why:** Orchestrator scripting often needs technical detail, divergence is acceptable

**Structure:**
```markdown
# API Reference

## Endpoints (all roles)
Method, path, purpose - 50% compression
Authentication requirements - preserved

## Request/Response (Dev primary, Orch needs)
Parameters and types - 40% compression
Response structure - 40% compression
Examples - preserved (critical for both)

## Error Handling (both roles)
Error codes and meanings - preserved
Retry logic - preserved

## Rate Limiting (Orch primary)
Limits and windows - preserved
Best practices - preserved

## Implementation Details (Dev primary)
SDK usage patterns - 35% compression
Advanced options - 40% compression

```

**Result:** Developer gets full detail, Orchestrator can extract what they need, minimal overhead

---

## Part 3: Intersection Strategy

### 3.1 When to Use Intersection Strategy

**Ideal Conditions:**
- Role divergence 20-40%
- Clear primary consumer role
- Secondary roles can work with compromise
- Moderate frequency (daily to weekly access)

**Key Question:** "Which role is the primary document consumer?"

**Decision Factors:**
- Access frequency per role
- Criticality to each role's work
- Alternative information sources available
- Acceptable compromise for secondary roles

### 3.2 Primary Role Identification

**Method 1: Frequency Analysis**
```
Role A accesses document: 10x/week
Role B accesses document: 2x/week
Role C accesses document: 1x/month

Primary: Role A (highest frequency)
Optimize for: Role A's compression target
```

**Method 2: Purpose Criticality**
```
For TASKS.md:
- Developer: Critical for daily work (must have implementation detail)
- Coordinator: Important for status tracking (can use summary view)

Primary: Developer (critical vs important)
```

**Method 3: Information Alternatives**
```
Role A needs this document + no alternatives
Role B can get 80% of info from other sources

Primary: Role A (no alternative paths)
```

### 3.3 Intersection Strategy Implementation

**Process:**
1. Identify all role targets for document
2. Calculate divergence (confirm 20-40%)
3. Determine primary role using frequency/criticality/alternatives
4. Optimize for primary role's compression target
5. Add lightweight accommodations for secondary roles
6. Validate secondary roles can still accomplish core purposes (with acceptable friction)

**Accommodation Techniques for Secondary Roles:**

**Technique 1: Progressive Detail Sections**
```markdown
# Technical Decision Log

## Summary (for all roles)
Quick reference of decisions - 60% compression

## Decision Details (primary: Developer + Maintainer)
Full context, alternatives, rationale - 35% compression

## Implementation Impact (primary: Developer)
Code changes, migration steps - 30% compression
```
Secondary roles (Coordinator, Strategic) get what they need from Summary section.

**Technique 2: Inline Summaries**
```markdown
## Decision X: Migration to New Framework

**TL;DR (Coordinator/Strategic):** Moving to React, 3-month timeline, no customer impact.

**Full Context (Developer/Maintainer):**
Current framework (Angular 1.x) at end-of-life...
[detailed rationale, 35% compression]
```

**Technique 3: Section Depth Markers**
```markdown
## Architecture Overview [Architect Primary]
High-level system design - 45% compression

### Implementation Details [Developer Deep Dive]
Code organization, patterns - 30% compression
(Architects can skip for summary understanding)
```

### 3.4 Intersection Strategy Examples

**Example 1: TASKS.md (Developer Primary)**

**Roles:**
- Developer: 30-50% compression (critical daily use)
- Coordinator: 50-70% compression (status tracking)

**Divergence:** 20-40%

**Primary:** Developer (implementation critical)

**Optimization:** Target 35-40% compression (Developer range)

**Structure:**
```markdown
# Active Tasks

## Task ID-123: Implement User Auth [Developer]
**Status:** In Progress | **Assigned:** Dev Team | **Due:** 2025-11-15

### Implementation Approach
[Detailed technical approach - 35% compression]
- Authentication flow design
- Security considerations
- Integration points with existing system

### Technical Details
[Code structure, dependencies - 30% compression]
- Key classes and modules
- Database schema changes
- API endpoints affected

### Testing Strategy
[Test approach - 35% compression]

### Status Updates [Coordinator view]
- 2025-10-28: Design complete, implementation started
- 2025-10-25: Requirements clarified with stakeholders
```

**Coordinator Accommodation:**
- Status field prominent at top
- Status Updates section for timeline
- Can get progress without reading implementation details

**Result:** Developer gets full implementation detail, Coordinator extracts status with 2-3x longer scan time (acceptable trade-off).

**Example 2: Configuration Documentation (Architect Primary)**

**Roles:**
- Architect: 40-60% compression (system design)
- Developer: 30-50% compression (implementation)
- Orchestrator: 60-80% compression (deployment automation)

**Divergence:** Architect vs Developer = 0-20%, Architect vs Orchestrator = 0-40%

**Primary:** Architect (system design decisions)

**Optimization:** Target 45-55% compression (Architect middle range)

**Structure:**
```markdown
# System Configuration Strategy

## Configuration Approach [Architect level]
Environment-based config with override hierarchy - 50% compression
Design rationale and alternatives considered - preserved

### Implementation [Developer detail]
Config loading mechanism - 40% compression
File formats and structure - 40% compression
[Link to detailed developer guide if extensive]

## Deployment [Orchestrator view]
**Quick Reference:** [Table of config files and locations - 70% compression]

See deployment automation docs for scripting details [link]
```

**Accommodations:**
- Developer gets inline implementation section (moderate compression)
- Orchestrator gets quick reference table + link to automation docs
- Architect gets design rationale focus

**Trade-off Analysis:**
- Developer: Acceptable (may need to reference separate detailed guide)
- Orchestrator: Acceptable (automation details separated appropriately)
- Architect: Optimal (primary focus maintained)

---

## Part 4: Layered Strategy

### 4.1 When to Use Layered Strategy

**Ideal Conditions:**
- Role divergence > 40%
- High-frequency document (daily access by multiple roles)
- Critical information for all roles
- Unacceptable for any role to compromise

**Warning:** Layered strategy has highest maintenance cost. Use sparingly.

**Cost/Benefit Threshold:**
```
Implement Layered IF:
  (Frequency_A × Criticality_A + Frequency_B × Criticality_B) × Divergence > Threshold

Where:
  Frequency: Daily = 5, Weekly = 3, Monthly = 1
  Criticality: Critical = 5, Important = 3, Useful = 1
  Divergence: Percentage difference / 10
  Threshold: Typically 50-75 (adjust for team size/capacity)

Example:
  Developer: Daily (5) × Critical (5) = 25
  Strategic: Weekly (3) × Important (3) = 9
  Total: 34 × 40% divergence / 10 = 136
  
  136 > 75 → Layered strategy justified
```

### 4.2 Layered Approaches

**Approach A: Progressive Detail (Single Document)**

Best for: Documents where all roles start with same context, then diverge

**Structure:**
```markdown
# Document Title

## Executive Summary [Strategic: 70% compression]
High-level overview, decisions, outcomes

## Technical Overview [Architect: 50% compression]  
System design, integration, implications

## Implementation Guide [Developer: 30% compression]
Detailed technical approach, code examples

## Maintenance Notes [Maintainer: 35% compression]
Evolution history, rationale, future considerations
```

**Advantages:**
- Single document (easier maintenance)
- Each role reads their depth
- Natural flow from high-level to detailed

**Disadvantages:**
- Document can become long
- Roles must skip irrelevant sections
- Navigation overhead

**Approach B: Role-Specific Views (Linked Documents)**

Best for: Documents where roles need fundamentally different information

**Structure:**
```
/docs/feature-x/
  overview.md [Strategic: 70% compression]
  architecture.md [Architect: 45% compression]
  implementation.md [Developer: 30% compression]
  operations.md [Orchestrator: 65% compression]
```

**Advantages:**
- Each document optimized for its role
- No unnecessary information per role
- Parallel maintenance possible

**Disadvantages:**
- Multiple documents to maintain
- Risk of inconsistency
- Shared information may duplicate

**Approach C: Core + Extensions (Hybrid)**

Best for: Documents with shared core, role-specific extensions

**Structure:**
```markdown
# Core Document (all roles)
Shared information, fundamental concepts - optimized for most-detail-needing role

## Extensions by Role

### [For Developers] Implementation Details
[Link to developer-deep-dive.md - 30% compression]

### [For Architects] System Integration
[Link to architecture-notes.md - 45% compression]

### [For Strategic] Business Impact
[Link to strategic-overview.md - 75% compression]
```

**Advantages:**
- Core information centralized
- Extensions independently optimized
- Clear separation of concerns

**Disadvantages:**
- Multiple files still
- Core document must serve multiple roles (may require Union strategy)

### 4.3 Layered Strategy Implementation

**Process:**
1. Confirm divergence > 40% and cost/benefit justifies layered approach
2. Select layered approach (Progressive / Role-Specific / Core+Extensions)
3. Design information architecture
4. Create initial versions for all roles
5. Establish cross-document consistency checks
6. Document maintenance responsibilities

**Maintenance Strategies:**

**Strategy 1: Single Owner with Review**
- One person maintains all views
- Role representatives review for accuracy
- Best for: Small teams, clear ownership

**Strategy 2: Distributed Ownership**
- Each role maintains their view
- Core/shared sections have designated owner
- Regular consistency reviews
- Best for: Larger teams, specialists per role

**Strategy 3: Generated Views**
- Single source document with metadata
- Role-specific views generated automatically
- Best for: High-frequency changes, technical documents

### 4.4 Layered Strategy Examples

**Example 1: PROJECT.md (All Roles)**

**Roles:** All 6 roles with divergence up to 50%

**Decision:** Layered - Progressive Detail (single document)

**Rationale:** 
- Every role needs project context
- Accessed every session (CRITICAL frequency)
- High cost/benefit score (5 × 5 × 6 roles = 150+)

**Structure:**
```markdown
# Project Name

## Strategic Context [Strategic/Coordinator: 70% compression]
- Project purpose and goals
- Current phase and status
- Key decisions and outcomes
- Success metrics

## Solution Approach [Architect: 50% compression]
- System design overview
- Integration architecture
- Technical strategy

## Core Principles [All roles: 60% compression]
- Non-negotiables
- Design philosophy
- Constraints

## Implementation Details [Developer: 35% compression]
- Technical stack
- Development approach
- Code organization

## Operational Workflows [Orchestrator: 65% compression]
- Deployment process
- Monitoring and maintenance
- Automation hooks

## Evolution History [Maintainer: 40% compression]
- Decision log
- Architecture changes
- Rationale for major shifts
```

**Role Navigation:**
- Strategic: Reads Strategic Context only (loads in seconds)
- Architect: Reads Strategic + Solution + Principles (medium load)
- Developer: Reads Principles + Implementation + skims Solution (detailed view)
- Orchestrator: Reads Operational Workflows primarily
- Maintainer: Reads Evolution + references other sections as needed
- Coordinator: Reads Strategic Context + skims status updates

**Maintenance:** Single document, section-level ownership, updated as part of regular workflow

**Example 2: DECISIONS.md (Coordinator + Maintainer + Architect)**

**Roles:**
- Coordinator: 50-70% compression (status, dependencies)
- Maintainer: 30-50% compression (rationale, evolution)
- Architect: 40-60% compression (system implications)

**Divergence:** 20-40% (Coordinator vs Maintainer)

**Decision:** Intersection with Progressive Detail (borderline case)

**Primary:** Maintainer (long-term value, critical for evolution understanding)

**Optimization:** Target 35-45% compression (Maintainer range)

**Structure:**
```markdown
# Decision Log

## Decision-123: Migrate to Microservices

**Date:** 2025-10-15 | **Status:** Approved | **Impact:** High

### Summary [Coordinator view - 60% compression]
Moving from monolith to microservices architecture. Timeline: 6 months. Team: Platform team lead.

### Context and Rationale [Maintainer/Architect - 35% compression]
Current monolith challenges:
- Scaling bottlenecks in payment processing
- Deployment coupling causing release delays
- Team coordination overhead with 20+ developers

Alternatives considered:
- Modular monolith: Insufficient isolation for scaling needs
- Vertical slicing: Organizational complexity too high
- Microservices: Selected for independent scaling + deployment

Trade-offs accepted:
- Operational complexity increase (monitoring, deployment)
- Distributed system challenges (latency, consistency)
- Worth it for: Team autonomy + independent scaling

### System Impact [Architect - 40% compression]
- Service boundaries: User, Payment, Inventory, Notification
- Communication: Async messaging primary, sync REST for queries
- Data: Database per service, eventual consistency patterns
- Migration approach: Strangler fig pattern over 6 months

### Implementation Status [Coordinator tracking]
- Phase 1 (Months 1-2): User service extraction [Complete]
- Phase 2 (Months 3-4): Payment service extraction [In Progress]
- Phase 3 (Months 5-6): Inventory + Notification [Planned]
```

**Accommodations:**
- Coordinator: Gets Summary + Status, can skip deep rationale (acceptable)
- Architect: Gets System Impact + enough context from Rationale
- Maintainer: Gets full rationale and "why not X" (optimal)

**Why Not Full Layered:**
- Frequency: Weekly for Coordinator, monthly for others
- Cost/benefit: (3 × 3) + (1 × 5) + (1 × 4) = 18 × 3 = 54 < threshold
- Intersection sufficient with progressive sections

**Example 3: Technical Documentation Suite (Developer + Architect + Orchestrator)**

**Roles:** 
- Developer: 30-50% compression (implementation detail)
- Architect: 40-60% compression (system design)
- Orchestrator: 60-80% compression (deployment automation)

**Divergence:** Developer vs Orchestrator = 30-50%

**Decision:** Layered - Core + Extensions

**Structure:**
```
/docs/platform/
  README.md [Core - all roles, 45% compression]
    - System overview
    - Key concepts
    - Quick start
    - Links to role-specific docs
  
  architecture/ [Architect focus]
    system-design.md [45% compression]
    integration-patterns.md [50% compression]
    decision-records.md [40% compression]
  
  development/ [Developer focus]
    setup-guide.md [30% compression]
    api-reference.md [35% compression]
    coding-standards.md [40% compression]
    troubleshooting.md [30% compression]
  
  operations/ [Orchestrator focus]
    deployment-guide.md [65% compression]
    monitoring-runbooks.md [70% compression]
    automation-scripts.md [75% compression]
```

**Rationale for Full Layered:**
- High divergence (50%)
- High frequency: Developer daily, Architect weekly, Orchestrator daily
- Critical for all roles in their contexts
- Cost/benefit: (5 × 5) + (3 × 4) + (5 × 5) = 62 × 5 = 310 > threshold

**Maintenance:**
- README.md: Shared ownership, reviewed on changes
- Role-specific directories: Owned by that role's representative
- Cross-links maintained in README
- Quarterly consistency review

---

## Part 5: Cost/Benefit Analysis Framework

### 5.1 Layered Strategy Cost Analysis

**Costs of Layered Approach:**

**Maintenance Overhead:**
- Multiple files/sections to update
- Risk of inconsistency across views
- Coordination overhead between maintainers
- Time to propagate changes across all views

**Typical Overhead:**
- Progressive Detail (single doc): +20-30% maintenance time
- Role-Specific Views (multiple docs): +50-100% maintenance time
- Core + Extensions: +40-60% maintenance time

**Creation Overhead:**
- Initial design and information architecture
- Creating multiple optimized versions
- Establishing cross-document linking
- Documenting maintenance process

**Typical Creation Overhead:**
- Progressive Detail: +30-50% creation time vs single optimized doc
- Role-Specific Views: +100-150% creation time
- Core + Extensions: +60-80% creation time

**Cognitive Overhead:**
- Understanding which document/section to read
- Navigating between views
- Potential confusion if views inconsistent

### 5.2 Layered Strategy Benefit Analysis

**Benefits of Layered Approach:**

**Role Efficiency:**
- Each role gets optimal information density
- No time wasted on irrelevant detail
- Faster comprehension and task completion

**Typical Savings:**
- Well-optimized layered: 30-60% time savings per access vs poorly-optimized single document
- Compounds with frequency: Daily access = significant cumulative benefit

**Information Fidelity:**
- Each role gets appropriate depth
- No critical information lost due to compression compromise
- Better decision-making and execution quality

**Scalability:**
- New roles can be added without compromising existing views
- Role responsibilities can evolve without document restructure
- Team growth doesn't degrade document utility

### 5.3 Break-Even Analysis

**Formula:**
```
Break-Even Point (in accesses) = 
  (Creation Overhead + Maintenance Overhead per Update × Expected Updates)
  / (Time Saved per Access × Number of Roles)

Example Calculation:

Progressive Detail in PROJECT.md:
  Creation Overhead: 4 hours (vs 3 hours for single optimized)
  Maintenance per Update: 30 min (vs 20 min single, +10 min overhead)
  Expected Updates: 50/year
  Time Saved per Access: 3 min per role (vs scanning single doc)
  Roles: 5 roles, varying access frequencies

  Total Overhead: 4 + (50 × 10/60) = 4 + 8.3 = 12.3 hours/year
  
  Access Frequencies:
    Developer: 200/year × 3 min = 600 min = 10 hours saved
    Architect: 100/year × 3 min = 300 min = 5 hours saved
    Strategic: 50/year × 3 min = 150 min = 2.5 hours saved
    Coordinator: 200/year × 3 min = 600 min = 10 hours saved
    Orchestrator: 100/year × 3 min = 300 min = 5 hours saved
  
  Total Saved: 32.5 hours/year
  
  ROI: 32.5 / 12.3 = 2.6× return (strong positive)
  Break-Even: 12.3 / (3/60 × 5) = ~50 accesses (reached in weeks for this doc)
```

**When Layered Makes Sense:**
- High-frequency documents: Daily/weekly access by multiple roles
- Long-lived documents: Multi-year lifespan justifies setup cost
- Critical documents: Poor optimization impacts work quality significantly
- Large teams: More roles = more cumulative benefit

**When to Avoid Layered:**
- Low-frequency: Monthly or less access
- Short-lived: Temporary documents, < 6-month lifespan
- Small teams: 2-3 people wearing multiple hats
- Low divergence: Union or Intersection sufficient

### 5.4 Trade-Off Decision Matrix

| Factor | Union | Intersection | Layered |
|--------|-------|--------------|---------|
| **Divergence** | <20% | 20-40% | >40% |
| **Frequency** | Any | Medium-High | High |
| **Maintenance Cost** | Low | Medium | High |
| **Role Efficiency** | Medium | Medium | High |
| **Setup Time** | Low | Low-Medium | High |
| **Consistency Risk** | Low | Low | Medium-High |
| **Best For** | Similar roles | Primary role clear | Critical multi-role docs |

**Decision Guide:**
1. Calculate divergence → Eliminates options
2. Assess frequency → Confirms viability
3. Evaluate criticality → Justifies overhead
4. Check maintenance capacity → Practical constraint
5. Calculate ROI if borderline → Data-driven decision

---

## Part 6: Implementation Templates

### 6.1 Progressive Detail Template

**File Structure:**
```markdown
# [Document Title]

**Roles:** [List all roles and their targets]
**Strategy:** Progressive Detail (Layered)
**Maintenance:** [Owner/process]

---

## Quick Reference [Highest compression roles]
<!-- Strategic/Coordinator view -->
<!-- Target: 70-80% compression -->

TL;DR summary, key decisions, current status

## [Section Name] [Medium compression roles]  
<!-- Architect/Orchestrator view -->
<!-- Target: 45-65% compression -->

Moderate detail, system-level information

### Subsection Detail [Lowest compression roles]
<!-- Developer/Maintainer view -->
<!-- Target: 30-50% compression -->

Full technical detail, implementation specifics

## Additional Sections
[Repeat pattern: high-level → detailed]

---

## Navigation Guide
- **Strategic/Coordinator:** Read Quick Reference only
- **Architect:** Read Quick Reference + [Section Names]
- **Developer:** Read all, focus on Detail subsections
- **Maintainer:** Full document, emphasize rationale sections
- **Orchestrator:** Quick Reference + Operational sections
```

**Usage Notes:**
- Clearly mark section depth/audience
- Provide navigation guide at start or end
- Use consistent heading levels for role tiers
- Link detailed sections from high-level summaries

### 6.2 Role-Specific Views Template

**Directory Structure:**
```
/docs/[topic]/
  _index.md                    # Overview + links to role views
  strategic-view.md            # 70-80% compression
  architect-view.md            # 45-60% compression  
  developer-view.md            # 30-50% compression
  operations-view.md           # 60-75% compression
  maintenance-log.md           # 35-50% compression
```

**_index.md Template:**
```markdown
# [Topic] Documentation

## Overview
[Brief description of topic - 60% compression]

## Documentation by Role

### For Strategic Planning
[One paragraph summary - 75% compression]
📄 [Full Strategic View](strategic-view.md)

### For System Architects  
[One paragraph summary - 60% compression]
📄 [Full Architecture View](architect-view.md)

### For Developers
[One paragraph summary - 50% compression]
📄 [Full Development Guide](developer-view.md)

### For Operations
[One paragraph summary - 70% compression]
📄 [Full Operations Guide](operations-view.md)

## Shared Resources
- [Decision Log](maintenance-log.md)
- [External References]

## Maintenance
**Owners:** [List role view owners]
**Update Process:** [How changes propagate]
**Last Updated:** YYYY-MM-DD
```

**Individual View Template:**
```markdown
# [Topic] - [Role] View

**Target Audience:** [Role]
**Compression Target:** [X-Y%]
**Related Views:** [Links to other role views]

---

## [Role-Optimized Content]
[Information structured and compressed for this role's needs]

## Cross-References
[Links to other views for additional detail/context]

## Maintenance Notes
**Owner:** [Name/Role]
**Update Frequency:** [Expected cadence]
**Dependencies:** [What impacts this view]
```

### 6.3 Core + Extensions Template

**Core Document Template:**
```markdown
# [Topic] Core Documentation

**Audience:** All Roles (baseline information)
**Compression:** [Moderate, typically 45-55%]

---

## Fundamentals
[Shared concepts, key information all roles need]

## Quick Start
[Basic getting-started applicable to all roles]

## Role-Specific Extensions

This core document provides baseline information. For role-optimized details:

- **📐 Architects:** See [Architecture Deep Dive](architecture/README.md)
  - System design, integration patterns, technical strategy
  
- **💻 Developers:** See [Development Guide](development/README.md)
  - Setup, API reference, coding standards, troubleshooting
  
- **⚙️ Operations:** See [Operations Runbooks](operations/README.md)
  - Deployment, monitoring, automation, incident response
  
- **📋 Maintainers:** See [Evolution History](maintenance/decision-log.md)
  - Decision rationale, architecture changes, "why not X"

## Common Information
[Shared resources, references, FAQs]
```

**Extension Document Template:**
```markdown
# [Topic] - [Role] Extension

**Extends:** [Link to core document]
**Target Audience:** [Role]
**Compression Target:** [X-Y%]

---

## Prerequisites
[Reference to core concepts from main doc]

## [Role-Specific Content]
[Detailed information optimized for this role]

## Integration with Core
[How this extends/relates to core document]
[When to reference core vs this extension]
```

### 6.4 Document Header Standards

**Multi-Role Document Headers:**
```markdown
# [Document Title]

**Created:** YYYY-MM-DD HH:MM TZ
**Last Updated:** YYYY-MM-DD HH:MM TZ
**Status:** Active | Complete | Archive

**Roles & Targets:**
- Primary: [Role] ([X-Y%] compression)
- Secondary: [Role] ([X-Y%] compression)
- Tertiary: [Role] ([X-Y%] compression)

**Strategy:** Union | Intersection | Layered ([Type])
**Divergence:** [X%]

**Related Documents:**
- [Link to related doc 1]
- [Link to related doc 2]

---
```

**Purpose:**
- Explicit about multi-role nature
- Documents strategy choice
- Aids future maintenance decisions
- Provides navigation context

---

## Part 7: Validation and Quality Assurance

### 7.1 Role Purpose Validation

**Critical Question:** Can each role accomplish their core purposes with this optimization?

**Validation Process:**

**Step 1: List Role Purposes**
```
For DECISIONS.md:

Coordinator Purposes:
- Track decision status and timelines
- Understand dependencies and blockers
- Coordinate across teams

Maintainer Purposes:
- Understand decision rationale
- Know what alternatives were considered and why rejected
- Track evolution of system thinking

Architect Purposes:
- Understand system implications
- Validate technical approach
- Ensure architectural consistency
```

**Step 2: Test Each Purpose**
```
Coordinator Test:
Q: Can you find decision status in <10 seconds?
Q: Can you identify dependencies without reading full rationale?
Q: Can you track timeline without implementation details?

Maintainer Test:
Q: Can you understand "why not X" for alternatives?
Q: Can you find rationale for future reference?
Q: Does compression lose critical evolution context?

Architect Test:
Q: Are system implications clear?
Q: Can you evaluate technical consistency?
Q: Is architectural impact preserved?
```

**Step 3: Measure Success**
```
PASS: Role can accomplish >90% of purposes with <2× effort vs optimal
ACCEPTABLE: Role can accomplish >80% of purposes with <3× effort
FAIL: Role cannot accomplish core purposes OR effort >3× optimal

If FAIL: Strategy inappropriate, reconsider approach
If ACCEPTABLE: Document known limitations, monitor for complaints
If PASS: Strategy validated
```

### 7.2 Divergence Measurement

**Method 1: Token-Based Divergence**
```
1. Create optimal document for Role A (compress to target A%)
2. Create optimal document for Role B (compress to target B%)
3. Compare information overlap

Divergence = 1 - (Shared Information Tokens / Total Information Tokens)

Example:
Role A optimal: 1000 tokens
Role B optimal: 800 tokens
Shared: 600 tokens of same information

Divergence = 1 - (600 / 900 average) = 1 - 0.67 = 33%
```

**Method 2: Content Section Divergence**
```
List sections needed by each role:

Role A needs: Sections 1, 2, 3, 4, 5, 6
Role B needs: Sections 1, 2, 7, 8

Shared sections: 1, 2 (2 of 8 unique sections)
Divergence: 1 - (2 / 8) = 75%
```

**Method 3: Compression Target Divergence** (Simplest)
```
Role A target: 30-50% compression
Role B target: 60-80% compression

Divergence = |30% - 80%| = 50% (use most different endpoints)

Quick assessment: Use this method for initial strategy selection
```

### 7.3 Multi-Role Optimization Quality Checklist

**For Union Strategy:**
- [ ] Divergence confirmed <20%
- [ ] All roles can accomplish core purposes
- [ ] Optimized for most-detail-needing role
- [ ] No role-specific tangents uncompressed
- [ ] Validation: Each role tested for purpose completion

**For Intersection Strategy:**
- [ ] Divergence confirmed 20-40%
- [ ] Primary role clearly identified and justified
- [ ] Primary role fully optimized
- [ ] Secondary roles have lightweight accommodations
- [ ] Validation: Secondary roles achieve >80% of purposes with acceptable friction
- [ ] Alternative information sources documented for secondary roles

**For Layered Strategy:**
- [ ] Divergence confirmed >40%
- [ ] Cost/benefit analysis performed and justified
- [ ] ROI calculation shows positive return
- [ ] Layered approach type selected (Progressive/Views/Core+Extensions)
- [ ] Maintenance process documented
- [ ] Consistency check process established
- [ ] Validation: Each role gets optimal experience
- [ ] Navigation guide provided for users

**General Checks (All Strategies):**
- [ ] Strategy choice documented in header
- [ ] Compression targets explicit per role
- [ ] Related documents linked
- [ ] Maintenance ownership clear
- [ ] Last updated timestamp current

### 7.4 Continuous Validation

**Monitoring Approach:**

**Frequency Tracking:**
```markdown
# Document Access Log (Optional for high-value docs)

| Date | Role | Purpose | Time Spent | Success? | Notes |
|------|------|---------|------------|----------|-------|
| 2025-10-15 | Dev | Find API endpoint | 2 min | Yes | Quick |
| 2025-10-16 | Coord | Status update | 8 min | Partial | Too much detail |
| 2025-10-17 | Arch | System review | 15 min | Yes | Appropriate depth |
```

**Purpose:** Identify if strategy working as intended or needs adjustment

**Feedback Collection:**
- Ask roles if document serves their needs
- Monitor time-to-information metrics
- Track complaints about "too much detail" or "not enough detail"
- Review quarterly and adjust strategy if needed

**Adjustment Triggers:**
```
If >20% of accesses report "wrong level of detail": Review strategy
If time-to-information >3× expected: Optimization insufficient
If role priorities shift: Reassess primary role for Intersection strategy
If divergence changes: May need strategy migration
```

### 7.5 Strategy Migration

**When to Migrate:**

**Union → Intersection:**
- Trigger: One role's access frequency much higher than others
- Action: Identify primary role, optimize for them
- Process: Add accommodations for secondary roles, test validation

**Intersection → Layered:**
- Trigger: Secondary roles cannot accomplish purposes (validation failure)
- Or: Frequency × criticality threshold exceeded
- Action: Calculate full ROI, design layered approach
- Process: Create progressive detail or separate views

**Layered → Intersection:**
- Trigger: Maintenance overhead > benefit (negative ROI)
- Or: Access frequency decreased
- Action: Consolidate to single document with primary role
- Process: Merge views, add lightweight accommodations

**Union → Layered:**
- Trigger: Rare but possible if divergence underestimated initially
- Process: Directly to layered if ROI justifies

**Migration Process:**
1. Document reason for migration
2. Create new structure alongside old (don't break existing first)
3. Test with representative users from each role
4. Cutover when validated
5. Archive old version with migration note
6. Update INDEX.md and related docs

---

## Part 8: Common Scenarios and Patterns

### 8.1 SESSION.md (Highest Frequency Document)

**Context:** Loaded every session, highest frequency document in project

**Roles:**
- All roles (Developer, Coordinator, Architect, Maintainer, Orchestrator, Strategic)
- Different depths needed per role

**Divergence:** Up to 50% (Developer 30-50% vs Strategic 60-80%)

**Strategy:** Layered - Progressive Detail (single document)

**Rationale:**
- CRITICAL frequency (every session start)
- All roles need session context
- Cost/benefit massively positive (hundreds of accesses)

**Structure:**
```markdown
# Session State

## WHERE WE ARE [All roles - 70% compression]
Current phase, immediate context, ready-to-continue summary

## ACCOMPLISHED [Coord/Strategic - 65% compression]
What was completed, outcomes, commits

## NEXT ACTIONS [Coord/Dev - 50% compression]
Immediate next steps, clear actionable tasks

### Technical Details [Developer deep-dive - 35% compression]
Implementation specifics if mid-task

## RECOVERY CONTEXT [Maintainer/Architect - 45% compression]
Broader project context, decision rationale, architecture notes

## FILES MODIFIED [Developer/Maintainer - 40% compression]
Changed files, locations, purposes

## BLOCKERS [Coordinator - 60% compression]
Issues preventing progress

## NOTES [Variable by section]
Additional context as needed
```

**Navigation Pattern:**
- Strategic: WHERE + ACCOMPLISHED only (~1-2 minutes)
- Coordinator: WHERE + ACCOMPLISHED + NEXT + BLOCKERS (~3-5 minutes)
- Developer: WHERE + NEXT + Technical Details + FILES (~5-10 minutes)
- Architect: WHERE + RECOVERY + skims others (~8-12 minutes)
- Maintainer: WHERE + RECOVERY + FILES (~10-15 minutes)
- Full read: Only when needed (~15-20 minutes)

**Why It Works:**
- Progressive depth allows selective reading
- High-level sections satisfy most roles quickly
- Deep context preserved for roles that need it
- Compounds with frequency: 2-minute savings × 200 sessions = 400 minutes saved/year per role

### 8.2 PROJECT.md (Strategic Context Document)

**Context:** Long-lived, all-roles reference, evolves over project lifetime

**Roles:** All 6 roles with varying needs

**Divergence:** Up to 50%

**Strategy:** Layered - Progressive Detail with stable structure

**Structure:** (Already covered in Part 4.4 Example 1)

**Key Innovation:** Strategic Context section evolves, other sections append-only
- Allows high-level to stay current and concise
- Preserves deep history for maintainers
- Balance between accessibility and preservation

### 8.3 TASKS.md (Work Tracking)

**Context:** Daily developer work, coordinator status tracking

**Roles:**
- Developer: 30-50% compression (primary)
- Coordinator: 50-70% compression (secondary)

**Divergence:** 20-40%

**Strategy:** Intersection with inline accommodations

**Structure:** (Already covered in Part 3.4 Example 1)

**Key Techniques:**
- Status fields prominent at top
- Implementation details preserved for developers
- Status Updates section for coordinator timeline
- Acceptable trade-off: Coordinator scans longer but gets what they need

### 8.4 Configuration Documentation (Architect Primary)

**Context:** System configuration strategy and implementation

**Roles:**
- Architect: 40-60% compression (design decisions)
- Developer: 30-50% compression (implementation)
- Orchestrator: 60-80% compression (deployment automation)

**Divergence:** 0-40% (varies by role pair)

**Strategy:** Intersection with Architect primary + section accommodations

**Key Approach:**
- Architect focus: Design rationale and strategy
- Developer section: Implementation inline (moderate compression)
- Orchestrator: Quick reference + link to automation docs

**Why Not Layered:**
- Frequency: Weekly for Architect, less for others
- Cost/benefit doesn't justify full layered
- Intersection with good accommodations sufficient

### 8.5 Archive Documents (Maintainer Primary)

**Context:** Completed project documentation, rarely accessed

**Roles:**
- Maintainer: 30-50% compression (historical reference)
- Occasional reference by others: 60-80% compression sufficient

**Divergence:** 30-50% but low frequency

**Strategy:** Intersection with Maintainer primary, aggressive compression of non-essential

**Structure:**
```markdown
# [Archived Project] Documentation

**Status:** ARCHIVED [Date]
**Historical Value:** [Why preserved]

## Summary [Quick reference for all - 80% compression]
What was accomplished, final outcomes, key learnings

## Complete Context [Maintainer deep reference - 40% compression]
Full project history, decisions, rationale, evolution

## Technical Details [Searchable reference - 50% compression]
Implementation specifics, preserved for future similar work

## Lessons Learned [Strategic value - 60% compression]
What worked, what didn't, recommendations
```

**Key Points:**
- Summary highly compressed (most roles only need this)
- Maintainer section preserved in detail (historical value)
- Searchable for future reference (primary archive value)
- Does not need to be skimmable (search-first access pattern)

### 8.6 API Documentation (Developer + Orchestrator)

**Context:** Technical reference for using APIs

**Roles:**
- Developer: 30-50% compression (comprehensive understanding)
- Orchestrator: 60-80% compression (automation scripting)

**Divergence:** 30-50%

**Strategy:** Depends on orchestrator needs:
- If orchestrator needs technical depth: Union (30-40%)
- If orchestrator needs quick reference: Intersection or Core+Extensions

**Common Pattern:**
```markdown
# API Documentation

## Quick Reference [Orchestrator - 70% compression]
[Table of endpoints, methods, purposes]

## Detailed Reference [Developer - 35% compression]

### Endpoint: POST /api/users
[Full detail: params, responses, examples, error handling]

### Endpoint: GET /api/users/{id}
[Full detail...]
```

**Why This Works:**
- Orchestrators scan Quick Reference table
- Developers read detailed sections as needed
- Both needs served without duplication

### 8.7 Runbooks (Orchestrator Primary)

**Context:** Operational procedures, incident response

**Roles:**
- Orchestrator: 60-80% compression (execution focus)
- Developer: 30-50% compression (deep troubleshooting)

**Divergence:** 30-50%

**Strategy:** Layered - Core + Extensions

**Structure:**
```
/docs/operations/
  runbooks/
    core-procedures.md [Orchestrator - 70% compression]
      - Step-by-step execution
      - When to escalate
      - Quick diagnostics
    
    troubleshooting/ [Developer extensions - 35% compression]
      deep-dive-debugging.md
      system-internals.md
      advanced-diagnostics.md
```

**Rationale:**
- Orchestrators need fast execution (incidents are time-sensitive)
- Developers need deep context when orchestrators escalate
- Separation prevents cognitive load during incidents
- Extensions available when needed but not in critical path

---

## Part 9: Best Practices and Anti-Patterns

### 9.1 Best Practices

**1. Document Strategy Choice Explicitly**
```markdown
**Strategy:** Intersection (Developer primary)
**Divergence:** 35%
**Rationale:** Developer daily access (critical), Coordinator weekly (acceptable compromise)
```

**Why:** Future maintainers understand optimization decisions, can reassess if context changes

**2. Provide Navigation Guidance**
```markdown
## How to Use This Document

- **Developers:** Read full document, focus on Implementation sections
- **Coordinators:** Read Summary + Status Updates only
- **Architects:** Read Summary + System Design + skim Implementation
```

**Why:** Reduces cognitive load, roles know where to focus

**3. Progressive Disclosure in Long Documents**
```markdown
## High-Level Summary [2 min read]
[Core information all roles need]

## Detailed Analysis [15 min read]
[Deep dive for specialist roles]
```

**Why:** Respects reader's time, allows quick scanning before deep reading

**4. Use Inline Role Markers**
```markdown
### Implementation Details [Developer Primary]
[Technical content...]

**For Coordinators:** This section contains implementation specifics. 
See Status Updates section for progress tracking.
```

**Why:** Prevents role confusion, guides selective reading

**5. Link Rather Than Duplicate**
```markdown
For deployment automation details, see [Operations Runbook](../operations/deployment.md)

For architectural rationale, see [ADR-0123](../decisions/adr-0123.md)
```

**Why:** Reduces maintenance overhead, single source of truth

**6. Establish Maintenance Rhythms**
```markdown
**Review Frequency:** Quarterly
**Owner:** Platform Team
**Process:** Validate strategy still appropriate, check role feedback
```

**Why:** Prevents document drift, catches strategy mismatches early

### 9.2 Anti-Patterns to Avoid

**Anti-Pattern 1: Premature Layering**

❌ **Bad:**
```
Creating separate role views for document accessed monthly with 25% divergence

Cost: High maintenance overhead
Benefit: Minimal (low frequency × moderate divergence)
```

✅ **Good:**
```
Use Intersection strategy, add lightweight accommodations
If access frequency increases, reassess later
```

**Anti-Pattern 2: Unexplained Optimization**

❌ **Bad:**
```markdown
# Configuration Guide
[Moderately compressed content with no role indication]
```

**Problem:** Readers don't know if this is right detail level for them

✅ **Good:**
```markdown
# Configuration Guide
**Target Audience:** Architects (system design focus)
**For Developers:** See [Implementation Guide](dev-guide.md) for code-level details
**For Operators:** See [Deployment Guide](deploy-guide.md) for automation
```

**Anti-Pattern 3: Hidden Navigation**

❌ **Bad:**
```markdown
[100-line document with sections for different roles, no guidance on which to read]
```

**Problem:** All roles read everything or miss important sections

✅ **Good:**
```markdown
## Navigation Guide (at top)
- Strategic: Read Executive Summary only
- Developers: Read sections 2, 4, 5
- Architects: Read sections 1, 2, 3
```

**Anti-Pattern 4: Duplication Without Linking**

❌ **Bad:**
```
/docs/feature-x/
  developer-view.md [Contains full system architecture]
  architect-view.md [Contains same architecture information]
```

**Problem:** Updates must be made twice, inconsistency risk

✅ **Good:**
```
/docs/feature-x/
  architecture.md [Single source of architecture]
  developer-view.md [Links to architecture, adds implementation detail]
  architect-view.md [Links to architecture, adds design rationale]
```

**Anti-Pattern 5: Ignoring Frequency**

❌ **Bad:**
```
Monthly-accessed document with full layered strategy (multiple role views)

Overhead: High
Benefit: Low (infrequent access doesn't compound savings)
```

✅ **Good:**
```
Use Intersection strategy for monthly docs
Save layered for daily/weekly high-frequency documents
```

**Anti-Pattern 6: Over-Engineering Low-Divergence Cases**

❌ **Bad:**
```
Developer (30-50%) + Maintainer (30-50%) documentation with separate role views

Divergence: 0-20%
Complexity: Unnecessary
```

✅ **Good:**
```
Union strategy at 35-40% compression
Serves both roles well with single document
```

**Anti-Pattern 7: Forgetting Secondary Role Validation**

❌ **Bad:**
```
Optimize for primary role, never test if secondary roles can accomplish purposes

Result: Secondary roles frustrated, complain about missing information
```

✅ **Good:**
```
After optimization, validate each secondary role can complete >80% of purposes
If not, adjust accommodations or reconsider strategy
```

### 9.3 Common Pitfalls

**Pitfall 1: Compression Creep**
- **Problem:** Document optimized for one role, gradually accumulates detail for others
- **Result:** Returns to poorly-optimized multi-role state
- **Prevention:** Quarterly reviews, enforce strategy discipline

**Pitfall 2: Role Assumption Errors**
- **Problem:** Assume role needs without validation
- **Result:** Optimize for wrong compression target
- **Prevention:** Ask roles what they actually need, test with real users

**Pitfall 3: Static Strategy in Dynamic Context**
- **Problem:** Set strategy once, never revisit as project evolves
- **Result:** Strategy becomes inappropriate (frequency changes, new roles, etc.)
- **Prevention:** Trigger review on major project transitions, role changes

**Pitfall 4: Consistency Failure in Layered Docs**
- **Problem:** Update one view, forget to update related views
- **Result:** Inconsistent information, user confusion
- **Prevention:** Update checklists, automated consistency checks, clear ownership

**Pitfall 5: Navigation Complexity**
- **Problem:** Too many role views, users don't know which to read
- **Result:** Cognitive overhead negates optimization benefits
- **Prevention:** Limit role views to essential, provide clear navigation, default recommendations

---

## Part 10: Integration with Broader Framework

### 10.1 Relationship to Multi-Dimensional Compression Matrix

**Matrix Provides:**
- Base compression targets per role (6 roles)
- Layer-specific adjustments (5 layers)
- Phase-aware modifiers (6 phases)
- Mode-switching considerations

**This Guide Provides:**
- How to handle when document serves multiple roles simultaneously
- Strategy selection based on role divergence
- Cost/benefit analysis for implementation approaches
- Validation that all roles can accomplish purposes

**Integration:**
```
1. Use Matrix to identify compression target for each role viewing document
2. Calculate divergence between role targets
3. Use this Guide to select strategy (Union/Intersection/Layered)
4. Apply strategy-specific optimization approach
5. Validate each role using processes in this Guide
6. Document strategy choice and rationale
```

### 10.2 Relationship to Information Preservation Framework

**Framework Provides:**
- 7 documentation purposes (WHY we document)
- Phase-aware compression guidance (WHEN to compress)
- ROI prioritization (WHAT to optimize first)
- Anti-compression patterns (when NOT to compress)

**This Guide Provides:**
- HOW to handle multiple audiences for same document
- Multi-role-specific trade-off analysis
- Strategy selection for competing optimization goals
- Validation that purposes preserved for all roles

**Integration:**
```
1. Use Framework to identify document purpose(s) and phase
2. Use Matrix to get role targets
3. Calculate multi-role divergence
4. Use this Guide to select and implement strategy
5. Use Framework's validation to ensure purposes preserved
6. Use Framework's ROI to prioritize which multi-role docs to optimize
```

### 10.3 Complete Decision Process

**Step-by-Step Multi-Role Compression Decision:**

**1. Document Analysis**
```
- Purpose: [From Framework - WHY]
- Phase: [From Framework - WHEN]
- Roles: [List all roles who read this document]
- Frequency: [Per role, from ROI framework]
```

**2. Target Calculation**
```
For each role:
- Base target from Matrix
- Layer-specific adjustment
- Phase modifier
- Final target: [X-Y%]
```

**3. Divergence Assessment**
```
- Most detail needed: [Role A at X%]
- Least detail needed: [Role B at Y%]
- Divergence: |X - Y| = Z%
```

**4. Strategy Selection**
```
If Z < 20%: Union strategy
If Z = 20-40%: Intersection (if primary clear) or borderline Layered
If Z > 40%: Evaluate Layered cost/benefit
```

**5. Cost/Benefit (if Layered considered)**
```
- Frequency × Criticality score
- Creation + maintenance overhead
- Time savings per access × roles
- ROI calculation
- Decision: Implement Layered? Yes/No
```

**6. Implementation**
```
- Apply selected strategy using templates from this Guide
- Create optimized version(s)
- Document strategy choice in header
```

**7. Validation**
```
- Test each role can accomplish purposes (this Guide)
- Verify information preserved per purpose (Framework)
- Measure actual vs expected access patterns
```

**8. Maintenance**
```
- Document ownership and process
- Schedule quarterly review
- Monitor for strategy migration triggers
```

### 10.4 Framework Coverage Summary

**Complete Coverage Across Three Documents:**

**Documentation Types Matrix (WHO):**
- Defines 6 audience categories
- Maps to project roles
- Provides base compression ranges

**Multi-Dimensional Compression Matrix (HOW MUCH):**
- Quantitative targets: [Role × Layer × Phase]
- Conflict resolution
- Mode-switching
- Worked examples

**Information Preservation Framework (WHY + WHEN):**
- 7 documentation purposes
- Phase-aware compression (6 phases)
- ROI prioritization
- Anti-compression patterns
- Validation requirements

**Multi-Role Document Strategies (THIS GUIDE - HOW to handle multiple roles):**
- Strategy selection: Union/Intersection/Layered
- Divergence calculation and decision trees
- Cost/benefit analysis for layered approaches
- Implementation templates and patterns
- Validation and quality assurance
- Common scenarios and best practices

**Together:** Complete methodology for systematic compression decisions on any document, single-role or multi-role.

---

## Conclusion

Multi-role documents are common, not edge cases. Effective multi-role optimization requires:

1. **Systematic Divergence Assessment**: Calculate role target differences quantitatively
2. **Strategy Selection**: Match strategy to divergence, frequency, and criticality
3. **Cost/Benefit Discipline**: Don't over-engineer, especially low-frequency docs
4. **Validation Rigor**: Ensure all roles can accomplish purposes, not just primary
5. **Maintenance Planning**: Document strategy, establish ownership, schedule reviews
6. **Integration**: Use with Matrix and Framework for complete decision system

**Key Takeaways:**

- **<20% divergence:** Union strategy (optimize for most detail)
- **20-40% divergence:** Intersection strategy (primary role + accommodations)
- **>40% divergence:** Evaluate Layered strategy (cost/benefit must justify overhead)
- **High frequency × criticality:** Strong indicator for layered investment
- **Always validate:** Each role must accomplish >80-90% of purposes
- **Document strategy choice:** Future maintainers need context

**Common Mistake to Avoid:** Premature layering on low-frequency documents

**Success Pattern:** Start with simpler strategies (Union/Intersection), migrate to Layered only when ROI clearly justifies the overhead

**Framework Integration:** This Guide completes the systematic compression methodology by addressing the multi-role optimization challenge that appears frequently in real projects.

---

**Next Steps:**
- Apply strategies to multi-role documents in your project
- Test with representative users from each role
- Monitor access patterns and adjust strategies as needed
- Document strategy choices for future maintainers
- Review quarterly and evolve as project context changes

---

*This guide is part of the Compression Project framework for systematic documentation optimization.*