---
case: 03_bangkok_eto_rice
title: "FAO-56 reference ET₀ and rice crop water requirement, Bangkok"
aquascope_version: "0.4.0"
showcases:
  - penman_monteith_eto
  - crop_water_requirement
  - soil_water_balance
data_source: "FAO-56 Example 18 (Allen et al. 1998) hardcoded inputs, plus live daily weather from Open-Meteo Historical Weather API for Bangkok"
runtime_minutes: 1
created: 2026-05-23
---

# FAO-56 reference ET₀ and rice crop water requirement, Bangkok

## The scenario

Bangkok sits in the Chao Phraya delta, the rice bowl of Thailand. Paddy rice consumes roughly 800 to 1,500 mm of water per cropping cycle, most of it lost to evapotranspiration. FAO Irrigation & Drainage Paper No. 56 (Allen et al., 1998), the international standard for reference ET, actually uses Bangkok as Example 18 in Annex 6 to walk through the daily Penman-Monteith calculation. This case does two things: first it reproduces that textbook example exactly (a deterministic numerical check), then it scales up to a full wet-season rice scenario using real daily weather pulled from the Open-Meteo historical API.

## What this proves about AquaScope

- `penman_monteith_daily(...)`: full FAO-56 Eq. 6 in one call. Six daily weather inputs plus location and day of year, returns ET₀ in mm/day. Matches FAO-56 Example 18 to within textbook tolerance.
- `crop_water_requirement(eto_series, crop="rice_paddy", ...)`: applies the FAO-56 Kc curve (initial, development, mid, late) across the 120-day rice cycle and returns a daily ETc series.
- `SoilWaterBalance(...).auto_irrigate(...)`: runs the daily water balance with automatic irrigation triggers, accounts for rainfall and irrigation efficiency, and reports seasonal irrigation depth and stress days.

## How to run

```bash
pip install -r requirements.txt
jupyter notebook notebook.ipynb
```

Runtime on a cold cache is about a minute. Open-Meteo is fast and needs no API key.

## Outputs

See `outputs/`:

- `bangkok_weather.csv`: cached daily weather (Tmin, Tmax, RHmin, RHmax, wind, Rs, precip) from Open-Meteo for the wet-season window.
- `daily_eto.csv`: Penman-Monteith ET₀ time series for the season.
- `crop_water_balance.csv`: daily Kc, ETc, precipitation, soil moisture, and irrigation events.
- `eto_seasonal.png`: daily ET₀ over the rice season with Kc and ETc overlaid.
- `water_balance.png`: soil-moisture trajectory with irrigation events and deficit periods marked.

## Validation

**Reference:** FAO Irrigation & Drainage Paper No. 56, *Crop Evapotranspiration: Guidelines for Computing Crop Water Requirements* (Allen, Pereira, Raes & Smith, 1998, ISBN 92-5-104219-5), Annex 6 Example 18 for Bangkok, Thailand. Inputs: T_min = 25.6 °C, T_max = 34.8 °C, RH_min = 63 %, RH_max = 84 %, u₂ = 2.0 m/s, R_s = 22.0 MJ/m²/day, latitude = 13.73 °N, elevation = 2 m, DOY = 274 (1 October). Reported ET₀ is about 5.0 mm/day.

The case passes if all three checks below are PASS:

1. FAO-56 Example 18 reproduction: `penman_monteith_daily(...)` on the textbook inputs returns ET₀ within ±0.5 mm/day of the published 5.0 mm/day (this is the tolerance used in the AquaScope test suite, see `tests/test_agri/test_agri.py::test_fao56_example18`).
2. Wet-season mean ET₀ from live Open-Meteo data falls in the FAO CLIMWAT/CROPWAT range of 3.5 to 5.5 mm/day for Bangkok station ([www.fao.org/land-water/databases-and-software/climwat-for-cropwat](https://www.fao.org/land-water/databases-and-software/climwat-for-cropwat/en/)).
3. Seasonal ETc over the 120-day rice cycle falls in the published 600 to 1,200 mm range (FAO-56 Table 22 for rice in tropical climates; Tabbal et al. 2002 *Agric. Water Manage.* 56, 93-112 for Asian paddy systems).

Run the notebook to see the actual numbers and PASS/FAIL summary in the final cell.
