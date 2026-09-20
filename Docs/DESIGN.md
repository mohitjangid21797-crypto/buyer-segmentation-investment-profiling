# Design Document
## Parcl Buyer Segmentation & Investment Profiling

**Version:** 1.0  
**Date:** September 2026  

---

## 1. Design Principles

1. **Clarity first** – Business users should understand segments without reading model docs.
2. **Theme-safe** – Prefer Streamlit native components (`st.info`, `st.metric`) over custom HTML where possible so light/dark mode works.
3. **Progressive disclosure** – Overview → deep dive → diagnostics.
4. **Filter-everywhere** – Sidebar filters apply globally across all tabs.
5. **Reproducible** – Fixed seeds, explicit requirements, no hidden state.

---

## 2. Visual Design

### 2.1 Color System

| Token | Hex | Usage |
|-------|-----|-------|
| Primary Teal | `#0f766e` | Global Investors, accents, primary charts |
| Blue | `#2563eb` | First-Time Buyers |
| Purple | `#7c3aed` | Corporate Buyers |
| Amber | `#d97706` | Luxury Investors |
| Header Gradient | `#0f172a → #1e3a5f → #0f766e` | Top banner |
| Surface | `#f8fafc` / dark theme auto | Cards, backgrounds |

### 2.2 Typography
- Font stack: Inter (via Google Fonts) with system fallbacks
- Headers: bold, tight letter-spacing
- Body: regular weight, high readability

### 2.3 Layout
- Wide layout (`layout="wide"`)
- Expanded sidebar for filters
- 6 top-level tabs
- Metric row (5 columns) on Overview
- Two-column chart grids on most analysis tabs

---

## 3. UI Structure

```
┌──────── Sidebar ────────┬────────── Main Area ──────────────────┐
│ Filters                 │  Header Banner                         │
│  - Country              │  ───────────────────────────────────── │
│  - Region               │  [Overview] [Segments] [Behavior] ...  │
│  - Purpose              │                                        │
│  - Client Type          │  Tab content (charts / tables / KPIs)  │
│  - Segment              │                                        │
│                         │                                        │
│ Showing X of Y clients  │                                        │
└─────────────────────────┴────────────────────────────────────────┘
```

---

## 4. Tab-by-Tab Design Spec

### Tab 1 – Overview
- 5 KPI metrics (clients, segments, satisfaction, investment %, loan %)
- Left: Donut chart of segment distribution
- Right: PCA 2D scatter colored by segment
- Bottom: 4 segment snapshot cards (count, avg age, investment %, loan %)

### Tab 2 – Segment Insights
- Segment selector dropdown
- 5 KPIs for selected segment
- 2×2 chart grid: purpose, client type, loan, referral
- Age / satisfaction / purchases histograms
- Descriptive statistics table

### Tab 3 – Investor Behavior
- Cross-segment bar charts (avg spend, unit price, investment %, loan %)
- Spend vs Age scatter (size = purchases)
- Full comparison table

### Tab 4 – Geographic Analysis
- Stacked bar: country × segment
- Horizontal bar: top regions
- Grouped bar: segment mix in top regions
- Heatmap: region × segment
- Grouped bar: avg spend by country × segment

### Tab 5 – Model Diagnostics
- Methodology summary (`st.info`)
- Elbow curve + Silhouette curve (side by side)
- K-Means vs Hierarchical agreement metric + crosstab heatmap
- Feature separation strength (horizontal bar)

### Tab 6 – Data Explorer
- Sortable/filterable dataframe of key columns
- CSV download button
- Segment definition reference table

---

## 5. Interaction Design

| Action | Behavior |
|--------|----------|
| Change any sidebar filter | Instant re-filter of all visible charts/tables |
| Select segment (Tab 2) | Refresh all charts/KPIs for that segment only |
| Download CSV | Exports currently filtered client rows |
| Hover on charts | Plotly tooltips with client/segment context |

---

## 6. Accessibility & Theme Notes
- Prefer Streamlit native widgets for automatic dark-mode support
- Avoid light text on light backgrounds (use `st.info` instead of custom light boxes)
- Charts use high-contrast segment colors
- Metric labels remain readable in both themes

---

## 7. Empty / Edge States
- If filters result in zero rows: Streamlit will show empty charts; sidebar still displays “Showing 0 of N clients”
- All clients have ≥ 3 linked properties → no empty aggregate edge case in current data
