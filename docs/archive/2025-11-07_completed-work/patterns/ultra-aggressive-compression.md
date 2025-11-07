# Ultra-Aggressive Compression Methods (95-99%)

**Created:** 2025-10-30 11:00 AEDT  
**Status:** Active - Session 4 deliverable  
**Related:** documentation-types-matrix.md, information-preservation-framework.md

---

## Purpose

Documents 95-99% compression techniques for archival and rarely-accessed documentation. This guide covers when ultra-aggressive compression is appropriate, specific techniques, reconstruction trade-offs, and quality assurance for extreme compression scenarios.

**Key Question:** When is it acceptable to compress away 95-99% of a document's tokens?

**Answer:** When storage efficiency matters more than immediate comprehension, and the preserved information enables reconstruction or search when needed.

---

## Overview

### Compression Range Comparison

| Range | Use Case | Primary Goal | Access Pattern |
|-------|----------|--------------|----------------|
| 0-20% | Human-readable docs | Comprehension | Frequent reading |
| 20-40% | Hybrid general | Balance | Regular reference |
| 40-60% | Hybrid technical | Efficiency | Periodic access |
| 70-85% | LLM session docs | Critical efficiency | Every session |
| **95-99%** | **Archive/rarely accessed** | **Storage efficiency** | **Rare/never** |

