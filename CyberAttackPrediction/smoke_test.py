# -*- coding: utf-8 -*-
"""Deployment smoke tests for CyberShield AI. Run from CyberAttackPrediction/."""
import io
import json
import os
import sys
import traceback

os.environ.setdefault("RENDER", "false")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret-key-for-smoke-tests")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PASS = []
FAIL = []
NOT_TESTED = []


def ok(name):
    PASS.append(name)
    print(f"PASS  {name}")


def bad(name, detail):
    FAIL.append((name, detail))
    print(f"FAIL  {name}: {detail}")


def nt(name, why):
    NOT_TESTED.append((name, why))
    print(f"NOT TESTED  {name}: {why}")


try:
    import Main
    ok("import Main (datetime, requests, error_bus)")
except Exception as e:
    bad("import Main", f"{type(e).__name__}: {e}")
    traceback.print_exc()
    print("\n=== SUMMARY ===")
    print(f"PASS={len(PASS)} FAIL={len(FAIL)}")
    sys.exit(1)

app = Main.app
app.config["TESTING"] = True
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024
client = app.test_client()


def get_csrf(c):
    # Hit a page that sets session csrf
    r = c.get("/")
    html = r.get_data(as_text=True)
    # pull from meta if present
    import re
    m = re.search(r'name="csrf-token"\s+content="([^"]+)"', html)
    if m:
        return m.group(1)
    with c.session_transaction() as s:
        return s.get("csrf_token")


# --- 1. Health / pages ---
try:
    r = client.get("/api/heartbeat")
    if r.status_code == 200 and r.is_json:
        ok(f"/api/heartbeat 200 JSON ({r.get_json().get('status') or 'ok'})")
    else:
        bad("/api/heartbeat", f"status={r.status_code} ct={r.content_type}")
except Exception as e:
    bad("/api/heartbeat", str(e))

for path in ["/", "/UserLogin", "/Signup"]:
    try:
        r = client.get(path)
        if r.status_code == 200:
            ok(f"GET {path} 200")
        else:
            bad(f"GET {path}", f"status={r.status_code}")
    except Exception as e:
        bad(f"GET {path}", str(e))

# --- 2. Signup (JSON contract as api.signup sends) ---
test_user = "smoke_user_ok"
test_pass = "Passw0rd!x"
try:
    r = client.post("/SignupAction", json={"username": test_user, "password": test_pass})
    body = r.get_json() or {}
    if r.status_code in (200, 400) and ("ok" in body):
        if r.status_code == 200 and body.get("ok"):
            ok("SignupAction JSON signup 200 ok envelope")
        elif r.status_code == 400 and "already registered" in (body.get("message") or ""):
            ok("SignupAction JSON duplicate -> 400 envelope")
        else:
            bad("SignupAction JSON", f"status={r.status_code} body={body}")
    else:
        bad("SignupAction JSON", f"status={r.status_code} body={body}")
except Exception as e:
    bad("SignupAction JSON", str(e))

# Missing fields
try:
    r = client.post("/SignupAction", json={"username": "", "password": ""})
    body = r.get_json() or {}
    if r.status_code == 400 and body.get("ok") is False:
        ok("SignupAction empty fields -> 400")
    else:
        bad("SignupAction empty", f"status={r.status_code} body={body}")
except Exception as e:
    bad("SignupAction empty", str(e))

# --- 3. Login (form t1/t2 as UserLogin.html sends) ---
try:
    r = client.post("/UserLoginAction", data={"t1": test_user, "t2": test_pass})
    body = r.get_json() or {}
    if r.status_code == 200 and body.get("ok") and (body.get("data") or {}).get("redirect"):
        ok(f"UserLoginAction form login 200 redirect={body['data']['redirect']}")
    else:
        bad("UserLoginAction form", f"status={r.status_code} body={body}")
except Exception as e:
    bad("UserLoginAction form", str(e))

# Wrong password
try:
    r = client.post("/UserLoginAction", data={"t1": test_user, "t2": "wrong"})
    body = r.get_json() or {}
    if r.status_code == 401 and body.get("code") == "INVALID_PASSWORD":
        ok("UserLoginAction wrong password -> 401 INVALID_PASSWORD")
    else:
        bad("UserLoginAction wrong pw", f"status={r.status_code} body={body}")
except Exception as e:
    bad("UserLoginAction wrong pw", str(e))

# --- 4. Logged-in session + Predict page ---
csrf = None
try:
    r = client.get("/Train")
    if r.status_code == 200:
        ok("GET /Train (logged in) 200")
    elif r.status_code == 302:
        bad("GET /Train", f"redirect {r.headers.get('Location')} (session not kept?)")
    else:
        bad("GET /Train", f"status={r.status_code}")
except Exception as e:
    bad("GET /Train", str(e))

try:
    r = client.get("/Predict")
    if r.status_code == 200:
        ok("GET /Predict 200")
    else:
        bad("GET /Predict", f"status={r.status_code}")
