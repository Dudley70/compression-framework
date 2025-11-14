# LLM Documentation Compression Skill

**Version**: 1.0.0  
**For**: Claude Desktop, Claude.ai, Claude Code, Claude API

---

## What It Does

Compresses technical documentation to maximum density (~85% reduction) while maintaining 100% completeness. Optimized for LLM consumption only.

**Before**: 1,332 lines / 134KB verbose technical doc  
**After**: 481 lines / 22KB dense LLM format  
**Reduction**: 84%, 100% complete

---

## Installation

### Claude Desktop / Claude.ai
1. Download `llm-doc-compression.zip`
2. Settings → Capabilities → Skills → Upload skill
3. Toggle ON

### Claude Code
```bash
cp -r llm-doc-compression ~/.claude/skills/
```

---

## Usage

Natural language requests trigger the skill automatically:

```
"Compress this document for LLM use"
"Apply dense compression to [file]"
"Optimize this doc for LLM consumption"
"Make this LLM-readable and compact"
```

Claude loads skill → applies 10 compression rules → outputs dense version.

---

## What Gets Compressed

**Aggressive** (85% reduction):
- Headers → ultra-terse (Src, L, KB)
- Prose → fragments (no subjects/filler)
- Tables → single-letter headers (E, R, Doc)
- Lists → combined, no numbering
- Scaffolding → removed entirely

**Preserved** (100% verbatim):
- Test prompts
- Code examples
- Schemas
- API parameters
- Commands

---

## Output Characteristics

- **Size**: 19-22KB (natural compression limit)
- **Lines**: 400-450
- **Format**: LLM-only (not human-readable)
- **Completeness**: 100% (all tests reproducible)
- **Symbols**: ✓✗⚠→ throughout
- **Abbreviations**: E/R, CoT, LLM, w/, w/o

---

## Example

### Before
```markdown
The model's performance on this task was exceptional. 
It successfully adopted the Socratic framework and 
demonstrated a sophisticated ability to engage in 
meta-level analysis.
```

### After
```markdown
Exceptional performance. Adopted Socratic framework + 
sophisticated meta-analysis ability.
```

---

## Files

- `SKILL.md` - Main skill (123 lines, compressed)
- `REFERENCE.md` - Complete rules (224 lines, compressed)
- `README.md` - This file

---

## Requirements

- Claude Pro, Max, Team, or Enterprise
- Code execution + file creation enabled
- Skills feature enabled

---

## When to Use

✓ Technical docs for LLM consumption  
✓ Maximum density required  
✓ Must preserve all code/prompts/tests  
✓ Natural limit target (~21KB)

✗ Human readability needed  
✗ Quick summaries wanted  
✗ Simple/non-technical docs

---

## Version History

- v1.0.0 (2025-11-14): Initial release, renamed from v7-compression

---

**Created**: 2025-11-14  
**Project**: Compression Framework  
**Location**: `/Users/dudley/Projects/Compression/docs/skills/llm-doc-compression/`