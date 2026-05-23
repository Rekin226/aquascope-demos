<div align="center">

# AquaScope demo cases

**Real-world hydrology use cases built with [AquaScope](https://github.com/Rekin226/aquascope).**
Self-contained, reproducible Jupyter notebooks on real data — every headline result checked against a published reference.

[![Main project](https://img.shields.io/badge/main%20project-AquaScope-1f77b4)](https://github.com/Rekin226/aquascope)
[![PyPI](https://img.shields.io/pypi/v/aquascope.svg?color=blue)](https://pypi.org/project/aquascope/)
[![Python](https://img.shields.io/badge/python-%E2%89%A53.10-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](#license)

</div>

---

## Cases

| #  | Title                                                                                  | Data                                                | Methods                                          | Validated against                                              |
|----|----------------------------------------------------------------------------------------|-----------------------------------------------------|--------------------------------------------------|----------------------------------------------------------------|
| 01 | [Bulletin 17C flood frequency — Potomac at Little Falls](01_potomac_flood_frequency/)  | USGS gauge 01646500 · 1931–2025 · n = 80            | LP3 · GEV (L-moments) · Q-Q & P-P                | FEMA DC FIS (2010) Table 4 — within ±10 %                      |
| 02 | [Baseflow & hydrological signatures — French Broad at Asheville](02_french_broad_baseflow/) | USGS gauge 03451500 · 1995–2025 daily                | Lyne-Hollick + Eckhardt filters · 22 signatures | Wolock (2003) USGS OFR 03-263; Santhi et al. (2008) JoH        |
| 03 | [FAO-56 ET₀ and rice crop water — Bangkok](03_bangkok_eto_rice/)                       | FAO-56 Example 18 + Open-Meteo daily, 2024 wet season | Penman-Monteith · Kc curves · soil water balance | FAO-56 Example 18 (5.0 mm/day) and CLIMWAT Bangkok climatic norms |
| 04 | [Mann-Kendall trend & Pettitt change-point — Red River at Grand Forks](04_red_river_trend/) | USGS gauge 05082500 · annual peaks 1882–2025         | Mann-Kendall · Sen's slope · Pettitt · PELT     | Ryberg et al. (2014) J. Hydrol. Eng.; Vecchia (2008) USGS SIR  |
| 05 | [Bivariate flood copula — Potomac peak/volume](05_potomac_copula/)                     | USGS gauge 01646500 · daily 1950–2025                | Gaussian/Clayton/Gumbel/Frank · joint return periods | Salvadori & De Michele (2004) WRR; Genest & Favre (2007) JHE  |

Every case fetches its own data at run time, runs the analysis end-to-end, generates the committed plots in `outputs/`, and prints a side-by-side comparison against the published reference.

---

## Quick start

### 1. Install AquaScope

AquaScope is the engine behind every case. Install it from PyPI:

```bash
pip install aquascope            # core — collectors + hydrology
pip install "aquascope[viz]"     # add matplotlib, seaborn, folium (used by the demos)
pip install "aquascope[all]"     # full stack — ML, viz, spatial, dashboard
```

For the complete feature list, documentation, and roadmap, see the [main AquaScope repository](https://github.com/Rekin226/aquascope).

### 2. Run a case

Each case folder pins its exact dependencies (AquaScope version + extras) in `requirements.txt`, so cases stay reproducible as the library evolves:

```bash
cd 01_potomac_flood_frequency                # pick a case
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt              # installs the pinned aquascope[viz] + case extras
jupyter notebook notebook.ipynb
```

> **Python.** AquaScope requires Python ≥ 3.10. On Python 3.14+ some scientific wheels may not yet be published; if installation is slow or fails, fall back to Python 3.13.

### 3. Read without running

GitHub renders `.ipynb` files natively. Open any case folder, click `notebook.ipynb`, and the full analysis — code, prose, plots, verified results — appears inline.

---

## Anatomy of a case

```
NN_<slug>/
├── README.md           ← scenario, methods, verified results
├── notebook.ipynb      ← the runnable analysis end-to-end
├── requirements.txt    ← pinned dependencies
├── data/               ← static inputs or a fetch script for live data
└── outputs/            ← generated artifacts — CSV tables, PNG figures
```

---

## License

Code: **MIT** — same licence as [AquaScope](https://github.com/Rekin226/aquascope/blob/main/LICENSE).

Data referenced by these notebooks is fetched from public-domain U.S. federal sources (USGS NWIS) under the [USGS data policy](https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits).

---

## Citation

If a case here informs your published research, please cite AquaScope itself — the canonical BibTeX entry lives in the [Citation section of the main repository](https://github.com/Rekin226/aquascope#-citation).
