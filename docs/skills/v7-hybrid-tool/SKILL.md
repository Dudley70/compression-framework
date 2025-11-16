---
name: v7-hybrid-tool
description: Production-grade V7 compression with guaranteed Rule 6 compliance. Uses hybrid architecture tool that programmatically validates test prompt preservation.
---

# V7 Hybrid Compression Tool

**Version**: 1.0.0 | **Method**: Hybrid Architecture (Deterministic Safety + LLM Intelligence)

## What This Does

I run the production `compress_v7_hybrid.py` tool that **guarantees Rule 6 compliance** through architectural separation of sacred content from LLM processing.

**Key Difference from Manual Compression:**
- ✅ **Guaranteed**: Sacred content extracted before LLM sees it, restored after, validated programmatically
- ✅ **Reliable**: Can't hallucinate success - verification is deterministic
- ✅ **Production-ready**: 35/35 tests passing, validated on 131KB real documents
- ⚠️ **Requires**: Anthropic API key in config file

---

## Prerequisites

**One-time setup required:**

1. **Create config directory:**
   ```bash
   mkdir -p ~/.anthropic
   ```

2. **Save your API key:**
   ```bash
   echo "YOUR_ANTHROPIC_API_KEY" > ~/.anthropic/api_key
   chmod 600 ~/.anthropic/api_key
   ```

3. **Verify setup:**
   ```bash
   cat ~/.anthropic/api_key
   ```

**That's it!** The skill will read the API key from this file automatically.

---

## How It Works

**4-Step Hybrid Pipeline:**

1. **Extract Sacred Content** (Deterministic)
   - Regex extraction of test prompts, code blocks
   - Replaced with placeholders before LLM sees content
   - Sacred content physically separated = can't be modified

2. **LLM Compression** (Intelligent)
   - Simple autonomous compression on remaining content
   - No complex constraints (just "compress for LLM use")
   - LLM does what it does best: semantic compression

3. **Restore Sacred Content** (Deterministic)
   - Replace placeholders with original sacred content
   - Apply 67 V7 transformation rules deterministically
   - Sacred content back, byte-for-byte identical

4. **Validate** (Programmatic)
   - Count prompts (expected vs found)
   - Verify byte-for-byte preservation
   - Check compression ratio
   - FAIL if any check fails (no hallucination possible)

---

## Usage

**Just say:**

```
"Compress this document with V7 hybrid tool"
```

I will:
1. Save your document to temp location
2. Read API key from `~/.anthropic/api_key`
3. Run `compress_v7_hybrid.py` with validation
4. Show you the results and compressed document
5. Report metrics (size reduction, Rule 6 compliance, etc.)

**Optional parameters you can specify:**

- **Model**: "use haiku" (cheap, $0.05/doc) or "use sonnet" (smart, $0.16/doc)
- **Expected prompts**: "expect 5 prompts" (for validation)
- **Verbose**: "show detailed progress"

---

## Execution Protocol

### Step 1: Setup Check

```bash
# Verify API key exists
if [ -f ~/.anthropic/api_key ]; then
  API_KEY=$(cat ~/.anthropic/api_key)
  echo "✅ API key found"
else
  echo "❌ API key not found. Please run setup (see Prerequisites)"
  exit 1
fi

# Verify tool exists
if [ -f /Users/dudley/Projects/Compression/compress_v7_hybrid.py ]; then
  echo "✅ Tool found"
else
  echo "❌ Tool not found at expected location"
  exit 1
fi
```

### Step 2: Save Uploaded Document

```bash
# Create temp directory
TEMP_DIR=$(mktemp -d)
INPUT_FILE="$TEMP_DIR/input.md"

# Save uploaded document content to temp file
# (Claude saves the uploaded document content to this file)

echo "📄 Document saved: $INPUT_FILE"
ls -lh "$INPUT_FILE"
```

### Step 3: Run Compression

