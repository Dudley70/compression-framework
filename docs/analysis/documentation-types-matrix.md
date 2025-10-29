# Documentation Types and Context Requirements Analysis

**Created**: 2025-10-29 21:40 AEDT
**Updated**: 2025-10-29 22:15 AEDT (Added technical vs non-technical hybrid distinction)
**Purpose**: Establish taxonomy of documentation types, audiences, and context preservation requirements to inform compression strategy selection
**Status**: Refined framework v1.1

---

## Executive Summary

Compression strategy cannot be one-size-fits-all. Different document types serve different audiences with different context preservation needs. This analysis creates a matrix to guide optimal format selection.

**Core Insight**: "Token efficiency" is not a single axis - it must balance against readability requirements, comprehension needs, and usage patterns.

**Critical Refinement**: "Hybrid" documents split into two distinct categories based on human technical literacy:
- **Hybrid-Technical**: Technical humans + LLMs (can read structured/code-like formats)
- **Hybrid-General**: Non-technical humans + LLMs (need prose and explanations)

---

## Document Type Taxonomy

### Primary Dimensions

1. **Audience** (Refined)
   - **LLM-only**: Never read by humans
   - **Hybrid-Technical**: LLMs + technical humans (developers, engineers, architects)
   - **Hybrid-General**: LLMs + non-technical humans (stakeholders, managers, clients)
   - **Human-Technical-only**: Technical humans only (never loaded to LLM)
   - **Human-General-only**: Non-technical humans only (never loaded to LLM)

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
   - High compression (structured but parseable)
   - Moderate compression (balance efficiency/readability)
   - Low compression (technical clarity)
   - Verbose acceptable (general audience clarity paramount)

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

### 2. Hybrid-Technical Documents

**Characteristics**:
- Read by technical humans (developers, engineers, architects) AND loaded to LLM context
- Audience understands code, structured formats, technical terminology
- Can read JSON-like structures and concise technical language
- Token efficiency important but must remain technically clear
- Often specification or instruction documents

**Examples**:
- System architecture diagrams (with structured metadata)
- API specifications (OpenAPI/Swagger style)
- Technical coding standards
- Infrastructure as Code configurations
- Database schema definitions
- CI/CD pipeline configurations
- Technical workflow procedures
- Test specifications (structured format)
- Technical decision records (ADRs)

**Context Preservation Requirements**:
- ✅ Complete technical specifications (no ambiguity)
- ✅ Structured format (parseable by both LLMs and developers)
- ✅ Domain-specific terminology (audience knows it)
- ✅ Code examples (when necessary for clarity)
- ⚖️ Balance: precision vs brevity
- ❌ Redundant explanations (technical audience infers)
- ❌ Non-technical analogies (not needed)

**Optimal Format**: Structured technical format
- YAML/JSON for configurations
- Markdown with code blocks
- Structured tables for specifications
- Short technical sentences
- Domain terminology without explanation
- Minimal prose, maximum structure

**Compression Target**: 40-60% reduction vs verbose prose
- More aggressive than general hybrid
- Technical humans can parse dense information
- Structure over explanation

**Example**:
```yaml
# Technical hybrid - developers can read this easily
auth:
  strategy: JWT
  refresh: true
  expiry: 15m
  rotation: 7d
  mfa: optional
```

---

### 3. Hybrid-General Documents

**Characteristics**:
- Read by non-technical humans (stakeholders, managers, clients) AND loaded to LLM context
- Audience needs explanations and context
- Cannot assume technical knowledge
- Must balance token efficiency with comprehension
- Often requirement or planning documents

**Examples**:
- Product requirements documents (PRDs)
- Project plans (for mixed audiences)
- User stories and acceptance criteria
- Business logic specifications
- Process documentation (for non-technical users)
- Training materials (technical topics for general audience)
- Onboarding documentation
- Feature specifications (business perspective)
- Testing scenarios (business cases)

