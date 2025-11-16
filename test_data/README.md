# Test Data

This directory contains test documents for validating the compression tool.

## Structure

```
test_data/
├── documents/          # Original test documents
│   └── gemini-self-assessment.md  # Primary test doc (130.9KB, 11 prompts)
├── expected/           # Expected compressed outputs
└── results/            # Actual compression results (gitignored)
```

## Primary Test Document

**gemini-self-assessment.md**
- Original size: 130.9KB
- Test prompts: 11
- Format: Research paper with code-fenced and prose prompts
- Expected compression: ~77% (to 19-24KB target)
- Use case: Validates Rule 6 compliance, compression ratio, structure preservation

## Running Tests

### Quick Validation
```bash
python compress_v7_hybrid.py \
  test_data/documents/gemini-self-assessment.md \
  test_data/results/gemini-compressed.md \
  --api-key $ANTHROPIC_API_KEY \
  --model haiku \
  --expected-prompts 11 \
  --report test_data/results/validation-report.json \
  --verbose
```

### Compare with Previous Results
After compression improvements, compare:
- Size reduction (target: 19-24KB)
- Rule 6 compliance (must be 100%)
- All 11 prompts preserved byte-for-byte

## Adding Test Documents

When adding new test documents:
1. Place original in `documents/`
2. Document stats (size, prompt count, format)
3. Update this README
4. Run baseline compression
5. Save expected results in `expected/`