```bash
# Set output paths
OUTPUT_FILE="$TEMP_DIR/compressed.md"
REPORT_FILE="$TEMP_DIR/validation-report.json"

# Default model: haiku (cheap)
MODEL=${MODEL:-haiku}

# Run compression with validation
cd /Users/dudley/Projects/Compression

python3 compress_v7_hybrid.py \
  "$INPUT_FILE" \
  "$OUTPUT_FILE" \
  --api-key "$API_KEY" \
  --model "$MODEL" \
  ${EXPECTED_PROMPTS:+--expected-prompts "$EXPECTED_PROMPTS"} \
  --report "$REPORT_FILE" \
  --verbose
```

### Step 4: Parse Results

```bash
# Check if compression succeeded
if [ $? -eq 0 ]; then
  echo "✅ Compression successful"
  
  # Show validation report
  if [ -f "$REPORT_FILE" ]; then
    echo ""
    echo "📊 Validation Report:"
    cat "$REPORT_FILE"
  fi
  
  # Show file sizes
  echo ""
  echo "📏 Size Comparison:"
  echo "  Original:   $(ls -lh "$INPUT_FILE" | awk '{print $5}')"
  echo "  Compressed: $(ls -lh "$OUTPUT_FILE" | awk '{print $5}')"
  
  # Calculate compression ratio
  ORIGINAL_SIZE=$(stat -f%z "$INPUT_FILE")
  COMPRESSED_SIZE=$(stat -f%z "$OUTPUT_FILE")
  REDUCTION=$((100 - (COMPRESSED_SIZE * 100 / ORIGINAL_SIZE)))
  echo "  Reduction:  ${REDUCTION}%"
  
  # Show compressed document
  echo ""
  echo "📄 Compressed Document:"
  cat "$OUTPUT_FILE"
  
else
  echo "❌ Compression failed"
  exit 1
fi
```

### Step 5: Cleanup

```bash
# Keep results in temp directory for user to access
echo ""
echo "💾 Files saved to: $TEMP_DIR"
echo "  - Input:  $INPUT_FILE"
echo "  - Output: $OUTPUT_FILE"
echo "  - Report: $REPORT_FILE"
```

---

## Expected Output

**Example session:**

```
User: "Compress this document with V7 hybrid tool, expect 11 prompts, use haiku"

Claude: 
✅ API key found
✅ Tool found
📄 Document saved: /var/folders/.../input.md (131KB)

Running compression...
[Progress output from tool...]

✅ Compression successful

📊 Validation Report:
{
  "rule_6_compliant": true,
  "prompts_found": 11,
  "prompts_expected": 11,
  "prompts_match": true,
  "original_size": 134144,
  "compressed_size": 31232,
  "compression_ratio": 76.7,
  "validation_passed": true
}

📏 Size Comparison:
  Original:   131KB
  Compressed: 30KB
  Reduction:  77%

📄 Compressed Document:
[Shows compressed content...]

💾 Files saved to: /var/folders/tmp.XXXXX
  - Input:  /var/folders/tmp.XXXXX/input.md
  - Output: /var/folders/tmp.XXXXX/compressed.md
  - Report: /var/folders/tmp.XXXXX/validation-report.json
```

---

## Error Handling

### Missing API Key

```
❌ API key not found at ~/.anthropic/api_key

Setup required:
1. mkdir -p ~/.anthropic
2. echo "YOUR_API_KEY" > ~/.anthropic/api_key
3. chmod 600 ~/.anthropic/api_key

Get your API key at: https://console.anthropic.com/
```

### Invalid API Key

```
❌ Compression failed

Error: API authentication failed
Please verify your API key in ~/.anthropic/api_key
```

### Rule 6 Violation Detected

```
❌ Validation failed: Rule 6 compliance check failed

Expected prompts: 11
Found prompts: 10
Missing: Test #7

This indicates sacred content was not preserved verbatim.
The compressed document cannot be used for test reproduction.

Please report this issue - the tool should guarantee Rule 6 compliance.
```

