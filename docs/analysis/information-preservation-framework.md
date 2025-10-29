# Information Preservation Framework: Purpose-Driven Compression

**Created**: 2025-10-29 22:25 AEDT
**Purpose**: Systematic framework for determining what information to preserve based on documentation purpose, with methods for analyzing content and selecting optimal representation formats
**Status**: Initial framework

---

## Executive Summary

**Critical Problem**: Compression without understanding purpose leads to information loss. A decision log compressed for "quick reference" loses learning value. A specification compressed for "execution" loses design rationale.

**Core Insight**: Documentation serves multiple purposes simultaneously or evolves between purposes over time. Safe compression requires:
1. **Identifying all purposes** the document serves (now and future)
2. **Mapping essential information** for each purpose
3. **Preserving the union** of all essential information sets
4. **Selecting optimal format** for primary purpose
5. **Validating preservation** against all purposes

**Framework Output**: Systematic methods to analyze any document, identify what can be safely stripped, and determine optimal representation format.

---

## Part 1: Documentation Purposes - Comprehensive Taxonomy

### Primary Purpose Categories

#### 1. **Execution Purposes** (Do Something)
Document enables someone/something to perform an action.

**Sub-purposes**:
- **Instruction**: Step-by-step procedures (how to do X)
- **Configuration**: System/tool setup (what settings to use)
- **Specification**: Requirements to implement (what to build)
- **Decision Application**: Apply a prior decision (what was decided)

**Essential Information**:
- ✅ What to do (actionable steps/requirements)
- ✅ Constraints and requirements
- ✅ Success criteria
- ✅ Critical context for correct execution
- ⚠️ Why (optional - helps with edge cases)
- ❌ Alternatives considered (not needed for execution)
- ❌ Discussion history (not needed for execution)

**Safe to Strip**:
- Rationale and explanation (unless affects execution)
- Historical context
- Alternative approaches
- Learning content
- Verbose examples (keep only essential ones)

**Optimal Format**: 
- Structured imperative (YAML/JSON for configs, numbered steps for procedures)
- High information density
- Minimal prose

---

#### 2. **Learning Purposes** (Understand Something)
Document teaches concepts, approaches, or context.

**Sub-purposes**:
- **Onboarding**: Help newcomers understand system/domain
- **Skill Development**: Build expertise
- **Context Building**: Understand why things are the way they are
- **Pattern Recognition**: Learn reusable approaches

**Essential Information**:
- ✅ Concepts and principles
- ✅ Rationale and reasoning (why)
- ✅ Examples and illustrations
- ✅ Context and background
- ✅ Alternatives and trade-offs
- ✅ Common pitfalls and gotchas
- ✅ Progressive complexity (simple → advanced)

**Safe to Strip**:
- Redundant explanations of same concept
- Excessive examples (keep representative ones)
- Verbose transitions

**Optimal Format**:
- Prose with examples
- Progressive disclosure (overview → details)
- Moderate verbosity acceptable
- Visual aids valuable

---

#### 3. **Reference Purposes** (Look Up Something)
Document provides quick access to specific facts or specifications.

**Sub-purposes**:
- **API Reference**: Function signatures, parameters, returns
- **Configuration Reference**: Available options and values
- **Data Dictionary**: Field definitions and formats
- **Quick Facts**: Specific values, formulas, constants

**Essential Information**:
- ✅ Specific facts and values
- ✅ Structure and organization (findability)
- ✅ Complete specifications
- ✅ Examples of usage
- ⚠️ Brief descriptions (minimal context)
- ❌ Extensive rationale
- ❌ Historical context

**Safe to Strip**:
- Verbose explanations
- Background and history
- Extended examples (keep one canonical example)
- Motivational content

**Optimal Format**:
- Highly structured (tables, YAML, JSON)
- Consistent organization
- Scannable (headers, lists)
- Dense but organized

---

#### 4. **Audit/Compliance Purposes** (Prove Something)
Document provides evidence for decisions, actions, or compliance.

**Sub-purposes**:
- **Decision Trail**: Who decided what and when
- **Compliance Record**: Evidence of following requirements
- **Accountability**: Track responsibility
- **Legal Protection**: Defensible record

