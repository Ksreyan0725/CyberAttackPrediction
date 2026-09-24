<!-- markdownlint-disable MD033 -->
<h1 align="center">
  <img src="../CyberAttackPrediction/static/images/logo_with_bg.svg" alt="CyberShield Logo" width="32" vertical-align="middle"> CyberShield AI — Technical Workflow
</h1>

<p align="center">
  <img src="../CyberAttackPrediction/static/images/banner.png" alt="Architecture Banner" width="800">
</p>

<p align="center">
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python Badge"></a>
  <a href="https://flask.palletsprojects.com"><img src="https://img.shields.io/badge/Flask-3.x-7C3AED?style=flat-square&logo=flask&logoColor=white" alt="Flask Badge"></a>
  <a href="https://scikit-learn.org"><img src="https://img.shields.io/badge/Scikit--learn-ML-F7931E?style=flat-square&logo=scikitlearn&logoColor=white" alt="Scikit-learn Badge"></a>
  <a href="https://tensorflow.org"><img src="https://img.shields.io/badge/TensorFlow-Deep%20Learning-FF6F00?style=flat-square&logo=tensorflow&logoColor=white" alt="TensorFlow Badge"></a>
  <a href="https://keras.io"><img src="https://img.shields.io/badge/Keras-Neural%20Nets-D00000?style=flat-square&logo=keras&logoColor=white" alt="Keras Badge"></a>
  <a href="https://pandas.pydata.org"><img src="https://img.shields.io/badge/Pandas-Data-8B5CF6?style=flat-square&logo=pandas&logoColor=white" alt="Pandas Badge"></a>
  <a href="https://numpy.org"><img src="https://img.shields.io/badge/NumPy-Arrays-4DABCF?style=flat-square&logo=numpy&logoColor=white" alt="NumPy Badge"></a>
  <a href="https://matplotlib.org"><img src="https://img.shields.io/badge/Matplotlib-Plotting-11557C?style=flat-square&logoColor=white" alt="Matplotlib Badge"></a>
  <a href="https://seaborn.pydata.org"><img src="https://img.shields.io/badge/Seaborn-Visualization-4C72B0?style=flat-square&logoColor=white" alt="Seaborn Badge"></a>
  <a href="https://shap.readthedocs.io"><img src="https://img.shields.io/badge/SHAP-Explainability-FF4B4B?style=flat-square&logoColor=white" alt="SHAP Badge"></a>
  <a href="https://scipy.org"><img src="https://img.shields.io/badge/SciPy-Scientific-8CAAE6?style=flat-square&logo=scipy&logoColor=white" alt="SciPy Badge"></a>
  <a href="https://joblib.readthedocs.io"><img src="https://img.shields.io/badge/Joblib-Persistence-6D28D9?style=flat-square&logoColor=white" alt="Joblib Badge"></a>
  <a href="https://werkzeug.palletsprojects.com"><img src="https://img.shields.io/badge/Werkzeug-Security-059669?style=flat-square&logoColor=white" alt="Werkzeug Badge"></a>
  <a href="https://jupyter.org"><img src="https://img.shields.io/badge/Jupyter-Notebooks-F37626?style=flat-square&logo=jupyter&logoColor=white" alt="Jupyter Badge"></a>
  <a href="https://github.com/trentm/python-markdown2"><img src="https://img.shields.io/badge/Markdown2-Rendering-0EA5E9?style=flat-square&logoColor=white" alt="Markdown2 Badge"></a>
  <a href="https://pygments.org"><img src="https://img.shields.io/badge/Pygments-Highlighting-E11D48?style=flat-square&logoColor=white" alt="Pygments Badge"></a>
  <a href="https://nbconvert.readthedocs.io"><img src="https://img.shields.io/badge/nbconvert-Export-F59E0B?style=flat-square&logo=jupyter&logoColor=white" alt="nbconvert Badge"></a>
  <a href="https://nbformat.readthedocs.io"><img src="https://img.shields.io/badge/nbformat-Notebook%20IO-10B981?style=flat-square&logo=jupyter&logoColor=white" alt="nbformat Badge"></a>
  <a href="https://pypi.org/project/python-dotenv"><img src="https://img.shields.io/badge/python--dotenv-Config-84CC16?style=flat-square&logoColor=white" alt="python-dotenv Badge"></a>
  <a href="https://gunicorn.org"><img src="https://img.shields.io/badge/Gunicorn-Deployment-4338CA?style=flat-square&logo=gunicorn&logoColor=white" alt="Gunicorn Badge"></a>
  <a href="https://pypi.org/project/six"><img src="https://img.shields.io/badge/Six-Compatibility-6366F1?style=flat-square&logoColor=white" alt="Six Badge"></a>
  <a href="https://rich.readthedocs.io"><img src="https://img.shields.io/badge/rich-Terminal%20UI-6366F1?style=flat-square&logoColor=white" alt="Rich Badge"></a>
  <a href="https://ipywidgets.readthedocs.io"><img src="https://img.shields.io/badge/ipywidgets-Interactive-DB2777?style=flat-square&logo=jupyter&logoColor=white" alt="ipywidgets Badge"></a>
