# Project Rules
## Parcl Buyer Segmentation & Investment Profiling

**Version:** 1.0  
**Date:** September 2026  

---

## 1. Code Rules

1. **Single entry point** – All application logic lives in `app.py` unless a clear module split is required later.
2. **No hardcoded absolute paths** – Use `os.path.dirname(os.path.abspath(__file__))` so the app is portable.
3. **Fixed random seeds** – `random_state=42` (or equivalent) on all sklearn estimators for reproducibility.
4. **Cache expensive work** – Data loading and clustering must use `@st.cache_data`.
5. **No secrets in repo** – Never commit API keys, passwords, or `.streamlit/secrets.toml`.
6. **Dependencies pinned by intent** – Keep `requirements.txt` minimal and version-aware.

---

## 2. Data Rules

1. **Source of truth** – `clients.csv` and `properties.csv` are the only data sources in v1.
2. **Do not mutate source files** – All cleaning happens in memory after load.
3. **Sold listings only** for spend/price aggregates; Available listings are excluded from financial metrics.
4. **Missing numerics → 0** after client–property join (clients with no sold units).
5. **Age is derived** from `date_of_birth` relative to 2026-01-01; never trust a pre-computed age column.

---

## 3. Modeling Rules

1. **Primary model = K-Means (k=4)**  
2. **Validation model = Agglomerative Hierarchical (ward, k=4)**  
3. **Optimal k evidence** must be shown (Elbow + Silhouette) even if k is fixed to 4 for business reasons.
4. **Segment names are business labels**, not raw cluster IDs. Mapping must be deterministic and documented.
5. **Do not leak future information** – Only use features available at client profile / transaction time.

---

## 4. UI / UX Rules

1. Prefer Streamlit native components (`st.metric`, `st.info`, `st.dataframe`) over custom HTML when theme compatibility matters.
2. Sidebar filters apply to **all tabs**.
3. Every chart should have a clear title and readable axis labels.
4. Segment colors are fixed (see DESIGN.md) and must stay consistent across the whole app.
5. Never show raw cluster integers (0–3) to end users; always show business segment names.

---

## 5. Git & Repository Rules

1. Do not commit `__pycache__/`, virtualenvs, or OS junk (see `.gitignore`).
2. Commit messages should be concise and descriptive.
3. Large generated artifacts (extra models, temp CSVs) stay out of the repo unless required for the demo.
4. Documentation files (`PRD.md`, `ARCHITECTURE.md`, etc.) stay in the project root next to `app.py`.

---

## 6. Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Python variables | snake_case | `total_spend` |
| Functions | snake_case | `load_and_prepare_data` |
| Streamlit tabs | Title Case labels | `"Model Diagnostics"` |
| Segment names | Title Case | `"First-Time Buyers"` |
| Files | snake_case or kebab | `app.py`, `requirements.txt` |

---

## 7. Definition of Done (Feature)

A feature is done when:
- [ ] It works with the provided CSVs
- [ ] It respects global sidebar filters
- [ ] It does not break dark mode readability
- [ ] It is covered by the relevant documentation section (if user-facing)
- [ ] Randomness is seeded where applicable
