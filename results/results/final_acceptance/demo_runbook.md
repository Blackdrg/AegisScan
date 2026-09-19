# AegisScan Demo Runbook

## Demo Startup
1. Open a terminal and navigate to `Aeronotics/aegis-scan`
2. Start the backend: `start.bat` (or manually run `python -m src.api.server`)
3. Open another terminal and navigate to `Aeronotics/aegis-scan/dashboard`
4. Start the frontend: `npm run dev`
5. Open the browser to `http://localhost:5173`

## Demo Sequence
1. **Simulation Initialization**: Start by opening the dashboard overview. 
2. **Spectrum Overview**: Show the live spectrum page to observe broad RF activity.
3. **Receiver State**: Switch to the Receivers page to show receiver availability.
4. **Detection & Bayesian Belief**: Navigate to the Intelligence Engine to show emitter beliefs evolving over time.
5. **AoI / WAoI & Scheduler Decision**: Show the Band Scheduling page. Highlight the scheduler prioritizing bands based on Age of Information.
6. **Receiver Tunes Selected Band & Next Observation**: Show timeline logs confirming receivers tuning to scheduler-selected bands.
7. **Feedback/reward & Next Action**: Observe scheduler adjusting policy on successful detection versus empty bands.

## What Judges Should Observe
Judges should observe the system autonomously selecting which RF bands to scan based on the current age of information and historical belief of emitter presence. They should see dynamic tuning and detection metrics updating in real-time.

## Scenario Demonstration
Use **Scenario A** (Single Stable Emitter) to explain the baseline behavior, then switch to **Scenario C** (Intermittent Emitter, 5 ON / 5 OFF) to demonstrate adaptive tracking under uncertainty.

## Recovery Procedure
- **Backend does not start**: Ensure virtual environment is activated and dependencies installed. Check port 8000.
- **WebSocket disconnects**: Refresh the browser page. The frontend has automatic reconnect logic.
- **Simulation stops**: Restart the backend API server.
- **Frontend fails to load**: Check Node.js process and ensure no port conflict on 5173.
- **Model fails to load**: Ensure `models/` directory contains the correct weights and configurations.

*Note: Do not create fake fallback telemetry. If the system fails, transparently debug using timeline logs.*
