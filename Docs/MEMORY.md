# Project Memory
## Parcl Buyer Segmentation & Investment Profiling

**Last Updated:** September 20, 2026  

---

## 1. Project Identity

| Field | Value |
|-------|-------|
| Project name | Parcl Buyer Segmentation & Investment Profiling |
| App title | Parcl \| Buyer Segmentation Intelligence |
| Primary file | `app.py` |
| Suggested GitHub repo | `parcl-buyer-segmentation` |
| Platform | Streamlit |
| Domain | Real estate / market intelligence |

---

## 2. Key Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-09-20 | Use real `clients.csv` + `properties.csv` (not synthetic) | Files provided in project folder |
| 2026-09-20 | Single-file Streamlit app | Simpler for internship submission & Cloud deploy |
| 2026-09-20 | k=4 fixed with Elbow + Silhouette shown | Matches recommended 4 business segments |
| 2026-09-20 | Heuristic segment naming (not hardcoded IDs) | Survives reordering of cluster labels |
| 2026-09-20 | Relative paths for CSVs | Portable across machines |
| 2026-09-20 | Prefer `st.info` over custom light HTML boxes | Dark-mode text visibility issue |
| 2026-09-20 | Cache both data load and clustering | Interactive filters stay fast |

---

## 3. Data Facts

- **clients.csv**: 2,000 rows  
  Fields: client_id, client_type, first_name, last_name, date_of_birth, gender, country, region, acquisition_purpose, satisfaction_score, loan_applied, referral_channel  

- **properties.csv**: 10,000 rows  
  Fields: listing_id, tower_number, transaction_date, unit_category, unit_number, floor_area_sqft, sale_price, listing_status, client_ref  

- Every client has at least 3 linked properties.  
- `sale_price` is a string with `$` and commas; must be cleaned before numeric ops.  
- `listing_status` = Sold (7,305) / Available (2,695). Only Sold used for financial aggregates.  
- `client_type` values: Individual / Company → normalized to Individual / Corporate.  
- `acquisition_purpose`: Home / Investment.  
- `loan_applied`: Yes / No → 1 / 0.  
- `satisfaction_score`: 1–5 integer.  

---

## 4. Segment Mapping Logic (Current Heuristic)

Order of assignment (remaining clusters only):
1. **Global Investors** – highest (investment_rate × total_spend)
2. **First-Time Buyers** – highest (loan_rate / age)
3. **Corporate Buyers** – highest corporate share
4. **Luxury Investors** – remaining cluster

Colors:
- Global Investors → `#0f766e`
- First-Time Buyers → `#2563eb`
- Corporate Buyers → `#7c3aed`
- Luxury Investors → `#d97706`

---

## 5. Known Issues & Fixes

| Issue | Fix | Date |
|-------|-----|------|
| White text on light methodology box (dark mode) | Replaced custom HTML with `st.info()` | 2026-09-20 |
| Hardcoded absolute paths | Switched to `os.path.dirname(__file__)` | 2026-09-20 |
| `streamlit` not found on user Windows | Instructed `pip install` + `python -m streamlit` | 2026-09-20 |

---

## 6. Run Commands (Reference)

```bash
cd buyer_segmentation_app
pip install -r requirements.txt
python -m streamlit run app.py
```

---

## 7. Open Items

- [ ] User to create GitHub repo `parcl-buyer-segmentation` and push
- [ ] Optional: research paper deliverable
- [ ] Optional: Streamlit Cloud deploy

---

## 8. Contact / Context

- Built as an internship / portfolio project under Unified Mentor style brief.
- Target company context: Parcl (real estate market intelligence).
- Original brief also listed a research paper; dashboard is the primary delivered artifact.
