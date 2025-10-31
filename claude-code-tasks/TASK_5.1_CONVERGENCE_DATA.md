# Task: Convergence Data Gathering - Automated Empirical Testing

**Task ID**: TASK-5.1-CONVERGENCE-DATA
**Created**: 2025-11-01
**Priority**: HIGH
**Type**: Automated Testing & Data Gathering
**Estimated Duration**: 4-6 hours
**Dependencies**: Task 4.1 FIX (complete), compress.py (production-ready)

---

## Objective

Generate comprehensive empirical data about compression convergence behavior through volume-based automated testing. Execute 960+ compression tests across multiple dimensions to identify convergence patterns, technique behaviors, and stability characteristics. This provides the data foundation for answering the intrinsic stability question.

---

## Background Context

### The Core Question
**User's Question**: "Does compression have natural convergence (like solving an equation) rather than requiring artificial safety blocks?"

**Example Analogy**:
```
2x + 5 = 15  (original)
→ 2x = 10    (simplified)
→ x = 5      (solved)
→ x = 5      (already solved, nothing more to do)
```

**Applied to Compression**:
- Round 1: Compress verbose document
- Round 2: Compress the compressed result
- Round 3: Compress again
- **Question**: Does it stabilize naturally (intrinsic) or need safety blocks (extrinsic)?

### Current Understanding
From Task 4.1 validation (validation_report_task_4.1_fixed.md):
- Tool is production-ready with 4-layer safety system
- All 5 LSC techniques operational
- Conservative safety blocks prevent re-compression
- **Unknown**: Would techniques stabilize WITHOUT safety blocks?

### What We Need to Learn
1. **Convergence curves**: Shape of tokens(round_n) over 20 rounds
2. **Technique behavior**: Do different techniques converge differently?
3. **Combination effects**: How do techniques interact?
4. **Safety necessity**: What happens with safety disabled? (careful)
5. **Document sensitivity**: Does initial state affect convergence?

---

## Test Matrix Design

### Dimensions
1. **Documents** (5): 
   - verbose_prose.md (score 0.228)
   - already_compressed.md (score 0.770)
   - mixed_state.md (mixed sections)
   - entity_heavy.md (technical terms)
   - semantic_test.md (security requirements)

2. **Techniques** (6):
   - lists_tables (individual)
   - hierarchical_structure (individual)
   - remove_redundancy (individual)
   - technical_shorthand (individual)
   - information_density (individual)
   - all_combined (full pipeline)

3. **Rounds** (20): Apply compression iteratively

4. **Safety Modes** (2):
   - safety_enabled (baseline)
   - safety_disabled (convergence test - CAREFUL)

**Total Tests**: 5 docs × 6 techniques × 20 rounds × 2 safety = **1,200 compression operations**

---

## Implementation Plan

### Phase 1: Test Infrastructure (Checkpoint 1) - 1.5 hours

**Objective**: Build test harness with TDD validation

**Step 1.1: Create Test Framework (30 minutes)**

