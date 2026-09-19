# Day 4 Implementation Audit

## Baseline Schedulers
1. **Random Scheduler**
   - **Path**: `src/aegis_scan/scheduling/baselines/random.py`
   - **Status**: IMPLEMENTED
   - **Details**: Selects a random band.

2. **Round Robin Scheduler**
   - **Path**: `src/aegis_scan/scheduling/baselines/round_robin.py`
   - **Status**: IMPLEMENTED
   - **Details**: Iterates sequentially through all bands.

3. **Greedy Scheduler**
   - **Path**: `src/aegis_scan/scheduling/baselines/greedy.py`
   - **Status**: IMPLEMENTED
   - **Details**: Selects the band with the highest historical hit rate.

4. **Earliest AoI Scheduler**
   - **Path**: `src/aegis_scan/scheduling/baselines/earliest_aoi.py`
   - **Status**: IMPLEMENTED
   - **Details**: Selects the band with the maximum standard Age of Information (AoI).

## Bandit Schedulers
5. **UCB / UCB1**
   - **Path**: `src/aegis_scan/scheduling/bandits/ucb.py` and `ucb_variants.py`
   - **Status**: IMPLEMENTED
   - **Details**: Uses `Q(a) + c * sqrt(ln(N)/N(a))`. The base `UCBScheduler` has multi-modality support logic built-in.

6. **UCB-Tuned**
   - **Path**: `src/aegis_scan/scheduling/bandits/ucb_variants.py`
   - **Status**: IMPLEMENTED
   - **Details**: Employs empirical variance bounds.

7. **Bayesian UCB**
   - **Path**: `src/aegis_scan/scheduling/bandits/ucb_variants.py`
   - **Status**: IMPLEMENTED
   - **Details**: Uses Bayesian belief posterior (`presence_probability`) directly from `EnvironmentState`.

8. **Thompson Sampling**
   - **Path**: `src/aegis_scan/scheduling/bandits/thompson.py`
   - **Status**: IMPLEMENTED
   - **Details**: Available in repository.

9. **LinUCB**
   - **Path**: `src/aegis_scan/scheduling/bandits/linucb.py`
   - **Status**: IMPLEMENTED
   - **Details**: Available in repository.

## Reinforcement Learning
10. **DQN / RL Scheduler**
    - **Path**: `src/aegis_scan/scheduling/rl/policy_scheduler.py`
    - **Status**: UNVERIFIED (Implementation exists as `RLScheduler` using `stable_baselines3.DQN`, but requires a valid trained checkpoint `model.pt` matching the exact environment observation space which we must verify during the run).

## Missing or Incomplete Integrations
- Tests specifically for scheduling are sparse in `tests/unit/`.
- Schedulers like `EarliestAoI` default to `RF` sensor modality. We built a `MultimodalEarliestAoIScheduler` wrapper in Day 3 to handle this. For Day 4, we will utilize the schedulers exactly as they are and adapt the benchmark environment.
