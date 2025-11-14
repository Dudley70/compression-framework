# V7 Compression Skill

**Version**: 1.0.0  
**Created**: 2025-11-14  
**For**: Claude Desktop, Claude.ai, Claude API

## What This Skill Does

Applies V7 Complete LLM-Optimized compression to technical documentation, achieving 84% reduction while maintaining 100% completeness through aggressive format-only compression.

## Installation

### For Claude Desktop / Claude.ai:
1. Download `v7-compression.zip`
2. Open Claude Desktop or go to claude.ai
3. Navigate to: Settings → Capabilities → Skills
4. Click "Upload skill"
5. Select the `v7-compression.zip` file
6. Toggle the skill ON

### For Claude Code:
```bash
cp -r v7-compression ~/.claude/skills/
```

## Usage

Simply request V7 compression in your conversation:

```
"Apply V7 compression to this document"
"Compress using V7 methodology"
"Use V7 compression skill on [file]"
```

Claude will automatically detect when this skill is needed based on your request.

## What V7 Compression Does

- **Compresses**: Headers, prose, tables, lists, scaffolding
- **Preserves**: Test prompts, code examples, schemas (100% verbatim)
- **Achieves**: ~84% reduction, ~21KB target, 400-450 lines
- **Audience**: LLM consumption only (not human-readable)

## Files in This Skill

- `SKILL.md` - Main skill definition and process
- `REFERENCE.md` - Complete compression rules (336 lines)
- `README.md` - This file

## Requirements

- Claude Pro, Max, Team, or Enterprise plan
- Code execution and file creation enabled in Settings
- Skills feature enabled

## Example

**Input**: 1,332 lines / 134KB technical documentation  
**Output**: 481 lines / 22KB V7 compressed (84% reduction)  
**Completeness**: 100% (all test patterns preserved)

## Support

Created as part of the Compression Framework project.  
Location: `/Users/dudley/Projects/Compression/docs/skills/v7-compression/`

## License

Part of the Compression Framework (Internal Project)