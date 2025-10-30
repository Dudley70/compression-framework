---
doc_type: API_REFERENCE
audience: llm-only
layer: Operational
phase: Complete
purpose: Reference

target_style:
  sigma: 0.8
  gamma: 0.6
  kappa: 0.2

compression:
  last_full_compression: 2025-10-30 14:30 AEDT
  baseline_tokens: 450
  parameters: {σ: 0.8, γ: 0.6, κ: 0.2}
  validation:
    entity_preservation: 0.96
    semantic_similarity: 0.89

writing_guide:
  preferred_patterns: |
    ✓ Bullet lists for parameters/returns
    ✓ Code examples inline
    ✓ HTTP status codes explicit
  anti_patterns: |
    ✗ Prose explanations
    ✗ Redundant descriptions
    ✗ Excessive scaffolding
---

# API Reference

## POST /auth
- Body: `{username, password}`
- Returns: `{token}` (200) | `{error}` (401)
- Headers: `Content-Type: application/json`

## GET /users
- Auth: Bearer token required
- Returns: User array
- Filters: `?role=admin&status=active`