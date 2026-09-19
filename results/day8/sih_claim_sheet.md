# SIH Claim Sheet

## Overview
This document compiles the finalized, mathematically backed statements that the team can legally and scientifically claim during the SIH presentation.

| Claim | Exact Metric | Evidence | Condition | Safe wording |
| ----- | ------------ | -------- | --------- | ------------ |
| **ML (RF CNN)** | Pd 96.87%, Pfa 2.22% | `ml_acceptance.md` | Standard evaluation script on dataset v1. | "Our RF CNN achieves a 96.87% probability of detection on the benchmark synthetic dataset." |
| **ML (IR CNN)** | Pd 96.34%, Pfa 1.90% | `ml_acceptance.md` | Standard evaluation script on dataset v1. | "Our IR CNN achieves a 96.34% probability of detection on the benchmark synthetic dataset." |
| **Simulation Speed** | 10,686 simulation steps/sec | `performance_report.md` | Profiling script executed in local Python 3.11 environment. | "The simulation engine achieved 10,686 simulation steps per second in our local benchmark." |
| **Primary Scheduler** | Mean AoI 4.34 | `scheduler_acceptance.md` | Aggregated across 10 random seeds using `PredictiveUCB`. | "PredictiveUCB is an implemented adaptive scheduler evaluated under the defined benchmark scenarios, achieving a Mean AoI of 4.34." |
| **Multimodal Tracking** | Successful Fusion | `multimodal_acceptance.md` | Dempster-Shafer effectively penalized modality disagreement. | "Dempster-Shafer data fusion effectively penalizes sensor disagreements to reduce false alarms in our tests." |
| **Live Telemetry** | 20Hz Update Rate | `day6_e2e_report.md` | Measured across the local WebSocket connection during a live simulation test. | "The dashboard receives live telemetry updates via WebSocket at a tested rate of 20Hz." |
| **System Stability** | Zero Data Loss | `failure_recovery_report.md`| Simulation data successfully retained and re-accessible after forced backend termination. | "Simulation data is persisted via SQLite and can survive backend restarts without data loss." |

## Presentation Rule
Any statement made by the team during the presentation must be traceable to one of the claims above. Do not fabricate or inflate metrics under pressure.
