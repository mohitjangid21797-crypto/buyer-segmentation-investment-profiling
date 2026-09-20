# Project Rules
## Nassau Candy Factory Optimizer

---

## 1. Coding Rules

1. **Single entry app** — Main logic lives in `nassau_streamlit_app.py` unless a clear split is needed.
2. **Paths** — Load data/models with relative paths and fallbacks (`os.path.dirname(__file__)`, `os.getcwd()`). Never hardcode Windows-only paths with unescaped backslashes.
3. **Caching** — Use `@st.cache_data` for CSV, `@st.cache_resource` for joblib models.
4. **No secrets in repo** — No API keys, passwords, or private credentials.
5. **Dependencies** — Every third-party package used must appear in `requirements.txt`.
6. **Python style** — Prefer clear names (`predict_lead_time`, `fact_summary`) over abbreviations.
7. **Errors** — Raise clear `FileNotFoundError` messages if CSV/models are missing.

---

## 2. Data Rules

1. Do not overwrite raw `Nassau Candy Distributor.csv` without a backup.
2. Prepared data lives in `nassau_prepared.csv` (includes Factory, Distance_mi, LeadTime_days).
3. Lead times are **engineered** (distance + ship mode); do not treat original multi-year ship dates as real lead times.
4. Factory assignments follow the product–factory mapping table in the PRD / research paper.
5. Kazookles defaults to Secret Factory when unassigned.

---

## 3. Model Rules

1. Production model is **Gradient Boosting** (`best_model.joblib`).
2. Always apply the same encoders and scaler used at train time.
3. Predictions must be clipped to a minimum of 1.0 day.
4. Do not retrain on Streamlit Cloud at runtime; use saved artifacts only.

---

## 4. UI Rules

1. Follow the Design System (navy / teal / amber palette).
2. Every page has a short hero description.
3. Show units on metrics (days, $, mi).
4. Mark “current factory” vs “recommended” explicitly.
5. Priority slider must affect Recommendation ranking (speed vs profit).

---

## 5. Git / Repo Rules

1. Public repo for submission.
2. Do not commit `__pycache__`, `.env`, or large temporary files.
3. Keep `requirements.txt` in sync with imports.
4. Research paper and executive summary may live in repo root or `/docs`.

---

## 6. Deployment Rules

1. App must run on Streamlit Community Cloud from the repo root entry file.
2. All four artifacts required at runtime: CSV + 3 joblib files.
3. After changing `requirements.txt`, reboot the Cloud app.

---

## 7. Submission Rules (Unified Mentor)

All form fields must be valid `https://` URLs:

- GitHub repository  
- Research paper  
- Deployed Streamlit app  
- Feedback video (YouTube/Loom)

---

## 8. Do Not

- Hardcode absolute paths like `C:\Users\...` in source.
- Leave trailing markers such as `EOF` in Python files.
- Commit model training notebooks as the only source of truth without saved joblib artifacts.
- Change factory coordinates without updating documentation.
