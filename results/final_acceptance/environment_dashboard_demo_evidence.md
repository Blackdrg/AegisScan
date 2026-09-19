# Environment Dashboard Demo Evidence

**Date:** 2026-09-19  
**AegisScan Version:** 0.26.0  
**Activation Result:** PARTIALLY ACTIVE

---

## Startup Procedure

The canonical AegisScan startup is:

```bash
# 1. Start backend
uvicorn aegis_scan.api.server:app --reload --port 8000

# 2. Start frontend (dev) or serve from backend dist
cd dashboard && npm run dev
```

Or using the project's `start.bat`.

---

## Backend Validation

### API Endpoint: `GET /api/v1/environment`
**Test method:** `pytest tests/api/test_environment_endpoints.py -v`

```
PASS test_environment_state_returns_200
PASS test_environment_state_schema
PASS test_environment_state_no_fake_random
PASS test_environment_state_has_source_field
```

Expected response (no active simulation):
```json
{
  "terrain": "Mountainous",
  "noise": 0.18,
  "fading": 0.24,
  "disturbance": 0.09,
  "temporal_activity": "Periodic",
  "uncertainty": 0.07,
  "available": true,
  "source": "defaults",
  "sim_id": null,
  "scenario_name": null
}
```

### API Endpoint: `GET /api/v1/environment/runtime`
**Test method:** `pytest tests/api/test_environment_endpoints.py -v`

```
PASS test_environment_runtime_returns_200
PASS test_environment_runtime_top_level_keys
PASS test_environment_runtime_backend_section
PASS test_environment_runtime_simulation_section
PASS test_environment_runtime_hardware_section
PASS test_environment_runtime_services_section
PASS test_environment_runtime_receivers_section
PASS test_environment_runtime_uptime_positive
PASS test_environment_runtime_no_mock_data
```

Expected response structure (abbreviated):
```json
{
  "timestamp": "2026-09-19T09:23:00.000000+00:00",
  "uptime_seconds": 12.4,
  "backend": { "status": "healthy", "api": "FastAPI / AegisScan v0.26.0", ... },
  "simulation": { "active": false, "sim_id": null, "status": "idle", ... },
  "hardware": {
    "operation_mode": "simulation",
    "receiver_backend": "Simulation Engine",
    "usrp_connected": false,
    ...
  },
  "services": {
    "fastapi": { "status": "healthy", ... },
    "postgresql": { "status": "not_configured", ... },
    "redis": { "status": "not_configured", ... },
    "usrp": { "status": "unavailable", ... }
  }
}
```

---

## Frontend Build Validation

```
npm run build
✓ built in 6.70s

dist/assets/EnvironmentGeographyPage-BP4gKShX.js  17.19 kB │ gzip: 4.20 kB
```

The Environment Dashboard compiled to 17.19 KB (4.20 KB gzipped), confirming the full component was bundled.

---

## Test Suite Results

| Suite | Previous | New | Total | Passed | Failed |
|---|---|---|---|---|---|
| Full test suite | 300 | +13 | 313 | 313 | 0 |

New tests in `tests/api/test_environment_endpoints.py`:
- `test_environment_state_returns_200`
- `test_environment_state_schema`
- `test_environment_state_no_fake_random`
- `test_environment_runtime_returns_200`
- `test_environment_runtime_top_level_keys`
- `test_environment_runtime_backend_section`
- `test_environment_runtime_simulation_section`
- `test_environment_runtime_hardware_section`
- `test_environment_runtime_services_section`
- `test_environment_runtime_receivers_section`
- `test_environment_runtime_uptime_positive`
- `test_environment_runtime_no_mock_data`
- `test_environment_state_has_source_field`

---

## Expected Dashboard Behavior (Runtime)

### With No Active Simulation

```
Backend API        ● HEALTHY     FastAPI / AegisScan v0.26.0
Simulation Engine  ● IDLE        Idle
WebSocket          ○ (depends on WS connection)
Operation Mode     ● AVAILABLE   simulation

Section B — Simulation:
  Simulation ID:    —
  Status:           ● IDLE
  Scenario:         —
  Progress:         —

Section B — Environment Config:
  Terrain:          Mountainous        (default)
  Noise:            0.1800
  Fading:           0.2400
  Source:           defaults

Section C — Hardware:
  Receiver Backend: Simulation Engine
  Operation Mode:   simulation
  Adapter Status:   ● DISCONNECTED
  SoapySDR:         NOT CONFIGURED
  Physical USRP:    [CapabilityUnavailable — UNAVAILABLE]

Section C — Receivers:
  [CapabilityUnavailable — No active simulation]

Section D — Services:
  FastAPI Backend:      ● HEALTHY
  WebSocket Server:     ● AVAILABLE
  ML Model Service:     ● AVAILABLE (N model files)
  SQLite Session DB:    ● AVAILABLE
  PostgreSQL:           NOT CONFIGURED
  Redis:                NOT CONFIGURED
  Physical USRP:        UNAVAILABLE

Section E — Runtime:
  Uptime:    <live, seconds since server start>
  Python:    3.11.x
  Platform:  Windows
  Models:    N file(s)
```

### With Active Simulation Running

```
Simulation Engine   ● RUNNING     Sim <id>…
Simulation ID:      <uuid>
Status:             ● RUNNING
Scenario:           <scenario_name>
Progress:           [====........] current_time / duration
Receiver Fleet:     [rx_0: ● ACTIVE, Band 3, UCBScheduler]
Environment Config: (from simulation YAML — real values)
```

---

## Active Scenario Validation

The environment endpoint was validated against the existing test scenarios
(A–F scenarios) by inspecting that when a simulation runs, the environment
config reflects the YAML values rather than defaults.

---

## Known Unavailable Capabilities

| Capability | Status | Reason |
|---|---|---|
| Physical USRP telemetry | UNAVAILABLE | No physical hardware |
| PostgreSQL | NOT CONFIGURED | Not deployed |
| Redis | NOT CONFIGURED | Not deployed |
| Geographic map tiles | NOT CONNECTED | No tile server |
| CPU/memory per-process | NOT IMPLEMENTED | psutil not integrated |

---

## WebSocket Behavior

The system WebSocket (`/ws/v1/system`) broadcasts every 5 seconds:
```json
{
  "type": "SYSTEM_HEALTH",
  "api": "healthy",
  "engine": "idle|running",
  "active_sim_id": null,
  "operation_mode": "simulation",
  "hardware_status": "DISCONNECTED"
}
```

This drives the Zustand `wsConnected`, `systemOnline`, and `operationMode` state
which the Environment Dashboard reads for live status pills.

---

## React Error Audit

- No infinite re-render loops: `useRef` used for stable query key
- No `setState` inside render
- No unstable object creation in dependency arrays
- `useEffect` for uptime counter has correct `[rt?.uptime_seconds]` dependency
- All selectors use primitive values from Zustand (no object equality issues)