Create `scripts/test_convergence.py`:
```python
"""
Convergence testing harness for LSC compression techniques.
Generates empirical data for pattern analysis.
"""

import json
import tiktoken
from pathlib import Path
from datetime import datetime
from compress import CompressionTool

class ConvergenceTester:
    """Automated convergence testing with comprehensive data collection"""
    
    def __init__(self, output_dir="convergence_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.encoder = tiktoken.encoding_for_model("gpt-4")
    
    def run_test_matrix(self):
        """Execute full test matrix: 1200 tests"""
        results = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_tests": 1200,
                "documents": 5,
                "techniques": 6,
                "max_rounds": 20,
                "safety_modes": 2
            },
            "tests": []
        }
        
        for doc_path in self.get_test_documents():
            for technique in self.get_techniques():
                # Test with safety enabled
                results["tests"].append(
                    self.test_convergence(doc_path, technique, safety=True)
                )
                # Test with safety disabled (ISOLATED)
                results["tests"].append(
                    self.test_convergence(doc_path, technique, safety=False)
                )
        
        return results
    
    def test_convergence(self, doc_path, technique, safety, max_rounds=20):
        """
        Run convergence test: compress same document repeatedly.
        Track token counts, detect convergence, measure stability.
        """
        original_text = Path(doc_path).read_text()
        original_tokens = len(self.encoder.encode(original_text))
        
        trajectory = {
            "document": doc_path.name,
            "technique": technique,
            "safety_enabled": safety,
            "original_tokens": original_tokens,
            "rounds": []
        }
        
        current_text = original_text
        previous_hash = None
        
        for round_num in range(max_rounds):
            # Apply compression
            if technique == "all_combined":
                compressed = self.compress_full_pipeline(current_text, safety)
            else:
                compressed = self.compress_single_technique(current_text, technique, safety)
            
            # Measure
            tokens = len(self.encoder.encode(compressed))
            content_hash = hash(compressed)
            
            round_data = {
                "round": round_num,
                "tokens": tokens,
                "chars": len(compressed),
                "ratio_to_original": tokens / original_tokens,
                "ratio_to_previous": tokens / len(self.encoder.encode(current_text)),
                "identical_to_previous": (content_hash == previous_hash),
                "content_hash": content_hash
            }
            
            trajectory["rounds"].append(round_data)
            
            # Check convergence
            if round_data["identical_to_previous"]:
                trajectory["converged_at_round"] = round_num
                trajectory["final_tokens"] = tokens
                trajectory["total_reduction"] = 1 - (tokens / original_tokens)
                break
            
            current_text = compressed
            previous_hash = content_hash
        
        # If never converged
        if "converged_at_round" not in trajectory:
            trajectory["converged"] = False
            trajectory["final_tokens"] = trajectory["rounds"][-1]["tokens"]
            trajectory["total_reduction"] = 1 - (trajectory["final_tokens"] / original_tokens)
        else:
            trajectory["converged"] = True
        
        return trajectory
    
    def compress_full_pipeline(self, text, safety_enabled):
        """Apply all LSC techniques in sequence"""
        # Implementation will use compress.py
        pass
    
    def compress_single_technique(self, text, technique, safety_enabled):
        """Apply single LSC technique"""
        # Implementation will use compress.py technique methods
        pass
    
    def get_test_documents(self):
        """Return test document paths"""
        fixtures = Path("tests/fixtures")
        return [
            fixtures / "verbose_prose.md",
            fixtures / "already_compressed.md",
            fixtures / "mixed_state.md",
            fixtures / "entity_heavy.md",
            fixtures / "semantic_test.md"
        ]
    
    def get_techniques(self):
        """Return technique names"""
        return [
            "lists_tables",
            "hierarchical_structure", 
            "remove_redundancy",
            "technical_shorthand",
            "information_density",
            "all_combined"
        ]
```

**Step 1.2: Create Validation Tests (30 minutes)**

Create `tests/test_convergence_harness.py`:
```python
"""Tests for convergence testing infrastructure"""

import pytest
from pathlib import Path
from scripts.test_convergence import ConvergenceTester

class TestConvergenceInfrastructure:
    """Validate test harness before running full suite"""
    
    def test_harness_initialization(self):
        """Test harness creates output directory"""
        tester = ConvergenceTester(output_dir="test_output")
        assert tester.output_dir.exists()
    
    def test_single_convergence_test(self):
        """Test single document + technique convergence"""
        tester = ConvergenceTester()
        doc = Path("tests/fixtures/verbose_prose.md")
        
        result = tester.test_convergence(doc, "lists_tables", safety=True, max_rounds=5)
        
        # Validate result structure
        assert "document" in result
        assert "technique" in result
        assert "safety_enabled" in result
        assert "rounds" in result
        assert len(result["rounds"]) <= 5
        assert "converged" in result
    
    def test_convergence_detection(self):
        """Test that convergence is detected correctly"""
        tester = ConvergenceTester()
        doc = Path("tests/fixtures/already_compressed.md")
        
        result = tester.test_convergence(doc, "all_combined", safety=True, max_rounds=3)
        
        # Already compressed should converge immediately or round 1
        assert result.get("converged", False) or result["rounds"][0]["identical_to_previous"]
    
    def test_token_counting_accuracy(self):
        """Test token counting is consistent"""
        tester = ConvergenceTester()
        test_text = "This is a test document with some content."
        
        tokens1 = len(tester.encoder.encode(test_text))
        tokens2 = len(tester.encoder.encode(test_text))
        
        assert tokens1 == tokens2  # Deterministic
        assert tokens1 > 0
    
    def test_technique_list_complete(self):
        """Test all techniques are available"""
        tester = ConvergenceTester()
        techniques = tester.get_techniques()
        
        assert len(techniques) == 6
        assert "lists_tables" in techniques
        assert "all_combined" in techniques
    
    def test_document_list_valid(self):
        """Test all test documents exist"""
        tester = ConvergenceTester()
        docs = tester.get_test_documents()
        
        assert len(docs) == 5
        for doc in docs:
            assert doc.exists(), f"Missing test document: {doc}"
```

