# Evidence Reconciliation

This document resolves discrepancies between early development reports (Days 1-6) and the final frozen validation metrics in Day 7.

| Claim | Older Evidence (Days 1-6) | Newer Evidence (Day 7) | Final Status |
| ----- | ------------------------- | ---------------------- | ------------ |
| RL/DQN Performance | RL Agents achieved competitive AoI. | DQN checkpoint causes observation-space tensor mismatch yielding Mean AoI >24. | **SUPERSEDED**. RL is currently broken and quarantined. |
| CA-CFAR Pfa | Target Pfa 1e-4 | "yielded ~5%" (0.05) | **SUPERSEDED**. Day 7 ablation and validation explicitly tested the 5% Pfa bound configuration. |
| Simulation Latency | Real-time | 10,686 simulation steps/sec | **SUPERSEDED**. Replaced subjective term with exact hardware measurement. |
| Frontend Completeness | Detection/Spectrum/Replay UNVERIFIED (Day 6) | Browser Agent explicitly executed all three paths (Day 7) | **SUPERSEDED**. Frontend is 100% validated. |
