"""Generate a synthetic Bangkok wet-season weather dataset.

Used as a fallback when the Open-Meteo historical archive is unreachable.
Values follow published climatic norms for Bangkok during the rice growing
season (May to September) per FAO CLIMWAT and Allen et al. (1998) Annex 2.

Usage:
    python data/generate_sample.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

OUTPUT = Path(__file__).parent / "sample_bangkok_weather.csv"


def generate(seed: int = 42, start: str = "2024-05-15", days: int = 120) -> pd.DataFrame:
    """120-day rice cycle starting 2024-05-15, matching the notebook scenario."""
    rng = np.random.default_rng(seed)
    dates = pd.date_range(start, periods=days, freq="D")
    doy = dates.dayofyear

    # Bangkok wet-season climatology (May to Sep):
    # Tmin ~24-26C, Tmax ~32-34C, RH 70-90%, wind 1-3 m/s at 2m,
    # Rs 15-22 MJ/m²/day, precipitation episodic.
    t_min = 25.0 + 1.0 * np.sin(2 * np.pi * (doy - 100) / 365) + rng.normal(0, 0.7, days)
    t_max = 33.0 + 1.5 * np.sin(2 * np.pi * (doy - 100) / 365) + rng.normal(0, 1.0, days)
    rh_min = np.clip(rng.normal(65, 6, days), 45, 85)
    rh_max = np.clip(rng.normal(90, 4, days), 75, 99)
    # Wind at 10 m height (km/h) — converted to 2 m m/s in the notebook.
    u10_kmh = np.clip(rng.normal(9, 3, days), 2, 20)
    rs = np.clip(rng.normal(19.0, 3.0, days), 8, 28)
    # Wet-season rainfall — bimodal: dry-spell zeros + occasional heavy events.
    rain = np.where(rng.random(days) < 0.55, rng.gamma(1.5, 6.0, days), 0.0)

    df = pd.DataFrame(
        {
            "t_min": np.round(t_min, 2),
            "t_max": np.round(t_max, 2),
            "rh_min": np.round(rh_min, 1),
            "rh_max": np.round(rh_max, 1),
            "u10_max_kmh": np.round(u10_kmh, 2),
            "rs_mj_m2": np.round(rs, 2),
            "precip_mm": np.round(rain, 2),
        },
        index=dates,
    )
    df.index.name = "date"
    # u2 conversion (FAO-56 Eq. 47): u2 = u10 × 4.87 / ln(67.8 × 10 − 5.42)
    u10_ms = df["u10_max_kmh"] / 3.6
    df["u2_ms"] = np.round(u10_ms * 4.87 / np.log(67.8 * 10 - 5.42), 3)
    return df


if __name__ == "__main__":
    df = generate()
    df.to_csv(OUTPUT)
    print(f"Wrote {len(df)} days to {OUTPUT}")
