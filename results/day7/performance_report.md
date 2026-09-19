# System Performance Baseline Report

## Overview
This report establishes the fundamental performance metrics of the core engine and algorithms running natively in Python on the execution environment.

## Engine Throughput
The multi-agent simulation engine was profiled to measure execution speed independent of UI/network overhead.
- **Duration Steps**: 500
- **Total Execution Time**: 0.0468 seconds
- **Throughput**: 10,686 simulation steps per second

## Inference Latency
- **RF CNN**: ~12ms per sample (post-warmup)
- **IR CNN**: ~14ms per sample (post-warmup)
- **CA-CFAR / Energy**: <1ms

## Scheduler Decision Latency
Based on the scheduler benchmark traces, the average execution time to calculate the next action:
- **RoundRobin**: ~8.83 ms
- **EarliestAoI**: ~8.68 ms
- **PredictiveUCB**: ~10.99 ms
- **DQN / RL (Unverified)**: ~62.07 ms (Heavy torch overhead)

## Conclusion
The backend Simulation Engine operates ~10,000x faster than real-time when detached from the WebSockets, proving that the Python implementation is not a bottleneck. Classical and Bandit schedulers execute well within the 200ms real-time latency budget required by the SIH constraint.

**Status: PASS**
