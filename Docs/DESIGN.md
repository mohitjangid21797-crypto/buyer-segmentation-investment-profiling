# Design System
## Nassau Candy Factory Optimizer UI

---

## 1. Design Goals

- Professional and suitable for leadership demos
- Clear hierarchy: KPIs → charts → actions
- Consistent factory color coding
- Dark theme for modern analytics look
- Readable on desktop (primary) and acceptable on laptop

---

## 2. Color Palette

| Role | Hex | Usage |
|------|-----|--------|
| Background | `#0B1120` | App background |
| Surface / cards | `#1E293B` | Metric cards, hero |
| Border | `#334155` | Card borders |
| Text primary | `#F8FAFC` | Titles, metric values |
| Text secondary | `#94A3B8` | Labels, captions |
| Accent (teal) | `#0EA5E9` | Primary actions, Lot's O' Nuts |
| Accent (violet) | `#8B5CF6` | Wicked Choccy's |
| Accent (teal-green) | `#14B8A6` | Sugar Shack / “current best” |
| Accent (amber) | `#F59E0B` | Secret Factory / highlights |
| Muted | `#64748B` | The Other Factory, footer |

### Factory colors (charts)

```
Lot's O' Nuts      → #0EA5E9
Wicked Choccy's    → #8B5CF6
Sugar Shack        → #14B8A6
Secret Factory     → #F59E0B
The Other Factory  → #64748B
```

---

## 3. Typography

- **Font:** Inter (system fallback: -apple-system, sans-serif)
- **Page title:** 1.55–1.75rem, weight 700
- **Section headers:** 1.1rem, weight 600
- **Metric labels:** 0.75rem, uppercase, letter-spacing 0.5px
- **Metric values:** 1.6rem, weight 700

---

## 4. Layout

- **Sidebar:** Fixed left, navigation + filters
- **Main:** Max width ~1400px, padded
- **Hero card:** Full-width intro banner per page
- **KPI row:** 5 equal columns on Overview
- **Charts:** 2-column where useful (bar + pie), full width for heatmap/treemap

---

## 5. Components

### Metric card
- Dark surface, subtle border, 12px radius
- Label (muted) + large value (white)

### Hero card
- Gradient surface, 14px radius, short title + subtitle

### Charts (Plotly)
- Transparent paper/plot background
- Soft grid lines
- Consistent font color `#CBD5E1`
- Color scales: navy → teal → amber for continuous data

### Alerts
- Streamlit success / info / warning with rounded corners

---

## 6. Navigation

Sidebar radio (icon + label):

1. Overview & KPIs  
2. Factory Simulator  
3. What-If Analysis  
4. Recommendations  
5. Risk & Impact  

Filters (shared):

- Speed ↔ Profit slider (0–1)
- Region multiselect
- Ship Mode multiselect

---

## 7. UX Rules

1. Always show **current factory** vs **recommended** clearly (color or badge).
2. Prefer numbers + short sentences over long paragraphs.
3. Empty states: one clear message (e.g. “No better alternatives under current priority”).
4. Loading: rely on Streamlit cache; avoid heavy recomputation on every widget change where possible.
5. Do not use neon pink or high-saturation candy colors for professional demos.

---

## 8. Responsive Notes

- Designed primarily for desktop width ≥ 1200px.
- Sidebar collapses on narrow screens (Streamlit default).
- Charts use `use_container_width=True` for fluid layout.
