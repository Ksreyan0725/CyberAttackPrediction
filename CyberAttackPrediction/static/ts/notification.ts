/**
 * CyberShield AI — Centralized Notification Center (TypeScript)
 * Preserves existing .premium-toast HTML, CSS, icons, animations, timing exactly
 * Adds: log persistence, copy/export, filters, event bus
 * Drop-in replacement for window.showToast — same API, same visuals
 */

import { ToastType, ToastOptions, LogEntry, LogQuery } from './types';

declare global {
  interface Window {
    showToast: (message: string, type: ToastType, details?: string | object) => void;
    cyberToast: (message: string, type: ToastType, details?: string | object) => void;
    showDetailModal: (title: string, html: string) => void;
    CyberNotify: NotificationCenter;
  }
}

interface StoredLog extends LogEntry {
  _persistedAt: number;
}

const STORAGE_KEY = 'cybershield_logs';
const MAX_LOGS = 500;
const DEDUP_WINDOW_MS = 3000;

export class NotificationCenter {
  private static instance: NotificationCenter;
  private container: HTMLElement | null = null;
  private lastToast: { message: string; time: number } | null = null;
  private logListeners: Set<(logs: LogEntry[]) => void> = new Set();
  private db: IDBDatabase | null = null;

  private constructor() {
    this.initContainer();
    this.initIndexedDB();
    this.patchGlobalShowToast();
    this.loadPersistedLogs();
    console.log('[CyberNotify] NotificationCenter initialized');
  }

  static getInstance(): NotificationCenter {
    if (!NotificationCenter.instance) {
      NotificationCenter.instance = new NotificationCenter();
    }
    return NotificationCenter.instance;
  }

  private initContainer(): void {
    let c = document.getElementById('toastContainer');
    if (!c) {
      c = document.createElement('div');
      c.id = 'toastContainer';
      c.style.cssText = 'position:fixed;bottom:1.5rem;right:1.5rem;z-index:10000;display:flex;flex-direction:column;gap:0.5rem;pointer-events:none;';
      document.body.appendChild(c);
    }
    this.container = c;
  }

  private async initIndexedDB(): Promise<void> {
    return new Promise((resolve, reject) => {
      const req = indexedDB.open('CyberShieldLogs', 1);
      req.onupgradeneeded = (e) => {
        const db = (e.target as IDBOpenDBRequest).result;
        if (!db.objectStoreNames.contains('logs')) {
          const store = db.createObjectStore('logs', { keyPath: 'id' });
          store.createIndex('timestamp', 'timestamp', { unique: false });
          store.createIndex('type', 'type', { unique: false });
          store.createIndex('source', 'source', { unique: false });
        }
      };
      req.onsuccess = (e) => {
        this.db = (e.target as IDBOpenDBRequest).result;
        resolve();
      };
      req.onerror = () => reject(req.error);
    });
  }

  private async loadPersistedLogs(): Promise<void> {
    if (!this.db) return;
    try {
      const tx = this.db.transaction('logs', 'readonly');
      const store = tx.objectStore('logs');
      const all = await new Promise<any[]>((resolve, reject) => {
        const req = store.getAll();
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => reject(req.error);
      });
      // Convert to LogEntry[] (strip _persistedAt)
      const logs = all.map(({ _persistedAt, ...rest }) => rest);
      this.notifyLogListeners();
    } catch (e) {
      console.warn('[CyberNotify] Failed to load persisted logs:', e);
    }
  }

  private async persistLog(log: LogEntry): Promise<void> {
    if (!this.db) return;
    try {
      const tx = this.db.transaction('logs', 'readwrite');
      const store = tx.objectStore('logs');
      const record = { ...log, _persistedAt: Date.now() };
      await new Promise<void>((resolve, reject) => {
        const req = store.put(record);
        req.onsuccess = () => resolve();
        req.onerror = () => reject(req.error);
      });
      // Enforce max logs
      let currentCount = 0;
      const countReq = store.count();
      countReq.onsuccess = () => {
        currentCount = countReq.result;
        if (currentCount > MAX_LOGS) {
          const cursorReq = store.openCursor(IDBKeyRange.lowerBound(0), 'next');
          cursorReq.onsuccess = (e) => {
            const cursor = (e.target as IDBRequest).result;
            if (cursor && currentCount > MAX_LOGS) {
              cursor.delete();
              currentCount--;
            }
          };
        }
      };
    } catch (e) {
      console.warn('[CyberNotify] Failed to persist log:', e);
    }
  }

  private patchGlobalShowToast(): void {
    // Keep legacy window.showToast working (legacy pages)
    const originalShowToast = window.showToast;
    window.showToast = (message: string, type: ToastType = 'info', details?: string | object) => {
      this.toast({ message, type, details });
    };
    window.cyberToast = window.showToast;
    window.CyberNotify = this;
  }

