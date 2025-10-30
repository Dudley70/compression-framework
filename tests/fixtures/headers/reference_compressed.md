---
doc_type: REFERENCE
audience: llm-only
layer: Operational
phase: Complete
purpose: Reference

target_style:
  sigma: 0.9
  gamma: 0.5
  kappa: 0.1

compression:
  last_full_compression: 2025-10-30 09:00 AEDT
  baseline_tokens: 280
  parameters: {σ: 0.9, γ: 0.5, κ: 0.1}
  validation:
    entity_preservation: 0.98
    semantic_similarity: 0.92
---

# Quick Reference: Git Commands

## Commit
`git add .` → `git commit -m "msg"` → `git push`

## Branch
- Create: `git checkout -b name`
- Switch: `git checkout name`
- Delete: `git branch -d name`

## Status
`git status` → changes
`git log -5` → recent commits
`git diff` → unstaged changes