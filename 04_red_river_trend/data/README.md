# Data

The annual peak series is fetched live from USGS NWIS by `notebook.ipynb` — there is no static CSV input. The notebook caches its fetch to `annual_peaks.csv` in `../outputs/`.

| File | Source | Last fetched | Notes |
|------|--------|--------------|-------|
| (none committed) | https://nwis.waterdata.usgs.gov/nwis/peak?site_no=05082500 | runtime | Annual peak streamflow, gauge 05082500 (Red River of the North at Grand Forks, ND), fetched via `dataretrieval`. |

If USGS NWIS is unreachable at run time, the notebook falls back to `../outputs/annual_peaks.csv` if present.
