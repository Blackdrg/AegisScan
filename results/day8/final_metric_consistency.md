# Phase 4: Final Metric Consistency Check

## ML Models (CNN) Verification
Metrics generated dynamically via `scripts/evaluate_v1_models.py` directly from the `best.pt` checkpoints on the underlying synthetic datasets match exactly with the historical/reported numbers.

**RF CNN Metrics:**
- **TP:** 712.0
- **TN:** 748.0
- **FP:** 17.0
- **FN:** 23.0
- **Pd:** 96.87%
- **Pfa:** 2.22%
- **Precision:** 97.66%
- **F1:** 97.26%
- **Accuracy:** 97.33%

**IR CNN Metrics:**
- **TP:** 738.0
- **TN:** 720.0
- **FP:** 14.0
- **FN:** 28.0
- **Pd:** 96.34%
- **Pfa:** 1.90%
- **Precision:** 98.13%
- **F1:** 97.23%
- **Accuracy:** 97.20%

## Dataset Artifacts
- The underlying `presence_detection_v1/metadata.json` confirms:
  - 20,000 samples total
  - Split: 14000 train / 3000 validation / 3000 test
  - IQ samples: 1024, FFT size: 1024

## Simulation Speed
- The simulation engine achieves >10,000 steps per second locally (recorded in previous acceptance benchmark as 10,686 steps/sec). This metric is consistent with local benchmark output.

## Status
**PASS.** All final reported metrics correspond accurately to the underlying ML artifacts and benchmarks currently checked into the repository.
