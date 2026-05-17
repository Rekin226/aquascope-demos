# Data

The annual-peak series is fetched live from USGS NWIS by `notebook.ipynb` — there is no static CSV input. The notebook caches its fetch to `annual_peaks.csv` in `../outputs/` for provenance.

| File | Source | Last fetched | Notes |
|------|--------|--------------|-------|
| (none committed) | https://nwis.waterdata.usgs.gov/nwis/peak?site_no=01646500 | runtime | Annual peak streamflow series, gauge 01646500 (Potomac River at Little Falls), fetched via `aquascope.collectors.usgs`. |

If USGS NWIS is unreachable at run time, the notebook falls back to `../outputs/annual_peaks.csv` if present.