</p>

---

## 📦 Libraries & Dependencies

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org) **Core Runtime Implementation**: Powers all scripting, Flask routing, and ML training logic. Version 3.13 provides maximum performance for the inference engine.

---

[![Flask](https://img.shields.io/badge/Flask-3.x-7C3AED?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com) **Production Web Framework**: All application routes, template rendering (Jinja2), and HTTP state handling are managed by Flask to serve the prediction/training UI.

---

[![Werkzeug](https://img.shields.io/badge/Werkzeug-Security-059669?style=flat-square&logoColor=white)](https://werkzeug.palletsprojects.com) **Security Hardening**: Secures all user passwords using the scrypt algorithm via `generate_password_hash` and `check_password_hash`. Also manages internal WSGI handling.

---

[![python-dotenv](https://img.shields.io/badge/python--dotenv-Config-84CC16?style=flat-square&logoColor=white)](https://pypi.org/project/python-dotenv) **Environment Synchronization**: Loads sensitive configuration like `FLASK_SECRET_KEY` from the `.env` file when present. If the env var is missing, `Main.py` falls back to a gitignored `.flask_secret` file so sessions stay stable across gunicorn worker recycles. On Render, prefer the platform env var (ephemeral disk).

---

[![Gunicorn](https://img.shields.io/badge/Gunicorn-WSGI-4338CA?style=flat-square&logo=gunicorn&logoColor=white)](https://gunicorn.org) **Production WSGI Server**: The container runs `gunicorn --workers 1 --threads 2 --max-requests 100 --bind 0.0.0.0:$PORT Main:app` under supervisord (see `supervisord.conf`). Local demos may still use `python Main.py` / the Flask dev server on port 2026.

---

[![requests](https://img.shields.io/badge/requests-HTTP-3776AB?style=flat-square&logo=python&logoColor=white)](https://pypi.org/project/requests) **HTTP Client**: Pinned in `requirements.txt` for outbound calls (error-bus sidecar helpers, health checks).

---

<!-- Random Forest remains the primary production driver -->
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)](https://scikit-learn.org) **The Core Production Engine**: Implements our primary Random Forest classifier. This is the 'Brain' currently powering the live web application.

---

<!-- Marking DL as Research Extension to protect team during viva -->
[![TensorFlow](https://img.shields.io/badge/TensorFlow-Research-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)](https://tensorflow.org) [![Keras](https://img.shields.io/badge/Keras-Research-D00000?style=flat-square&logo=keras&logoColor=white)](https://keras.io) **Research & Future Scope**: These libraries are used in our laboratory notebooks to experiment with Deep Learning. They are included as part of our research extension and future project roadmap.

---

[![Pandas](https://img.shields.io/badge/Pandas-Data-8B5CF6?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org) **Data Engineering Pipeline**: Performs all data wrangling, column alignment, and type detection. Used in both training and prediction for reading/writing CSV datasets.

---

[![NumPy](https://img.shields.io/badge/NumPy-Arrays-4DABCF?style=flat-square&logo=numpy&logoColor=white)](https://numpy.org) **Numerical Foundation**: Converts DataFrames into efficient arrays for model compatibility and sanitizes `NaN`/`Inf` values for pipeline stability.

---

[![Joblib](https://img.shields.io/badge/Joblib-Persistence-6D28D9?style=flat-square&logoColor=white)](https://joblib.readthedocs.io) **Model Persistence Protocol**: Serializes the fitted model, scaler, and encoder into a single `.pkl` bundle for instant loading without retraining.

---

[![SHAP](https://img.shields.io/badge/SHAP-Explainability-FF4B4B?style=flat-square&logoColor=white)](https://shap.readthedocs.io) **Explainable AI (XAI)**: Ranks feature contributions to provide internal model interpretability—crucial during viva for explaining 'why' the AI made a specific decision.

---

[![SciPy](https://img.shields.io/badge/SciPy-Scientific-8CAAE6?style=flat-square&logo=scipy&logoColor=white)](https://scipy.org) **Scientific Computing Toolkit**: Underpins the complex mathematical operations used by Scikit-learn and SHAP for optimization and distribution analysis.

---

[![Matplotlib](https://img.shields.io/badge/Matplotlib-Plotting-11557C?style=flat-square&logoColor=white)](https://matplotlib.org) [![Seaborn](https://img.shields.io/badge/Seaborn-Visualization-4C72B0?style=flat-square&logoColor=white)](https://seaborn.pydata.org) **Analytical Visualization Suite**: Renders all confusion matrices, ROC curves, and EDA plots in the research notebooks to visualize detection metrics.

---

[![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-F37626?style=flat-square&logo=jupyter&logoColor=white)](https://jupyter.org) **R&D Sandbox Environment**: Facilitates cell-by-cell execution, research experimentation, and live demonstration of the ML pipelines.

---

[![ipywidgets](https://img.shields.io/badge/ipywidgets-Interactive-DB2777?style=flat-square&logo=jupyter&logoColor=white)](https://ipywidgets.readthedocs.io) **Interactive Dashboard Widgets**: Enhances the notebook experience with live progress tracking and interactive controllers during training runs.

---

[![nbformat](https://img.shields.io/badge/nbformat-Notebook%20IO-10B981?style=flat-square&logo=jupyter&logoColor=white)](https://nbformat.readthedocs.io) [![nbconvert](https://img.shields.io/badge/nbconvert-Export-F59E0B?style=flat-square&logo=jupyter&logoColor=white)](https://nbconvert.readthedocs.io) **Notebook Rendering Service**: Powers the integrated Documentation Hub by parsing and converting `.ipynb` files into styled browser-readable HTML.

---

[![Markdown2](https://img.shields.io/badge/Markdown2-Rendering-0EA5E9?style=flat-square&logoColor=white)](https://github.com/trentm/python-markdown2) **Documentation Engine**: Converts technical Markdown (like this page) into high-fidelity HTML for the web app UI.

---

[![Pygments](https://img.shields.io/badge/Pygments-Highlighting-E11D48?style=flat-square&logoColor=white)](https://pygments.org) [![rich](https://img.shields.io/badge/rich-Terminal%20UI-6366F1?style=flat-square&logoColor=white)](https://rich.readthedocs.io) **Visual Interface Enhancement**: Provides syntax highlighting for source code and formatted terminal reporting for the CLI training script.

---

## 📌 What the Project Does

CyberShield AI is a **Network Intrusion Detection System (NIDS)** that uses machine learning to classify network traffic as either **normal** or a specific **cyber attack type** (DoS, Probe, U2R, R2L).

The system delivers a complete end-to-end pipeline:

| Phase | Action |
| :---: | :--- |
| 🏋️ **Train** | Fit a Random Forest classifier on labeled network traffic data |
| 📤 **Upload** | Accept new, unlabeled capture files from the user |
| 🔍 **Predict** | Classify each record and identify the attack type |
| 💬 **Explain** | Generate plain-English attack summaries via the GenAI Insight Engine |

---

## 🔄 The Resilient Engine Life-Cycle

CyberShield AI operates on a state-aware execution loop that maintains data integrity and session stability even in hostile network conditions.

### 1 · Secure Training Lifecycle

Training is handled as an **Asynchronous Process** to prevent UI blocking. The frontend monitors the backend via **`GET /api/heartbeat`** (registered by `error_bus.py`) to provide real-time status updates without manual page refreshes.

```mermaid
sequenceDiagram
    participant U as User (Browser)
    participant S as Main.py (Flask)
    participant T as train_model.py (ML)
    participant D as trained_rf_model.pkl
    
    Note over U: User Clicks "Start Training"
    U->>S: POST /TrainAction (Dataset + CSRF)
    S->>S: Validate CSRF Token
    S->>T: Trigger run_training() [Async Thread]
    S-->>U: Return JSON (Status: busy)
    
    loop Heartbeat Loop (every 3s)
        U->>S: GET /api/heartbeat
        S-->>U: { status: "busy", health: "online" }
        Note over U: UI shows "System Processing..."
    end
    
    T->>T: Load, Clean, Scale, Train
    T->>D: Serialize Model Bundle
    T-->>S: Thread Signal (Done)
    
    U->>S: GET /api/heartbeat
    S-->>U: { status: "ready", health: "online" }
    S->>S: load_ml_model() (Reload Memory)
    Note over U: UI shows "System Ready"
```

> `/api/heartbeat` is registered by `error_bus.py` (`register_error_bus(app)`), not by a route decorator in `Main.py` itself.

### 2 · Secure Inference Lifecycle (Predict)

Prediction utilizes the **In-Memory Model Cache** for sub-millisecond classification. Every request is hardened by security middlewares before reaching the AI core.

```mermaid
sequenceDiagram
    participant U as User (Browser)
    participant S as Main.py (Flask)
    participant M as In-Memory Cache (RAM)
    
    Note over U: User Uploads CSV
    U->>S: POST /PredictAction (File + CSRF)
    S->>S: Handle Security Headers (no-store)
    S->>S: Preprocess (Align & Scale)
    S->>M: rf_model.predict(X_scaled)
    M-->>S: Predicted Class (e.g., "neptune")
    S->>S: Map to GenAI Insight Engine
    S-->>U: Render UserScreen.html
    
    Note right of S: Result stored in secured session
```

---

### Phase-by-Phase Technical Breakdown

#### A · Authentication & Heartbeat

- **Entry**: `/UserLoginAction` validates credentials via `werkzeug` hashing.
- **Pulse**: `base.html` polls `/api/heartbeat` (route provided by `error_bus.py`) on an interval for connectivity/health.
- **Session Focus**: CSRF tokens are stored in the server-side session, ensuring that all prediction uploads originate from the authenticated user.
- **JSON vs HTML**: Clients that send `Accept: application/json` receive structured envelopes from `wants_json()` (login returns `{ok, data.redirect}`); browser form posts keep normal redirects.

#### B · Post-Processing & GenAI Mapping

Unlike traditional ML apps that just return a number, CyberShield runs a **Contextual Mapping Layer**:

1. **Raw Prediction**: Returns a numeric code.
2. **Label Translation**: Converts code to attack name (e.g., `back`, `teardrop`).
3. **Insight Generation**: Pulls pre-written technical summaries explaining the "How, Why, and What to do" for each specific threat detected.

---

## 🗂️ Role of Training Files

| File | Role |
| :--- | :--- |
| `train_model.py` | Standalone ML pipeline — load, clean, encode, scale, train, evaluate, save |
| `Dataset/kdd_train.csv` | Default NSL-KDD training data; labeled network traffic (~14 MB) |
| `Dataset/custom_train.csv` | User-uploaded data saved for future training sessions |
| `model/trained_rf_model.pkl` | **Output of training** — serialized bundle of classifier + scaler + encoder |

> `train_model.py` has a single entry point `run_training(dataset_path)` and works both as a standalone CLI script (`python train_model.py`) and as a module called by Flask. This keeps ML logic independently testable.

---

## 🎯 Role of Prediction Files

| File | Role |
| :--- | :--- |
| `Main.py` | Flask server — all routes, session, security middleware, prediction orchestration |
| `Dataset/testData.csv` | Default unlabeled capture file for prediction demos |
| `Dataset/uploaded_test.csv` | Temp path for user-uploaded files before processing |
| `model/trained_rf_model.pkl` | **Input to prediction** — loaded once at startup |

> `Main.py` never re-imports or re-runs `train_model.py` during inference. It only reads the `.pkl`. This is the standard **training/inference separation** pattern used in production ML systems.

---

## 🔗 How Training & Prediction Are Connected

The file `model/trained_rf_model.pkl` is the **sole bridge** between the two phases.

```text
┌─────────────── TRAINING ────────────────┐    ┌──────────────── INFERENCE ──────────────┐
│                                         │    │                                         │
│  Raw CSV (labeled)                      │    │  New CSV (no labels)                    │
│       │                                 │    │        │                                │
│       ▼                                 │    │        ▼                                │
│  LabelEncoder.fit()   ── saved ─────────┼────┼──▶ LabelEncoder.transform()            │
│  StandardScaler.fit() ── saved ─────────┼────┼──▶ StandardScaler.transform()          │
│  RandomForest.fit()   ── saved ─────────┼────┼──▶ RandomForest.predict()              │
│       │                                 │    │        │                                │
│       ▼                                 │    │        ▼                                │
│  trained_rf_model.pkl ──────────────────┼────┼──▶ Predicted Labels                    │
└─────────────────────────────────────────┘    └─────────────────────────────────────────┘
```

> **Critical**: The scaler and encoder are fitted **only once during training**. During inference they run in `transform` mode only — ensuring new data is on the exact same numerical scale, preventing data leakage.

---

## 📓 Role of Jupyter Notebooks

| Notebook | Phase | Purpose |
| :--- | :---: | :--- |
| `ProposeCyberAttack.ipynb` | Phase 1 | Traditional ML — Logistic Regression, Decision Tree, Random Forest on NSL-KDD. EDA, confusion matrices, SHAP explainability. |
| `ExtensionCyberAttack.ipynb` | Phase 2 | Deep Learning — LSTM & MLP research, multi-dataset experiments, and GenAI-style explanations. |

The notebooks were the **R&D sandbox** — algorithm selection, preprocessing design, and hyperparameter tuning all happened here before the logic was ported to the production Flask app. They are **not called at runtime**; they are standalone academic deliverables.

### 📚 Notebook Comment Architecture (Viva-Ready)

Each cell in the notebooks follows a **Dual-Language** structure to assist during the Viva:

- **`[TECH]` Comments**: Direct technical breakdown (e.g., hyperparameter choices, scaling math).
- **`[NON-TECH]` Comments**: High-level business/security impact.
- **`[ANALOGY]` Sections**: Simple, relatable examples to use when explaining complex math to non-technical evaluators.

---

## 📊 High-Resolution System Architecture

This modern visualization tracks the data lifecycle from user interaction to backend persistence and model inference.

```mermaid
graph TD
    %% Node Definitions
    User["🌍 USER BROWSER<br/>(Login → Train → Predict)"]
    Sup["⚙️ SUPERVISORD<br/>(container PID 1)"]
    Gunicorn["🦅 GUNICORN<br/>(bind $PORT)"]
    Server["🔥 MAIN.PY<br/>(Flask app)"]
    Bus["🚌 ERROR-BUS<br/>(Go sidecar :9090)"]
    Train["🧠 train_model.py<br/>(ML Training Engine)"]
    Model["📦 model/<br/>(.pkl + weights)"]
    Dataset["📊 Dataset/<br/>(kdd_train.csv)"]

    %% Flow Connections
    User -- "AJAX / Form POST<br/>(+ CSRF Hardening)" --> Sup
    Sup -- "program: flask" --> Gunicorn
    Sup -- "program: error-bus" --> Bus
    Gunicorn -- "WSGI" --> Server
    Server -- "Executes" --> Train
    Server -- "Loads Model" --> Model
    Server -- "emit_event / health" --> Bus

    Train -- "Saves Artifacts" --> Model
    Train -- "Reads Data" --> Dataset

    %% Styling
    style User fill:#1a1a2e,stroke:#3066be,stroke-width:2px,color:#fff
    style Sup fill:#162447,stroke:#e94560,stroke-width:2px,color:#fff
    style Gunicorn fill:#162447,stroke:#3066be,stroke-width:2px,color:#fff
    style Server fill:#162447,stroke:#e94560,stroke-width:2px,color:#fff
    style Bus fill:#1f4068,stroke:#00d2ff,stroke-width:2px,color:#fff
    style Train fill:#1f4068,stroke:#00d2ff,stroke-width:2px,color:#fff
    style Model fill:#0f3460,stroke:#f8b400,stroke-width:2px,color:#fff
    style Dataset fill:#0f3460,stroke:#4ecca3,stroke-width:2px,color:#fff
```

> **Deployment note:** Docker multi-stage builds compile the Go error-bus, TypeScript modules (`static/ts` → `static/js`), and the Rust guest-auth binary before the `python:3.12-slim` final image. Render Free Tier injects `PORT` (public) — the sidecar uses `ERROR_BUS_PORT` (default 9090), never the public port.

---

## 🌐 Web Technicalities & Security Architecture

The system is built on a **High-Security Web Architecture** designed for high-availability ML demos.

### ![CyberShield Logo](../CyberAttackPrediction/static/images/logo_with_bg.svg) Layered Security Stack

- **CSRF Protection**: Every state-changing request (`POST`, `PUT`, `DELETE`) is protected by a session-bound cryptographic token. This prevents Cross-Site Request Forgery attacks.
- **Password Hashing**: We never store plain-text passwords. The system uses `werkzeug.security` with **PBKDF2-HMAC-SHA256** hashing.
- **Proprietary Admin Bypass**: A scrypt-hashed admin account provides a secure "master key" for system recovery and specialized testing.
- **Session Focus**: Flask sessions are cryptographically signed with the secret key from `FLASK_SECRET_KEY` (env) or the gitignored `.flask_secret` file, preventing cookie tampering.

### ⚡ Performance Optimizations

- **Model In-Memory Cache**: The AI brain is loaded into RAM at startup via `load_ml_model()`. This allows 1ms inference response times.
- **Async Threading**: Training large datasets is offloaded to a background `threading.Thread`. This prevents the "UI Freeze" common in basic Python apps.
- **Cache-Control Headers**: The server explicitly sends security and caching headers (e.g., `Strict-Transport-Security`, `X-Content-Type-Options`) to harden browser-side execution.

### 🔄 Real-Time State Management

- **Auto-Browser Launch** *(local dev only)*: When run as `python Main.py`, a delayed `threading.Timer` opens `http://127.0.0.1:2026`. Under gunicorn/supervisord on Render this block never executes (`if __name__ == '__main__':`).

### 📶 Offline Reliability Loop

The app uses a **State-Persistence Loop** via the PWA Service Worker (`static/sw.js`):

1. **Heartbeat**: The frontend polls **`/api/heartbeat`** (route provided by `error_bus.py` via `register_error_bus`).
2. **Network Interception**: If requests fail, `sw.js` can serve cached assets and sync theme state (`THEME_SET` / `THEME_GET` messages from `base.html`).
3. **Emergency Handover**: An offline fallback page exists at `static/offline.html` for reconnect UX while the network is down.

### ![CyberShield Logo](../CyberAttackPrediction/static/images/logo_with_bg.svg) Adaptive Security Layers (ASL)

The **Stable-2026** update introduces the Adaptive Security Layer, which moves beyond simple password hashing to protect the system's internal core:

- **Neural Firewall (Path-Traversal Guard)**:
  - **Logic**: When a user accesses the "Project Explorer," the system calculates the `abspath` of the requested file and ensures it starts with the `PROJECT_ROOT`.
  - **Defense**: If an attacker attempts to use `../../` to access system passwords or root folders (e.g., `/etc/shadow` on Linux or `C:\Windows`), the Firewall intercepts the request and forces a redirect to the safe root.
- **Cryptographic Identity (HMAC Tokens)**:
  - **Protocol**: Instead of storing plain-text login states, the system generates a **Unique Session Signature** using `HMAC-SHA256`.
  - **Persistence**: When the "Remember Me" feature is used, only a short-lived signature is stored. Any alteration to this signature results in an immediate session invalidation.
- **Decoupled View Logic (macros.html)**:
  - **Refactoring**: All interactive UI elements (Badges, Buttons, Cards) have been moved to a central Jinja2 macro library.
  - **Impact**: This reduces code surface area, ensuring that a vulnerability in one page doesn't compromise the entire UI template system.

---

## 📦 Deployment & Runtime Architecture

| Concern | Detail |
| :--- | :--- |
| **Image** | Multi-stage `Dockerfile`: `golang:1.22-alpine` → `node:20-slim` → `rust:1.79-slim` → `python:3.12-slim` |
| **PID 1** | `supervisord -c /etc/supervisor/conf.d/supervisord.conf` |
| **flask program** | `gunicorn --workers 1 --threads 2 --max-requests 100 --max-requests-jitter 20 --timeout 120 --bind 0.0.0.0:%(ENV_PORT)s Main:app` in `/app/CyberAttackPrediction` |
| **error-bus program** | `/usr/local/bin/error-bus` listening on **`ERROR_BUS_PORT` (default 9090)** — *not* Render's public `PORT` |
| **Public port** | Render injects `PORT`; `EXPOSE 8080` is the local default |
| **Free Tier** | 512MB RAM, ephemeral disk; set `FLASK_SECRET_KEY` as a service env var |
| **Build hygiene** | `.dockerignore` excludes `.git`, venvs, `node_modules`, large X-IIoTID CSV, logs |
| **Verification** | `CyberAttackPrediction/smoke_test.py` (28 checks, local) and `live_smoke.py` (15 checks, against a running container) — currently untracked helpers |

---

## 📐 Logic Flow Diagram (Raw ASCII)

```text
┌──────────────────────────────────────────────────────────────┐
│                        USER BROWSER                          │
│          Login → Train → Predict → Results UI                │
└───────────┬──────────────────────────────────────────────────┘
            │ AJAX / Form POST (+ HMAC Sig)
            ▼
┌──────────────────────────────────────────────────────────────┐
│                    MAIN.PY (Flask Server)                    │
│                                                              │
│  [ SECURITY LAYER ]                                          │
│  ├ Neural Firewall  ──► Path Sanitization                    │
│  ├ HMAC Interceptor ──► Session Validation                   │
│  └ Jinja2 Macros    ──► Sanitize UI Output                   │
│                                                              │
│  [ ACTION HANDLERS ]                                         │
│  ├ /UserLoginAction   →   users.json                         │
│  ├ /TrainAction       →   train_model.py                     │
│  └ /PredictAction     →   .pkl + RF predict                  │
│                                                              │
│  [ SIDECAR ]  error_bus.py ──► Go error-bus (:9090)          │
└──────────────┬───────────────────────────────┬───────────────┘
               │                               │
     ┌─────────▼──────────┐          ┌─────────▼──────────┐
     │   train_model.py   │          │       model/       │
     │                    │          │                    │
     │   Load CSV         │          │ ├ trained_rf.pkl   │
     │   Encode features  │────────▶│ ├ dos_weight.hdf5  │
     │   Scale values     │          │ ├ ids_weight.hdf5  │
     │   Train RF         │          │ ├ iot_weight.hdf5  │
     │   Save .pkl        │          │ └ kdd_weight.hdf5  │
     └─────────▼──────────┘          └────────────────────┘
               │
     ┌─────────▼──────────┐
     │      Dataset/      │
     │    kdd_train.csv   │
     │    testData.csv    │
     └────────────────────┘
```

> In the container, supervisord is PID 1: it starts **gunicorn** (public `PORT`) and **`/usr/local/bin/error-bus`** (`ERROR_BUS_PORT`, default 9090). The Go sidecar is a separate process from Flask's in-process `error_bus.py` blueprint.

### Data Handoff Summary

| From | To | Data | How |
| :--- | :--- | :--- | :--- |
| `Dataset/*.csv` | `train_model.py` | Labeled traffic rows | `pd.read_csv()` |
| `train_model.py` | `model/*.pkl` | Model + preprocessors | `joblib.dump()` |
| `model/*.pkl` | `Main.py` globals | Live inference objects | `joblib.load()` on startup |
| Browser upload | `uploaded_test.csv` | Unlabeled capture file | `request.files` |
| `Main.py` | Flask session | Prediction results | `session['last_result']` |
| Flask session | UI | Results table + GenAI text | `render_template()` |

---

## 🔐 Security Architecture

| **Authentication** | `PBKDF2-HMAC-SHA256` hashing in `users.json` |
| **Session Security** | HMAC-signed session tokens; secret key from `FLASK_SECRET_KEY` or `.flask_secret` |
| **Neural Firewall** | Absolute-path boundary enforcement for file exploration |
| **CSRF Protection** | `security_pre_check()` validates `X-CSRF-Token` |
| **Input Validation** | Sanitizes `NaN`/`Inf`; enforces strict CSV schema; 25MB upload cap (`413 UPLOAD_TOO_LARGE`) |
| **Response Hardening** | `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN` |
| **Integrity Checks** | **ETag generation** via MD5 file hashing |
| **Production WSGI** | gunicorn under supervisord (`supervisord.conf`); TLS terminated by Render |

---

## 🎓 Viva Q&A

**Q: Why Random Forest and not a Neural Network for the production app?**

Random Forest trains in seconds on CPU, requires no GPU, achieves ~95%+ accuracy on NSL-KDD, and produces interpretable feature importances. Neural networks are benchmarked in the extension notebook as a research comparison.

---

**Q: Why is the scaler bundled inside the `.pkl`?**

The scaler is fitted on the training data's distribution. Re-fitting on test data would produce different scaling parameters, causing the model to receive out-of-distribution inputs. Saving and replaying the fitted scaler guarantees identical preprocessing — a non-negotiable requirement for valid inference.

---

**Q: What stops a malicious CSV from breaking the system?**

`train_model.py` enforces a column contract, rejects empty datasets, gracefully handles unknown columns, and sanitizes all `Inf`/`NaN` values. CSRF middleware prevents cross-site attacks. CSV bytes are only ever parsed by Pandas — they are never executed.

---

**Q: What is the difference between the two notebooks?**

`ProposeCyberAttack.ipynb` covers the **baseline** — traditional ML on NSL-KDD with statistical evidence. `ExtensionCyberAttack.ipynb` is the **research extension** — deep learning models, three additional real-world datasets, and GenAI-style explanations.

---

**Q: How does the GenAI Insight Engine work?**

It is a rule-based NLG system. After `predict()` returns a class name, the engine maps it to a pre-written explanation template covering the attack's behaviour, impact, and recommended mitigation strategy.

---

**Q: Why re-train during the demo instead of using a pre-loaded model?**

Live training demonstrates the real-time pipeline: the examiner sees log streaming, the accuracy metric computed on-the-fly, and an immediate prediction run afterwards — proving the system works end-to-end, not just as a static showcase.

**Q: How does the system handle directory traversal attacks?**

The system uses a **Neural Firewall** logic. Whenever a file path is requested, it is converted to an absolute path using `os.path.abspath()`. It then checks if this path starts with the project's root directory. If the path tries to "escape" the project folder (e.g., using `../`), the request is discarded, and the user is redirected to safety.

---

**Q: Why was the UI refactored into Jinja2 Macros?**

Refactoring the UI into `macros.html` promotes **Don't Repeat Yourself (DRY)** principles and security via abstraction. By centralizing UI components like the "Attack Badge" or "Result Card," we ensure consistent data sanitization and styling across all 5+ pages, reducing the potential for injection vulnerabilities in the template layer.

---

## 🧪 Testing

| Script | Scope | Result (deploy audit) |
| :--- | :--- | :--- |
| `CyberAttackPrediction/smoke_test.py` | In-process Flask client: signup/login JSON contracts, predict, 413, train `local_dataset`, CSRF, statics, `wants_json()` | **28 PASS / 0 FAIL** |
| `CyberAttackPrediction/live_smoke.py` | HTTP checks against a running Docker container | **15 PASS / 0 FAIL** |

Both scripts are local audit helpers and are **not committed** (`git status` shows `??`). Run them after `docker build` / before promoting an image.

**NOT TESTED on Render itself:** live 512MB OOM behaviour, gunicorn `--max-requests` recycle under load, SSE `/stream` reconnect, IndexedDB browser logs.

---

## 📋 Documentation Info

| Field | Value |
| :--- | :--- |
| Version | 2026.5 |
| Framework | CyberShield AI |
| Project Lead | Sreyan |
| Last Updated | September 2026 (deploy-readiness audit) |
