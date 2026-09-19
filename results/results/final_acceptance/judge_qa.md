# Judge Q&A Preparation

### 1. What is AegisScan?
AegisScan is an intelligent RF scheduling and detection system designed to optimize wide-spectrum scanning when using limited hardware resources.

### 2. What problem does it solve?
Sequential scanning (sweeping) wastes time observing empty bands. AegisScan allocates receiver time only to bands where there is high belief of activity or where information is stale.

### 3. What is actually novel?
The integration of a Bayesian belief engine with Age of Information (AoI) constraints, driving an RL scheduler. Instead of just detecting, it actively plans its next observation based on the confidence of its intelligence.

### 4. Why UCB?
Upper Confidence Bound balances exploiting known active bands and exploring unknown bands.

### 5. Why LinUCB?
LinUCB allows us to incorporate context, such as current geographic parameters or spectral density, to make informed exploration decisions.

### 6. Why Thompson Sampling?
It provides a probabilistic approach to exploration by sampling from the posterior belief distribution of each band's reward, handling uncertainty robustly.

### 7. Why DQN?
Deep Q-Networks allow the scheduler to learn non-linear policies that consider the entire environment state, adapting to complex patterns like frequency hoppers that simpler bandits might miss.

### 8. Why AoI/WAoI?
Age of Information ensures the system does not get trapped staring at one highly active band. WAoI (Weighted AoI) prioritizes freshness in high-value or high-risk bands.

### 9. Why Bayesian belief?
It provides a mathematically sound way to accumulate evidence over time, turning noisy, discrete detections into a smooth probability of emitter presence.

### 10. Why CNN + classical detector?
The classical energy detector handles rapid, lightweight triggering, while the CNN provides robust, feature-based classification when sufficient data is collected, reducing false alarms.

### 11. How is Pd calculated?
Probability of Detection is the ratio of true positive detection events over the total number of actual emitter transmission events within the simulation.

### 12. How is Pfa calculated?
Probability of False Alarm is the ratio of false positive detections over the total number of non-transmission observation windows.

### 13. What is the ground truth?
The ground truth is provided by the simulation engine's deterministic scenario configuration, tracking exactly when and where emitters are active.

### 14. How do you avoid data leakage?
We use strict isolation between the simulation ground truth and the receiver/detector state. The scheduler only receives noisy, processed observations, never direct simulation state.

### 15. How was the CNN trained?
It was trained on synthetically generated IQ datasets featuring various modulation schemes and noise profiles to emulate realistic RF environments.

### 16. Is the data real or synthetic?
Currently, all validation data is synthetic, generated deterministically to ensure reproducible benchmarking.

### 17. Does it work with real SDR hardware?
The architecture is SDR-ready and uses SoapySDR interfaces, but physical validation is planned as future work.

### 18. What happens under jamming?
The system will detect the jammer energy. If it's a Targeted Mimic Jammer, the system may initially focus on it, but advanced belief models will flag it as an anomaly if its behavior deviates from expected target signatures.

### 19. What happens when the emitter is intermittent?
The Bayesian belief decays when the emitter is off. However, the system learns the temporal pattern (e.g., via DQN) to predict when it will turn on again.

### 20. What happens when SNR falls?
Detection confidence drops. The scheduler adapts by spending more time dwelling on those bands to integrate more signal energy and overcome the noise floor.

### 21. How does the scheduler receive feedback?
It receives a reward signal calculated from detection confidence, intelligence gain (reduction in uncertainty), and AoI reduction.

### 22. How is AoI different from ordinary detection?
Detection is an instantaneous event; AoI is a continuous metric measuring how long it has been since we last looked at a band.

### 23. What happens if the backend disconnects?
The frontend will indicate a connection loss and attempt to automatically reconnect via WebSocket once the backend is restored.

### 24. What are the current limitations?
We rely on synthetic data, lack physical SDR testing, and occasionally miss very short discrete impulses in our end-to-end Pd metrics due to simulation tick resolution.

### 25. How would you deploy it on physical SDR hardware?
We will map the existing SoapySDR hardware abstraction layer to physical USRP devices, feeding raw IQ streams into our processing pipeline instead of simulated signals.
