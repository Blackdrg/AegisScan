


// AegisScan — Typed API response definitions
// Every type here maps 1:1 to a backend response schema.

// ── System ────────────────────────────────────────────────────
export interface SystemHealth {
  api:              { status: 'healthy' | 'degraded' | 'offline'; detail: string };
  engine:           { status: 'running' | 'idle' | 'offline'; detail: string };
  session_registry: { status: string; detail: string };
  uptime_seconds:   number;
  timestamp:        string;
}

export interface SystemInfo {
  name:           string;
  full_name:      string;
  version:        string;
  api_version:    string;
  python_version: string;
  platform:       string;
  started_at:     string;
}

// ── Scenarios ─────────────────────────────────────────────────
export interface Scenario {
  id:             string;
  name:           string;
  duration:       number | null;
  num_bands:      number | null;
  emitter_count:  number;
  multi_receiver: boolean;
  num_receivers:  number;
  scheduler_type: string;
  detector_type:  string;
  raw:            Record<string, unknown>;
}

// ── Simulations ───────────────────────────────────────────────
export type SimulationStatus =
  | 'PENDING' | 'RUNNING' | 'PAUSED' | 'COMPLETE' | 'FAILED' | 'STOPPED';

export interface SimulationSummary {
  sim_id:        string;
  scenario_name: string;
  status:        SimulationStatus;
  created_at:    string;
  started_at:    string | null;
  completed_at:  string | null;
  current_time:  number;
  duration:      number;
  progress:      number;
  error:         string | null;
}

export interface ValidationResult {
  valid:           boolean;
  issues:          string[];
  resolved_config: Record<string, unknown> | null;
}

export interface MetricsSummary {
  available:              boolean;
  sim_id?:                string;
  status?:                SimulationStatus;
  total_observations?:    number;
  total_hits?:            number;
  total_misses?:          number;
  total_false_alarms?:    number;
  total_correct_rejections?: number;
  total_time_consumed?:   number;
  hit_rate?:              number;
  false_alarm_rate?:      number;
  detail?:                string;
}

// ── Receivers ─────────────────────────────────────────────────
export interface ReceiverState {
  id:             string;
  status:         'ACTIVE' | 'IDLE';
  current_band:   number | null;
  dwell_time:     number | null;
  last_detection: DetectionInfo | null;
  scheduler_type: string | null;
}

export interface ReceiverFleet {
  available:  boolean;
  sim_id?:    string;
  receivers:  ReceiverState[];
  detail?:    string;
}

export interface ReceiverDetail {
  id:          string;
  history:     ReceiverHistoryEntry[];
  total_scans: number;
  hits:        number;
  misses:      number;
}

export interface ReceiverHistoryEntry {
  time:      number;
  action:    { band_id: number; dwell_time: number } | null;
  detection: DetectionInfo | null;
  feedback:  { outcome: string; reward: number } | null;
}

// ── Spectrum ──────────────────────────────────────────────────
export interface BandState {
  band_id:           number;
  frequency_range:   [number, number];
  bandwidth:         number;
  is_active:         boolean;
  signal_count:      number;
  last_scanned:      number | null;
  age_of_information:number | null;
  last_detection:    DetectionInfo | null;
  emitter_ids:       string[];
}

export interface SpectrumState {
  available:    boolean;
  sim_id?:      string;
  current_time: number;
  band_count:   number;
  active_count: number;
  bands:        BandState[];
  detail?:      string;
}

// ── Detections ────────────────────────────────────────────────
export type DetectionOutcome = 'HIT' | 'MISS' | 'FALSE_ALARM' | 'CORRECT_REJECTION';

export interface DetectionInfo {
  detected:     boolean;
  confidence:   number | null;
  band_id:      number;
  source_class: string | null;
}

export interface DetectionEvent {
  time:            number;
  band_id:         number;
  outcome:         DetectionOutcome | null;
  true_state:      boolean;
  snr_db:          number | null;
  dwell_time:      number;
  switching_delay: number;
}

export interface DetectionList {
  available: boolean;
  sim_id?:   string;
  total:     number;
  offset:    number;
  limit:     number;
  events:    DetectionEvent[];
  detail?:   string;
}

export interface DetectionSummary {
  available:           boolean;
  sim_id?:             string;
  total_observations:  number;
  hits:                number;
  misses:              number;
  false_alarms:        number;
  correct_rejections:  number;
  p_d:                 number;
  p_fa:                number;
  precision:           number;
  recall:              number;
  detail?:             string;
}

