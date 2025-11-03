---
compression:
  sigma: 0.8
  gamma: 0.5
  kappa: 0.2
  audience: LLM
  tier: T3
  phase: active
  template: meeting-notes
  version: 1.0
---

# [Team/Project] Meeting - [Date] - [Duration]

**Attendees**: [Names]
**Decisions**: [Count]
**Actions**: [Count]

## Decisions Made
- **Decision 1**: [Decision statement with brief rationale] → Owner: [Person] (Due: [Date])
- **Decision 2**: [Decision statement with brief rationale] → Owner: [Person] (Due: [Date])

## Action Items
- [ ] Action - Owner @person (due [Date])
- [ ] Action - Owner @person (due [Date])

## Key Discussion Points
- Topic 1: [1-2 sentence summary of key outcomes]
- Topic 2: [1-2 sentence summary of key outcomes]

## Blockers
[If any, list with resolution ETA]

## Next Meeting
[Date, time, agenda preview]

---

## Example: Engineering Team Sync

---
compression:
  sigma: 0.8
  gamma: 0.5
  kappa: 0.2
  audience: LLM
  tier: T3
  phase: active
  template: meeting-notes
  version: 1.0
---

# Engineering Team Sync - 2025-11-03 - 30 min

**Attendees**: Alice (lead), Bob (backend), Carol (frontend), David (devops)
**Decisions**: 2
**Actions**: 4

## Decisions Made
- **Decision 1**: Use Redis for cache layer (TTL-based, not event-based) → Owner: Bob (Due: Nov 10)
- **Decision 2**: Frontend refactor deferred to Q1 2026 → Owner: Carol (Due: planning session Nov 17)

## Action Items
- [ ] Cache layer spike - Bob @bob (due Nov 10)
- [ ] Database load benchmarking - David @david (due Nov 08)
- [ ] API endpoint documentation update - Carol @carol (due Nov 05)
- [ ] Performance monitoring dashboard setup - David @david (due Nov 12)

## Key Discussion Points
- Cache layer: Decided TTL-based over event-based to reduce complexity. Bob prototyped TTL approach, showing 85% hit rate target achievable with simple implementation.
- Database performance: Current load growing 15% quarterly. Cache layer targets 60% reduction in main database queries. Baseline measurement needed before implementation.
- Frontend refactor: Deferred from Q4 to Q1 after reassessing capacity. Current priorities: stability improvements, monitoring enhancement.
- Q4 objectives: Cache implementation, performance stabilization, monitoring improvements.

## Blockers
None

## Next Meeting
2025-11-10 - Engineering sync (Cache implementation status review)
