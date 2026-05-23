---
case: 04_red_river_trend
title: "Mann-Kendall trend and Pettitt change-point, Red River at Grand Forks"
aquascope_version: "0.4.0"
showcases:
  - mann_kendall_trend
  - sens_slope
  - pettitt_changepoint
data_source: "USGS NWIS, gauge 05082500 (Red River of the North at Grand Forks, ND) via `dataretrieval`"
runtime_minutes: 1
created: 2026-05-23
---

# Mann-Kendall trend and Pettitt change-point on the Red River at Grand Forks

## The scenario

USGS gauge **05082500** on the Red River of the North at Grand Forks, ND has annual peak flows going back to 1882, one of the longest peak records in the U.S. interior. The basin covers about 30,000 mi² across the northern prairie pothole region, and the April 1997 flood (137,000 cfs at this gauge) destroyed large parts of Grand Forks and East Grand Forks. Several peer-reviewed studies (Wiche 1992, Macek-Rowland 2007, Ryberg et al. 2014) have documented a statistically significant increasing trend in Red River peaks since the late 19th century, with a clear regime shift somewhere in the mid-20th century. This case picks that up using non-parametric tests.

The notebook pulls the full annual peak series, runs a Mann-Kendall trend test (Mann 1945, Kendall 1948) with Sen's slope (1968), then runs a Pettitt (1979) change-point test to locate the regime shift. It cross-checks the result with PELT for multiple change-points, and finally compares the headline numbers to the published literature.

## What this proves about AquaScope

- `pymannkendall.original_test` (used by AquaScope's trend-analysis pipeline): returns Kendall τ, Z, p-value, and Sen's slope for a single time series. The non-parametric trend test of record for hydrology.
- `detect_changepoints(method="pettitt")`: non-parametric single change-point detector, standard companion to MK. Returns the most likely change year and its p-value.
- `detect_changepoints(method="pelt")`: PELT segmentation for cross-check. Useful when you suspect more than one regime shift.

## How to run

```bash
pip install -r requirements.txt
jupyter notebook notebook.ipynb
```

Runtime on a cold cache is about a minute (USGS fetch is ~10 s, the tests are fast, plotting is cheap).

## Outputs

See `outputs/`:

- `annual_peaks.csv`: cleaned annual peak series from USGS NWIS, full record.
- `trend_summary.csv`: one-row summary with τ, Z, p-value, Sen's slope, intercept, change-point year and its p-value.
- `trend_plot.png`: annual peaks with Sen's slope and Pettitt change-point marker, pre/post means annotated.
- `changepoint_plot.png`: Pettitt U_k statistic vs year.

## Validation

**References:**

- Ryberg, K.R., Lin, W., Vecchia, A.V. (2014). *Impact of climate variability on runoff in the north-central United States.* **J. Hydrol. Eng.** 19, 148-158. doi:[10.1061/(ASCE)HE.1943-5584.0000775](https://doi.org/10.1061/(ASCE)HE.1943-5584.0000775)
- Macek-Rowland, K.M. & Burr, J.J. (2007). *Flood frequency for selected streams in North Dakota.* **USGS Scientific Investigations Report 2007-5022**. ([pubs.usgs.gov/sir/2007/5022](https://pubs.usgs.gov/sir/2007/5022/))
- Wiche, G.J. (1992). *Streamflow variability of the Red River of the North.* **USGS Water-Supply Paper 2375**.

These studies all report a statistically significant (α < 0.05) increasing trend in Red River peak flows over the 20th-century record. Vecchia (2008) and Ryberg et al. (2014) place the regime shift somewhere in the early-to-mid 1940s, tied to changes in winter precipitation and snowmelt timing.

The case passes if all four checks below are PASS:

1. MK trend is significant (p < 0.05) and increasing (τ > 0).
2. Sen's slope is positive (cfs/year).
3. Pettitt detects a single change-point at p < 0.05.
4. The change-point year falls between 1930 and 1960, bracketing the regime shift in Ryberg et al. 2014 and Vecchia 2008.

Run the notebook to see the actual numbers and PASS/FAIL summary in the final cell.
