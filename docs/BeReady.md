# PROJECT READINESS SYLLABUS

**Project Title:** Cyber Attack Prediction: From Traditional ML to Generative AI

**Team Prepared For:** Viva Voce / Seminar Presentation

**Academic Year:** 2023–2026

**Programme:** Bachelor of Computer Applications (BCA) — Final Year

**Total Preparation Hours:** ~18 Hours

---

## COURSE OBJECTIVE

To ensure every team member can confidently understand, explain, demonstrate, and
defend all technical and conceptual aspects of this project during viva, seminar,
or panel evaluation.

---

## LEARNING OUTCOMES

Upon completing self-study of this project, the student will be able to:

- Identify and explain all 4 NSL-KDD attack families and specific attack mechanics
  (Neptune, Smurf, Satan) with reference to the dataset features.
- Trace the full ML pipeline in `train_model.py` from raw data to a saved `.pkl` model,
  explaining every preprocessing step and design decision.
- Justify the use of Random Forest and StackingClassifier and compare their accuracy,
  training time, and architecture.
- Interpret SHAP Summary Plots generated in `ExtensionCyberAttack.ipynb` and explain
  which features influenced each prediction and why.
- Describe the Flask web application architecture in `Main.py` including all routes,
  session management, and the prediction pipeline.
- Explain the current GenAI insight mechanism and articulate what changes are needed
  to integrate a live LLM like Google Gemini.
- Critically evaluate the limitations of the system and propose at least 3 specific,
  evidence-based improvements with justification.

---

## UNIT I: THE PROBLEM SPACE — NETWORKS AND CYBER ATTACKS

**Hours:** 3 | **Files to Open:** `PROJECT_GUIDE.md`

### Unit I — Core Topics

- What is the NSL-KDD dataset and why is it used in this project?
- The 4 attack families the model classifies: DoS, Probe, R2L, U2R.
- Specific attacks you must know: Neptune, Smurf, Satan, Guess_Passwd, Rootkit.
- The 41 network features — 3 categories:

| Category | Count | Examples |
| --- | --- | --- |
| Basic | 9 | `duration`, `protocol_type`, `src_bytes`, `dst_bytes` |
| Content | 13 | `logged_in`, `num_compromised`, `root_shell` |
| Traffic | 9 | `count`, `srv_count`, `dst_host_count` |

- How does a SYN Flood (Neptune) attack work step by step?
- What does the `flag` column represent? (`SF` = normal, `S0` = half-open/attack indicator).
- What is an IDS and why is this project an anomaly-based IDS?

### Unit I — Viva Questions

- Why did you choose this dataset over others?
- What is the difference between DoS and DDoS?
- What is U2R and why is it the most dangerous attack type?

---

## UNIT II: THE MACHINE LEARNING PIPELINE

**Hours:** 5 | **Files to Open:** `train_model.py`, `ProposeCyberAttack.ipynb`

### Unit II — Core Topics

- The complete preprocessing steps executed in `train_model.py`:
  - Load data with `pd.read_csv()` (limited to 20,000 rows for performance)
  - Fill missing values using `df.fillna(0)`
  - Label-encode categorical columns (`protocol_type`, `service`, `flag`)
  - Save original label names: `labels_list = np.unique(dataset['labels'])`
  - Split features and target: `X` and `y`
  - Apply `train_test_split()` with 80/20 ratio and `random_state=42`
  - Normalize with `StandardScaler` (fit on train only, transform both)
- Why `RandomForestClassifier` is used: 100 trees vote, reduces overfitting.
- The 4 evaluation metrics and what they mean in a cybersecurity context:

| Metric | Formula | Importance in This Project |
| --- | --- | --- |
| Accuracy | Correct / Total | Overall health of the model |
| Precision | TP / (TP + FP) | Avoid false alarms |
| Recall | TP / (TP + FN) | Never miss a real attack |
| F1-Score | 2×P×R / (P+R) | Balance between precision and recall |

- Why the model is saved with `pickle` into `model/trained_rf_model.pkl` as a
  dictionary: `{'model': rf, 'scaler': scaler, 'labels': labels_list}`.
- Why `n_jobs=-1` is set: uses all CPU cores, reduces training time significantly.

### Unit II — Viva Questions

- What happens if you forget to call `StandardScaler.transform()` on the test data?
- Why do we save `labels_list` before encoding, not after?
- Why do we use `random_state=42`?

---

