/**
 * CyberShield AI — Centralized API Layer (TypeScript)
 * Unified fetch with timeout, retry, progress, error mapping
 * Upload helper with real progress events
 * All errors route through NotificationCenter
 */

import { NotificationCenter } from './notification';
import { ApiResponse, ApiError, ApiErrorCode, UploadProgress, TrainResult, PredictResult, HealthStatus, LogEntry, LogQuery, LogsResponse } from './types';

const CYBER_NOTIFY = (window as any).CyberNotify || (() => { throw new Error('CyberNotify not initialized'); })();

/** Default timeout for API calls (ms) */
const DEFAULT_TIMEOUT_MS = 120000; // 2 min for Render free tier

/** Retry configuration */
interface RetryConfig {
  retries: number;
  baseDelayMs: number;
  maxDelayMs: number;
  shouldRetry: (error: ApiError) => boolean;
}

const DEFAULT_RETRY_CONFIG: RetryConfig = {
  retries: 2,
  baseDelayMs: 800,
  maxDelayMs: 6000,
  shouldRetry: (err) => err.code === 'TIMEOUT' || err.code === 'NETWORK_ERROR' || (err.code === 'SERVER_ERROR' && (err as any).status >= 500),
};

/** CSRF token getter */
function getCsrfToken(): string | null {
  return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || null;
}

/** Build headers with CSRF + JSON Accept (Flask wants_json() keys off this) */
function buildHeaders(customHeaders?: Record<string, string>): Headers {
  const headers = new Headers();
  const csrf = getCsrfToken();
  if (csrf) headers.set('X-CSRF-Token', csrf);
  headers.set('Accept', 'application/json');
  if (customHeaders) {
    Object.entries(customHeaders).forEach(([k, v]) => headers.set(k, v));
  }
  return headers;
}

/** Map HTTP status to ApiErrorCode */
function mapStatusToCode(status: number): ApiErrorCode {
  switch (status) {
    case 400: return 'VALIDATION_ERROR';
    case 401: return 'UNAUTHORIZED';
    case 403: return 'FORBIDDEN';
    case 404: return 'NOT_FOUND';
    case 408: return 'TIMEOUT';
    case 413: return 'UPLOAD_TOO_LARGE';
    case 429: return 'RATE_LIMIT';
    default:
      if (status >= 500) return 'SERVER_ERROR';
      return 'UNKNOWN';
  }
}

/** Parse response body safely */
async function parseResponse(response: Response): Promise<any> {
  const ct = response.headers.get('content-type') || '';
  if (ct.includes('application/json')) {
    try { return await response.json(); } catch { return null; }
  }
  return response.text();
}

/** Build standardized ApiError from response */
function buildApiError(response: Response, body: any, defaultMessage: string): ApiError {
  let code = mapStatusToCode(response.status);
  let message = defaultMessage;
  let details = body;

  if (body && typeof body === 'object') {
    if (body.message) message = body.message;
    if (body.details) details = body.details;
    if (body.code) code = body.code as ApiErrorCode;
  }

  const err: ApiError = {
    ok: false,
    code,
    message,
    details,
    timestamp: new Date().toISOString(),
  };
  return err;
}

/** Delay helper */
const delay = (ms: number) => new Promise(r => setTimeout(r, ms));

/**
 * Centralized fetch with timeout, retry, error normalization, and toast integration
 */
