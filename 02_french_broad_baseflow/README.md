---
case: 02_french_broad_baseflow
title: "Baseflow separation and hydrological signatures, French Broad at Asheville"
aquascope_version: "0.4.0"
showcases:
  - baseflow_lyne_hollick
  - baseflow_eckhardt
  - hydrological_signatures
data_source: "USGS NWIS, gauge 03451500 (French Broad River at Asheville, NC) via `dataretrieval`"
runtime_minutes: 2
created: 2026-05-23
---

# Baseflow separation and hydrological signatures, French Broad at Asheville

## The scenario

USGS gauge **03451500** sits on the French Broad River as it leaves Asheville, NC. The basin drains 945 mi² of the Blue Ridge: humid, forested, with thin soils over fractured crystalline bedrock. The daily discharge record goes back to 1895, making it one of the oldest continuous gauges east of the Mississippi. It shows up in the USGS *Hydrologic Atlas* as the canonical humid mountain catchment and it is part of the CAMELS large-sample dataset.

This case grabs 30 years of daily flow, runs two independent baseflow filters on it, and then computes the full set of 22 hydrological signatures (flow magnitude, variability, high and low flow regimes, flashiness, recession, seasonality).

## What this proves about AquaScope

- `baseflow_analysis(method="lyne_hollick")`: three-pass recursive filter with α = 0.925 per Nathan & McMahon (1990). Returns total, baseflow, and quickflow series plus the baseflow index (BFI).
- `baseflow_analysis(method="eckhardt")`: two-parameter filter (α = 0.98, BFI_max = 0.80 for perennial streams over porous aquifers) per Eckhardt (2005). It uses a different formulation, so agreement with Lyne-Hollick is a real cross-check.
- `compute_all_signatures()`: a single call returns 22 signatures (Q5, Q95, flashiness, baseflow index, high-flow frequency, recession constant, Markham seasonality, peak month, and the rest). Same metric set used in CAMELS-style comparative hydrology (Addor et al. 2017).

## How to run

```bash
pip install -r requirements.txt
jupyter notebook notebook.ipynb
```

Runtime on a cold cache: about 2 minutes (USGS fetch is ~10 s, the rest is filtering and plotting).

## Outputs

See `outputs/`:

- `daily_discharge.csv`: cleaned daily mean discharge from USGS NWIS, cached for offline re-runs.
- `baseflow_separation.png`: three-panel plot showing total flow with each baseflow estimator overlaid for a representative 3-year window.
- `baseflow_components.csv`: daily total, baseflow (LH), baseflow (Eckhardt), quickflow.
- `signatures.csv`: the 22 hydrological signatures, one row of values.
- `signatures_dashboard.png`: flow-duration curve plus a summary panel of the headline signatures.

## Validation

**References:** Wolock, D.M. (2003). *Base-flow index grid for the conterminous United States.* U.S. Geological Survey Open-File Report 03-263 ([pubs.usgs.gov/of/2003/ofr03263](https://pubs.usgs.gov/of/2003/ofr03263/)) for the PART-derived national BFI grid. Mau, D.P. & Winter, T.C. (1997). *Estimating ground-water recharge from streamflow hydrographs.* **Ground Water** 35, 291-304, and Eckhardt (2008) *Hydrol. Process.* 22, 1873-1882, doi:[10.1002/hyp.6772](https://doi.org/10.1002/hyp.6772) for digital-filter BFI ranges.

Important: digital-filter BFI (Lyne-Hollick, Eckhardt) is systematically higher than PART-derived BFI by 0.1 to 0.2 for the same basin (Eckhardt 2008, Table 1). Published values for humid forested Southern Appalachian basins:

- PART (Wolock 2003, Santhi et al. 2008): 0.45 to 0.65
- Digital filters (Mau & Winter 1997, Eckhardt 2008): 0.55 to 0.85

We test against the digital-filter range here because that is what the notebook computes.

The case passes if all four checks below are PASS:

1. Lyne-Hollick BFI between 0.55 and 0.85 (digital-filter range for humid Appalachian basins).
2. Eckhardt BFI also between 0.55 and 0.85 (independent filter agrees).
3. |BFI_LH − BFI_Eckhardt| < 0.10 (typical inter-method spread per Eckhardt 2008).
4. Flashiness index < 0.5 (Baker et al. 2004, *JAWRA* 40, 503-522, report 0.1-0.4 for humid forested Appalachian basins).

Run the notebook to see the actual numbers and PASS/FAIL summary in the final cell.
