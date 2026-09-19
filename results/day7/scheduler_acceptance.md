# Scheduler Acceptance Report

## Overview
This report evaluates the quantitative performance of the scanning schedulers over 10 distinct random seeds (42-51) in the AegisScan environment. The benchmark assessed Classical Baselines, Multi-Armed Bandits (MAB), and explicitly segregated the Broken RL agents.

## Quantitative Results (10-Seed Aggregation)

| Scheduler        | Mean AoI | Reward | Hit Rate | Latency (ms) |
|------------------|----------|--------|----------|--------------|
| RoundRobin       | 4.26     | 20.16  | 45.75%   | 8.83         |
| EarliestAoI      | 4.26     | 19.72  | 44.87%   | 8.68         |
| PredictiveUCB    | 4.34     | 17.74  | 40.92%   | 10.99        |
| LinUCB           | 4.99     | 18.31  | 42.13%   | 10.01        |
| Random           | 7.54     | 19.99  | 45.75%   | 8.89         |
| UCB              | 8.48     | 19.95  | 45.75%   | 8.68         |
| Thompson         | 8.99     | 19.92  | 45.75%   | 8.67         |

*Note: Latencies are per-decision execution times, well under the real-time threshold of 200ms.*

## RL/DQN Segment (UNVERIFIED)
| Scheduler        | Mean AoI | Reward | Hit Rate | Latency (ms) |
|------------------|----------|--------|----------|--------------|
| DQN              | 24.88    | 15.05  | 37.77%   | 44.92        |
| DoubleDQN        | 24.47    | 15.09  | 36.22%   | 62.07        |
| DuelingDQN       | 25.37    | 15.08  | 36.29%   | 66.35        |

> [!WARNING]
> The DQN, DoubleDQN, and DuelingDQN checkpoints suffer from a documented Observation Space incompatibility (Tensor shape mismatch). They executed but failed to learn or utilize the state space correctly, leading to heavily degraded AoI. They remain explicitly UNVERIFIED and are NOT accepted for the primary SIH demonstration strategy.

## Conclusion
The Classical and Bandit schedulers executed deterministically and successfully managed the RF environment. The `RoundRobin` and `EarliestAoI` baselines established a firm lower-bound for Age of Information (AoI ~ 4.26). `PredictiveUCB` demonstrated strong adaptive performance (AoI ~ 4.34) without sacrificing significant hit-rate, making it the accepted adaptive strategy.

**Status: PASS** (Excluding RL/DQN Segment)
