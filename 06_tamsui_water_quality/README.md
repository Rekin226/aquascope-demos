---
case: 06_tamsui_water_quality
title: "Taiwan River Pollution Index and trends, Tamsui River basin"
aquascope_version: "0.4.0"
showcases:
  - taiwan_moenv_collector
  - ai_methodology_recommender
  - taiwan_river_pollution_index
  - mann_kendall_water_quality_trend
data_source: "Taiwan Ministry of Environment (MOENV) open data portal, dataset AQX_P_07 (river water quality monitoring) via `TaiwanMOENVCollector`"
runtime_minutes: 2
created: 2026-05-23
---

# Taiwan River Pollution Index and trends, Tamsui River basin

## The scenario

The Tamsui River flows through Taipei, draining about 2,700 km² of the northern Taiwan watershed. In the 1980s it was one of the most polluted rivers in Asia. After three decades of sewer build-out, industrial regulation, and tributary cleanup under the Taiwan EPA's *Severely Polluted River Remediation Plan*, water quality has improved significantly. The Tamsui is the textbook case for tracking that recovery in Taiwan.

This case pulls river water quality data from the Taiwan Ministry of Environment (MOENV) open data portal (dataset AQX_P_07), filters to Tamsui basin stations, runs AquaScope's AI methodology recommender to suggest analyses, computes the official Taiwan River Pollution Index (RPI) for every station-date, and applies a Mann-Kendall trend test on dissolved oxygen at the longest-recorded station.

## What this proves about AquaScope

- `TaiwanMOENVCollector`: pages through the MOENV open data API, normalises records into the unified `WaterQualitySample` schema, maps Chinese parameter names to English (溶氧量 to DO, 生化需氧量 to BOD5, and so on). The same schema other AquaScope collectors use.
- `recommend(DatasetProfile(...))`: AI methodology recommender. Given dataset characteristics (parameters, station count, time span, research goal), it scores and ranks AquaScope's 26 catalogued methods.
- `run_wqi(...)`: the Taiwan River Pollution Index pipeline. Encodes the official 4-parameter scoring (DO, BOD5, SS, NH3-N) with thresholds 1/3/6/10 and four pollution categories.
- `pymannkendall` trend test on a per-station DO series: tracks long-term recovery.

## How to run

```bash
pip install -r requirements.txt
jupyter notebook notebook.ipynb
```

Runtime on a cold cache is about 2 minutes (MOENV pagination dominates).

The MOENV endpoint works without an API key under a rate limit. For unrestricted access, request a free key at [data.moenv.gov.tw/en/apikey](https://data.moenv.gov.tw/en/apikey) and set the environment variable `MOENV_API_KEY` before launching Jupyter.

## Outputs

See `outputs/`:

- `tamsui_samples.csv`: raw water quality samples for the Tamsui basin, cached for offline re-runs.
- `ai_recommendations.csv`: top-5 methodology recommendations with score and rationale.
- `rpi_by_station_date.csv`: RPI score and category per station-date.
- `rpi_distribution.png`: bar chart of the four pollution categories.
- `rpi_by_station.png`: mean RPI per station, ordered from upstream to estuary.
- `do_trend.png`: dissolved oxygen time series at the most-sampled station, with Sen's slope.

## Validation

**Reference:**

- Taiwan EPA, *Annual Report on Water Quality Monitoring* (MOENV, multiple years; methodology at [www.moenv.gov.tw](https://www.moenv.gov.tw)). The RPI is defined in MOENV environmental monitoring standards using the 4-parameter scoring encoded in `aquascope.pipelines.model_builder.run_wqi`.
- Chen, C.-N. & Liu, S.-W. (2003). *Assessment of pollution loadings in the Tamsui River basin.* **Environ. Monit. Assess.** 86, 153-179. doi:[10.1023/A:1024033728067](https://doi.org/10.1023/A:1024033728067). Establishes the upstream-to-estuary pollution gradient.
- Liu, W.-C., Hsu, M.-H., Wu, C.-R., et al. (2019). *Long-term water quality variation in Tamsui River, Taiwan.* **Water** 11, 1851. doi:[10.3390/w11091851](https://doi.org/10.3390/w11091851). Documents the improving DO trend at downstream stations during the post-2000 sewer build-out.

The case passes if all four checks below are PASS:

1. AI recommender returns at least one trend-detection methodology (Mann-Kendall, Sen's slope, STL, or similar) in the top-5 for a Tamsui water-quality profile.
2. RPI computation produces at least one record in each of the four official Taiwan EPA categories that actually appear in the sample (Non-polluted, Lightly polluted, Moderately polluted, Severely polluted), or at least two categories overall (the Tamsui basin spans a real pollution gradient, never single-category).
3. Mean RPI at upstream stations is lower (cleaner) than mean RPI at downstream stations, matching the published Tamsui spatial gradient (Chen & Liu 2003).
4. Mann-Kendall trend on DO at the most-sampled station is either non-significant (p ≥ 0.05) or shows an increasing trend (τ ≥ 0). A significant decreasing DO trend would contradict the documented recovery (Liu et al. 2019) and fail the check.

Run the notebook to see the actual numbers and PASS/FAIL summary in the final cell.
