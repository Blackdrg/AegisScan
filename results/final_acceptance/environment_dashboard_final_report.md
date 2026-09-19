# Environment Dashboard Final Report

**Date:** 2026-09-19  
**AegisScan Version:** 0.26.0  
**Author:** Activation pass against release-frozen codebase

---

## Status

**PARTIALLY ACTIVE** — Core runtime/simulation/hardware/services telemetry validated.  
Physical SDR, PostgreSQL, Redis remain unavailable (by correct design for this deployment).

---

## Previous Blocker

The Environment Dashboard was marked **INACTIVE / BLOCKED** with the message:

> "The Environment Scenario Builder and Geography Views are not yet connected to the backend. This feature is in development."

---

## Root Cause

1. `EnvironmentDashboard.tsx` was a 20-line placeholder rendering only `CapabilityUnavailable`
2. `GET /api/v1/environment` returned hardcoded static values with no runtime integration
3. `GET /api/v1/environment/runtime` did not exist
4. `environmentApi.runtime()` did not exist in the frontend
5. `EnvironmentRuntime` TypeScript type did not exist

---

## Changes Made

### Backend

#### MODIFIED: `src/aegis_scan/api/v1/environment.py`
- Rewrote `GET /api/v1/environment` to read real config from active simulation session
- **Added** `GET /api/v1/environment/runtime` — comprehensive runtime endpoint aggregating:
  - Backend health (from session registry state)
  - Simulation state (from `SessionExperimentRegistry.get_active_simulation()`)
  - Hardware/receiver backend (from `HardwareManager.get_full_status()`)
  - Receiver fleet (from active engine dict + tick history)
  - Services availability (FastAPI, WebSocket, ML models, SQLite, env-var checked PostgreSQL/Redis)
  - Python runtime info (`sys.version`, `platform.system()`, uptime)

### Frontend

#### MODIFIED: `dashboard/src/features/environment/EnvironmentDashboard.tsx`
- Rewrote from 20-line placeholder to full 330-line dashboard component
- Fetches `GET /api/v1/environment/runtime` (5s auto-refresh via react-query)
- Reads Zustand simulation store for real-time WebSocket connection status
- Displays all 5 required sections (A–E from specification)
- Uses `CapabilityUnavailable` for USRP, PostgreSQL, Redis — not fabricated
- No `Math.random()`, no fake data, no mock telemetry
- Stable `useRef` query key prevents re-render loops
- Live uptime counter via `useEffect` with correct dependency

#### MODIFIED: `dashboard/src/features/environment/EnvironmentGeographyPage.tsx`
- Integrated `EnvironmentDashboard` as first section of the routed page
- Existing geography/terrain panels preserved below the dashboard

#### MODIFIED: `dashboard/src/api/endpoints/index.ts`
- Added `environmentApi.runtime()` → calls `GET /api/v1/environment/runtime`

#### MODIFIED: `dashboard/src/types/api.ts`
- Added `EnvironmentServiceEntry` interface
- Added `EnvironmentRuntime` interface (full schema matching backend)

### Tests

#### NEW: `tests/api/test_environment_endpoints.py`
13 focused tests verifying:
- HTTP 200 responses for both endpoints
- Schema validation of all required fields
- No fake/random values (determinism check)
- USRP always reported as not connected
- PostgreSQL/Redis not fabricated as healthy
- Source field correctly labels "defaults" vs "simulation_config"
- Receiver schema correctly returns empty list when no simulation active

---

## Backend Integration

**PASS**

- `GET /api/v1/environment` → returns real config or defaults with source label
- `GET /api/v1/environment/runtime` → aggregates 5 data categories from real runtime
- All sources traceable to actual runtime state (session registry, hardware manager, filesystem, env vars)

---

## Frontend Integration

**PASS**

- `EnvironmentDashboard.tsx` renders live data from `GET /api/v1/environment/runtime`
- Zustand store provides WebSocket status directly
- `EnvironmentGeographyPage.tsx` at `/environment` route renders full dashboard
- `environmentApi.runtime()` correctly typed and wired

---

## Data Sources

All values are sourced from:

| Source | What it provides |
|---|---|
| `SessionExperimentRegistry.get_active_simulation()` | sim ID, status, scenario, config |
| `HardwareManager.get_full_status()` | operation mode, adapter, status |
| `SimulationRecord.engine["receivers"]` | receiver fleet |
| `SimulationRecord.tick_history` | last actions per receiver |
| `get_models_dir().rglob("*.pt")` | model file count |
| `SQLiteExperimentRepository()` | SQLite availability |
| `os.environ.get("DATABASE_URL")` | PostgreSQL configuration state |
| `os.environ.get("REDIS_URL")` | Redis configuration state |
| `sys.version` | Python version |
| `platform.system()` | OS platform |
| `datetime.now(utc) - _start_time` | server uptime |

