#!/usr/bin/env python3
"""
Advanced convergence pattern analysis for LSC compression data.
Generates comprehensive analysis report with curve classification and insights.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ConvergenceAnalyzer:
    """Advanced pattern detection and analysis for convergence data"""

    def __init__(self, data_file: str, output_dir: str = "convergence_results"):
        self.data_file = Path(data_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Load the data
        with open(self.data_file, 'r') as f:
            self.data = json.load(f)

        logger.info(f"Loaded {len(self.data['tests'])} test results for analysis")

    def analyze_patterns(self) -> Dict[str, Any]:
        """Perform comprehensive pattern analysis"""
        logger.info("Starting pattern analysis...")

        analysis = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "source_data": self.data_file.name,
                "analysis_version": "1.0"
            },
            "overall_statistics": self._overall_stats(),
            "curve_classifications": self._classify_curves(),
            "technique_analysis": self._by_technique_analysis(),
            "document_analysis": self._by_document_analysis(),
            "safety_comparison": self._safety_impact_analysis(),
            "convergence_patterns": self._convergence_patterns(),
            "key_insights": self._key_insights()
        }

        logger.info("Pattern analysis complete")
        return analysis

    def _overall_stats(self) -> Dict[str, Any]:
        """Calculate overall statistics"""
        tests = self.data["tests"]
        total = len(tests)
        converged = sum(1 for t in tests if t.get("converged", False))
        failed = sum(1 for t in tests if "error" in t)

        # Calculate average rounds to convergence
        converged_tests = [t for t in tests if t.get("converged", False)]
        avg_rounds = sum(t.get("converged_at_round", 0) for t in converged_tests) / len(converged_tests) if converged_tests else 0

        # Calculate reduction statistics
        total_reductions = [t.get("total_reduction", 0) for t in tests if "total_reduction" in t]
        avg_reduction = sum(total_reductions) / len(total_reductions) if total_reductions else 0

        return {
            "total_tests": total,
            "converged": converged,
            "convergence_rate": converged / total,
            "failed": failed,
            "failure_rate": failed / total,
            "avg_rounds_to_convergence": avg_rounds,
            "avg_compression_reduction": avg_reduction,
            "execution_time": self.data["metadata"].get("execution_time", 0)
        }

    def _classify_curves(self) -> Dict[str, List]:
        """Classify convergence curve types"""
        classifications = {
            "instant": [],      # Converges in round 0-1
            "fast": [],         # Converges in rounds 2-5
            "gradual": [],      # Converges in rounds 6-15
            "slow": [],         # Converges after round 15
            "divergent": [],    # Never converges
            "failed": []        # Error occurred
        }

        for test in self.data["tests"]:
            if "error" in test:
                classifications["failed"].append(test)
            elif not test.get("converged", False):
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

        # Convert to counts for summary
        return {
            category: {
                "count": len(tests),
                "percentage": len(tests) / len(self.data["tests"]),
                "tests": tests
            }
            for category, tests in classifications.items()
        }

    def _by_technique_analysis(self) -> Dict[str, Dict]:
        """Analyze each technique's behavior"""
        techniques = ["lists_tables", "hierarchical_structure", "remove_redundancy",
                     "technical_shorthand", "information_density", "all_combined"]

        analysis = {}
        for tech in techniques:
            tech_tests = [t for t in self.data["tests"] if t["technique"] == tech]
            converged_tests = [t for t in tech_tests if t.get("converged", False)]

            # Calculate statistics
            convergence_rate = len(converged_tests) / len(tech_tests) if tech_tests else 0
            avg_rounds = sum(t.get("converged_at_round", 0) for t in converged_tests) / len(converged_tests) if converged_tests else 0
            avg_reduction = sum(t.get("total_reduction", 0) for t in tech_tests) / len(tech_tests) if tech_tests else 0

            # Safety comparison
            safety_enabled = [t for t in tech_tests if t["safety_enabled"]]
            safety_disabled = [t for t in tech_tests if not t["safety_enabled"]]

            analysis[tech] = {
                "total_tests": len(tech_tests),
                "convergence_rate": convergence_rate,
                "avg_rounds_to_converge": avg_rounds,
                "avg_compression_reduction": avg_reduction,
                "safety_enabled_convergence": sum(1 for t in safety_enabled if t.get("converged", False)) / len(safety_enabled) if safety_enabled else 0,
                "safety_disabled_convergence": sum(1 for t in safety_disabled if t.get("converged", False)) / len(safety_disabled) if safety_disabled else 0,
                "curve_type": self._determine_curve_type(tech_tests)
            }

        return analysis

    def _by_document_analysis(self) -> Dict[str, Dict]:
        """Analyze behavior by document type"""
        documents = list(set(t["document"] for t in self.data["tests"]))

        analysis = {}
        for doc in documents:
            doc_tests = [t for t in self.data["tests"] if t["document"] == doc]
            converged_tests = [t for t in doc_tests if t.get("converged", False)]

            # Original token counts (should be consistent across tests for same doc)
            original_tokens = doc_tests[0]["original_tokens"] if doc_tests else 0

            analysis[doc] = {
                "total_tests": len(doc_tests),
                "original_tokens": original_tokens,
                "convergence_rate": len(converged_tests) / len(doc_tests) if doc_tests else 0,
                "avg_rounds": sum(t.get("converged_at_round", 0) for t in converged_tests) / len(converged_tests) if converged_tests else 0,
                "avg_reduction": sum(t.get("total_reduction", 0) for t in doc_tests) / len(doc_tests) if doc_tests else 0,
                "technique_performance": self._document_technique_performance(doc_tests)
            }

        return analysis

    def _safety_impact_analysis(self) -> Dict[str, Any]:
        """Compare safety-enabled vs safety-disabled results"""
        enabled = [t for t in self.data["tests"] if t["safety_enabled"]]
        disabled = [t for t in self.data["tests"] if not t["safety_enabled"]]

        enabled_converged = [t for t in enabled if t.get("converged", False)]
        disabled_converged = [t for t in disabled if t.get("converged", False)]

        return {
            "safety_enabled": {
                "tests": len(enabled),
                "convergence_rate": len(enabled_converged) / len(enabled) if enabled else 0,
                "avg_rounds": sum(t.get("converged_at_round", 0) for t in enabled_converged) / len(enabled_converged) if enabled_converged else 0,
                "avg_reduction": sum(t.get("total_reduction", 0) for t in enabled) / len(enabled) if enabled else 0
            },
            "safety_disabled": {
                "tests": len(disabled),
                "convergence_rate": len(disabled_converged) / len(disabled) if disabled else 0,
                "avg_rounds": sum(t.get("converged_at_round", 0) for t in disabled_converged) / len(disabled_converged) if disabled_converged else 0,
                "avg_reduction": sum(t.get("total_reduction", 0) for t in disabled) / len(disabled) if disabled else 0
            },
            "impact_analysis": {
                "convergence_rate_difference": (len(disabled_converged) / len(disabled) - len(enabled_converged) / len(enabled)) if enabled and disabled else 0,
                "rounds_difference": (sum(t.get("converged_at_round", 0) for t in disabled_converged) / len(disabled_converged) -
                                    sum(t.get("converged_at_round", 0) for t in enabled_converged) / len(enabled_converged)) if enabled_converged and disabled_converged else 0,
                "safety_necessity": self._assess_safety_necessity(enabled, disabled)
            }
        }

    def _convergence_patterns(self) -> Dict[str, Any]:
        """Identify specific convergence patterns"""
        patterns = {
            "immediate_stability": [],  # Converges at round 0 or 1
            "exponential_decay": [],    # Rapid convergence with decreasing improvement
            "linear_progression": [],   # Steady improvement over rounds
            "oscillation": [],          # Non-monotonic behavior
            "plateau": [],              # Long periods without change
            "progressive_degradation": [] # Getting worse over rounds (safety disabled)
        }

        for test in self.data["tests"]:
            if not test.get("rounds"):
                continue

            rounds = test["rounds"]
            pattern_type = self._identify_pattern_type(rounds)
            patterns[pattern_type].append(test)

        return {
            pattern: {
                "count": len(tests),
                "percentage": len(tests) / len(self.data["tests"]),
                "examples": tests[:3]  # First 3 examples
            }
            for pattern, tests in patterns.items()
        }

    def _key_insights(self) -> List[str]:
        """Generate key insights from the analysis"""
        insights = []
        stats = self._overall_stats()
        curve_classes = self._classify_curves()

        # Convergence rate insights
        if stats["convergence_rate"] > 0.9:
            insights.append("Extremely high convergence rate (>90%) suggests LSC techniques naturally stabilize")
        elif stats["convergence_rate"] > 0.7:
            insights.append("High convergence rate indicates good intrinsic stability for most techniques")
        else:
            insights.append("Moderate convergence rate suggests some techniques may need safety blocks")

        # Speed insights
        if stats["avg_rounds_to_convergence"] < 2:
            insights.append("Very fast convergence (< 2 rounds) indicates strong intrinsic stopping behavior")
        elif stats["avg_rounds_to_convergence"] < 5:
            insights.append("Fast convergence suggests techniques naturally find stable states")

        # Curve type insights
        instant_pct = curve_classes["instant"]["percentage"]
        if instant_pct > 0.5:
            insights.append("Majority of tests show instant convergence - supports intrinsic stability hypothesis")

        # Safety impact
        safety_analysis = self._safety_impact_analysis()
        conv_diff = safety_analysis["impact_analysis"]["convergence_rate_difference"]
        if abs(conv_diff) < 0.05:
            insights.append("Safety system has minimal impact on convergence - techniques naturally stable")
        elif conv_diff > 0.1:
            insights.append("Safety disabled shows higher convergence - safety blocks may be overly conservative")

        return insights

    def _determine_curve_type(self, tests: List[Dict]) -> str:
        """Determine the dominant curve type for a set of tests"""
        converged = [t for t in tests if t.get("converged", False)]
        if not converged:
            return "divergent"

        avg_rounds = sum(t.get("converged_at_round", 0) for t in converged) / len(converged)
        if avg_rounds <= 1:
            return "instant"
        elif avg_rounds <= 5:
            return "fast"
        else:
            return "gradual"

    def _document_technique_performance(self, doc_tests: List[Dict]) -> Dict[str, float]:
        """Analyze technique performance for a specific document"""
        performance = {}
        techniques = list(set(t["technique"] for t in doc_tests))

        for tech in techniques:
            tech_tests = [t for t in doc_tests if t["technique"] == tech]
            converged = [t for t in tech_tests if t.get("converged", False)]
            performance[tech] = len(converged) / len(tech_tests) if tech_tests else 0

        return performance

    def _assess_safety_necessity(self, enabled_tests: List[Dict], disabled_tests: List[Dict]) -> str:
        """Assess whether safety blocks are necessary"""
        if not enabled_tests or not disabled_tests:
            return "insufficient_data"

        enabled_conv = sum(1 for t in enabled_tests if t.get("converged", False)) / len(enabled_tests)
        disabled_conv = sum(1 for t in disabled_tests if t.get("converged", False)) / len(disabled_tests)

        diff = disabled_conv - enabled_conv

        if diff > 0.1:
            return "safety_blocks_hinder_convergence"
        elif diff < -0.1:
            return "safety_blocks_necessary"
        else:
            return "safety_blocks_neutral"

    def _identify_pattern_type(self, rounds: List[Dict]) -> str:
        """Identify the convergence pattern from round data"""
        if len(rounds) <= 1:
            return "immediate_stability"

        # Check for immediate convergence
        if len(rounds) <= 2:
            return "immediate_stability"

        # For longer sequences, analyze token progression
        tokens = [r["tokens"] for r in rounds]

        # Check for oscillation (non-monotonic)
        increases = sum(1 for i in range(1, len(tokens)) if tokens[i] > tokens[i-1])
        if increases > len(tokens) * 0.3:  # More than 30% increases
            return "oscillation"

        # Check for plateau (no change for multiple rounds)
        no_change = sum(1 for i in range(1, len(tokens)) if tokens[i] == tokens[i-1])
        if no_change > len(tokens) * 0.6:  # More than 60% no change
            return "plateau"

        # Default to exponential decay for decreasing sequences
        return "exponential_decay"

    def generate_report(self, analysis: Dict[str, Any]) -> str:
        """Generate comprehensive analysis report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.output_dir / f"analysis_report_{timestamp}.md"

        with open(report_path, 'w') as f:
            f.write("# Convergence Analysis Report\n\n")
            f.write(f"**Generated**: {analysis['metadata']['timestamp']}\n")
            f.write(f"**Source Data**: {analysis['metadata']['source_data']}\n")
            f.write(f"**Analysis Version**: {analysis['metadata']['analysis_version']}\n\n")

            # Executive Summary
            f.write("## Executive Summary\n\n")
            stats = analysis["overall_statistics"]
            f.write(f"- **Total Tests**: {stats['total_tests']}\n")
            f.write(f"- **Overall Convergence Rate**: {stats['convergence_rate']:.1%}\n")
            f.write(f"- **Average Rounds to Convergence**: {stats['avg_rounds_to_convergence']:.1f}\n")
            f.write(f"- **Average Compression Reduction**: {stats['avg_compression_reduction']:.1%}\n")
            f.write(f"- **Execution Time**: {stats['execution_time']:.2f} seconds\n\n")

            # Key Insights
            f.write("## Key Insights\n\n")
            for insight in analysis["key_insights"]:
                f.write(f"- {insight}\n")
            f.write("\n")

            # Curve Classifications
            f.write("## Convergence Curve Classification\n\n")
            curves = analysis["curve_classifications"]
            for curve_type, data in curves.items():
                f.write(f"### {curve_type.title()} Convergence\n")
                f.write(f"- **Count**: {data['count']} tests ({data['percentage']:.1%})\n")
                f.write(f"- **Description**: {self._get_curve_description(curve_type)}\n\n")

            # Technique Analysis
            f.write("## Technique Performance Analysis\n\n")
            tech_analysis = analysis["technique_analysis"]
            for tech, data in tech_analysis.items():
                f.write(f"### {tech}\n")
                f.write(f"- **Convergence Rate**: {data['convergence_rate']:.1%}\n")
                f.write(f"- **Average Rounds**: {data['avg_rounds_to_converge']:.1f}\n")
                f.write(f"- **Average Reduction**: {data['avg_compression_reduction']:.1%}\n")
                f.write(f"- **Curve Type**: {data['curve_type']}\n")
                f.write(f"- **Safety Impact**: Enabled={data['safety_enabled_convergence']:.1%}, Disabled={data['safety_disabled_convergence']:.1%}\n\n")

            # Document Analysis
            f.write("## Document-Specific Analysis\n\n")
            doc_analysis = analysis["document_analysis"]
            for doc, data in doc_analysis.items():
                f.write(f"### {doc}\n")
                f.write(f"- **Original Tokens**: {data['original_tokens']}\n")
                f.write(f"- **Convergence Rate**: {data['convergence_rate']:.1%}\n")
                f.write(f"- **Average Rounds**: {data['avg_rounds']:.1f}\n")
                f.write(f"- **Average Reduction**: {data['avg_reduction']:.1%}\n\n")

            # Safety Analysis
            f.write("## Safety System Impact Analysis\n\n")
            safety = analysis["safety_comparison"]
            f.write("### Safety Enabled Results\n")
            f.write(f"- **Tests**: {safety['safety_enabled']['tests']}\n")
            f.write(f"- **Convergence Rate**: {safety['safety_enabled']['convergence_rate']:.1%}\n")
            f.write(f"- **Average Rounds**: {safety['safety_enabled']['avg_rounds']:.1f}\n\n")

            f.write("### Safety Disabled Results\n")
            f.write(f"- **Tests**: {safety['safety_disabled']['tests']}\n")
            f.write(f"- **Convergence Rate**: {safety['safety_disabled']['convergence_rate']:.1%}\n")
            f.write(f"- **Average Rounds**: {safety['safety_disabled']['avg_rounds']:.1f}\n\n")

            f.write("### Impact Assessment\n")
            impact = safety["impact_analysis"]
            f.write(f"- **Convergence Rate Difference**: {impact['convergence_rate_difference']:+.1%} (disabled - enabled)\n")
            f.write(f"- **Rounds Difference**: {impact['rounds_difference']:+.1f}\n")
            f.write(f"- **Safety Necessity**: {impact['safety_necessity'].replace('_', ' ').title()}\n\n")

            # Convergence Patterns
            f.write("## Convergence Pattern Analysis\n\n")
            patterns = analysis["convergence_patterns"]
            for pattern, data in patterns.items():
                if data["count"] > 0:
                    f.write(f"### {pattern.replace('_', ' ').title()}\n")
                    f.write(f"- **Count**: {data['count']} ({data['percentage']:.1%})\n")
                    f.write(f"- **Description**: {self._get_pattern_description(pattern)}\n\n")

            # Conclusions
            f.write("## Conclusions\n\n")
            f.write("### Intrinsic Stability Assessment\n\n")
            if stats['convergence_rate'] > 0.9 and stats['avg_rounds_to_convergence'] < 2:
                f.write("**STRONG EVIDENCE for intrinsic stability**:\n")
                f.write("- Very high convergence rate (>90%)\n")
                f.write("- Rapid convergence (< 2 rounds average)\n")
                f.write("- Most techniques naturally find stable states\n")
            elif stats['convergence_rate'] > 0.7:
                f.write("**MODERATE EVIDENCE for intrinsic stability**:\n")
                f.write("- Good convergence rate (>70%)\n")
                f.write("- Some techniques show natural stability\n")
                f.write("- Safety blocks may be beneficial for edge cases\n")
            else:
                f.write("**LIMITED EVIDENCE for intrinsic stability**:\n")
                f.write("- Moderate convergence rate\n")
                f.write("- Safety blocks appear necessary\n")
                f.write("- Further investigation needed\n")

            f.write("\n### Recommendations for Interactive Analysis\n\n")
            f.write("1. **Plot convergence curves** for each technique to visualize behavior patterns\n")
            f.write("2. **Examine safety-disabled results** manually for content quality\n")
            f.write("3. **Investigate non-converging tests** to understand failure modes\n")
            f.write("4. **Compare document-specific patterns** to identify content sensitivities\n")
            f.write("5. **Test edge cases** with longer documents or different content types\n")

        logger.info(f"Analysis report generated: {report_path}")
        return str(report_path)

    def _get_curve_description(self, curve_type: str) -> str:
        """Get description for curve type"""
        descriptions = {
            "instant": "Converges immediately or within 1 round",
            "fast": "Converges within 2-5 rounds",
            "gradual": "Converges within 6-15 rounds",
            "slow": "Converges after 15+ rounds",
            "divergent": "Does not converge within test limits",
            "failed": "Test encountered an error"
        }
        return descriptions.get(curve_type, "Unknown curve type")

    def _get_pattern_description(self, pattern: str) -> str:
        """Get description for convergence pattern"""
        descriptions = {
            "immediate_stability": "Content unchanged after first compression",
            "exponential_decay": "Rapid improvement followed by stabilization",
            "linear_progression": "Steady improvement over multiple rounds",
            "oscillation": "Non-monotonic behavior with ups and downs",
            "plateau": "Long periods without significant change",
            "progressive_degradation": "Quality degrades over successive rounds"
        }
        return descriptions.get(pattern, "Unknown pattern type")


def main():
    """Main execution function"""
    if len(sys.argv) < 2:
        print("Usage: python analyze_convergence.py <data_file.json>")
        sys.exit(1)

    data_file = sys.argv[1]
    if not Path(data_file).exists():
        print(f"Error: Data file not found: {data_file}")
        sys.exit(1)

    # Initialize analyzer
    analyzer = ConvergenceAnalyzer(data_file)

    # Run analysis
    print("MCP:PROGRESS {\"pct\":0.1,\"msg\":\"Starting pattern analysis\"}")
    analysis = analyzer.analyze_patterns()

    print("MCP:PROGRESS {\"pct\":0.8,\"msg\":\"Generating analysis report\"}")
    report_path = analyzer.generate_report(analysis)

    print(f"MCP:COMPLETE {{\"summary\":\"Analysis complete - report generated at {report_path}\"}}")
    print(f"Analysis report generated: {report_path}")


if __name__ == "__main__":
    main()