### Tool Not Found

```
❌ Tool not found at /Users/dudley/Projects/Compression/compress_v7_hybrid.py

The compression tool may not be installed or the path has changed.
Please verify the tool location.
```

---

## Model Selection

**Available models:**

- **haiku** (claude-haiku-4-5): Fast, cheap ($0.05/doc), good quality
- **sonnet** (claude-sonnet-4-5): Slower, expensive ($0.16/doc), best quality

**Recommendation:** Start with haiku. Only use sonnet if haiku's compression isn't sufficient.

**Usage:**
- Default (haiku): "Compress this"
- Explicit: "Compress this with haiku" or "Compress this with sonnet"

---

## Validation Checks

**The tool automatically verifies:**

1. ✅ **Prompt Count**: Expected vs found matches
2. ✅ **Prompt Preservation**: Byte-for-byte identical
3. ✅ **Structure Integrity**: Key sections present
4. ✅ **Compression Ratio**: Within expected range

**If any check fails:**
- Tool returns error
- Validation report shows failure details
- Original document unchanged

**This is the key difference from manual compression:** Validation is programmatic, not LLM-based.

---

## Cost Estimates

**Per document (assuming 130KB input):**

- **Haiku**: ~$0.05 per compression (~35 seconds)
- **Sonnet**: ~$0.16 per compression (~60 seconds)

**For 100 documents:**
- Haiku: ~$5 total
- Sonnet: ~$16 total

---

## Troubleshooting

### "Command not found: python3"

**Solution:** Verify Python 3 is installed:
```bash
which python3
python3 --version
```

If not installed, install via Homebrew:
```bash
brew install python3
```

### "Permission denied: ~/.anthropic/api_key"

**Solution:** Fix file permissions:
```bash
chmod 600 ~/.anthropic/api_key
```

### "Tool output is empty"

**Possible causes:**
1. API rate limit hit
2. Network connectivity issue
3. Invalid API key

**Solution:** Check tool output for error messages, verify API key, check internet connection.

---

## Advantages Over Manual Compression

| Feature | Manual Compression (Skill) | V7 Hybrid Tool |
|---------|---------------------------|----------------|
| Rule 6 Compliance | ❌ Not guaranteed (LLM can fail) | ✅ Guaranteed (architectural) |
| Validation | ❌ LLM self-assessment (unreliable) | ✅ Programmatic (deterministic) |
| Reproducibility | ⚠️ Variable (depends on LLM behavior) | ✅ Consistent (deterministic rules) |
| Speed | ✅ Immediate (no tool setup) | ⚠️ Requires API call (~35s) |
| Cost | ✅ Free (uses conversation tokens) | ⚠️ $0.05-0.16 per doc |
| Setup | ✅ None | ⚠️ One-time (API key config) |

**Use manual compression for:** Quick, casual use when Rule 6 isn't critical

**Use V7 hybrid tool for:** Production use where test prompts must be preserved exactly

---

## Example: Real Document Test

**Input:** Gemini Self-Assessment (131KB, 11 test prompts)

**Command:**
```
"Compress the Gemini document with V7 hybrid tool, expect 11 prompts, use haiku, show verbose output"
```

**Expected Results:**
- ✅ All 11 prompts preserved byte-for-byte
- ✅ Compression: 131KB → ~20-30KB (77-85% reduction)
- ✅ Rule 6 compliance: VERIFIED
- ✅ Cost: ~$0.05
- ✅ Time: ~35 seconds

---

## Ready to Use

**To compress a document:**

1. Upload your markdown document to Claude Desktop
2. Say: "Compress this with V7 hybrid tool"
3. I'll run the tool and show you results

**First time?** Make sure you've completed the Prerequisites (API key setup).

**Questions about the tool?** Ask me to explain any part of the process.
