import sys
import numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from aegis_scan.config.loader import ConfigLoader
from aegis_scan.factory.experiment_builder import ExperimentBuilder
from aegis_scan.simulation.engine import MultiAgentSimulationEngine
from aegis_scan.ground_truth.evaluator import Evaluator

def compute_metrics(metrics_engine, total_bands=10, duration=500):
    timeline = metrics_engine.get_timeline()
    print("Metrics keys:", metrics_engine.summary(all_events=[]).keys())
    
def run_scenario(name: str, config_dict: dict):
    print(f"\n{'='*50}\nRunning Scenario: {name}\n{'='*50}")
    
    # Base config
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
    
    metrics = result.metrics
    print(f"Engine Result Metrics: {metrics}")
    
    if "total_hits" in metrics:
        pass
    else:
        print("Standard detection metrics (Pd, Pfa) not directly in result dict. We must compute them.")

if __name__ == "__main__":
    run_scenario("Scenario A - Noise Only", {
        "emitters": []
    })
    
    run_scenario("Scenario B - Single Emitter", {
        "emitters": [
            {"type": "static", "band_id": 3, "snr": 10.0}
        ]
    })

    run_scenario("Scenario C - Multi Emitter", {
        "emitters": [
            {"type": "static", "band_id": 2, "snr": 10.0},
            {"type": "static", "band_id": 5, "snr": 5.0},
            {"type": "static", "band_id": 8, "snr": 0.0}
        ]
    })
    
    run_scenario("Scenario D - Periodic Emitter", {
        "emitters": [
            {"type": "periodic", "band_id": 4, "snr": 5.0, "period": 10, "on_duration": 5}
        ]
    })

    run_scenario("Scenario E - Changing SNR", {
        "emitters": [
            {"type": "static", "band_id": 1, "snr": 10.0} # Will fix SNR sequence internally
        ]
    })

    run_scenario("Scenario F - Jamming", {
        "emitters": [
            {"type": "static", "band_id": 3, "snr": 10.0}
        ],
        "interferences": [
            {"type": "TargetedMimicJammer", "target_band": 3, "power_db": 15.0}
        ]
    })
