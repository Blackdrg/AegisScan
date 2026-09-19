# AegisScan: SIH Project Description

## Problem
Existing wide-spectrum scanning can waste scan time when emitter intelligence is incomplete or outdated. Traditional sequential scanning is highly inefficient in sparse RF environments or when targets are intermittent and agile.

## Solution
AegisScan adaptively allocates scanning effort using:
- Signal detection
- CNN-assisted classification
- Bayesian belief updates
- AoI/WAoI (Age of Information)
- UCB/LinUCB/Thompson baselines
- DQN-based scheduling
- Receiver orchestration
- Live monitoring

## Technical Novelty
Our novelty lies in the system-level integration of:
Detection + Emitter belief + Information age + Adaptive scheduling + Receiver feedback.
Instead of treating detection and scheduling as separate problems, AegisScan tightly couples them—the scheduler uses the Bayesian belief of emitter presence and the staleness of prior scans (Age of Information) to make optimal scanning decisions, maximizing the Probability of Detection (Pd).

## Prototype
The current working prototype consists of a Python-based backend providing RF environment simulation, signal processing, and an RL-driven scheduling engine. A React-based frontend dashboard provides real-time telemetry, live spectrum visualization, and intelligence tracking over WebSockets.

## Validation
- 300+ tests passed
- Validated on Scenarios A–F
- 10 deterministic seeds evaluated
- Backend/frontend parity verified
- Reproducible benchmarks generated

## Limitations
- Evaluation is currently limited to synthetic RF dataset generation.
- No physical USRP/SDR validation has been performed yet.
- SoapySDR fallback is currently used for hardware abstraction.
- Environment Dashboard is inactive.
- Extremely short discrete detection impulses sometimes fall under the simulation engine metrics tracker, producing lower perceived end-to-end Pd values even though the underlying detector triggers hits (known discrete-time model limitation).

## Future Deployment
- Integration with physical SDR platforms.
- Testing with USRP/compatible hardware.
- Validation using real RF/IQ datasets.
- Hardware-in-the-loop validation.
- Field testing for operational readiness.