**Essential Information**:
- ✅ What was decided/done
- ✅ Who made the decision/performed action
- ✅ When it occurred (timestamps)
- ✅ Authority/approval chain
- ✅ Rationale (defensibility)
- ✅ Alternatives considered (due diligence)
- ✅ Risk assessment
- ✅ Traceability to requirements

**Safe to Strip**:
- Redundant discussion (but keep decisions)
- Informal communication
- Excessive detail in rationale (keep key points)

**Optimal Format**:
- Structured with metadata (who, when, what)
- Preserved verbatim or lightly summarized
- Immutable records
- Timestamped entries

**Cannot Strip**: Almost nothing - compliance requires comprehensive records

---

#### 5. **Communication Purposes** (Tell Someone)
Document conveys information to specific audiences.

**Sub-purposes**:
- **Status Update**: Current state and progress
- **Proposal**: Persuade adoption of approach
- **Report**: Inform stakeholders
- **Handover**: Transfer knowledge between people/sessions

**Essential Information**:
- ✅ Key message (what they need to know)
- ✅ Audience-appropriate context
- ✅ Actionable items (if any)
- ✅ Current state
- ⚠️ Background (calibrate to audience knowledge)
- ⚠️ Supporting details (enough to convince/inform)

**Safe to Strip**:
- Verbose explanations (once communicated, can compress for archive)
- Excessive background for knowledgeable audiences
- Persuasive elements (once decision made)

**Optimal Format**:
- Audience-dependent (technical vs general)
- Clear structure (executive summary → details)
- Progressive disclosure
- May need multiple versions per audience

---

#### 6. **Analysis/Research Purposes** (Explore Something)
Document captures investigation, findings, and insights.

**Sub-purposes**:
- **Problem Investigation**: Understanding a problem
- **Solution Exploration**: Evaluating approaches
- **Data Analysis**: Extracting insights from data
- **Feasibility Study**: Assess viability

**Essential Information**:
- ✅ Problem/question being explored
- ✅ Methodology used
- ✅ Findings and insights
- ✅ Data/evidence supporting conclusions
- ✅ Limitations and caveats
- ⚠️ Exploration process (valuable for learning, not for reference)

**Safe to Strip**:
- Dead-end explorations (keep mention, not full detail)
- Redundant data (keep summary statistics, not raw data)
- Verbose process descriptions (keep key insights)

**Optimal Format**:
- Structured findings document
- Compress exploration, preserve insights
- May need two versions: full (during) and summary (after)

---

#### 7. **Maintenance/Evolution Purposes** (Change Something)
Document enables understanding and modifying existing systems.

**Sub-purposes**:
- **Debugging**: Understand why something behaves unexpectedly
- **Enhancement**: Add capabilities
- **Refactoring**: Improve without changing behavior
- **Migration**: Move to new approach

**Essential Information**:
- ✅ Design rationale (why it works this way)
- ✅ Constraints and assumptions
- ✅ Dependencies and relationships
- ✅ Known limitations
- ✅ Alternative approaches and why rejected
- ✅ Evolution history (major changes)

**Safe to Strip**:
- Minor implementation details
- Obsolete approaches (once migrated)
- Excessive historical minutiae (keep key decisions)

**Optimal Format**:
- Decision records (ADRs)
- Rationale-rich but concise
- Structured for finding relevant decisions

---

### Purpose Multiplicity and Evolution

**Critical Reality**: Most documents serve **multiple purposes simultaneously** or **evolve between purposes**.

**Example: Decision Document**
- **During**: Communication (proposal, discussion, persuasion)
- **Immediate after**: Execution (apply the decision)
- **Short-term**: Reference (what was decided)
- **Long-term**: Learning (understand patterns), Audit (compliance), Maintenance (why this way)

**Compression Strategy**:
1. Identify current AND future purposes
2. Preserve union of essential information
3. May need multiple representations (full for learning, compressed for execution)

---

## Part 2: Information Types and Preservation Requirements

### Core Information Elements

#### Decision Information

**Minimum (Execution)**:
- What was decided
- When to apply it

