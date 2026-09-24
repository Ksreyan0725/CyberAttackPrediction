# -*- coding: utf-8 -*-
"""Live container smoke tests against running Docker image."""
import io
import re
import sys

import requests

BASE = "http://127.0.0.1:18080"
EB = "http://127.0.0.1:19090"
pass_n = fail_n = 0


def ok(n):
    global pass_n
    pass_n += 1
    print("PASS ", n)


def bad(n, d):
    global fail_n
    fail_n += 1
    print("FAIL ", n, ":", d)


s = requests.Session()

try:
    r = s.get(BASE + "/api/heartbeat", timeout=10)
    ok("/api/heartbeat") if r.status_code == 200 else bad("hb", r.status_code)
except Exception as e:
    bad("hb", e)

for p in ["/", "/UserLogin", "/Signup", "/static/sw.js", "/static/js/api.js", "/static/js/notification.js", "/static/css/main.css"]:
    try:
        r = s.get(BASE + p, timeout=10)
        ok("GET " + p) if r.status_code == 200 else bad(p, r.status_code)
    except Exception as e:
        bad(p, e)

try:
    r = requests.get(EB + "/health", timeout=5)
    ok("error-bus /health") if r.status_code == 200 else bad("eb", r.status_code)
except Exception as e:
    bad("eb", e)

try:
    r = s.get(BASE + "/UserLogin", timeout=10)
    m = re.search(r'name="csrf-token"\s+content="([^"]+)"', r.text)
    csrf = m.group(1) if m else None
    ok("csrf") if csrf else bad("csrf", "missing")
except Exception as e:
    csrf = None
    bad("csrf", e)

h = {"Accept": "application/json", "X-CSRF-Token": csrf or ""}

try:
    r = s.post(BASE + "/SignupAction", json={"username": "livesmoke4", "password": "Passw0rd!x"}, headers=h, timeout=10)
    body = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
    if r.status_code in (200, 400) and "ok" in body:
        ok("signup " + str(r.status_code))
    else:
        bad("signup", (r.status_code, r.text[:200]))
except Exception as e:
    bad("signup", e)

try:
    r = s.post(BASE + "/UserLoginAction", data={"t1": "livesmoke4", "t2": "Passw0rd!x"}, headers=h, timeout=10)
    j = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
    if r.status_code == 200 and j.get("ok") and (j.get("data") or {}).get("redirect"):
        ok("login " + j["data"]["redirect"])
    else:
        bad("login", (r.status_code, r.text[:200]))
except Exception as e:
    bad("login", e)

try:
    big = io.BytesIO(b"0" * (26 * 1024 * 1024))
    r = s.post(BASE + "/PredictAction", files={"t1": ("big.csv", big)}, data={"csrf_token": csrf}, headers=h, timeout=60)
    if r.status_code == 413:
        ok("26MB -> 413")
    else:
        bad("26MB", (r.status_code, r.text[:200]))
except Exception as e:
    bad("26MB", type(e).__name__ + ": " + str(e)[:200])

try:
    small = io.BytesIO(b"x,y,z\n1,2,3\n")
    r = s.post(BASE + "/PredictAction", files={"t1": ("s.csv", small)}, data={"csrf_token": csrf}, headers=h, timeout=30)
    ct = r.headers.get("content-type", "")
    if r.status_code in (200, 400) and "application/json" in ct:
        ok("predict structured " + str(r.status_code))
    else:
        bad("predict", (r.status_code, ct, r.text[:200]))
except Exception as e:
    bad("predict", e)

# 404 API handler with datetime
try:
    r = s.get(BASE + "/api/no-such-route", headers=h, timeout=10)
    j = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
    if r.status_code == 404 and j.get("timestamp"):
        ok("API 404 has timestamp")
    else:
        bad("API 404", (r.status_code, j))
except Exception as e:
    bad("API 404", e)

print("LIVE PASS=%d FAIL=%d" % (pass_n, fail_n))
sys.exit(1 if fail_n else 0)
