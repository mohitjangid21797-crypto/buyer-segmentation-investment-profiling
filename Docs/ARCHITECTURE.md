# Architecture Document
## Parcl Buyer Segmentation & Investment Profiling

**Version:** 1.0  
**Date:** September 2026  

---

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Frontend                       │
│  (Tabs: Overview | Segments | Behavior | Geo | Model | Data) │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer (app.py)                 │
│  • Sidebar filters                                           │
│  • Cached data loading                                       │
│  • Cached clustering pipeline                                │
│  • Plotly visualizations                                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
           ┌───────────────┴───────────────┐
           ▼                               ▼
┌─────────────────────┐         ┌─────────────────────┐
│   clients.csv       │         │  properties.csv     │
│   (2,000 rows)      │         │  (10,000 rows)      │
└─────────────────────┘         └─────────────────────┘
```

---

## 2. Data Flow

```
1. Load CSVs
       │
2. Clean clients (dedupe, parse DOB → age, map loan/client_type)
       │
3. Clean properties (parse sale_price, filter Sold)
       │
4. Aggregate property metrics per client_id
       │
5. Left-join aggregates onto clients
       │
6. Encode categoricals (LabelEncoder)
       │
7. Scale numeric + encoded features (StandardScaler)
       │
8. Fit K-Means (k=4) + Hierarchical (validation)
       │
9. PCA (2D) for visualization
       │
10. Map cluster IDs → business segment names
       │
11. Apply sidebar filters → render tabs
```

---

## 3. Component Breakdown

| Component | Responsibility | Tech |
|-----------|----------------|------|
| Data Loader | Read CSVs, clean, join, feature engineering | pandas, numpy |
| Clustering Engine | Scale, K-Means, Hierarchical, PCA, metrics | scikit-learn |
| Segment Mapper | Heuristic mapping of cluster → business label | pandas |
| Filter Engine | Sidebar multiselects → boolean mask | Streamlit |
| Visualization | Charts, heatmaps, scatter, tables | Plotly |
| UI Shell | Layout, tabs, metrics, download | Streamlit |

---

## 4. Feature Set Used for Clustering

**Categorical (Label Encoded)**
- client_type
- gender
- country
- region
- acquisition_purpose
- referral_channel

**Numeric**
- age
- satisfaction_score
- loan_applied
- total_purchases
- total_spend
- avg_unit_price
- avg_floor_area
- apartment_count
- office_count

---

## 5. Caching Strategy

| Function | Decorator | Reason |
|----------|-----------|--------|
| `load_and_prepare_data()` | `@st.cache_data` | Avoid re-reading & re-joining CSVs |
| `run_clustering()` | `@st.cache_data` | Avoid re-fitting models on every interaction |

Filters operate on the already-clustered dataframe in memory — no model retrain on filter change.

---

## 6. Deployment Model

```
Local / Dev:
  python -m streamlit run app.py

Production options:
  • Streamlit Community Cloud
  • Docker + any container host
  • Internal server (port 8501)
```

No external database or API dependencies in v1. All data is file-based.

---

## 7. File Structure

```
buyer_segmentation_app/
├── app.py                 # Main application
├── clients.csv            # Client master data
├── properties.csv         # Property transactions
├── requirements.txt       # Python dependencies
├── .gitignore
├── PRD.md
├── ARCHITECTURE.md
├── DESIGN.md
├── RULES.md
├── TASKS.md
└── MEMORY.md
```

---

## 8. Key Design Decisions

1. **Single-file app** – Simpler for internship/portfolio submission and Streamlit Cloud deploy.
2. **Relative paths** – App runs from any working directory as long as CSVs sit next to `app.py`.
3. **Heuristic segment naming** – Clusters are mapped to business labels using domain rules (investment rate, loan rate, corporate share, spend) rather than hard-coded IDs.
4. **No database** – Keeps the project self-contained and reproducible.
