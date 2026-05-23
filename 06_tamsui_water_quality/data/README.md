# Data

The notebook reads its data from one of two places, in order:

1. **Live Taiwan MOENV API** (preferred). Dataset `AQX_P_07` at [data.moenv.gov.tw](https://data.moenv.gov.tw), pulled via `TaiwanMOENVCollector` and filtered to the Tamsui basin. Works without a key under a rate limit. For higher throughput, request a free key at [data.moenv.gov.tw/en/apikey](https://data.moenv.gov.tw/en/apikey) and set `MOENV_API_KEY` in your environment.

2. **Bundled synthetic fallback** (this folder). If MOENV is unreachable, rate-limited, or returns no Tamsui-basin records in the current snapshot, the notebook loads `sample_tamsui_wq.csv` so the rest of the analysis (AI recommender, RPI computation, MK trend, plots) still runs end-to-end.

| File | Contents |
|------|----------|
| `sample_tamsui_wq.csv` | 1,992 rows. 6 Tamsui basin stations spanning headwaters to estuary, monthly sampling 2018-01 through 2024-12, with DO/BOD5/SS/NH3-N at each station-date. Synthetic but realistic. Drawn from published ranges in Chen & Liu (2003) *Environ. Monit. Assess.* 86 and the recovery trend documented by Liu et al. (2019) *Water* 11. |
| `generate_sample.py` | Reproducible generator. Uses `np.random.default_rng(seed=42)`. Run `python data/generate_sample.py` to regenerate. |

The synthetic fallback is intentionally honest: it is labeled as such in the notebook printouts, and the schema matches what `TaiwanMOENVCollector` produces so downstream code is identical.