// ── Knowledge ─────────────────────────────────────────────────
export interface BandMemory {
  band_id:           number;
  observation_count: number;
  detection_count:   number;
  p_on:              number | null;
  last_seen:         number | null;
  age_of_information:number | null;
  confidence:        number | null;
}

export interface KnowledgeState {
  available:    boolean;
  sim_id?:      string;
  current_time: number;
  band_count:   number;
  bands:        BandMemory[];
  detail?:      string;
}

// ── Scheduling ────────────────────────────────────────────────
export interface SchedulerDecision {
  receiver_id:    string;
  scheduler_type: string;
  last_action:    { band_id: number; dwell_time: number; sensor_modality?: string } | null;
  last_feedback:  { outcome: string; reward: number } | null;
}

export interface SchedulingHistory {
  available: boolean;
  sim_id?:   string;
  total:     number;
  history:   SchedulingHistoryEntry[];
  detail?:   string;
}

export interface SchedulingHistoryEntry {
  time:      number;
  receiver:  string;
  band_id:   number;
  sensor_modality?: string;
  dwell_time:number;
  outcome:   string | null;
  reward:    number | null;
}

export interface SchedulerPerformance {
  available:  boolean;
  sim_id?:    string;
  schedulers: SchedulerPerf[];
  detail?:    string;
}

export interface SchedulerPerf {
  receiver_id:     string;
  scheduler_type:  string;
  total_decisions: number;
  hits:            number;
  misses:          number;
  hit_rate:        number;
  total_reward:    number;
  avg_reward:      number;
}

// ── Models ────────────────────────────────────────────────────
export interface ModelInfo {
  id:          string;
  name:        string;
  file:        string;
  extension:   string;
  size_bytes:  number;
  modified_at: number;
  type:        'CNN' | 'RL' | 'unknown';
  config:      Record<string, unknown> | null;
  status:      'AVAILABLE';
}

export interface ModelsList {
  available:         boolean;
  model_count:       number;
  models_directory:  string;
  models:            ModelInfo[];
}

// ── Metrics ───────────────────────────────────────────────────
export interface TimelineEvent {
  time:            number;
  band_id:         number;
  receiver_action: string;
  outcome:         DetectionOutcome | null;
  true_state:      boolean;
  snr_db:          number | null;
  reward:          number | null;
  dwell_time:      number;
  switching_delay: number;
}

export interface TimelineResponse {
  available: boolean;
  sim_id?:   string;
  total:     number;
  offset:    number;
  limit:     number;
  events:    TimelineEvent[];
  detail?:   string;
}

export interface SNRPoint {
  snr_db:             number;
  hits:               number;
  misses:             number;
  false_alarms:       number;
  correct_rejections: number;
  p_d:                number;
  p_fa:               number;
}

export interface SNRAnalysis {
  available: boolean;
  sim_id?:   string;
  snr_curve: SNRPoint[];
  detail?:   string;
}

// ── Replay ────────────────────────────────────────────────────
export interface ReplayRecord {
  sim_id:        string;
  scenario_name: string;
  status:        SimulationStatus;
  tick_count:    number;
  duration:      number;
  started_at:    string | null;
  completed_at:  string | null;
}

export interface ReplayTimeline {
  sim_id:          string;
  scenario_name:   string;
  status:          SimulationStatus;
  total_ticks:     number;
  filtered_ticks:  number;
  from_time:       number;
  to_time:         number;
  ticks:           SimulationTick[];
}

// ── Logs ──────────────────────────────────────────────────────
export interface LogEntry {
  time:     number | null;
  category: 'SIMULATION' | 'DETECTION' | 'SYSTEM';
  type:     string | null;
  band_id:  number | null;
  outcome:  string | null;
  message:  string;
}

export interface LogsResponse {
  available: boolean;
  sim_id?:   string;
  total:     number;
  offset:    number;
  limit:     number;
  logs:      LogEntry[];
  detail?:   string;
}

// ── WebSocket Messages ─────────────────────────────────────────
export interface SimulationTick {
  type:      'SIMULATION_TICK';
  sim_id:    string;
  time:      number;
  duration:  number;
  progress:  number;
  // single receiver
  receiver?: string;
  action?:   { band_id: number; dwell_time: number; sensor_modality?: string };
  detection?:DetectionInfo;
  feedback?: { outcome: string; reward: number };
  // multi receiver
  receivers?: Array<{
    receiver:  string;
    action:    { band_id: number; dwell_time: number; sensor_modality?: string };
    detection: DetectionInfo;
    feedback:  { outcome: string; reward: number };
  }>;
  truth:     Array<{ band_id: number; active: boolean }>;
  metrics:   MetricsSummary;
  geography?: {
    name: string;
    latitude: number;
    longitude: number;
    altitude: number;
  };
  scheduler?: string;
  beliefs?: Array<{
    band_id: number;
    observation_count: number;
    detection_count: number;
    p_on: number | null;
    last_seen: number | null;
    age_of_information: number | null;
  }>;
  spectrum?: {
    band_count: number;
    active_count: number;
    bands: Array<{
      band_id: number;
      observation_count: number;
      detection_count: number;
      p_on: number | null;
      last_seen: number | null;
      age_of_information: number | null;
    }>;
  };
  logs?: Array<{
    time: number;
    category: string;
    message: string;
  }>;
}

