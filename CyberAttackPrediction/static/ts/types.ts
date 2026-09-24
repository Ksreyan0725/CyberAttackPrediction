/**
 * CyberShield AI — Shared TypeScript/Flask/Go types
 * Single source of truth for notification/error/log contracts
 * Keep in sync with Flask error_bus.py and Go error-bus/main.go
 */

export type ToastType = 'success' | 'error' | 'warning' | 'info' | 'danger';

export interface ToastOptions {
  message: string;
  type: ToastType;
  details?: string | object;
  persistent?: boolean;      // don't auto-dismiss
  source?: 'client' | 'server';
}

export interface LogEntry {
  id: string;
  timestamp: string;          // ISO8601
  type: ToastType;
  source: 'client' | 'server';
  code: string;               // e.g. 'VALIDATION_ERROR', 'OOM', 'UNAUTHORIZED'
  message: string;
  details?: any;
  route?: string;
  userId?: string;
  sanitized?: boolean;        // true if sensitive fields were stripped
}

export type ApiErrorCode =
  | 'VALIDATION_ERROR'
  | 'OOM'
  | 'UNAUTHORIZED'
  | 'FORBIDDEN'
  | 'NOT_FOUND'
  | 'TIMEOUT'
  | 'SERVER_ERROR'
  | 'NETWORK_ERROR'
  | 'UPLOAD_TOO_LARGE'
  | 'UPLOAD_EMPTY'
  | 'INVALID_FORMAT'
  | 'MODEL_NOT_READY'
  | 'TRAINING_FAILED'
  | 'PREDICTION_FAILED'
  | 'SESSION_EXPIRED'
  | 'CSRF_INVALID'
  | 'RATE_LIMIT'
  | 'UNKNOWN';

export interface ApiError {
  ok: false;
  code: ApiErrorCode;
  message: string;
  details?: any;
  timestamp: string;          // ISO8601
  requestId?: string;
}

export interface ApiSuccess<T> {
  ok: true;
  data: T;
  message?: string;
  timestamp: string;
}

export type ApiResponse<T> = ApiSuccess<T> | ApiError;

export interface UploadProgress {
  loaded: number;
  total: number;
  percent: number;
  phase: 'uploading' | 'analyzing';
}

export interface TrainResult {
  status: 'success' | 'error';
  accuracy?: number;
  model_path?: string;
  classes?: string[];
  dataset_used?: string;
  message?: string;
  details?: string;
}

export interface PredictResult {
  status: 'success' | 'error';
  predictions?: string[];
  raw_data?: any[][];
  feature_columns?: string[];
  message?: string;
  details?: string;
}

export interface HealthStatus {
  status: 'ready' | 'busy' | 'offline';
  health: 'online' | 'offline';
  pulse: 'active' | 'none';
  engine?: 'rust-windows' | 'rust-linux' | 'python-fallback';
  timestamp: string;
}

export interface LogQuery {
  type?: ToastType;
  source?: 'client' | 'server';
  code?: string;
  route?: string;
  limit?: number;
  offset?: number;
  search?: string;
  startDate?: string;
  endDate?: string;
}

export interface LogsResponse {
  logs: LogEntry[];
  total: number;
  limit: number;
  offset: number;
}