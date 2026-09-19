# Environment Dashboard Audit

**Date:** 2026-09-19  
**AegisScan Version:** 0.26.0  
**Audit Type:** Pre-activation — root cause investigation

---

## 1. Existing Frontend Implementation

### Primary Component
**File:** `dashboard/src/features/environment/EnvironmentDashboard.tsx`  
**Status before activation:** 20 lines — 100% placeholder

```tsx
export const EnvironmentDashboard: React.FC = () => {
  return (
    <div style={{ padding: 'var(--space-6)' }}>
      <EngineeringPanel>
        <PanelHeader title="Environment-Aware Adaptive Sensing" />
        <PanelBody>
          <CapabilityUnavailable
            title="Environment Dashboard"
            detail="The Environment Scenario Builder and Geography Views are not yet
                    connected to the backend. This feature is in development."
          />
        </PanelBody>
      </EngineeringPanel>
    </div>
  );
};
```

> **Finding:** The `EnvironmentDashboard` component was a static placeholder.  
> It made **zero API calls**. It rendered only `CapabilityUnavailable`.

### Secondary Component (Already Functional)
**File:** `dashboard/src/features/environment/EnvironmentGeographyPage.tsx`  
**Status before activation:** Partially connected — fetched `/api/v1/environment` and `/api/v1/geography/map`

The `EnvironmentGeographyPage` was the **actual routed component** at `/environment`.  
It rendered terrain/noise/fading/disturbance metrics from the backend.  
However, this page did NOT display:
- Backend health
- Simulation active state
- Hardware mode / receiver backend
- Service availability (PostgreSQL, Redis, ML models, SQLite)
- WebSocket connection status
- Receiver fleet status
- Python runtime info

### Routing
**File:** `dashboard/src/app/router/index.tsx` (line 99–103)

```tsx
<Route path="/environment" element={
  <ErrorBoundary moduleName="Environment & Geography">
    <EnvironmentGeographyPage />
  </ErrorBoundary>
} />
```

The `EnvironmentDashboard` component was **imported but never used in routing**.

### Zustand Stores
Only `stores/simulation.ts` exists — tracks `activeSim`, `wsConnected`, `systemOnline`, `operationMode`, `recentTicks`.  
No dedicated environment Zustand store was needed (simulation store already exposes needed state).

### API Client (Before Activation)
```ts
export const environmentApi = {
  state: () => api.get<EnvironmentState>('/environment'),  // only this
};
```

Missing: No `runtime`, `health`, `receivers`, or `services` call.

### TypeScript Types
`EnvironmentState` existed (terrain, noise, fading, etc.) but **`EnvironmentRuntime` was absent**.

---

## 2. Existing Backend Implementation

### `/api/v1/environment` (Before Activation)
**File:** `src/aegis_scan/api/v1/environment.py`

```python
@router.get("")
async def get_environment_state():
    return {
        "terrain": "Mountainous",       # HARDCODED
        "noise": 0.18,                  # HARDCODED
        "fading": 0.24,                 # HARDCODED
        "disturbance": 0.09,            # HARDCODED
        "temporal_activity": "Periodic",# HARDCODED
        "uncertainty": 0.07,            # HARDCODED
        "available": True,
    }
```

> **Finding:** Entire endpoint was hardcoded. Values did not reflect active simulation config.

**No `/api/v1/environment/runtime` endpoint existed.**

---

## 3. Existing Endpoints Available for Integration

The following real endpoints already existed and were usable for the Environment Dashboard:

| Endpoint | What it provides |
|---|---|
| `GET /api/v1/system/health` | API status, engine status, uptime |
| `GET /api/v1/system/info` | Python version, platform, AegisScan version |
| `GET /api/v1/hardware/status` | Operation mode, adapter, capabilities |
| `GET /api/v1/receivers` | Receiver fleet from active simulation |
| `GET /api/v1/scheduling/current` | Scheduler decisions per receiver |
| `GET /api/v1/simulations` | Session registry listing |
| `GET /api/v1/models` | Scans real model files on disk |
| `GET /api/v1/environment` | Environment state (was hardcoded) |
| `GET /api/v1/geography/map` | Static geography zones |
| `WS /ws/v1/system` | System health broadcast (5s) |
| `WS /ws/v1/hardware` | Hardware status broadcast (5s) |

---

## 4. Missing Endpoints (Before Activation)

| Missing Endpoint | Reason |
|---|---|
| `GET /api/v1/environment/runtime` | Did not exist — aggregates system/hardware/receivers/services |

---

## 5. Missing Environment Configuration

None required. The existing configuration system was sufficient:
- Session registry exposes simulation config (`config.environment.*`, `config.experiment.*`)
- Hardware manager exposes operation mode
- Path utilities expose model/data directories
- Environment variables `DATABASE_URL` and `REDIS_URL` checked for optional services

---

## 6. Missing Dependencies

None. All needed Python modules were already present:
- `fastapi`, `platform`, `sys`, `datetime` — standard
- `aegis_scan.api.session.registry` — existing
- `aegis_scan.hardware.manager.hardware_manager` — existing
- `aegis_scan.paths.get_models_dir` — existing
- `aegis_scan.persistence.sqlite_repository` — existing

---

## 7. Missing Runtime Services

| Service | Missing? | Reason |
|---|---|---|
| FastAPI | No | Always present |
| WebSocket | No | Always present |
| SQLite | No | Persistence layer exists |
| PostgreSQL | Yes (by design) | Not configured — documented as future phase |
| Redis | Yes (by design) | Not configured — documented as future phase |
| Physical USRP | Yes (by design) | No hardware present |

---

## 8. What Can Be Activated Safely

| Capability | Source |
|---|---|
| Backend health | `/api/v1/system/health` |
| Simulation state | session registry |
| Environment config | active simulation config |
| WebSocket status | Zustand store |
| Operation mode | hardware manager |
| Receiver backend label | hardware manager |
| Adapter name/status | hardware manager |
| Receiver fleet | active simulation engine |
| Scheduler types | active simulation engine |
| ML model count | filesystem scan via `get_models_dir()` |
| Data store path | `get_data_dir()` |
| SQLite availability | `SQLiteExperimentRepository` instantiation |
| Python version | `sys.version` |
| Platform | `platform.system()` |
| Uptime | computed from server start time |

---

## 9. What Cannot Be Activated Without New Infrastructure

| Capability | Reason |
|---|---|
| Physical USRP telemetry | No USRP connected |
| PostgreSQL status | Not configured in this deployment |
| Redis status | Not configured in this deployment |
| Cloud infrastructure metrics | No cloud monitoring |
| Kubernetes metrics | No Kubernetes environment |
| Real-time CPU/memory per-process | Not implemented without psutil |
| Geographic map tiles | No tile server |

---

## Root Cause Summary

The Environment Dashboard was marked **INACTIVE / BLOCKED** because:

1. The `EnvironmentDashboard.tsx` component was a 20-line placeholder rendering only `CapabilityUnavailable`
2. The backend `/api/v1/environment` endpoint returned only hardcoded static values with no runtime integration
3. No `/api/v1/environment/runtime` endpoint existed to aggregate system/hardware/services state
4. The `environmentApi` only had a `state()` method — no `runtime()` method
5. The `EnvironmentRuntime` TypeScript type did not exist

**All these blockers have been resolved without touching validated algorithms, tests, or architectural components.**
