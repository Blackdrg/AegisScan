# Frontend Mock / Demo Data Audit

## Methodology
Searched the `dashboard/src` directory for terms: `mock`, `dummy`, `fake`, `placeholder`, `sample`, `hardcoded`, `Math.random`, `random(`, `TODO`, `FIXME`.

## Findings and Classifications

### 1. `mock_hardware` in API Types and Settings
- **Files**: `src/types/api.ts`, `src/features/hardware/LabHardwarePage.tsx`, `src/app/layout/TopBar.tsx`
- **Context**: Used to toggle between `lab` and `mock_hardware` mode.
- **Classification**: **A. REAL BACKEND DATA**
- **Action Taken**: None. The prompt explicitly states "MockSDR is intentional and must not be treated as a UI mock" (Rule 14).

### 2. `sample_rate_hz` / `sample_rates_hz`
- **Files**: `src/types/api.ts`, `src/features/recordings/RecordedDataPage.tsx`, `src/features/hardware/LabHardwarePage.tsx`
- **Context**: Backend variables for RF hardware sampling rates.
- **Classification**: **A. REAL BACKEND DATA**
- **Action Taken**: None.

### 3. `.placeholderText` / `.placeholderVis` / `.map-placeholder`
- **Files**: `OverviewPage.tsx`, `OverviewPage.module.css`, `EnvironmentDashboard.tsx`, `EnvironmentDashboard.css`
- **Context**: CSS classes and `div` wrappers for areas where a graph or map will render, or for empty states.
- **Classification**: **B. STATIC UI CONTENT**
- **Action Taken**: None. Intentionally used for structural styling.

### 4. `Math.random()` in WebSocket Client
- **Files**: `src/api/websocket.ts` (Line 156)
- **Context**: `const jitter = (Math.random() - 0.5) * 0.4 * this.reconnectDelay;`
- **Classification**: **B. STATIC UI CONTENT** (Operational networking logic)
- **Action Taken**: None. Expected networking backoff strategy.

### 5. `DemoMode.tsx` Synthetic Simulation Generator
- **Files**: `src/features/demo/DemoMode.tsx`
- **Context**: Uses `Math.random()` to generate a synthetic stream of `SIMULATION_TICK` events when the user starts the "Demo Tour".
- **Classification**: **C. DEMO/EXAMPLE DATA**
- **Action Taken**: Documented. This feature is explicitly bounded within `DemoMode` and does not affect the live system operation. As per rule 15 ("If a frontend feature is intentionally demo-only, document it instead of pretending it is live"), this is acceptable. The live dashboard depends on actual WebSocket data, while the Demo feature has its own encapsulated synthetic event injector.

## Conclusion
The live workflows (Overview, Simulation, Scheduling, Analytics) do not rely on mock or fake values. All data rendered during actual simulations flows directly from the WebSocket (`simWS`) and REST endpoints. The mock-like elements found are either intentional system configurations (`mock_hardware`), CSS layout placeholders, or explicitly segregated demo components (`DemoMode.tsx`).
