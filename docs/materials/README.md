<!-- markdownlint-disable MD033 -->
<h1 align="center">
  <img src="../CyberAttackPrediction/static/images/logo_with_bg.svg" alt="CyberShield Logo" width="32" vertical-align="middle"> Cyber Attack Prediction
</h1>

<p align="center">A Machine Learning & Generative AI project for predicting cyber attacks.</p>

## 👥 4-Person Team Setup Guide

To ensure everyone is working in the exact same environment without conflicts, please follow these steps carefully.

### 1. Prerequisites

- **Python 3.10+**
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
   python -m venv venv
   ```

2. **Activate it:**
   - **Windows:** `venv\Scripts\activate`
   - **Mac/Linux:** `source venv/bin/activate`

3. **Install the exact team dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### 4. Handling Datasets (NSL-KDD / CIC-IDS)

**DO NOT COMMIT DATASETS TO GIT.** They are too large and will break your repository.

1. Download the datasets manually.
2. Place them inside the `data/` folder on your own laptop.
3. The `data/` folder is intentionally ignored by `.gitignore`, so your datasets stay safely on your local machine.
