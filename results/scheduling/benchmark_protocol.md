# Benchmark Protocol for Day 4 Scheduler Validation

## Fairness Criteria

To ensure a fair and rigorous comparison between all evaluated schedulers, the following experimental protocol was enforced dynamically during the benchmark execution:

### 1. Environment Standardization
- **Scenario configuration**: All schedulers were tested against exactly the same 6 scenarios (Static, Periodic, Low SNR, Multimodal, Temporally Changing, Congested).
- **Environment**: Used identical instantiation of `MultiAgentSimulationEngine` across all runs.
- **Detector**: Used `ProbabilisticEnergyDetector` with an identical static configuration (`p_false_alarm=0.05`).
- **Initial State**: Belief and AoI/WAoI engines were fully reset using identical priors before each simulation run.

### 2. Determinism
- **Seed Initialization**: The global numpy seed, as well as the local seeds for the environment, truth generator, and detectors, were strictly set at the start of every iteration (seeds 42 through 51).
- **Step Count**: Every scenario was executed for precisely 500 ticks.

### 3. Action Space and Representation
- **Multimodal Masking**: Schedulers natively selecting only band IDs were seamlessly adapted via a minimal test adapter that toggles the `sensor_modality` field. The scheduling logic itself remained purely dependent on the state provided (AoI, Belief, etc.).

### 4. Hardware Latency Isolation
- Scheduler decision latency was strictly isolated using `time.perf_counter()` directly wrapped around the `select_action` call.
- One-time overhead such as model loading or simulator object instantiation was kept outside the latency loop.

### 5. Verified Schedulers
The following schedulers were tested in identical loops:
1. Random
2. RoundRobin
3. Greedy
4. EarliestAoI
5. UCB1
6. UCBTuned
7. BayesianUCB
8. ThompsonSampling

*(Note: DQN/RL and LinUCB were excluded from the unified quantitative matrix if their specific state dependencies were unaligned with the current generic state shape, guaranteeing that the compared schedulers were receiving identical inputs.)*
