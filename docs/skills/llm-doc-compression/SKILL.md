---
name: llm-doc-compression
description: Interactive V7 compression coach - guides you through compressing technical docs step-by-step with checkpoints, feedback, and running size totals. Achieves 85% reduction (134KB→22KB) with 95% information retention through structured process.
---

# LLM Documentation Compression Coach

**Version**: 2.0.0 | **Mode**: Interactive Step-by-Step Guidance

## How This Works

I'm your compression coach. I'll guide you through V7 compression in stages:
1. I analyze your document structure
2. We compress section-by-section
3. I check each section's size and quality
4. I give you specific feedback ("compress more" or "good")
5. We track running total toward 22KB target

**You provide**: The document to compress
**I provide**: Step-by-step instructions, checkpoints, feedback

---

## Initial Analysis

When you provide a document, I'll first analyze:
- Document size (KB/lines)
- Section structure
- Sacred content (prompts/code to preserve 100%)
- Target size (typically 19-22KB for 130KB+ docs)
- Compression plan with size budget per section

**Example analysis output**:
```
📊 Document Analysis:
- Size: 134KB, 1,332 lines
- Structure: Exec summary + 10 test sections + conclusion
- Sacred content: 15 test prompts (~6KB) - PRESERVE VERBATIM
- Target: 22KB (84% reduction)

📋 Compression Plan:
1. Exec summary: 1KB (from 3KB)
2. Methodology: 1KB (from 5KB)
3. Tests 1-5: 10KB total (from 60KB)
4. Tests 6-10: 8KB total (from 55KB)
5. Conclusion: 2KB (from 5KB)
```

---

## Step-by-Step Process

After analysis, I'll guide you through each section:

### STEP 1: Executive Summary

**Instructions**:
- Reduce to 3 sentences maximum
- Format: "Assessment of [model] for [purpose]. Findings: [key results]. Conclusion: [recommendation]."
- Delete: All scaffolding, elaboration, background
- Keep: Core finding, main conclusion

**Example**:
❌ Before (verbose, 3KB):
"This report presents a systematic, evidence-based self-assessment of the Gemini 2.5 Pro large language model, with a specific focus on its capacity to execute advanced prompting techniques within a single-shot, non-conversational context..."

✅ After (terse, 0.9KB):
"Systematic assessment: Gemini 2.5 Pro advanced prompting in single-shot execution. Findings: Exceptional on native API features (structured output, grounding, Thinking), strong on emergent capabilities (CoT, Socratic). Conclusion: Highly capable for complex single-shot when leveraging architecture."

**Size check**: Should be ~1KB

**When you provide your compressed version, I'll**:
- Check size (✓ if 0.8-1.2KB, ⚠ if over)
- Check quality (3 sentences? Core info preserved?)
- Give feedback: "Good! 0.9KB ✓" or "Still 2KB - compress to 3 sentences max"

---

### STEP 2: Each Test Section

For each test, I'll guide you through this format:

```
### [N]. [Name]

**Def**: [1 terse sentence]
**Doc**: [✓/✗/⚠ + brief]
**Test**: [Key requirement in 1 line]

**Prompt**:
```
[100% VERBATIM - EVERY WORD EXACT]
```

**Output**: [Key results only - no narration]
**Analysis**: [Fragments, no subjects, keep reasoning]
**Scores**: E=[N]/10 ([full reasoning]), R=[N]/10 ([full reasoning])
```

**For each test section, I'll specify**:

1. **Sacred content** (what to preserve 100%):
   - The entire prompt in code block
   - Any persona descriptions in prompt
   - Technical numbers, calculations

2. **Output compression** (70% reduction):
   - Extract: Final answer, key numbers, proof of success
   - Delete: "Certainly", "Let me", "This means", step narration
   - Keep: All technical accuracy, all numbers
   
   Decision question: "What's minimum text to prove model succeeded?"

