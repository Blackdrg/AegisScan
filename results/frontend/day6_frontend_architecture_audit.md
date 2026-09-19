# Phase 0: Frontend Architecture Audit

## Framework and Technologies
- **Framework**: React 19.2.8
- **Build Tool**: Vite 8.2.2
- **Language**: TypeScript 6.0.2
- **State Management**: Zustand 5.0.15
- **Routing**: React Router DOM 7.18.3
- **Styling**: Emotion 11, Material UI 5, Recharts 3 for charts

## Architecture Structure
- **Entry Point**: `src/main.tsx` and `index.html`
- **Route Structure**: Handled by `src/app/router/` and `src/app/layout/`
- **API Architecture**: `src/api/client.ts` exports a typed fetch wrapper. API base URL is resolved via `VITE_API_BASE` or falls back to `http://localhost:8000`. Wait, Vite proxy in `vite.config.ts` points `/api` to `127.0.0.1:8001`! This is a configuration mismatch with the backend running on `8000`.
- **WebSocket Architecture**: `src/api/websocket.ts` implements a reconnecting WebSocket client with schema validation.
- **State Management Architecture**: Stores located in `src/stores/`, e.g., `simulation.ts`.

## Configuration
- **API Base URL**: `import.meta.env.VITE_API_BASE` or `http://localhost:8000`
- **WebSocket URL**: derived from API base by replacing `http` with `ws`
- **Production Build Command**: `npm run build` (`tsc -b && vite build`)

## Potential Issues Discovered
- `vite.config.ts` proxies `/api` to port `8001`, while backend `start.bat` runs on port `8000`.
- Found "mock" references in `src/types/api.ts`, `src/features/hardware/LabHardwarePage.tsx`, and `src/app/layout/TopBar.tsx`.