**Context Preservation Requirements**:
- ✅ Complete specifications (no ambiguity)
- ✅ Explanations for non-obvious points
- ✅ Context for decisions
- ✅ Examples when helpful for understanding
- ✅ Structured but readable format
- ⚖️ Balance: accessibility vs token efficiency
- ❌ Technical jargon without explanation
- ❌ Excessive verbosity (but can't be too terse)

**Optimal Format**: Structured accessible prose
- Clear section headers
- Short paragraphs (3-5 sentences max)
- Bullet points for lists
- Plain language (avoid jargon or explain it)
- Examples for clarity
- Structured but readable

**Compression Target**: 20-40% reduction vs verbose prose
- Less aggressive than technical hybrid
- Must maintain comprehension for non-technical readers
- Cannot sacrifice clarity for tokens

**Example**:
```markdown
## Authentication Strategy

**Approach**: JSON Web Tokens (JWT) with refresh capability

**Why**: JWTs allow secure, stateless authentication without 
requiring server-side session storage.

**User Experience**: Users stay logged in for 15 minutes of 
activity. System automatically refreshes tokens in background.

**Security**: Optional two-factor authentication available for 
sensitive accounts.
```

---

### 4. Human-Technical-Only Documents

**Characteristics**:
- Read only by technical humans (developers, engineers)
- Never loaded into LLM context
- Code-heavy or highly technical
- Token count completely irrelevant
- Can use technical depth and examples freely

**Examples**:
- Detailed architecture deep-dives
- Code review guidelines (with extensive examples)
- Performance optimization guides
- Debugging playbooks
- Technical blog posts
- Deep-dive research papers
- Infrastructure troubleshooting guides
- Advanced technical tutorials

**Context Preservation Requirements**:
- ✅ Complete technical depth
- ✅ Extensive code examples
- ✅ Edge cases and gotchas
- ✅ Performance considerations
- ✅ Technical trade-offs explained in depth
- ✅ Links to external resources

**Optimal Format**: Rich technical prose
- Detailed explanations
- Multiple code examples
- Diagrams and visualizations
- Technical depth over brevity
- Assume expert knowledge

**Compression Target**: 0-10% (technical conciseness only)
- Optimize for technical clarity, not tokens
- Use technical shorthand naturally
- Can be dense but must be clear

---

### 5. Human-General-Only Documents

**Characteristics**:
- Read only by non-technical humans
- Never loaded into LLM context
- Narrative and explanatory
- Token count irrelevant
- Persuasive or educational intent

**Examples**:
- Board papers and executive briefings
- Client-facing proposals
- Marketing materials
- User documentation and guides
- Project retrospectives (for teams)
- Strategic plans (stakeholder communication)
- Training materials (non-technical)
- Business case documents

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
- Storytelling where appropriate

**Compression Target**: 0% - optimize for human comprehension
- Clarity is paramount
- Use whatever length needed for understanding
- Persuasion and engagement matter

---

### 6. Archival Documents

**Characteristics**:
- Rarely or never loaded to context
- Historical record
- Storage efficiency matters
- Searchability important

**Examples**:
- Completed session logs
- Historical decision rationale
- Old project versions
- Deprecated specifications

**Token Impact**: Minimal (rarely accessed)

**Compression Priority**: Storage efficiency only

**Recommended Approach**:
- Conversational compression (99.5% reduction for verbose logs)
- Structured summaries (decisions, outcomes, artifacts)
- Compressed but searchable (can find when needed)

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
- Convert to LSC format (70-85% reduction) for LLM-only versions
- Keep human-readable versions separate if needed
- Use retrieval-augmented when available (load only relevant slices)

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

## Comprehensive Mapping Matrix (Refined)

| Document Type | Audience | Access Pattern | Compression Priority | Optimal Format | Target Reduction |
|--------------|----------|----------------|---------------------|----------------|------------------|
| **Strategic Context** (PROJECT.md) | LLM-only | Session startup | Critical | LSC format | 70-85% |
| **Session State** (SESSION.md) | LLM-only | Session startup | Critical | LSC format | 70-85% |
| **Handover Protocol** (HANDOVER.md) | LLM-only | Session startup | Critical | LSC format | 70-85% |
| **System Instructions** | Hybrid-Technical | Session startup | High | Structured technical | 40-60% |
| **API Specifications** | Hybrid-Technical | On-demand | Moderate | YAML/JSON | 40-60% |
| **Technical Standards** | Hybrid-Technical | On-demand | Moderate | Structured technical | 40-60% |
| **Product Requirements** | Hybrid-General | On-demand | Moderate | Structured accessible | 20-40% |
| **User Stories** | Hybrid-General | On-demand | Moderate | Structured accessible | 20-40% |
| **Feature Specs** | Hybrid-General | On-demand | Moderate | Structured accessible | 20-40% |
| **Architecture Deep-Dives** | Human-Technical-only | Never loaded | None | Rich technical prose | 0-10% |
| **Technical Tutorials** | Human-Technical-only | Never loaded | None | Rich technical prose | 0-10% |
| **Board Papers** | Human-General-only | Never loaded | None | Traditional prose | 0% |
| **Client Proposals** | Human-General-only | Never loaded | None | Traditional prose | 0% |
| **User Documentation** | Human-General-only | Never loaded | None | Traditional prose | 0% |
| **Session Logs** | Archival | Rarely | Low | Conversational compression | 95-99% |
| **Decision Archives** | Archival | Rarely | Low | Structured summaries | 50-70% |
| **Code Comments** | Human-Technical-only | Never loaded | None | Concise technical | Minimal |
| **Test Cases** | Hybrid-Technical | On-demand | Moderate | Structured format | 40-60% |
| **Infrastructure Config** | Hybrid-Technical | On-demand | Moderate | YAML/JSON | 40-60% |

---

## Audience Comprehension Requirements

### Technical Humans (Developers, Engineers, Architects)

**Can Understand**:
- Structured formats (JSON, YAML, TOML)
- Domain-specific terminology without explanation
- Code examples as documentation
- Dense technical specifications
- Inferred relationships and context
- Technical shorthand

**Documentation Style**:
- Minimal prose, maximum structure
- Technical precision over accessibility
- Assume foundational knowledge
- Examples show edge cases and nuances
- Can handle high information density

**Compression Approach**: Aggressive (40-60% for hybrid, 0-10% for technical-only)

---

### Non-Technical Humans (Stakeholders, Managers, Clients)

**Need**:
- Plain language explanations
- Context for decisions
- Analogies and examples
- Linear narrative structure
- Visual formatting for scannability
- Explicit connections and relationships

**Documentation Style**:
- Prose-based with clear structure
- Explain technical terms when used
- Provide context before details
- Use examples for clarity
- Progressive disclosure (summary → details)
- Accessible language

**Compression Approach**: Conservative (20-40% for hybrid, 0% for general-only)

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

1. **Explanatory Prose** (Audience-Dependent)
   - LLM-only: Remove all, generate on demand
   - Hybrid-Technical: Minimize, technical audience infers
   - Hybrid-General: Reduce but keep key explanations
   - Human-only: Keep all necessary for understanding

2. **Examples** (Context-Dependent)
   - LLM-only: Remove unless essential for specification
   - Hybrid-Technical: Keep critical edge cases only
   - Hybrid-General: Keep examples that aid understanding
   - Human-only: Include freely for comprehension

3. **Formatting** (Format-Dependent)
   - LLM-only: Remove all visual formatting
   - Hybrid-Technical: Minimal structural formatting
   - Hybrid-General: Keep headers and structure
   - Human-only: Rich formatting for readability

4. **Redundancy**
   - All audiences: Remove information stated multiple times
   - Use references (IDs) instead of repetition
   - Eliminate context repeated across documents

---

## Compression Strategy Selection Guide

### Decision Tree (Refined)

**Step 1: Who is the primary audience?**
- LLM-only → Maximum compression (LSC, 70-85%)
- Technical humans + LLMs → High compression (structured technical, 40-60%)
- Non-technical humans + LLMs → Moderate compression (structured accessible, 20-40%)
- Technical humans only → Minimal compression (technical clarity, 0-10%)
- Non-technical humans only → No compression (optimize clarity, 0%)

**Step 2: What is the access pattern?**
- Session startup → Critical compression (every token counts)
- On-demand → Moderate compression (balance findability/cost)
- Archival → Storage-focused compression (searchability matters)

**Step 3: What is the information type?**
- Strategic/principles → LSC format (ID-driven, structured)
- Technical specs → Structured format (YAML/JSON for technical, tables for general)
- Conversational logs → Conversational compression (summarize outcomes)
- Instructions → Match to audience (technical: structured, general: accessible prose)

**Step 4: What are the comprehension requirements?**
- Machine-only parsing → Maximum structure (JSON/YAML)
- Technical human reading → Technical concise (domain-specific terms okay)
- General audience reading → Accessible prose (explain terms, provide context)

---

## Practical Recommendations

### For New Projects

1. **Identify document audiences early**
   - Map each document type to primary audience
   - Split hybrid into technical vs general
   - Identify which documents load to context vs human-only

2. **Apply appropriate format from the start**
   - LLM-only docs: Use LSC format initially
   - Hybrid-Technical docs: Use structured technical format (YAML, concise markdown)
   - Hybrid-General docs: Use structured accessible format (clear prose with structure)
   - Human-only: Traditional prose optimized for audience

3. **Separate concerns**
   - Don't mix LLM context docs with human communication
   - Generate human-readable views from machine docs when needed
   - Keep source of truth in optimal format for primary use
   - Create audience-specific versions when needed

### For Existing Projects

1. **Audit current documentation**
   - Identify which documents load to context regularly
   - Classify audiences (LLM/technical/general)
   - Measure current token consumption
   - Calculate compression opportunity

2. **Prioritize conversion by impact**
   - High-frequency + high-token = highest priority
   - Convert session startup docs first
   - Archive verbose historical content with compression

3. **Migrate incrementally**
   - Start with one document type
   - Validate information preservation
   - Test with both LLMs and human audiences
   - Measure actual reduction achieved
   - Expand to other document types

### Hybrid-Technical Document Guidelines

**Key Principle**: Optimize for technical scannability + machine parseability

**Structure**:
```yaml
# System Authentication Configuration

strategy: jwt  # JSON Web Tokens
refresh_enabled: true
token_ttl: 15m
refresh_ttl: 7d

security:
  mfa: optional
  rate_limit: 100/min
  token_rotation: required

# Technical audience understands implications without prose
```

**Language**:
- Use domain-specific terms freely (audience knows them)
- Structured over prose (prefer YAML/JSON where possible)
- Code-like formats acceptable
- Minimal explanation (technical context assumed)
- Short technical sentences when prose needed

**Lists vs Prose**:
- Prefer structured formats (YAML, JSON, tables)
- Use prose only for complex logic that needs explanation
- Specifications in structured formats
- Minimal narrative

---

### Hybrid-General Document Guidelines

**Key Principle**: Balance comprehension + token efficiency

**Structure**:
```markdown
# Authentication System

## Overview
Users authenticate using secure tokens (JWT - JSON Web Tokens). 
Tokens expire after 15 minutes to protect against unauthorized access.

## User Experience
- Login once, stay authenticated for 15 minutes
- System automatically refreshes in background
- Optional two-factor authentication for sensitive accounts

## Technical Details
- Token expiry: 15 minutes
- Refresh token expiry: 7 days
- Rate limit: 100 requests per minute
```

**Language**:
- Plain language with technical terms explained
- Complete sentences (but concise)
- Active voice
- Provide context before technical details
- Examples for clarity

**Lists vs Prose**:
- Lists: For specifications, features, requirements
- Prose: For explanations, rationale, user impact
- Mix as needed for comprehension

---

## Common Anti-Patterns

### ❌ Anti-Pattern 1: One-Size-Fits-All Compression
**Problem**: Applying same compression level to all documents
**Impact**: Over-compressed human docs become unreadable, under-compressed LLM docs waste tokens
**Solution**: Use the refined matrix - match compression to audience (LLM/technical/general) and access pattern

### ❌ Anti-Pattern 2: Treating All Hybrid Documents the Same
**Problem**: Not distinguishing between technical and non-technical human readers
**Impact**: Technical docs too verbose for engineers, general docs too terse for stakeholders
**Solution**: Split hybrid into technical (40-60%) and general (20-40%) compression targets

### ❌ Anti-Pattern 3: Premature Optimization
**Problem**: Compressing documents that are rarely loaded
**Impact**: Wasted effort, potential information loss
**Solution**: Focus on session startup docs first (highest cumulative impact)

### ❌ Anti-Pattern 4: Destroying Technical Comprehension for Tokens
**Problem**: Over-compressing hybrid docs to point where humans can't understand them
**Impact**: Maintenance becomes impossible, errors introduced, human audience alienated
**Solution**: 
- Hybrid-Technical: 40-60% reduction maintains technical comprehension
- Hybrid-General: 20-40% reduction maintains general comprehension

### ❌ Anti-Pattern 5: Mixing Audience Types in Single Document
**Problem**: Creating docs that try to serve technical humans, non-technical humans, and LLMs equally
**Impact**: Compromises all use cases, no audience well-served
**Solution**: 
- Create audience-specific versions (technical spec + general summary)
- Or separate documents entirely
- Or generate views from structured source

### ❌ Anti-Pattern 6: Compressing Without Measurement
**Problem**: Assuming compression worked without measuring
**Impact**: May not achieve expected benefits, may lose essential information
**Solution**: Measure token counts before/after, validate information preservation with both LLMs and target human audience

### ❌ Anti-Pattern 7: Assuming Technical Literacy
**Problem**: Writing for technical audience when stakeholders/clients will read
**Impact**: Document becomes inaccessible, decisions made without understanding
**Solution**: Identify actual audience early, create appropriate version for their literacy level

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

**Target Ranges by Audience**:
- LLM-only: 70-85% reduction
- Hybrid-Technical: 40-60% reduction
- Hybrid-General: 20-40% reduction
- Human-Technical-only: 0-10% (technical conciseness)
- Human-General-only: 0% (optimize clarity)
- Archival: 95-99% reduction (conversational logs)

### Information Preservation Validation

**Checklist**:
- [ ] All factual statements preserved
- [ ] Relationships/dependencies intact
- [ ] Temporal ordering maintained
- [ ] Actionable information complete
- [ ] Can reconstruct understanding from compressed version

**Testing Method**:
1. **For LLM-only docs**:
   - Load compressed version to LLM
   - Ask LLM to answer key questions about the content
   - Compare answers to original version
   - Verify no critical information lost

2. **For Hybrid-Technical docs**:
   - Load to LLM (test machine readability)
   - Have developer review (test human readability)
   - Verify both audiences can extract needed information

3. **For Hybrid-General docs**:
   - Load to LLM (test machine readability)
   - Have non-technical stakeholder review (test human readability)
   - Verify comprehension without technical background

---

## Next Steps

### Research Phase
1. **Create test corpus**
   - Select representative documents from each refined category
   - Include both technical and general hybrid examples
   - Measure baseline token counts
   - Document information requirements per audience

2. **Apply compression techniques**
   - LSC for LLM-only docs
   - Structured technical for hybrid-technical docs
   - Structured accessible for hybrid-general docs
   - Conversational compression for archives

3. **Measure and compare**
   - Token reduction achieved per category
   - Information preservation validated (LLM + appropriate human audience)
   - Comprehension testing with target audiences

### Implementation Phase
1. **Develop format templates**
   - LSC schema for strategic docs
   - Structured technical templates (YAML/JSON patterns)
   - Structured accessible templates (clear prose patterns)
   - Compression scripts for conversational logs

2. **Create migration guides**
   - Step-by-step conversion procedures per audience type
   - Validation checklists (LLM + human audience testing)
   - Rollback procedures

3. **Build tooling**
   - Token counters
   - Format validators (per document type)
   - Compression utilities
   - Audience comprehension testing tools

---

## Conclusion

**Core Insight**: Compression is not about "making everything smaller" - it's about **optimizing each document for its specific audience and access pattern**.

**Critical Refinement**: Splitting "hybrid" into technical vs general audiences provides much more precise guidance.

**Key Takeaways**:
1. **Know your audience precisely**: LLM-only, technical humans, non-technical humans, or combinations
2. **Technical literacy matters**: Technical humans can handle 40-60% compression, general audiences need 20-40%
3. **Measure access patterns**: Session startup docs have highest compression ROI
4. **Preserve information fidelity**: Compression must not lose essential context
5. **Balance trade-offs appropriately**: Different audiences have different comprehension requirements
6. **Validate with actual users**: Test with both LLMs AND appropriate human audiences

**Success Criteria**:
- ✅ LLM-only docs achieve 70-85% reduction with zero information loss
- ✅ Hybrid-Technical docs achieve 40-60% reduction while remaining clear to developers
- ✅ Hybrid-General docs achieve 20-40% reduction while remaining clear to stakeholders
- ✅ Human-Technical-only docs optimized for technical depth (0-10% technical conciseness)
- ✅ Human-General-only docs remain optimized for clarity (0%)
- ✅ Archival conversational logs achieve 95-99% reduction with key outcomes preserved

**Next Document**: Create test corpus with representative examples from each refined category to validate compression techniques against this framework.

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

**Audience**: LLM-only
**Information Preserved**: ✅ All facts, ❌ explanatory prose (can be regenerated)

---

### Example 2: System Instructions (Hybrid-Technical)

**Before (Verbose)**: 89 tokens
```markdown
When you encounter a file operation request from the user, you should 
first verify that the file or directory exists by using the appropriate 
tool to check its existence. This is important because attempting operations 
on non-existent paths will result in errors and waste time.
```

**After (Structured Technical)**: 18 tokens (80% reduction)
```yaml
file_ops:
  verify_exists: true  # check path before ops
  tools: [list_directory, get_file_info]
```

**Audience**: Hybrid-Technical (developers)
**Information Preserved**: ✅ Complete specification, ✅ Technical humans can parse, ❌ Verbose explanation

**Alternative Format** (28 tokens, 69% reduction):
```markdown
**File Operations**: Verify path exists (list/get_file_info) before operations. 
Prevents errors on non-existent paths.
```

---

### Example 3: Product Requirements (Hybrid-General)

**Before (Verbose)**: 156 tokens
```markdown
The authentication system should provide a secure login experience for our 
users while maintaining ease of use. Users will log in using their email 
and password, and the system will keep them authenticated for 15 minutes 
of active use. After 15 minutes of inactivity, they will need to log in 
again. This balance between security and convenience ensures that user 
accounts remain protected while not requiring frequent re-authentication 
during active sessions.
```

**After (Structured Accessible)**: 78 tokens (50% reduction)
```markdown
## Authentication Requirements

**Login**: Email + password

**Session Duration**: 15 minutes of active use

**Security Model**: Sessions expire after 15 minutes of inactivity, 
requiring re-login.

**Rationale**: Balances account protection with user convenience during 
active work sessions.
```

**Audience**: Hybrid-General (stakeholders + LLMs)
**Information Preserved**: ✅ All requirements, ✅ Rationale, ✅ Clear to non-technical readers

---

### Example 4: API Specification (Hybrid-Technical)

**Before (Verbose Documentation)**: 215 tokens
```markdown
The authentication endpoint accepts POST requests at /api/auth/login. 
The request body should be a JSON object containing the user's email 
address and password. The endpoint will validate the credentials and, 
if successful, return a JSON response containing an access token and 
a refresh token. The access token expires after 15 minutes and should 
be included in the Authorization header of subsequent requests. The 
refresh token can be used to obtain a new access token when the current 
one expires.
```

**After (OpenAPI-Style)**: 65 tokens (70% reduction)
```yaml
POST /api/auth/login:
  body:
    email: string
    password: string
  response:
    access_token: string  # expires 15m
    refresh_token: string  # for renewal
  auth:
    header: "Authorization: Bearer {access_token}"
```

**Audience**: Hybrid-Technical (developers + LLMs)
**Information Preserved**: ✅ Complete specification, ✅ Technical readers understand immediately

---

### Example 5: Feature Description (Hybrid-General)

**Before (Technical)**: 124 tokens
```markdown
Implement JWT-based authentication with refresh token rotation. Access 
tokens should have 15-minute TTL with RS256 signing algorithm. Refresh 
tokens persist for 7 days with automatic rotation on use. Include rate 
limiting at 100 req/min per IP. Optional TOTP-based MFA for enhanced security.
```

**After (Accessible)**: 95 tokens (23% reduction)
```markdown
## User Authentication

**Login Security**: Users authenticate with encrypted tokens that 
automatically expire after 15 minutes.

**Stay Logged In**: System refreshes authentication automatically for 
up to 7 days of regular use.

**Protection**: Rate limiting prevents automated attacks (100 attempts 
per minute maximum).

**Optional**: Two-factor authentication available for sensitive accounts.
```

**Audience**: Hybrid-General (stakeholders, clients, LLMs)
**Information Preserved**: ✅ All features, ✅ Understandable without technical background, ❌ Implementation details (can be in separate technical spec)

---

### Example 6: Technical Deep-Dive (Human-Technical-Only)

**Before**: Would never compress this document type
**Format**: Rich technical prose with extensive examples, diagrams, code samples

**Example Content**:
```markdown
## JWT Token Validation Performance Analysis

### Background
JWT validation in Node.js applications can become a bottleneck under 
high load. This analysis examines three validation strategies...

[Extensive technical discussion with code examples, performance 
benchmarks, trade-off analysis, edge cases, etc.]
```

**After**: No compression (0% reduction)
**Audience**: Human-Technical-only (never loaded to LLM context)
**Rationale**: Token count irrelevant, optimize for technical depth and learning

---

### Example 7: Conversational Log (Archival)

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

**Audience**: Archival (rarely retrieved)
**Information Preserved**: ✅ Decision, ✅ Artifacts, ✅ Outcome, ❌ Verbose discussion (not needed for future reference)

---

## Summary Table: Audience Types and Compression Targets

| Audience Type | Technical Literacy | Token Priority | Compression Target | Format Type | Example Use Case |
|--------------|-------------------|----------------|-------------------|-------------|------------------|
| **LLM-only** | N/A | Critical | 70-85% | Machine-first (LSC) | PROJECT.lsc, SESSION.lsc |
| **Hybrid-Technical** | High | High | 40-60% | Structured technical | API specs, system config |
| **Hybrid-General** | Low | Moderate | 20-40% | Structured accessible | Product requirements, user stories |
| **Human-Technical-only** | High | None | 0-10% | Rich technical prose | Architecture deep-dives, tutorials |
| **Human-General-only** | Low | None | 0% | Traditional prose | Board papers, client proposals |
| **Archival** | N/A | Low | 95-99% | Conversational compression | Session logs, history |

---

**End of Document**