3. **Analysis compression** (67% reduction):
   - Delete subjects: "The model" → start with verb
   - Keep reasoning: Why the score? What's the insight?
   - Format: Fragments with → and symbols
   
   Decision question: "What's core insight justifying the score?"

**Size check per test**: ~2KB each (prompts ~0.6KB + output ~0.4KB + analysis ~0.5KB + scores ~0.5KB)

**When you provide compressed test, I'll**:
- ✓ Prompt is 100% verbatim
- ✓ Output has key results
- ✓ Analysis has complete reasoning in fragments
- ✓ Size is ~2KB
- Give specific feedback if any element is wrong

---

### Running Total Tracking

After each section, I'll show:
```
✅ Executive Summary: 0.9KB (target: 1KB) ✓
✅ Methodology: 1.1KB (target: 1KB) ✓
✅ Test 1 (CoT): 2.1KB (target: 2KB) ✓
   Running total: 4.1KB / 22KB target (19% complete)
   
⚠️ Test 2 (Structured Output): 3.5KB (target: 2KB) ⚠️ OVER
   → Compress output section more (currently 1.2KB, should be ~0.4KB)
   Running total: 7.6KB / 22KB (behind pace)
```

This keeps you on track toward the 22KB goal.

---

## Feedback Types

**✓ Good**: Section meets size and quality targets
- "Good! 2.1KB, prompt verbatim, analysis complete ✓"

**⚠ Over**: Section too large, needs more compression
- "⚠ 3.5KB (target: 2KB). Output section verbose - extract key results only"
- I'll specify which part to compress more

**❌ Quality Issue**: Size good but content wrong
- "❌ Prompt altered ('think stepwise' instead of 'think step by step') - must be 100% exact"
- "❌ Analysis missing reasoning for E=10 score - why 10?"

**🎯 On Target**: Running total on pace
- "🎯 Running total: 12KB / 22KB (55% complete, on pace)"

**📊 Final Check**: When complete
- Total size (19-22KB? ✓)
- All prompts verbatim? ✓
- All analysis has reasoning? ✓
- Can reproduce tests? ✓

---

## Example Interaction

**User**: [Provides Gemini assessment, 134KB]

**Me**: 
```
📊 Analysis: 134KB, 1,332L → Target: 22KB, 450L (84% reduction)

Structure:
- Exec summary: 3KB → 1KB
- Methodology: 5KB → 1KB  
- 10 test sections: 115KB → 18KB (~1.8KB each)
- Conclusion: 5KB → 2KB

Sacred content: 15 test prompts (~6KB total) - PRESERVE 100%

Ready to start? I'll guide you section by section with checkpoints.

STEP 1: Compress executive summary to 3 sentences max (~1KB)
```

**User**: [Provides compressed exec summary]

**Me**:
```
✓ Good! 0.9KB, 3 sentences, core findings preserved.

Running total: 0.9KB / 22KB (4%)

STEP 2: Compress methodology section
- Delete: Long explanations of why hybrid approach
- Keep: Key point that it's doc analysis + empirical testing
- Target: ~1KB (currently 5KB)
```

[Continue through document with feedback at each step]

---

## Key Advantages Over Rule-Based Skill

**Old approach** (rule-based):
- Give all rules upfront
- User tries to apply to entire 134KB doc
- No feedback until complete
- Result: 58KB, 61KB (inconsistent, over-target)

**New approach** (coaching):
- Break into small chunks (1-2KB at a time)
- Immediate feedback on each chunk
- Course-correct before moving to next section
- Running total keeps user on track
- Result: Consistent 22KB ✓

---

## What I Need From You

**To start**: Attach your document and say "compress this"

**During process**: 
- Provide compressed version of each section as I request
- If you get stuck, ask "show me an example for this section"
- If feedback unclear, ask "what specifically should I change?"

**My commitment**:
- Clear, specific guidance for each section
- Size checks with explicit targets
- Feedback on what's right and what needs adjustment
- Support until we hit 22KB with 95% retention

---

## Start Now

Ready to compress? Attach your document and I'll begin with the analysis and step 1.
