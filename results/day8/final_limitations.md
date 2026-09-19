# Final System Limitations

## Overview
Transparency builds scientific credibility. This document lists the explicit limitations of the AegisScan v1.0 architecture as frozen for the SIH 2026 demonstration.

## 1. Deep RL (DQN) Observation Space Incompatibility
The DQN, DoubleDQN, and DuelingDQN checkpoints were trained on an earlier version of the environment state space. The observation tensor dimensions have since evolved to accommodate the multi-agent design, causing a fatal shape mismatch during inference. These RL agents are completely non-functional in the current build and have been quarantined.

## 2. Hardware Abstraction (MockSDR vs Physical)
While the `Hardware Driver Interface` is fully implemented and capable of connecting to physical SoapySDR devices, the current CI/CD environment and SIH demonstration rely entirely on the `MockSDRDriver`. The system has not yet been subjected to live, over-the-air (OTA) atmospheric noise in a physical field test.

## 3. Synthetic Dataset Limitations
The RF and IR Convolutional Neural Networks (CNNs) were trained on `dataset_v1`, which is highly synthetic. While they perform with >96% accuracy against this synthetic test set, their real-world generalization bounds are untested. They serve primarily as a demonstration of the *pipeline architecture* rather than deployable military-grade classification models.

## 4. Local Benchmark Constraints
The throughput metric of 10,686 ticks/sec was measured on a single local machine without network latency. Multi-node distributed simulation performance (while architecturally supported) remains untested and unbenchmarked.

## Conclusion
AegisScan is an advanced prototype. It successfully solves the theoretical orchestration of an intelligent Electronic Warfare scanning strategy, but requires substantial physical-hardware field testing before field deployment.
