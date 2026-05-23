# Data

Daily mean discharge is fetched live from USGS NWIS by `notebook.ipynb` — there is no static CSV input. The notebook caches its fetch to `daily_discharge.csv` in `../outputs/`.

| File | Source | Last fetched | Notes |
|------|--------|--------------|-------|
| (none committed) | https://waterdata.usgs.gov/nwis/dv?site_no=01646500 | runtime | Daily mean discharge (parameter 00060), gauge 01646500 (Potomac River at Little Falls), fetched via `dataretrieval`. ~75 years of daily values. |

The annual peak / 30-day volume pairs derived from the daily series are written to `../outputs/peak_volume_pairs.csv`.

If USGS NWIS is unreachable at run time, the notebook falls back to `../outputs/daily_discharge.csv` if present.