**Standard (Reference)**:
- What, when, who
- Brief rationale

**Comprehensive (Learning/Audit/Maintenance)**:
- Problem/context
- Alternatives considered
- Evaluation criteria
- Trade-offs analyzed
- Decision made (what)
- Decision maker (who)
- Timestamp (when)
- Rationale (why this option)
- Constraints that influenced choice
- Risks and mitigations
- Expected outcomes
- Review/revision criteria

**Compression by Purpose**:
```
Execution:      5-10% of comprehensive
Reference:      20-30% of comprehensive
Learning:       80-100% of comprehensive
Audit:          100% (cannot compress)
Maintenance:    60-80% of comprehensive
```

---

#### Procedure/Process Information

**Minimum (Execution)**:
- Steps in order
- Prerequisites
- Success criteria

**Standard (Reference)**:
- Steps, prerequisites, success criteria
- Common variations
- Error handling

**Comprehensive (Learning/Maintenance)**:
- Problem being solved
- Design rationale (why these steps)
- Steps with explanations
- Variations and when to use
- Edge cases and handling
- Common mistakes
- Optimization opportunities
- Evolution history

---

#### Architectural/Design Information

**Minimum (Execution)**:
- Component structure
- Interfaces
- Key constraints

**Standard (Reference)**:
- Structure, interfaces, constraints
- Component responsibilities
- Key patterns used

**Comprehensive (Learning/Maintenance)**:
- Problem domain context
- Design principles applied
- Architecture patterns and why
- Alternative architectures considered
- Trade-offs and decisions
- Component structure and responsibilities
- Key constraints and assumptions
- Known limitations
- Evolution path

---

#### Specification Information

**Minimum (Execution)**:
- Requirements (what must be done)
- Acceptance criteria
- Constraints

**Standard (Reference)**:
- Requirements with brief context
- Acceptance criteria
- Constraints and dependencies
- Examples

**Comprehensive (Learning/Communication)**:
- Problem/opportunity
- User/business context
- Requirements with full rationale
- Acceptance criteria with test scenarios
- Constraints and why they exist
- Dependencies and risks
- Examples and use cases
- Non-functional requirements

---

## Part 3: Systematic Analysis Method

### Step 1: Purpose Identification

**Questions to Ask**:
1. **Who will use this document?**
   - LLM only, technical humans, non-technical humans, mixed

2. **When will they use it?**
   - Session startup, during work, after completion, years later

3. **What will they do with it?**
   - Execute tasks, learn concepts, look up facts, prove compliance, understand decisions

4. **How often will they access it?**
   - Every session, occasionally, rarely, never (archival)

5. **What questions must this answer?**
   - List specific questions the document must support

6. **What happens if information is missing?**
   - Task fails, learning incomplete, compliance violated, decisions can't be understood

**Output**: List of all purposes (current and future) with priority

---

### Step 2: Essential Information Mapping

For each identified purpose, map to information requirements:

**Template**:
```yaml
document: [name]
purposes:
  - purpose: [execution|learning|reference|audit|communication|analysis|maintenance]
    priority: [critical|high|moderate|low]
    essential_information:
      - what: [specific information element]
        why_essential: [reason it's required]
        safe_to_compress: [yes|no|partial]
    
questions_must_answer:
  - "[specific question]"
  
failure_modes:
  - if_missing: "[information type]"
    consequence: "[what breaks]"
```

**Example - Decision Document**:
```yaml
document: Authentication Strategy Decision
purposes:
  - purpose: execution
    priority: high
    essential_information:
      - what: "Use JWT with refresh tokens"
        why_essential: "Team needs to know what to implement"
        safe_to_compress: no
      
  - purpose: maintenance  
    priority: high
    essential_information:
      - what: "Rejected session-based auth due to scaling concerns"
        why_essential: "Future maintainers need to know why not to revert"
        safe_to_compress: partial (keep outcome, compress discussion)
      
  - purpose: audit
    priority: moderate
    essential_information:
      - what: "Security team approved on 2025-10-15"
        why_essential: "Compliance requirement"
        safe_to_compress: no

questions_must_answer:
  - "What authentication approach should we implement?"
  - "Why didn't we use sessions?"
  - "Who approved this for security?"

failure_modes:
  - if_missing: "rationale for rejection of sessions"
    consequence: "Team may waste time reconsidering"
  - if_missing: "security approval"
    consequence: "Compliance violation"
```

