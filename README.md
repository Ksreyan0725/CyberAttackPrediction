<!-- markdownlint-disable MD033 -->
<h1 align="center">
  <img src="CyberAttackPrediction/static/images/logo_with_bg.svg" alt="CyberShield Logo" width="32" vertical-align="middle"> Cyber Attack Prediction: From Traditional ML to Generative AI
</h1>

<p align="center">
  <img src="CyberAttackPrediction/static/images/favicon.svg" alt="CyberShield Favicon" width="128">
</p>

<h2 align="center">CyberShield AI</h2>

<p align="center">
  **Predicting network intrusions with precision. Explaining security with intelligence.**
</p>

![Python](https://img.shields.io/badge/Python-3.13.2-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-v3.1.3-000000?style=for-the-badge&logo=flask&logoColor=white) ![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-v1.8.0-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white) ![Status](https://img.shields.io/badge/Status-Stable--2026--Hardened-success?style=for-the-badge) [![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://cyberattackprediction.onrender.com/)

### 🚀 [Live Web Application](https://cyberattackprediction.onrender.com/)
Experience the live deployed model running on Render.
## 🏛️ Academic Institutional Details

- **Institution**: Roland Institute of Computer & Management Studies, Berhampur
- **Program**: Bachelor of Computer Applications (BCA) — Final Year
- **Session**: 2023–2026
- **Guide**: Mr. Rasmi Roy Badakumar

### 👥 The Development Team

- **Kumar Sreyan Pattanayak** (Roll: 23PBCA1355)
- **Ankita Pati** (Roll: 23PBCA1335)
- **Subhashree Pathy** (Roll: 23PBCA1386)
- **Tanmaya Ranjan Jena** (Roll: 23PBCA1391)

---

## 🌟 Executive Summary

**CyberShield AI** is a final-year Bachelor of Computer Applications (BCA) project that bridges the gap between traditional network security and modern Artificial Intelligence. By analyzing network traffic patterns using the industry-standard **NSL-KDD dataset**, the system classifies attacks into four primary families (DoS, Probe, R2L, U2R) and provides human-readable mitigation strategies via a simulated Generative AI engine.

---

## 🚀 Academic Quick Launch (Examiner Ready)

This project includes all necessary software. Follow these **5 steps** to launch the application for your viva:

1. **Install Python**: Open `python-3.13.12-amd64.exe` (must be installed manually or retrieved from python.org). Local dev uses Python 3.13.x; the Docker/Render container runs Python 3.12-slim.
2. **Configure Secrets**: Create a `.env` file in the project root (there is no `.env.example` — use the template in [Installation & Setup](#️-installation--setup) below). Alternatively, omit `FLASK_SECRET_KEY` and let the app auto-generate a gitignored `.flask_secret` file.
3. **Setup Dependencies**: Run `scripts/install_deps.ps1` to automatically prepare the high-performance environment.
4. **Unified Launch**: Run `scripts/start_launcher.bat` (or `launcher.py`) to access the **Command Center**. Choose **Mode 1** for the Web Dashboard or **Mode 2** for Jupyter research.
5. **Active Session Guard**: Start scripts now feature **Venv Persistence**, ensuring the `.venv` environment remains active and isolated for high-performance operation.

> [!TIP]
> **Admin Dashboard Bypass**: Use Username `admin` and Password `admin` to immediately access the full features and Master Badge interface.

---

## 💎 Key Features

- **🧠 Stacking Ensemble AI** — Multi-model architecture (Random Forest, KNN, MLP) achieving **98%+ accuracy**.
- **🤖 GenAI Mitigation Insights** — Converts classification results into plain-English advice for security administrators.
- **![CyberShield Logo](CyberAttackPrediction/static/images/logo_with_bg.svg) Stable-2026 Hardening** — Integrated **Neural Firewall** (path traversal protection) and **Cryptographic Identity** (HMAC session tokens).
- **🔍 Explainable AI (SHAP)** — Visualizes *why* a network packet was flagged using Shapley Additive Explanations.
- **📂 In-Browser Repository Explorer** — Logged-in users can browse and read all project files directly in the app, protected by root-level sandboxing.

---

## 📊 Project Foundations

![Project Roadmap](CyberAttackPrediction/static/images/roadmap_HD.png)
*The systematic development lifecycle from data ingestion to Generative AI integration.*

![Five Pillars](CyberAttackPrediction/static/images/five_pillars_HD.png)
*Aligning with cybersecurity frameworks for comprehensive monitoring and defense.*

---

## 🛠️ Installation & Setup

1. **Clone the repository**:

```bash
git clone https://github.com/Ksreyan0725/CyberAttackPrediction---College_Project.git
cd CyberAttackPrediction---College_Project
```

2. **Setup Virtual Environment**:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

3. **Install Dependencies**:

```bash
# Runtime / web app (also used by Docker)
pip install -r CyberAttackPrediction/requirements.txt

# Notebook / research stack (SHAP, matplotlib, Jupyter) — optional, local only
pip install -r CyberAttackPrediction/requirements-dev.txt
```

4. **Configure Environment** (optional for local runs):
   Create a `.env` file in the project root. There is **no** `.env.example` in the repo:

```env
FLASK_SECRET_KEY=your_secure_hex_key
ADMIN_USER=admin
ADMIN_PASS=admin
ADMIN_HASH=pbkdf2:sha256:600000$...
```

   If `FLASK_SECRET_KEY` is unset, `Main.py` auto-generates a persistent
   `CyberAttackPrediction/.flask_secret` (gitignored). On Render’s **ephemeral
   disk** that file is wiped on every redeploy — set `FLASK_SECRET_KEY` as a
   service environment variable in the dashboard so sessions stay stable.

5. **Run the Application** (local):
   Launch via `Start_WebApp_Venv.bat` or `python CyberAttackPrediction/Main.py`.
   The local dev server listens on `http://127.0.0.1:2026/`.

## 🐳 Deployment (Docker / Render Free Tier)

The production image is a **multi-stage Dockerfile** at the repo root:

| Stage | Base image | Builds |
| --- | --- | --- |
| `go-builder` | `golang:1.22-alpine` | Go error-bus sidecar → `/usr/local/bin/error-bus` |
| `ts-builder` | `node:20-slim` | `static/ts/*.ts` → `static/js/` |
| `rust-builder` | `rust:1.79-slim` | Rust guest-auth binary |
| final | `python:3.12-slim` | App + supervisord + gunicorn |

**Process model** (`supervisord.conf`):

- **flask**: `gunicorn --workers 1 --threads 2 --max-requests 100 --bind 0.0.0.0:${PORT} Main:app`
- **error-bus**: `/usr/local/bin/error-bus` on **`ERROR_BUS_PORT` (default `9090`)** — *not* Render’s public `PORT`

```bash
docker build -t cybershield .
docker run -p 8080:8080 -e PORT=8080 -e RENDER=true cybershield
```

**Render Free Tier notes**: 512MB RAM, ephemeral disk, platform injects `PORT`
and sets `RENDER=true` (disables `allow_custom` training on the live site).
No `render.yaml`/`Procfile` — configure the Docker runtime in the dashboard.

**Local verification** (not part of the image):

```bash
python CyberAttackPrediction/smoke_test.py   # 28 in-process checks
python CyberAttackPrediction/live_smoke.py   # 15 checks against a running container
```

> `smoke_test.py` and `live_smoke.py` are local audit helpers and are currently
> untracked in git.

## 🏗️ Project Structure

- 📁 [**CyberAttackPrediction/**](CyberAttackPrediction/) — Main project folder
  - 📁 [static/](CyberAttackPrediction/static/) — Styles, images, `sw.js`; `ts/` holds TypeScript sources (compiled to gitignored `js/` in Docker)
  - 📁 [templates/](CyberAttackPrediction/templates/) — HTML pages
  - 📁 [model/](CyberAttackPrediction/model/) — Saved AI model files
  - 📁 [Dataset/](CyberAttackPrediction/Dataset/) — Training & test CSVs (most tracked so Render can train; `uploaded_*.csv` / `custom_train.csv` ignored)
  - 📁 [error-bus/](CyberAttackPrediction/error-bus/) — Go sidecar source (`go.mod`, `main.go`; binary ignored)
  - 📁 [rust_auth/](CyberAttackPrediction/rust_auth/) — Rust guest-auth crate (`Cargo.lock` tracked)
  - 📁 [static/ts/](CyberAttackPrediction/static/ts/) — TypeScript sources + `package.json`
  - 🐍 **[Main.py](CyberAttackPrediction/Main.py)** — Flask backend (heart of the project)
  - 🐍 [error_bus.py](CyberAttackPrediction/error_bus.py) — In-process event/heartbeat routes
  - 🐍 [train_model.py](CyberAttackPrediction/train_model.py) — AI trainer script
  - 📔 [ExtensionCyberAttack.ipynb](CyberAttackPrediction/ExtensionCyberAttack.ipynb) — Research notebook (Phase 2)
  - 📔 [ProposeCyberAttack.ipynb](CyberAttackPrediction/ProposeCyberAttack.ipynb) — Research notebook (Phase 1)
  - 📄 [requirements.txt](CyberAttackPrediction/requirements.txt) — Runtime deps (Docker/Render)
  - 📄 [requirements-dev.txt](CyberAttackPrediction/requirements-dev.txt) — Notebook/SHAP stack (local only)
  - 📄 users.json — User registry (**gitignored**)
- 🐳 [Dockerfile](Dockerfile) — Multi-stage production image
- ⚙️ [supervisord.conf](supervisord.conf) — Runs gunicorn + error-bus in the container
- 📄 [.dockerignore](.dockerignore) — Keeps `.git`, venvs, node_modules, large CSVs out of the build context
- 📁 [**assets/**](assets/) — Project assets
  - 📁 [images/](assets/images/) — Academic flowcharts and diagrams
- 📁 [**docs/**](docs/) — Unified documentation hub
  - 📁 [reports/](docs/reports/) — Final reports in PDF and Word formats
  - 📁 [materials/](docs/materials/) — Reference books and technical guides
- 📁 [**scripts/**](scripts/) — Startup and installation scripts
  - ⚙️ [Start_WebApp_Venv.bat](scripts/Start_WebApp_Venv.bat) — Web app launcher
  - ⚙️ [Start_Jupyter_Venv.bat](scripts/Start_Jupyter_Venv.bat) — Jupyter launcher
  - 📜 [install_deps.ps1](scripts/install_deps.ps1) — Automated dependency installer
- 🐍 [launcher.py](launcher.py) — Unified command center
- 🔐 `.env` — Sensitive configuration & secrets (gitignored; optional if using `.flask_secret`)

**Git tracking rules (post-deploy audit):** error-bus *sources*, `Cargo.lock`,
and `static/ts/*` are tracked; `static/js/`, `node_modules/`, compiled binaries,
`.flask_secret`, `users.json`, and `.env` are ignored.

## 📡 API Contracts (frontend ↔ Flask)

- Requests with `Accept: application/json` (or `cyberFetch`) get a JSON envelope via `wants_json()`; HTML form posts keep normal redirects.
- **Login** (`/UserLoginAction`): `{ ok: true, data: { redirect: "/..." } }` (also accepts `data.redirect` at top level). Error codes: `INVALID_USERNAME`, `INVALID_PASSWORD`, etc.
- **Signup** (`/SignupAction`): accepts a JSON body *or* form data.
- **Train** (`/TrainAction`): multipart field `training_data` (file) or `local_dataset` (repo CSV name, e.g. `kdd_train.csv`).
- **Uploads**: 25MB max → `413` with `code: "UPLOAD_TOO_LARGE"`; training files capped at 5000 rows.
- `window.api` / `window.cyberFetch` are exposed from `base.html` for page scripts.

Built with ❤️ for Academic Excellence — 2026
