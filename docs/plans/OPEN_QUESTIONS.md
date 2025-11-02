# Open Questions - Strategic Replanning

**Date**: 2025-11-01 (Session 13)
**Context**: Paradigm shift from reactive to proactive+reactive compression
**Purpose**: Capture uncertainties requiring strategic decisions
**Review By**: TASK-6.1 Project Review

---

## Scope & Boundaries

### Q1: What's In Scope?
**Question**: How much should we build vs document vs leave to users?

**Options**:
- **A)** Theory + Tool only (original scope)
- **B)** Theory + Tool + Integration guidance (minimal expansion)
- **C)** Theory + Tool + Templates + Skill (full proactive)
- **D)** Complete methodology with all 6 layers (maximum scope)

**Considerations**:
- User preference: "Elegant full solution (not partial)"
- Risk: Scope creep without boundaries
- Value: Proactive patterns may have higher adoption
- Effort: Each layer adds 4-12 hours of work

**Decision Needed**: Where do we draw the line?

---

### Q2: Framework vs Methodology vs Reference Implementation?

**Question**: What are we actually building?

**Options**:
- **Framework**: Theory + decision matrices + guidance
- **Methodology**: Framework + practical patterns + integration
- **Reference Implementation**: Methodology + complete working examples

**Implications**:
```
Framework:
- Scope: Theory-heavy, practical patterns minimal
- Users: Need to implement themselves
- Effort: Lower
- Value: Flexible but requires expertise

Methodology:
- Scope: Theory + patterns + integration guidance
- Users: Can follow patterns to implement
- Effort: Medium
- Value: Practical adoption easier

Reference Implementation:
- Scope: Everything including working examples
- Users: Can copy/paste and adapt
- Effort: Higher
- Value: Highest adoption, lowest barriers
```

**Decision Needed**: Which level of completeness?

---

### Q3: Monolithic or Modular?

**Question**: How should the framework be structured?

**Current**: 14,873 lines in docs/ directory (mostly monolithic)

**Options**:
- **Monolithic**: Keep as integrated framework documentation
  - Pro: Single source of truth
  - Con: Overwhelming, hard to navigate

- **Modular**: Split into separate concerns
  - Pro: Easier to understand and maintain
  - Con: Integration complexity, cross-references

**Potential Modular Structure**:
```
docs/
├─ theory/
│  ├─ UNIFIED_MODEL.md (σ,γ,κ parameters)
│  ├─ DECISION_MATRIX.md (Role × Layer × Phase)
│  └─ CONVERGENCE.md (intrinsic stability)
├─ reactive/
│  ├─ TOOL_GUIDE.md (compress.py usage)
│  ├─ TECHNIQUES.md (LSC methods)
│  └─ SAFETY.md (validation system)
├─ proactive/
│  ├─ TEMPLATES.md (pre-optimization)
│  ├─ SKILL_GUIDE.md (Claude integration)
│  └─ PATTERNS.md (best practices)
├─ integration/
│  ├─ DECISION_FRAMEWORKS.md
│  ├─ USE_CASES.md
│  └─ CASE_STUDIES.md (CCM example)
└─ lifecycle/
   ├─ PHASES.md (Active → Archive)
   └─ MAINTENANCE.md (update patterns)
```

**Decision Needed**: Restructure now or later? How granular?

---

## Implementation Priorities

### Q4: Outstanding Tasks Still Relevant?

**TASK-5.2**: Threshold Calibration (MEDIUM, 4-6 hours)
- **Status**: Deferred post-deployment
- **Question**: Still needed? Or is intrinsic stability proof enough?
- **Consideration**: Conservative thresholds work fine, tuning may not add value

**TASK-5.3**: LSC Technique Improvement (MEDIUM, 8-12 hours)
- **Status**: Depends on 5.1 findings
- **Question**: Worth improving reactive techniques vs building proactive?
- **Consideration**: Better compression ratios vs new paradigm

**TASK-5.4**: Model Caching (LOW, 2-3 hours)
- **Status**: Performance optimization
- **Question**: User pain point or premature optimization?
- **Consideration**: 20-25s is acceptable, 15-20s is loading

