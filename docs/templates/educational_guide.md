---
compression:
  sigma: 0.4
  gamma: 0.9
  kappa: 0.8
  audience: new-users
  tier: T1
  phase: active
  template: educational
  version: 1.0
---

# [Topic] Getting Started

## What is [Topic]?
[Introduction explaining concept clearly for newcomers, with concrete examples]

## Why Does This Matter?
[Practical examples showing why someone should care about this topic]

## Prerequisites
- [What foundational knowledge you should have before starting]
- [Tools or software you need installed]
- [Concepts you should be familiar with]

## Step 1: [First Learning Objective]

[Explain the core concept clearly with real-world analogy or comparison]

Here's a simple example to illustrate the idea:

```
code example showing basic concept
```

[Explain what the example shows and why each part matters. What would happen if we changed it?]

## Step 2: [Next Learning Objective]

[Continue with progressive disclosure - build on step 1]

When you're working with this, you'll typically follow this pattern:

```
code example building on step 1
```

[Explain the new capability this adds and how it builds on the previous step]

## Step 3: [Third Learning Objective]

[Further build the skill with practical application]

[Continue pattern...]

## Common Questions

**Q**: [Question that often comes up]
**A**: [Answer with full context explaining why and how]

**Q**: [Question that often comes up]
**A**: [Answer with full context explaining why and how]

## Next Steps
[What to learn next, where to go for deeper knowledge, recommended next topics]

## Troubleshooting

**Issue**: [Symptom or error you might encounter]
**Solution**: [How to fix it with explanation of why this works]

**Issue**: [Symptom or error you might encounter]
**Solution**: [How to fix it with explanation of why this works]

---

## Example: Getting Started with Document Compression

---
compression:
  sigma: 0.4
  gamma: 0.9
  kappa: 0.8
  audience: new-users
  tier: T1
  phase: active
  template: educational
  version: 1.0
---

# Document Compression Getting Started Guide

## What is Document Compression?

Document compression is a systematic approach to making your written documents shorter and more efficient to read, while keeping all the important information intact. Think of it like editing a long email: you remove the "fluff" but keep the core message clear.

The compression framework uses three simple dimensions to control how you write:

1. **Structure (σ)**: How organized should the content be? (0 = flowing prose, 1 = tables and lists)
2. **Detail (γ)**: How much information should you include? (0 = keywords only, 1 = complete sentences)
3. **Context (κ)**: How much background explanation? (0 = assume expertise, 1 = explain everything)

You pick the levels based on what you're writing and who will read it. There's no "best" compression level—it depends entirely on your document.

## Why Does This Matter?

**Problem**: Without compression, documents grow verbose over time. Status updates become narratives. Technical specs turn into novels. Readers spend more time reading than thinking.

**Solution**: Compression lets you write efficiently from the start. A status update might look like:

```
## Status - 2025-11-03

| Task | Status | Notes |
|------|--------|-------|
| Feature A | 90% | Ready for QA |
| Bug fix | Complete | Deployed |
```

Instead of:

```
We have been making good progress on Feature A. It's approximately 
90% complete and we believe it is ready for the quality assurance 
testing phase. The bug fix has been completely finished and has 
been deployed to production...
```

Same information, but the compressed version takes 10 seconds to read instead of 30 seconds.

## Prerequisites
- Basic familiarity with markdown format (headers, bullet lists, tables)
- Understanding of your intended audience (who will read this?)
- A document you want to write or improve

## Step 1: Choose Your Document Type

First, identify what you're writing. Different documents need different compression styles:

**Status updates**: High structure (tables), low detail (just facts), minimal context
**Design documents**: Medium structure (mix of prose + lists), medium detail, moderate context  
**Onboarding guides**: Low structure (flowing prose), high detail (full explanations), high context

Why? Because a busy manager reading a status wants quick facts in a table. A developer reading a design doc needs to understand the reasoning. A new employee needs full explanation.

## Step 2: Add Compression Metadata

Every compressed document starts with metadata telling the system how to maintain your chosen compression level:

```yaml
---
compression:
  sigma: 0.8       # Highly structured (tables/lists)
  gamma: 0.4       # Concise facts only
  kappa: 0.2       # Minimal context
  audience: LLM    # For AI/system reading
  tier: T2         # Valuable information
  phase: active    # Current/ongoing work
---
```

