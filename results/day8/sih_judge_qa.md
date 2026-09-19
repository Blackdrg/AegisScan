# Phase 11: Final SIH Judge Questions

These answers are tailored for technical accuracy based solely on validated features, designed for honest presentation by the student team.

1. **What is AegisScan?**  
   AegisScan is an intelligent scheduling and simulation framework designed to optimize the allocation of limited sensing resources across multiple channels to detect signals using adaptive strategies.

2. **What is the core novelty?**  
   The core novelty lies in using Age of Information (AoI) and contextual bandit algorithms (like PredictiveUCB) to dynamically schedule sensor dwells, replacing static round-robin sweeps.

3. **Why adaptive scanning?**  
   Static scanning wastes time on empty channels. Adaptive scanning learns which channels are active and focuses resources there, reducing latency in threat detection.

4. **Why AoI?**  
   Age of Information measures the freshness of our knowledge about a channel. Minimizing AoI ensures the system doesn't "forget" about channels while focusing elsewhere.

5. **Why WAoI?**  
   Weighted Age of Information (WAoI) allows the system to prioritize critical channels over others, ensuring high-priority threats are monitored more frequently.

6. **Why UCB/PredictiveUCB?**  
   PredictiveUCB provides a mathematically sound balance between exploring unknown channels and exploiting known active channels, adapting to changing environments over time.

7. **Why CNN?**  
   Convolutional Neural Networks excel at pattern recognition in 2D data (like spectrograms), providing higher accuracy for complex signal classification than simple energy thresholding.

8. **Why Energy Detector?**  
   It serves as a fast, computationally inexpensive baseline and pre-filter, preventing the heavier CNN from running on empty noise.

9. **Why CA-CFAR?**  
   Cell-Averaging Constant False Alarm Rate dynamically adjusts the detection threshold based on the local noise floor, handling environments with fluctuating background noise.

10. **Why RF + IR?**  
    Multimodal sensing reduces single-point-of-failure vulnerabilities. A threat might spoof an RF signature but lack the corresponding physical IR signature.

11. **Why Dempster-Shafer?**  
    Dempster-Shafer theory allows us to combine beliefs from multiple independent sensors (RF and IR) and explicitly model the *uncertainty* or conflict between them.

12. **What happens when RF and IR disagree?**  
    The fusion engine penalizes the overall belief score, often requiring additional dwells or preventing a premature "detected" classification, thereby reducing false alarms.

13. **How was the model trained?**  
    The CNN models were trained using PyTorch on a generated synthetic dataset featuring various SNR levels, using early stopping to prevent overfitting.

14. **Where did the data come from?**  
    The current v1 dataset was synthetically generated to model basic presence/absence of signals across defined SNR bands for MVP validation.

15. **Is the dataset real or synthetic?**  
    The v1 dataset is purely synthetic.

16. **Has this been tested on physical SDR?**  
    No. Physical SDR integration is architecturally implemented but currently unverified. The demo relies entirely on a simulated environment using `MockSDR`.

17. **Why is DQN not being used?**  
    The deep reinforcement learning models were quarantined due to an observation-space tensor dimensionality mismatch between the trained checkpoint and the current environment.

18. **What happens if hardware fails?**  
    The backend architecture utilizes a hardware abstraction layer that can report connection failures, and SQLite persistence ensures simulation state recovers safely upon restart.

19. **Is Internet/API access required?**  
    No, the entire pipeline (simulation, backend, models, and React dashboard) runs entirely locally without internet access.

20. **How is latency measured?**  
    Latency is modeled conceptually via the Age of Information (AoI) metric within the simulation, quantifying the time since a channel was last observed.

21. **How reproducible are the results?**  
    Highly reproducible. All benchmarks use fixed random seeds, and the simulation engine outputs deterministic metrics across multiple runs.

22. **What are the major limitations?**  
    The system currently relies on synthetic data (lacking real-world signal multipath fading), operates only in simulation (no OTA SDR testing), and lacks verified deep RL scheduling.

23. **How would this scale?**  
    The modular architecture allows adding more simulated sensors or upgrading the backend to a distributed task queue (like Celery) for heavier inference workloads.

24. **What would be the next research step?**  
    The immediate next steps are resolving the DQN tensor mismatch, replacing synthetic datasets with real-world OTA captures, and conducting physical SDR field tests.