**Step 1.3: Implement Core Methods (30 minutes)**

Implement compression methods in test_convergence.py:
- `compress_full_pipeline()` - Use compress.py tool
- `compress_single_technique()` - Call individual LSC methods
- Handle safety_enabled parameter properly

**Checkpoint 1 Validation**:
```bash
pytest tests/test_convergence_harness.py -v
```

**Expected**: All infrastructure tests pass (6/6)

**Deliverable**: `checkpoint_1_infrastructure.md`
- Infrastructure tests passing
- Code structure validated
- Ready for full test execution

---

### Phase 2: Full Test Execution (Checkpoint 2) - 2-3 hours

**Objective**: Run complete test matrix and generate data files

**Step 2.1: Execute Test Suite (1.5-2 hours)**

Run full convergence testing:
```bash
python scripts/test_convergence.py
```

Expected output:
```
Starting convergence test suite...
Test matrix: 5 docs × 6 techniques × 20 rounds × 2 safety = 1200 tests
Estimated time: 30-60 minutes

Progress: [====================] 1200/1200 tests
Testing complete!
Total tests run: 1200
Converged: 487 (40.6%)
Never converged: 713 (59.4%)

Results saved to convergence_results/
  - convergence_data_20251101_143022.json
  - convergence_curves_20251101_143022.csv
  - convergence_summary_20251101_143022.md
```

**Step 2.2: Data Export (30 minutes)**

Implement export methods:

1. **JSON Export** (complete data):
```python
def save_json(self, results, path):
    """Save complete results as JSON"""
    with open(path, 'w') as f:
        json.dump(results, f, indent=2)
```

2. **CSV Export** (for plotting):
```python
def save_csv(self, results, path):
    """Export as CSV for easy plotting"""
    import csv
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "document", "technique", "safety", 
            "round", "tokens", "ratio_to_original",
            "converged"
        ])
        for test in results["tests"]:
            for round_data in test["rounds"]:
                writer.writerow([
                    test["document"],
                    test["technique"],
                    test["safety_enabled"],
                    round_data["round"],
                    round_data["tokens"],
                    round_data["ratio_to_original"],
                    test.get("converged", False)
                ])
```

3. **Markdown Summary**:
```python
def generate_summary(self, results, path):
    """Generate human-readable summary report"""
    # Calculate statistics
    total = len(results["tests"])
    converged = sum(1 for t in results["tests"] if t.get("converged"))
    
    # Group by technique
    by_technique = {}
    for test in results["tests"]:
        tech = test["technique"]
        if tech not in by_technique:
            by_technique[tech] = []
        by_technique[tech].append(test)
    
    # Write markdown
    with open(path, 'w') as f:
        f.write("# Convergence Testing Summary\n\n")
        f.write(f"**Total Tests**: {total}\n")
        f.write(f"**Converged**: {converged} ({converged/total:.1%})\n\n")
        
        f.write("## By Technique\n\n")
        for tech, tests in by_technique.items():
            conv = sum(1 for t in tests if t.get("converged"))
            f.write(f"### {tech}\n")
            f.write(f"- Tests: {len(tests)}\n")
            f.write(f"- Converged: {conv} ({conv/len(tests):.1%})\n")
            f.write(f"- Avg rounds: {self.avg_rounds(tests):.1f}\n\n")
```

**Step 2.3: Validate Data Quality (30 minutes)**

Create validation tests for output data:
```python
def test_json_output_structure():
    """Validate JSON output has correct structure"""
    result_file = Path("convergence_results").glob("convergence_data_*.json")
    data = json.load(open(next(result_file)))
    
    assert "metadata" in data
    assert "tests" in data
    assert len(data["tests"]) == 1200
    
def test_csv_output_completeness():
    """Validate CSV has all expected rows"""
    csv_file = Path("convergence_results").glob("convergence_curves_*.csv")
    import csv
    rows = list(csv.reader(open(next(csv_file))))
    
    # Header + data rows (varies based on convergence)
    assert len(rows) > 1200  # At least 1 row per test
    assert rows[0] == ["document", "technique", "safety", "round", "tokens", "ratio_to_original", "converged"]

def test_summary_generated():
    """Validate summary markdown exists and has content"""
    summary_file = Path("convergence_results").glob("convergence_summary_*.md")
    summary = open(next(summary_file)).read()
    
    assert "# Convergence Testing Summary" in summary
    assert "Total Tests" in summary
    assert len(summary) > 500  # Should have substantial content
```

