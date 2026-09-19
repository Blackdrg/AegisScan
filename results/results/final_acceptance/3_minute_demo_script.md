# 3-Minute Demo Script

## 0:00–0:30: Problem
"Hello judges, we are presenting AegisScan. Traditional wide-spectrum scanning wastes critical time sweeping empty frequencies. When looking for intermittent or agile targets, you can't afford to look everywhere at once. Our solution stops blind sweeping and starts intelligent, adaptive scheduling."

## 0:30–1:00: Architecture
"AegisScan uses a Bayesian intelligence engine combined with Reinforcement Learning. As receivers detect signals, our system updates its belief of where targets are. The scheduler then balances exploiting known active bands and exploring unknown bands based on the Age of Information."

## 1:00–2:15: Live Demonstration
"(Switch to Dashboard) Here is the live spectrum. Notice how the scheduler isn't just sweeping left to right. It focuses on Band 2 because our Intelligence Engine (point to Bayesian belief chart) has high confidence a target is there.
(Switch to Scenario C) Now we introduce an intermittent target that turns on and off. Watch the belief decay when it's off, and see how the scheduler periodically checks back (based on Age of Information) and catches it the moment it turns back on."

## 2:15–2:45: Benchmark & Validation Evidence
"We validated this rigorously. Our continuous integration runs over 300 tests. Across 10 deterministic benchmark seeds, our system consistently improves Probability of Detection (Pd) over sequential scanning, maintaining sub-millisecond scheduling latency."

## 2:45–3:00: Impact & Future Deployment
"AegisScan provides a software-defined intelligence layer ready for hardware integration. While our current validation uses synthetic data, our architecture natively supports SoapySDR. The next step is deploying this directly onto physical USRP hardware for field-ready electronic warfare and spectrum monitoring. Thank you."
