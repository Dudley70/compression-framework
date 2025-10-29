# Documentation Types and Context Requirements Analysis

**Created**: 2025-10-29 21:40 AEDT
**Purpose**: Establish taxonomy of documentation types, audiences, and context preservation requirements to inform compression strategy selection
**Status**: Initial framework - to be refined

---

## Executive Summary

Compression strategy cannot be one-size-fits-all. Different document types serve different audiences (LLM-only, human-only, hybrid) with different context preservation needs. This analysis creates a matrix to guide optimal format selection.

**Core Insight**: "Token efficiency" is not a single axis - it must balance against readability requirements, comprehension needs, and usage patterns.

---

## Document Type Taxonomy

### Primary Dimensions

1. **Audience**
   - LLM-only (never read by humans)
   - Human-only (never loaded to LLM context)
   - Hybrid (both humans and LLMs interact)

2. **Purpose**
   - Strategic context (decisions, principles, architecture)
   - Operational state (current status, blockers, next actions)
   - Reference material (specs, APIs, data)
   - Communication (reports, proposals, briefings)
   - Archival (historical records)

3. **Access Pattern**
   - Session startup (loaded every session)
   - On-demand retrieval (loaded when needed)
   - One-time read (archival)
   - Continuous reference (during work)

4. **Information Density Requirement**
   - Maximum compression (every token counts)
   - Moderate compression (balance efficiency/readability)
   - Verbose acceptable (clarity paramount)

---

## Document Type Matrix

### 1. LLM-Only Documents

**Characteristics**:
- Never read by humans in raw form
- Loaded into context windows
- Token efficiency critical
- Machine-parseable structure essential

**Examples**:
- PROJECT.lsc (strategic context in LSC format)
- SESSION.lsc (operational state)
- HANDOVER.lsc (cross-session continuity)
- Memory blocks (retrieval-augmented systems)
- Decision logs (machine-queryable)
- Principle registries (ID-based references)

**Context Preservation Requirements**:
- ✅ All factual content (decisions, principles, state)
- ✅ Relationships and dependencies
- ✅ Temporal ordering (when things happened)
- ❌ Explanatory prose (generate on demand)
- ❌ Narrative flow (not needed for machines)
- ❌ Examples (unless essential for specification)

**Optimal Format**: LSC or similar machine-first structured format
- JSON/YAML with short stable keys
- ID-driven references (P1, D4, not repeated descriptions)
- Triple-based facts for relationships
- Flat structure to minimize nested key repetition

**Compression Target**: 70-85% reduction vs human-readable

---

### 2. Human-Only Documents

**Characteristics**:
- Never loaded into LLM context
- Read and interpreted by humans
- Clarity and comprehension paramount
- Narrative flow important
- Token count irrelevant

**Examples**:
- Board papers and executive briefings
- Detailed research reports (for humans)
- Client-facing proposals
- User documentation and guides
- Project retrospectives (team reading)
- Strategic plans (stakeholder communication)

**Context Preservation Requirements**:
- ✅ Complete explanations and rationale
- ✅ Examples and analogies
- ✅ Narrative flow and structure
- ✅ Context for non-technical audiences
- ✅ Visual formatting (headers, emphasis, lists)
- ✅ Persuasive or educational elements

**Optimal Format**: Traditional markdown/prose
- Full sentences and paragraphs
- Logical section flow
- Visual hierarchy (headers, emphasis)
- Examples and case studies
- Accessible language for target audience

**Compression Target**: None - optimize for human comprehension

---

### 3. Hybrid Documents (Critical Category)

**Characteristics**:
- Read by both humans AND loaded to context
- Must balance token efficiency with human comprehension
- Need to remain understandable without being verbose
- Often instruction-based or specification documents

**Examples**:
- System instructions (project rules, behaviors)
- API specifications (humans design, LLMs consume)
- Workflow procedures (humans author, LLMs execute)
- Coding standards (humans define, LLMs follow)
- Test specifications (humans write, LLMs implement)

**Context Preservation Requirements**:
- ✅ Complete specifications (no ambiguity)
- ✅ Concise but clear language
- ✅ Structured format (parseable)
- ✅ Human-scannable (can quickly find sections)
- ⚖️ Balance: explanations vs brevity
- ❌ Verbose explanations (unless critical for understanding)

**Optimal Format**: Structured concise prose
- Clear section headers
- Bullet points for lists (not paragraphs)
- Consistent terminology
- Minimal duplication
- Short sentences (but complete thoughts)
- Examples only when necessary for clarity

