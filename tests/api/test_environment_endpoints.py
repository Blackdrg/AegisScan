"""
Tests for the /api/v1/environment endpoints.
Verifies:
  - /api/v1/environment returns real schema (not fake)
  - /api/v1/environment/runtime returns full structured response
  - Schema validation of all required fields
  - Unavailable services are marked correctly, not fabricated
  - No active simulation → graceful idle response
"""
import pytest
from fastapi.testclient import TestClient
from aegis_scan.api.server import app

client = TestClient(app)


def test_environment_state_returns_200():
    """GET /api/v1/environment returns 200."""
    response = client.get("/api/v1/environment")
    assert response.status_code == 200


def test_environment_state_schema():
    """GET /api/v1/environment has required terrain/noise fields."""
    response = client.get("/api/v1/environment")
    data = response.json()
    assert "terrain" in data
    assert "noise" in data
    assert "fading" in data
    assert "disturbance" in data
    assert "temporal_activity" in data
    assert "uncertainty" in data
    assert "available" in data
    assert data["available"] is True


def test_environment_state_no_fake_random():
    """
    /api/v1/environment must return deterministic values (no Math.random equivalent).
    Call it twice — values must be identical when no simulation is running.
    """
    r1 = client.get("/api/v1/environment").json()
    r2 = client.get("/api/v1/environment").json()
    # Non-timestamp fields must be equal
    for key in ("terrain", "temporal_activity"):
        assert r1[key] == r2[key], f"Non-deterministic field: {key}"


def test_environment_runtime_returns_200():
    """GET /api/v1/environment/runtime returns 200."""
    response = client.get("/api/v1/environment/runtime")
    assert response.status_code == 200


def test_environment_runtime_top_level_keys():
    """GET /api/v1/environment/runtime has all required top-level sections."""
    response = client.get("/api/v1/environment/runtime")
    data = response.json()
    required = ["timestamp", "uptime_seconds", "backend", "websocket",
                "simulation", "environment_config", "hardware", "receivers", "services"]
    for key in required:
        assert key in data, f"Missing key: {key}"


def test_environment_runtime_backend_section():
    """Backend section must be healthy and populated."""
    data = client.get("/api/v1/environment/runtime").json()
    backend = data["backend"]
    assert backend["status"] == "healthy"
    assert "python_version" in backend
    assert "platform" in backend
    assert "api" in backend


def test_environment_runtime_simulation_section():
    """Simulation section must be present with expected schema."""
    data = client.get("/api/v1/environment/runtime").json()
    sim = data["simulation"]
    assert "active" in sim
    assert "sim_id" in sim
    assert "status" in sim
    assert "scenario_name" in sim
    assert "mode" in sim
    assert isinstance(sim["current_time"], int)
    assert isinstance(sim["duration"], int)
    assert isinstance(sim["num_bands"], int)
    # When idle, active should be False
    assert isinstance(sim["active"], bool)


def test_environment_runtime_hardware_section():
    """Hardware section must not claim USRP connected in default simulation mode."""
    data = client.get("/api/v1/environment/runtime").json()
    hw = data["hardware"]
    assert "operation_mode" in hw
    assert "receiver_backend" in hw
    assert "adapter_name" in hw
    assert "adapter_status" in hw
    # CRITICAL: USRP must NOT be reported as connected without physical validation
    assert hw["usrp_connected"] is False, "USRP must never be marked connected without physical validation"
    # Default mode should be simulation
    assert hw["operation_mode"] in ("simulation", "mock_hardware", "lab_hardware", "physical_hardware", "recorded_data", "unavailable")


def test_environment_runtime_services_section():
    """Services section must report real availability, not fabricated."""
    data = client.get("/api/v1/environment/runtime").json()
    services = data["services"]
    required_services = ["fastapi", "websocket", "ml_model_service", "data_store",
                         "sqlite_session", "postgresql", "redis", "sdr_hardware", "usrp"]
    for svc in required_services:
        assert svc in services, f"Missing service: {svc}"
        assert "status" in services[svc]
        assert "detail" in services[svc]

    # FastAPI must always be healthy if we're responding
    assert services["fastapi"]["status"] == "healthy"

    # PostgreSQL and Redis must NOT be fabricated as healthy
    # In this deployment they are not configured
    assert services["postgresql"]["status"] in ("not_configured", "configured_not_validated")
    assert services["redis"]["status"] in ("not_configured", "configured_not_validated")

    # USRP must not be claimed as available
    assert services["usrp"]["status"] in ("unavailable", "not_configured")


def test_environment_runtime_receivers_section():
    """Receivers section returns valid schema even with no active simulation."""
    data = client.get("/api/v1/environment/runtime").json()
    receivers = data["receivers"]
    assert "available" in receivers
    assert "receivers" in receivers
    assert isinstance(receivers["receivers"], list)
    # With no active simulation, receivers should not be available
    if not receivers["available"]:
        assert receivers["receivers"] == []


def test_environment_runtime_uptime_positive():
    """Uptime must be a positive number."""
    data = client.get("/api/v1/environment/runtime").json()
    assert data["uptime_seconds"] >= 0


def test_environment_runtime_no_mock_data():
    """
    Environment runtime must not return obviously hardcoded fake values.
    Specifically: noise/fading/disturbance must be in reasonable ranges.
    """
    data = client.get("/api/v1/environment/runtime").json()
    env_cfg = data["environment_config"]
    # These come from config or sensible defaults — not Math.random()
    assert 0.0 <= float(env_cfg["noise"]) <= 1.0
    assert 0.0 <= float(env_cfg["fading"]) <= 1.0
    assert 0.0 <= float(env_cfg["disturbance"]) <= 1.0
    assert 0.0 <= float(env_cfg["uncertainty"]) <= 1.0


def test_environment_state_has_source_field():
    """Environment state should report its data source."""
    data = client.get("/api/v1/environment").json()
    assert "source" in data
    assert data["source"] in ("simulation_config", "defaults")