export interface SimulationCompleteMsg {
  type:    'SIMULATION_COMPLETE';
  sim_id:  string;
  metrics: MetricsSummary;
}

export interface SimulationStoppedMsg {
  type:   'SIMULATION_STOPPED';
  sim_id: string;
}

export interface SimulationErrorMsg {
  type:   'SIMULATION_ERROR';
  sim_id: string;
  error:  string;
}

export interface SystemHealthMsg {
  type:            'SYSTEM_HEALTH';
  api:             string;
  engine:          string;
  active_sim_id:   string | null;
  session_count:   number;
  ws_connections:  number;
  operation_mode?: string;
  hardware_status?:string;
}

export interface HardwareStatusMsg {
  type:            'HARDWARE_STATUS';
  mode:            string;
  adapter_status:  string;
  active_adapter?: string | null;
  health?:         HealthStatus;
  telemetry?:      HardwareTelemetry;
  capabilities?:   ReceiverCapabilities;
}

export type WSMessage =
  | SimulationTick
  | SimulationCompleteMsg
  | SimulationStoppedMsg
  | SimulationErrorMsg
  | SystemHealthMsg
  | HardwareStatusMsg;

// ── API generic wrappers ───────────────────────────────────────
export interface CapabilityUnavailable {
  available:   false;
  capability?: string;
  detail:      string;
}

export type ApiResponse<T> = T | CapabilityUnavailable;

// ── Hardware Abstraction & Operating Modes ────────────────────
export type OperationMode =
  | 'simulation'
  | 'recorded_data'
  | 'lab_hardware'
  | 'mock_hardware'
  | 'unavailable';

export type ReceiverStatus =
  | 'DISCONNECTED'
  | 'CONNECTING'
  | 'INITIALIZING'
  | 'READY'
  | 'SCANNING'
  | 'BUSY'
  | 'ERROR'
  | 'UNAVAILABLE';

export interface ReceiverCapabilities {
  adapter_name:                  string;
  supported_bands:               number[];
  frequency_range_hz:            [number, number];
  min_dwell_ticks:               number;
  max_dwell_ticks:               number;
  sample_rates_hz:               number[];
  iq_available:                  boolean;
  telemetry_available:           boolean;
  temperature_readback:          boolean;
  frequency_readback_available:  boolean;
  switching_delay_ticks:         number;
  supports_realtime_stream:      boolean;
  metadata?:                     Record<string, unknown>;
}

export interface HealthStatus {
  state:              ReceiverStatus;
  device_id:          string;
  driver_version:     string;
  temperature_c:      number | null;
  last_heartbeat_utc: string;
  error_code:         string;
  error_message:      string | null;
  resource_usage:     Record<string, number>;
}

export interface HardwareTelemetry {
  device_id:              string;
  packet_count:           number;
  dropped_samples:        number;
  buffer_fill_pct:        number;
  clock_sync_locked:      boolean;
  current_center_freq_hz: number;
  rssi_dbm:               number;
  noise_floor_dbm:        number;
  timestamp_utc:          string;
}

export interface HardwareStatusResponse {
  mode:             OperationMode;
  adapter_name:     string;
  adapter_status:   ReceiverStatus;
  capabilities:     ReceiverCapabilities | null;
  health:           HealthStatus | null;
  telemetry:        HardwareTelemetry | null;
  available_modes:  OperationMode[];
}

export interface HardwareLogEntry {
  run_id:            string;
  timestamp_utc:     string;
  mode:              string;
  receiver_state:    string;
  observation_count: number;
  error_count:       number;
  rssi_dbm:          number | null;
  temperature_c:     number | null;
  adapter_name:      string;
  message:           string;
}

// ── Recorded IQ Datasets ──────────────────────────────────────
export interface RecordingMetadata {
  recording_id:        string;
  filename:            string;
  format:              string;
  sample_rate_hz:      number;
  center_frequency_hz: number;
  duration_seconds:    number;
  start_time:          string;
  source:              string;
  checksum_sha256:     string;
  total_samples:       number;
  num_channels:        number;
  bands_covered:       number[];
  description:         string;
  tags:                string[];
  custom_metadata?:    Record<string, unknown>;
}

