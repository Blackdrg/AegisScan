import json
from pathlib import Path

MATRIX = [
    {
        "ID": "REQ-01",
        "Subsystem": "Detection",
        "Requirement": "CA-CFAR operates with 20 training and 4 guard cells.",
        "Test/Scenario": "Unit Test / CA-CFAR",
        "Expected Behavior": "Threshold multiplier is strictly applied excluding guard cells.",
        "Actual Result": "TBD",
        "Metric": "Threshold Error",
        "Threshold": "< 0.001",
        "Status": "NOT_ACTIVE",
        "Evidence File": "tests/test_cfar.py",
        "Code Location": "src/aegis_scan/core/cfar.py",
        "Regression Test": "TBD",
        "Notes": "TBD"
    },
    {
        "ID": "REQ-02",
        "Subsystem": "Detection",
        "Requirement": "Pd and Pfa handled without div-by-zero errors.",
        "Test/Scenario": "Scenario Math Audit",
        "Expected Behavior": "Zero denominator yields NaN or defined fallback without crashing.",
        "Actual Result": "TBD",
        "Metric": "Exception Count",
        "Threshold": "0",
        "Status": "NOT_ACTIVE",
        "Evidence File": "scenario_metrics.json",
        "Code Location": "src/aegis_scan/ground_truth/evaluator.py",
        "Regression Test": "TBD",
        "Notes": "TBD"
    },
    {
        "ID": "REQ-03",
        "Subsystem": "Environment",
        "Requirement": "Scenario A produces 0 TP and predictable FP.",
        "Test/Scenario": "Scenario A - Noise Only",
        "Expected Behavior": "TP=0, Pd=NaN or None, Pfa matches CFAR configuration.",
        "Actual Result": "TBD",
        "Metric": "Pd, Pfa",
        "Threshold": "Pfa ~ 0.05",
        "Status": "NOT_ACTIVE",
        "Evidence File": "scenario_metrics.json",
        "Code Location": "scripts/validate_scenarios.py",
        "Regression Test": "TBD",
        "Notes": "TBD"
    },
    {
        "ID": "REQ-04",
        "Subsystem": "Environment",
        "Requirement": "Scenario B discriminates signal from noise.",
        "Test/Scenario": "Scenario B - Single Persistent",
        "Expected Behavior": "Pd is high >0.8, Pfa is nominal.",
        "Actual Result": "TBD",
        "Metric": "Pd, Pfa",
        "Threshold": "Pd > 0.8",
        "Status": "NOT_ACTIVE",
        "Evidence File": "scenario_metrics.json",
        "Code Location": "scripts/validate_scenarios.py",
        "Regression Test": "TBD",
        "Notes": "TBD"
    },
    {
        "ID": "REQ-05",
        "Subsystem": "Environment",
        "Requirement": "Scenario C handles disjoint multiple emitters.",
        "Test/Scenario": "Scenario C - Multi Emitter",
        "Expected Behavior": "Independent band tracking.",
        "Actual Result": "TBD",
        "Metric": "Coverage / Pd per band",
        "Threshold": "> 0.5",
        "Status": "NOT_ACTIVE",
        "Evidence File": "scenario_metrics.json",
        "Code Location": "scripts/validate_scenarios.py",
        "Regression Test": "TBD",
        "Notes": "TBD"
    },
    {
        "ID": "REQ-06",
        "Subsystem": "Environment",
        "Requirement": "Scenario D handles periodic deterministic 5/5 ticks.",
        "Test/Scenario": "Scenario D - Periodic",
        "Expected Behavior": "Belief goes up and down over 10-tick period.",
        "Actual Result": "TBD",
        "Metric": "Belief Variance",
        "Threshold": "> 0.1",
        "Status": "NOT_ACTIVE",
        "Evidence File": "scenario_metrics.json",
        "Code Location": "scripts/validate_scenarios.py",
        "Regression Test": "TBD",
        "Notes": "TBD"
    },
    {
        "ID": "REQ-07",
        "Subsystem": "Environment",
        "Requirement": "Scenario E logs degraded Pd as SNR drops.",
        "Test/Scenario": "Scenario E - Changing SNR",
        "Expected Behavior": "Pd strictly decreases as SNR drops from +10 to -5.",
        "Actual Result": "TBD",
        "Metric": "Pd sequence",
        "Threshold": "Pd(10) > Pd(-5)",
        "Status": "NOT_ACTIVE",
        "Evidence File": "scenario_metrics.json",
        "Code Location": "scripts/validate_scenarios.py",
        "Regression Test": "TBD",
        "Notes": "TBD"
    },
    {
        "ID": "REQ-08",
        "Subsystem": "Environment",
        "Requirement": "Scenario F uses TargetedMimicJammer.",
        "Test/Scenario": "Scenario F - Jammer",
        "Expected Behavior": "Jammer triggers false detection or is correctly logged.",
        "Actual Result": "TBD",
        "Metric": "Jammer Active",
        "Threshold": "True",
        "Status": "NOT_ACTIVE",
        "Evidence File": "scenario_metrics.json",
        "Code Location": "scripts/validate_scenarios.py",
        "Regression Test": "TBD",
        "Notes": "TBD"
    },
    {
        "ID": "REQ-09",
        "Subsystem": "ML",
        "Requirement": "CNN preprocessing in inference matches training.",
        "Test/Scenario": "CNN Preprocessing Audit",
        "Expected Behavior": "Shapes, Normalization, Channel alignment perfectly match.",
        "Actual Result": "TBD",
        "Metric": "Parity",
        "Threshold": "True",
        "Status": "NOT_ACTIVE",
        "Evidence File": "algorithm_validation.md",
        "Code Location": "src/aegis_scan/ml/detector.py",
        "Regression Test": "TBD",
        "Notes": "TBD"
    },
    {
        "ID": "REQ-10",
        "Subsystem": "Intelligence",
        "Requirement": "Belief probabilities strictly [0, 1].",
        "Test/Scenario": "Bayesian Bounds Test",
        "Expected Behavior": "No probability exceeds 1.0 or drops below 0.0.",
        "Actual Result": "TBD",
        "Metric": "Bounds Exception Count",
        "Threshold": "0",
        "Status": "NOT_ACTIVE",
        "Evidence File": "tests/test_belief_state.py",
        "Code Location": "src/aegis_scan/knowledge/belief_state.py",
        "Regression Test": "TBD",
        "Notes": "TBD"
    },
    {
        "ID": "REQ-11",
        "Subsystem": "Intelligence",
        "Requirement": "AoI / WAoI scaling with time.",
        "Test/Scenario": "AoI Deterministic Test",
        "Expected Behavior": "AoI resets on observation, increments otherwise.",
        "Actual Result": "TBD",
        "Metric": "AoI Reset",
        "Threshold": "True",
        "Status": "NOT_ACTIVE",
        "Evidence File": "tests/test_aoi_engine.py",
        "Code Location": "src/aegis_scan/knowledge/aoi.py",
        "Regression Test": "TBD",
        "Notes": "TBD"
    },
    {
        "ID": "REQ-12",
        "Subsystem": "Schedulers",
        "Requirement": "Schedulers execute mathematical updates.",
        "Test/Scenario": "Scheduler Unit Tests",
        "Expected Behavior": "UCB, LinUCB, Thompson, DQN properly select actions and update internal weights.",
        "Actual Result": "TBD",
        "Metric": "Pass Rate",
        "Threshold": "100%",
        "Status": "NOT_ACTIVE",
        "Evidence File": "algorithm_validation.md",
        "Code Location": "src/aegis_scan/scheduling/",
        "Regression Test": "TBD",
        "Notes": "TBD"
    },
    {
        "ID": "REQ-13",
        "Subsystem": "Integration",
        "Requirement": "Full Receiver Feedback Loop executes.",
        "Test/Scenario": "E2E Trace Logging",
        "Expected Behavior": "scheduler -> receiver -> detect -> belief -> reward.",
        "Actual Result": "TBD",
        "Metric": "Log Continuity",
        "Threshold": "True",
        "Status": "NOT_ACTIVE",
        "Evidence File": "algorithm_validation.md",
        "Code Location": "src/aegis_scan/simulation/engine.py",
        "Regression Test": "TBD",
        "Notes": "TBD"
    },
    {
        "ID": "REQ-14",
        "Subsystem": "Integration",
        "Requirement": "Simulation is strictly reproducible with fixed seed.",
        "Test/Scenario": "Reproducibility Test",
        "Expected Behavior": "Two runs with same seed produce identical state and outputs.",
        "Actual Result": "TBD",
        "Metric": "State Match",
        "Threshold": "True",
        "Status": "NOT_ACTIVE",
        "Evidence File": "reproducibility.md",
        "Code Location": "scripts/validate_scenarios.py",
        "Regression Test": "TBD",
        "Notes": "TBD"
    },
    {
        "ID": "REQ-15",
        "Subsystem": "Benchmarking",
        "Requirement": "10-seed multi-agent benchmark exports correctly.",
        "Test/Scenario": "10-Seed Final Benchmark",
        "Expected Behavior": "Outputs aggregated mean, std, min, max.",
        "Actual Result": "TBD",
        "Metric": "File Existence & Integrity",
        "Threshold": "True",
        "Status": "NOT_ACTIVE",
        "Evidence File": "results/final_acceptance/benchmark_summary.csv",
        "Code Location": "scripts/final_acceptance_benchmark.py",
        "Regression Test": "TBD",
        "Notes": "TBD"
    },
    {
        "ID": "REQ-16",
        "Subsystem": "Visualization",
        "Requirement": "Scientific plots generated via Matplotlib without cherry-picking.",
        "Test/Scenario": "Graph Generation",
        "Expected Behavior": "Pd vs SNR, Pfa, Precision/Recall, Belief, AoI, Actions, Timeline plotted.",
        "Actual Result": "TBD",
        "Metric": "Plot Integrity",
        "Threshold": "True",
        "Status": "NOT_ACTIVE",
        "Evidence File": "results/final_acceptance/plots/",
        "Code Location": "scripts/generate_plots.py",
        "Regression Test": "TBD",
        "Notes": "TBD"
    },
    {
        "ID": "REQ-17",
        "Subsystem": "Frontend/Backend",
        "Requirement": "Numerical formatting Parity.",
        "Test/Scenario": "verify_frontend.cjs",
        "Expected Behavior": "NaN/Infinity handling exactly matches expected formats.",
        "Actual Result": "TBD",
        "Metric": "Pass Rate",
        "Threshold": "100%",
        "Status": "NOT_ACTIVE",
        "Evidence File": "results/final_acceptance/frontend_backend_parity.md",
        "Code Location": "dashboard/verify_frontend.cjs",
        "Regression Test": "TBD",
        "Notes": "TBD"
    },
    {
        "ID": "REQ-18",
        "Subsystem": "Integration",
        "Requirement": "API / WebSocket Consistency.",
        "Test/Scenario": "WebSocket Live Validation",
        "Expected Behavior": "Telemetry flows properly without falsified values.",
        "Actual Result": "TBD",
        "Metric": "Telemetry Drop Rate",
        "Threshold": "< 1%",
        "Status": "NOT_ACTIVE",
        "Evidence File": "results/final_acceptance/frontend_backend_parity.md",
        "Code Location": "tests/api/test_websocket.py",
        "Regression Test": "TBD",
        "Notes": "TBD"
    },
    {
        "ID": "REQ-19",
        "Subsystem": "Frontend",
        "Requirement": "Environment Dashboard classified properly.",
        "Test/Scenario": "Dashboard Availability Check",
        "Expected Behavior": "Marked PARTIAL/BLOCKED if backend endpoints missing.",
        "Actual Result": "TBD",
        "Metric": "Status classification",
        "Threshold": "Honest",
        "Status": "NOT_ACTIVE",
        "Evidence File": "limitations.md",
        "Code Location": "dashboard/src/components/EnvironmentView",
        "Regression Test": "TBD",
        "Notes": "TBD"
    },
    {
        "ID": "REQ-20",
        "Subsystem": "Backend",
        "Requirement": "Dataset/Model persistence validated.",
        "Test/Scenario": "Persistence Integration Tests",
        "Expected Behavior": "Correct metadata loaded from DB or Disk.",
        "Actual Result": "TBD",
        "Metric": "Persistence Integrity",
        "Threshold": "True",
        "Status": "NOT_ACTIVE",
        "Evidence File": "algorithm_validation.md",
        "Code Location": "src/aegis_scan/persistence/",
        "Regression Test": "TBD",
        "Notes": "TBD"
    }
]

def generate_matrix():
    out_dir = Path("results/final_acceptance")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    with open(out_dir / "acceptance_matrix.json", "w") as f:
        json.dump(MATRIX, f, indent=4)
        
    with open(out_dir / "acceptance_matrix.md", "w") as f:
        f.write("# AegisScan Final Acceptance Matrix\n\n")
        f.write("| ID | Subsystem | Requirement | Test/Scenario | Expected Behavior | Actual Result | Metric | Threshold | Status | Evidence File | Code Location | Regression Test | Notes |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")
        for m in MATRIX:
            f.write(f"| {m['ID']} | {m['Subsystem']} | {m['Requirement']} | {m['Test/Scenario']} | {m['Expected Behavior']} | {m['Actual Result']} | {m['Metric']} | {m['Threshold']} | {m['Status']} | {m['Evidence File']} | {m['Code Location']} | {m['Regression Test']} | {m['Notes']} |\n")

if __name__ == "__main__":
    generate_matrix()
    print("Acceptance matrix generated.")