  /**
   * Core toast — preserves EXACT existing behavior, HTML, CSS, animations
   */
  toast(options: ToastOptions): void {
    const { message, type = 'info', details, persistent = false, source = 'client' } = options;

    // Deduplication (same 3s window as original)
    const now = Date.now();
    if (this.lastToast && this.lastToast.message === message && now - this.lastToast.time < 3000) {
      return;
    }
    this.lastToast = { message, time: now };

    // Ensure container
    if (!this.container) this.initContainer();
    if (!this.container) return;

    // Create log entry
    const logEntry: LogEntry = {
      id: crypto.randomUUID(),
      timestamp: new Date().toISOString(),
      type,
      source,
      code: this.inferCode(type, options),
      message,
      details,
    };
    this.addLog(logEntry);

    // Build toast element — EXACT same HTML as original showToast
    const icons: Record<ToastType, string> = {
      success: 'check-circle',
      error: 'exclamation-circle',
      danger: 'exclamation-circle',
      warning: 'exclamation-triangle',
      info: 'info-circle',
    };
    const icon = icons[type] || icons.info;

    const subtext = details
      ? `<div class="xx-small opacity-75 mt-1 mt-n1"><i class="fas fa-search-plus me-1"></i>Click to view details</div>`
      : '';

    const toast = document.createElement('div');
    toast.className = `premium-toast toast-${type}${details ? ' cursor-pointer' : ''}`;
    toast.style.cssText = ''; // Let CSS handle everything

    toast.innerHTML = `
      <div class="toast-icon text-white"><i class="fas fa-${icon}"></i></div>
      <div class="toast-body">
        <div class="small fw-bold dynamic-text">${this.escapeHtml(message)}</div>
        ${subtext}
      </div>
      <button type="button" class="btn-close ms-2 small" style="font-size:0.6rem;filter:var(--close-filter,none);"
        onclick="event.stopPropagation();this.parentElement.remove()"></button>
    `;

    // Details click handler (same as original)
    if (details) {
      toast.onclick = () => {
        const detailHtml = typeof details === 'string'
          ? `<div class="p-3 rounded-3 border-glass font-monospace text-break" style="background:var(--bg-card-soft);">${this.escapeHtml(details)}</div>`
          : `<div class="p-3 rounded-3 border-glass font-monospace text-break" style="background:var(--bg-card-soft);"><pre>${this.escapeHtml(JSON.stringify(details, null, 2))}</pre></div>`;
        if (window.showDetailModal) {
          window.showDetailModal(`${type.toUpperCase()} DETAILS`, detailHtml);
        }
      };
    }

    // Close button
    const closeBtn = toast.querySelector('.btn-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.removeToast(toast);
      });
    }

    // Append and animate (same spring physics as CSS)
    this.container!.appendChild(toast);
    // Force reflow for animation
    toast.offsetHeight;
    toast.classList.add('show');

    // Auto-dismiss (unless persistent)
    if (!persistent) {
      setTimeout(() => this.removeToast(toast), 5000);
    }
  }

  private removeToast(toast: HTMLElement): void {
    toast.classList.add('hide');
    setTimeout(() => toast.remove(), 500);
  }

  private inferCode(type: ToastType, options: ToastOptions): string {
    if (options.details && typeof options.details === 'object' && 'code' in options.details) {
      return String(options.details.code);
    }
    switch (type) {
      case 'success': return 'OPERATION_SUCCESS';
      case 'warning': return 'VALIDATION_WARNING';
      case 'error':
      case 'danger': return 'OPERATION_ERROR';
      default: return 'INFO';
    }
  }

  private escapeHtml(s: string): string {
    const map: Record<string, string> = { '&': '&', '<': '<', '>': '>', "'": "&apos;", '"': '"' };
    return s.replace(/[&<>'"]/g, (c) => map[c]);
  }

  // --- Log Management ---

  private addLog(log: LogEntry): void {
    this.persistLog(log);
    this.notifyLogListeners(); // will re-fetch from IndexedDB
  }

  private notifyLogListeners(): void {
    if (!this.db) return;
    const tx = this.db.transaction('logs', 'readonly');
    const store = tx.objectStore('logs');
    const req = store.getAll();
    req.onsuccess = () => {
      const logs = req.result.map(({ _persistedAt, ...rest }) => rest) as LogEntry[];
      this.logListeners.forEach(cb => cb(logs));
    };
  }

  // --- Public API ---

  /** Subscribe to log updates (Settings Logs tab) */
  onLogsChange(callback: (logs: LogEntry[]) => void): () => void {
    this.logListeners.add(callback);
    // Initial load
    if (this.db) {
      const tx = this.db.transaction('logs', 'readonly');
      const store = tx.objectStore('logs');
      const req = store.getAll();
      req.onsuccess = () => {
        const logs = req.result.map(({ _persistedAt, ...rest }) => rest) as LogEntry[];
        callback(logs);
      };
    }
    return () => this.logListeners.delete(callback);
  }

  /** Get all logs (for initial render) */
  async getLogs(query?: LogQuery): Promise<LogEntry[]> {
    if (!this.db) return [];
    return new Promise((resolve, reject) => {
      const tx = this.db!.transaction('logs', 'readonly');
      const store = tx.objectStore('logs');
      const req = store.getAll();
      req.onsuccess = () => {
        let logs = req.result.map(({ _persistedAt, ...rest }) => rest) as LogEntry[];
        // Apply filters
        if (query) {
          if (query.type) logs = logs.filter(l => l.type === query.type);
          if (query.source) logs = logs.filter(l => l.source === query.source);
          if (query.code) logs = logs.filter(l => l.code === query.code);
          if (query.route) logs = logs.filter(l => l.route === query.route);
          if (query.search) {
            const s = query.search.toLowerCase();
            logs = logs.filter(l => l.message.toLowerCase().includes(s) ||
              JSON.stringify(l.details || '').toLowerCase().includes(s));
          }
          if (query.startDate) logs = logs.filter(l => l.timestamp >= query.startDate!);
          if (query.endDate) logs = logs.filter(l => l.timestamp <= query.endDate!);
        }
        // Sort newest first
        logs.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
        if (query?.limit) logs = logs.slice(query.offset || 0, (query.offset || 0) + query.limit);
        resolve(logs);
      };
      req.onerror = () => reject(req.error);
    });
  }

  /** Copy logs to clipboard */
  async copyLogs(logs?: LogEntry[], format: 'json' | 'text' = 'text'): Promise<boolean> {
    const toCopy = logs || await this.getLogs();
    const text = format === 'json'
      ? JSON.stringify(toCopy, null, 2)
      : toCopy.map(l => `[${l.timestamp}] [${l.type.toUpperCase()}] [${l.code}] ${l.message}${l.details ? '\n  ' + JSON.stringify(l.details) : ''}`).join('\n\n');
    try {
      await navigator.clipboard.writeText(text);
      this.toast({ message: `Copied ${toCopy.length} log(s) to clipboard`, type: 'success' });
      return true;
    } catch (e) {
      this.toast({ message: 'Failed to copy logs', type: 'error', details: String(e) });
      return false;
    }
  }

  /** Clear all logs */
  async clearLogs(): Promise<void> {
    if (!this.db) return;
    return new Promise((resolve, reject) => {
      const tx = this.db!.transaction('logs', 'readwrite');
      const store = tx.objectStore('logs');
      const req = store.clear();
      req.onsuccess = () => {
        this.notifyLogListeners();
        resolve();
      };
      req.onerror = () => reject(req.error);
    });
  }

  /** Export logs as file download */
  exportLogs(format: 'json' | 'csv' = 'json'): void {
    this.getLogs().then(logs => {
      let content: string, mime: string, ext: string;
      if (format === 'json') {
        content = JSON.stringify(logs, null, 2);
        mime = 'application/json';
        ext = 'json';
      } else {
        const headers = ['timestamp', 'type', 'source', 'code', 'message', 'details'];
        const rows = logs.map(l => [
          l.timestamp, l.type, l.source, l.code, `"${l.message.replace(/"/g, '""')}"`,
          `"${JSON.stringify(l.details || '').replace(/"/g, '""')}"`
        ].join(','));
        content = [headers.join(','), ...rows].join('\n');
        mime = 'text/csv';
        ext = 'csv';
      }
      const blob = new Blob([content], { type: mime });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `cybershield-logs-${new Date().toISOString().slice(0,19).replace(/:/g,'-')}.${ext}`;
      a.click();
      URL.revokeObjectURL(url);
    });
  }

  // Convenience methods matching original API
  success(message: string, details?: string | object): void { this.toast({ message, type: 'success', details }); }
  error(message: string, details?: string | object): void { this.toast({ message, type: 'error', details }); }
  warning(message: string, details?: string | object): void { this.toast({ message, type: 'warning', details }); }
  info(message: string, details?: string | object): void { this.toast({ message, type: 'info', details }); }
  danger(message: string, details?: string | object): void { this.toast({ message, type: 'danger', details }); }
}

// Initialize singleton on load
if (typeof window !== 'undefined') {
  window.CyberNotify = NotificationCenter.getInstance();
  // Legacy flash-message bridge (runs after DOM ready)
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll<HTMLElement>('.flash-message-data').forEach(el => {
      const msg = el.dataset.message;
      const cat = el.dataset.category as ToastType;
      if (msg && cat) window.CyberNotify.toast({ message: msg, type: cat, source: 'server' });
      el.remove();
    });
  });
}

export const CyberNotify = NotificationCenter.getInstance();