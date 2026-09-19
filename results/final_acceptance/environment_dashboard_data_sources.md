# Environment Dashboard — Data Sources Traceability

**Date:** 2026-09-19  
**AegisScan Version:** 0.26.0

Every value displayed in the Environment Dashboard must have a traceable source.
No `Math.random()`. No hardcoded telemetry. No mock/demo data.

---

## Section A — Backend Connectivity

### Backend Status
```
UI field: "Backend API" status pill
↓ frontend: systemApi.health() → Zustand systemOnline
↓ backend: GET /api/v1/system/health
↓ source: FastAPI application state — returns "healthy" when responding
```

### Simulation Engine Status
```
UI field: "Simulation Engine" status pill
↓ frontend: useSimulationStore activeSim.status OR health.engine.status
↓ backend: GET /api/v1/system/health → { engine: { status: "running"|"idle" } }
           AND GET /api/v1/environment/runtime → simulation.status
↓ source: session registry → get_active_simulation() check
```

### WebSocket Status
```
UI field: "WebSocket" status pill
↓ frontend: useSimulationStore wsConnected (set by WebSocket onopen/onclose)
↓ source: AegisWebSocket connection state — directly from browser WebSocket API
```

### Operation Mode
```
UI field: "Operation Mode" info chip
↓ frontend: GET /api/v1/environment/runtime → hardware.operation_mode
           OR useSimulationStore operationMode (from SYSTEM_HEALTH WS message)
↓ backend: hardware_manager.mode.value → OperationMode enum
↓ source: HardwareManager._mode — defaults to SIMULATION
```

---

## Section B — Active Environment / Simulation

### Simulation ID
```
UI field: "Simulation ID"
↓ frontend: GET /api/v1/environment/runtime → simulation.sim_id
↓ backend: registry.get_active_simulation().sim_id
↓ source: SessionExperimentRegistry → SQLiteExperimentRepository
```

### Simulation Status
```
UI field: "Status" pill
↓ frontend: GET /api/v1/environment/runtime → simulation.status
↓ backend: registry.get_active_simulation().status.value
↓ source: SimulationStatus enum (PENDING/RUNNING/PAUSED/COMPLETE/FAILED/STOPPED)
```

### Scenario Name
```
UI field: "Scenario"
↓ frontend: GET /api/v1/environment/runtime → simulation.scenario_name
↓ backend: registry.get_active_simulation().scenario_name
↓ source: scenario YAML loaded during simulation creation
```

### Terrain Type
```
UI field: "Terrain Type" (both Section B and Environment Config)
↓ frontend: GET /api/v1/environment/runtime → environment_config.terrain
           OR GET /api/v1/environment → terrain
↓ backend: active simulation config["environment"].get("terrain_type", "Mountainous")
↓ source: simulation YAML config → environment.terrain_type field
```

### Noise / Fading / Disturbance / Uncertainty
```
UI field: Metric cards in environment config
↓ frontend: GET /api/v1/environment/runtime → environment_config.{noise,fading,disturbance,uncertainty}
↓ backend: active simulation config["environment"] fields
↓ source: simulation YAML → environment.{noise_level, fading_factor, disturbance_score, uncertainty_index}
          Falls back to: 0.18, 0.24, 0.09, 0.07 (scenario defaults, not random)
```

### Progress Bar
```
UI field: "Progress" (current_time / duration bar)
↓ frontend: GET /api/v1/environment/runtime → simulation.{current_time, duration}
↓ backend: record.current_time (updated per tick) / record.duration (from config)
↓ source: SimulationRecord.current_time incremented in _run_simulation loop
```

---

## Section C — Hardware / Receiver Backend

### Operation Mode
```
UI field: "Operation Mode" chip
↓ frontend: GET /api/v1/environment/runtime → hardware.operation_mode
↓ backend: hardware_manager.get_full_status()["mode"]
↓ source: HardwareManager._mode.value → OperationMode enum
```

### Receiver Backend Label
```
UI field: "Receiver Backend"
↓ frontend: GET /api/v1/environment/runtime → hardware.receiver_backend
↓ backend: _get_hardware_context() — classified from operation_mode:
           simulation → "Simulation Engine"
           mock_hardware → "MockSDR (adapter_name)"
           lab_hardware → "LabSDR (adapter_name)"
           physical_hardware → "Physical SDR (adapter_name)"
↓ source: HardwareManager._mode + adapter_name from capabilities
```

### Adapter Status
```
UI field: "Adapter Status" pill
↓ frontend: GET /api/v1/environment/runtime → hardware.adapter_status
↓ backend: active_adapter.get_status().value (ReceiverStatus enum)
           OR "DISCONNECTED" when no adapter active (simulation mode)
↓ source: MockReceiverAdapter / LabReceiverAdapter state
```

