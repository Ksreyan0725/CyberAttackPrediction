# Cyber Attack Prediction — Comprehensive Project Guide (Updated 2026)

Welcome to the Cyber Attack Prediction project! This guide covers the modernized architecture, datasets, ML/DL models, Generative AI integration, and instructions for running the system.

---

## 1. Project Overview & Architecture

This project is an advanced Machine Learning and Deep Learning-based **Intrusion Detection System (IDS)** that classifies network traffic as **"Normal"** or a specific **"Cyber Attack"**.

The project features a hybrid architecture:

- **A. Research Environment** (Jupyter Notebooks): For data analysis, model comparison, and Deep Learning experiments.
- **B. Production Web Application** (Flask + Bootstrap 5): A modernized, responsive UI for real-time predictions.
- **C. Model Persistence Layer**: A training script (`train_model.py`) to save models, ensuring the web app is fast and efficient.
- **D. Generative AI Insight Engine**: Automatically generates natural language explanations and mitigation steps for detected attacks.
- **E. Deployment Layer** (Docker + Render): Multi-stage image builds the Go error-bus, TypeScript modules, and Rust guest-auth binary; **supervisord** runs **gunicorn** (Flask) + the **error-bus** sidecar. Target: Render Free Tier (512MB, ephemeral disk, public `PORT` injected by the platform).

---

## 2. Dataset Analysis

The system evaluates models across four major cybersecurity datasets:

- **NSL-KDD** (`kdd_train.csv`): Primary dataset for the web app and research baseline.
- **CICIDS 2017**, **CICDDoS 2019**, **X-IIoTID**: Used in the research notebooks for multi-algorithm benchmarking.
- **Custom Captures**: User-provided CSV files for testing and inference via the web app.

### Preprocessing Steps

| Step | What It Does |
| --- | --- |
| Label Encoding | Converts text/categorical columns to numbers |
| Imputation | Fills in missing values with means or zeros |
| Normalization | Scales all features to a comparable range using `StandardScaler` |

---

## 3. AI & Machine Learning Models

### Traditional ML & Deep Learning

- Random Forest, KNN, SVM, MLP, Logistic Regression, Naive Bayes
- Deep Neural Networks (DNN) built with Keras/TensorFlow

### Generative AI Integration *(New)*

After a prediction is made, the system provides a detailed AI-generated explanation of the threat and recommended security measures.

### Explainable AI (XAI)

Uses **SHAP** (SHapley Additive exPlanations) in the notebooks to visualize which network features most impacted the model's decision.

---

## 4. Folder Structure

### Inside `CyberAttackPrediction/`

| File / Folder | Description |
| --- | --- |
| `Main.py` | The Flask backend server (optimized for model loading) |
| `error_bus.py` | In-process event bus + `/api/heartbeat`, `/api/logs` routes |
| `error-bus/` | Go sidecar source (`go.mod`, `main.go`); binary is gitignored |
| `rust_auth/` | Rust guest-auth crate; `Cargo.lock` tracked for Docker builds |
| `static/ts/` | TypeScript sources compiled to `static/js/` inside Docker |
| `train_model.py` | Run this to train and save the ML model to disk |
| `.env` | Optional local secrets (`FLASK_SECRET_KEY`, admin creds) |
| `templates/base.html` | Modern Jinja2 base template with Bootstrap 5 |
| `model/trained_rf_model.pkl` | The persistent, pre-trained model file |
| `requirements.txt` | Runtime deps (Flask, gunicorn, requests, scikit-learn) |
| `requirements-dev.txt` | Notebook/SHAP stack (Jupyter, matplotlib) — local only |
| `smoke_test.py` / `live_smoke.py` | Local audit smoke tests (untracked) |

### Inside the main `Project/` folder

| File / Folder | Description |
| --- | --- |
| `Dockerfile` | Multi-stage production image (Go + TS + Rust + Python) |
| `supervisord.conf` | Runs gunicorn (`$PORT`) + error-bus (`ERROR_BUS_PORT=9090`) |
| `.dockerignore` | Excludes `.git`, venvs, node_modules, large CSVs from build |
| `.venv` | Isolated Python virtual environment containing all libraries |
| `.gitignore` | Tracks deploy sources/datasets; ignores binaries, `static/js/`, `node_modules/`, `.env`, `.flask_secret`, `users.json` |

---

## 5. How to Run the Project

### Step 1: Initial Setup *(First Time Only)*

1. Open a terminal in the project root.
2. **Setup Secrets** (optional locally): Create a `.env` file in the project root. There is **no** `.env.example` in the repo — use:

   ```env
   FLASK_SECRET_KEY=generate_a_long_hex_key
   ADMIN_USER=admin
   ADMIN_PASS=admin
   ```

   If `FLASK_SECRET_KEY` is omitted, `Main.py` auto-generates a gitignored
   `.flask_secret`. On Render, set `FLASK_SECRET_KEY` as a service env var so
   the session key survives deploys (the disk is ephemeral).

3. Install dependencies:

   ```bat
   .venv\Scripts\python.exe -m pip install -r CyberAttackPrediction\requirements.txt
   .venv\Scripts\python.exe -m pip install -r CyberAttackPrediction\requirements-dev.txt
   ```

   (`requirements.txt` = runtime/Docker; `requirements-dev.txt` = notebooks/SHAP.)

4. Train the model:

   ```bat
   .venv\Scripts\python.exe CyberAttackPrediction\train_model.py
   ```

### Step 2: Running the Project

#### A. Research & Notebooks

1. Double-click **`Start_Jupyter_Venv.bat`** in the main folder.
2. Open `ExtensionCyberAttack.ipynb` or `ProposeCyberAttack.ipynb`.
3. Run cells to view graphs, model comparisons, and SHAP plots.

#### B. User-Facing Web Application (local)

1. Double-click **`Start_WebApp_Venv.bat`** in the main folder.
2. Wait for `Running on http://127.0.0.1:2026/` in the terminal.
3. Open <http://127.0.0.1:2026> in your browser.
4. Login using the credentials defined in your `.env` file *(Default: admin / admin)*.
5. Upload `testData.csv` to see real-time predictions and AI insights.

#### C. Production / Container (Docker → Render)

```bash
docker build -t cybershield .
docker run -p 8080:8080 -e PORT=8080 -e RENDER=true cybershield
```

- **flask** (gunicorn) binds `0.0.0.0:$PORT` (Render injects `PORT`).
- **error-bus** listens on `ERROR_BUS_PORT` (default **9090**), never on the public `PORT`.
- Verify after boot: `python CyberAttackPrediction/smoke_test.py` (local) or `live_smoke.py` against a running container.

Live demo: <https://cyberattackprediction.onrender.com/>

> **Important:** Always use the `.bat` files or the `.venv` path to ensure you are using the correct Python version and libraries.