**Checkpoint 2 Validation**:
```bash
pytest tests/test_convergence_data.py -v
```

**Expected**: All data validation tests pass

**Deliverable**: `checkpoint_2_data_generated.md`
- All 1200 tests executed successfully
- 3 output files generated (JSON, CSV, Markdown)
- Data quality validated
- No crashes or errors

---

### Phase 3: Pattern Analysis (Checkpoint 3) - 1-2 hours

**Objective**: Automated pattern detection and statistical analysis

**Step 3.1: Convergence Pattern Detection (45 minutes)**

Implement pattern analysis:
```python
class ConvergenceAnalyzer:
    """Automated pattern detection in convergence data"""
    
    def analyze_convergence_curves(self, results):
        """Identify curve types and convergence patterns"""
        analysis = {
            "overall_statistics": self.overall_stats(results),
            "technique_analysis": self.by_technique_analysis(results),
            "document_analysis": self.by_document_analysis(results),
            "safety_comparison": self.safety_impact_analysis(results),
            "curve_classifications": self.classify_curves(results)
        }
        return analysis
    
    def classify_curves(self, results):
        """
        Classify convergence curve types:
        - instant: Converges in round 0-1
        - fast: Converges in rounds 2-5
        - gradual: Converges in rounds 6-15
        - slow: Converges after round 15
        - divergent: Never converges
        """
        classifications = {
            "instant": [],
            "fast": [],
            "gradual": [],
            "slow": [],
            "divergent": []
        }
        
        for test in results["tests"]:
            if not test.get("converged"):
                classifications["divergent"].append(test)
            else:
                rounds = test["converged_at_round"]
                if rounds <= 1:
                    classifications["instant"].append(test)
                elif rounds <= 5:
                    classifications["fast"].append(test)
                elif rounds <= 15:
                    classifications["gradual"].append(test)
                else:
                    classifications["slow"].append(test)
        
        return classifications
    
    def by_technique_analysis(self, results):
        """Analyze each technique's behavior"""
        by_tech = {}
        
        for tech in ["lists_tables", "hierarchical_structure", "remove_redundancy", 
                     "technical_shorthand", "information_density", "all_combined"]:
            tech_tests = [t for t in results["tests"] if t["technique"] == tech]
            
            by_tech[tech] = {
                "total_tests": len(tech_tests),
                "convergence_rate": sum(1 for t in tech_tests if t.get("converged")) / len(tech_tests),
                "avg_rounds_to_converge": self.avg_convergence_rounds(tech_tests),
                "avg_final_reduction": self.avg_reduction(tech_tests),
                "safety_enabled_convergence": self.convergence_rate_with_safety(tech_tests, True),
                "safety_disabled_convergence": self.convergence_rate_with_safety(tech_tests, False)
            }
        
        return by_tech
    
    def safety_impact_analysis(self, results):
        """Compare safety-enabled vs safety-disabled results"""
        enabled = [t for t in results["tests"] if t["safety_enabled"]]
        disabled = [t for t in results["tests"] if not t["safety_enabled"]]
        
        return {
            "safety_enabled": {
                "tests": len(enabled),
                "convergence_rate": sum(1 for t in enabled if t.get("converged")) / len(enabled),
                "avg_rounds": self.avg_convergence_rounds(enabled),
                "avg_reduction": self.avg_reduction(enabled)
            },
            "safety_disabled": {
                "tests": len(disabled),
                "convergence_rate": sum(1 for t in disabled if t.get("converged")) / len(disabled),
                "avg_rounds": self.avg_convergence_rounds(disabled),
                "avg_reduction": self.avg_reduction(disabled)
            },
            "comparison": {
                "convergence_diff": "calculated difference",
                "rounds_diff": "calculated difference",
                "reduction_diff": "calculated difference"
            }
        }
```

**Step 3.2: Generate Analysis Report (45 minutes)**