export async function cyberFetch<T = any>(
  url: string,
  options: RequestInit = {},
  config: {
    timeoutMs?: number;
    retryConfig?: Partial<RetryConfig>;
    showToastOnError?: boolean;
    toastType?: 'error' | 'warning' | 'info';
    onUploadProgress?: (progress: UploadProgress) => void;
  } = {}
): Promise<{ ok: true; data: T } | { ok: false; error: ApiError }> {
  const {
    timeoutMs = DEFAULT_TIMEOUT_MS,
    retryConfig = {},
    showToastOnError = true,
    toastType = 'error',
    onUploadProgress,
  } = config;

  const mergedRetryConfig: RetryConfig = { ...DEFAULT_RETRY_CONFIG, ...retryConfig };
  const headers = buildHeaders(options.headers as Record<string, string>);
  const csrfToken = getCsrfToken();
  if (csrfToken && !headers.has('X-CSRF-Token')) {
    headers.set('X-CSRF-Token', csrfToken);
  }

  // Don't set Content-Type for FormData (browser sets with boundary)
  if (!(options.body instanceof FormData) && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  let attempt = 0;
  let lastError: ApiError | null = null;

  while (attempt <= mergedRetryConfig.retries) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

    try {
      const fetchOptions: RequestInit = {
        ...options,
        headers,
        signal: controller.signal,
        credentials: 'same-origin',
      };

      const response = await fetch(url, fetchOptions);
      clearTimeout(timeoutId);

      const body = await parseResponse(response);

      if (response.ok) {
        return { ok: true, data: body as T };
      }

      // Server responded with error status
      const apiError = buildApiError(response, body, `Server error ${response.status}`);

      // Don't retry on client errors (4xx except 408, 413, 429)
      const isRetryableStatus = response.status === 408 || response.status === 413 || response.status === 429 || response.status >= 500;
      if (!isRetryableStatus || attempt >= mergedRetryConfig.retries) {
        if (showToastOnError) {
          CYBER_NOTIFY.toast({ message: apiError.message, type: 'error', details: apiError.details });
        }
        return { ok: false, error: apiError };
      }

      // Will retry
      lastError = apiError;
    } catch (err: any) {
      clearTimeout(timeoutId);

      if (err.name === 'AbortError' || err.name === 'TimeoutError') {
        lastError = { ok: false, code: 'TIMEOUT', message: `Request timed out after ${timeoutMs / 1000}s`, timestamp: new Date().toISOString() };
      } else if (err instanceof TypeError && err.message.includes('Failed to fetch')) {
        lastError = { ok: false, code: 'NETWORK_ERROR', message: 'Network error — server unreachable or connection lost', timestamp: new Date().toISOString() };
      } else {
        lastError = { ok: false, code: 'UNKNOWN', message: err?.message || 'Unknown error', details: String(err), timestamp: new Date().toISOString() };
      }

      // Retry logic
      const isRetryable = mergedRetryConfig.shouldRetry(lastError);
      if (!isRetryable || attempt >= mergedRetryConfig.retries) {
        if (showToastOnError) {
          CYBER_NOTIFY.toast({ message: lastError.message, type: 'error', details: lastError.details });
        }
        return { ok: false, error: lastError };
      }
    }

    // Retry with exponential backoff + jitter
    attempt++;
    if (attempt <= mergedRetryConfig.retries) {
      const delayMs = Math.min(
        mergedRetryConfig.baseDelayMs * Math.pow(2, attempt - 1) + Math.random() * 500,
        mergedRetryConfig.maxDelayMs
      );
      console.warn(`[CyberFetch] Retry ${attempt}/${mergedRetryConfig.retries} after ${delayMs}ms:`, lastError?.message);
      await delay(delayMs);
    }
  }

  // All retries exhausted
  const finalError = lastError || { ok: false, code: 'UNKNOWN', message: 'Request failed after retries', timestamp: new Date().toISOString() };
  if (showToastOnError) {
    CYBER_NOTIFY.toast({ message: finalError.message, type: 'error', details: finalError.details });
  }
  return { ok: false, error: finalError };
}

/**
 * Convenience methods for common HTTP verbs
 */
export const cyberApi = {
  get: <T>(url: string, opts?: RequestInit, cfg?: typeof cyberFetch extends (u: string, o: any, c: infer C) => any ? C : never) =>
    cyberFetch<T>(url, { ...opts, method: 'GET' }, cfg),

  post: <T>(url: string, body?: any, opts?: RequestInit, cfg?: any) =>
    cyberFetch<T>(url, { ...opts, method: 'POST', body: body instanceof FormData ? body : JSON.stringify(body) }, cfg),

  put: <T>(url: string, body?: any, opts?: RequestInit, cfg?: any) =>
    cyberFetch<T>(url, { ...opts, method: 'PUT', body: body instanceof FormData ? body : JSON.stringify(body) }, cfg),

  delete: <T>(url: string, opts?: RequestInit, cfg?: any) =>
    cyberFetch<T>(url, { ...opts, method: 'DELETE' }, cfg),
};

