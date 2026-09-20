# Tasks
## Nassau Candy Factory Reallocation Project

Status legend: `[x]` done · `[ ]` todo · `[~]` in progress

---

## Phase 1 — Data & Modeling

- [x] Load and explore raw order dataset
- [x] Assign products to factories (mapping table)
- [x] Engineer distance (haversine from factory to state centroid)
- [x] Engineer synthetic lead times (distance + ship mode)
- [x] Encode categoricals + scale numeric features
- [x] Train Linear Regression baseline
- [x] Train Random Forest
- [x] Train Gradient Boosting (selected, R² ≈ 0.884)
- [x] Save model, encoders, scaler (joblib)
- [x] Export `nassau_prepared.csv`

---

## Phase 2 — Application

- [x] Build Overview & KPIs module
- [x] Build Factory Optimization Simulator
- [x] Build What-If Scenario Analysis
- [x] Build Recommendation Dashboard (priority slider)
- [x] Build Risk & Impact Panel
- [x] Apply professional UI theme (navy / teal)
- [x] Path-safe loading for Windows + Cloud

---

## Phase 3 — Documentation & Paper

- [x] Research paper (EDA, methodology, recommendations)
- [x] Executive summary
- [x] PRD.md
- [x] ARCHITECTURE.md
- [x] DESIGN.md
- [x] RULES.md
- [x] TASKS.md
- [x] MEMORY.md

---

## Phase 4 — Deploy & Submit

- [x] Create GitHub repository
- [x] Push app, data, models, requirements
- [x] Deploy to Streamlit Community Cloud
- [x] Fix joblib / requirements on Cloud
- [x] Upload research paper to GitHub
- [ ] Write/improve README.md with screenshots
- [ ] Record project feedback video (3–8 min)
- [ ] Submit all 4 URLs on Unified Mentor form
- [ ] Move Kanban card to Completed after submission

---

## Optional / Stretch

- [ ] Add map view of factories vs regions
- [ ] Export recommendations to CSV from dashboard
- [ ] Simple capacity constraint toggle
- [ ] Unit tests for `predict_lead_time` and haversine

---

## Quick reference links

| Item | URL |
|------|-----|
| GitHub | https://github.com/mohitjangid21797-crypto/Nassu-Candy-Optimisier |
| Live app | https://qxuoj48fmif7qpz3vefvrb.streamlit.app |
| Research paper | https://github.com/mohitjangid21797-crypto/Nassu-Candy-Optimisier/blob/main/Factory%20Reallocation%20%26%20Shipping%20Optimization.docx |