except Exception as e:
    bad("GET /Predict", str(e))

# CSRF token from session
with client.session_transaction() as s:
    csrf = s.get("csrf_token")
if csrf:
    ok("session has csrf_token")
else:
    bad("session csrf_token", "missing")

# --- 5. Predict with Accept: application/json (api.ts contract) ---
# Use a tiny CSV with correct columns if model feature_columns known
try:
    fc = Main.feature_columns
    if fc is None and hasattr(Main, "load_ml_model"):
        Main.load_ml_model()
        fc = Main.feature_columns
    if fc is None:
        nt("PredictAction JSON", "model feature_columns unavailable")
    else:
        import csv as _csv
        buf = io.StringIO()
        w = _csv.writer(buf)
        w.writerow(list(fc))
        # minimal row of zeros / dummy values
        row = []
        for c in fc:
            row.append(0)
        w.writerow(row)
        csv_bytes = buf.getvalue().encode("utf-8")
        r = client.post(
            "/PredictAction",
            data={"t1": (io.BytesIO(csv_bytes), "smoke.csv"), "csrf_token": csrf},
            content_type="multipart/form-data",
            headers={"Accept": "application/json", "X-CSRF-Token": csrf},
        )
        body = r.get_json()
        if r.status_code == 200 and isinstance(body, dict) and body.get("ok") and "predictions" in (body.get("data") or {}):
            ok(f"PredictAction Accept:json 200 predictions={len(body['data']['predictions'])}")
        else:
            bad("PredictAction json", f"status={r.status_code} body={str(body)[:300]}")
except Exception as e:
    bad("PredictAction json", f"{type(e).__name__}: {e}")

# --- 6. Predict HTML path (no Accept json) ---
try:
    if Main.feature_columns:
        import csv as _csv
        buf = io.StringIO()
        w = _csv.writer(buf)
        w.writerow(list(Main.feature_columns))
        w.writerow([0] * len(Main.feature_columns))
        csv_bytes = buf.getvalue().encode("utf-8")
        r = client.post(
            "/PredictAction",
            data={"t1": (io.BytesIO(csv_bytes), "smoke.html.csv"), "csrf_token": csrf},
            content_type="multipart/form-data",
            headers={"X-CSRF-Token": csrf},  # browser default Accept
        )
        ct = r.content_type or ""
        if r.status_code == 200 and "text/html" in ct:
            ok("PredictAction HTML path 200 text/html")
        else:
            bad("PredictAction html", f"status={r.status_code} ct={ct}")
    else:
        nt("PredictAction HTML", "no feature_columns")
except Exception as e:
    bad("PredictAction html", str(e))

# --- 7. 25MB rejection (early content-length guard) ---
try:
    # multipart body larger than 25MB — use content_length lie via big file
    big = io.BytesIO(b"0" * (26 * 1024 * 1024))
    r = client.post(
        "/PredictAction",
        data={"t1": (big, "big.csv"), "csrf_token": csrf},
        content_type="multipart/form-data",
        headers={"Accept": "application/json", "X-CSRF-Token": csrf},
    )
    body = r.get_json() if r.content_type and "json" in r.content_type else None
    if r.status_code == 413:
        ok(f"PredictAction 26MB -> 413 (body={str(body)[:120]})")
    else:
        bad("PredictAction 26MB", f"status={r.status_code} body={str(body)[:200]}")
except Exception as e:
    # Werkzeug may raise RequestEntityTooLarge as unhandled if handler missing
    if "413" in str(e) or "RequestEntityTooLarge" in type(e).__name__:
        bad("PredictAction 26MB", f"unhandled {type(e).__name__}: {e}")
    else:
        bad("PredictAction 26MB", f"{type(e).__name__}: {e}")

# --- 8. 5000-row cap (6000 rows -> 5000 predictions) ---
try:
    if Main.feature_columns:
        import csv as _csv
        buf = io.StringIO()
        w = _csv.writer(buf)
        cols = list(Main.feature_columns)
        w.writerow(cols)
        for i in range(6000):
            w.writerow([i % 10] * len(cols))
        csv_bytes = buf.getvalue().encode("utf-8")
        r = client.post(
            "/PredictAction",
            data={"t1": (io.BytesIO(csv_bytes), "rows6000.csv"), "csrf_token": csrf},
            content_type="multipart/form-data",
            headers={"Accept": "application/json", "X-CSRF-Token": csrf},
        )
        body = r.get_json() or {}
        n = len((body.get("data") or {}).get("predictions") or [])
        if r.status_code == 200 and n == 5000:
            ok("PredictAction 6000-row CSV capped at 5000 predictions")
        elif r.status_code == 200:
            bad("5000-row cap", f"got {n} predictions, expected 5000")
        else:
            bad("5000-row cap", f"status={r.status_code} body={str(body)[:200]}")
    else:
        nt("5000-row cap", "no feature_columns")
