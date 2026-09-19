import sys
import json
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from aegis_scan.factory.experiment_builder import ExperimentBuilder
from aegis_scan.simulation.engine import MultiAgentSimulationEngine

def safe_div(num, denom):
    if denom == 0:
        return None
    return num / denom

def compute_metrics(timeline, duration):
    tp, fp, tn, fn = 0, 0, 0, 0
    scans = 0
    detections = 0
    
    # We reconstruct ground truth from environment state if timeline doesn't have it explicitly.
    # Actually, let's see how engine metrics computes it or do it from timeline.
    for event in timeline:
        if event.get("event_type") == "DETECTION":
            scans += 1
            is_detected = event.get("detected", False)
            if is_detected:
                detections += 1
            # Wait, the default metrics engine doesn't log TP/FP nicely in timeline?
            # It should be in the summary.
            
    return {}

def run_scenario(name: str, config_dict: dict):
    print(f"\nRunning Scenario: {name}")
    
    base_config = {
        "experiment": {
            "name": name,
            "seed": 42,
            "duration": 500
        },
        "environment": {
            "num_bands": 10,
            "snr_db": config_dict.get("snr_db", 10.0)
        },
        "receiver": {
            "switching_delay": 0,
            "default_dwell_time": 1
        },
        "detection": {
            "type": "probabilistic_energy",
            "p_false_alarm": 0.05
        },
        "scheduler": {
            "type": "round_robin",
            "dwell_time": 1
        },
        "emitters": config_dict.get("emitters", [])
    }
    
    if "interferences" in config_dict:
        base_config["interferences"] = config_dict["interferences"]
        
    components = ExperimentBuilder.build(base_config)
    engine = MultiAgentSimulationEngine(components)
    result = engine.run()
    
    # Extract TP, FP, TN, FN directly from metrics engine
    m = result.metrics
    tp = m.get('total_hits', 0)
    fp = m.get('total_false_alarms', 0)
    tn = m.get('total_correct_rejections', 0)
    fn = m.get('total_misses', 0)
    scans = m.get('total_observations', 0)
    detections = tp + fp
    
    pd = safe_div(tp, tp + fn)
    pfa = safe_div(fp, fp + tn)
    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    
    return {
        "scenario": name,
        "TP": tp,
        "FP": fp,
        "TN": tn,
        "FN": fn,
        "Pd": pd,
        "Pfa": pfa,
        "Precision": precision,
        "Recall": recall,
        "scans": scans,
        "detections": detections,
        "timeline": result.timeline
    }

def main():
    scenarios = [
        ("Scenario A - Noise Only", {"emitters": []}),
        ("Scenario B - Single Emitter", {"emitters": [{"type": "static", "band_id": 3, "snr": 10.0}]}),
        ("Scenario C - Multi Emitter", {"emitters": [
            {"type": "static", "band_id": 2, "snr": 10.0},
            {"type": "static", "band_id": 5, "snr": 5.0},
            {"type": "static", "band_id": 8, "snr": 0.0}
        ]}),
        ("Scenario D - Periodic Emitter", {"emitters": [{"type": "periodic", "band_id": 4, "snr": 5.0, "period": 10, "on_duration": 5}]}),
        ("Scenario E - Changing SNR - 10dB", {"emitters": [{"type": "static", "band_id": 1, "snr": 10.0}]}),
        ("Scenario E - Changing SNR - 5dB", {"emitters": [{"type": "static", "band_id": 1, "snr": 5.0}]}),
        ("Scenario E - Changing SNR - 0dB", {"emitters": [{"type": "static", "band_id": 1, "snr": 0.0}]}),
        ("Scenario E - Changing SNR - -5dB", {"emitters": [{"type": "static", "band_id": 1, "snr": -5.0}]}),
        ("Scenario F - Jamming", {
            "emitters": [{"type": "static", "band_id": 3, "snr": 10.0}],
            "interferences": [{"type": "TargetedMimicJammer", "target_band": 3, "power_db": 15.0}]
        })
    ]
    
    results = []
    
    out_dir = Path("results/final_acceptance")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    for name, conf in scenarios:
        res = run_scenario(name, conf)
        # Avoid dumping the huge timeline to the summary JSON
        summary = {k: v for k, v in res.items() if k != "timeline"}
        results.append(summary)
        print(f"{name}: Pd={summary['Pd']}, Pfa={summary['Pfa']}, Precision={summary['Precision']}, Recall={summary['Recall']}")
        
    with open(out_dir / "scenario_metrics.json", "w") as f:
        json.dump(results, f, indent=4)
        
    import csv
    with open(out_dir / "scenario_metrics.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    main()