**Compression Target**: 30-50% reduction vs verbose prose
- Not as aggressive as LLM-only
- Not as verbose as human-only
- Focus: information density without sacrificing comprehension

---

## Access Pattern Analysis

### Session Startup Documents

**Pattern**: Loaded every session, sometimes multiple times per day

**Examples**:
- PROJECT.md / PROJECT.lsc
- SESSION.md / SESSION.lsc
- HANDOVER.md / HANDOVER.lsc

**Token Impact**: High (cumulative cost across many sessions)

**Compression Priority**: Critical
- Even small reductions compound over time
- 50 sessions × 2,000 tokens = 100,000 token savings per 1,000 token reduction

**Recommended Approach**:
- Convert to LSC format (70-85% reduction)
- Use retrieval-augmented when available (load only relevant slices)
- Keep only essential context

---

### On-Demand Retrieval Documents

**Pattern**: Loaded only when specifically needed

**Examples**:
- API reference documentation
- Technical specifications
- Decision archives
- Research findings

**Token Impact**: Moderate (loaded occasionally)

**Compression Priority**: Moderate
- Balance: findability vs token cost
- Must be easy to identify what to retrieve
- Content can be more detailed since not loaded constantly

**Recommended Approach**:
- Good indexing and metadata (find the right document)
- Moderate compression within documents
- Consider progressive disclosure (summaries → details)

---

### Archival Documents

**Pattern**: Rarely or never loaded to context

**Examples**:
- Completed session logs
- Historical decision rationale
- Old project versions
- Deprecated specifications

**Token Impact**: Minimal (rarely accessed)

**Compression Priority**: Storage efficiency only
- Token count irrelevant (not loaded to context)
- Focus on storage cost and searchability

**Recommended Approach**:
- Conversational compression (99.5% reduction for verbose logs)
- Structured summaries (decisions, outcomes, artifacts)
- Compressed but searchable (can find when needed)

---

## Comprehensive Mapping Matrix

| Document Type | Audience | Access Pattern | Compression Priority | Optimal Format | Target Reduction |
|--------------|----------|----------------|---------------------|----------------|------------------|
| **Strategic Context** (PROJECT.md) | LLM-only (or hybrid) | Session startup | Critical | LSC format | 70-85% |
| **Session State** (SESSION.md) | LLM-only | Session startup | Critical | LSC format | 70-85% |
| **Handover Protocol** (HANDOVER.md) | LLM-only | Session startup | Critical | LSC format | 70-85% |
| **System Instructions** | Hybrid | Session startup | High | Structured concise | 30-50% |
| **Decision Log** | LLM-primary | On-demand | Moderate | LSC or structured | 50-70% |
| **API Reference** | Hybrid | On-demand | Moderate | Structured concise | 30-50% |
| **Technical Specs** | Hybrid | On-demand | Moderate | Structured concise | 30-50% |
| **Board Papers** | Human-only | Never loaded | None | Traditional prose | 0% (optimize clarity) |
| **Client Proposals** | Human-only | Never loaded | None | Traditional prose | 0% (optimize persuasion) |
| **User Documentation** | Human-only | Never loaded | None | Traditional prose | 0% (optimize comprehension) |
| **Session Logs** | Archival | Rarely | Low | Conversational compression | 95-99% |
| **Research Notes** | Hybrid/Archival | Varies | Moderate | Structured summaries | 40-60% |
| **Code Comments** | Human-primary | Never loaded | None | Concise prose | Minimal |
| **Test Cases** | Hybrid | On-demand | Moderate | Structured format | 30-50% |
| **Workflow Procedures** | Hybrid | Session startup | High | Structured concise | 40-60% |

---

## Context Preservation Framework

### Essential Elements (Always Preserve)

Regardless of compression level, these must be preserved:

1. **Factual Accuracy**
   - Decisions made
   - Principles established
   - Technical specifications
   - State information

2. **Relationships**
   - Dependencies between components
   - Decision rationale chains
   - Temporal ordering

3. **Actionable Information**
   - What needs to be done
   - Constraints and requirements
   - Success criteria

4. **Recoverability**
   - Enough context to reconstruct understanding
   - Ability to trace decisions back to reasoning

### Compression-Safe Elements (Can Reduce/Remove)

Elements that can be compressed without losing essential information:

1. **Explanatory Prose**
   - Long explanations (→ concise statements)
   - Repeated context (→ references)
   - Scaffolding language ("As we discussed", "It's important to note")

2. **Examples** (when non-critical)
   - Illustrative examples (keep only essential ones)
   - Analogies (unless core to understanding)
   - Edge cases (document separately if needed)

