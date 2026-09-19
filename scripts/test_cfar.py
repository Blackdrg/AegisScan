import sys
import numpy as np
from pathlib import Path
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from aegis_scan.core.cfar import CACFARDetector

@dataclass
class SignalObservationMock:
    power_spectrum: np.ndarray

def test_ca_cfar():
    # CFAR is configured with 10 train cells and 2 guard cells per side
    # For REQ-01: "20 training and 4 guard cells" total => meaning 10 train cells/side and 2 guard cells/side
    # We set those below explicitly.
    detector = CACFARDetector(
        num_guard_cells=2,
        num_train_cells=10,
        threshold_mode="multiplier", 
        k_multiplier=5.0
    )
    
    # Create deterministic mock signal
    # power_spectrum_db is in dB
    # We want base noise to be 0 dB, so power_linear = 1.0
    raw_signal = np.zeros(100)
    
    # Add a huge spike at index 50
    # 20 dB means linear power of 100.
    # Noise linear is 1, Threshold multiplier is 5.0 => Threshold linear is 5.0
    # Cut power will be 100 > 5.0 => Hit.
    raw_signal[50] = 20.0 
    
    obs = SignalObservationMock(power_spectrum=raw_signal)
    
    is_hit, prob = detector.detect(obs)
    print(f"CFAR Detected: {is_hit}, Confidence: {prob}")
    if is_hit:
        print("CA-CFAR successfully detected spike.")
    else:
        print("CA-CFAR failed to detect spike.")

if __name__ == "__main__":
    test_ca_cfar()
