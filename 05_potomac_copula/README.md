---
case: 05_potomac_copula
title: "Bivariate flood copula, Potomac peak vs 30-day volume"
aquascope_version: "0.4.0"
showcases:
  - copula_family_selection
  - kendall_spearman_dependence
  - joint_return_period
data_source: "USGS NWIS, gauge 01646500 (Potomac River near Washington, DC) via `dataretrieval`"
runtime_minutes: 2
created: 2026-05-23
---

# Bivariate flood copula, joint peak and volume on the Potomac

## The scenario

A flood is more than a peak. Levee overtopping, reservoir storage, and floodplain inundation depend on flood volume just as much as on the peak discharge. Designing only for the 100-year peak underestimates risk when peaks and volumes are positively dependent, which is the classical motivation for bivariate flood frequency analysis with copulas (Salvadori & De Michele 2004, *WRR*; Genest & Favre 2007).

This case pulls 75 years of daily mean discharge at USGS gauge **01646500** (Potomac at Little Falls, the same gauge as Case 01 to keep the data download light), extracts the annual peak and the annual 30-day maximum volume (a proxy for spring-freshet duration), fits all four copula families AquaScope supports, picks the best by AIC, and reports joint return periods for design-flood scenarios.

## What this proves about AquaScope

- `fit_copula(family="auto")`: fits Gaussian, Clayton, Gumbel, and Frank, returns the best by AIC in one call.
- `fit_copula(family=...)`: individual fits exposing θ, Kendall τ, Spearman ρ, AIC, log-likelihood.
- `joint_exceedance_probability(...)`: joint AND/OR exceedance probabilities and return periods, e.g. P(Q_peak > q₁ AND V_30 > v₁).
- `tail_dependence(copula)`: upper- and lower-tail dependence coefficients λ_U, λ_L for the selected copula. Gumbel implies upper-tail dependence (extreme peaks tend to coincide with extreme volumes), Gaussian is asymptotically independent.

## How to run

```bash
pip install -r requirements.txt
jupyter notebook notebook.ipynb
```

Runtime on a cold cache is about 2 minutes, dominated by the USGS daily fetch.

## Outputs

See `outputs/`:

- `daily_discharge.csv`: cleaned daily mean discharge for gauge 01646500.
- `peak_volume_pairs.csv`: annual (peak cfs, 30-day volume cfs-day) pairs.
- `copula_comparison.csv`: AIC ranking of the four families with θ, τ, ρ, log-likelihood.
- `joint_return_periods.csv`: joint return-period table for combinations of peak and volume thresholds.
- `copula_scatter.png`: peak vs 30-day volume on pseudo-observation (u, v) coordinates with the best-fit copula density contours.
- `family_aic_bars.png`: AIC bar chart across the four families.

## Validation

**References:**

- Salvadori, G. & De Michele, C. (2004). *Frequency analysis via copulas: theoretical aspects and applications to hydrological events.* **Water Resour. Res.** 40, W12511. doi:[10.1029/2004WR003133](https://doi.org/10.1029/2004WR003133)
- Genest, C. & Favre, A.-C. (2007). *Everything you always wanted to know about copula modeling but were afraid to ask.* **J. Hydrol. Eng.** 12, 347-368. doi:[10.1061/(ASCE)1084-0699(2007)12:4(347)](https://doi.org/10.1061/(ASCE)1084-0699(2007)12:4(347))
- Zhang, L. & Singh, V.P. (2006). *Bivariate flood frequency analysis using the copula method.* **J. Hydrol. Eng.** 11, 150-164.

These studies report:

1. Strong positive dependence between annual flood peak and flood volume in temperate humid catchments, typically Kendall's τ in the range 0.4 to 0.8.
2. Gumbel-family copulas (which have upper-tail dependence) are often selected as best fits for peak/volume pairs because both variables tend to reach their extremes during the same storm or freshet (Genest & Favre 2007 §6; Zhang & Singh 2006 Table 4).

The case passes if all four checks below are PASS:

1. Kendall τ > 0.30 and Spearman ρ > 0.30 (strong positive dependence).
2. At least one of Gumbel or Clayton beats the Gaussian on AIC, consistent with upper-tail dependence in extreme floods.
3. The best-fit family is one of Gumbel, Clayton, or Gaussian (Frank is symmetric with no tail dependence and rarely fits peak/volume pairs).
4. The joint 100-year AND return period is strictly greater than 100 years. When X and Y are positively dependent but not perfectly so, the joint return period for both variables at their 100-year marginal thresholds has to exceed 100 years (sanity check on `joint_exceedance_probability`).

Run the notebook to see the actual numbers and PASS/FAIL summary in the final cell.
