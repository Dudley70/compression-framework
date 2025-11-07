
## Open Questions

### 1. Intrinsic Stability (HIGH Priority - Task 5.1)
**Status**: Investigation task created, awaiting execution
**Question**: Can compression achieve natural convergence (like solving a mathematical equation) rather than requiring artificial safety blocks?

**Current Approach**: Extrinsic blocking with arbitrary thresholds
- Pre-check: score ≥ 0.8
- Minimal benefit: ratio > 0.85 (< 15% reduction)
- Entity preservation: < 80% retained
- Semantic similarity: < 75% similarity

**Key Questions**:
- Do LSC techniques naturally exhaust (no more patterns to transform)?
- Is there mathematical proof of convergence?
- What happens without safety blocks?
- Can techniques be designed for intrinsic idempotency?

**Investigation Plan**: TASK_5.1_INTRINSIC_STABILITY.md (3-5 hours)
- Phase 1: Code analysis of LSC technique implementations
- Phase 2: Empirical testing with safety blocks disabled (careful review)
- Phase 3: Mathematical convergence analysis

**Impact**: Fundamental to design philosophy, safety guarantees, and white paper formalization

### 2. Threshold Calibration (MEDIUM Priority - Task 5.2)
**Status**: Post-deployment task, requires usage data
**Question**: Are current safety thresholds optimal for practical use?

**Current Issue**: Conservative thresholds block 17/43 test cases (valid compression rejected)

**Investigation Needed**:
- Collect production usage data (2-3 weeks)
- Analyze compression success rates by threshold layer
- A/B test threshold adjustments
- Optimize balance: safety vs usability

**Expected Outcome**: Higher compression success rate while maintaining safety

### 3. LSC Technique Effectiveness (MEDIUM Priority - Task 5.3)
**Status**: Enhancement task, depends on Task 5.1
**Question**: Can LSC techniques achieve better compression ratios within safety bounds?

**Current Issue**: Techniques operational but produce <15% reduction (insufficient benefit)

**Investigation Needed**:
- Analyze technique effectiveness individually
- Identify missed compression opportunities
- Enhance pattern matching and transformations
- Target: 30-50% reduction on verbose documents

**Expected Outcome**: Improved compression ratios passing safety validation