---

### Step 3: Information Preservation Decision Matrix

Create matrix of information elements × purposes:

| Information Element | Execution | Learning | Reference | Audit | Maintenance | Keep? |
|---------------------|-----------|----------|-----------|-------|-------------|-------|
| Decision outcome | ✅ Critical | ✅ Important | ✅ Critical | ✅ Required | ✅ Important | **YES** |
| Alternatives considered | ❌ Not needed | ✅ Critical | ⚠️ Optional | ✅ Required | ✅ Critical | **YES** |
| Discussion verbatim | ❌ Not needed | ⚠️ Helpful | ❌ Not needed | ⚠️ Maybe | ❌ Not needed | **COMPRESS** |
| Who decided | ⚠️ Optional | ⚠️ Helpful | ⚠️ Optional | ✅ Required | ⚠️ Helpful | **YES** |
| When decided | ⚠️ Optional | ❌ Not needed | ⚠️ Optional | ✅ Required | ⚠️ Helpful | **YES** |
| Implementation details | ✅ Critical | ⚠️ Helpful | ✅ Critical | ❌ Not needed | ⚠️ Optional | **YES** |

**Decision Rules**:
- If **any purpose** marks ✅ Critical/Required → **MUST preserve verbatim**
- If **all purposes** mark ✅/⚠️ Important/Helpful → **preserve but can compress format**
- If **majority** mark ⚠️ Optional → **preserve in summary form**
- If **all purposes** mark ❌ Not needed → **safe to strip completely**

---

### Step 4: Format Selection

Based on primary purpose and preservation requirements:

**Decision Tree**:

```
Primary Purpose?
├─ Execution
│  ├─ Structured data? → YAML/JSON
│  ├─ Procedures? → Numbered steps (markdown)
│  └─ Specifications? → Structured tables
│
├─ Learning
│  └─ Prose with examples (markdown with code blocks)
│
├─ Reference
│  ├─ API? → OpenAPI/Swagger
│  ├─ Config options? → YAML with comments
│  └─ Data? → Structured tables
│
├─ Audit
│  └─ Structured records with metadata (JSON/YAML with timestamps)
│
├─ Communication
│  ├─ Technical audience? → Structured technical
│  └─ General audience? → Prose
│
└─ Maintenance
   └─ ADR format (markdown with structured sections)
```

---

## Part 4: Compression Methods by Information Type

### Method 1: Structural Compression (Preserve Facts, Remove Prose)

**When**: Information is factual and can be represented structurally

**Technique**: Convert prose to structured format

**Example**:
```markdown
BEFORE (124 tokens):
"The authentication system uses JSON Web Tokens (JWT) for stateless 
authentication. We chose JWT over session-based authentication because 
it scales better horizontally without requiring session storage. Access 
tokens expire after 15 minutes for security, and refresh tokens allow 
users to stay logged in for up to 7 days without re-entering credentials."

AFTER (28 tokens, 77% reduction):
```yaml
auth:
  type: JWT
  rationale: horizontal_scaling
  access_ttl: 15m
  refresh_ttl: 7d
```
```

**Information Preserved**: All facts
**Information Lost**: Explanatory prose (can be regenerated if needed)
**Best For**: Execution, Reference purposes

---

### Method 2: Summary Compression (Extract Key Points)

**When**: Learning/context content that can be summarized

**Technique**: Identify and extract key insights, discard verbose explanation

**Example**:
```markdown
BEFORE (250 tokens of discussion):
[Long discussion about various authentication approaches, pros/cons, team concerns, etc.]

AFTER (45 tokens, 82% reduction):
**Key Insights**:
- JWT chosen for horizontal scaling
- Rejected sessions: scaling complexity
- Rejected OAuth: overkill for internal app
- 15m expiry balances security/UX
```

