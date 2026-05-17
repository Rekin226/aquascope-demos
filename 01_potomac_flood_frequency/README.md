---
case: 01_potomac_flood_frequency
title: "Bulletin 17C flood frequency on the Potomac at Little Falls"
aquascope_version: "0.4.0"
showcases:
  - flood_analysis_lp3
  - flood_analysis_gev_lmoments
  - qq_diagnostics
data_source: "USGS NWIS, gauge 01646500 (Potomac River near Washington, DC, Little Falls Pump Station) via `dataretrieval`"
runtime_minutes: 1
created: 2026-05-17
---

# Bulletin 17C flood frequency on the Potomac at Little Falls

## The scenario

USGS gauge **01646500** (Potomac River near Washington, DC, at the Little Falls Pump Station) has one of the longest continuous peak-flow records in the eastern United States — annual peaks back to **1930**, including the historic March 1936 flood (~484,000 cfs). This makes it a textbook reference site for **Bulletin 17C flood frequency analysis**, the federal standard used by FEMA, USACE, and state DOTs to set design floods for bridges, levees, and floodplain maps.

This case fits a **Log-Pearson Type III (LP3)** distribution to the annual peak series and a **GEV** for comparison, reports 10 / 50 / 100 / 500-year flood estimates with bootstrap confidence intervals, and validates against published Bulletin 17B/17C estimates for the same gauge.

## What this proves about AquaScope

- **`flood_analysis(method="lp3")`** — runs the federal-standard LP3 fit (method-of-moments + weighted regional skew per Bulletin 17C §5.2.4) and returns return-period estimates with variance-of-estimate CIs.
- **`flood_analysis(method="gev_lmoments")`** — fits the GEV alternative via L-moments; the same call signature. L-moments are the standard estimator for GEV on annual maxima — far more robust than scipy MLE on records with historical outliers (e.g. the 1936 peak).
- **Q-Q and P-P diagnostics** — assembled directly from `FloodFreqResult.params` and `annual_max`; the plots reviewers expect on any flood-frequency paper.

Data is fetched via the `dataretrieval` package (USGS's official Python client) since AquaScope's `USGSCollector` targets the new OGC API which does not yet expose historical annual peaks.

## Verified results

Run on 2026-05-17, n = 80 annual peaks (1931–2025):

| Return period | LP3 (Bulletin 17C) | LP3 90 % CI       | GEV (L-moments) |
|---------------|--------------------|-------------------|-----------------|
| 10 yr         | 236,820 cfs        | [207k, 271k]      | 247,066 cfs     |
| 50 yr         | 374,509 cfs        | [312k, 449k]      | 284,952 cfs     |
| **100 yr**    | **443,154 cfs**    | **[363k, 542k]**  | 297,433 cfs     |
| 500 yr        | 629,636 cfs        | [494k, 803k]      | 320,175 cfs     |

The 1936 St. Patrick's Day flood (484,000 cfs) sits within the LP3 100-year 90 % CI — consistent with the historic event being approximately a 100-year flood.

## How to run

```bash
pip install -r requirements.txt
jupyter notebook notebook.ipynb
```

Runtime on a cold cache: ~3 min (USGS fetch ~5 s + analysis + plots).

## Outputs

See `outputs/`:

- `flood_frequency_curve.png` — return level vs. return period, LP3 with 90 % CI band, GEV overlaid.
- `qq_diagnostic.png` — Q-Q and probability plots for the LP3 fit.
- `return_periods.csv` — numeric table: return period, LP3 estimate, GEV estimate, lower/upper CI for each.
- `annual_peaks.csv` — the cleaned annual-peak series fetched from USGS NWIS (provenance-traceable).

## Validation

**Reference:** FEMA Flood Insurance Study, District of Columbia, Washington D.C., FIS Number 110001V000A, revised 2010-09-27 ([msc.fema.gov FIS](https://map1.msc.fema.gov/data/11/S/PDF/110001V000A.pdf) · also at [ncpc.gov](https://www.ncpc.gov/docs/DC_Flood_Insurance_Study_Pre-17th_Street_Levee.pdf)), **Table 4 page 15** — the 2005 USACE Bulletin 17B/LP3 update of the effective 1985 hydrology for gauge 01646500.

The FIS used Bulletin 17B / HEC-FFA with data through 2003 (~73 annual peaks plus the 1889 historical peak), station skew 0.3, no regional weighting. Our analysis extends the record through 2025 (80 annual peaks) and uses Bulletin 17C-style weighted regional skew (0.4). The case is considered correct if every return period (10, 50, 100, 500 yr) falls within ±10 % of the FIS value.

| Return period | LP3 here (1931–2025) | FIS 2010 (1931–2003) | Δ %    | Within ±10 % |
|---------------|----------------------|----------------------|--------|--------------|
| 10 yr         | 236,820 cfs          | 240,000 cfs          | -1.3 % | ✅           |
| 50 yr         | 374,509 cfs          | 395,000 cfs          | -5.2 % | ✅           |
| **100 yr**    | **443,154 cfs**      | **475,000 cfs**      | **-6.7 %** | ✅       |
| 500 yr        | 629,636 cfs          | 698,000 cfs          | -9.8 % | ✅           |

**Overall: PASS.** The small systematic underestimate at long return periods is expected — the FIS censors the 1889 historical peak into the analysis (raising the upper tail), while our run uses only the 1931–2025 systematic record with weighted regional skew.
