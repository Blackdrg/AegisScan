# Detector Parameter Reconciliation

## Overview
This document reconciles the exact parameters used by the classical detection algorithms (Energy Detector and CA-CFAR) to ensure theoretical claims match the actual software implementation.

## CA-CFAR Configuration
- **Training Cells**: 20 total (10 per side)
- **Guard Cells**: 4 total (2 per side)
- **Target Probability of False Alarm (Pfa)**: Earlier benchmarks evaluated a strict 1e-4 Pfa limit. However, the final Day 7 Multimodal and Ablation validation explicitly evaluated the engine configured at a 5% (0.05) Pfa bound to test multi-agent noise suppression.
- **Detector Type**: Cell-Averaging Constant False Alarm Rate (CA-CFAR)

### Final Configuration Table

| Parameter | Isolated Test Limit | System Ablation Bound |
| :--- | :--- | :--- |
| Training Cells (Total) | 20 | 20 |
| Guard Cells (Total) | 4 | 4 |
| Target Pfa | 1e-4 | 5% (0.05) |
| Multi-Agent Suppression | N/A | Active |

## Reconciliation
The discrepancy between "1e-4" and "5%" is a difference in testing contexts:
1. The **isolated detector component tests** evaluated the mathematical limit (1e-4).
2. The **Full-System Ablation tests** evaluated the Bayesian engine's ability to suppress higher environmental noise, purposefully utilizing detectors tuned to a 5% Pfa.

Both statements are correct in their respective contexts. The SIH demonstration uses the 5% baseline to actively demonstrate the Bayesian fusion engine filtering out false alarms.
