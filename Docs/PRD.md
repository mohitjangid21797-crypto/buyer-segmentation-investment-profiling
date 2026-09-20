# Product Requirements Document (PRD)
## Factory Reallocation & Shipping Optimization Recommendation System
### Nassau Candy Distributor

---

## 1. Overview

**Product name:** Nassau Candy Factory Optimizer  
**Type:** Decision-intelligence web application (Streamlit)  
**Goal:** Help leadership decide which products to reassign to which factories to reduce shipping lead times without harming profitability.

---

## 2. Problem Statement

Nassau Candy currently assigns products to factories using static rules. This causes:

- Suboptimal shipping distances
- High lead times for certain regions
- Margin erosion from logistics inefficiencies

There is no system to:

- Simulate factory–product reassignment scenarios
- Quantify operational impact before execution
- Recommend optimal configurations at scale

---

## 3. Objectives

1. Predict shipping lead time given product, factory, region, and ship mode.
2. Simulate reassignment of products to alternate factories.
3. Rank recommendations by lead-time reduction and profit impact.
4. Provide an interactive dashboard for what-if analysis and risk review.

---

## 4. Users

| User | Needs |
|------|--------|
| Operations / Logistics manager | See slow routes, test reassignments |
| Leadership / executives | Clear recommendations + profit safety |
| Analyst | Explore data, KPIs, model confidence |

---

## 5. Core Features

### 5.1 Overview & KPIs
- Total orders, avg lead time, sales, gross profit, avg distance
- Factory performance bar chart
- Orders-by-factory pie chart
- Lead-time heatmap (Region × Ship Mode)
- Product volume treemap

### 5.2 Factory Optimization Simulator
- Select product
- View predicted lead time across all 5 factories
- Highlight current vs best factory

### 5.3 What-If Scenario Analysis
- Select product, region, ship mode
- Compare current vs all alternate factories
- Show distance, predicted lead time, relative profit factor

### 5.4 Recommendation Dashboard
- Ranked reassignment suggestions for top products
- Expected lead-time reduction %
- Confidence level (High / Medium / Low)
- Priority slider: Speed ↔ Profit

### 5.5 Risk & Impact Panel
- High-risk product–factory combinations
- Scenario confidence metrics
- Factory capacity notes

---

## 6. Data

**Source:** Nassau Candy Distributor order dataset (~10,194 rows)

**Key fields:** Order ID, Ship Mode, Region, Product Name, Division, Sales, Units, Gross Profit, Cost

**Engineered:** Factory assignment, distance (haversine), synthetic lead time (distance + ship-mode factors)

**Factories:**
| Factory | Lat | Lon |
|---------|-----|-----|
| Lot's O' Nuts | 32.88 | -111.77 |
| Wicked Choccy's | 32.08 | -81.09 |
| Sugar Shack | 48.12 | -96.18 |
| Secret Factory | 41.45 | -90.57 |
| The Other Factory | 35.12 | -89.97 |

---

## 7. Success Metrics (KPIs)

| KPI | Target / observed |
|-----|-------------------|
| Lead Time Reduction | 8–15% on top reassignments |
| Model R² | ≥ 0.85 (achieved 0.884) |
| Profit Impact Stability | High (margin sensitivity < 5%) |
| Recommendation Coverage | Majority of top-10 volume products |

---

## 8. Out of Scope

- Real-time ERP integration
- Live capacity / inventory constraints
- Multi-echelon inventory optimization
- Mobile native app

---

## 9. Deliverables

1. Streamlit dashboard (deployed)
2. Research paper (EDA + modeling + recommendations)
3. Executive summary
4. Trained models + prepared dataset
5. GitHub repository

---

## 10. Constraints

- Must run on Streamlit Community Cloud
- Python stack: pandas, scikit-learn, joblib, plotly
- Public demo URL required for submission
