# Phase 12: Final Presentation Script (60–90 seconds)

"Good morning Judges. We are team ByteMind, and this is AegisScan.

**The Problem:** Modern spectrum monitoring suffers from latency. When you have limited sensing hardware but thousands of channels to monitor, traditional static sweeping wastes critical time on empty frequencies while missing fleeting signals.

**Our Approach & Scheduling:** To solve this, we implemented an adaptive scheduling framework. Instead of scanning blindly, we track the 'Age of Information' for each channel. Using a contextual bandit algorithm called PredictiveUCB, the system mathematically balances exploring stale channels against exploiting known active ones.

**Sensing & Detection:** We simulate multimodal inputs across both RF and IR sensors. For rapid triage, we use a CA-CFAR energy detector to establish a dynamic noise floor. When activity is detected, we pass the data through our Convolutional Neural Networks, which achieved a 96% probability of detection on our synthetic benchmark. 

**Belief:** To combine these modalities safely, we use a Bayesian belief engine with Dempster-Shafer fusion. If the RF and IR sensors disagree, the engine explicitly models that uncertainty, effectively penalizing the confidence score to reduce false alarms.

**The Dashboard & Results:** All of this is visualized on our React dashboard through a live WebSocket connection at 20Hz. In our local benchmarks, the simulation engine processed over 10,000 steps per second, and our PredictiveUCB scheduler successfully achieved a mean Age of Information of 4.34 across 10 random seeds.

**Limitation:** It is important to note that our current implementation is a software simulation. The datasets are synthetic, and while our Deep RL agents were explored, they require further tensor stabilization. Our next major milestone is migrating this validated simulation logic onto physical Over-The-Air SDR hardware.

Thank you."