**Information Preserved**: Key decisions and insights
**Information Lost**: Discussion details (preserved elsewhere if needed for audit)
**Best For**: Learning, Communication (post-decision)

---

### Method 3: Reference Compression (ID-Based)

**When**: Repeated references to same entities

**Technique**: Assign IDs, reference by ID instead of repeating

**Example**:
```markdown
BEFORE (180 tokens):
"The async-first architecture principle requires that all long-running 
operations use async patterns. This principle is mandatory because..."
[Later] "According to the async-first architecture principle..."
[Later] "The async-first architecture principle also applies to..."

AFTER (65 tokens, 64% reduction):
```json
{"id":"P1","name":"async_first","status":"mandatory","rule":"long_ops_use_async"}
```
[Later] "Per P1..."
[Later] "P1 also applies to..."
```

**Information Preserved**: Full specification (first mention), references
**Information Lost**: Repeated verbose descriptions
**Best For**: LLM-only documents with frequent references

---

### Method 4: Layered Compression (Multiple Representations)

**When**: Document serves multiple purposes with different information needs

**Technique**: Create multiple versions optimized for different purposes

**Example**:
```
decision-auth-strategy.full.md      (1200 tokens - Learning/Audit)
├─ Full context and discussion
├─ All alternatives considered
├─ Complete rationale
└─ Audit trail

decision-auth-strategy.summary.md   (300 tokens - Communication)
├─ Decision and key rationale
├─ Major alternatives
└─ Next steps

decision-auth-strategy.exec.yaml    (80 tokens - Execution)
├─ Decision outcome only
├─ Implementation requirements
└─ Constraints
```

**Information Preserved**: Everything (in appropriate version)
**Best For**: High-value decisions serving multiple purposes long-term

---

### Method 5: Temporal Compression (Compress After Use)

**When**: Document purpose changes over time

**Technique**: Keep full version during active use, compress after purpose completed

**Example**:
```
During project (Learning/Communication):
- Keep full proposal with rationale, examples, persuasive elements

After approval (Execution):
- Compress to requirements and specifications
- Archive full version

After completion (Reference/Audit):
- Further compress to decision record
- Keep full version archived

After archival period (Historical):
- Extreme compression to key outcomes
- Full version in cold storage
```

**Lifecycle**:
1. Active: Full version (all purposes)
2. Current: Compressed for primary purpose (execution/reference)
3. Recent: Decision record format (maintenance/learning)
4. Archived: Minimal summary (searchability)
5. Historical: Conversational compression (storage efficiency)

---

## Part 5: Validation Framework

### Preservation Validation Checklist

For each compression, verify:

**Purpose Coverage**:
- [ ] All identified purposes can still be served
- [ ] All critical questions can still be answered
- [ ] No failure modes introduced

**Information Integrity**:
- [ ] All facts preserved accurately
- [ ] Relationships intact
- [ ] No ambiguity introduced
- [ ] Traceability maintained

**Audience Validation**:
- [ ] LLM can parse and use (if applicable)
- [ ] Technical humans can understand (if applicable)
- [ ] Non-technical humans can understand (if applicable)

**Purpose-Specific Validation**:
- [ ] **Execution**: Can task be completed correctly?
- [ ] **Learning**: Can concepts be understood?
- [ ] **Reference**: Can facts be found quickly?
- [ ] **Audit**: Is compliance trail intact?
- [ ] **Maintenance**: Can future changes be made safely?

---

### Testing Method

**Step 1: Question-Based Testing**

List critical questions document must answer, then test compressed version:

```yaml
test_case:
  question: "Why didn't we use session-based authentication?"
  compressed_doc_answer: "[extract from compressed version]"
  original_doc_answer: "[extract from original]"
  information_preserved: [yes|partial|no]
  acceptable: [yes|no]
```

**Step 2: Task Simulation**

For execution purposes, attempt to complete task using only compressed version:

```
Task: Implement authentication system
Using: Compressed specification only
Result: [success|partial|failure]
Missing information: [list anything needed but not present]
```

**Step 3: Audience Review**

Have representative from each audience review:

- Technical reviewer: Can you implement from this?
- Non-technical reviewer: Can you understand the decision?
- LLM test: Can LLM extract correct information?

