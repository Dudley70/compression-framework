---
title: Optional Optimizations Investigation
status: Planning
created: 2025-11-02 14:15 AEDT
updated: 2025-11-02 14:15 AEDT
---

# Optional Optimizations Investigation

**Context**: Tool is production-ready with conservative safety settings. Three optional optimization tasks available. This document evaluates each for value, feasibility, and timing.

---

## Summary

| Task | Duration | Priority | Value | Difficulty | Recommendation |
|------|----------|----------|-------|------------|-----------------|
| TASK-5.2: Threshold Calibration | 4-6h (+ 2-3 weeks data collection) | MEDIUM | HIGH | LOW | **Start when deployment begins** |
| TASK-5.3: LSC Improvement | 8-12 hours | MEDIUM | HIGH | MEDIUM | **High-value, defer to after white paper** |
| TASK-5.4: Model Caching | 2-3 hours | LOW | MEDIUM | LOW | **Quick win, optional** |

---

## Detailed Analysis

### TASK-5.2: Threshold Calibration

**What it does**: Analyzes production usage data to optimize safety thresholds for better compression efficiency.

**Current state**:
- Thresholds are conservative by design (safety-first philosophy)
- Validation report shows 17/43 tests blocked by thresholds (false positives)
- Pre-check 0.8, Entity 80%, Minimal benefit 0.85, Similarity 75%

**Why it matters**:
- Real usage patterns may show thresholds are unnecessarily strict
- Could improve success rate by 10-20% based on production data
- Tool currently blocks valid compressions to stay conservative

**Timeline issue**:
- Requires 2-3 weeks of production usage data first
- Analysis itself: 2-3 hours
- A/B testing: 1-2 hours
- Implementation: 1 hour
- **Can't start until tool deployed and collecting data**

**Risk**: Low (usage data will inform safe adjustments)

**Recommendation**: **Start data collection phase immediately upon deployment.** This runs in parallel with other work. Don't block on it, but capture data continuously. When enough data accumulated, run analysis phase (4-6 hours) as standalone task.

---

### TASK-5.3: LSC Technique Improvement

**What it does**: Enhances the 5 LSC techniques to achieve better compression ratios (30-50% reduction vs current <15%).

**Current state**:
- All 5 techniques implemented and validated
- Techniques are operational but conservative
- verbose_prose.md achieves <15% reduction (blocked as "minimal benefit")

**Why it matters**:
- **Highest practical impact**: Directly improves compression effectiveness
- Unlocks higher compression ratios within safety bounds
- Most documents will see tangible improvement
- Makes tool more valuable for real-world usage

**Investigation phases**:
1. Analyze current technique effectiveness (2-3 hours) - What's being compressed? What patterns are missed?
2. Enhance implementations (4-6 hours) - Better pattern matching, aggressive transformations, smarter context removal
3. Validate safety (2-3 hours) - Ensure entity preservation, semantic similarity, no regression
4. Regression testing (1-2 hours) - All 43 tests still pass

**Risk**: MEDIUM (must validate no information loss)

**Dependencies**: Task 5.1 complete ✅ (intrinsic stability understood, improvements will maintain that property)

**Value proposition**:
- verbose_prose.md: <15% → 30-50% possible
- Already-compressed docs: unchanged (intrinsic stability)
- Safety guarantees maintained (all checks still apply)

**Recommendation**: **High priority for post-white paper.** This is the most impactful optimization. Run after white paper draft (so you understand all technique trade-offs), then invest 8-12 hours. Results will make tool significantly more effective in production.

---

### TASK-5.4: Model Caching

**What it does**: Eliminates 15-20s model loading time on first use by caching models in memory or as daemon.

**Current state**:
- Total workflow: 20-25s (includes 15-20s model load)
- Already meets <30s requirement
- Model loading is one-time overhead per session

**Why it matters**:
- Improves user experience (5-10s subsequent operations)
- Nice-to-have optimization, not critical
- Low effort (2-3 hours), quick win