**Decision Needed**: Complete these or deprioritize for proactive work?

---

### Q5: Which Layer Has Highest Value?

**Priority Assessment**:

**Layer 3 - Templates** (4-6 hours):
- Value: Medium-High
- Effort: Low-Medium
- Impact: Guides efficient writing
- Adoption: Easy (just use templates)

**Layer 4 - Claude Skill** (4-6 hours):
- Value: HIGHEST
- Effort: Medium
- Impact: Transforms compression experience
- Adoption: Automatic once installed

**Layer 5 - Integration Patterns** (8-12 hours):
- Value: High
- Effort: Medium-High
- Impact: Enables other projects to adopt
- Adoption: Requires understanding

**Layer 6 - Lifecycle Management** (4-6 hours):
- Value: Medium
- Effort: Low-Medium
- Impact: Long-term maintainability
- Adoption: Optional, for mature projects

**Decision Needed**: Build order and which are MVP vs future?

---

### Q6: Incremental Shipping Strategy?

**Question**: Can we ship pieces or must everything be complete?

**Options**:

**Option A - Ship Layers Sequentially**:
```
v1.0: Theory + Reactive Tool (current state)
v1.1: + Templates
v1.2: + Claude Skill
v1.3: + Integration Patterns
v2.0: + Lifecycle Management
```

**Option B - Ship By Use Case**:
```
v1.0: Reactive compression (compress existing content)
v2.0: Proactive compression (write compressed natively)
v3.0: Complete methodology (lifecycle + integration)
```

**Option C - Ship When Complete**:
```
v1.0: All 6 layers documented and implemented
     (wait until everything ready)
```

**Considerations**:
- User preference: "Elegant full solution (not partial)"
- Pragmatism: "Simple solutions for 95% of cases"
- Risk: Shipping incomplete vs never shipping

**Decision Needed**: Release strategy?

---

## White Paper Strategy

### Q7: White Paper Scope?

**Question**: What belongs in academic white paper vs separate documentation?

**Options**:

**Option A - Theory Only**:
- (σ,γ,κ) unified model
- Mathematical proofs
- Empirical validation
- Convergence properties
- Academic contribution focused

**Option B - Theory + Practical Patterns**:
- Everything in Option A
- Proactive compression patterns
- Integration frameworks
- CCM case study
- More comprehensive but less focused

**Option C - Theory Paper + Integration Guide**:
- White paper: Theory and validation
- Separate: Integration guide with practical patterns
- Clean separation of concerns

**Considerations**:
- Academic audience vs practitioner audience
- Paper length (30-50 pages theory vs 60-80 with patterns)
- Publication venue expectations

**Decision Needed**: White paper boundaries?

---

### Q8: CCM Case Study Inclusion?

**Question**: Should CCM project be documented as case study?

**Pros**:
- Real-world validation
- Shows framework adoption
- Demonstrates integration patterns
- Validates (σ,γ,κ) independently

**Cons**:
- External project dependency
- May complicate white paper
- Not our implementation

**Alternatives**:
- Brief mention in white paper
- Detailed case study in integration guide
- Appendix in white paper
- Omit entirely (internal validation only)

**Decision Needed**: How to handle CCM insights?

---

## User Adoption

### Q9: Which Scenarios Support in v1.0?

**Scenario 1 - Reactive Compression**:
- User has existing verbose content
- Wants to optimize and compress
- Tools: compress.py ✅

**Scenario 2 - Proactive Writing**:
- User creating new content
- Wants to write efficiently from start
- Tools: Templates ❌ + Skill ❌

**Scenario 3 - Full Methodology**:
- User wants complete lifecycle management
- Needs integration in project workflow
- Tools: Everything ❌

**Question**: Which scenarios MUST work in v1.0?