## UNIT III: THE EXTENSION — STACKING AND EXPLAINABLE AI

**Hours:** 4 | **Files to Open:** `ExtensionCyberAttack.ipynb`

### Unit III — Core Topics

- What is `StackingClassifier`? Combines 3 base models whose outputs feed a meta-learner.
- The 3 base estimators used in this project:

| Model | Role | Key Setting |
| --- | --- | --- |
| `RandomForestClassifier` | Tree ensemble | `n_jobs=-1`, `n_estimators=100` |
| `MLPClassifier` | Neural network | `early_stopping=True`, `max_iter=100` |
| `KNeighborsClassifier` | Distance-based | `n_neighbors=5` |

- Why `cv=3` is used in `StackingClassifier`: generates out-of-fold predictions
  without data leakage.
- What is SHAP? SHapley Additive exPlanations — assigns each feature a contribution
  score for each prediction.
- The SHAP fix for multi-class output: `shap_values[:, :, 0]` selects class-0
  SHAP values because SHAP v0.40+ returns a 3D array.
- Reading a SHAP Summary Plot:
  - X-axis: SHAP value (positive = pushes toward "Attack")
  - Color: Red = high feature value, Blue = low
  - Y-axis: Features ranked by importance
- Why `feature_names` must be passed explicitly (column names lost after `StandardScaler`).

### Unit III — Viva Questions

- What is the difference between Random Forest and StackingClassifier?
- What does a high SHAP value for `src_bytes` mean?
- Why is Explainable AI important specifically in cybersecurity?

---

## UNIT IV: THE WEB APPLICATION

**Hours:** 4 | **Files to Open:** `Main.py`, `templates/`

### Unit IV — Core Topics

- The complete route map of the Flask application (key routes; `Main.py` registers ~35 plus routes added by `error_bus.py`):

| Route | Method | What It Does |
| --- | --- | --- |
| `/`, `/index` | GET | Landing / redirects toward login |
| `/UserLogin` | GET, POST | Login form |
| `/UserLoginAction` | POST | Credential check (form or JSON) → `{ok, data.redirect}` |
| `/Signup`, `/SignupAction` | GET / POST | Registration (JSON body or form) |
| `/GuestLogin` | POST | Guest session |
| `/Predict`, `/PredictView` | GET | CSV upload / results view |
| `/PredictAction` | POST | Runs model prediction |
| `/Train` | GET | Training page + local dataset list |
| `/TrainAction` | POST | Starts training (`training_data` file or `local_dataset`) |
| `/Logout` | **POST** | Clears session, redirects to login |
| `/Account` | GET | Account settings |
| `/api/clear-session` | POST | Clears prediction session keys |
| `/api/heartbeat` | GET, POST | Health/pulse (registered by `error_bus.py`) |
| `/api/logs` | GET | Recent error-bus events (registered by `error_bus.py`) |

- How session protection works in every route:

  ```python
  if 'user' not in session:
      return redirect('/UserLogin')
  ```

- How credentials are kept secure: hashed passwords in `users.json` (PBKDF2 via Werkzeug); optional `.env` + `load_dotenv()` for admin bootstrap. Session secret = `FLASK_SECRET_KEY` env **or** gitignored `.flask_secret`.
- Why the model is loaded once at startup (`load_ml_model()`) and not per request.
- The full prediction flow in `PredictAction()`:
  - Enforce 25MB cap → `413 UPLOAD_TOO_LARGE` for oversized bodies
  - Read uploaded data into Pandas DataFrame
  - Rename and encode columns using the same `LabelEncoder` logic
  - Apply saved `StandardScaler.transform()`
  - Call `model.predict()` to get integer predictions
  - Decode integers back: `labels_list[pred]`
  - Look up GenAI insight from the dictionary
  - Pass results to the result template via `render_template()` (or JSON if `wants_json()`)
- Why training runs in a background `threading.Thread`: Flask/gunicorn would otherwise block worker threads for the whole fit.
- The `Timer(1.5, open_browser).start()` pattern: **local dev only** (`if __name__ == '__main__'`). Under gunicorn/supervisord on Render it never runs.

### Unit IV — Viva Questions

- What happens if `app.secret_key` is not set?
- What does `session.clear()` do?
- What is the difference between `request.form` and `request.files`?

---

## UNIT V: GENERATIVE AI INSIGHTS

**Hours:** 1 | **Files to Open:** `Main.py` (insight dictionary section)