Create comprehensive analysis markdown:
```markdown
# Convergence Analysis Report

## Executive Summary
- Total tests: 1200
- Overall convergence rate: X%
- Average rounds to convergence: Y
- Safety impact: Z% difference

## Technique Comparison

### lists_tables
- Convergence rate: X%
- Average rounds: Y
- Curve type: [instant/fast/gradual/slow/divergent]
- Safety impact: [significant/moderate/minimal]

[... for each technique ...]

## Convergence Curve Classification

### Instant Convergence (0-1 rounds)
- Count: X tests
- Techniques: [list]
- Documents: [list]

### Fast Convergence (2-5 rounds)
- Count: X tests
- Techniques: [list]
- Documents: [list]

[... etc ...]

## Safety System Impact

### With Safety Enabled
- Convergence rate: X%
- Avg rounds: Y
- Avg reduction: Z%

### With Safety Disabled
- Convergence rate: X%
- Avg rounds: Y
- Avg reduction: Z%

### Key Findings
- [Does safety prevent convergence?]
- [Do results differ significantly?]
- [Is safety necessary for stability?]

## Document-Specific Patterns

[Analysis of how different document types behave]

## Recommendations for Further Investigation

[What patterns warrant interactive analysis]
```

**Checkpoint 3 Validation**:

Create meta-tests for analysis quality:
```python
def test_analysis_completeness():
    """Validate analysis covers all required dimensions"""
    analysis_file = Path("convergence_results").glob("analysis_report_*.md")
    content = open(next(analysis_file)).read()
    
    # Must have all sections
    assert "Executive Summary" in content
    assert "Technique Comparison" in content
    assert "Safety System Impact" in content
    assert len(content) > 2000  # Substantial analysis

def test_all_techniques_analyzed():
    """Validate all 6 techniques are analyzed"""
    analysis_file = Path("convergence_results").glob("analysis_report_*.md")
    content = open(next(analysis_file)).read()
    
    techniques = ["lists_tables", "hierarchical_structure", "remove_redundancy",
                  "technical_shorthand", "information_density", "all_combined"]
    for tech in techniques:
        assert tech in content
```

**Deliverable**: `checkpoint_3_analysis_complete.md`
- Pattern analysis executed
- Analysis report generated
- All techniques analyzed
- Safety comparison completed

---

## Safety Protocol for Safety-Disabled Tests

**CRITICAL**: Safety-disabled tests require careful handling

### Execution Safety
1. Run safety-enabled tests first (validate baseline)
2. Review safety-enabled results before proceeding
3. Safety-disabled tests run in ISOLATED mode
4. All outputs saved for manual review
5. NO automatic decisions based on safety-disabled results

### Data Handling
```python
def run_safety_disabled_tests_with_review(self):
    """Execute safety-disabled tests with review protocol"""
    print("⚠️  WARNING: Running tests with safety disabled")
    print("All outputs will be saved for manual review")
    print("DO NOT use results without human verification")
    
    # Run tests
    disabled_results = []
    for test in self.tests:
        result = self.test_convergence(test, safety=False)
        disabled_results.append(result)
        
        # Save each result immediately
        self.save_for_review(result, f"review_{test['id']}.md")
    
    # Generate review summary
    self.generate_review_summary(disabled_results)
    
    print("\n✅ Safety-disabled tests complete")
    print(f"📁 Results saved to: convergence_results/safety_disabled_review/")
    print("⚠️  REQUIRES MANUAL REVIEW before analysis")
```

### Review Checklist
For each safety-disabled result:
- [ ] Does content make semantic sense?
- [ ] Are key facts preserved?
- [ ] Is there progressive degradation?
- [ ] Does it differ from safety-enabled?
- [ ] Is convergence genuine or artifact?

---

## Success Criteria

### Phase 1: Infrastructure ✅
- [ ] Test harness implemented
- [ ] Infrastructure tests pass (6/6)
- [ ] Can run single convergence test
- [ ] Token counting accurate

### Phase 2: Data Gathering ✅
- [ ] All 1200 tests execute successfully
- [ ] JSON output complete (1200 test results)
- [ ] CSV output formatted for plotting
- [ ] Markdown summary generated
- [ ] No crashes or errors
- [ ] Data validation tests pass

### Phase 3: Analysis ✅
- [ ] Pattern analysis executed
- [ ] All techniques analyzed
- [ ] Safety comparison completed
- [ ] Curve types classified
- [ ] Analysis report generated
- [ ] Analysis quality tests pass

