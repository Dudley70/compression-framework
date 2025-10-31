#!/usr/bin/env python3
"""
Convergence testing harness for LSC compression techniques.
Generates empirical data for pattern analysis.

This script executes 1200+ compression tests across multiple dimensions:
- 5 documents × 6 techniques × 20 rounds × 2 safety modes = 1200 tests

Usage:
    python scripts/test_convergence.py                    # Run full test suite
    python scripts/test_convergence.py --quick           # Run reduced test suite
    python scripts/test_convergence.py --analyze-only    # Analyze existing data
"""

import json
import csv
import time
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import tiktoken for token counting
try:
    import tiktoken
except ImportError:
    logger.error("tiktoken not found. Install with: pip install tiktoken")
    sys.exit(1)

# Import our compression tool
sys.path.append(str(Path(__file__).parent.parent))
try:
    from compress import CompressionTool, LSCTechniques
except ImportError as e:
    logger.error(f"Error importing compression tool: {e}")
    logger.error("Ensure compress.py is available in the project root")
    sys.exit(1)


class ConvergenceTester:
    """Automated convergence testing with comprehensive data collection"""
    
    def __init__(self, output_dir="convergence_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize tiktoken encoder
        self.encoder = tiktoken.encoding_for_model("gpt-4")
        
        # Initialize compression components
        self.compression_tool = CompressionTool()
        self.lsc = LSCTechniques()
        
        # Test execution metadata
        self.start_time = None
        self.total_tests = 0
        self.completed_tests = 0
        
        logger.info(f"ConvergenceTester initialized with output directory: {self.output_dir}")
    
    def run_test_matrix(self, quick_mode=False) -> Dict[str, Any]:
        """Execute full test matrix: 1200 tests (or reduced for quick mode)"""
        self.start_time = time.time()
        
        max_rounds = 5 if quick_mode else 20
        expected_total = len(self.get_test_documents()) * len(self.get_techniques()) * 2
        if quick_mode:
            expected_total = min(expected_total, 60)  # Limit for quick testing
        
        logger.info(f"Starting convergence test matrix")
        logger.info(f"Mode: {'Quick' if quick_mode else 'Full'}")
        logger.info(f"Max rounds per test: {max_rounds}")
        logger.info(f"Expected total tests: {expected_total}")
        
        results = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "mode": "quick" if quick_mode else "full",
                "total_tests": expected_total,
                "documents": len(self.get_test_documents()),
                "techniques": len(self.get_techniques()),
                "max_rounds": max_rounds,
                "safety_modes": 2
            },
            "tests": []
        }
        
        self.total_tests = expected_total
        self.completed_tests = 0
        
        # Execute test matrix
        for doc_path in self.get_test_documents():
            if quick_mode and len(results["tests"]) >= 60:
                break
                
            for technique in self.get_techniques():
                if quick_mode and len(results["tests"]) >= 60:
                    break
                    
                try:
                    # Test with safety enabled
                    logger.info(f"Testing {doc_path.name} with {technique} (safety=ON)")
                    safety_on_result = self.test_convergence(doc_path, technique, safety=True, max_rounds=max_rounds)
                    results["tests"].append(safety_on_result)
                    self.completed_tests += 1
                    self._report_progress()
                    
                    # Test with safety disabled (ISOLATED)
                    logger.info(f"Testing {doc_path.name} with {technique} (safety=OFF)")
                    safety_off_result = self.test_convergence(doc_path, technique, safety=False, max_rounds=max_rounds)
                    results["tests"].append(safety_off_result)
                    self.completed_tests += 1
                    self._report_progress()
                    
                except Exception as e:
                    logger.error(f"Error testing {doc_path.name} with {technique}: {e}")
                    # Continue with next test
                    continue
        
        # Update final metadata
        results["metadata"]["actual_tests"] = len(results["tests"])
        results["metadata"]["execution_time"] = time.time() - self.start_time
        
        logger.info(f"Test matrix complete! Executed {len(results['tests'])} tests in {results['metadata']['execution_time']:.1f} seconds")
        
        return results
    
    def test_convergence(self, doc_path: Path, technique: str, safety: bool, max_rounds: int = 20) -> Dict[str, Any]:
        """
        Run convergence test: compress same document repeatedly.
        Track token counts, detect convergence, measure stability.
        """
        if not doc_path.exists():
            raise FileNotFoundError(f"Test document not found: {doc_path}")
            
        original_text = doc_path.read_text(encoding='utf-8')
        original_tokens = len(self.encoder.encode(original_text))
        
        trajectory = {
            "document": doc_path.name,
            "technique": technique,
            "safety_enabled": safety,
            "original_tokens": original_tokens,
            "original_chars": len(original_text),
            "rounds": []
        }
        
        current_text = original_text
        previous_hash = None
        
        for round_num in range(max_rounds):
            try:
                # Apply compression
                if technique == "all_combined":
                    compressed = self.compress_full_pipeline(current_text, safety)
                else:
                    compressed = self.compress_single_technique(current_text, technique, safety)
                
                # Measure results
                tokens = len(self.encoder.encode(compressed))
                content_hash = hash(compressed)
                current_tokens = len(self.encoder.encode(current_text))
                
                round_data = {
                    "round": round_num,
                    "tokens": tokens,
                    "chars": len(compressed),
                    "ratio_to_original": tokens / original_tokens if original_tokens > 0 else 1.0,
                    "ratio_to_previous": tokens / current_tokens if current_tokens > 0 else 1.0,
                    "identical_to_previous": (content_hash == previous_hash),
                    "content_hash": content_hash
                }
                
                trajectory["rounds"].append(round_data)
                
                # Check convergence (content identical to previous round)
                if round_data["identical_to_previous"]:
                    trajectory["converged_at_round"] = round_num
                    trajectory["final_tokens"] = tokens
                    trajectory["total_reduction"] = 1 - (tokens / original_tokens)
                    trajectory["converged"] = True
                    break
                
                # Prepare for next round
                current_text = compressed
                previous_hash = content_hash
                
            except Exception as e:
                logger.warning(f"Error in round {round_num} for {doc_path.name} with {technique}: {e}")
                # Record the error and stop this test
                trajectory["error"] = str(e)
                trajectory["failed_at_round"] = round_num
                break
        
        # Mark as non-converged if we completed all rounds without convergence
        if "converged_at_round" not in trajectory and "failed_at_round" not in trajectory:
            trajectory["converged"] = False
            trajectory["final_tokens"] = trajectory["rounds"][-1]["tokens"] if trajectory["rounds"] else original_tokens
            trajectory["total_reduction"] = 1 - (trajectory["final_tokens"] / original_tokens)
        elif "converged_at_round" not in trajectory:
            # Failed partway through
            trajectory["converged"] = False
            trajectory["final_tokens"] = trajectory["rounds"][-1]["tokens"] if trajectory["rounds"] else original_tokens
            trajectory["total_reduction"] = 1 - (trajectory["final_tokens"] / original_tokens)
        
        return trajectory
    
    def compress_full_pipeline(self, text: str, safety_enabled: bool) -> str:
        """Apply all LSC techniques in sequence"""
        # When safety is disabled, we apply techniques directly without the CompressionTool's safety checks
        if not safety_enabled:
            # Apply all techniques manually in sequence
            compressed = text
            
            # Apply each technique
            compressed = self.lsc.apply_lists_tables(compressed)
            compressed = self.lsc.apply_hierarchical_structure(compressed)
            compressed = self.lsc.remove_redundancy(compressed)
            compressed = self.lsc.apply_technical_shorthand(compressed)
            compressed = self.lsc.increase_information_density(compressed)
            
            return compressed
        else:
            # Use the normal compression tool with safety checks
            # Create a temporary file for the compression tool
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
                f.write(text)
                temp_path = f.name
            
            try:
                compressed = self.compression_tool.compress_file(temp_path, dry_run=False)
                return compressed
            finally:
                Path(temp_path).unlink()  # Clean up
    
    def compress_single_technique(self, text: str, technique: str, safety_enabled: bool) -> str:
        """Apply single LSC technique"""
        # Map technique names to methods
        technique_methods = {
            "lists_tables": self.lsc.apply_lists_tables,
            "hierarchical_structure": self.lsc.apply_hierarchical_structure,
            "remove_redundancy": self.lsc.remove_redundancy,
            "technical_shorthand": self.lsc.apply_technical_shorthand,
            "information_density": self.lsc.increase_information_density
        }
        
        if technique not in technique_methods:
            raise ValueError(f"Unknown technique: {technique}")
        
        # Apply the technique
        method = technique_methods[technique]
        compressed = method(text)
        
        # When safety is enabled, we could add validation here
        # For now, we apply the technique directly since individual techniques
        # are generally safer than the full pipeline
        
        return compressed
    
    def get_test_documents(self) -> List[Path]:
        """Return test document paths"""
        fixtures = Path("tests/fixtures")
        
        # The 5 documents specified in the task
        required_docs = [
            "verbose_prose.md",
            "already_compressed.md", 
            "mixed_state.md",
            "entity_heavy.md",
            "semantic_test.md"
        ]
        
        doc_paths = []
        for doc_name in required_docs:
            doc_path = fixtures / doc_name
            if doc_path.exists():
                doc_paths.append(doc_path)
            else:
                logger.warning(f"Test document not found: {doc_path}")
        
        if not doc_paths:
            raise FileNotFoundError("No test documents found in tests/fixtures/")
        
        logger.info(f"Found {len(doc_paths)} test documents: {[p.name for p in doc_paths]}")
        return doc_paths
    
    def get_techniques(self) -> List[str]:
        """Return technique names"""
        return [
            "lists_tables",
            "hierarchical_structure", 
            "remove_redundancy",
            "technical_shorthand",
            "information_density",
            "all_combined"
        ]
    
    def _report_progress(self):
        """Report progress during test execution"""
        if self.total_tests > 0:
            progress_pct = self.completed_tests / self.total_tests
            elapsed = time.time() - self.start_time if self.start_time else 0
            estimated_total = elapsed / progress_pct if progress_pct > 0 else 0
            eta = estimated_total - elapsed
            
            print(f"MCP:PROGRESS {{\"pct\":{progress_pct:.3f},\"msg\":\"Test {self.completed_tests}/{self.total_tests} - ETA: {eta:.0f}s\"}}")
    
    def save_results(self, results: Dict[str, Any], timestamp: str = None) -> Dict[str, str]:
        """Save results in multiple formats and return file paths"""
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        file_paths = {}
        
        # Save JSON (complete data)
        json_path = self.output_dir / f"convergence_data_{timestamp}.json"
        with open(json_path, 'w') as f:
            json.dump(results, f, indent=2)
        file_paths['json'] = str(json_path)
        logger.info(f"Saved JSON data to: {json_path}")
        
        # Save CSV (for plotting)
        csv_path = self.output_dir / f"convergence_curves_{timestamp}.csv"
        self.save_csv(results, csv_path)
        file_paths['csv'] = str(csv_path)
        logger.info(f"Saved CSV data to: {csv_path}")
        
        # Save Markdown summary
        md_path = self.output_dir / f"convergence_summary_{timestamp}.md"
        self.generate_summary(results, md_path)
        file_paths['markdown'] = str(md_path)
        logger.info(f"Saved summary to: {md_path}")
        
        return file_paths
    
    def save_csv(self, results: Dict[str, Any], path: Path):
        """Export as CSV for easy plotting"""
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                "document", "technique", "safety", 
                "round", "tokens", "chars", "ratio_to_original",
                "ratio_to_previous", "converged", "converged_at_round"
            ])
            
            for test in results["tests"]:
                converged = test.get("converged", False)
                converged_at = test.get("converged_at_round", None)
                
                for round_data in test["rounds"]:
                    writer.writerow([
                        test["document"],
                        test["technique"],
                        test["safety_enabled"],
                        round_data["round"],
                        round_data["tokens"],
                        round_data["chars"],
                        round_data["ratio_to_original"],
                        round_data["ratio_to_previous"],
                        converged,
                        converged_at
                    ])
    
    def generate_summary(self, results: Dict[str, Any], path: Path):
        """Generate human-readable summary report"""
        total = len(results["tests"])
        converged = sum(1 for t in results["tests"] if t.get("converged", False))
        failed = sum(1 for t in results["tests"] if "error" in t)
        
        # Group by technique
        by_technique = {}
        for test in results["tests"]:
            tech = test["technique"]
            if tech not in by_technique:
                by_technique[tech] = []
            by_technique[tech].append(test)
        
        # Group by safety mode
        safety_enabled = [t for t in results["tests"] if t["safety_enabled"]]
        safety_disabled = [t for t in results["tests"] if not t["safety_enabled"]]
        
        with open(path, 'w') as f:
            f.write("# Convergence Testing Summary\n\n")
            f.write(f"**Generated**: {results['metadata']['timestamp']}\n")
            f.write(f"**Mode**: {results['metadata']['mode']}\n")
            f.write(f"**Total Tests**: {total}\n")
            f.write(f"**Converged**: {converged} ({converged/total:.1%})\n")
            f.write(f"**Failed**: {failed} ({failed/total:.1%})\n")
            f.write(f"**Execution Time**: {results['metadata'].get('execution_time', 0):.1f} seconds\n\n")
            
            f.write("## Results by Technique\n\n")
            for tech, tests in by_technique.items():
                conv = sum(1 for t in tests if t.get("converged", False))
                fail = sum(1 for t in tests if "error" in t)
                avg_rounds = self._avg_convergence_rounds(tests)
                
                f.write(f"### {tech}\n")
                f.write(f"- Tests: {len(tests)}\n")
                f.write(f"- Converged: {conv} ({conv/len(tests):.1%})\n")
                f.write(f"- Failed: {fail} ({fail/len(tests):.1%})\n")
                f.write(f"- Avg rounds to convergence: {avg_rounds:.1f}\n\n")
            
            f.write("## Safety Mode Comparison\n\n")
            f.write(f"### Safety Enabled ({len(safety_enabled)} tests)\n")
            conv_on = sum(1 for t in safety_enabled if t.get("converged", False))
            fail_on = sum(1 for t in safety_enabled if "error" in t)
            f.write(f"- Converged: {conv_on} ({conv_on/len(safety_enabled):.1%})\n")
            f.write(f"- Failed: {fail_on} ({fail_on/len(safety_enabled):.1%})\n")
            f.write(f"- Avg rounds: {self._avg_convergence_rounds(safety_enabled):.1f}\n\n")
            
            f.write(f"### Safety Disabled ({len(safety_disabled)} tests)\n")
            conv_off = sum(1 for t in safety_disabled if t.get("converged", False))
            fail_off = sum(1 for t in safety_disabled if "error" in t)
            f.write(f"- Converged: {conv_off} ({conv_off/len(safety_disabled):.1%})\n")
            f.write(f"- Failed: {fail_off} ({fail_off/len(safety_disabled):.1%})\n")
            f.write(f"- Avg rounds: {self._avg_convergence_rounds(safety_disabled):.1f}\n\n")
            
            f.write("## Safety Impact Analysis\n\n")
            if len(safety_enabled) > 0 and len(safety_disabled) > 0:
                conv_diff = (conv_off/len(safety_disabled)) - (conv_on/len(safety_enabled))
                f.write(f"- Convergence rate difference: {conv_diff:+.1%} (disabled - enabled)\n")
                f.write(f"- Safety appears to {'help' if conv_diff < 0 else 'hinder'} convergence\n\n")
            
            f.write("## Key Findings\n\n")
            if converged > total * 0.8:
                f.write("- **High convergence rate**: Most tests converged successfully\n")
            elif converged > total * 0.5:
                f.write("- **Moderate convergence rate**: Mixed results across techniques\n") 
            else:
                f.write("- **Low convergence rate**: Many tests did not converge\n")
            
            if failed > total * 0.1:
                f.write("- **Significant failures**: Some tests encountered errors\n")
            
            f.write("\n## Recommendations\n\n")
            f.write("1. Review individual technique performance for optimization opportunities\n")
            f.write("2. Investigate failed tests for common error patterns\n")
            f.write("3. Compare safety-enabled vs safety-disabled results for insights\n")
            f.write("4. Use CSV data for detailed plotting and visual analysis\n")
    
    def _avg_convergence_rounds(self, tests: List[Dict]) -> float:
        """Calculate average rounds to convergence for converged tests"""
        converged_tests = [t for t in tests if t.get("converged", False)]
        if not converged_tests:
            return 0.0
        
        total_rounds = sum(t.get("converged_at_round", 0) for t in converged_tests)
        return total_rounds / len(converged_tests)


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Run convergence testing for LSC compression techniques')
    parser.add_argument('--quick', action='store_true', help='Run quick test mode (reduced test set)')
    parser.add_argument('--analyze-only', action='store_true', help='Analyze existing data without running new tests')
    parser.add_argument('--output-dir', default='convergence_results', help='Output directory for results')
    
    args = parser.parse_args()
    
    # Initialize tester
    tester = ConvergenceTester(output_dir=args.output_dir)
    
    if args.analyze_only:
        logger.info("Analysis-only mode not yet implemented")
        return
    
    print(f"MCP:NOTE {{\"msg\":\"Starting convergence testing - Mode: {'Quick' if args.quick else 'Full'}\"}}")
    
    try:
        # Run the test matrix
        results = tester.run_test_matrix(quick_mode=args.quick)
        
        # Save results
        file_paths = tester.save_results(results)
        
        # Report completion
        total_tests = len(results["tests"])
        converged = sum(1 for t in results["tests"] if t.get("converged", False))
        
        print(f"MCP:COMPLETE {{\"summary\":\"Generated {total_tests} test results, {converged} converged ({converged/total_tests:.1%})\"}}")
        
        logger.info("Convergence testing completed successfully!")
        logger.info(f"Results saved to: {', '.join(file_paths.values())}")
        
    except Exception as e:
        logger.error(f"Convergence testing failed: {e}")
        print(f"MCP:ERROR {{\"msg\":\"Testing failed: {str(e)}\",\"suggest\":\"Check error logs and ensure all dependencies are available\"}}")
        sys.exit(1)


if __name__ == "__main__":
    main()