### Unit V — Core Topics

- How the current GenAI insight works: a Python `dict` maps each attack label to a
  professional explanation and 3 mitigation recommendations.
- Why this approach works for a BCA project: deterministic, fast, no API cost,
  no internet required during demo.
- The upgrade path to a live API call:

  ```python
  import google.generativeai as genai
  model = genai.GenerativeModel('gemini-pro')
  response = model.generate_content(f"Explain {attack} and suggest 3 mitigations.")
  ```

- Prompt engineering: specificity matters — include the attack name and top SHAP
  features in the prompt for actionable, context-aware security guidance.

### Unit V — Viva Questions

- Is your project using a real Large Language Model?
- What would you need to change to use Google Gemini for real insights?
- What is prompt engineering?

---

## UNIT VI: DESIGN DECISIONS AND ETHICS

**Hours:** 1 | **Files to Open:** `PROJECT_GUIDE.md` (Sections I and K)

### Unit VI — Core Topics

- Why Flask over Django: lightweight, minimal overhead, perfect for a focused ML demo.
- Why pickle over retraining: training takes seconds; inference must be milliseconds.
- Why `nrows=20000` in training: trade-off between speed and accuracy for a live demo.
- Why Glassmorphism UI: modern aesthetic matching current industry design trends.
- Ethical considerations of this project:
  - False positives block legitimate users.
  - Network traffic data is sensitive — must not be logged indefinitely.
  - AI decisions must be auditable, not black-box — hence SHAP.

### Unit VI — Viva Questions

- What is the biggest limitation of your current system?
- Propose 2 improvements you would make with more time.
- What is model drift and how would you detect it?

---

## VIVA READINESS CHECKLIST

### Unit I — Problem Space

- [ ] I can name all 4 attack families with one real example each.
- [ ] I can explain how a SYN Flood (Neptune) attack works step by step.
- [ ] I know what columns `protocol_type`, `src_bytes`, and `flag` represent.
- [ ] I can explain why NSL-KDD is better than KDD'99.

### Unit II — ML Pipeline

- [ ] I can trace the 7 preprocessing steps from raw data to `StandardScaler`.
- [ ] I can explain why Recall matters more than Precision in this context.
- [ ] I know what's inside `trained_rf_model.pkl` and why it's a dictionary.

### Unit III — Extension and SHAP

- [ ] I can explain the role of each of the 3 base models in the stacker.
- [ ] I can read a SHAP Summary Plot and describe what the axes mean.
- [ ] I know why `shap_values[:, :, 0]` is used and what it selects.

### Unit IV — Web Application

- [ ] I can trace a data upload from browser click to prediction on screen.
- [ ] I can explain how session management protects routes.
- [ ] I know why training runs in a background thread.
- [ ] I can state the login JSON contract (`{ok, data.redirect}`) and the 413/`UPLOAD_TOO_LARGE` behaviour.
- [ ] I know the production process model: supervisord → gunicorn (`$PORT`) + error-bus (`ERROR_BUS_PORT=9090`).

### Unit V and VI — GenAI and Design

- [ ] I can explain the current insight mechanism and how to upgrade it.
- [ ] I can state 2 ethical concerns and 2 future improvements confidently.

---

## STUDY SCHEDULE

| Day | Hours | Focus |
| --- | --- | --- |
| Day 1 | 3 hrs | Unit I — Dataset, attacks, and the 41 features |
| Day 2 | 3 hrs | Unit II — Run `train_model.py`, trace every line |
| Day 3 | 2 hrs | Unit III — Open `ExtensionCyberAttack.ipynb`, run SHAP |
| Day 4 | 3 hrs | Unit IV — Open `Main.py`, trace a full predict request |
| Day 5 | 1.5 hrs | Unit V and VI — GenAI and design decisions |
| Day 6 | 2 hrs | Full demo run and viva checklist answer rehearsal |
| Day 7 | 1.5 hrs | Weak topic revision and verbal explanation practice |

---

## PROJECT FILE REFERENCE

### `train_model.py`

**Purpose:** Trains the Random Forest model and saves it to disk.

- Focus on: `pd.read_csv()` with `nrows=20000`, `LabelEncoder` loop, `StandardScaler` fit/transform
- Focus on: `np.unique(dataset['labels'])` saved **before** encoding — this is a common viva trap
- Focus on: `pickle.dump({'model': rf, 'scaler': scaler, 'labels': labels_list}, f)` — structure of the saved dict
- Covers: Unit II topics — preprocessing pipeline, model training, metric evaluation

