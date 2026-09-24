# Dataset Folder Audit — Simple Summary

## What Was the Issue?

The project had **two folders** both named "Dataset" in different locations. This was confusing — it looked like datasets were duplicated or placed in the wrong spot.

**Fix:** The old, unused duplicate folder (`static/Dataset/`) has been deleted. ✅

---

## Why Are There 4 Datasets But the Website Seems to Use Only 1?

The project has two separate "parts":

### 📓 Part 1: The Research Notebooks

These are the Jupyter Notebook files where the initial research was done — testing multiple algorithms, comparing results, generating charts. **4 of the 8 CSV files** are used here to prove the AI works across different types of network data.

| File | What It Is |
| --- | --- |
| `kdd_train.csv` | Classic network attack data — the industry standard benchmark. Used for both research AND as the website's default. |
| `CIC-IDS2017.csv` | More modern network attack data from 2017. Research notebooks only. |
| `CICDDos2019.csv` | Focused specifically on flood/overload type attacks. Research notebooks only. |
| `X-IIoTID dataset.csv` | Attack data from smart industrial devices (IoT). Research notebooks only. |

### 🌐 Part 2: The Website (Flask Web App)

The live website uses **NSL-KDD as its default** but also creates and manages its own working files automatically:

| File | What It Is |
| --- | --- |
| `kdd_train.csv` | Default training data (shared with notebooks) |
| `custom_train.csv` | Saved copy of any CSV the user uploads to retrain the AI |
| `sample_train.csv` | A small example file users can download from the site to see the correct format |
| `testData.csv` | A default test file used for prediction demos |
| `uploaded_test.csv` | Temporary file saved when a user uploads data to get predictions |

So in total: **4 research datasets + 4 website working files = 8 CSVs**. All are valid and needed.

---

## What Was Done

| What | Status |
| --- | --- |
| Deleted the old, empty `static/Dataset/` folder | ✅ Done |
| Removed its mention from the project docs | ✅ Done |
| Added a clear note in the docs explaining the 4-dataset vs. web app split | ✅ Done |

---

## Git Tracking (post deploy-audit)

`.gitignore` keeps most of `CyberAttackPrediction/Dataset/` **tracked** so the
Render container can train on its ephemeral disk, while ignoring runtime
artifacts:

- Ignored: `uploaded_*.csv`, `custom_train.csv`, `X-IIoTID dataset.csv`, `static/Dataset/*.csv`
- Tracked: research CSVs such as `kdd_train.csv`, `CIC-IDS2017.csv`, `CICDDos2019.csv`, sample/test files

---

## In One Sentence

> The project uses 4 datasets for research (in the notebooks) but the website only uses 1 by default — the duplicate folder was a leftover from an earlier phase and has been cleaned up.
