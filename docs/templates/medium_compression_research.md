---
compression:
  sigma: 0.5
  gamma: 0.7
  kappa: 0.5
  audience: dual
  tier: T2
  phase: active
  template: analysis
  version: 1.0
---

# [Analysis Topic] Analysis & Findings

## Executive Summary
[Key findings in 3-5 bullet points]

## Research Question
[What are we trying to understand? What gap are we addressing?]

## Methodology
[How did we gather data? What sources? What approach?]

## Findings

### Finding 1: [Concise Finding Title]
**Data**: [Evidence supporting this finding]

| Factor | Value | Significance |
|--------|-------|-------------|
| Key metric | measurement | Why it matters |

**Implication**: [What does this mean for our decisions or next steps?]

### Finding 2: [Concise Finding Title]
[Continue pattern with data, metrics, implications]

### Finding 3: [Concise Finding Title]
[Continue pattern with data, metrics, implications]

## Recommendations
1. [Action] - because [evidence from findings]
2. [Action] - because [evidence from findings]
3. [Action] - because [evidence from findings]

## Limitations & Caveats
[What might invalidate these findings? What data is missing? What assumptions are we making?]

## Next Steps
[Follow-up research or implementation needed]

---

## Example: Query Performance Analysis

---
compression:
  sigma: 0.5
  gamma: 0.7
  kappa: 0.5
  audience: dual
  tier: T2
  phase: active
  template: analysis
  version: 1.0
---

# Database Query Performance Analysis

## Executive Summary
- Average query time increased 40% over 6 months (1.2s → 1.7s)
- Top 5 queries account for 78% of total database load
- Index optimization could reduce top query time by 55-70%
- Caching would impact 3 of top 5 queries effectively (50% of load)

## Research Question
Where are the biggest performance bottlenecks in our database workload, and which interventions would have the highest impact?

## Methodology
Analyzed 2.3M queries from production database over 30-day period. Instrumented queries with execution time, row count, and index usage. Ranked queries by total load (execution time × frequency). Tested optimization approaches on staging environment mirroring production data patterns.

## Findings

### Finding 1: Top 5 Queries Drive Majority of Load
**Data**:
```
Query 1 (user search): 2,100s total time (28% of load)
Query 2 (feed generation): 1,850s total time (25%)
Query 3 (analytics aggregation): 1,200s total time (16%)
Query 4 (recommendation fetch): 890s total time (12%)
Query 5 (notification check): 740s total time (10%)
```

**Analysis**: These 5 queries represent 6,780s of 8,740s total database time (77.6%). Addressing these yields maximum ROI.

**Implication**: Optimization efforts should focus here first. Even small improvements (10%) save significant time.

### Finding 2: Index Gaps Account for 40% of Top Query Slowness
**Data**:
- Query 1: Missing index on user_type + created_at (full table scan)
- Query 3: Inefficient multi-column index (wrong column order)
- Query 4: Query 4: Full index scan instead of range scan (index not optimized)

**Testing Results**: Adding missing indices and reordering columns reduced execution times:
- Query 1: 340ms → 150ms (56% improvement) ✓
- Query 3: 280ms → 120ms (57% improvement) ✓
- Query 4: 190ms → 85ms (55% improvement) ✓

**Implication**: Index optimization is low-effort, high-impact intervention. No application changes required.

### Finding 3: Caching Reduces Load for 3 of 5 Top Queries
**Data**:

| Query | Type | Cacheable | Hit Rate | Impact |
|-------|------|-----------|----------|--------|
| Feed generation | Read | Yes | 85% | -30% load |
| Analytics agg | Read | Partial | 60% | -15% load |
| Recommendation | Read | Yes | 90% | -25% load |
| Notification | Write-heavy | No | 10% | -2% load |

**Testing**: Cache layer simulation shows 50% load reduction on cacheable queries.

**Implication**: Combined index + cache strategy targets 65-70% reduction of top query load.

## Recommendations
1. **Immediate**: Add missing indices and optimize column order (2-3 hours implementation)
   - Evidence: 55-57% improvement on individual queries, 40% of slowness addressed
   
2. **Week 2**: Implement caching for feed generation and recommendation queries (1-2 days)
   - Evidence: 85-90% cache hit rates, 50% load reduction on these queries
   
3. **Post-optimization measurement**: Re-baseline after changes to validate improvement
   - Evidence: Need before/after comparison on production workload

## Limitations & Caveats
- Analysis based on 30-day sample; seasonal patterns may exist
- Staging tests don't capture peak load behavior (only average)
- Query patterns may change with new features (not predictive)
- Index maintenance has write-time cost (not calculated here)

## Next Steps
1. Validate index changes on staging with production-like data volume
2. Plan cache layer implementation with team
3. Schedule 2-week performance improvement sprint
4. Establish ongoing monitoring for query performance trends
