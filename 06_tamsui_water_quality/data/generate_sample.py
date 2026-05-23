"""Generate a small synthetic Tamsui-like water quality dataset.

Used as a fallback when the Taiwan MOENV API is unreachable or rate-limited.
Values are not real measurements. They are drawn from published ranges in
Chen & Liu (2003) Environ. Monit. Assess. 86 and Liu et al. (2019) Water 11.
Layout matches what TaiwanMOENVCollector produces, so the notebook code path
is identical for live and synthetic input.

Usage:
    python data/generate_sample.py    # writes data/sample_tamsui_wq.csv
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

OUTPUT = Path(__file__).parent / "sample_tamsui_wq.csv"


# Stations from upstream tributaries to estuary. Coordinates approximate.
# Mean parameter levels increase with urbanisation downstream, except DO
# which decreases. Liu et al. (2019) report an improving DO trend at
# downstream stations through the 2000s and 2010s, encoded here as a
# small positive linear drift on DO at the two estuary-adjacent stations.
STATIONS = [
    # (station_id, en_name, zh_name, river, lat, lon,
    #  DO_mean, BOD5_mean, SS_mean, NH3N_mean, do_trend_per_year)
    ("01001", "Xindian River - Bitan",        "新店溪-碧潭",      "新店溪", 24.957, 121.539,  8.5, 0.8, 10.0, 0.15, 0.00),
    ("02001", "Dahan River - Shanchia",       "大漢溪-山佳",      "大漢溪", 24.965, 121.404,  8.0, 1.2, 15.0, 0.25, 0.00),
    ("03001", "Xindian River - Xiulang Br.",  "新店溪-秀朗橋",    "新店溪", 25.001, 121.511,  6.5, 3.2, 28.0, 0.85, 0.03),
    ("04001", "Tamsui River - Zhongxing Br.", "淡水河-中興橋",    "淡水河", 25.063, 121.508,  4.0, 6.0, 45.0, 2.30, 0.05),
    ("05001", "Tamsui River - Guandu Br.",    "淡水河-關渡橋",    "淡水河", 25.115, 121.459,  5.0, 4.0, 40.0, 1.50, 0.06),
    ("06001", "Tamsui River - Estuary",       "淡水河-河口",      "淡水河", 25.182, 121.413,  6.0, 2.5, 35.0, 0.90, 0.04),
]


def generate(seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    # Monthly sampling, 2018-01 through 2024-12 (84 dates per station)
    dates = pd.date_range("2018-01-15", "2024-12-15", freq="MS") + pd.Timedelta(days=14)

    for (sid, en, zh, river, lat, lon,
         do_mu, bod_mu, ss_mu, nh_mu, do_trend) in STATIONS:
        for d in dates:
            years_since_start = (d - dates[0]).days / 365.25
            # Seasonal modulation: wet season (Jun-Sep) brings more SS, lower DO,
            # higher loadings due to runoff.
            season = np.sin(2 * np.pi * (d.month - 4) / 12)  # peaks in Aug
            do_val = max(0.2, rng.normal(do_mu + do_trend * years_since_start - 0.6 * season, 0.6))
            bod_val = max(0.1, rng.normal(bod_mu * (1 + 0.20 * season), max(0.2, 0.18 * bod_mu)))
            ss_val = max(1.0, rng.normal(ss_mu * (1 + 0.45 * max(0, season)), max(2.0, 0.25 * ss_mu)))
            nh_val = max(0.02, rng.normal(nh_mu * (1 + 0.10 * season), max(0.05, 0.20 * nh_mu)))

            for param, value, unit in [
                ("DO", do_val, "mg/L"),
                ("BOD5", bod_val, "mg/L"),
                ("SS", ss_val, "mg/L"),
                ("NH3-N", nh_val, "mg/L"),
            ]:
                rows.append({
                    "station_id": sid,
                    "station_name": en,
                    "sample_datetime": d.isoformat(),
                    "parameter": param,
                    "value": round(value, 3),
                    "unit": unit,
                    "basin": "淡水河",
                    "river": river,
                    "county": "New Taipei / Taipei",
                    "latitude": lat,
                    "longitude": lon,
                })

    df = pd.DataFrame(rows)
    return df


if __name__ == "__main__":
    df = generate()
    df.to_csv(OUTPUT, index=False)
    print(f"Wrote {len(df):,} rows across {df['station_id'].nunique()} stations to {OUTPUT}")