---

### `Main.py`

**Purpose:** Flask web application — routing, session management, prediction, training trigger.

- Focus on: `load_ml_model()` — loaded once at startup, stored in global variable
- Focus on: `PredictAction()` — the full predict pipeline (encode → scale → predict → decode → insight) plus 25MB/`413 UPLOAD_TOO_LARGE` handling
- Focus on: `wants_json()` — switches responses between JSON envelopes and HTML redirects
- Focus on: `@app.route` decorators, `session['user']` checks on every protected route
- Focus on: `threading.Thread(target=run_training).start()` — async training pattern
- Focus on: Session secret — `FLASK_SECRET_KEY` env or persistent `.flask_secret` file
- Focus on: `Timer(1.5, open_browser).start()` — local-only auto-launch (not used under gunicorn)
- Covers: Unit IV topics — all Flask routes, session, env vars, async training, API contracts

---

### `ProposeCyberAttack.ipynb`

**Purpose:** The proposed solution — standard Random Forest classifier on NSL-KDD.

- Focus on: Data loading, Label Encoding loop across categorical columns
- Focus on: `RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)`
- Focus on: `classification_report()` output — be ready to read precision/recall/F1 per class
- Focus on: Confusion matrix visualization — know what TP, FP, FN, TN represent on it
- Covers: Unit I (dataset structure) + Unit II (full ML pipeline, evaluation metrics)

---

### `ExtensionCyberAttack.ipynb`

**Purpose:** The extension solution — StackingClassifier + SHAP explainability.

- Focus on: `StackingClassifier` definition — 3 base estimators + meta-learner
- Focus on: `MLPClassifier(early_stopping=True, max_iter=100)` — why these settings
- Focus on: `shap.TreeExplainer(rf)` → `shap_values[:, :, 0]` — the 3D array fix
- Focus on: `shap.summary_plot()` with `feature_names` passed explicitly
- Focus on: Performance comparison table between Proposed and Extension models
- Covers: Unit III topics — stacking, MLP, KNN, SHAP interpretation

---

### `docs/PROJECT_GUIDE.md`

**Purpose:** Deep technical reference — 100 viva Q&A, feature dictionary, troubleshooting.

- Focus on: Section B (Project Architecture) — the system flow diagram in text
- Focus on: Section C (ML Algorithms) — RF, Stacking, MLP, KNN explained
- Focus on: Section D (Cybersecurity) — attack mechanics, NSL-KDD, IDS types
- Focus on: Troubleshooting Encyclopedia — 25 real errors and their project-specific fixes
- Covers: Revision reference for all 6 units

---

### `.env` (and `.flask_secret`)

**Purpose:** Stores sensitive credentials outside the codebase.

- Contains (optional): `FLASK_SECRET_KEY`, `ADMIN_USER`, `ADMIN_PASS`
- Session secret: if `FLASK_SECRET_KEY` is unset, `Main.py` uses/creates gitignored `.flask_secret`
- Key rule: Never commit `.env` or `.flask_secret` — both are listed in `.gitignore`
- Loaded by: `load_dotenv()` at the top of `Main.py` (when the file exists)
- On Render: set `FLASK_SECRET_KEY` as a service env var (ephemeral disk wipes files)
- Covers: Unit IV — environment variable security, session key configuration

---

### `templates/` folder

**Purpose:** All HTML pages rendered by Flask via Jinja2.

- Files to know: `login.html`, `home.html`, `predict.html`, `result.html`
- Focus on: How `{{ variable }}` injects Python data into HTML
- Focus on: How `{% if 'user' in session %}` conditionally shows logout button
- Covers: Unit IV — Jinja2 templating, frontend rendering

---

### `README.md` (Root)

**Purpose:** Project homepage, installation guide, and key feature showcase.

- Focus on: **Key Features** list — ready to orally describe the "Liquid Glass UI" and "Explainable AI".
- Focus on: **Deployment (Docker / Render)** section for the production process model.
- Focus on: **Installation & Setup** and **API Contracts** in case you're asked how to set it up or how the frontend talks to Flask.
- Covers: Unit IV and VI — Web UI features, deployment, and overall project design.

---

Prepared for the project team — BCA Final Year, 2023–2026

Roland Institute of Computer and Management Studies
