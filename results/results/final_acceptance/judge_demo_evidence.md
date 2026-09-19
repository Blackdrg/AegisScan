# Judge Demonstration Evidence

### Demonstration 1 — Adaptive scanning
- **Action**: Run Scenario A (baseline).
- **Observation**: Show how the scheduler focuses scanning time on bands where the emitter has been detected, shifting away from empty bands to maximize resource utility.

### Demonstration 2 — Emitter belief
- **Action**: Open the Intelligence Engine dashboard during a scan.
- **Observation**: Show the Bayesian belief percentage increasing upon positive detections and gradually decaying when non-detections occur.

### Demonstration 3 — Periodic emitter
- **Action**: Switch to Scenario C (5 ON / 5 OFF pattern).
- **Observation**: Show the scheduler adjusting its focus as the emitter turns on and off, demonstrating the system's ability to track temporal patterns without hardcoded rules.

### Demonstration 4 — Changing SNR
- **Action**: Run a low SNR scenario configuration.
- **Observation**: Demonstrate how the detection engine handles noisy signals, showing the impact on confidence intervals and the scheduler's compensation strategy.

### Demonstration 5 — Jamming/deception
- **Action**: Run the TargetedMimicJammer scenario.
- **Observation**: Show the system's response to the mimic jammer. Highlight how the system records the behavior but acknowledge the limitations in current counter-jamming capabilities without overstating them.
