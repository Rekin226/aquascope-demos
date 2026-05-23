# Data

Daily discharge is fetched live from USGS NWIS by `notebook.ipynb` — there is no static CSV input. The notebook caches its fetch to `daily_discharge.csv` in `../outputs/` for provenance.

| File | Source | Last fetched | Notes |
|------|--------|--------------|-------|
| (none committed) | https://waterdata.usgs.gov/nwis/dv?site_no=03451500 | runtime | Daily mean discharge (parameter 00060), gauge 03451500 (French Broad River at Asheville), fetched via `dataretrieval`. |

If USGS NWIS is unreachable at run time, the notebook falls back to `../outputs/daily_discharge.csv` if present.