/**
 * Upload file with real progress events
 * Returns structured result or error
 */
export async function uploadFile(
  url: string,
  file: File,
  options: {
    fieldName?: string;           // form field name (default 'file')
    extraFields?: Record<string, string>;
    timeoutMs?: number;
    onProgress?: (progress: UploadProgress) => void;
    showToastOnError?: boolean;
  } = {}
): Promise<{ ok: true; data: any } | { ok: false; error: ApiError }> {
  const {
    fieldName = 'file',
    extraFields = {},
    timeoutMs = DEFAULT_TIMEOUT_MS,
    onProgress,
    showToastOnError = true,
  } = options;

  const formData = new FormData();
  formData.append(fieldName, file);
  Object.entries(extraFields).forEach(([k, v]) => formData.append(k, v));

  return cyberFetch(url, {
    method: 'POST',
    body: formData,
  }, {
    timeoutMs,
    showToastOnError,
    onUploadProgress: (progress: UploadProgress) => {
      if (onProgress) onProgress(progress);
    },
    retryConfig: { retries: 0 }, // never retry uploads
  });
}

/**
 * Specific API endpoints
 */
export const api = {
  /** POST /PredictAction — upload CSV for prediction */
  predict: (file: File, onProgress?: (p: UploadProgress) => void) =>
    uploadFile('/PredictAction', file, {
      fieldName: 't1',
      timeoutMs: 10 * 60 * 1000, // 10 min
      onProgress,
    }),

  /** POST /TrainAction — train model (custom File or local dataset filename) */
  train: (fileOrLocal?: File | string) => {
    const formData = new FormData();
    if (fileOrLocal instanceof File) {
      formData.append('training_data', fileOrLocal);
    } else if (typeof fileOrLocal === 'string' && fileOrLocal) {
      formData.append('local_dataset', fileOrLocal);
    }
    return cyberFetch<TrainResult>('/TrainAction', { method: 'POST', body: formData }, { timeoutMs: 10 * 60 * 1000 });
  },

  /** POST /api/logs/clear — clear server logs */
  clearServerLogs: () => cyberFetch('/api/logs/clear', { method: 'POST' }),

  /** GET /api/logs — fetch server logs */
  getServerLogs: (query?: { type?: string; limit?: number; offset?: number }) => {
    const params = new URLSearchParams();
    if (query?.type) params.set('type', query.type);
    if (query?.limit) params.set('limit', String(query.limit));
    if (query?.offset) params.set('offset', String(query.offset));
    return cyberFetch<{ logs: any[]; total: number }>(`/api/logs?${params.toString()}`);
  },

  /** GET /api/health — health check */
  health: () => cyberFetch<HealthStatus>('/api/heartbeat', { method: 'GET' }, { showToastOnError: false, retryConfig: { retries: 0 } }),

  /** POST /UpdateAccountAction — update profile (backend reads request.form) */
  updateAccount: (data: { username: string; password?: string }) => {
    const formData = new FormData();
    formData.append('username', data.username);
    if (data.password) formData.append('password', data.password);
    return cyberFetch('/UpdateAccountAction', { method: 'POST', body: formData });
  },

  /** POST /SignupAction — create account (JSON body; SignupAction accepts JSON or form) */
  signup: (username: string, password: string) =>
    cyberFetch('/SignupAction', { method: 'POST', body: JSON.stringify({ username, password }) }),

  /** POST /UserLoginAction — login (backend reads form fields t1/t2) */
  login: (username: string, password: string, remember?: boolean) => {
    const formData = new FormData();
    formData.append('t1', username);
    formData.append('t2', password);
    if (remember) formData.append('remember', 'on');
    return cyberFetch('/UserLoginAction', { method: 'POST', body: formData });
  },

  /** POST /GuestLogin — guest access */
  guestLogin: () => cyberFetch('/GuestLogin', { method: 'POST' }),
};

/** Upload progress type (re-export for consumers) */
export type { UploadProgress };