### SoapySDR Available
```
UI field: "SoapySDR" status pill
↓ frontend: GET /api/v1/environment/runtime → hardware.soapysdr_available
↓ backend: mode in (lab_hardware, physical_hardware, mock_hardware)
↓ source: HardwareManager._mode — SoapySDR only relevant in hardware modes
```

### USRP Connected
```
UI field: Physical USRP — CapabilityUnavailable
↓ frontend: GET /api/v1/environment/runtime → hardware.usrp_connected (always False)
↓ backend: hardcoded False — no physical USRP validation exists
↓ source: N/A — documented as UNAVAILABLE
NOTE: USRP can NEVER be shown as connected without physical device validation.
```

### Receiver Fleet
```
UI field: Receiver cards (ID, status, band, scheduler)
↓ frontend: GET /api/v1/environment/runtime → receivers.receivers[]
↓ backend: active_simulation.engine["receivers"] dict
           last_action from record.tick_history
↓ source: MultiAgentSimulationEngine receiver dict + tick history
```

---

## Section D — Services

### FastAPI
```
UI field: "FastAPI Backend" service row
↓ frontend: GET /api/v1/environment/runtime → services.fastapi
↓ backend: status = "healthy" (constant — backend is responding)
↓ source: logical — if endpoint responds, FastAPI is healthy
```

### WebSocket Server
```
UI field: "WebSocket Server" service row
↓ frontend: GET /api/v1/environment/runtime → services.websocket
↓ backend: status = "available" (constant — ws_router mounted at startup)
↓ source: router.py — WebSocket endpoints always registered
```

### ML Model Service
```
UI field: "ML Model Service" + model count
↓ frontend: GET /api/v1/environment/runtime → services.ml_model_service.model_count
↓ backend: len(list(models_dir.rglob("*.pt")) + rglob("*.pth") + rglob("*.onnx"))
↓ source: filesystem scan of get_models_dir()
```

### SQLite Session DB
```
UI field: "SQLite Session DB" service row
↓ frontend: GET /api/v1/environment/runtime → services.sqlite_session
↓ backend: SQLiteExperimentRepository() instantiation test
↓ source: persistence/sqlite_repository.py
```

### PostgreSQL
```
UI field: "PostgreSQL" service row — shows NOT CONFIGURED
↓ frontend: GET /api/v1/environment/runtime → services.postgresql
↓ backend: os.environ.get("DATABASE_URL", "") — checks env var only
↓ source: environment variable (not configured → "not_configured")
NOTE: NOT fabricated as healthy. Shows actual configuration state.
```

### Redis
```
UI field: "Redis" service row — shows NOT CONFIGURED
↓ frontend: GET /api/v1/environment/runtime → services.redis
↓ backend: os.environ.get("REDIS_URL", "") — checks env var only
↓ source: environment variable (not configured → "not_configured")
NOTE: NOT fabricated as healthy. Shows actual configuration state.
```

---

## Section E — Runtime Information

### Uptime
```
UI field: "Uptime" (live, auto-increments every 5s in UI)
↓ frontend: GET /api/v1/environment/runtime → uptime_seconds
           then useEffect increments locally between API calls
↓ backend: (datetime.now(utc) - _start_time).total_seconds()
↓ source: system.py → _start_time = datetime.now(timezone.utc) at module load
```

### Python Version
```
UI field: "Python"
↓ frontend: GET /api/v1/environment/runtime → backend.python_version
↓ backend: sys.version.split()[0]
↓ source: Python interpreter sys module
```

### Platform
```
UI field: "Platform"
↓ frontend: GET /api/v1/environment/runtime → backend.platform
↓ backend: platform.system()
↓ source: Python platform module
```

### Model Count
```
UI field: "Models"
↓ frontend: GET /api/v1/environment/runtime → services.ml_model_service.model_count
↓ backend: filesystem scan
↓ source: get_models_dir() filesystem
```

---

## Anti-Patterns Explicitly Avoided

| Pattern | Status |
|---|---|
| `Math.random()` | ❌ Never used |
| `setInterval(() => fakeData)` | ❌ Never used |
| Hard-coded CPU values | ❌ Never used |
| Hard-coded SDR values | ❌ Never used |
| Fake USRP connection | ❌ Never shown as connected |
| Fake PostgreSQL health | ❌ Shown as NOT CONFIGURED |
| Fake Redis health | ❌ Shown as NOT CONFIGURED |
| Second simulation engine | ❌ Not created |
| Mock/demo data disguised as real | ❌ Never used |