---

## Part 6: Decision Framework Summary

### Systematic Process

**For any document to compress**:

1. **Identify purposes** (current and future)
   - Use taxonomy (execution, learning, reference, audit, communication, analysis, maintenance)
   - Prioritize each purpose
   
2. **Map essential information** for each purpose
   - Use information type templates
   - Create preservation matrix
   
3. **Determine preservation requirements**
   - Union of all essential information
   - Apply decision rules (any critical → must keep)
   
4. **Select compression method**
   - Structural (facts → structure)
   - Summary (extract key insights)
   - Reference (use IDs)
   - Layered (multiple versions)
   - Temporal (compress over time)
   
5. **Choose optimal format**
   - Based on primary purpose and audience
   - Text vs structure decision tree
   
6. **Validate preservation**
   - Question-based testing
   - Task simulation
   - Audience review

7. **Document compression decisions**
   - What was stripped and why
   - What purposes are still served
   - When to revisit (if temporal)

---

## Part 7: Best Practices and Patterns

### Best Practice 1: Purpose-First Design

**Before compressing, ask**:
- "What are ALL the purposes this serves?"
- "What will break if I remove X?"
- "Will future needs be met?"

### Best Practice 2: Preservation Over Compression

**When in doubt**:
- Preserve rather than strip
- Can always compress more later
- Cannot recover lost information

### Best Practice 3: Separate Concerns

**Don't try to optimize for everything**:
- Create purpose-specific versions
- LLM-optimized ≠ human-optimized
- Execution ≠ learning

### Best Practice 4: Metadata Richness

**Always preserve**:
- Who, what, when, why
- Purpose and audience
- Relationships and dependencies
- Compression decisions made

### Best Practice 5: Temporal Awareness

**Recognize lifecycle**:
- Different stages need different formats
- Active documents need more detail
- Completed work can be more compressed
- Archive deeply but keep searchable

---

## Part 8: Common Patterns

### Pattern 1: Decision Compression

**Full Version** (Learning/Audit):
- Problem context
- Options evaluated (all)
- Evaluation criteria
- Analysis of each option
- Discussion points
- Decision made
- Rationale
- Risks and mitigations

**Reference Version**:
- Decision
- Key rationale (2-3 sentences)
- Date and decision maker

**Execution Version**:
- Decision only
- Implementation requirements

### Pattern 2: Specification Compression

**Full Version** (Communication):
- User stories with context
- Requirements with rationale
- Examples and scenarios
- Non-functional requirements
- Acceptance criteria
- Design constraints

**Technical Version** (Hybrid-Technical):
- Requirements (structured)
- Acceptance criteria
- Constraints
- Key examples

**Execution Version** (LLM):
- Requirements only (YAML)
- Acceptance criteria (structured)

### Pattern 3: Architecture Compression

**Full Version** (Learning/Maintenance):
- Problem domain
- Architecture patterns
- Design rationale
- Component responsibilities
- Alternatives considered
- Trade-offs
- Known limitations

**Reference Version**:
- Component structure
- Key interfaces
- Design patterns used
- Critical constraints

**Execution Version**:
- Component structure
- Interfaces
- Configuration

---

## Conclusion

**Key Insights**:

1. **Purpose determines preservation**: What to keep depends entirely on why the document exists

2. **Multiple purposes require union**: Preserve enough for ALL purposes, not just primary

3. **Format follows purpose**: Structured for execution, prose for learning, metadata-rich for audit

4. **Compression is contextual**: Same content needs different compression for different purposes

5. **Validation is essential**: Test preservation against all identified purposes

6. **Temporal awareness matters**: Purpose changes over document lifecycle

**Systematic Method**:
Purpose Identification → Essential Information Mapping → Preservation Matrix → Method Selection → Format Selection → Validation

**Safety Principle**:
When uncertain, err on side of preservation. Information loss is permanent; over-preservation can be corrected later.

---

## Next Steps

1. Apply framework to sample documents
2. Create compression decision templates
3. Build validation test suites
4. Develop purpose-specific format templates
5. Create automated analysis tools

---

**End of Document**