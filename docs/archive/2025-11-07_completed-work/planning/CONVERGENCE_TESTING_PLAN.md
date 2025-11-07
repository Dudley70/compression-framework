# Convergence Testing Plan - Volume-Based Automated Data Gathering

**Created**: 2025-11-01
**Purpose**: Automated empirical testing to identify compression convergence patterns
**Approach**: HYBRID - Automated data gathering + Interactive analysis

---

## Objective

Generate comprehensive empirical data about compression convergence behavior through volume-based automated testing. Answer quantitative questions about compression curves, technique interactions, and convergence properties.

---

## Key Research Questions (Data-Driven)

### 1. Convergence Curves
- **Question**: What shape is the compression curve? (exponential decay, linear, step function, instant convergence?)
- **Test**: Plot tokens(round_n) for n=0..20
- **Expectation**: If intrinsic stability exists, curve should flatten (asymptotic)

### 2. Technique-Specific Behavior
- **Question**: Do different techniques have different convergence speeds?
- **Test**: Run each LSC technique in isolation for 20 rounds
- **Expectation**: Some techniques may be naturally idempotent (instant convergence), others progressive

### 3. Combination Effects
- **Question**: Do techniques interfere with or complement each other?
- **Test**: Compare sequential application in different orders
- **Expectation**: If truly idempotent, order shouldn't matter at convergence

### 4. Document Type Sensitivity
- **Question**: Does initial compression score affect convergence behavior?
- **Test**: Test on verbose (0.2), medium (0.5), compressed (0.8) documents
- **Expectation**: Different starting points may have different convergence trajectories

### 5. Safety Block Necessity
- **Question**: What happens without safety blocks? (CAREFUL)
- **Test**: Compare with/without safety enabled (isolated, reviewed)
- **Expectation**: If intrinsic stability, results should be similar; if extrinsic required, divergence/degradation

---

## Test Matrix Design

### Dimensions
1. **Documents** (4): verbose_prose.md, already_compressed.md, mixed_state.md, code-heavy fixture
2. **Techniques** (6): Each of 5 LSC + All Combined
3. **Rounds** (20): Compress same document repeatedly
4. **Safety** (2): Enabled vs Disabled (Disabled = isolated review)

**Total Combinations**: 4 docs × 6 techniques × 20 rounds × 2 safety = **960 data points**

---

## Test Implementation Design

### Script Structure: `scripts/test_convergence.py`

