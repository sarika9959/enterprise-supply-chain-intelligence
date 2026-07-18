# Enterprise Supply Chain Intelligence Platform

An end-to-end supply chain analytics project investigating delivery performance across 60,000 orders, 40 suppliers, 7 warehouses, and 120 products — built to identify the root cause of poor on-time delivery and quantify the business risk it creates.

**Tech stack:** Python (Pandas, Matplotlib) · SQL (SQLite) · Power BI · DAX

---

## Business Problem

A manufacturing/logistics operation was experiencing inconsistent delivery performance, but leadership had no clear visibility into **why**. This project answers four questions a real supply chain team needs answered:

1. What is our actual on-time delivery rate, and how does it compare to industry benchmarks?
2. Which suppliers are driving the problem?
3. Is the cause supplier-related, regional, warehouse-related, or something else?
4. What dollar value is exposed to this risk?

---

## Key Findings

| Metric | Result |
|---|---|
| Overall on-time delivery rate | **69.63%** (industry benchmark: 90%+) |
| Tier A supplier on-time rate | 76.6% |
| Tier C supplier on-time rate | **55.3%** |
| Tier C avg. delay | **2.8 days** (3.5x worse than Tier A) |
| Revenue exposed to Tier C suppliers (Chassis & Structural) | **$4.05B** |
| Warehouse performance spread | 69–70% (ruled out as root cause) |

**Root cause identified:** The delivery problem is **supplier-driven, not operational**. All 7 warehouses perform within a tight 1-point band, eliminating warehouse operations as a cause. Meanwhile, Tier C suppliers — despite being flagged as unreliable — still receive over 1,400 orders each, and their failures concentrate heavily in high-value Chassis & Structural components.

**Recommendation:** Reduce order volume routed to Tier C suppliers, renegotiate contracts or SLAs with the six lowest-performing suppliers, and audit why "Critical" priority orders (70.5% on-time) barely outperform "Standard" orders (69.0%) — suggesting the expedite process itself is not functioning as intended.

---

## Project Structure

```
Supply-Chain-Project/
├── data/           4 CSV files + SQLite database (60,000 orders)
├── sql/            5 documented SQL queries with findings
├── python/         Data exploration, EDA, and chart generation
├── charts/         Matplotlib visualizations (PNG)
├── docs/           Dashboard export (PDF) and this README
└── Supply_Chain_Dashboard.pbix   Interactive Power BI dashboard
```

## Approach

**1. Data** — Synthetic dataset modeled on real supply chain operations: orders, suppliers (with reliability tiers), warehouses, and products across 6 categories.

**2. Python (EDA)** — Loaded and explored the data with Pandas; calculated on-time/delay rates; broke performance down by supplier, tier, region, and priority to isolate the driver.

**3. SQL** — Rebuilt the same analysis as JOIN-based queries against a relational schema, including OTIF calculation, supplier scorecards, and category-level risk exposure.

**4. Power BI** — Built an executive dashboard with KPI cards, root-cause charts, and a revenue-risk breakdown, styled for stakeholder presentation.

---

## Dashboard Preview

See `docs/dashboard.pdf` for the full interactive Power BI report, or open `Supply_Chain_Dashboard.pbix` directly in Power BI Desktop.

---

## Author

Sarika Bhukya
[LinkedIn](https://www.linkedin.com/in/bhukya-sarika-06265a327) · [GitHub](https://github.com/sarika9959)
