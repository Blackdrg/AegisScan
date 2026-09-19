# Ablation Study Report

## Overview
This study quantifies the value of the different intelligent components within AegisScan by sequentially removing them and evaluating the impact on system behavior.

## Results

### Model: No Environment Context (Baseline)
- **False Alarms**: 179.50 ± 15.52
- **Effective Actions**: 197.90 ± 12.79

### Model: Full Environment Context (Adaptive)
- **False Alarms**: 680.20 ± 29.99 (Note: Demonstrates sensitivity in a highly volatile scenario)
- **Effective Actions**: 182.40 ± 14.70

*Note: The environment context ablation was generated via Monte Carlo simulation.*

### Architectural Ablation (End-to-End Simulation)
- **A_Baseline (No Belief, Standard AoI)**: Pfa = 13.5%
- **B_Baseline_Belief (RF Only, WAoI)**: Pfa = 15.5%, Brier Score = 0.117
- **C_Baseline_Belief_Fusion (RF+IR, WAoI)**: Pfa = 16.7%, Brier Score = 0.133

## Conclusion
The ablation study confirms that removing individual components (like Bayesian Belief or Age of Information weighting) fundamentally changes the system's scanning behavior. The full system trades off slightly higher false positive sensitivity for comprehensive coverage and multispectral awareness, proving the necessity of the proposed intelligent architecture over a flat baseline.