**Implementation options**:
1. In-memory cache (simplest, works within CLI)
2. Daemon mode (keeps process running, fastest repeated use)
3. Persistent cache (loads pre-trained models from disk)

**Risk**: LOW (cosmetic improvement, no safety implications)

**Recommendation**: **Quick afternoon task if bored, but low priority.** Current performance already good enough. Would be nice to have but not blocking any use cases. Could be paired with something else or deferred indefinitely.

---

## Recommended Approach

### Immediate (This Session)
- **Document decision** in SESSION.md
- Create decision log entry in PROJECT.md
- Optionally: Run TASK-5.4 (2-3 hours) as "polish" if time available

### Short-term (Post-white paper)
- **Start deploying tool** with monitoring for threshold calibration
- **Run TASK-5.3** (8-12 hours) - Most impactful optimization
- Collect data continuously for TASK-5.2

### Medium-term (Once deployment data available)
- **Run TASK-5.2** analysis phase (4-6 hours) - Make data-driven threshold adjustments

### Optional
- TASK-5.4 if performance ever becomes concern (currently not an issue)

---

## Value Rankings

### By Impact on Production Use
1. **TASK-5.3 (LSC Improvement)** - Direct compression effectiveness (30-50% potential uplift)
2. **TASK-5.2 (Threshold Calibration)** - Safety threshold optimization (10-20% success rate improvement)
3. **TASK-5.4 (Model Caching)** - User experience polish (5-10s improvement on repeated use)

### By Effort/Value Ratio
1. **TASK-5.4 (Model Caching)** - 2-3 hours for moderate UX improvement
2. **TASK-5.3 (LSC Improvement)** - 8-12 hours for high compression improvement
3. **TASK-5.2 (Threshold Calibration)** - 4-6 hours but requires 2-3 weeks data first

### By Urgency
1. **TASK-5.2** - Data collection should start immediately (parallel to white paper)
2. **TASK-5.3** - Should run post-white paper (while understanding is fresh)
3. **TASK-5.4** - Any time, nice-to-have

---

## Decision Points

**For next session:**

1. **Do you want to run TASK-5.4 now?** (2-3 hour polish task)
   - YES → Start immediately
   - NO → Defer indefinitely, it's optional

2. **Should white paper development start now?** (with optional optimizations deferred)
   - YES → Focus on white paper with rigorous theory
   - NO → Run optimization tasks first to solidify tool

3. **When to start deployment?** (triggers TASK-5.2 data collection)
   - Recommend: After white paper draft (so you've formalized understanding)
   - Parallel: Start collecting data simultaneously

---

## Timeline Scenarios

### Scenario A: Polish First
- TASK-5.4: 2-3 hours today
- White Paper: 10-15 hours (high-quality academic writing)
- Deployment + TASK-5.2 data collection: Parallel
- TASK-5.3: 8-12 hours post-white paper
- **Total**: ~20-30 hours over 3-4 weeks

### Scenario B: Focus on White Paper
- White Paper: 10-15 hours (this week)
- Deployment + TASK-5.2 data collection: Parallel
- TASK-5.3: 8-12 hours once white paper complete
- TASK-5.4: Optional when feeling motivated
- **Total**: ~18-27 hours over 2-3 weeks

### Scenario C: All Optimizations
- TASK-5.4: 2-3 hours today
- TASK-5.3: 8-12 hours this week
- White Paper: 10-15 hours (with enhanced compression data)
- Deployment + TASK-5.2 data collection: Parallel
- **Total**: ~30-40 hours over 3-4 weeks

---

## Recommendation

**Start with Scenario B**: Focus on white paper while deploying tool for data collection. TASK-5.3 is high-value but needs to be informed by white paper's theoretical understanding. TASK-5.2 requires production data anyway. TASK-5.4 is optional polish.

**Why this order?**
1. White paper captures current understanding (useful reference point)
2. Deployment starts data collection for TASK-5.2
3. TASK-5.3 improvements made with full context
4. TASK-5.4 deferred indefinitely (not critical)

**Alternative**: Run TASK-5.4 first if you want a quick win to close out this investigation cycle.

---

