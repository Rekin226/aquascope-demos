---
case: NN_<slug>
title: "<one-line human-readable title>"
aquascope_version: "0.4.0"
showcases:                  # which aquascope features this case proves
  - <feature_x>
  - <feature_y>
data_source: "<dataset name + URL or DOI>"
runtime_minutes: 0          # cold-cache wall clock, fill once notebook runs end-to-end
created: YYYY-MM-DD
---

# <Title from frontmatter>

## The scenario

2-3 sentences. Real problem, real location, real data. Why a hydrologist or water-resources engineer would care.

## What this proves about AquaScope

Bullet list mapping to the `showcases:` frontmatter field.

- **`<feature_x>`** — what the notebook demonstrates about it (e.g., "FAO-56 reference ET computed in 8 lines from raw weather data").
- **`<feature_y>`** — ...

## How to run

```bash
pip install -r requirements.txt
jupyter notebook notebook.ipynb
```

Runtime on a cold cache: ~`runtime_minutes` (see frontmatter).

## Outputs

See `outputs/` for the generated artifacts:

- `<output_file_1>` — what it is in one line.
- `<output_file_2>` — ...

## Validation

How the headline result is checked against a published reference (e.g., a regulatory report, a peer-reviewed value, a benchmark dataset). Cite the source and the page or table number.
