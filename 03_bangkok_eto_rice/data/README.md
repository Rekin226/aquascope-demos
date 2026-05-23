# Data

Two data sources, both pulled at run time:

| File | Source | Notes |
|------|--------|-------|
| (hardcoded in notebook) | FAO-56 Annex 6, Example 18 (Allen et al. 1998) | Single-day inputs for Bangkok on DOY 274. Deterministic; used to verify Penman-Monteith implementation. |
| (none committed) | [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) | Daily Tmin / Tmax / RHmin / RHmax / wind / shortwave radiation / precipitation for Bangkok (13.7563 °N, 100.5018 °E) over the wet-season window. Free, no API key. |

If the Open-Meteo fetch fails, the notebook falls back to `../outputs/bangkok_weather.csv` if present.