export interface DataQualityReport {
  recording_id:           string;
  is_valid:               boolean;
  status:                 'HEALTHY' | 'WARNING' | 'CORRUPT' | 'INVALID';
  nan_count:              number;
  inf_count:              number;
  clipping_ratio:         number;
  estimated_snr_db:       number | null;
  mean_power_dbm:         number;
  noise_floor_dbm:        number;
  timestamp_gaps_count:   number;
  sample_loss_pct:        number;
  checksum_verified:      boolean;
  issues:                 string[];
  analysis_time_utc:      string;
}

export interface RecordingsListResponse {
  count:       number;
  recordings:  RecordingMetadata[];
}

// ── Domain Shift Sim-to-Real Comparison ───────────────────────
export interface DomainShiftMetric {
  detector_name:        string;
  sim_pd:               number;
  sim_pfa:              number;
  recorded_pd:          number;
  recorded_pfa:         number;
  pd_delta:             number;
  pfa_delta:            number;
  sim_snr_mean_db:      number;
  recorded_snr_mean_db: number;
}

export interface DomainShiftReport {
  analysis_id:      string;
  recording_id:     string;
  scenario_name:    string;
  num_eval_trials:  number;
  metrics:          Record<string, DomainShiftMetric>;
  timestamp_utc:    string;
}

// ── Experiments ────────────────────────────────────────────────
export interface ExperimentState {
  status: 'running' | 'idle';
  active_experiment_id: string | null;
  progress: number;
  results: Record<string, unknown> | null;
}

// ── Benchmarks ─────────────────────────────────────────────────
export interface BenchmarkSummary {
  algorithm: string;
  num_seeds: number;
  reward_mean: number;
  mean_aoi_mean: number;
  detection_probability_mean: number;
  [key: string]: unknown;
}

export interface BenchmarkListResponse {
  available: boolean;
  summary: BenchmarkSummary[];
  raw_runs: Array<{ id: string; agent_name: string; seed: number }>;
}

export interface BenchmarkRun {
  id: string;
  agent_name: string;
  seed: number;
  [key: string]: unknown;
}

// ── Environment ────────────────────────────────────────────────────────────
export interface EnvironmentState {
  terrain: string;
  temporal_activity: string;
  noise: string | number;
  fading: string | number;
  disturbance: string | number;
  uncertainty: string | number;
}

export interface EnvironmentServiceEntry {
  status: string;
  detail: string;
  model_count?: number;
}

export interface EnvironmentRuntime {
  timestamp: string;
  uptime_seconds: number;
  backend: { status: string; api: string; python_version: string; platform: string };
  websocket: { status: string; endpoints: string[] };
  simulation: {
    active: boolean;
    sim_id: string | null;
    status: string;
    scenario_name: string | null;
    mode: string;
    current_time: number;
    duration: number;
    num_bands: number;
  };
  environment_config: {
    terrain: string;
    temporal_activity: string;
    noise: number;
    fading: number;
    disturbance: number;
    uncertainty: number;
    source: string;
  };
  hardware: {
    operation_mode: string;
    receiver_backend: string;
    adapter_name: string;
    adapter_status: string;
    sdr_interface: string;
    physical_device: string;
    soapysdr_available: boolean;
    usrp_connected: boolean;
    note: string;
  };
  receivers: {
    available: boolean;
    sim_id?: string;
    detail?: string;
    receivers: Array<{
      id: string;
      status: string;
      current_band: number | null;
      scheduler_type: string | null;
      backend: string;
    }>;
  };
  services: {
    fastapi: EnvironmentServiceEntry;
    websocket: EnvironmentServiceEntry;
    ml_model_service: EnvironmentServiceEntry;
    data_store: EnvironmentServiceEntry;
    sqlite_session: EnvironmentServiceEntry;
    postgresql: EnvironmentServiceEntry;
    redis: EnvironmentServiceEntry;
    sdr_hardware: EnvironmentServiceEntry;
    usrp: EnvironmentServiceEntry;
  };
}

// ── Reasoning ──────────────────────────────────────────────────
export interface ReasoningTrace {
  band_id: number;
  observation: string;
  detector_evidence: number;
  environmental_evidence: number;
  geographic_context: string;
  temporal_context: string;
  posterior: number;
  uncertainty: number;
  aoi: number;
  scheduler_score: number;
  action: string;
  available: boolean;
}
