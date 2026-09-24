"""
CyberShield AI — Flask Error/Log Bus
Standardizes error envelopes, provides /api/logs endpoints,
emits structured events to Go sidecar (if running).
"""
import os
import json
import time
import uuid
import logging
from functools import wraps
from datetime import datetime
from typing import Any, Dict, Optional, Tuple, Union
from flask import Flask, request, jsonify, g, Response

# ─── Configuration ───
ERROR_BUS_URL = os.getenv('ERROR_BUS_URL', 'http://localhost:9090/event')
EMIT_TIMEOUT_MS = 50  # non-blocking fire-and-forget
SENSITIVE_FIELDS = {'password', 'token', 'secret', 'auth', 'csrf', 'api_key', 'credit_card', 'ssn'}

# ─── Structured Error Envelope ───
class ApiError(Exception):
    """Standardized API error with code, message, details."""
    def __init__(
        self,
        code: str,
        message: str,
        details: Any = None,
        status: int = 400,
        request_id: Optional[str] = None
    ):
        self.code = code
        self.message = message
        self.details = details
        self.status = status
        self.request_id = request_id or str(uuid.uuid4())[:8]
        super().__init__(message)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'ok': False,
            'code': self.code,
            'message': self.message,
            'details': self.details,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'requestId': self.request_id,
        }

def error_response(
    code: str,
    message: str,
    details: Any = None,
    status: int = 400,
    request_id: Optional[str] = None
) -> Tuple[Response, int]:
    """Return standardized JSON error response."""
    err = ApiError(code, message, details, status)
    return jsonify(err.to_dict()), err.status

def success_response(data: Any = None, message: str = '', status: int = 200) -> Tuple[Response, int]:
    """Return standardized JSON success response."""
    return jsonify({
        'ok': True,
        'data': data,
        'message': message,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
    }), status

# ─── Sensitive Data Sanitizer ───
def sanitize(obj: Any) -> Any:
    """Recursively strip sensitive fields from dicts/lists."""
    if isinstance(obj, dict):
        return {
            k: '[REDACTED]' if k.lower() in SENSITIVE_FIELDS else sanitize(v)
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [sanitize(v) for v in obj]
    return obj

# ─── Structured Logging ───
class StructuredLogger:
    """Thread-safe structured logger with in-memory ring buffer + file output."""
    def __init__(self, max_entries: int = 1000, log_file: str = 'logs/server_events.log'):
        self.buffer = []
        self.max_entries = max_entries
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    def _emit(self, level: str, code: str, message: str, **kwargs):
        entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': level,
            'code': code,
            'message': message,
            **{k: sanitize(v) for k, v in kwargs.items()},
        }
        # In-memory ring buffer
        self.buffer.append(entry)
        if len(self.buffer) > 1000:
            self.buffer.pop(0)
        # File output (JSON lines)
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception:
            pass  # never let logging break the app

    def info(self, code: str, message: str, **kw): self._emit('info', code, message, **kw)
    def warning(self, code: str, message: str, **kw): self._emit('warning', code, message, **kw)
    def error(self, code: str, message: str, **kw): self._emit('error', code, message, **kw)

    def get_logs(self, limit: int = 100, offset: int = 0, filters: Dict = None) -> Dict:
        """Return paginated, filtered logs from memory buffer."""
        logs = self.buffer
        if filters:
            if 'type' in filters:
                logs = [l for l in logs if l.get('level') == filters['type']]
            if 'code' in filters:
                logs = [l for l in logs if l.get('code') == filters['code']]
            if 'search' in filters:
                s = filters['search'].lower()
                logs = [l for l in logs if s in str(l.get('message', '')).lower() or
                        s in json.dumps(l.get('details', '')).lower()]
            if 'startDate' in filters:
                logs = [l for l in logs if l['timestamp'] >= filters['startDate']]
            if 'endDate' in filters:
                logs = [l for l in logs if l['timestamp'] <= filters['endDate']]
        logs.sort(key=lambda x: x['timestamp'], reverse=True)
        total = len(logs)
        paginated = logs[offset:offset + limit]
        return {'logs': paginated, 'total': len(self.buffer), 'limit': limit, 'offset': offset}

    def clear(self):
        self.buffer.clear()

# Global logger instance
event_logger = StructuredLogger()

# ─── Go Sidecar Emitter (non-blocking) ───
def emit_event(level: str, code: str, message: str, **kwargs):
    """Fire-and-forget emit to Go sidecar (best effort, never blocks)."""
    payload = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'level': level,
        'code': code,
        'message': message,
        **{k: sanitize(v) for k, v in kwargs.items()},
    }
    try:
        import requests
        requests.post(ERROR_BUS_URL, json=payload, timeout=EMIT_TIMEOUT_MS / 1000)
    except Exception:
        pass  # never let emitter break the app