```python
"""
Automated convergence testing for LSC techniques.
Generates comprehensive empirical data for pattern analysis.
"""

import json
import tiktoken
from pathlib import Path
from compress import CompressionTool, LSC_TECHNIQUES
from datetime import datetime

class ConvergenceTestHarness:
    """Automated testing for compression convergence behavior"""
    
    def __init__(self, output_dir="convergence_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.encoder = tiktoken.encoding_for_model("gpt-4")
        
    def run_full_suite(self):
        """Execute complete test matrix"""
        results = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_tests": 960,
                "test_matrix": {
                    "documents": 4,
                    "techniques": 6,
                    "rounds": 20,
                    "safety_modes": 2
                }
            },
            "tests": []
        }
        
        # Test each document
        for doc in self.get_test_documents():
            # Test each technique
            for technique in self.get_techniques():
                # Test with safety enabled
                results["tests"].append(
                    self.test_convergence(doc, technique, safety=True)
                )
                # Test with safety disabled (ISOLATED)
                results["tests"].append(
                    self.test_convergence(doc, technique, safety=False)
                )
        
        # Save comprehensive results
        self.save_results(results)
        return results
    
    def test_convergence(self, document_path, technique, safety, max_rounds=20):
        """
        Test convergence for single document + technique + safety combination.
        Returns detailed trajectory data.
        """
        original = Path(document_path).read_text()
        
        trajectory = {
            "document": document_path.name,
            "technique": technique,
            "safety_enabled": safety,
            "rounds": []
        }
        
        current = original
        for round_num in range(max_rounds):
            # Apply compression
            compressed = self.apply_technique(current, technique, safety)
            
            # Measure everything
            round_data = {
                "round": round_num,
                "tokens": len(self.encoder.encode(compressed)),
                "chars": len(compressed),
                "compression_ratio": len(compressed) / len(original),
                "identical_to_previous": (compressed == current),
                "content_hash": hash(compressed),
                "technique_applied": technique,
                "safety_decision": None  # Populated if safety blocked
            }
            
            trajectory["rounds"].append(round_data)
            
            # Check convergence
            if round_data["identical_to_previous"]:
                trajectory["converged_at_round"] = round_num
                trajectory["convergence_type"] = "stable"
                break
            
            current = compressed
        
        # Post-processing
        trajectory["final_tokens"] = trajectory["rounds"][-1]["tokens"]
        trajectory["initial_tokens"] = trajectory["rounds"][0]["tokens"]
        trajectory["total_reduction"] = 1 - (trajectory["final_tokens"] / trajectory["initial_tokens"])
        trajectory["converged"] = "converged_at_round" in trajectory
        
        return trajectory
    
    def apply_technique(self, text, technique_name, safety_enabled):
        """Apply single LSC technique or all combined"""
        if technique_name == "all_combined":
            tool = CompressionTool(safety_enabled=safety_enabled)
            return tool.compress(text)
        else:
            # Apply single technique
            tool = CompressionTool(safety_enabled=safety_enabled)
            return tool.apply_single_technique(text, technique_name)
    
    def get_test_documents(self):
        """Return list of test document paths"""
        fixtures = Path("tests/fixtures")
        return [
            fixtures / "verbose_prose.md",
            fixtures / "already_compressed.md",
            fixtures / "mixed_state.md",
            fixtures / "code_heavy.md"  # May need to create
        ]
    
    def get_techniques(self):
        """Return list of techniques to test"""
        return [
            "lists_tables",
            "hierarchical_structure",
            "remove_redundancy",
            "technical_shorthand",
            "information_density",
            "all_combined"
        ]
    
    def analyze_convergence_patterns(self, results):
        """
        Post-processing analysis to identify patterns.
        This generates summary statistics and pattern detection.
        """
        analysis = {
            "convergence_summary": {
                "total_tests": len(results["tests"]),
                "converged_count": sum(1 for t in results["tests"] if t.get("converged")),
                "convergence_rate": 0.0
            },
            "technique_comparison": {},
            "document_comparison": {},
            "safety_impact": {}
        }
        
        # Group by technique
        by_technique = {}
        for test in results["tests"]:
            tech = test["technique"]
            if tech not in by_technique:
                by_technique[tech] = []
            by_technique[tech].append(test)
        
        # Analyze each technique
        for tech, tests in by_technique.items():
            analysis["technique_comparison"][tech] = {
                "avg_rounds_to_convergence": self.avg_convergence_rounds(tests),
                "convergence_rate": sum(1 for t in tests if t.get("converged")) / len(tests),
                "avg_final_reduction": self.avg_reduction(tests),
                "curve_type": self.identify_curve_type(tests)
            }
        
        return analysis
    
    def save_results(self, results):
        """Save results to multiple formats for analysis"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON (complete data)
        json_path = self.output_dir / f"convergence_data_{timestamp}.json"
        with open(json_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        # CSV (for plotting)
        csv_path = self.output_dir / f"convergence_curves_{timestamp}.csv"
        self.export_to_csv(results, csv_path)
        
        # Markdown summary
        md_path = self.output_dir / f"convergence_summary_{timestamp}.md"
        self.generate_summary_report(results, md_path)
        
        print(f"Results saved to {self.output_dir}/")
        print(f"  - JSON: {json_path.name}")
        print(f"  - CSV: {csv_path.name}")
        print(f"  - Summary: {md_path.name}")


def main():
    """Execute convergence testing suite"""
    harness = ConvergenceTestHarness()
    
    print("Starting convergence test suite...")
    print("Test matrix: 4 docs × 6 techniques × 20 rounds × 2 safety modes = 960 tests")
    print("Estimated time: 30-60 minutes")
    print()
    
    results = harness.run_full_suite()
    
    print()
    print("Testing complete!")
    print(f"Total tests run: {len(results['tests'])}")
    print(f"Results saved to convergence_results/")
    
    # Run analysis
    analysis = harness.analyze_convergence_patterns(results)
    print()
    print("Pattern Analysis:")
    print(f"  Overall convergence rate: {analysis['convergence_summary']['convergence_rate']:.1%}")
    print(f"  Techniques analyzed: {len(analysis['technique_comparison'])}")


if __name__ == "__main__":
    main()
```

