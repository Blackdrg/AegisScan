# Failure & Recovery Test Report

## Overview
This report validates the system's ability to gracefully handle negative paths and expected operational errors.

## Test Cases

### 1. Missing Hardware
- **Execution**: Started the backend without a physical SDR attached.
- **Result**: The system elegantly fell back to `MockSDRDriver` as designed. The UI indicates `LAB MODE / MOCK` instead of crashing.
- **Status: PASS**

### 2. Invalid Simulation Configuration
- **Execution**: Attempted to post invalid scenario definitions via `/api/v1/simulations`.
- **Result**: FastAPI Pydantic validators caught the missing fields, returning a `422 Unprocessable Entity`. The frontend UI displayed a toast error and did not crash.
- **Status: PASS**

### 3. Backend Restart & SQLite Integrity
- **Execution**: Force-killed the Python backend while the frontend was open. Restarted the backend.
- **Result**: The SQLite file `aegis.db` retained all historical simulations. The frontend successfully reconnected its WebSocket after the backend came online via its exponential backoff jitter logic.
- **Status: PASS**

### 4. Empty Database
- **Execution**: Purged the `aegis.db` file to test cold-start.
- **Result**: The Experiments tab safely rendered an "Empty State" UI rather than throwing map/reduce exceptions on empty arrays.
- **Status: PASS**

## Conclusion
The application demonstrates robust fault tolerance appropriate for the demonstration environment.

**Status: PASS**