# ─── Flask Middleware / Helpers ───
def register_error_bus(app: Flask):
    """Register error bus middleware and endpoints on Flask app."""
    
    @app.before_request
    def _inject_request_id():
        g.request_id = request.headers.get('X-Request-ID') or uuid.uuid4().hex[:8]
        g.start_time = time.time()

    @app.after_request
    def _log_response(response):
        duration_ms = int((time.time() - g.start_time) * 1000)
        if request.path.startswith('/api/') or request.path in ('/PredictAction', '/TrainAction', '/SignupAction', '/UserLoginAction'):
            level = 'error' if response.status_code >= 400 else 'info'
            code = 'HTTP_' + str(response.status_code)
            event_logger.info(
                code=f'HTTP_{response.status_code}',
                message=f'{request.method} {request.path} -> {response.status_code}',
                route=request.path,
                method=request.method,
                status=response.status_code,
                duration_ms=duration_ms,
                request_id=getattr(g, 'request_id', None),
            )
            emit_event('info', f'HTTP_{response.status_code}', f'{request.method} {request.path}',
                       route=request.path, status=response.status_code, duration_ms=duration_ms)
        return response

    @app.errorhandler(Exception)
    def _handle_exception(e):
        """Global exception handler — returns standardized error envelope."""
        from werkzeug.exceptions import HTTPException
        request_id = getattr(g, 'request_id', None)

        if isinstance(e, HTTPException):
            status = e.code or 500
            code_map = {
                400: 'BAD_REQUEST', 401: 'UNAUTHORIZED', 403: 'FORBIDDEN',
                404: 'NOT_FOUND', 405: 'METHOD_NOT_ALLOWED',
                413: 'UPLOAD_TOO_LARGE', 429: 'RATE_LIMIT',
            }
            err_code = code_map.get(status, f'HTTP_{status}')
            message = e.description or str(e)
        else:
            status = getattr(e, 'status', 500) if isinstance(getattr(e, 'status', None), int) else 500
            raw_code = getattr(e, 'code', 'SERVER_ERROR')
            err_code = raw_code if isinstance(raw_code, str) else 'SERVER_ERROR'
            message = str(e)

        event_logger.error(
            code=err_code,
            message=message,
            route=request.path,
            method=request.method,
            request_id=request_id,
            traceback=__import__('traceback').format_exc(),
        )
        emit_event('error', err_code, message, route=request.path, request_id=request_id)

        return jsonify({
            'ok': False,
            'code': err_code,
            'message': message,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'requestId': request_id,
        }), status

    # ─── API Endpoints ───
    @app.route('/api/logs')
    def get_logs():
        """GET /api/logs?type=&code=&limit=&offset=&search=&startDate=&endDate="""
        try:
            limit = min(int(request.args.get('limit', 100)), 500)
            offset = int(request.args.get('offset', 0))
            filters = {}
            for k in ('type', 'code', 'search', 'startDate', 'endDate'):
                if request.args.get(k):
                    filters[k] = request.args.get(k)
            return jsonify(event_logger.get_logs(limit=limit, offset=0, filters=filters))
        except Exception as e:
            return jsonify({'ok': False, 'code': 'SERVER_ERROR', 'message': str(e)}), 500

    @app.route('/api/logs/clear', methods=['POST'])
    def clear_logs():
        event_logger.clear()
        return jsonify({'ok': True, 'message': 'Logs cleared'})

    @app.route('/api/heartbeat', methods=['GET', 'POST'])
    def heartbeat():
        # Update global pulse detection flag in Main module
        try:
            import Main
            Main.PULSE_DETECTED = True
            # Cancel browser launch timer if active
            if Main.browser_timer and Main.browser_timer.is_alive():
                Main.browser_timer.cancel()
                print("[Pulse Detection] Pulse received, cancelling auto-launch timer.")
        except Exception:
            pass
        return jsonify({
            'status': 'ready',
            'health': 'online',
            'pulse': 'active',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
        })

    # Patch existing jsonify responses to standard envelope (opt-in via response.headers['X-Standard-Envelope'])
    @app.after_request
    def _maybe_wrap_json(response):
        if response.is_json and response.headers.get('X-Standard-Envelope') == 'true':
            data = response.get_json()
            if isinstance(data, dict) and 'ok' not in data:
                wrapped = {'ok': True, 'data': data, 'timestamp': datetime.utcnow().isoformat() + 'Z'}
                response.set_data(json.dumps(wrapped))
        return response

# ─── Decorator for Standardized Route Responses ───
def standard_response(f):
    """Decorator: wraps route return value in standard envelope if not already."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        if isinstance(result, tuple):
            data, status = result
            if isinstance(data, dict) and 'ok' not in data:
                return jsonify({'ok': True, 'data': data, 'timestamp': datetime.utcnow().isoformat() + 'Z'}), status
        elif isinstance(result, Response):
            return result
        else:
            return jsonify({'ok': True, 'data': result, 'timestamp': datetime.utcnow().isoformat() + 'Z'})
        return result
    return wrapper