This metadata serves two purposes: (1) It clearly documents your compression choice so the system can help maintain it, (2) It provides context to anyone reading the document later.

Think of this like setting your writing "tone" in an email client. Once set, it guides how you naturally write.

## Step 3: Write Following Your Compression Level

With metadata set, write your content matching the parameters:

**For σ=0.8 (highly structured)**: Use tables for data, bullet lists for facts, minimal paragraphs

Example for status update:
```
## Accomplished
- [x] Feature implementation - 100% complete
- [x] Testing - 45/50 tests passing
- [x] Documentation - API docs updated

## Metrics
| Metric | Current | Target |
|--------|---------|--------|
| Code coverage | 78% | 80% |
| Test pass rate | 90% | 95% |
```

**For σ=0.4 (less structured)**: Flowing paragraphs with clear sections, prose-first

Example for getting started guide (this document):
```
Document compression is a systematic approach to making your written 
documents shorter and more efficient to read, while keeping all the 
important information intact. Think of it like editing a long email: 
you remove the "fluff" but keep the core message clear.
```

The structure choice is about matching format to content type. Data belongs in tables. Complex reasoning needs prose.

## Step 4: Validate Your Compression

After writing, check that your compression level is actually enforced:

**Check 1: Does format match σ?**
- High σ: Should see lots of tables, lists, structured data
- Low σ: Should read like natural prose with clear narrative flow

**Check 2: Does detail match γ?**
- High γ: Complete sentences with full explanation
- Low γ: Keywords and abbreviations acceptable, assume reader context

**Check 3: Does context match κ?**
- High κ: Multiple headers, explanations of decisions, background provided
- Low κ: Jump to content, assume shared knowledge

## Common Questions

**Q**: What if my document doesn't fit the template exactly?
**A**: Templates are starting points, not strict rules. Adapt them to fit your needs while keeping the compression parameters in mind. The key is consistency: if you choose σ=0.8, maintain that structured format throughout. Templates help you avoid drifting toward verbosity while editing.

**Q**: Can I have different compression levels in different sections?
**A**: Generally no—keep compression consistent throughout a document for readability. However, you can update the parameters if your needs change. For example, if you realize a document needs more context, update κ from 0.2 → 0.5 and adjust subsequent sections.

**Q**: What's the difference between γ (detail) and κ (context)?
**A**: Detail is *what information* you include (facts, metrics, findings). Context is *how much scaffolding* you provide (explanations, headers, rationale). High γ with low κ means you include lots of detail but assume the reader understands the background. High κ with low γ means you include minimal facts but provide lots of context explaining them.

## Next Steps

1. **Choose your first document**: Pick something you need to write (status update, design doc, analysis)
2. **Select a template**: Find the template matching your document type
3. **Customize metadata**: Adjust σ, γ, κ based on your audience and needs
4. **Write following the template**: Let the structure guide your content
5. **Share and iterate**: Get feedback—does the compression work for your audience?

For deeper learning:
- Read "Quick Reference Guide" for all templates and parameter settings
- Study example documents in each template
- Review decision records to understand why certain compression levels work for specific use cases

## Troubleshooting

**Issue**: My document still feels too long even though I'm using high σ
**Solution**: Check your γ setting. If γ is high (0.7+), you're including too much detail. For status updates, aim for γ=0.4 (concise facts only). Reduce explanations, remove context, stick to outcomes and metrics.

**Issue**: The compressed format feels unnatural or rushed
**Solution**: This usually means κ is too low. Readers unfamiliar with your project need more context. Try increasing κ from 0.2 → 0.4. Add brief explanations of decisions and background. Compression shouldn't feel forced—it should be natural communication style.

**Issue**: My readers are confused by the compressed format
**Solution**: Your audience may need higher κ (more scaffolding) or lower σ (less structure). Try adding more section headers (κ) or converting tables back to prose (↓σ). Remember: compression is about being efficient, not cryptic. If readers don't understand it, adjust parameters.

Constraint validation: σ=0.4 (less structured prose) + γ=0.9 (highly detailed) + κ=0.8 (full scaffolding) = 2.1 ≥ 1.3 (new-users + active) ✓