---

## Deliverables (Automated)

### 1. Raw Data (`convergence_data_TIMESTAMP.json`)
Complete dataset with all 960 test runs:
- Token counts per round
- Compression ratios
- Convergence detection
- Safety decisions

### 2. Plotting Data (`convergence_curves_TIMESTAMP.csv`)
Format for easy visualization:
```
document,technique,safety,round,tokens,compression_ratio
verbose_prose.md,lists_tables,enabled,0,847,1.00
verbose_prose.md,lists_tables,enabled,1,642,0.76
verbose_prose.md,lists_tables,enabled,2,642,0.76
...
```

### 3. Summary Report (`convergence_summary_TIMESTAMP.md`)
Automated pattern detection:
- Convergence rates by technique
- Average rounds to convergence
- Curve type classification
- Safety impact analysis

---

## Interactive Analysis Phase (After Automation)

Once automated tests complete, we analyze together:

### Questions to Answer
1. **Convergence Shape**: Do we see exponential decay or instant convergence?
2. **Technique Comparison**: Which techniques are naturally idempotent?
3. **Safety Necessity**: What's different with safety disabled?
4. **Mathematical Model**: What function f(n) describes tokens at round n?

### Analysis Tools
- Plot curves in spreadsheet/matplotlib
- Identify patterns visually
- Compare safety-enabled vs disabled
- Develop mathematical models

### Expected Outcomes
- **If Intrinsic Stability**: Curves flatten quickly, safety makes no difference
- **If Extrinsic Required**: Safety-disabled shows degradation or divergence
- **Hybrid**: Some techniques intrinsic, others extrinsic

---

## Safety Considerations (Phase 2 - Safety Disabled)

**CRITICAL**: Safety-disabled tests MUST be reviewed manually

### Safety Protocol
1. Run safety-enabled tests first (validate automation)
2. Review safety-enabled results
3. IF safe to proceed: Run safety-disabled in isolated environment
4. Manual review of ALL safety-disabled outputs before analysis
5. Track any information loss or degradation
6. Compare to safety-enabled baseline

### Abort Criteria
- If safety-disabled shows information loss
- If progressive degradation detected
- If results become unintelligible

---

## Execution Options

### Option A: Run Locally (Recommended)
```bash
# You run the script
python scripts/test_convergence.py

# Takes 30-60 minutes
# Generates results in convergence_results/

# We analyze together
```

### Option B: Delegate Data Gathering
- Create as TASK-5.1-A (automated subset)
- TDD: Tests validate data format
- Checkpoints: Validate each technique completes
- Human reviews safety-disabled results

### Option C: Interactive Execution
- I implement and run in real-time
- You review outputs as generated
- Adjust parameters based on findings

---

## Success Criteria

### Automated Phase Success
- [ ] 960 tests execute successfully
- [ ] All data files generated
- [ ] No crashes or errors
- [ ] Summary report produced

### Data Quality
- [ ] Token counts consistent and reasonable
- [ ] Convergence detection working
- [ ] Safety decisions logged correctly
- [ ] CSV format suitable for plotting

### Ready for Analysis
- [ ] Curves can be plotted
- [ ] Patterns are visible in data
- [ ] Safety comparison possible
- [ ] Mathematical modeling feasible

---

## Timeline

**Automated Execution**: 30-60 minutes (unattended)
**Interactive Analysis**: 1-2 hours (together)
**Total**: 2-3 hours

---

## Next Steps

**Immediate**:
1. Review this test plan
2. Choose execution option (A, B, or C)
3. Implement test script
4. Run automated tests
5. Analyze results together

**After Analysis**:
- Document findings in convergence report
- Answer intrinsic stability question
- Update safety system if needed
- Proceed to white paper with evidence

---

## Notes

This hybrid approach separates:
- **Objective data gathering** (automated, deterministic)
- **Subjective interpretation** (interactive, analytical)

The volume-based testing provides the empirical foundation for answering your convergence question with data rather than speculation.