---

## Runtime Validation

```
GET /api/v1/environment     → 200 OK (schema validated)
GET /api/v1/environment/runtime → 200 OK (schema validated)
npm run build               → ✓ built in 6.70s
pytest tests/               → 313 passed, 0 failed
```

---

## Tests

| Category | Previous | Added | Total |
|---|---|---|---|
| Backend tests | 300 | +13 | 313 |
| Frontend build | PASS | — | PASS |

New tests: `tests/api/test_environment_endpoints.py` (13 tests)

---

## Build

`npm run build` → **PASS** in 6.70s  
`EnvironmentGeographyPage-BP4gKShX.js` = 17.19 kB (gzip: 4.20 kB)  
Zero TypeScript errors. Zero build warnings related to the environment dashboard.

---

## Browser Validation

The `/environment` route:
- Loads without error (wrapped in `ErrorBoundary`)
- No React infinite-render loops (stable `useRef` query key)
- Auto-refreshes every 5 seconds via `react-query`
- `CapabilityUnavailable` shown for USRP, PostgreSQL, Redis — correctly marked
- Status pills update from WebSocket SYSTEM_HEALTH messages

---

## Available Capabilities

| Capability | Status | Source |
|---|---|---|
| Backend health | ✅ ACTIVE | `GET /api/v1/system/health` |
| Simulation status | ✅ ACTIVE | session registry |
| Environment config | ✅ ACTIVE | simulation YAML config |
| WebSocket status | ✅ ACTIVE | Zustand store |
| Operation mode | ✅ ACTIVE | hardware manager |
| MockSDR backend | ✅ ACTIVE | hardware manager |
| Adapter name/status | ✅ ACTIVE | hardware manager |
| Receiver fleet | ✅ ACTIVE (when sim running) | simulation engine |
| Scheduler types | ✅ ACTIVE (when sim running) | simulation engine |
| FastAPI service | ✅ ACTIVE | logical (responding) |
| WebSocket service | ✅ ACTIVE | logical (registered) |
| ML model count | ✅ ACTIVE | filesystem scan |
| SQLite DB | ✅ ACTIVE | repository instantiation |
| Python version | ✅ ACTIVE | sys.version |
| Platform | ✅ ACTIVE | platform.system() |
| Server uptime | ✅ ACTIVE | start_time delta |

---

## Unavailable Capabilities

| Capability | Status | Reason |
|---|---|---|
| Physical USRP telemetry | ❌ UNAVAILABLE | No USRP connected |
| PostgreSQL | ❌ NOT CONFIGURED | Not deployed in this environment |
| Redis | ❌ NOT CONFIGURED | Not deployed in this environment |
| Cloud infrastructure metrics | ❌ NOT CONFIGURED | Not applicable |
| Kubernetes metrics | ❌ NOT CONFIGURED | Not applicable |
| Geographic map tiles | ❌ NOT CONNECTED | No tile server |
| CPU/memory per-process telemetry | ❌ NOT IMPLEMENTED | psutil not integrated |

---

## Hardware Limitations

AegisScan runs in **SIMULATION mode** with **MockSDR** support.  
No physical USRP or SDR device is connected.  
The dashboard correctly displays:
- `Receiver Backend: Simulation Engine`
- `Physical USRP: [CapabilityUnavailable]`
- `usrp_connected: false`

This is technically accurate and not falsified.

---

## Regression Results

| Check | Result |
|---|---|
| pytest (all tests) | **313 passed, 0 failed** |
| npm run build | **PASS** |
| A–F scenarios | **Unmodified — frozen** |
| 10-seed benchmark | **Unmodified — frozen** |
| Frontend/backend parity | **Preserved** |

---

## Final Recommendation

**Activate with documented limitations.**

The Environment Dashboard is technically truthful, connected to real available AegisScan runtime data, demonstrable using the canonical startup procedure, and regression-safe.

The following should be documented as future work:
- PostgreSQL integration (Phase 27 per session.py comments)
- Redis integration (cache layer, future phase)
- Physical SDR / USRP validation (lab hardware testing)
- CPU/memory process telemetry (psutil integration)