### Overall Success ✅
- [ ] Complete dataset available
- [ ] Multiple output formats
- [ ] Automated pattern detection
- [ ] Ready for interactive analysis
- [ ] Safety-disabled data flagged for review

---

## Deliverables

### Code
1. `scripts/test_convergence.py` (500-700 lines)
   - ConvergenceTester class
   - ConvergenceAnalyzer class
   - Main execution logic

2. `tests/test_convergence_harness.py` (200-300 lines)
   - Infrastructure tests
   - Data validation tests
   - Analysis quality tests

### Data Files (in convergence_results/)
3. `convergence_data_TIMESTAMP.json` - Complete raw data (1200 tests)
4. `convergence_curves_TIMESTAMP.csv` - Plotting data
5. `convergence_summary_TIMESTAMP.md` - Summary statistics
6. `analysis_report_TIMESTAMP.md` - Pattern analysis
7. `safety_disabled_review/` - Safety-disabled results (flagged)

### Checkpoint Reports
8. `checkpoint_1_infrastructure.md` - Phase 1 validation
9. `checkpoint_2_data_generated.md` - Phase 2 completion
10. `checkpoint_3_analysis_complete.md` - Phase 3 results

### Final Report
11. `convergence_testing_results.md` - Complete summary with:
    - Test execution summary
    - Data quality assessment
    - Pattern detection findings
    - Safety comparison results
    - Recommendations for interactive analysis
    - Open questions requiring human interpretation

---

## Testing Requirements

### TDD Approach
1. Write infrastructure tests FIRST
2. Implement to make tests pass
3. Validate at each checkpoint
4. Test data quality after generation
5. Validate analysis completeness

### Test Coverage
- Infrastructure: 6 tests minimum
- Data validation: 5 tests minimum
- Analysis quality: 3 tests minimum
- Total: 14+ tests, all passing

---

## Timeline

**Phase 1**: 1.5 hours (Infrastructure)
**Phase 2**: 2-3 hours (Data gathering + validation)
**Phase 3**: 1-2 hours (Pattern analysis)
**Total**: 4-6 hours

---

## Context References

### Validation Results
- `validation_report_task_4.1_fixed.md` - Tool validation
- `empirical_validation_results.md` - Initial compression data
- `compress.py` - Production-ready compression tool (862 lines)

### Test Fixtures
- `tests/fixtures/verbose_prose.md` - Score 0.228
- `tests/fixtures/already_compressed.md` - Score 0.770
- `tests/fixtures/mixed_state.md` - Mixed compression states
- `tests/fixtures/entity_heavy.md` - Technical entities
- `tests/fixtures/semantic_test.md` - Security requirements

### LSC Techniques (5 total in compress.py)
1. lists_tables - Convert enumerations to lists
2. hierarchical_structure - Add headers
3. remove_redundancy - Eliminate repetition
4. technical_shorthand - Abbreviate terms
5. information_density - Combine techniques

---

## Expected Outcomes

### If Intrinsic Stability Exists
- Curves flatten quickly (exponential decay)
- Safety-disabled results similar to safety-enabled
- Techniques converge in 1-3 rounds
- No progressive degradation

### If Extrinsic Blocking Required
- Curves continue descending without flattening
- Safety-disabled shows degradation
- Techniques never stabilize
- Progressive information loss

### Hybrid (Most Likely)
- Some techniques intrinsically stable (instant convergence)
- Others require safety blocks (slow/no convergence)
- Document-dependent behavior
- Technique-specific patterns

---

## Notes

**This task provides DATA, not ANSWERS**. The automated testing generates empirical evidence. Human analysis (interactive) will interpret patterns and answer the intrinsic stability question.

**Safety Priority**: All safety-disabled results MUST be reviewed manually before drawing conclusions. Do not trust automated analysis of potentially unsafe compression.

**Success = Good Data**: If this task delivers clean, comprehensive data in usable formats, it succeeds even if patterns aren't immediately clear. The interactive analysis phase will extract insights.

---

## Post-Task: Interactive Analysis Session

After task completion, human + Claude will:
1. Review generated data files
2. Plot convergence curves
3. Identify patterns visually
4. Compare safety-enabled vs disabled
5. Answer intrinsic stability question
6. Document findings for white paper

**Estimated Interactive Time**: 1-2 hours