3. **Formatting**
   - Visual formatting (bold, emphasis)
   - Whitespace (condense while maintaining structure)
   - Narrative transitions (compress to structured sections)

4. **Redundancy**
   - Information stated multiple times
   - Context repeated across documents
   - Verbose descriptions when IDs suffice

---

## Compression Strategy Selection Guide

### Decision Tree

**Step 1: Who is the primary audience?**
- LLM-only → Maximum compression (LSC, 70-85%)
- Human-only → No compression (optimize clarity)
- Both → Moderate compression (structured concise, 30-50%)

**Step 2: What is the access pattern?**
- Session startup → Critical compression (every token counts)
- On-demand → Moderate compression (balance findability/cost)
- Archival → Storage-focused compression (searchability matters)

**Step 3: What is the information type?**
- Strategic/principles → LSC format (ID-driven, structured)
- Specifications → Structured concise (clear but not verbose)
- Conversational logs → Conversational compression (summarize outcomes)
- Instructions → Structured concise (unambiguous but efficient)

**Step 4: What are the comprehension requirements?**
- Machine-only parsing → Maximum structure (JSON/YAML)
- Expert human reading → Technical concise (domain-specific terms okay)
- General audience → Detailed explanations (clarity paramount)

---

## Practical Recommendations

### For New Projects

1. **Start with audience identification**
   - Map each document type to primary audience
   - Identify which documents load to context vs human-only

2. **Apply appropriate format from the start**
   - LLM-only docs: Use LSC format initially
   - Hybrid docs: Use structured concise format
   - Human-only: Traditional prose

3. **Separate concerns**
   - Don't mix LLM context docs with human communication
   - Generate human-readable views from machine docs when needed
   - Keep source of truth in optimal format for primary use

### For Existing Projects

1. **Audit current documentation**
   - Identify which documents load to context regularly
   - Measure current token consumption
   - Calculate compression opportunity

2. **Prioritize conversion by impact**
   - High-frequency + high-token = highest priority
   - Convert session startup docs first
   - Archive verbose historical content with compression

3. **Migrate incrementally**
   - Start with one document type
   - Validate information preservation
   - Measure actual reduction achieved
   - Expand to other document types

### Hybrid Document Guidelines

**Key Principle**: Optimize for scannability + parseability

**Structure**:
```markdown
# Clear Section Headers

## Purpose (2-3 sentences)
Brief explanation of what this does and why it matters.

## Specification
- Requirement: Clear statement
- Constraint: Explicit limitation  
- Success criteria: Measurable outcome

## Examples (optional)
Only include if essential for understanding.
```

**Language**:
- Use domain-specific terms (audience knows them)
- Complete sentences (but short)
- Active voice
- Avoid redundant phrases ("in order to" → "to")
- Remove scaffolding language

**Lists vs Prose**:
- Lists: For specifications, requirements, procedures
- Prose: For explanations, rationale, context
- Never: Long paragraphs in list format

---

## Common Anti-Patterns

### ❌ Anti-Pattern 1: One-Size-Fits-All Compression
**Problem**: Applying same compression level to all documents
**Impact**: Over-compressed human docs become unreadable, under-compressed LLM docs waste tokens
**Solution**: Use the matrix - match compression to audience and access pattern

### ❌ Anti-Pattern 2: Premature Optimization
**Problem**: Compressing documents that are rarely loaded
**Impact**: Wasted effort, potential information loss
**Solution**: Focus on session startup docs first (highest cumulative impact)

### ❌ Anti-Pattern 3: Destroying Comprehension for Tokens
**Problem**: Compressing hybrid docs to point where humans can't understand them
**Impact**: Maintenance becomes impossible, errors introduced
**Solution**: Hybrid docs need balance - 30-50% reduction maintains comprehension

### ❌ Anti-Pattern 4: Mixing Audiences in Single Document
**Problem**: Creating docs that try to serve both LLMs and humans equally
**Impact**: Compromises both use cases, neither audience well-served
**Solution**: Separate documents, or generate human views from machine source

### ❌ Anti-Pattern 5: Compressing Without Measurement
**Problem**: Assuming compression worked without measuring
**Impact**: May not achieve expected benefits, may lose essential information
**Solution**: Measure token counts before/after, validate information preservation

---

## Measurement Criteria

### Token Efficiency Metrics

**Baseline Measurement**:
- Count tokens in original document (use LLM tokenizer)
- Identify information density (facts per 100 tokens)
- Calculate overhead (scaffolding language percentage)

**Post-Compression Measurement**:
- Count tokens in compressed document
- Calculate reduction percentage
- Verify information density maintained or improved

