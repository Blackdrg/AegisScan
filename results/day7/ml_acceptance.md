# ML Acceptance Report

## Overview
This phase evaluated the validated v1 models for the CNN-based detectors (RF and IR). The models were subjected to a fresh inference pass on the standardized dataset, measuring probability of detection (Pd), probability of false alarm (Pfa), Precision, and F1.

## RF CNN Evaluation
* **True Positives (TP)**: 712.0
* **True Negatives (TN)**: 748.0
* **False Positives (FP)**: 17.0
* **False Negatives (FN)**: 23.0
* **Probability of Detection (Pd / Recall)**: 0.9687 (96.87%)
* **Probability of False Alarm (Pfa)**: 0.0222 (2.22%)
* **Precision**: 0.9766 (97.66%)
* **F1 Score**: 0.9726 (97.26%)
* **Accuracy**: 0.9733 (97.33%)

## IR CNN Evaluation
* **True Positives (TP)**: 738.0
* **True Negatives (TN)**: 720.0
* **False Positives (FP)**: 14.0
* **False Negatives (FN)**: 28.0
* **Probability of Detection (Pd / Recall)**: 0.9634 (96.34%)
* **Probability of False Alarm (Pfa)**: 0.0190 (1.90%)
* **Precision**: 0.9813 (98.13%)
* **F1 Score**: 0.9723 (97.23%)
* **Accuracy**: 0.9720 (97.20%)

## Conclusion
Both RF and IR models satisfy the project requirements with >96% Pd and <3% Pfa. The inference latency results (typically <15ms per frame post-warmup) satisfy the real-time operational constraints. These models remain officially ACCEPTED for SIH demonstration.
