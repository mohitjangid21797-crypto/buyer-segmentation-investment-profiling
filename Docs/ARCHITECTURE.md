# Architecture
## Nassau Candy Factory Reallocation Optimizer

---

## 1. High-Level Architecture

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│  Order Dataset  │────▶│  Data Preparation    │────▶│  Feature Matrix │
│  (CSV)          │     │  + Lead-time engine  │     │  + Labels       │
└─────────────────┘     └──────────────────────┘     └────────┬────────┘
                                                              │
                                                              ▼
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│  Streamlit UI   │◀────│  Scenario Engine     │◀────│  ML Models      │
│  (5 modules)    │     │  + Ranking logic     │     │  (GB best)      │
└─────────────────┘     └──────────────────────┘     └─────────────────┘
```

---

## 2. Components

### 2.1 Data Layer
- `nassau_prepared.csv` — cleaned orders with Factory, Distance_mi, LeadTime_days, CustLat/Lon
- `best_model.joblib` — Gradient Boosting Regressor
- `encoders.joblib` — LabelEncoders for Product, Factory, Region, Ship Mode, Division
- `scaler.joblib` — StandardScaler for Distance_mi, Units

### 2.2 Modeling Layer
| Model | Role | R² (test) |
|-------|------|-----------|
| Linear Regression | Baseline | 0.782 |
| Random Forest | Ensemble | 0.881 |
| **Gradient Boosting** | **Production** | **0.884** |

**Target:** LeadTime_days  
**Features:** Product Name, Factory, Region, Ship Mode, Distance_mi, Units, Division

### 2.3 Simulation & Optimization Layer
- For each product × alternate factory × region:
  - Recompute haversine distance
  - Predict lead time with production model
  - Score = weighted (speed_score, profit_score) via priority slider
- Rank and filter by confidence thresholds

### 2.4 Presentation Layer
- Streamlit single-page app with sidebar navigation
- Five modules: Overview, Simulator, What-If, Recommendations, Risk
- Plotly charts (bar, pie, heatmap, treemap, scatter)

---

## 3. Runtime Flow

1. App loads CSV + joblib artifacts (cached).
2. User selects page + filters (region, ship mode, priority).
3. Overview: aggregate KPIs and charts from filtered data.
4. Simulator / What-If: call `predict_lead_time()` for candidate factories.
5. Recommendations: loop top products → score all factories → emit ranked table.
6. Risk: compute risk score from lead time + profit contribution.

---

## 4. Deployment

| Environment | Details |
|-------------|---------|
| Local | `streamlit run nassau_streamlit_app.py` |
| Cloud | Streamlit Community Cloud |
| Repo | GitHub (public) |
| Entry file | `nassau_streamlit_app.py` |
| Dependencies | `requirements.txt` |

**Public URL:** https://qxuoj48fmif7qpz3vefvrb.streamlit.app

---

## 5. File Structure

```
Nassu-Candy-Optimisier/
├── nassau_streamlit_app.py      # Main application
├── nassau_prepared.csv          # Prepared dataset
├── best_model.joblib            # Production model
├── encoders.joblib
├── scaler.joblib
├── requirements.txt
├── README.md
├── docs/
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   ├── DESIGN.md
│   ├── RULES.md
│   ├── TASKS.md
│   └── MEMORY.md
└── Factory Reallocation & Shipping Optimization.docx
```

---

## 6. Key Design Decisions

1. **Synthetic lead times** — Original order/ship dates produced multi-year gaps; lead time is engineered from distance + ship-mode multipliers for realistic modeling.
2. **State-centroid distances** — Customer location approximated by state centroid for scalable haversine calculation.
3. **Single-file Streamlit app** — Simpler deploy on Streamlit Cloud; no multi-page package required.
4. **Priority slider** — Soft multi-objective ranking (speed vs profit) without hard constraints.
