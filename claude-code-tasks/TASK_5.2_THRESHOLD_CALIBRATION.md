# Task: Threshold Calibration

**Task ID**: TASK-5.2-THRESHOLD-CALIBRATION
**Created**: 2025-11-01
**Priority**: MEDIUM (Post-deployment)
**Type**: Optimization
**Estimated Duration**: 4-6 hours
**Dependencies**: Production deployment, usage data collection

---

## Objective

Calibrate safety system thresholds based on real-world usage data to optimize the balance between compression efficiency and information preservation.

---

## Background

Current thresholds are **conservative by design**:
- **Pre-check**: score ≥ 0.8 (blocks already-compressed documents)
- **Entity preservation**: ≥ 80% retention required
- **Minimal benefit**: < 85% compression ratio (requires ≥ 15% reduction)
- **Semantic similarity**: ≥ 75% similarity required

**Issue**: Validation report shows 17/43 tests "failing" due to conservative thresholds blocking valid compression. High false positive rate limits practical usability.

---

## Investigation Plan

### Phase 1: Usage Data Collection (2-3 weeks post-deployment)

**Metrics to Track**:
1. Compression attempt rate (attempts per day)
2. Success rate (% passing all safety layers)
3. Failure breakdown by layer (which layers block most?)
4. User feedback on blocked compressions (false positives?)
5. Token reduction achieved on successful compressions
6. Document types and characteristics

**Data Collection**:
- Log all compression attempts with full safety details
- Survey users on satisfaction with compression results
- Track manual overrides (if implemented)
- Gather examples of "should have compressed" cases

### Phase 2: Threshold Analysis (2-3 hours)

**Analysis Questions**:
1. What % of attempts blocked by each layer?
2. Are any thresholds too strict? Too lenient?
3. What token reduction do successful compressions achieve?
4. Are there document type patterns (code-heavy vs prose)?
5. Do users report false positives?

**Optimization Targets**:
- **Pre-check**: Should 0.8 become 0.85? (less aggressive)
- **Minimal benefit**: Should 0.85 become 0.80? (accept 20% reduction)
- **Entity preservation**: Is 80% optimal or should it be 75%/85%?
- **Semantic similarity**: Is 75% optimal or should it adjust?

### Phase 3: A/B Testing (1-2 hours)

**Test Design**:
- Run compression with current thresholds (baseline)
- Run compression with adjusted thresholds (experimental)
- Compare: success rate, token reduction, user satisfaction
- Validate: no information loss in experimental group

**Safety**: Manual review of experimental results before deployment

### Phase 4: Implementation (1 hour)

**Deliverables**:
- Update threshold constants in compress.py
- Document rationale for changes
- Update tests to reflect new thresholds
- Deploy updated tool

---

## Success Criteria

- [ ] Usage data collected (min 2 weeks, 50+ compression attempts)
- [ ] Threshold analysis complete with recommendations
- [ ] A/B testing validates improvements
- [ ] Updated thresholds deployed
- [ ] Success rate improved by ≥10% while maintaining safety

---

## Deliverables

1. **usage_data_analysis.md** - Analysis of production usage
2. **threshold_optimization_recommendations.md** - Proposed changes with rationale
3. **ab_test_results.md** - Validation of threshold changes
4. Updated compress.py with optimized thresholds

---

## Timeline

- **Data Collection**: 2-3 weeks post-deployment
- **Analysis & Testing**: 4-6 hours
- **Implementation**: 1 hour
- **Total**: ~3-4 weeks calendar time