**Considerations**:
- compress.py is production-ready (Scenario 1 works now)
- Proactive tools not built (Scenario 2 doesn't work)
- Integration incomplete (Scenario 3 doesn't work)

**Decision Needed**: MVP definition?

---

### Q10: Adoption Path Design?

**Question**: How do users get started?

**Current path** (implicit):
1. Read 14,873 lines of framework
2. Understand (σ,γ,κ) theory
3. Install compress.py
4. Configure and use

**Issues**:
- High barrier to entry
- No guided onboarding
- Missing quickstart
- Unclear value proposition

**Better path** (proposed):
1. **Quickstart**: 5-minute introduction
2. **Use case selection**: What do you want to do?
   - Compress existing content → Reactive guide
   - Write new content → Proactive guide
   - Full integration → Methodology guide
3. **Installation**: Tools and templates
4. **Tutorial**: Guided examples
5. **Reference**: Deep documentation

**Decision Needed**: Create onboarding materials?

---

## Integration & Modularity

### Q11: How Do Projects Reference Framework?

**Question**: What's the integration model?

**Options**:

**Option A - Fork and Customize**:
- Copy framework to project
- Modify for specific needs
- Standalone, no dependencies

**Option B - Submodule/Reference**:
- Link to framework repo
- Use as-is or extend
- Updates propagate

**Option C - NPM-style Package**:
- Install as dependency
- Import components
- Version management

**Considerations**:
- Simplicity vs flexibility
- Update propagation
- Customization needs
- User technical sophistication

**Decision Needed**: Distribution model?

---

### Q12: Template Library Scope?

**Question**: How many templates and how detailed?

**Minimal** (5-8 templates):
- High compression (status, metrics)
- Medium compression (analysis, specs)
- Low compression (strategy, narrative)
- Basic coverage only

**Comprehensive** (15-20 templates):
- Multiple variants per compression level
- Domain-specific (engineering, PM, analysis)
- Use-case specific (onboarding, API docs, decisions)
- Complete coverage

**Reference Implementation** (30+ templates):
- Everything in Comprehensive
- Real-world examples
- Multiple industries/domains
- Copy-paste ready

**Considerations**:
- Effort: 1 hour per template for quality
- Maintenance: Updates needed over time
- Value: Diminishing returns after core set

**Decision Needed**: Template library size?

---

### Q13: Frontmatter Standard?

**Question**: What parameters and format?

**Minimal**:
```yaml
---
compression:
  sigma: 0.6
  gamma: 0.5
  kappa: 0.3
---
```

**Extended**:
```yaml
---
compression:
  sigma: 0.6        # Structure density
  gamma: 0.5        # Granularity
  kappa: 0.3        # Scaffolding
  audience: dual    # LLM | human | dual
  tier: T2          # T1 | T2 | T3
  phase: active     # active | complete | archive
  updated: 2025-11-01
---
```

**Comprehensive**:
```yaml
---
compression:
  parameters:
    sigma: 0.6
    gamma: 0.5
    kappa: 0.3
  context:
    audience: dual
    tier: T2
    phase: active
    role: PM
    layer: strategic
  metadata:
    created: 2025-10-29
    updated: 2025-11-01
    version: 1.2
  techniques:
    - lists_tables
    - hierarchical_structure
---
```

**Decision Needed**: Frontmatter spec and extensibility?

---

## Technical Architecture

### Q14: Claude Skill Implementation Details?

**Question**: How should skill work technically?

**Approach A - Instruction-Based**:
```markdown
# compression.md

When writing documents with compression metadata:
1. Read frontmatter parameters
2. Apply techniques based on σ,γ,κ values
3. Maintain compression throughout
```

**Approach B - Examples-Heavy**:
```markdown
# compression.md

σ=0.3 example: [prose example]
σ=0.6 example: [structured example]
σ=0.9 example: [dense example]

Match style to parameters.
```

**Approach C - Hybrid**:
- Instructions for behavior
- Examples for each (σ,γ,κ) range
- Technique reference
- Validation guidance

**Decision Needed**: Skill structure and depth?

---

### Q15: Tool Integration?

**Question**: Should compress.py read frontmatter parameters?

**Current**: Tool has hardcoded technique selection

**Proposed**: Tool reads (σ,γ,κ) and applies appropriate techniques

**Benefits**:
- Consistent with skill approach
- Automated technique selection
- Easier to use

**Drawbacks**:
- More complex tool
- Parameter interpretation needed
- May limit power-user control

**Decision Needed**: Enhance tool or keep separate?

---

## Documentation & Maintenance

### Q16: Documentation Split?

**Question**: One mega-doc or multiple focused docs?

**Current Pain**:
- Framework: 14,873 lines (overwhelming)
- Hard to navigate
- Unclear where to start
- Mixes theory, implementation, validation

**Proposed Split**:
```
Compression Framework/
├─ README.md (overview, quickstart)
├─ THEORY.md (σ,γ,κ model, proofs)
├─ REACTIVE_GUIDE.md (compress.py usage)
├─ PROACTIVE_GUIDE.md (templates + skill)
├─ INTEGRATION_GUIDE.md (adoption patterns)
├─ CASE_STUDIES.md (CCM + others)
├─ REFERENCE.md (complete technical reference)
└─ WHITE_PAPER.md (academic formalization)
```

**Decision Needed**: Restructure timing and approach?

---

### Q17: Maintenance Strategy?

**Question**: How to keep framework updated?

**Considerations**:
- Templates need periodic refresh
- Skill needs tuning based on usage
- Integration patterns emerge over time
- Theory is stable, patterns evolve

**Options**:
- Version releases (v1.0, v1.1, etc.)
- Rolling updates (continuous improvement)
- Hybrid (theory stable, patterns updated)

**Decision Needed**: Update cadence and process?

---

## Project Completion Definition

### Q18: What Does "Done" Look Like?

**Question**: How do we know project is complete?

**Option A - MVP Done**:
```
✓ Theory validated
✓ compress.py production-ready
✓ Basic documentation
✓ White paper drafted
```

**Option B - Full Framework Done**:
```
✓ All 6 layers implemented
✓ Complete documentation
✓ Template library (15-20)
✓ Claude skill deployed
✓ Integration guide comprehensive
✓ White paper published
✓ Case studies documented
```

**Option C - Sustainable Ecosystem**:
```
✓ Everything in Option B
✓ Community contributions enabled
✓ Maintenance plan documented
✓ Adoption metrics tracked
✓ Continuous improvement process
```

**Decision Needed**: Project completion criteria?

---

### Q19: Relationship to Outstanding Work?

**Question**: What happens to TASK-5.2, 5.3, 5.4?

**Options**:
- Complete before moving to proactive
- Defer indefinitely (focus on proactive)
- Integrate into replanned roadmap
- Cancel (not needed given paradigm shift)

**Considerations**:
- Sunk cost fallacy (don't do just because planned)
- Opportunity cost (proactive may have higher ROI)
- Completeness (do we need these for production?)

**Decision Needed**: Outstanding task disposition?

---

## Success Criteria

### Q20: How Do We Measure Success?

**Metrics to Consider**:

**Theory Quality**:
- Mathematical rigor
- Empirical validation
- Peer review acceptance

**Tool Adoption**:
- compress.py usage
- Template downloads
- Skill installations

**Framework Impact**:
- Projects adopting methodology
- Token savings achieved
- User satisfaction

**Academic Contribution**:
- White paper citations
- Research extensions
- Industry adoption

**Decision Needed**: Which metrics matter for this project?

---

## Summary of Critical Decisions

**Must Decide**:
1. Scope boundaries (Q1, Q2)
2. MVP definition (Q9, Q18)
3. Build priorities (Q5, Q6)
4. White paper scope (Q7, Q8)

**Should Decide**:
5. Framework structure (Q3, Q16)
6. Outstanding tasks (Q4, Q19)
7. Adoption path (Q10)
8. Integration model (Q11)

**Can Defer**:
9. Template library size (Q12)
10. Frontmatter standard details (Q13)
11. Skill implementation details (Q14)
12. Maintenance strategy (Q17)
13. Success metrics (Q20)

---

**Status**: Questions documented, awaiting TASK-6.1 analysis and strategic decisions
