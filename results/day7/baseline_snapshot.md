# Baseline Snapshot

This document serves as the official frozen state of the AegisScan environment prior to the Day 7 acceptance validation suite. 

## Environment Details
- **OS**: Windows (Platform dynamically extracted)
- **Python**: 3.11.9
- **Node**: NPM version dynamically extracted
- **Git Commit**: Refer to `baseline_snapshot.json` for exact HEAD hash

## Datasets and Configuration
- **Dataset Version**: v1 (RF and IR)
- **Seed Aggregation**: 42-51 for 10-seed benchmarks
- **Backend Configuration**: FastAPI on port 8000, Vite dev server on port 5173
- **Hardware Configuration**: `MockSDRDriver` for CI and standardized testing

## ML Model Hashes
- **RF CNN**: `models/rf_cnn_v1.pt` (validated)
- **IR CNN**: `models/ir_cnn_v1.pt` (validated)
- **DQN/RL Checkpoints**: `models/dqn/best.pt` (Explicitly marked as UNVERIFIED due to tensor mismatch)

This state is locked. All benchmarks run in this phase are subject to this configuration.
