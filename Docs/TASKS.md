# Task Tracker
## Parcl Buyer Segmentation & Investment Profiling

**Last Updated:** September 2026  

---

## Phase 1 – Data & Pipeline

| ID | Task | Status | Notes |
|----|------|--------|-------|
| T1.1 | Load and inspect `clients.csv` / `properties.csv` | ✅ Done | 2000 clients, 10000 properties |
| T1.2 | Clean clients (dedupe, DOB→age, loan map, client_type normalize) | ✅ Done | |
| T1.3 | Clean properties (sale_price parse, Sold filter) | ✅ Done | |
| T1.4 | Aggregate property metrics per client | ✅ Done | purchases, spend, unit price, floor area |
| T1.5 | Join client + property features | ✅ Done | |

---

## Phase 2 – Machine Learning

| ID | Task | Status | Notes |
|----|------|--------|-------|
| T2.1 | Encode categoricals (LabelEncoder) | ✅ Done | |
| T2.2 | Scale features (StandardScaler) | ✅ Done | |
| T2.3 | Elbow Method (k=2..8) | ✅ Done | |
| T2.4 | Silhouette Score evaluation | ✅ Done | |
| T2.5 | Fit K-Means k=4 | ✅ Done | Primary model |
| T2.6 | Fit Hierarchical k=4 (validation) | ✅ Done | |
| T2.7 | PCA 2D projection | ✅ Done | |
| T2.8 | Map clusters → business segment names | ✅ Done | Heuristic rules |

---

## Phase 3 – Streamlit Application

| ID | Task | Status | Notes |
|----|------|--------|-------|
| T3.1 | App shell, page config, CSS | ✅ Done | |
| T3.2 | Sidebar filters (country, region, purpose, type, segment) | ✅ Done | |
| T3.3 | Overview tab | ✅ Done | KPIs, pie, PCA, cards |
| T3.4 | Segment Insights tab | ✅ Done | |
| T3.5 | Investor Behavior tab | ✅ Done | |
| T3.6 | Geographic Analysis tab | ✅ Done | |
| T3.7 | Model Diagnostics tab | ✅ Done | Fixed dark-mode text issue |
| T3.8 | Data Explorer tab + CSV download | ✅ Done | |
| T3.9 | Caching for load + clustering | ✅ Done | `@st.cache_data` |
| T3.10 | Relative file paths for portability | ✅ Done | |

---

## Phase 4 – Documentation & Delivery

| ID | Task | Status | Notes |
|----|------|--------|-------|
| T4.1 | `requirements.txt` | ✅ Done | |
| T4.2 | `.gitignore` | ✅ Done | |
| T4.3 | PRD.md | ✅ Done | |
| T4.4 | ARCHITECTURE.md | ✅ Done | |
| T4.5 | DESIGN.md | ✅ Done | |
| T4.6 | RULES.md | ✅ Done | |
| T4.7 | TASKS.md | ✅ Done | This file |
| T4.8 | MEMORY.md | ✅ Done | |
| T4.9 | Push to GitHub | 🔄 In Progress | Repo name: `parcl-buyer-segmentation` |

---

## Phase 5 – Optional / Future

| ID | Task | Status | Notes |
|----|------|--------|-------|
| T5.1 | Research paper (EDA + insights + recommendations) | ⏳ Optional | Mentioned in original brief |
| T5.2 | Deploy to Streamlit Community Cloud | ⏳ Optional | |
| T5.3 | Add authentication | ⏳ Out of scope v1 | |
| T5.4 | Connect live database | ⏳ Out of scope v1 | |

---

## How to Use This File
- Mark tasks ✅ when complete
- Move blocked items to a “Blocked” note with reason
- Keep Phase 5 items optional unless product owner prioritizes them