**Critical Distinction:** Ultra-aggressive compression (95-99%) is NOT for active documents. It's for:
- Historical records rarely retrieved
- Searchable archives (find but don't load full content)
- Long-term storage where space matters
- Conversational logs that may never be reviewed

### When Ultra-Aggressive Compression is Appropriate

**Yes - Use 95-99% compression:**
- ✅ Completed session logs (historical reference only)
- ✅ Deprecated specifications (searchable archive)
- ✅ Old project versions (historical record)
- ✅ Verbose conversation transcripts (outcome preserved elsewhere)
- ✅ Exploratory discussions (decision already documented)
- ✅ Temporary research notes (conclusions extracted)
- ✅ Meeting transcripts (action items captured separately)

**No - Do NOT use 95-99% compression:**
- ❌ Active project documentation
- ❌ Reference specs that may be needed
- ❌ Compliance/audit records requiring full detail
- ❌ Legal documentation
- ❌ Decision rationale (maintainer value)
- ❌ Architecture context (system understanding)
- ❌ Any document where full reconstruction might be needed

---

## Part 1: Conversational Compression Method

### 1.1 Core Technique

**Conversational Compression** is the most aggressive method (99%+ reduction possible), designed for verbose AI-human dialogue that has already produced concrete outcomes.

**Philosophy:** Once a conversation has produced tangible artifacts (code, decisions, documents), the verbose exploratory dialogue becomes less valuable. Extract the essential outcomes and compress the rest.

**Typical Use Case:** 
- 8,500 token conversation → 42 token summary (99.5% reduction)
- Multi-hour session dialogue → Structured outcome record

### 1.2 Four-Tier Compression Strategy

**Tier 0: Artifacts (Preserve 100%)**
```json
{
  "artifacts": [
    {"type": "code", "path": "src/auth.ts", "status": "created"},
    {"type": "code", "path": "src/middleware.ts", "status": "modified"},
    {"type": "doc", "path": "docs/auth-design.md", "status": "created"}
  ]
}
```
**What:** Actual files created or modified  
**Why:** These are the tangible outcomes with full value  
**Compression:** 0% (preserve completely, link to actual files)

**Tier 1: Decisions (High Compression, Structured)**
```json
{
  "query": "implement_authentication",
  "decision": "JWT_with_refresh_tokens",
  "alternatives_considered": ["session_cookies", "OAuth_only"],
  "key_rationale": "stateless_auth_with_mobile_support",
  "timeline": "3_days_implementation"
}
```
**What:** What was decided and why  
**Why:** Decision context valuable for future understanding  
**Compression:** 90-95% (structured outcomes, not full discussion)

**Tier 2: Process Milestones (Ultra-High Compression)**
```json
{
  "milestones": [
    {"event": "design_complete", "timestamp": "2025-10-28T14:30"},
    {"event": "implementation_start", "timestamp": "2025-10-28T15:00"},
    {"event": "testing_complete", "timestamp": "2025-10-29T10:00"}
  ]
}
```
**What:** Major progress points  
**Why:** Timeline understanding, effort estimation  
**Compression:** 98% (timestamps and events only, no detail)

**Tier 3: Dialogue Content (Near-Total Compression)**
```json
{
  "dialogue_summary": "explored_auth_options_discussed_tradeoffs_implemented_JWT"
}
```
**What:** Extremely condensed summary of conversation  
**Why:** Minimal searchability (did we discuss X?)  
**Compression:** 99.5%+ (lossy, barely preserves that conversation happened)

### 1.3 Information Preservation Matrix

| Information Type | Preserve? | Compression | Why |
|-----------------|-----------|-------------|-----|
| Final code/files | 100% | 0% | Tangible artifact, full value |
| Decision + rationale | Core only | 90-95% | Future understanding |
| Alternatives considered | Names only | 95% | Context for "why not X" |
| Timeline/milestones | Events only | 98% | Historical reference |
| Exploratory discussion | Summary | 99%+ | Searchability only |
| Examples shown | None | 100% loss | Recreatable if needed |
| Explanations | None | 100% loss | Artifacts are self-documenting or documented elsewhere |
| Questions asked | None | 100% loss | Answers captured in artifacts/decisions |

### 1.4 Implementation Example

**Before: Full Conversation (8,500 tokens)**
```markdown
User: I need to implement authentication for our app. What are the options?

Claude: There are several approaches to authentication, each with trade-offs:

1. Session-based authentication with cookies
   - Traditional approach
   - Requires server-side session storage
   - Good for web-only applications
   - Challenges with mobile apps and distributed systems

2. JWT (JSON Web Tokens)
   - Stateless authentication
   - No server-side session storage needed
   - Works well across web and mobile
   - Can include user claims directly in token
   - Requires careful handling of token refresh

3. OAuth 2.0 / OpenID Connect
   - Delegated authentication
   - Best for third-party integration
   - More complex to implement
   - Industry standard for social login

For your use case, I'd recommend JWT with refresh tokens because...

[5,000 more tokens of detailed explanation, examples, implementation discussion,
code snippets, debugging suggestions, security considerations, etc.]

User: Let's go with JWT. How do I implement it?

Claude: Here's a complete implementation...

[2,500 more tokens of code examples, configuration, testing, deployment steps, etc.]

User: Perfect! It works. Thanks!
```

**After: Conversational Compression (42 tokens)**
```json
{
  "query": "implement_auth",
  "decision": "JWT_with_refresh",
  "artifacts": ["auth.ts", "middleware.ts"],
  "outcome": "working_implementation"
}
```

**Compression Ratio:** 8,500 → 42 tokens = **99.5% reduction**

**What's Lost:**
- Detailed exploration of alternatives
- Explanations and rationale (preserved in core decision)
- Code examples (actual code in artifacts)
- Step-by-step guidance
- Troubleshooting discussion

**What's Preserved:**
- Query intent (what was being solved)
- Final decision (which approach chosen)
- Artifacts created (where the work lives)
- Outcome (whether it worked)

**Reconstruction:** If full conversation needed later, artifacts + decision provide enough context to understand what happened. The verbose exploration rarely needs to be reviewed.

### 1.5 When to Use Conversational Compression

**Use When:**
- Session dialogue has produced concrete artifacts
- Decisions documented separately in decision log
- Conversation exploratory with many iterations
- Outcome successful (working code/docs)
- Unlikely to need full transcript for learning/audit

**Don't Use When:**
- Legal/compliance requirement for full record
- Educational value in seeing exploration process
- Decision rationale needs full context preservation
- Troubleshooting sessions (valuable for future similar issues)
- High-stakes decisions requiring audit trail

### 1.6 Quality Assurance for Conversational Compression

**Validation Checklist:**
- [ ] All artifacts referenced actually exist
- [ ] Decision captured accurately
- [ ] Enough context for future understanding ("what did we do?")
- [ ] Searchable (can find this session if looking for topic)
- [ ] No compliance/legal requirements violated

**Red Flags (Don't Compress):**
- Decision made without clear rationale → Need fuller preservation
- Artifacts don't tell full story → Need decision context
- May need to explain "why not X" to stakeholders → Need alternatives discussion
- Complex multi-step process → Milestones more important

---

## Part 2: Search-Optimized Compression

### 2.1 Core Technique

**Search-Optimized Compression** focuses on preserving searchability while aggressively compressing content. The compressed form may not be directly readable, but enables finding the right document.

**Philosophy:** You don't need to load full document into context if you can find it when needed. Optimize for discovery, not comprehension.

**Typical Use Case:**
- Large spec collection → Keyword index with minimal descriptions
- Historical decision log → Searchable summaries
- Research archive → Topic tags + outcome summaries

### 2.2 Three-Layer Search Architecture

**Layer 1: Keyword Index (Ultra-High Compression)**
```json
{
  "doc_id": "auth_design_v2",
  "keywords": ["JWT", "refresh_tokens", "stateless", "mobile", "security"],
  "timestamp": "2025-10-28",
  "status": "implemented"
}
```
**Purpose:** Find relevant documents quickly  
**Compression:** 99% (just enough to match search queries)  
**Searchability:** Excellent (keyword matching)

**Layer 2: Structured Summary (High Compression)**
```json
{
  "doc_id": "auth_design_v2",
  "summary": "JWT auth with 15min expiry, 7day refresh, optional MFA",
  "decision": "stateless_preferred_for_mobile",
  "related": ["auth_v1", "security_audit_2025"]
}
```
**Purpose:** Understand what document contains without loading  
**Compression:** 95-98% (structured minimal description)  
**Searchability:** Good (summary provides context)

**Layer 3: Full Document (Separate)**
```
Full detailed specification (not loaded unless specifically needed)
Stored separately, referenced by doc_id
Only loaded if Layers 1-2 indicate relevance
```
**Purpose:** Complete information when needed  
**Compression:** Document-appropriate (40-85% depending on type)  
**Searchability:** Not indexed directly (accessed via doc_id)

### 2.3 Search-Optimized Formats

**Format A: Structured Index**
```yaml
documents:
  - id: auth_v2
    tags: [auth, JWT, security, mobile]
    date: 2025-10-28
    summary_tokens: 45
    full_doc: docs/archive/auth_v2.md
  
  - id: payment_flow
    tags: [payment, stripe, webhooks]
    date: 2025-09-15
    summary_tokens: 38
    full_doc: docs/archive/payment_v1.md
```
**When to Use:** Large document collections  
**Search Method:** Text search on tags/id  
**Compression:** 98-99% (index only)

**Format B: Embedded Summaries**
```markdown
# Archive Index

## auth_v2 (2025-10-28)
**Tags:** JWT, refresh, mobile  
**Summary:** Implemented stateless JWT auth with refresh tokens  
[Full doc: 3,500 tokens](docs/archive/auth_v2.md)

## payment_flow (2025-09-15)
**Tags:** Stripe, webhooks, async  
**Summary:** Stripe integration with async webhook processing  
[Full doc: 2,800 tokens](docs/archive/payment_v1.md)
```
**When to Use:** Moderate collections (< 100 docs)  
**Search Method:** Text search in index file  
**Compression:** 96-98% (summaries + links)

### 2.4 Keyword Selection Strategy

**High-Value Keywords (Always Include):**
- Technology/framework names (JWT, React, PostgreSQL)
- Core concepts (authentication, caching, migration)
- Problem domains (payment, user-management, reporting)
- Decision points (chosen vs alternatives)
- Status markers (implemented, deprecated, proposed)

**Low-Value Keywords (Usually Exclude):**
- Generic terms (system, application, code)
- Process words (discussion, meeting, review)
- Common verbs (implement, create, update)
- Filler words (various, multiple, several)

**Example Transformation:**
```
Before (Full text - 450 tokens):
"We discussed various approaches to implementing user authentication
in our application. After reviewing multiple options including 
traditional session-based authentication and modern token-based
approaches, we decided to implement JWT authentication with refresh
token capability to support both web and mobile clients..."

After (Search-optimized - 8 tokens):
auth JWT refresh mobile web security stateless decision
```

### 2.5 When to Use Search-Optimized Compression

**Use When:**
- Large archive of historical documents
- Need to find specific topics across many documents
- Full documents rarely loaded (search first, load if relevant)
- Storage efficiency critical
- Documents have clear subject matter

**Don't Use When:**
- Small document collection (< 20 docs)
- Documents frequently loaded fully
- Content too similar (keywords don't differentiate)
- Full-text search already available (no additional value)

---

## Part 3: Reconstruction Trade-Offs

### 3.1 The Reconstruction Spectrum

**Key Principle:** Ultra-aggressive compression is lossy. Information is permanently lost. The question is: what level of reconstruction is needed?

| Reconstruction Level | Compression | Use Case | Example |
|---------------------|-------------|----------|---------|
| **None Required** | 99%+ | Searchability only | Find if topic discussed |
| **Outcome Only** | 98-99% | What was result | Decision + artifacts |
| **Context Summary** | 95-98% | Why and what | Structured decision record |
| **Detailed Context** | 85-95% | Full understanding | Abbreviated but complete |
| **Full Reconstruction** | <85% | Must recreate original | Legal/compliance docs |

### 3.2 Acceptable Information Loss

**Information Types by Reconstruction Need:**

**Can Safely Discard (99%+ compression acceptable):**
- Exploratory questions and initial discussion
- Examples that illustrate (final implementation is example)
- Repeated explanations of same concept
- Tangential discussions
- Process overhead (coordination, scheduling, admin)
- Intermediate failed attempts (if final version succeeded)

**Preserve in Summary Form (95-98% compression):**
- Final decision made
- Key rationale (1-2 main reasons)
- Alternatives considered (names only)
- Outcome/status
- Artifacts created

**Preserve in Structured Detail (85-95% compression):**
- Decision rationale with context
- "Why not X" for major alternatives
- Trade-offs and constraints
- Future considerations
- Success/failure criteria

**Preserve Fully (<85% compression):**
- Legal commitments and agreements
- Compliance audit trails
- Architecture decisions with system-wide impact
- Security decisions and threat models
- Data governance and privacy decisions

### 3.3 Irreversible vs Reversible Compression

**Irreversible Compression:**
- Information permanently lost
- Cannot recreate original from compressed form
- Appropriate when original not needed

**Example:**
```
Original: "After extensive discussion about authentication approaches, 
considering the trade-offs between session-based and token-based 
authentication, reviewing security implications, performance 
characteristics, and mobile client requirements, we decided to 
implement JWT with refresh tokens."

Compressed: {decision: "JWT_with_refresh"}

Lost Forever: The detailed exploration process
Preserved: The outcome
```

**Reversible Compression** (Not truly 95-99%):
- Original can be recreated perfectly
- Techniques: Gzip, zlib, compression algorithms
- Not "ultra-aggressive" in our context (doesn't reduce tokens, just bytes)

**Key Distinction:** Ultra-aggressive compression is INTENTIONALLY lossy. We're choosing what to forget.

### 3.4 Reconstruction Quality Assessment

**Quality Tiers:**

**Tier 1: Search Result (Lowest Quality)**
```json
{"topic": "auth_implementation", "date": "2025-10-28"}
```
**Can Reconstruct:** "We worked on auth on this date"  
**Cannot Reconstruct:** Any details whatsoever  
**Acceptable When:** Just need to know topic was discussed

**Tier 2: Outcome Record**
```json
{
  "query": "implement_auth",
  "decision": "JWT",
  "outcome": "working"
}
```
**Can Reconstruct:** What was done and result  
**Cannot Reconstruct:** Why, how, alternatives, process  
**Acceptable When:** Outcome is what matters, process irrelevant

**Tier 3: Decision Summary**
```json
{
  "query": "implement_auth",
  "decision": "JWT_with_refresh",
  "rationale": "stateless_auth_mobile_support",
  "alternatives": ["sessions", "OAuth"],
  "outcome": "implemented_successfully"
}
```
**Can Reconstruct:** What, why (briefly), what else considered, result  
**Cannot Reconstruct:** Detailed rationale, full discussion, examples  
**Acceptable When:** Context needed but not full detail

**Tier 4: Abbreviated Record (85-95%, not truly "ultra-aggressive")**
```markdown
## Authentication Decision

**Chose:** JWT with refresh tokens
**Why:** Stateless auth supports mobile, web, and future API clients without session storage
**Alternatives:** Session cookies (server-side state required), OAuth only (over-engineered for our needs)
**Trade-offs:** Token management complexity vs stateless benefits
**Result:** Implemented successfully, 3-day effort
```
**Can Reconstruct:** Most of decision context  
**Cannot Reconstruct:** Full discussion details  
**Acceptable When:** Decision may need explanation to future team members

### 3.5 When Full Reconstruction Matters

**Scenarios Requiring <85% Compression (Not Ultra-Aggressive):**

**Legal and Compliance:**
- Audit trails for regulated industries
- Contractual agreements
- Data governance decisions
- Privacy/GDPR related decisions
- Security incident records

**Architecture with Long-Term Impact:**
- System-wide architecture decisions
- Technology stack choices
- Data model decisions
- API contract decisions
- Migration strategies

**Learning and Knowledge Transfer:**
- Post-mortems (valuable learning)
- Complex problem-solving sessions (reusable patterns)
- Novel approaches (may benefit future similar problems)

**Stakeholder Communication:**
- Executive decision briefings
- Customer-facing explanations
- Team alignment documents

**Decision:** If any of these apply, do NOT use ultra-aggressive compression. Use 40-85% compression with full context preserved.

---

## Part 4: Archive Lifecycle and Transition Strategy

### 4.1 Document State Lifecycle

**Active → Complete → Archive → Ultra-Compressed**

**Active (Phase-appropriate compression: 30-70%)**
- Document in use for current work
- Compression based on role/layer/phase from Matrix
- Full context needed

**Complete (Phase +15-25% more compression: 45-85%)**
- Work finished, document reference only
- Increase compression, reduce "how-to" detail
- Preserve outcomes and decisions

**Archive (Additional +10-20%: 55-95%)**
- Historical record, rarely accessed
- Further compression of process detail
- Focus on searchability and outcomes

**Ultra-Compressed (95-99% for eligible docs)**
- Very old historical records
- Outcomes preserved elsewhere (git history, artifacts)
- Searchability only, or not even that

### 4.2 When to Transition to Ultra-Aggressive Compression

**Time-Based Triggers:**
- 6+ months since last access
- 1+ year since document completion
- 2+ years for any document

**Event-Based Triggers:**
- Project completely deprecated/replaced
- Technology stack migrated away
- Decision superseded by newer decision
- Artifacts moved to long-term archive storage

**Value-Based Triggers:**
- Outcome fully captured in other docs
- No compliance/audit requirement
- No educational value identified
- No active links/references from active docs

**Process:**
1. Identify document meeting trigger criteria
2. Verify no compliance/legal retention requirements
3. Check for references from active documents
4. Extract any uncaptured outcomes/decisions
5. Create ultra-compressed version
6. Move original to deep archive (cold storage) or delete
7. Update index with search-optimized reference

### 4.3 Reversible Archive Strategy

**For Documents with Uncertain Future Value:**

**Two-Tier Archive:**
```
/docs/archive/
  active-reference/     # 85-95% compression, may be needed
  cold-storage/         # 95-99% compression, rarely/never needed
```

**Active-Reference Archive:** Documents that might be consulted
- Detailed summaries (85-95% compression)
- Preserved in main repository
- Searchable and accessible
- Examples: Completed features, recent decisions

**Cold-Storage Archive:** Documents unlikely to be needed
- Ultra-compressed (95-99%)
- Moved to separate storage or deleted with index entry
- Minimal searchability
- Examples: Very old sessions, deprecated specs, replaced documentation

### 4.4 Archive Compression Workflow

**Step 1: Pre-Compression Review**
```
Questions:
- When was this last accessed? (Check git log)
- Are there active references? (grep -r "document_name")
- Compliance requirements? (Check retention policy)
- Extracted outcomes? (Verify decision log, artifacts)
- Educational value? (Ask team)
```

**Step 2: Compression Type Selection**
```
Conversational (session logs, discussions) → Tier 2-3 compression
Search-Optimized (specs, references) → Keyword index + summary
Outcome-Only (completed work) → Artifacts + decision record
```

**Step 3: Create Compressed Version**
```
Apply selected compression technique
Validate searchability if needed
Preserve doc_id and metadata
```

**Step 4: Verification**
```
Can find document if searching for topic? YES/NO
Enough context to understand what it was? YES/NO
Artifacts/outcomes preserved elsewhere? YES/NO
No compliance issues? YES/NO

If all YES → proceed
If any NO → reconsider compression level
```

**Step 5: Archive**
```
Move original to appropriate tier
Update index
Add archive metadata (date, reason, compression type)
```

---

## Part 5: Best Practices and Warnings

### 5.1 Best Practices

**1. Compress Progressively, Not Immediately**
```
Day 0: Active work (30-70% compression)
Day 30: Complete (45-85% compression)
Month 6: Archive (55-95% compression)
Year 1+: Ultra-compressed (95-99% compression)

Don't jump straight to ultra-aggressive
```

**2. Extract Before Compressing**
```
WRONG: Compress verbose document → lose information
RIGHT: Extract decisions/outcomes → then compress discussion
```

**3. Maintain Search Layer**
```
Ultra-compressed documents should still be findable
Keyword index or search-optimized summaries
"Did we discuss X?" should be answerable
```

**4. Document Compression Decisions**
```yaml
archive_metadata:
  original_size: 8500_tokens
  compressed_size: 42_tokens
  compression_ratio: 99.5%
  compression_type: conversational
  date_compressed: 2025-10-30
  reason: session_log_outcomes_captured
  artifacts_preserved: [auth.ts, middleware.ts, docs/auth.md]
```

**5. Validate Artifacts Exist**
```
Before compressing conversation to just artifact references,
verify artifacts actually exist and are complete.

Compressed: {artifacts: ["auth.ts"]}
Reality: auth.ts was later deleted or moved

Result: Lost all context permanently
```

**6. Keep Escape Hatch**
```
For first 6-12 months after ultra-compression:
- Keep original in cold storage (cheap S3/archive tier)
- Can restore if compression was too aggressive
- Delete original only after confidence period
```

### 5.2 Anti-Patterns and Warnings

**Anti-Pattern 1: Premature Ultra-Compression**
❌ **Bad:** Compress to 99% while project still active  
✅ **Good:** Wait until truly archived (6+ months old)

**Why:** You'll likely need the detail sooner than expected

**Anti-Pattern 2: Compress Without Extraction**
❌ **Bad:** Ultra-compress document containing undocumented decisions  
✅ **Good:** Extract decisions to decision log first, then compress

**Why:** Lose information that should be preserved

**Anti-Pattern 3: Uniform Compression**
❌ **Bad:** Apply same 99% compression to all old documents  
✅ **Good:** Assess each document type individually

**Why:** Some old documents have ongoing value (architecture, decisions)

**Anti-Pattern 4: Lose Searchability**
❌ **Bad:** Compress to point where you can't find document later  
✅ **Good:** Maintain keyword index or search layer

**Why:** "Did we discuss X?" becomes unanswerable

**Anti-Pattern 5: Ignore Compliance**
❌ **Bad:** Ultra-compress audit trail because it's old  
✅ **Good:** Check retention requirements before any compression

**Why:** Legal/compliance violations, potential liability

**Anti-Pattern 6: Compress Active References**
❌ **Bad:** Ultra-compress document that's still linked from active docs  
✅ **Good:** Check for references, update links before compressing

**Why:** Break active workflows, confuse team members

### 5.3 Quality Assurance Checklist

**Before Ultra-Aggressive Compression (95-99%):**

**Document Assessment:**
- [ ] Document is truly archival (6+ months old OR explicitly obsolete)
- [ ] No compliance/legal retention requirements for full detail
- [ ] No active references from current documentation
- [ ] Outcomes/decisions extracted and preserved elsewhere

**Compression Planning:**
- [ ] Compression type selected (conversational / search-optimized / outcome-only)
- [ ] Identified what to preserve vs discard
- [ ] Search/findability strategy defined
- [ ] Escape hatch planned (cold storage of original for 6-12 months)

**Post-Compression Validation:**
- [ ] Can find document if searching for relevant topic
- [ ] Compressed version has enough context to understand what it was
- [ ] All artifact references validated (files exist)
- [ ] Archive metadata documented
- [ ] Index updated

**Long-Term:**
- [ ] Monitor for unexpected access requests (sign compression was too aggressive)
- [ ] Review annually: still appropriate compression level?
- [ ] Delete originals after confidence period (6-12 months)

---

## Conclusion

Ultra-aggressive compression (95-99%) is a powerful technique for storage-efficient archival, but requires careful application. Key principles:

1. **Progressive Compression:** Don't jump straight to 99%. Transition through Active → Complete → Archive → Ultra-Compressed.

2. **Extract Before Compressing:** Preserve outcomes, decisions, and artifacts separately before compressing discussion.

3. **Maintain Searchability:** Even ultra-compressed docs should be findable.

4. **Assess Appropriateness:** Not all old documents should be ultra-compressed (compliance, architecture, learning value).

5. **Keep Escape Hatch:** Cold-storage original for 6-12 months before permanent deletion.

6. **Validate Thoroughly:** Check compliance, references, artifacts before compressing.

**When Ultra-Aggressive Compression Works:**
- Conversational logs with outcomes captured elsewhere
- Verbose explorations that produced concrete artifacts
- Historical records with minimal ongoing value
- Search-only archives (find but don't load)

**When to Avoid:**
- Compliance/legal retention requirements
- Architecture decisions with ongoing impact
- Decision rationale that may need explanation
- Educational value for future similar problems
- Active references or uncertain future value

**Remember:** Ultra-aggressive compression is intentionally lossy. Make conscious decisions about what to forget, and preserve what matters separately before compressing away the rest.

---

*This guide is part of the Compression Project framework for systematic documentation optimization.*