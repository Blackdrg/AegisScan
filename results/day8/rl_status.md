# Reinforcement Learning Status (DQN Quarantine)

## Overview
This document formally records the status of the deep reinforcement learning agents (DQN, DoubleDQN, DuelingDQN) implemented in the repository.

## Checkpoint Status
- **Status**: **UNVERIFIED / FAILED VALIDATION**
- **Root Cause**: The saved PyTorch checkpoints (`best.pt`) expect an observation tensor of a specific dimensionality. However, the current `AegisScanEnv` observation space output has been modified since those models were trained, leading to a documented tensor shape mismatch during inference.

## Quarantine Enforcement
The DQN agent executes the simulation by falling back to default/randomized tensors when the mismatch is caught, leading to extremely poor performance (Mean AoI >24). 
- We will **NOT** retrain the models at this stage, as retraining deep RL agents is stochastic and time-prohibitive for a frozen validation phase.
- We will **NOT** compare the DQN's current broken performance against validated schedulers as if it were a valid quantitative result.

**Explicit Statement**: RL is NOT part of the validated primary demonstration path. The SIH demonstration will exclusively utilize the validated Classical and Bandit schedulers.