**Target Ranges**:
- LLM-only: 70-85% reduction
- Hybrid: 30-50% reduction
- Archival: 95-99% reduction (conversational logs)

### Information Preservation Validation

**Checklist**:
- [ ] All factual statements preserved
- [ ] Relationships/dependencies intact
- [ ] Temporal ordering maintained
- [ ] Actionable information complete
- [ ] Can reconstruct understanding from compressed version

**Testing Method**:
1. Load compressed version to LLM
2. Ask LLM to answer key questions about the content
3. Compare answers to original version
4. Verify no critical information lost

---

## Next Steps

### Research Phase
1. **Create test corpus**
   - Select representative documents from each category
   - Measure baseline token counts
   - Document information requirements

2. **Apply compression techniques**
   - LSC for LLM-only docs
   - Structured concise for hybrid docs
   - Conversational compression for archives

3. **Measure and compare**
   - Token reduction achieved
   - Information preservation validated
   - Comprehension testing (for hybrid docs)

### Implementation Phase
1. **Develop format templates**
   - LSC schema for strategic docs
   - Structured concise templates for hybrid docs
   - Compression scripts for conversational logs

2. **Create migration guides**
   - Step-by-step conversion procedures
   - Validation checklists
   - Rollback procedures

3. **Build tooling**
   - Token counters
   - Format validators
   - Compression utilities

---

## Conclusion

**Core Insight**: Compression is not about "making everything smaller" - it's about **optimizing each document for its specific audience and access pattern**.

**Key Takeaways**:
1. **Know your audience**: LLM-only, human-only, or hybrid determines strategy
2. **Measure access patterns**: Session startup docs have highest compression ROI
3. **Preserve information fidelity**: Compression must not lose essential context
4. **Balance trade-offs**: Hybrid docs need human comprehension AND token efficiency
5. **Validate results**: Measure token reduction AND information preservation

**Success Criteria**:
- ✅ LLM-only docs achieve 70-85% reduction with zero information loss
- ✅ Hybrid docs achieve 30-50% reduction while maintaining human comprehension
- ✅ Archival conversational logs achieve 95-99% reduction with key outcomes preserved
- ✅ Human-only docs remain optimized for clarity, not token count

**Next Document**: Create test corpus with representative examples from each category to validate compression techniques against this framework.

---

## References

- LSC Framework: docs/research/lsc/LSC_CONTEXT_EFFICIENCY.md
- Context Compression Method: docs/research/context-compression-method.md
- PROJECT.md: Strategic context and principles

---

## Appendix: Example Transformations

### Example 1: Strategic Context (LLM-Only)

**Before (Human-Readable)**: 156 tokens
```markdown
The async-first architecture principle is mandatory because tasks run 
for 10-60 minutes and blocking tool calls would provide zero progress 
visibility, risk timeouts, and prevent user interaction during execution. 
This principle ensures users can see progress updates, cancel long-running 
tasks, and interact with the system while background work continues.
```

**After (LSC Format)**: 12 tokens (92% reduction)
```json
{"id":"P1","rule":"async_first","why":"10-60min_blocking=fail","status":"mandatory"}
```

**Information Preserved**: ✅ All facts, ❌ explanatory prose (can be regenerated)

---

### Example 2: System Instructions (Hybrid)

**Before (Verbose)**: 89 tokens
```markdown
When you encounter a file operation request from the user, you should 
first verify that the file or directory exists by using the appropriate 
tool to check its existence. This is important because attempting operations 
on non-existent paths will result in errors and waste time.
```

**After (Structured Concise)**: 28 tokens (69% reduction)
```markdown
**File Operations**: Verify path exists (list/get_file_info) before operations. 
Prevents errors on non-existent paths.
```

**Information Preserved**: ✅ Complete specification, ✅ Human-readable, ❌ Verbose explanation

---

### Example 3: Conversational Log (Archival)

**Before (Full Conversation)**: ~8,500 tokens
```markdown
[Verbose back-and-forth about implementing authentication, including
exploration of options, discussion of trade-offs, multiple code iterations,
explanations, examples, and final implementation]
```

**After (Compressed Summary)**: 42 tokens (99.5% reduction)
```json
{
  "query": "implement_auth",
  "decision": "JWT_with_refresh",
  "artifacts": ["auth.ts", "middleware.ts"],
  "outcome": "working_implementation"
}
```

**Information Preserved**: ✅ Decision, ✅ Artifacts, ✅ Outcome, ❌ Verbose discussion (not needed for future reference)

---

**End of Document**