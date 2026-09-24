
# ![CyberShield Logo](../CyberAttackPrediction/static/images/logo_with_bg.svg) 🎓 FINAL YEAR PROJECT: CYBER ATTACK PREDICTION SYSTEM

## Academic Year 2023-2026 | 6th Semester Project

---

## 🏛️ COLLEGE & TEAM INFORMATION

**Institution**: Roland Institute of Computer & Mgmt. Studies, Surya Vihar, Berhampur
**Project Title**: Cyber Attack Prediction: From Traditional ML to Generative AI
**Guide Teacher**: Mr. Rasmi Roy Badakumar

### 👥 THE TEAM MEMBERS

1. **ANKITA PATI** (Roll No: 23PBCA1335)
2. **KUMAR SREYAN PATTANAYAK** (Roll No: 23PBCA1355)
3. **SUBHASHREE PATHY** (Roll No: 23PBCA1386)
4. **TANMAYA RANJAN JENA** (Roll No: 23PBCA1391)

---

## 📢 PRESENTATION TALKING POINTS (STEP-BY-STEP)

*Follow these points for your seminar/viva to sound confident!*

1. **Introduction**: "Good morning/afternoon. We are presenting our project on Cyber Attack Prediction. In today's world, everything is online, and hackers are always trying to steal data. Our project uses AI to stop them."
2. **The Problem**: "Usually, security systems only block known hackers. But what if a new hacker comes? Our system uses Machine Learning to 'learn' how hackers behave, so it can catch new ones too."
3. **The Solution**: "We built a website where you can upload network data. Our AI checks the data and tells you if there is an attack like a 'SYN Flood' or 'Password Guessing'."
4. **The 'GenAI' Part**: "The best part is our Generative AI. It doesn't just say 'Attack'; it explains the attack in simple English and tells the user exactly how to fix it."
5. **Conclusion**: "Our system is fast, accurate, and easy to use even for people who don't know much about computers."

---

## 🛠️ INDIVIDUAL MEMBER CONTRIBUTIONS

*If the teacher asks "What did YOU do?", here are your answers:*

- **Ankita Pati**: "I worked on the **Data Research and Problem Scope**. I studied the NSL-KDD dataset and identified the 41 behavior clues (features) that help the project distinguish between a normal user and a hacker."
- **Subhashree Pathy**: "I focused on the **User Interface and Visual Delivery**. I designed the real-time Dashboard to ensure that clear security insights are always visible to the network administrator."
- **Kumar Sreyan Pattanayak**: "I was responsible for the **Core AI Brain and Backend Engine**. I built the Random Forest classification logic and the Generative AI Insight Engine that explains attacks in plain English."
- **Tanmaya Ranjan Jena**: "I handled the **System Testing and Performance Verification**. I benchmarked the final accuracy and helped document the results to ensure the project is stable and ready for real-world use."

---

## 🔄 THE DATA FLOW DIAGRAM (HOW IT WORKS)

*This simple diagram shows how a user's file becomes a smart prediction.*

```text
[ USER ]
   │
   ▼
( Uploads CSV File )
   │
   ▼
[ FLASK BACKEND (Main.py) ] <─── Loads ─── [ TRAINED AI MODEL ]
   │                                            (.pkl file)
   ▼
( Cleans & Processes Data )
   │
   ▼
[ PREDICTION ENGINE ] ─── Checks ───► [ ATTACK DICTIONARY ]
   │                                     (GenAI Insights)
   ▼
[ FINAL RESULT PAGE ]
( Shows Attack Type + AI Advice )
```

---

## 🔐 THE "SECURITY GUARD" ANALOGY (EXPLAINING THE PROJECT)

Imagine a very busy school gate (The Internet). Thousands of students (Data) enter every day.

- **Traditional Security**: The guard has a list of "Banned People." If someone on the list shows up, they are stopped. But what if a new troublemaker arrives? The guard won't know!
- **Our AI Security (ML)**: Instead of just a list, the guard is "trained" to watch behavior. If someone is running too fast, wearing a mask, or trying to climb a wall, the guard stops them—even if they've never seen that person before.
- **The Helpful Report (GenAI)**: After stopping the person, the guard doesn't just say "Get out." The guard gives a detailed report: "I stopped this person because they were carrying a spray-can. I suggest we lock the art room."

---

## 📑 TABLE OF CONTENTS

