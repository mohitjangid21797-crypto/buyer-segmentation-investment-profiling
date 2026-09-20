# Product Requirements Document (PRD)
## Parcl Buyer Segmentation & Investment Profiling

**Version:** 1.0  
**Date:** September 2026  
**Status:** Delivered  

---

## 1. Overview

### 1.1 Product Name
Parcl Buyer Segmentation & Investment Profiling Dashboard

### 1.2 Summary
An AI-driven Streamlit web application that segments real estate buyers using unsupervised machine learning (K-Means + Hierarchical clustering) and provides interactive investment profiling, geographic analysis, and model diagnostics for the Parcl platform.

### 1.3 Problem Statement
Parcl currently lacks a data-driven understanding of:
- Different types of property buyers
- Investment motivations across demographics
- Geographic differences in investment behavior
- Customer financing patterns

This leads to inefficient marketing spend, generic property recommendations, and poor investor targeting.

### 1.4 Goals
- Discover hidden buyer segments using clustering algorithms
- Enable data-driven marketing and targeting strategies
- Provide interactive dashboards for business stakeholders
- Support filtering by country, region, purpose, and client type

---

## 2. Users & Stakeholders

| Persona | Needs |
|---------|-------|
| Marketing Team | Segment-specific campaigns, channel effectiveness |
| Sales / Advisors | Buyer profiles, financing behavior, geographic hotspots |
| Product / Data Team | Model diagnostics, feature importance, cluster validation |
| Leadership | High-level KPIs, investment vs home-buyer mix |

---

## 3. Functional Requirements

### 3.1 Data Pipeline
- Ingest `clients.csv` (2,000 clients) and `properties.csv` (10,000 listings)
- Clean and parse dates of birth → age
- Aggregate property-level features per client (purchases, spend, unit price, floor area)
- Encode categoricals, scale numeric features

### 3.2 Machine Learning
- K-Means clustering (primary, k=4)
- Hierarchical (Agglomerative) clustering for validation
- Elbow Method + Silhouette Score for optimal k selection
- PCA projection for visual cluster separation
- Business-mapped segments:
  - Global Investors
  - First-Time Buyers
  - Corporate Buyers
  - Luxury Investors

### 3.3 Dashboard Tabs
1. **Overview** – KPIs, segment distribution, PCA scatter, snapshot cards
2. **Segment Insights** – Deep dive per segment (demographics, financing, stats)
3. **Investor Behavior** – Cross-segment spend, loan rate, investment purpose comparison
4. **Geographic Analysis** – Country/region breakdowns, heatmaps
5. **Model Diagnostics** – Elbow, Silhouette, agreement matrix, feature importance
6. **Data Explorer** – Filterable table + CSV download

### 3.4 Filters (Sidebar)
- Country
- Region
- Acquisition Purpose
- Client Type
- Segment

---

## 4. Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Performance | Data load + clustering cached; interactive filters < 1s |
| Usability | Clean UI, dark-mode compatible, responsive layout |
| Portability | Relative paths; runs with `streamlit run app.py` |
| Reproducibility | Fixed random seeds; clear requirements.txt |

---

## 5. Success Metrics
- Clear, interpretable 4-segment solution
- Interactive dashboard usable by non-technical stakeholders
- Downloadable filtered client list for downstream campaigns
- Model diagnostics available for technical review

---

## 6. Out of Scope (v1)
- Real-time data ingestion / database connection
- Supervised prediction models
- User authentication / multi-tenant access
- Automated email / campaign triggers
- Mobile native app

---

## 7. Deliverables
- [x] Streamlit web application (`app.py`)
- [x] `clients.csv` + `properties.csv`
- [x] `requirements.txt`
- [x] Documentation suite (PRD, ARCHITECTURE, DESIGN, RULES, TASKS, MEMORY)