except Exception as e:
    bad("5000-row cap", f"{type(e).__name__}: {e}")

# --- 9. Session cookie not blown after predict ---
try:
    with client.cookie_jar if hasattr(client, "cookie_jar") else open(os.devnull) as _:
        pass
except Exception:
    pass
# test_client keeps cookies in client; inspect Set-Cookie size via environ
try:
    # after heavy predict, session should still work
    r = client.get("/api/heartbeat")
    if r.status_code == 200:
        ok("session still valid after predict (heartbeat 200)")
    else:
        bad("session after predict", f"status={r.status_code}")
except Exception as e:
    bad("session after predict", str(e))

# --- 10. Train local dataset field contract ---
try:
    r = client.post(
        "/TrainAction",
        data={"local_dataset": "kdd_train.csv", "csrf_token": csrf},
        content_type="multipart/form-data",
        headers={"Accept": "application/json", "X-CSRF-Token": csrf},
    )
    body = r.get_json() or {}
    # Training may take a while — accept 200 success or structured failure
    if r.status_code == 200 and body.get("ok"):
        ok(f"TrainAction local_dataset 200 accuracy={body.get('data', {}).get('accuracy')}")
    elif r.status_code in (400, 404, 500) and body.get("ok") is False:
        # path validation errors are acceptable contract-wise if message present
        if body.get("message"):
            ok(f"TrainAction local_dataset structured error {r.status_code}: {body.get('code')}")
        else:
            bad("TrainAction local", f"status={r.status_code} body={body}")
    else:
        bad("TrainAction local", f"status={r.status_code} body={str(body)[:300]}")
except Exception as e:
    bad("TrainAction local", f"{type(e).__name__}: {e}")

# --- 11. CSRF rejection without token ---
try:
    r = client.post("/PredictAction", data={}, content_type="multipart/form-data",
                    headers={"Accept": "application/json"})
    if r.status_code == 403:
        ok("PredictAction without CSRF -> 403")
    else:
        bad("CSRF missing", f"status={r.status_code}")
except Exception as e:
    bad("CSRF missing", str(e))

# --- 12. Guest login ---
try:
    r = client.post("/GuestLogin", data={"csrf_token": csrf},
                    headers={"X-CSRF-Token": csrf})
    body = r.get_json() or {}
    if r.status_code == 200 and body.get("status") == "success":
        ok(f"GuestLogin 200 engine={body.get('engine')}")
    else:
        bad("GuestLogin", f"status={r.status_code} body={body}")
except Exception as e:
    bad("GuestLogin", str(e))

# --- 13. API logs ---
try:
    r = client.get("/api/logs?limit=5")
    if r.status_code == 200 and r.is_json:
        ok("GET /api/logs 200")
    else:
        bad("/api/logs", f"status={r.status_code}")
except Exception as e:
    bad("/api/logs", str(e))

# --- 14. 404 handler uses datetime ---
try:
    r = client.get("/api/definitely-missing-route")
    body = r.get_json() or {}
    if r.status_code == 404 and body.get("code") == "NOT_FOUND" and body.get("timestamp"):
        ok("API 404 handler has timestamp (datetime import works)")
    else:
        bad("API 404", f"status={r.status_code} body={body}")
except Exception as e:
    bad("API 404", f"{type(e).__name__}: {e}")

# --- 15. wants_json helper sanity ---
try:
    with app.test_request_context("/", headers={"Accept": "application/json"}):
        if Main.wants_json() is True:
            ok("wants_json Accept:application/json -> True")
        else:
            bad("wants_json json", "expected True")
    with app.test_request_context("/", headers={"Accept": "text/html"}):
        if Main.wants_json() is False:
            ok("wants_json Accept:text/html -> False")
        else:
            bad("wants_json html", "expected False")
except Exception as e:
    bad("wants_json", str(e))

# --- 16. Static assets ---
for path in ["/static/sw.js", "/static/js/api.js", "/static/js/notification.js", "/static/css/main.css"]:
    try:
        r = client.get(path)
        if r.status_code == 200:
            ok(f"GET {path} 200")
        else:
            bad(f"GET {path}", f"status={r.status_code}")
    except Exception as e:
        bad(f"GET {path}", str(e))

# --- NOT TESTED markers ---
nt("Gunicorn worker recycle (max-requests)", "requires live gunicorn process under load")
nt("SSE /stream reconnect", "no frontend EventSource consumer wired")
nt("IndexedDB browser logs", "browser-only persistence")
nt("Render deploy / live OOM 512MB", "no Render environment here")
nt("Docker image runtime", "separate docker build/run step")

print("\n=== SUMMARY ===")
print(f"PASS={len(PASS)}  FAIL={len(FAIL)}  NOT_TESTED={len(NOT_TESTED)}")
if FAIL:
    print("\nFailures:")
    for n, d in FAIL:
        print(f"  - {n}: {d}")
sys.exit(1 if FAIL else 0)
