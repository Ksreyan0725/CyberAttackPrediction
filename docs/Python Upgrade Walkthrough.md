<!-- markdownlint-disable MD033 -->
<h1 align="center">
  <img src="../CyberAttackPrediction/static/images/logo_with_bg.svg" alt="CyberShield Logo" width="32" vertical-align="middle"> CyberShield AI: Technical Hardening & Versioning Log
</h1>

<p align="center">
  <img src="../CyberAttackPrediction/static/images/banner.png" alt="CyberShield Architecture Banner" width="800">
</p>

This document tracks the technical evolution of the CyberShield AI project, from legacy modernization to high-performance security hardening.

---

## Phase 2: High-Performance Hardening (Python 3.13.12) 🚀

### Status: CURRENT / RECOMMENDED (2026 Stable) — local development

In this phase, we migrated the project to the **Python 3.13.12 Core** to leverage modern memory management and faster JIT (Just-In-Time) compilation for ML inference.

> **Deployment note (post-audit):** Local venv / notebooks stay on **Python 3.13.x**.
> The production Docker image and Render runtime use **`python:3.12-slim`**
> (`Dockerfile` final stage; `requirements.txt` header). Keep both in sync when
> adding native wheels.

### Key Accomplishments

1. **3.13.12 Runtime**: Finalized the local environment on the high-performance stable core.
2. **2026 Dependency Stack**:
    - **Scikit-Learn 1.8.0+**: Modern ensemble logic and faster Joblib serialization.
    - **Deep learning (TensorFlow/Keras)**: Research notebooks only — *not* pinned in `requirements.txt` or `requirements-dev.txt` for the web runtime (verify before citing a version in a report).
    - **Pandas 3.0.2+**: High-speed data ingestion.
3. **Terminal Profile Hardening**:
    - Restricted the IDE to **Windows PowerShell 5.1** for maximum administrative stability.
    - Enabled **Visible Activation**, ensuring the green `(.venv)` prefix is always active in the shell.
4. **Serialization Patch**: Standardized model artifacts on **Joblib**, reducing loading latency to sub-ms levels.

### Current Environment Verification

- **Active Interpreter**: Python 3.13.12 ('.venv': venv)
- **Path**: `<repo>\.venv` (project root under `Desktop\STUDY  MATERIALS (NOTES)\Project` on the current machine)
- **Shell**: Windows PowerShell 5.1 (Original Blue Shell)

---

## Phase 1: Legacy Modernization (Python 3.11) 📜

### Status: HISTORICAL / ARCHIVE

Initially, the project was modernized to reconcile legacy conflicts and enable modern IDE features. I successfully migrated the project from legacy Python 3.7.2 to Python 3.11.6.

### Key Improvements

1. **Modern Stack**: Upgraded to **Python 3.11**, resolving environment conflicts.
2. **Pylance Support**: Enabled full autocompletion and error-checking in VS Code.
3. **Model Retraining**: Patched `Series.ravel()` compatibility issues for modern Scikit-Learn.

### Historical Verification Results

- **Active Python**: Python 3.11.6
- **Result**: Successfully generated `trained_rf_model.pkl` compatible with 2024-standard libraries.

---

## Running the Intelligence Hub

Launch the application via the unified command center:

```powershell
python launcher.py
```

*Choose **Mode 1** for the Web Dashboard or **Mode 2** for Jupyter research. The (.venv) will persist automatically.*

**Container / production equivalent:**

```powershell
docker build -t cybershield .
docker run -p 8080:8080 -e PORT=8080 -e RENDER=true cybershield
```

(Supervisord starts gunicorn on `$PORT` and the error-bus on `ERROR_BUS_PORT=9090`.)

Built for Technical Excellence & Academic Integrity — 2026 ![CyberShield Logo](../CyberAttackPrediction/static/images/logo_with_bg.svg)
