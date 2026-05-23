# Data

River water quality samples come from the Taiwan Ministry of Environment (MOENV) open data portal at run time. No static input file is required.

| File | Source | Notes |
|------|--------|-------|
| (none committed) | [data.moenv.gov.tw](https://data.moenv.gov.tw), dataset `AQX_P_07` | River water quality monitoring. Pulled via `TaiwanMOENVCollector`. Sampling parameters include DO, BOD5, COD, SS, NH3-N, TP, pH, conductivity, temperature, E. coli. |

The MOENV API works without a key under a rate limit. For higher throughput, request a free key at [data.moenv.gov.tw/en/apikey](https://data.moenv.gov.tw/en/apikey) and set `MOENV_API_KEY` in your environment before running the notebook.

If MOENV is unreachable at run time, the notebook falls back to `../outputs/tamsui_samples.csv` if a previous successful run cached it there.
