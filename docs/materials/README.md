<!-- markdownlint-disable MD033 -->
<h1 align="center">
  <img src="../CyberAttackPrediction/static/images/logo_with_bg.svg" alt="CyberShield Logo" width="32" vertical-align="middle"> Cyber Attack Prediction
</h1>

<p align="center">A Machine Learning & Generative AI project for predicting cyber attacks.</p>

## 👥 4-Person Team Setup Guide

To ensure everyone is working in the exact same environment without conflicts, please follow these steps carefully.

### 1. Prerequisites

- **Python 3.13** (local dev; the Docker/Render image uses Python 3.12-slim)
- **Git**

### 2. Getting the Code

Since this is a collaborative project, one person needs to create a GitHub repository and the rest will clone it.

**Person A (Project Lead):**

1. Create a new empty repository on GitHub (e.g., `cyber-attack-prediction`).
2. Run these commands in this exact `Project` folder on your PC:

   ```bash
   git add .
   git commit -m "Initial project setup"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/cyber-attack-prediction.git
   git push -u origin main
   ```

**Persons B, C, and D:**

1. Clone the repository to your own laptops:

   ```bash
   git clone https://github.com/YOUR-USERNAME/cyber-attack-prediction.git
   cd cyber-attack-prediction
   ```

### 3. Setting Up the Virtual Environment (Every Team Member)

You must **never** push your virtual environment to Git. We have already added it to `.gitignore`. Everyone builds their own locally.

1. **Create the environment:**

   ```bash
   python -m venv .venv
   ```

2. **Activate it:**
   - **Windows:** `.venv\Scripts\activate`
   - **Mac/Linux:** `source .venv/bin/activate`

3. **Install the exact team dependencies:**

   ```bash
   # Runtime / web app
   pip install -r CyberAttackPrediction/requirements.txt
   # Notebooks & SHAP (optional, local research only)
   pip install -r CyberAttackPrediction/requirements-dev.txt
   ```

   There is no root-level `requirements.txt`.

### 4. Handling Datasets (NSL-KDD / CIC-IDS)

Datasets live in **`CyberAttackPrediction/Dataset/`** (not a `data/` folder).

- Most committed CSVs **are tracked** in git so the Render container can train on its ephemeral disk.
- Runtime uploads stay local/ignored: `uploaded_*.csv`, `custom_train.csv`, `X-IIoTID dataset.csv`, and `static/Dataset/*.csv` (see `.gitignore`).
- If you need a huge research CSV that is intentionally ignored, drop it in `CyberAttackPrediction/Dataset/` under an ignored name — do not invent a separate `data/` folder.
