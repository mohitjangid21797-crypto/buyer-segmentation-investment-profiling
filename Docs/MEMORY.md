# Project Memory
## Nassau Candy Factory Optimizer

Persistent facts for AI-assisted development and handoff.

---

## Project identity

- **Name:** Factory Reallocation & Shipping Optimization Recommendation System for Nassau Candy Distributor
- **Platform:** Unified Mentor internship / project allotment
- **Stack:** Python, pandas, scikit-learn, joblib, Streamlit, Plotly
- **Repo:** https://github.com/mohitjangid21797-crypto/Nassu-Candy-Optimisier
- **Live app:** https://qxuoj48fmif7qpz3vefvrb.streamlit.app

---

## Business context

- Static product→factory rules cause long lead times and logistics inefficiency.
- Leadership needs: simulate reassignment, quantify impact, recommend with profit safety.
- Five factories with fixed coordinates (AZ, GA, MN area, IL/IA area, TN area).
- Products: mostly Wonka Bars (Chocolate), some Sugar and Other lines.

---

## Data facts

- Raw file: `Nassau Candy Distributor.csv` (~10,194 rows).
- Prepared file: `nassau_prepared.csv` (adds Factory, Distance_mi, LeadTime_days, CustLat, CustLon).
- Original Order Date / Ship Date gaps were multi-year; **not used** as real lead time.
- Lead time is synthetic: f(distance, ship mode) + noise, range roughly 1–11 days.
- Regions: Interior, Atlantic, Gulf, Pacific.
- Ship modes: Standard Class, Second Class, First Class, Same Day.

---

## Model facts

- Best model: **Gradient Boosting Regressor** (R² ≈ 0.884, RMSE ≈ 0.76 days).
- Artifacts: `best_model.joblib`, `encoders.joblib`, `scaler.joblib`.
- Features: Product Name, Factory, Region, Ship Mode, Distance_mi, Units, Division.
- Do not retrain at app runtime on Cloud.

---

## Product → Factory mapping (current)

| Division | Product | Factory |
|----------|---------|---------|
| Chocolate | Wonka Bar - Nutty Crunch Surprise | Lot's O' Nuts |
| Chocolate | Wonka Bar - Fudge Mallows | Lot's O' Nuts |
| Chocolate | Wonka Bar -Scrumdiddlyumptious | Lot's O' Nuts |
| Chocolate | Wonka Bar - Milk Chocolate | Wicked Choccy's |
| Chocolate | Wonka Bar - Triple Dazzle Caramel | Wicked Choccy's |
| Sugar | Laffy Taffy, SweeTARTS, Nerds, Fun Dip | Sugar Shack |
| Other | Fizzy Lifting Drinks | Sugar Shack |
| Sugar | Everlasting Gobstopper | Secret Factory |
| Sugar | Hair Toffee | The Other Factory |
| Other | Lickable Wallpaper, Wonka Gum | Secret Factory |
| Other | Kazookles | Secret Factory (default) |

---

## App modules

1. Overview & KPIs  
2. Factory Simulator  
3. What-If Analysis  
4. Recommendations (Speed ↔ Profit slider)  
5. Risk & Impact  

---

## UI theme (current)

- Dark navy background `#0B1120`
- Cards `#1E293B`
- Accent teal `#0EA5E9`, amber `#F59E0B`
- Professional (not neon candy pink)

---

## Submission status (as of last update)

- [x] GitHub public repo  
- [x] Streamlit Cloud deploy working  
- [x] Research paper on GitHub  
- [ ] Feedback video  
- [ ] Final form submit + Kanban → Completed  

---

## Known pitfalls

1. Windows path with `\Users` in a normal string → unicodeescape SyntaxError. Use raw strings or `os.path`.
2. Streamlit Cloud needs `joblib` (and all deps) in `requirements.txt`.
3. Browser downloads may rename files to `file (1).py` — rename before running.
4. MSYS2 Python on Windows may lack pip/streamlit; prefer official CPython 3.12 or `py -3.12`.

---

## Decisions log

- Use engineered lead times instead of broken date differences.
- Use Gradient Boosting as production model.
- Single-file Streamlit app for simpler Cloud deploy.
- Priority slider for soft multi-objective ranking (speed vs profit).
- Professional navy/teal theme for stakeholder demos.
