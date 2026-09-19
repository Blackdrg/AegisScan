# SIH Demonstration Runbook

## Objective
This runbook defines the ONE deterministic, validated path to be executed live during the SIH 2026 presentation.

## Demonstration Architecture Path
`Scenario` → `RF/IR Sensing` → `Energy/CNN/CA-CFAR Detection` → `Belief` → `AoI/WAoI` → `PredictiveUCB` → `Simulation` → `WebSocket` → `Dashboard` → `Analytics`

## Live Execution Steps

### 1. System Startup
- Run `start.bat` to boot the FastAPI backend (Port 8000).
- Run `npm run dev` to boot the Vite frontend (Port 5173).
- **Check**: Open `http://localhost:5173`. Ensure System Health badge in the top right is **ONLINE**.

### 2. Simulation Execution
- Navigate to the **Simulation** tab.
- Select the `Two Periodic Emitters` or `Static Targets` scenario.
- Select the **PredictiveUCB** scheduler.
- Click **Start Simulation**.
- **Check**: The judges should see the simulation state transition to `RUNNING`.

### 3. Real-Time Telemetry (The "Wow" Factor)
- Navigate immediately to the **Overview** or **Detection** tab.
- Explain the real-time WebSocket connection updating the charts at 20Hz.
- Point out the False Alarm Rate (Pfa) settling around the 5% target limit (proving the CA-CFAR configuration).
- Point out the Belief Engine's multimodal fusion successfully tracking the targets.

### 4. Final Analytics
- Once the simulation hits 100%, navigate to **Analytics**.
- Demonstrate the quantitative performance: 
  - Mean AoI settling around ~4.34.
  - High probability of detection (>96%).

### 5. Benchmark & Scalability
- Navigate to the **Experiments** / **RL Benchmark** tab.
- Show the previously run 10-seed benchmarks, demonstrating that the engine runs 10,000x faster than real-time when detached from the UI, solving the massive computational constraints of EW processing.

## Backup Path (Hardware Failure)
If the presentation laptop fails or SDR hardware is disconnected, the system is designed to gracefully fallback to `MockSDRDriver` (Lab Mode). This mode runs the exact same software logic, guaranteeing a successful software demonstration regardless of external environmental RF noise.