1. [THE BIG PICTURE (FOR NON-TECH READERS)](#the-big-picture-simple-explanation)
2. [CORE CONCEPTS & TERMINOLOGY](#core-concepts--terminology)
3. [PROJECT ARCHITECTURE: THE FRONTEND & BACKEND SPLIT](#project-architecture)
4. [ALGORITHMIC DEEP DIVE (THE MATH & LOGIC)](#algorithmic-deep-dive)
5. [EXHAUSTIVE FILE-BY-FILE DOCUMENTATION](#exhaustive-file-by-file-documentation)
6. [DETAILED FUNCTION-BY-FUNCTION LOGIC](#detailed-function-by-function-logic)
7. [THE STEP-BY-STEP DATA LIFECYCLE](#the-step-by-step-data-lifecycle)
8. [DATASET FEATURE DICTIONARY (ALL 41 COLUMNS EXPLAINED)](#dataset-feature-dictionary)
9. [ATTACK TAXONOMY: UNDERSTANDING THE THREATS](#attack-taxonomy)
10. [EXPLAINABLE AI (XAI) & SHAP INTERPRETATION](#explainable-ai-xai--shap-interpretation)
11. [GENERATIVE AI INSIGHT ENGINE: HOW IT WORKS](#generative-ai-insight-engine)
12. [VIVA PREPARATION: TOP 100 QUESTIONS & ANSWERS](#viva-preparation-top-100-questions--answers)
13. [INSTALLATION & THE TROUBLESHOOTING ENCYCLOPEDIA](#troubleshooting-encyclopedia)

14. [SECURITY, ETHICS & BEST PRACTICES](#security-ethics--best-practices)
15. [FUTURE ROADMAP & EXTENSIONS](#future-roadmap--extensions)
16. [GLOSSARY OF TERMS](#glossary-of-terms)

---

## THE BIG PICTURE SIMPLE EXPLANATION

### 🏫 The "Security Guard" Analogy

Imagine a school gate where many people enter every day.

- **Traditional Security (Old Way)**: The guard only stops people on a "Banned List." If a new thief comes who is not on the list, the guard lets them in!
- **Our AI Security (Our Project)**: The guard is smart. He watches *behavior*. If someone is trying to climb a wall or running too fast, he stops them, even if he doesn't know their name.
- **The Helpful Report (GenAI)**: After stopping the thief, the guard tells the school: "I stopped this person because they were carrying a spray-can. I suggest we lock the art room."

### 🔍 Why do we need this?

The internet is like a massive highway. Millions of pieces of information travel every second. Humans cannot watch it all. Our AI is like a super-fast robot that watches the highway 24/7 and stops hackers before they can steal anything.

### 🤖 Old Machine Learning vs. New Generative AI

- **Old Machine Learning**: Like a doctor who only says "You have a fever." (Just identifies the problem).
- **Generative AI (Our Project)**: Like a doctor who says "You have a fever, here is the medicine, and here is how to stay healthy next time." (Explains the problem and gives a solution).

### 📶 Offline-First Resilience (PWA)

Our system is built to survive in hostile network environments.

- **Service Worker**: `static/sw.js` is registered from `base.html`. It caches critical assets and handles theme sync messages from the page.
- **Pulse Detection**: The page polls `/api/heartbeat` (registered by `error_bus.py`) and reacts to connectivity loss. An offline fallback page exists at `static/offline.html`.

---

## CORE CONCEPTS & TERMINOLOGY

### Intrusion Detection System (IDS)

A software application that monitors a network or systems for malicious activity or policy violations.

### Anomaly vs. Signature Detection

- **Signature Detection**: Looks for specific patterns (like a fingerprint). It's fast but misses new attacks.
- **Anomaly Detection**: Looks for anything that isn't "normal." It's great at catching new attacks but can sometimes flag innocent users (False Positives).

### The Datasets (The Textbooks)

- **NSL-KDD**: Our primary dataset. It's a clean version of the classic KDD cup data.

---

## PROJECT ARCHITECTURE

### 🏗️ The Backend (The "Engine Room")

- **Language**: Python.
- **Framework**: Flask, served in production by **gunicorn** (1 worker / 2 threads) under **supervisord**.
- **Role**: It does the heavy lifting. It calculates the math, loads the AI models, and talks to the data files. It's the "Brain" that decides if a user is a hacker.

### 🎨 The Frontend (The "Face")

- **Language**: HTML, CSS (Bootstrap 5), TypeScript (`static/ts/` → compiled `static/js/` in Docker).
- **Role**: It's what the user sees. The buttons, the tables, and the colors. It makes complex AI data look beautiful and easy to understand.

### 🐳 The Deployment Layer

- **Multi-stage Dockerfile**: builds a Go **error-bus** sidecar, TypeScript modules, and a Rust guest-auth binary, then packages everything on `python:3.12-slim`.
- **supervisord**: runs `gunicorn --bind 0.0.0.0:$PORT Main:app` plus `/usr/local/bin/error-bus` on **`ERROR_BUS_PORT` (default 9090)** — the sidecar never binds Render's public `PORT`.
- **Target**: Render Free Tier (512MB RAM, ephemeral disk, injects `PORT` / `RENDER=true`). Session secret comes from `FLASK_SECRET_KEY` or a gitignored `.flask_secret` file.

---

## ALGORITHMIC DEEP DIVE

### 🌲 Random Forest (The Wisdom of the Crowd)

Imagine asking 100 people if a fruit is an apple. If 90 say yes, it's probably an apple. Random Forest uses 100 "Decision Trees" to vote on an attack. It's incredibly accurate.

### 🧠 Deep Neural Networks (DNN)

These are inspired by the human brain. They have "neurons" (mathematical functions) that pass information to each other. They are excellent at finding very hidden secrets in data.

### 🤝 Hybrid Stacking (The Council of Experts)

We take three different AI models (MLP, KNN, Random Forest) and let them all guess. Then, a final "Meta-Model" decides which guess is the best. It's like having a panel of expert doctors consulting on one patient.

---

## EXHAUSTIVE FILE-BY-FILE DOCUMENTATION

### 📁 ROOT DIRECTORY: The Command Center

#### 1. `.venv/` (Directory)

- **What is it?**: A "Bubble" for Python.
- **Detailed Logic**: Python versions change all the time. If you have Python 3.14 on your PC but this project needs **3.13.12**, they will fight. The `.venv` folder contains its own private copy of Python. It ensures the project works forever, even if you update your PC.

#### 2. `Start_WebApp_Venv.bat` (Automation)

- **Line-by-Line Logic**:
  - `@echo off`: Keeps the window clean.
  - `call .venv\Scripts\activate`: "Wakes up" the project bubble.
  - `python CyberAttackPrediction\Main.py`: Starts the website.
- **Role**: It's the "Start Button" for the whole system.

#### 3. `Start_Jupyter_Venv.bat` (Automation)

- **Role**: The "Laboratory Launcher."
- **Detailed Logic**: This activates the environment and immediately launches Jupyter Lab. It allows the research team to interact with the notebooks without manually typing terminal commands.

#### 4–6. Deployment files (repo root)

| File | Role |
| --- | --- |
| `Dockerfile` | Multi-stage image: Go error-bus, TS modules, Rust guest auth → `python:3.12-slim` + supervisord |
| `supervisord.conf` | `flask` = gunicorn on `$PORT`; `error-bus` on `ERROR_BUS_PORT` (9090) |
| `.dockerignore` | Excludes `.git`, venvs, node_modules, large CSVs from `docker build` context |

#### 7. `.gitignore` (Configuration)

- **Role**: The "Filter."
- **Details**: Tracks what Render and the Docker build need (error-bus sources, `Cargo.lock`, `static/ts/` sources, most `Dataset/` CSVs) and ignores what must not be committed (`.env`, `.flask_secret`, `users.json`, `static/js/` build output, `node_modules/`, compiled `error-bus` binaries, `rust_auth/target/`, runtime `uploaded_*.csv` / `custom_train.csv`).

#### 5. `Dockerfile` / `supervisord.conf` / `.dockerignore` (Deployment)

- **Dockerfile**: Multi-stage build — Go error-bus, TypeScript modules, Rust guest auth, then `python:3.12-slim` final image. `CMD` is `supervisord`.
- **supervisord.conf**: `flask` program = gunicorn bound to `$PORT`; `error-bus` program = `/usr/local/bin/error-bus` on `ERROR_BUS_PORT` (9090). Logs go to stdout/stderr (`/dev/null` for supervisord itself).
- **.dockerignore**: Keeps `.git`, venvs, `node_modules`, large X-IIoTID CSV, and logs out of the build context.

---

### 📁 `static/` DIRECTORY: The Visuals & Resilience

#### 1. `sw.js` (Service Worker)

- **Role**: The Network Interceptor / theme-sync helper.
- **Logic**: Registered from `base.html`. Caches critical assets and receives `THEME_SET` / `THEME_GET` messages. An offline fallback lives at `offline.html`.

#### 2. `offline.html` (The Emergency Deck)

- **Role**: A branded landing page for network-status / reconnect UX when the service worker serves the offline path.

#### 3. `ts/` → `js/` (TypeScript build)

- **Role**: Source lives in `static/ts/` (`api.ts`, `notification.ts`, `types.ts`). Docker's `ts-builder` stage compiles to `static/js/`, which is **gitignored** — always build via Docker (or `npm run build` in `static/ts/`) rather than committing `js/`.

---

## DETAILED FUNCTION-BY-FUNCTION LOGIC

### In `Main.py`

#### 1. `load_ml_model()`

- **What it does**: This function runs when the website starts. It looks inside the `model/` folder for `trained_rf_model.pkl`.
- **Technical Logic**: It uses the `pickle` library to "unfreeze" the AI model. This is critical because training an AI can take minutes, but loading a saved one takes milliseconds.

#### 2. `PredictAction()`

- **What it does**: This is the "Brain" of the website. It handles the user's uploaded CSV file.
- **Technical Steps**:
  1. **Saves File**: It saves the user's upload to a temporary file.
  2. **Reads Data**: It uses `pandas` to read the CSV into a table.
  3. **Encodes Data**: It finds words like "TCP" and turns them into numbers (like `1`) using `LabelEncoder`.
  4. **Scales Data**: It uses `StandardScaler` to make sure all numbers are on the same scale.
  5. **Predicts**: It gives the cleaned data to the AI model and gets a list of attack guesses.
  6. **Insights**: It calls `get_genai_insight()` for every guess.

#### 3. `get_genai_insight(attack_type)`

- **What it does**: Simulates a Generative AI explanation by mapping each attack type to a hard-coded professional cybersecurity mitigation strategy.
- **Logic**: Uses a Python dictionary to look up the attack name and return the relevant advisory text.

#### 4. `UserLoginAction()`

- **What it does**: Handles multi-user authentication with password hashing protection.
- **Logic**:
  1. **Ultimate Bypass**: Checks if credentials match the hardcoded `admin`/`admin` master account first.
  2. **Database Check**: If not the master admin, it searches the `users.json` database.
  3. **Hash Verification**: Uses `check_password_hash()` to compare the submitted password against the stored PBKDF2 hash.
  4. **Session**: Creates an encrypted session and sets a 'MASTER' flag if the ultimate admin is used.

### In `train_model.py`

#### `run_training()`

- **What it does**: The full ML training pipeline in one function.
- **Technical Steps**:
  1. Loads `kdd_train.csv` (first 20,000 rows for speed).
  2. Label-encodes all non-numeric columns.
  3. Fills NaN values with 0.
  4. Fits a `StandardScaler`, then transforms all features.
  5. Splits data 80/20 into train/test sets.
  6. Trains a `RandomForestClassifier` with 100 trees.
  7. Saves the model, scaler, labels, and encoder as a single `.pkl` dictionary.

---

## THE STEP-BY-STEP DATA LIFECYCLE

Let's follow one single network packet (a "visit" to a website):

1. **CAPTURE**: The packet arrives. It has info like "Length: 500, Protocol: TCP, Service: HTTP."
2. **UPLOAD**: You upload a CSV file containing this info to our website.
3. **CLEANING**: The backend sees "TCP" and converts it to a number (like `1`) because AI only understands numbers.
4. **SCALING**: It shrinks large numbers (like `500000` bytes) down to small numbers so the AI doesn't get confused.
5. **PREDICTION**: The AI (Random Forest) looks at the numbers and says: "This looks 99% like a Neptune Attack!"
6. **GEN-AI INSIGHT**: The system looks up "Neptune" and finds: "Warning! This is a SYN flood attack. You should block this IP immediately."
7. **DISPLAY**: You see the result on your screen in a nice table.

---

## DATASET FEATURE DICTIONARY

The AI doesn't just "see" an attack; it looks at 41 different clues. Here is the exhaustive list explained with technical details and real-world analogies:

### 🌐 Basic Features (The ID Card)

- **[1] Duration**: Length (number of seconds) of the connection.
  - *Analogy*: How long a person stands at your front door.
  - *Technical*: High duration can indicate a slow-rate DoS or a long-running data exfiltration session.
- **[2] Protocol_type**: Type of protocol, e.g. tcp, udp, icmp.
  - *Analogy*: The language being spoken (English, Spanish, etc.).
  - *Technical*: Attacks often target specific protocols (e.g., Neptune targets TCP SYN).
- **[3] Service**: Network service on the destination, e.g., http, telnet, ftp, smtp.
  - *Analogy*: Which room in the house the visitor is trying to enter.
  - *Technical*: Hackers often target 'telnet' or 'ftp' because they are older and less secure.
- **[4] Flag**: Normal or error status of the connection (SF, S0, REJ, etc.).
  - *Analogy*: The "vibe" of the visitor (Friendly, Angry, or Silent).
  - *Technical*: 'S0' means a connection attempt was seen but no response was sent, common in SYN floods.

### 📦 Content Features (The Suitcase)

- **[5] Src_bytes**: Number of data bytes sent from source to destination.
  - *Analogy*: How many heavy bags the visitor is bringing into your house.
  - *Technical*: Massive spikes here could mean an "Upload" attack or a Buffer Overflow attempt.
- **[6] Dst_bytes**: Number of data bytes sent from destination to source.
  - *Analogy*: How many heavy bags the visitor is taking out of your house.
  - *Technical*: High values here often indicate "Data Exfiltration" (stealing your files).
- **[7] Land**: 1 if connection is from/to the same host/port; 0 otherwise.
  - *Analogy*: Someone trying to mail a letter to themselves.
  - *Technical*: This is a classic "Land Attack" used to crash old operating systems.
- **[8] Wrong_fragment**: Number of "wrong" fragments.
  - *Technical*: Used in "Teardrop" attacks to crash the network stack by sending overlapping fragments.
- **[9] Urgent**: Number of urgent packets.
  - *Technical*: High urgent counts are rare in normal traffic and often signal an exploit attempt.
- **[10] Hot**: Number of "hot" indicators (e.g., entering a system directory).
  - *Technical*: Indicators like accessing sensitive files or running unauthorized commands.
- **[11] Num_failed_logins**: Number of failed login attempts.
  - *Technical*: A clear sign of a "Brute Force" or "Password Guessing" attack.
- **[12] Logged_in**: 1 if successfully logged in; 0 otherwise.
  - *Technical*: Helps the AI distinguish between a successful hack and a failed attempt.
- **[13] Num_compromised**: Number of "compromised" conditions.
  - *Technical*: Measures if the attacker successfully changed files or settings.
- **[14] Root_shell**: 1 if root shell is obtained; 0 otherwise.
  - *Technical*: 'Root' is the highest level of permission. Obtaining it is a "Game Over" scenario for security.
- **[15] Su_attempted**: 1 if "su root" command attempted; 0 otherwise.
  - *Technical*: 'su' stands for 'substitute user', used to escalate privileges.
- **[16] Num_root**: Number of "root" accesses.
- **[17] Num_file_creations**: Number of file creation operations.
  - *Technical*: Hackers often create "Backdoors" (new files) to return later.
- **[18] Num_shells**: Number of shell prompts opened.
- **[19] Num_access_files**: Number of operations on access control files.
  - *Technical*: Attacks on files like `/etc/passwd` in Linux.
- **[20] Num_outbound_cmds**: Number of outbound commands in an ftp session.
- **[21] Is_hot_login**: 1 if the login belongs to the "hot" list; 0 otherwise.
- **[22] Is_guest_login**: 1 if the login is a "guest" login; 0 otherwise.

### 🕵️ Traffic Features (The Behavior)

- **[23] Count**: Number of connections to the same host in the past two seconds.
  - *Technical*: A classic signature of a Denial of Service (DoS) attack.
- **[24] Srv_count**: Number of connections to the same service in the past two seconds.
- **[25] Serror_rate**: Percentage of connections that have "SYN" errors.
  - *Technical*: High Serror rate indicates a SYN Flood attack.
- **[26] Srv_serror_rate**: Percentage of connections to the same service with "SYN" errors.
- **[27] Rerror_rate**: Percentage of connections that have "REJ" (Rejected) errors.
  - *Technical*: Often seen during Port Scanning.
- **[28] Srv_rerror_rate**: Percentage of connections to the same service with "REJ" errors.
- **[29] Same_srv_rate**: Percentage of connections to the same service.
- **[30] Diff_srv_rate**: Percentage of connections to different services.
  - *Technical*: Indicates a "Port Sweep" or "Service Scan."
- **[31] Srv_diff_host_rate**: Percentage of connections to different hosts for the same service.
- **[32] Dst_host_count**: Number of connections to the same destination host.
- **[33] Dst_host_srv_count**: Number of connections to the same destination host service.
- **[34] Dst_host_same_srv_rate**: Percentage of connections to the same service on the destination host.
- **[35] Dst_host_diff_srv_rate**: Percentage of connections to different services on the destination host.
- **[36] Dst_host_same_src_port_rate**: Percentage of connections to the same source port on the destination host.
- **[37] Dst_host_srv_diff_host_rate**: Percentage of connections to different hosts for the same service.
- **[38] Dst_host_serror_rate**: Percentage of connections to the destination host with "SYN" errors.
- **[39] Dst_host_srv_serror_rate**: Percentage of connections to the destination host service with "SYN" errors.
- **[40] Dst_host_rerror_rate**: Percentage of connections to the destination host with "REJ" errors.
- **[41] Dst_host_srv_rerror_rate**: Percentage of connections to the destination host service with "REJ" errors.

---

## ATTACK TAXONOMY

Our system is trained to recognize four major families of cyber attacks. Understanding these is vital for your Viva.

### 💥 Category 1: Denial of Service (DoS)

**Goal**: To make a computer or network resource unavailable to its intended users.

- **Neptune (SYN Flood)**:
  - *Logic*: The attacker sends many "SYN" (Synchronize) requests but never finishes the "Handshake." The server waits forever, uses up all its memory, and crashes.
  - *GenAI Insight*: "Enable SYN Cookies and reduce the connection timeout period."
- **Smurf**:
  - *Logic*: The attacker sends a ping (ICMP) to a "Broadcast" address using the victim's IP as the sender. Thousands of computers reply to the victim at once, crushing their internet.
- **Teardrop**:
  - *Logic*: Sends fragmented packets that overlap. When the victim's computer tries to reassemble them, it gets confused and "Panics" (Crashes).
- **Pod (Ping of Death)**:
  - *Logic*: Sends a ping packet larger than the maximum allowed size (65,535 bytes), causing the system to crash.

### 🕵️ Category 2: Probing (Reconnaissance)

**Goal**: To gather information about a network to find vulnerabilities for a future attack.

- **Satan**:
  - *Logic*: An automated tool that scans for common vulnerabilities like weak passwords or unpatched software.
- **IPsweep**:
  - *Logic*: Pings every IP address in a range to see which computers are "Alive" and connected.
- **Portsweep**:
  - *Logic*: Tries to connect to every port on one computer to see which "Doors" are open (like HTTP, SSH, FTP).
- **Nmap**:
  - *Logic*: The most famous probing tool. It can even guess which Operating System you are using just by looking at the packets.

### 🔓 Category 3: User to Root (U2R)

**Goal**: An attacker starts with a normal user account and tries to gain "Root" (Admin) privileges.

- **Buffer Overflow**:
  - *Logic*: Sending more data to a program than it can handle. The "Overflow" data spills into the computer's memory and can execute the attacker's malicious code.
- **Loadmodule**:
  - *Logic*: Exploiting a bug in how the operating system loads new hardware drivers (modules) to run unauthorized commands as root.
- **Perl**:
  - *Logic*: Exploiting bugs in the Perl programming language interpreter to gain elevated access.

### 📧 Category 4: Remote to Local (R2L)

**Goal**: An attacker who does not have an account on the machine tries to gain local access.

- **Guess_passwd**:
  - *Logic*: Using a dictionary of millions of common passwords (like "password123") to try and log in.
- **Warezclient / Warezmaster**:
  - *Logic*: Unauthorized uploading or downloading of illegal software/files through FTP.
- **Imap**:
  - *Logic*: Exploiting vulnerabilities in the email protocol (IMAP) to gain access to the server.
- **Spy**:
  - *Logic*: Monitoring user activity or stealing sensitive information like keystrokes.

---

## ALGORITHMIC COMPARISON: WHY WE CHOSE OUR MODELS

### 1. Random Forest (The "Leader")

- **Type**: Ensemble Learning (Bagging).
- **Mechanism**: It creates 100 different "Decision Trees." Each tree sees a random subset of the data. The final prediction is the "Majority Vote."
- **Why it's great**: It is extremely resistant to "Overfitting" and handles the 41 features of NSL-KDD perfectly without needing much tuning.

### 2. Deep Neural Networks (The "Expert")

- **Type**: Multi-Layer Perceptron (MLP).
- **Mechanism**: It has an Input Layer (41 neurons), multiple Hidden Layers, and an Output Layer. It uses "Backpropagation" to learn from its mistakes.
- **Why it's great**: It can find incredibly complex, non-linear patterns that a simple tree might miss.

### 3. Support Vector Machines (SVM)

- **Type**: Kernel-based Classifier.
- **Mechanism**: It tries to find the "Widest Street" (Hyperplane) that separates "Normal" data from "Attack" data.
- **Why it's great**: It works very well even if you don't have a lot of data, as long as the data is clean.

### 4. Hybrid Stacking (The "Genius")

- **Mechanism**: We combine the guesses of RF, MLP, and KNN. A final Meta-Learner looks at their guesses and makes the final call.
- **Result**: Usually achieves 1-2% higher accuracy than any single model alone.

---

## EXPLAINABLE AI XAI & SHAP INTERPRETATION

### 🧠 Generative AI Insight Engine

Traditionally, AI just gives a label: `0` or `1`. Our system uses a **Generative Logic Layer**.

- **How it works**: We mapped every attack type to a professional cybersecurity knowledge base. When the ML model detects "Neptune", the GenAI layer generates a human-readable explanation and a mitigation plan.
- **Academic Value**: This bridges the gap between "Black Box" AI and human-usable tools.

### 📊 Explainable AI (SHAP)

**SHAP (SHapley Additive exPlanations)** is used in our Jupyter Notebooks to explain the "Why."

- **Feature Importance**: It shows which of the 41 features was most important for a specific prediction.
- **Trust**: If a system says "Attack" because the `duration` was high, a human can verify if that makes sense. This makes the system trustworthy.

---

## GENERATIVE AI INSIGHT ENGINE

See the Algorithmic Comparison and XAI sections above for full details on how the GenAI insight layer works.

---

## VIVA PREPARATION TOP 100 QUESTIONS & ANSWERS

*Below are the most critical questions you might face, categorized for easy learning.*

### 🛠️ Category A: Implementation & Code

1. **Q: What is the role of `Main.py`?**
   - *A*: It is the heart of the project. It handles routing (URL paths), file uploads, model prediction, and rendering HTML templates via Flask.
2. **Q: Why do we use `Jinja2` templates?**
   - *A*: It allows us to use logic (like `if` and `for` loops) inside HTML. It also enables "Template Inheritance" using `base.html` so we don't rewrite the Navbar on every page.
3. **Q: What does `StandardScaler` do exactly?**
   - *A*: It calculates the mean and standard deviation of each feature. It then subtracts the mean and divides by the deviation. This ensures all features are on the same scale (usually -3 to +3).
4. **Q: How do you handle new attacks not in the training data?**
   - *A*: The model will likely classify them as the closest known attack type because their behavior (e.g., high count, wrong fragments) will differ significantly from "Normal" traffic.
5. **Q: What is the significance of `requirements.txt`?**
   - *A*: It lists every external library (Flask, Scikit-learn, Pandas, gunicorn, requests) and its version. Runtime deps live in `CyberAttackPrediction/requirements.txt` (used by Docker/Render); notebook-only packages (Jupyter, SHAP, matplotlib) live in `requirements-dev.txt`. Recreate the environment with `pip install -r CyberAttackPrediction/requirements.txt`.
6. **Q: What is `pickle` used for in this project?**
   - *A*: `pickle` serializes the trained model to a `.pkl` file so we don't retrain it every time the server restarts. The `load_ml_model()` function deserializes it back into memory.
7. **Q: Why do we load the model on startup instead of loading it per request?**
   - *A*: Loading a model takes time. Loading it once at startup and keeping it in memory means each prediction request is instant instead of waiting seconds.
8. **Q: Why do we use hashed passwords instead of environment variables now?**
   - *A*: Storing passwords in `.env` is better than hardcoding, but they are still plain text. By using `werkzeug.security` hashes in `users.json`, we ensure that even if a hacker steals the database, they cannot see the actual passwords.
9. **Q: What is the purpose of the `saved_creds.json` file?**
   - *A*: It stores a hashed 'Quick Access' token. When you click 'Quick Access' on the login page, the app verifies this token against your local machine to log you in instantly without typing.
10. **Q: What is the purpose of the `secrets.json` file?**
    - *A*: It stores the admin credentials locally for the "Remember Me" feature. When the user returns, the app reads this file to auto-authenticate without re-entering the password.

### 📊 Category B: Data & Statistics

- **Q: What is a "False Positive" (Type I Error)?**
  - *A*: When the AI flags a "Normal" user as an "Attacker." This is bad because it blocks innocent people.
- **Q: What is a "False Negative" (Type II Error)?**
  - *A*: When a "Hacker" gets through and the AI thinks they are "Normal." This is the most dangerous error in cybersecurity.
- **Q: Which is more important: Precision or Recall?**
  - *A*: In cybersecurity, **Recall** is usually more important. We would rather have a few False Positives (block an innocent user) than a single False Negative (let a hacker in).
- **Q: What is "Data Imbalance" and how do you fix it?**
  - *A*: It's when you have 90% "Normal" data and only 10% "Attack" data. We fix it using SMOTE (Synthetic Minority Over-sampling Technique) to create synthetic attack data.
- **Q: Why do we split data into 80% training and 20% testing?**
  - *A*: The 80% trains the model. The 20% is data the model has never seen, so we get a real-world measure of accuracy.
- **Q: What is Cross-Validation?**
  - *A*: Instead of one 80/20 split, we split the data into 5 parts (folds). The model trains on 4 and tests on 1, cycling through all 5. The final accuracy is the average.
- **Q: What is the F1-Score and when do you use it?**
  - *A*: F1 = 2 × (Precision × Recall) / (Precision + Recall). Use it when you need to balance both metrics, especially with imbalanced data.
- **Q: Why do we use `fillna(0)` in the preprocessing?**
  - *A*: Machine learning models cannot process `NaN` (missing) values. Filling with 0 ensures all inputs are valid numbers.
- **Q: What is a Confusion Matrix?**
  - *A*: A 4-cell table showing True Positives, False Positives, True Negatives, and False Negatives. It gives a complete picture of model performance beyond just accuracy.
- **Q: What is ROC-AUC?**
  - *A*: ROC (Receiver Operating Characteristic) is a curve. AUC (Area Under the Curve) summarizes it as a single score. An AUC of 1.0 is perfect; 0.5 is random guessing.

### 🤖 Category C: Machine Learning Algorithms

- **Q: Why Random Forest and not just a single Decision Tree?**
  - *A*: A single tree memorizes the training data (overfitting). Random Forest averages 100 trees, each trained on random subsets. This makes it robust and generalizable.
- **Q: What is "Bagging"?**
  - *A*: Bootstrap Aggregating. Each tree trains on a random sample (with replacement) from the data. Predictions are then averaged. This reduces variance.
- **Q: What is "Boosting" and how is XGBoost different from Random Forest?**
  - *A*: Boosting trains trees sequentially — each tree corrects the errors of the previous one. XGBoost is an optimized boosting algorithm. Random Forest trains all trees in parallel.
- **Q: What is a "Hyperparameter" in Random Forest?**
  - *A*: Settings like `n_estimators` (number of trees), `max_depth` (depth of each tree), and `random_state` (for reproducibility). These are set before training.
- **Q: How does `KNeighborsClassifier` predict?**
  - *A*: It finds the K nearest data points to the new input (using Euclidean distance). The majority class among those K neighbors becomes the prediction.
- **Q: What is the role of `MLPClassifier` in the stacking model?**
  - *A*: It's a neural network base estimator. Its internal representation can capture non-linear patterns that Random Forest might miss, making the stack more powerful.
- **Q: What is the Meta-Learner in `StackingClassifier`?**
  - *A*: After all base models (RF, MLP, KNN) make their predictions, those predictions become the input features for the Meta-Learner. It learns which models to trust more.
- **Q: Why do we set `cv=3` in StackingClassifier?**
  - *A*: `cv=3` means the base estimators are trained using 3-fold cross-validation to generate out-of-fold predictions the meta-learner learns from. It prevents leakage.
- **Q: What is "early_stopping" in MLP?**
  - *A*: The MLP reserves a small validation set. If validation accuracy doesn't improve for several iterations, training stops automatically. This prevents wasted time and overfitting.
- **Q: What is `n_jobs=-1` doing in `RandomForestClassifier`?**
  - *A*: It tells scikit-learn to use all available CPU cores in parallel for training. This dramatically speeds up fitting time on multi-core machines.

### ![CyberShield Logo](../CyberAttackPrediction/static/images/logo_with_bg.svg) Category D: Cybersecurity Concepts

- **Q: What is the NSL-KDD dataset and why is it better than KDD'99?**
  - *A*: NSL-KDD removes redundant records from KDD'99 so that each row is unique. This ensures the model doesn't "learn" by simply counting duplicates.
- **Q: What is a SYN Flood attack?**
  - *A*: The attacker sends thousands of TCP SYN packets but never completes the 3-way handshake. The server allocates memory for each half-open connection and eventually runs out.
- **Q: What is the difference between DoS and DDoS?**
  - *A*: DoS (Denial of Service) comes from one machine. DDoS (Distributed DoS) comes from thousands of compromised machines (a botnet), making it much harder to block.
- **Q: What is a "Probe" attack in NSL-KDD?**
  - *A*: Reconnaissance — the attacker scans ports or IPs to find open vulnerabilities before launching the real attack.
- **Q: What is "U2R" and why is it dangerous?**
  - *A*: User-to-Root. An attacker starts with a regular user account but exploits vulnerabilities to gain root (administrator) access — a "Game Over" scenario.
- **Q: What is a Buffer Overflow?**
  - *A*: A program has a fixed-size memory buffer. If you send more data than it can hold, it overflows into adjacent memory, allowing an attacker to execute malicious code.
- **Q: What is an IDS vs. IPS?**
  - *A*: IDS (Intrusion Detection System) only detects and alerts. IPS (Intrusion Prevention System) actively blocks suspicious traffic. Our project is an IDS-like system.
- **Q: What is the CIA Triad?**
  - *A*: Confidentiality (data is private), Integrity (data is not tampered with), and Availability (data is accessible when needed).
- **Q: What is "Port Scanning"?**
  - *A*: Systematically checking all network ports on a host to discover which services are running and potentially exploitable.
- **Q: What is a Botnet?**
  - *A*: A network of internet-connected devices infected with malware and remotely controlled by an attacker to perform coordinated tasks like DDoS attacks.

### 🌐 Category E: Networking Concepts

- **Q: What is the TCP 3-Way Handshake?**
  - *A*: Client sends SYN → Server replies SYN-ACK → Client replies ACK. Neptune attacks exploit this by never sending the final ACK.
- **Q: What is the difference between TCP and UDP?**
  - *A*: TCP is reliable and connection-based (checks each packet was received). UDP is fast but connectionless (fires and forgets). Attacks may target either.
- **Q: What is an IP Address?**
  - *A*: A unique identifier for a device on a network. IPv4 addresses look like `192.168.1.1`.
- **Q: What is a Port Number?**
  - *A*: A number (0-65535) that identifies a specific process/service. HTTP uses port 80, HTTPS uses 443, SSH uses 22.
- **Q: Why does the dataset have a "Flag" column?**
  - *A*: The flag represents the connection state. 'SF' means normal established. 'S0' means a connection was initiated but not completed — a key DDoS indicator.

### 🐍 Category F: Python & Flask

- **Q: What is `wants_json()` used for in `Main.py`?**
  - *A*: Decides whether a response should be a JSON envelope or an HTML redirect. True when the client sends `Accept: application/json` (or is on an exempt AJAX path such as `/UserLoginAction`, `/SignupAction`, `/api/heartbeat`).
- **Q: What happens on a 25MB+ upload?**
  - *A*: Flask raises `RequestEntityTooLarge`; `handle_413` returns JSON `{ok:false, code:"UPLOAD_TOO_LARGE"}` for API clients or a friendly HTML page for browsers. Training files are also capped at 5000 rows.
- **Q: What is the role of `os.path.dirname(os.path.abspath(__file__))`?**
  - *A*: Gets the absolute path of the directory containing the running script so paths like Dataset/ and model/ work regardless of where the code is run from.
- **Q: What is `jsonify()` in Flask?**
  - *A*: Converts a Python dictionary to a JSON HTTP response. Used for AJAX calls from the frontend (like the training progress updates).
- **Q: What does `session.clear()` do?**
  - *A*: Removes all data from the user's session cookie, effectively logging them out.
- **Q: What is `@app.route` in Flask?**
  - *A*: A Python decorator that maps a URL path to a Python function. `@app.route('/Predict')` means visiting `/Predict` calls the `predictView()` function.
- **Q: Why do we check `if 'user' not in session` at the start of protected routes?**
  - *A*: To prevent unauthorized access. If a user visits `/Predict` without logging in, they are redirected to the login page.
- **Q: What is the purpose of the `Timer` class in `Main.py`?**
  - *A*: `Timer(1.5, open_browser).start()` opens the web browser 1.5 seconds after Flask starts **in local `python Main.py` / launcher mode only**. It never runs under gunicorn/supervisord on Render (that code is inside `if __name__ == '__main__':`).
- **Q: What is `load_dotenv()` for?**
  - *A*: Reads the `.env` file and loads its key-value pairs as environment variables, making sensitive values available via `os.getenv()` without hardcoding them.
- **Q: What is `request.form.get('t1')` doing?**
  - *A*: Retrieves the value of a form field named `t1` from an HTTP POST request. This is how the username is extracted from the login form.
- **Q: What is the difference between `request.form` and `request.files`?**
  - *A*: `request.form` contains text field values. `request.files` contains file uploads. The CSV file upload is accessed via `request.files['t1']`.
- **Q: What is `render_template` and how does it work?**
  - *A*: Takes an HTML template filename, injects Python variables into it via Jinja2, and returns the full HTML page as an HTTP response.

### 📊 Category G: Data Preprocessing

- **Q: What is Label Encoding?**
  - *A*: Converting categorical text values like "TCP", "UDP", "ICMP" into integer numbers like 0, 1, 2. Required because ML algorithms only process numbers.
- **Q: What is the difference between Label Encoding and One-Hot Encoding?**
  - *A*: Label Encoding assigns a single integer. One-Hot Encoding creates separate binary columns. Label Encoding is simpler; One-Hot Encoding avoids artificial ordering.
- **Q: What is the problem with using a `LabelEncoder` on test data?**
  - *A*: If the test data has a category not seen during training, the encoder will raise an error. Our code handles this by assigning `-1` for unseen labels.
- **Q: Why do we fit the `StandardScaler` only on training data?**
  - *A*: Fitting on test data causes "data leakage" — the scaler would use future information. We transform test data using the training data's mean and standard deviation.
- **Q: What is `nrows=20000` in the training script and why?**
  - *A*: Limits the loaded data to 20,000 rows — a deliberate trade-off between training time and accuracy, making the training feature responsive for demos.

### 🔍 Category H: SHAP & Explainable AI

- **Q: What does SHAP stand for?**
  - *A*: SHapley Additive exPlanations.
- **Q: What is a SHAP Summary Plot?**
  - *A*: A dot plot where each dot represents one data point. The X-axis shows the SHAP value (positive = pushes toward "Attack"). Color shows if the feature value was high (red) or low (blue).
- **Q: What does it mean if `src_bytes` has a high positive SHAP value?**
  - *A*: A high source byte count strongly pushed the model's prediction toward "Attack" for that particular data row.
- **Q: Why is Explainable AI important in cybersecurity?**
  - *A*: Security analysts need to trust and audit AI decisions. SHAP lets them verify the reason for a classification instead of blindly trusting a black-box output.
- **Q: What is the difference between a global and local SHAP explanation?**
  - *A*: Global SHAP (Summary Plot) shows feature importance across all predictions. Local SHAP (Force Plot) explains why the model made one specific prediction.
- **Q: What is a SHAP Force Plot?**
  - *A*: A visualization showing which features pushed a single prediction higher (toward "Attack") or lower (toward "Normal") from the base expected value.
- **Q: How does SHAP calculate feature importance differently from Random Forest's built-in feature importance?**
  - *A*: RF's built-in importance measures how much a feature reduces impurity across trees. SHAP measures the actual contribution of each feature to each individual prediction.
- **Q: What is `shap.TreeExplainer`?**
  - *A*: A fast SHAP explainer optimized for tree-based models. It calculates exact SHAP values using the tree structure, not approximations.
- **Q: What is the "background dataset" in SHAP?**
  - *A*: The baseline data SHAP uses to calculate expected model output. SHAP values measure the deviation from this baseline caused by each feature.
- **Q: What does SHAP indexing `[:, :, 0]` fix?**
  - *A*: In newer SHAP versions with multi-class output, the returned array has 3 dimensions. `[:, :, 0]` selects values for the first class, making it compatible with the Summary Plot.

### 🔧 Category I: Project Design Decisions

- **Q: Why did you choose Flask over Django?**
  - *A*: Flask is a micro-framework — lightweight and flexible. For a focused ML prediction app, Flask gives us everything we need without unnecessary complexity.
- **Q: Why save the model as `.pkl` instead of retraining on every request?**
  - *A*: Training takes seconds to minutes. Loading a `.pkl` takes milliseconds. A web app must respond instantly — retraining on every request would make it unusable.
- **Q: Why use `StackingClassifier` for the extension notebook?**
  - *A*: A single model has limitations. Stacking combines RF, MLP, and KNN strengths to overcome each model's individual weaknesses, generally achieving higher accuracy.
- **Q: Why is the virtual environment (.venv) important for this project?**
  - *A*: It isolates project dependencies. Without it, library version conflicts between projects can break one or both. It also makes the project reproducible on any machine.
- **Q: Why do we use `random_state=42` in model definitions?**
  - *A*: Setting a fixed seed makes results reproducible. Without it, the model gets slightly different results each run, making debugging and comparison harder.
- **Q: What is a Python decorator and give an example from the project?**
  - *A*: A decorator modifies a function's behavior without changing its code. `@app.route('/Predict')` registers the function as the handler for the `/Predict` URL.
- **Q: Why do we store `labels_list = np.unique(dataset['labels'])` before encoding?**
  - *A*: After encoding, labels become integers. We save the original class names (like "normal", "neptune") so the result page can display human-readable attack names.
- **Q: What is `Glassmorphism` in the UI design?**
  - *A*: A UI design trend using semi-transparent panels, frosted glass blur (`backdrop-filter: blur()`), and subtle borders to create a modern, depth-layered aesthetic.
- **Q: Why do we use environment variables for the admin password?**
  - *A*: Hardcoding credentials in Python files risks exposing them on GitHub. Environment variables are loaded from `.env` at runtime, keeping secrets outside the codebase.
- **Q: What is the purpose of the `secrets.json` file?**
  - *A*: It stores the admin credentials locally for the "Remember Me" feature. When the user returns, the app reads this file to auto-authenticate without re-entering the password.

### 🎓 Category J: Academic & Theoretical Concepts

- **Q: What is the difference between Artificial Intelligence and Machine Learning?**
  - *A*: AI is the broad concept of making machines intelligent. ML is a subset of AI where machines learn from data automatically without being explicitly programmed.
- **Q: What is Supervised vs. Unsupervised Learning?**
  - *A*: Supervised ML uses labeled data (we know the answer). Unsupervised ML finds hidden patterns without labels. Our project uses Supervised Learning.
- **Q: What is Overfitting and how do Random Forests prevent it?**
  - *A*: Overfitting is when a model memorizes training data instead of learning patterns. RF prevents it by averaging 100 diverse trees trained on random data subsets.
- **Q: What is Regularization?**
  - *A*: A technique to prevent overfitting by adding a "penalty" to complex models. L1 (Lasso) can zero out less important features. L2 (Ridge) limits the size of all weights.
- **Q: What is "Feature Engineering"?**
  - *A*: Creating new input features from existing data to improve model performance. For example, calculating the ratio of `src_bytes` to `dst_bytes` as a new feature.
- **Q: What is "Transfer Learning"?**
  - *A*: Taking a model trained on one task and reusing it for a different but related task. Could be a future enhancement using a model pre-trained on similar network traffic.
- **Q: What is the Bias-Variance Tradeoff?**
  - *A*: High Bias (Underfitting) = model is too simple. High Variance (Overfitting) = model is too complex. The goal is to find the sweet spot between both.
- **Q: Why does this project use 4 datasets instead of 1?**
  - *A*: Each dataset captures different types of traffic (IoT, web, cloud). Using all 4 makes the model robust across diverse network environments.
- **Q: What is the difference between classification and regression?**
  - *A*: Classification predicts a discrete category (Normal or Attack). Regression predicts a continuous number (like the probability of an attack on a 0-100 scale).
- **Q: What are Epochs in neural network training?**
  - *A*: One full pass through the entire training dataset. The MLP trains for up to 100 epochs, stopped early by `early_stopping` if performance plateaus.

### 🚀 Category K: Project Improvements & Future Scope

- **Q: How could you improve the model's accuracy further?**
  - *A*: Apply GridSearchCV for hyperparameter tuning, use SMOTE to balance class distribution, add feature selection to remove noisy features, and train on larger datasets.
- **Q: What would a real-world deployment of this system look like?**
  - *A*: Already deployed as a Docker image on **Render** (Free Tier) with gunicorn under supervisord and a Go error-bus sidecar. Next steps: attach live traffic (Wireshark/Zeek), real-time alerting, and horizontal scale on a paid plan.
- **Q: How would you add a real Generative AI to the insights?**
  - *A*: Integrate the Google Gemini API or GPT-4 API. When an attack is detected, pass the type and features to the LLM asking it to explain and suggest 3 mitigations.
- **Q: What is the limitation of training on only 20,000 rows?**
  - *A*: The model is exposed to only a fraction of possible traffic patterns. Training on the full dataset would improve recall for rare attack types.
- **Q: How could you make the web app more secure? (Already Implemented!)**
  - *A*: We have already implemented several advanced layers: **Password Hashing** (PBKDF2), **Multi-user support** via a protected JSON database, and **Session flags** for administrative privileges. Future scope includes CSRF protection and rate-limiting.
- **Q: What is "model drift" and how would you detect it?**
  - *A*: Over time, network traffic patterns change and model accuracy drops. Detect it by monitoring prediction confidence scores and scheduling periodic retraining on fresh data.
- **Q: How could you scale this to handle millions of packets per second?**
  - *A*: Replace Flask with an async framework (FastAPI), use a message queue (Kafka) to buffer data, and deploy multiple prediction workers behind a load balancer.
- **Q: What ethical concerns exist in automated cyber attack detection?**
  - *A*: False positives can block legitimate users. Privacy concerns arise if traffic is logged indefinitely. XAI is essential so humans can audit AI classifications.
- **Q: How would you add support for real-time streaming predictions?**
  - *A*: Use WebSockets in Flask (via Flask-SocketIO) to push predictions to the browser in real time instead of waiting for a full CSV upload.
- **Q: What is the academic contribution of this project?**
  - *A*: It demonstrates a full ML pipeline — from raw network data to human-readable AI-generated mitigations — integrating Random Forest with Explainable AI (SHAP) and a simulated GenAI layer.

### ![CyberShield Logo](../CyberAttackPrediction/static/images/logo_with_bg.svg) Category L: Advanced Security (Stable-2026)

- **Q: What is the "Neural Firewall" in your project?**
  - *A*: It is a security logic that prevents "Directory Traversal." It ensures that a user can only view files inside the project folder and cannot use `../` to access sensitive system files on the host computer.
- **Q: How do you protect against "Session Hijacking"?**
  - *A*: We use **HMAC-SHA256 Cryptographic Tokens**. Every login session is uniquely signed. If someone tries to steal and modify the session cookie, the signature won't match, and the system logs them out immediately.
- **Q: Why do you have a `.env` file?**
  - *A*: It's an industry-best practice for "Secret Management." It keeps sensitive info like the Flask Secret Key and Admin credentials out of the main code, so they don't get accidentally uploaded to GitHub.
- **Q: What is the benefit of using "Jinja2 Macros" for the UI?**
  - *A*: It makes the UI "Decoupled" and "Modular." By defining elements like the "Attack Badge" in a macro, we ensure that the logic for displaying data is safe and consistent across all pages.
- **Q: What hashing algorithm is used for the database?**
  - *A*: We use `PBKDF2-HMAC-SHA256`. It is much slower and harder for hackers to crack compared to traditional MD5 or SHA1, making it highly secure for student projects.

### CATEGORY L: JUPYTER & NOTEBOOK ENVIRONMENTS

- **Q: What is the primary difference between a `.py` script and a `.ipynb` notebook?**
  - *A*: A `.py` file is a plain text file executed linearly. A `.ipynb` (JSON format) allows "literate programming," mixing code, rich text (Markdown), and inline visualizations. It is stateful, meaning you can run cells out of order.
- **Q: What is a "Kernel" in the context of Jupyter?**
  - *A*: The Kernel is the execution engine (usually Python) that runs the code in the background. If you restart the kernel, all variables and memory are cleared, providing a "clean slate."
- **Q: What are "Magic Commands" like `%matplotlib inline` or `%%time`?**
  - *A*: Line magics (`%`) and Cell magics (`%%`) are special Jupyter-specific syntax. They allow you to time executions, configure plots, or interact with the operating system without standard Python code.
- **Q: Why are "Checkpoints" important?**
  - *A*: Jupyter saves periodic checkpoints to prevent data loss if the browser or system crashes, allowing you to revert to a previous autosaved state.

### CATEGORY M: ARTIFICIAL INTELLIGENCE & GENERATIVE MODELS

- **Q: What is the difference between "Narrow AI" (ANI) and "General AI" (AGI)?**
  - *A*: Narrow AI (like this project) is designed for a specific task (attack prediction). General AI (AGI) would have the human-like ability to understand and learn any intellectual task a human can.
- **Q: What is "Prompt Engineering" in the context of LLMs like Gemini or GPT-4?**
  - *A*: It is the practice of crafting specific, high-quality text inputs to guide a Generative AI model toward an accurate or desired output style (e.g., "Summarize this network log as a security expert").
- **Q: What are "Hallucinations" in Generative AI?**
  - *A*: This is when a model generates text that sounds confident but is factually incorrect or nonsensical, often due to patterns in training data that don't match reality.
- **Q: How does RAG (Retrieval-Augmented Generation) differ from Fine-Tuning?**
  - *A*: Fine-tuning updates the model's actual weights using new data. RAG provides the model with external documents (at inference time) as context, allowing it to "read" new information without retraining.

### CATEGORY N: DEEP LEARNING & NEURAL NETWORKS

- **Q: Why is it called "Deep" Learning?**
  - *A*: "Deep" refers to the number of hidden layers in a Neural Network. While a shallow network has 1–2 layers, a Deep Network may have hundreds.
- **Q: What is the role of an "Activation Function" (like ReLU or Sigmoid)?**
  - *A*: It introduces "non-linearity" into the network. Without it, the network would just be a giant linear equation, incapable of learning complex patterns like images or non-linear security threats.
- **Q: What is the "Vanishing Gradient" problem?**
  - *A*: During training (Backpropagation), gradients get smaller as they move toward the early layers. If they "vanish" to zero, the network stops learning. ReLU helps solve this compared to older Sigmoid functions.
- **Q: What is the difference between Weights and Biases?**
  - *A*: Weights determine the *strength* of a connection between neurons. Biases allow the activation function to be shifted (offset) to better fit the data. `Output = (Weights * Input) + Bias`.

### CATEGORY O: PYTHON FOR AI ENGINEERING

- **Q: What is the "Global Interpreter Lock" (GIL)?**
  - *A*: A mutex that allows only one thread to execute Python bytecode at a time. This simplifies memory management but can limit true multi-core parallel processing in CPU-bound tasks.
- **Q: What is a "List Comprehension" and why use it?**
  - *A*: A concise way to create lists (`[x for x in data if x > 0]`). It is often faster and more readable than standard `for` loops.
- **Q: Difference between `is` and `==`?**
  - *A*: `==` checks for **equality** (do they have the same value?). `is` checks for **identity** (are they the exact same object in memory?).
- **Q: What is the purpose of `pip` vs `conda`?**
  - *A*: `pip` is the standard Python package manager. `conda` is a cross-language environment and package manager (common in Data Science) that handles binary dependencies more robustly for libraries like NumPy.

---

## TROUBLESHOOTING ENCYCLOPEDIA

### ❌ Error: `ImportError: cannot import name 'joblib' from 'sklearn.externals'`

- **Cause**: In newer versions of Scikit-learn (v0.23+), `joblib` was removed from `sklearn.externals`.
- **Solution**: Install it separately: `pip install joblib` and change all imports to `import joblib` directly.

---

### ❌ Error: `ValueError: Found input variables with inconsistent numbers of samples`

- **Cause**: Your `X` (features) and `Y` (labels) arrays have different row counts after preprocessing.
- **Solution**: Check your data loading code. This usually happens if a row was dropped from `X` during `dropna()` but the corresponding label in `Y` was not dropped. Always use `df.dropna()` on the full dataframe *before* splitting.

---

### ❌ Error: `FileNotFoundError: Dataset/kdd_train.csv`

- **Cause**: The script is being run from a different working directory than expected.
- **Solution**: The code uses `os.path.dirname(os.path.abspath(__file__))` to resolve paths automatically. Ensure the `Dataset` folder sits directly inside `CyberAttackPrediction/`. Do not move or rename it.

---

### ❌ Error: `Internal Server Error (500)` on File Upload

- **Cause**: The uploaded CSV is missing required columns or has wrong headers.
- **Solution**: Ensure the CSV has exactly 41 columns matching the NSL-KDD schema (e.g., `duration`, `protocol_type`, `src_bytes`, etc.). Add header validation in `PredictAction()` using `if not all(col in df.columns for col in expected_cols)`.

---

### ❌ Error: `NameError: name 'rf' is not defined` (in Jupyter Notebook)

- **Cause**: A cell was executed out of order — the model definition cell was skipped.
- **Solution**: Use **Kernel → Restart & Run All** to guarantee all cells execute in order from top to bottom.

---

### ❌ Error: Model loads but `labels` is `None`

- **Cause**: The `.pkl` file was saved by an older version of `train_model.py` that did not include the `labels` key in the saved dictionary.
- **Solution**: Delete `model/trained_rf_model.pkl` and retrain using the latest `train_model.py`. The model saves as a dictionary: `{'model': rf, 'scaler': scaler, 'labels': labels_list}`.

---

### ❌ Error: SHAP `IndexError` or `ValueError` on Summary Plot

- **Cause**: SHAP v0.40+ returns a 3D array `(samples, features, classes)` for multi-class models.
- **Solution**: Slice it before plotting: `shap.summary_plot(shap_values[:, :, 0], X_test_sample)`. The `[:, :, 0]` selects SHAP values for class index 0.

---

### ❌ Error: Flask says `OSError: [Errno 98] Address already in use` on port 2026

- **Cause**: A previous Flask process is still running in the background.
- **Solution (Windows)**: Run `taskkill /f /im python.exe` in a terminal. Alternatively, change the port at the bottom of `Main.py`: `app.run(port=2027)`.
- **On Render/Docker**: The public port is whatever the platform injects as `PORT` (do not hardcode 2026 — that is the local dev port only). The error-bus sidecar uses `ERROR_BUS_PORT` (default 9090).

---

### ❌ Warning: VS Code keeps asking to select Python Interpreter

- **Cause**: Multiple `.vscode/settings.json` files exist in nested project subdirectories.
- **Solution**: Keep only the root-level `.vscode/settings.json`. Delete any inner `.vscode` folders. Set `"python.defaultInterpreterPath": ".venv/Scripts/python.exe"` in the root settings.

---

### ❌ Error: `pip install` fails with permission errors

- **Cause**: Running `pip install` without the virtual environment activated — installing globally instead.
- **Solution**: Activate the virtual environment first: `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Linux/Mac), then retry `pip install -r requirements.txt`.

---

### ❌ Error: `ModuleNotFoundError: No module named 'flask'` despite installing

- **Cause**: Flask was installed in the system Python, not the active virtual environment.
- **Solution**: Confirm the correct Python is active: `which python` (Linux) or `where python` (Windows). It should point to `.venv/Scripts/python.exe`. Reinstall inside the venv: `pip install flask`.

---

### ❌ Error: `KeyError: 'labels'` when loading the model in `Main.py`

- **Cause**: The model was saved using `pickle.dump(rf, f)` (bare model) instead of the dictionary format.
- **Solution**: Retrain using the updated `train_model.py` which saves the full dictionary: `pickle.dump({'model': rf, 'scaler': scaler, 'labels': labels_list}, f)`.

---

### ❌ Error: `ValueError: X has X features, but StandardScaler is expecting Y features`

- **Cause**: The uploaded prediction CSV has a different number of columns than the training data — either missing columns or extra columns present.
- **Solution**: Ensure the prediction CSV has the exact same 41 features as the training set. Drop any extra columns before uploading. The `rename_columns()` function in `Main.py` handles name normalization, but extra or missing columns will still fail.

---

### ❌ Error: Prediction always returns `"normal"` regardless of input

- **Cause**: The model was trained on a heavily imbalanced dataset where 80%+ of rows are "normal", causing it to always predict the majority class.
- **Solution**: Retrain the model with balanced data. Apply SMOTE (`from imblearn.over_sampling import SMOTE`) or use `class_weight='balanced'` in `RandomForestClassifier` to penalize majority class predictions.

---

### ❌ Error: SHAP plot shows wrong feature names (displays indices like `0`, `1`, `2`)

- **Cause**: The feature names were lost during `StandardScaler` transformation — the scaler outputs a NumPy array without column names.
- **Solution**: Capture feature names before scaling: `feature_names = X_train.columns.tolist()`, then pass them explicitly: `shap.summary_plot(shap_values, X_test_sample, feature_names=feature_names)`.

---

### ❌ Error: Training the model in the web app freezes the browser tab

- **Cause**: `train_model.py` is a blocking synchronous call. Flask's default server is single-threaded, so it blocks all requests while training runs.
- **Solution**: The project uses a background `threading.Thread` to run training asynchronously. The `/Train` route launches training in a thread; the frontend polls progress (AJAX against the training status/log endpoints — not a separate `/TrainStatus` route) so the UI stays responsive.

---

### ❌ Error: `Jinja2 TemplateNotFound` for a specific HTML page

- **Cause**: The HTML file is either not inside the `templates/` folder or the filename casing is wrong (Windows is case-insensitive, Linux is not).
- **Solution**: Verify the file exists at `CyberAttackPrediction/templates/filename.html`. Ensure `render_template('filename.html')` matches the exact filename including case.

---

### ❌ Error: Login succeeds but user is immediately redirected back to login

- **Cause**: `session['user']` is being set but not persisting across redirects — usually because `app.secret_key` is unstable or missing.
- **Solution**: `Main.py` uses `FLASK_SECRET_KEY` from the environment when set; otherwise it reads/writes a gitignored `.flask_secret` file next to `Main.py`. Ensure one of those is stable across worker recycles (gunicorn `--max-requests` restarts workers; a random key per boot would invalidate sessions). On Render, set `FLASK_SECRET_KEY` as a service env var because the disk is ephemeral.

---

### ❌ Error: `.env` file values not loading (`os.getenv()` returns `None`)

- **Cause**: `load_dotenv()` was not called, or the `.env` file is in the wrong directory.
- **Solution**: Call `load_dotenv()` at the very top of `Main.py` (before any `os.getenv()` calls). Place the `.env` file in the same directory as `Main.py`. Verify there are no extra spaces around `=` in `.env` entries: `KEY=value` ✅ not `KEY = value` ❌.

---

### ❌ Error: `MemoryError` or system lag during Jupyter Notebook training

- **Cause**: Training with too many estimators or full dataset without memory constraints.
- **Solution**: Reduce `n_estimators` to 50 or 100. Use `nrows=20000` in `pd.read_csv()` to limit data. Ensure no other memory-heavy processes are running simultaneously.

---

### ❌ Error: Stacking model training takes 3–5 minutes (too slow)

- **Cause**: Default `MLPClassifier` trains for 200 iterations with large hidden layers, and `StackingClassifier` with `cv=5` multiplies training time by 5.
- **Solution**: Set `max_iter=100`, `early_stopping=True`, and `cv=3`. Add `n_jobs=-1` to base estimators that support it. This reduces training time to under 30 seconds.

---

### ❌ Error: `UnicodeDecodeError` when reading the CSV dataset

- **Cause**: The CSV file was saved with a non-UTF-8 encoding (e.g., Latin-1 or Windows-1252).
- **Solution**: Specify encoding explicitly: `pd.read_csv('file.csv', encoding='latin-1')` or `encoding='cp1252'`. Alternatively, open the file in Notepad++ and re-save it as UTF-8.

---

### ❌ Error: Browser opens but Flask page shows `This site can't be reached`

- **Cause**: The `Timer(1.5, open_browser).start()` fires before Flask has fully started listening on the port.
- **Solution**: Increase the delay: `Timer(3.0, open_browser).start()`. Alternatively, manually open `http://127.0.0.1:2026` after running the script.

---

### ❌ Error: CSV upload returns predictions but result table is empty

- **Cause**: The `labels_list` in the loaded model does not match the encoded integer outputs, causing the decoding step (`labels_list[pred]`) to return empty strings.
- **Solution**: Retrain the model. Verify that `labels_list = np.unique(dataset['labels'])` was saved correctly *before* label encoding was applied. Print `labels_list` in `train_model.py` to confirm it shows strings like `['DoS', 'Normal', 'Probe', ...]`.

---

### ❌ Error: `DeprecationWarning` or `FutureWarning` spam in Jupyter output

- **Cause**: Using older API signatures that are scheduled for removal in future library versions.
- **Solution**: These are warnings, not errors — they do not affect functionality. To suppress them for cleaner output, add at the top of the notebook cell: `import warnings` then `warnings.filterwarnings('ignore')`. Address them properly when upgrading libraries.

---

## SECURITY ETHICS & BEST PRACTICES

- **Never store plaintext passwords**: Use environment variables and consider hashing (`bcrypt`) for production.
- **Validate all file uploads**: Check file extension, size limit, and column schema before processing uploaded CSVs.
- **Hardened Security Headers**:
  - **`X-Frame-Options: SAMEORIGIN`**: Prevents "Clickjacking" (hacker overlaying our site on theirs).
  - **`X-Content-Type-Options: nosniff`**: Prevents the browser from "guessing" file types (security risk).
  - **`Cache-Control: no-store`**: Ensures that sensitive prediction data is never stored in the browser's temporary files.
- **CSRF Protection**: Every single form submission (POST) requires a unique, one-time "Security Token" (CSRF Token). Even if a hacker tricks a user into clicking a link, they cannot submit the form without this secret token.
- **Use HTTPS in production**: Locally, Flask's built-in server is for development only. In the container we run **gunicorn under supervisord** (no Nginx in-image); TLS/HTTPS is terminated by **Render** in front of the container.
- **Log predictions responsibly**: Network traffic data can be sensitive personal information. Log only metadata (attack type, timestamp) rather than raw packet data.
- **Audit AI decisions**: Always have a human review AI-flagged attacks before taking automated blocking actions.

---

## FUTURE ROADMAP & EXTENSIONS

- **Real Generative AI**: Replace the simulated insight dictionary with Google Gemini API or GPT-4 for dynamic, context-aware mitigation advice.
- **SMOTE Integration**: Apply Synthetic Minority Over-sampling to the training pipeline to balance rare attack classes like U2R and R2L.
- **Live Packet Capture**: Integrate with `pyshark` or `scapy` to analyze real-time network traffic instead of file uploads.
- **Dashboard Analytics**: Add a prediction history dashboard showing attack frequency over time using `Chart.js`.
- **Model Versioning**: Use `MLflow` to track model versions, accuracy metrics, and hyperparameters across training runs.
- **Multi-User Support**: Add a user management system with role-based access control (Admin vs. Analyst roles). *(Partially done: multi-user `users.json`, signup, account settings.)*
- **API Endpoint**: JSON envelopes already work on existing routes when the client sends `Accept: application/json` (`wants_json()`). A dedicated `/api/predict` wrapper and OpenAPI docs would be the next step.

---

## GLOSSARY OF TERMS

- **Backpropagation**: The "Learning" phase of a Neural Network; errors are propagated backward to adjust weights.
- **Bias**: Systematic error from wrong assumptions in the learning algorithm.
- **Cross-Validation**: Splitting data multiple times to test the model more rigorously.
- **Epoch**: One full pass through the entire training dataset by a neural network.
- **Gradient Descent**: Iterative optimization algorithm that minimizes the model's error function.
- **Hyperparameter**: A setting chosen before training (e.g., number of trees in a forest).
- **One-Hot Encoding**: Turning categories into separate binary columns (e.g., `is_TCP`, `is_UDP`).
- **Overfitting**: When a model memorizes training data and fails to generalize to new data.
- **Pickle**: Python library to serialize and deserialize Python objects to/from files.
- **Scaler**: A preprocessing transformation that normalizes feature values to a common range.
- **Session**: A server-side mechanism to remember a user's state across multiple HTTP requests.
- **SHAP**: SHapley Additive exPlanations — a game-theory-based method to explain AI predictions.
- **StandardScaler**: Scales data to zero mean and unit variance using the formula: `(x - mean) / std`.
- **Virtual Environment**: An isolated Python environment for a project to avoid library conflicts.

---

**Project Developed by:**

- Ankita Pati (23PBCA1335)
- Kumar Sreyan Pattanayak (23PBCA1355)
- Subhashree Pathy (23PBCA1386)
- Tanmaya Ranjan Jena (23PBCA1391)

**Academic Year:** 2023-2026
**Institution:** Roland Institute of Computer & Mgmt. Studies
**Degree:** BCA Final Year

---

*End of Project Guide.*
