# AegisScan v2.2 Final Remediation Plan

This document outlines the step-by-step remediation plan to replace all mocked prototypes in AegisScan v2.2 with fully functional, trained, and integrated systems, leading to a legitimate final certification.

## Open Questions

> [!WARNING]
> This is a massive effort involving training multiple Deep Learning models (CNN, Multimodal, RL), rewriting major UI components, setting up full Playwright E2E testing, and orchestrating extensive benchmarks. Are there specific time constraints or computational budget limits (e.g., GPU availability) for the RL/CNN training phases? 
>
> If you approve, I will begin executing Phase A and work sequentially through the list.

## Remediation Phases

### Phase A: Simulation Control Fix
- **Root Cause**: Missing backend state machine and API endpoints for pausing/resuming.
- **Fix**: Implement `pause()`, `resume()`, and `stop()` in `engine.py`. Connect to FastAPI and React UI. Add state transitions (`CREATED`, `RUNNING`, `PAUSED`, etc.).
- **Dependency**: None.

### Phase B & C: Geography Foundation & Ground Truth
- **Root Cause**: Geography layer was entirely stubbed out.
- **Fix**: Create `geography/` module supporting 2D/3D coordinates and integrate it directly into `EnvironmentState`, `GroundTruth`, and `BayesianFusion`.

### Phase D, F, G, H, I: CNN Baseline & Multimodal ML Training
- **Root Cause**: Preprocessing mismatch in CNN baseline; model was untrained. Multimodal, Spectrogram, and Temporal branches never implemented.
- **Fix**: 
  1. Standardize IQ/Spectrogram preprocessing (STFT, FFT size, window, normalization) into a canonical pipeline.
  2. Generate versioned datasets for IQ, Spectrogram, and Temporal sequences.
  3. Train a 1D IQ CNN, 2D Spectrogram CNN, and a fused Multibranch Model.
  4. Train a Temporal sequence model (GRU/LSTM).
  5. Save checkpoints with embedded metadata to prevent mismatch.

### Phase L: Bayesian Geographic Fusion
- **Root Cause**: Fake probabilities used instead of rigorous Bayesian updates. Geographic context was missing.
- **Fix**: Implement rigorous Bayesian fusion (`P(S | D, E, G, T)`) incorporating geography and time. Add reference unit tests.

### Phase M, N, O: RL Training & Action Masking
- **Root Cause**: Stable-Baselines3 default initialization with 0 timesteps; masking failed completely.
- **Fix**: 
  1. Fix valid/invalid action mask generation.
  2. Retrain DQN, Double DQN, and Dueling DQN with action masking and Huber loss for `500,000` steps.
  3. Inject Geography into RL state space.

### Phase P, Q, R: Frontend Un-Mocking & Feature Parity
- **Root Cause**: UI heavily relied on fake static arrays for charts, metrics, and demo modes.
- **Fix**: 
  1. Delete all static mock data from `AnalyticsPage.tsx`, `SchedulingPage.tsx`, and `DemoMode.tsx`.
  2. Implement a real `Geography` UI rendering actual map state.
  3. Wire frontend directly to live WebSocket/REST API for all components.

### Phase S & U: Security & Persistence Fixes
- **Root Cause**: Path traversal vulnerability in scenario loader; WebSocket exceptions leaked raw traces; database schema was non-existent.
- **Fix**: Sanitize `scenario_id` paths. Return safe error codes over WS. Implement robust SQLite persistence for `simulations` and verify survival across restarts.

### Phase T, V, W, X, Y, Z: Testing, E2E, & Benchmarks
- **Root Cause**: Playwright tests were stubs. Performance claims were fabricated (used trivial energy detector). Benchmarks were unverified.
- **Fix**: 
  1. Configure full Playwright E2E suite capturing video/screenshots on a live FastAPI/SQLite backend.
  2. Profile the *actual* CNN inference to report real latency (expected ~2.44 ms, not 0.61 ms).
  3. Run the final 10-seed multi-algorithm benchmark, stress tests, and ablation studies.

### Phase AA & AB: Final Reporting
- **Root Cause**: Reports contained historical fabricated claims.
- **Fix**: Re-write `REPORT.md` and generate all `results/final_certification/` artifacts containing real, verifiable metrics. Update `MASTER_CHECKLIST.md` with honest outcomes.
