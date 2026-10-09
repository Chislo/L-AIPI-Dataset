# Longitudinal AI Preparedness Index (L-AIPI, 2000–2023)

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.laipi-blue.svg)](https://doi.org)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Data Formats](https://img.shields.io/badge/Formats-CSV%20%7C%20Stata%20%7C%20Excel-green.svg)](#data-files)
[![Temporal Coverage](https://img.shields.io/badge/Coverage-2000--2023-orange.svg)](#dataset-coverage)
[![IMF Validation](https://img.shields.io/badge/IMF_Validation-r%3D0.912%20(p%3C0.001)-blueviolet.svg)](#validation-against-the-imf-benchmark)

The **Longitudinal AI Preparedness Index ($\text{L-AIPI}$)** is an open-access, multi-decade macro panel dataset tracking national artificial intelligence readiness across 2000–2023. Grounded in the multi-pillar conceptual framework of the International Monetary Fund (IMF) AI Preparedness Index (AIPI; Cazzaniga et al., 2024), $\text{L-AIPI}$ reconstructs continuous, time-varying readiness scores to enable longitudinal econometric estimation, dynamic panel modeling, and development policy analysis.

---

## Quick Start: 1-Line Data Loaders

You can load the $\text{L-AIPI}$ panel directly into your statistical software without manual downloading:

### Python (pandas)
```python
import pandas as pd

# Load the core developing economies estimation panel (149 economies, 2000-2023)
url = "https://raw.githubusercontent.com/Chislo/L-AIPI-Dataset/main/data/laipi_developing_panel_2000_2023.csv"
df = pd.read_csv(url)
print(df.head())
```

### Stata (14+)
```stata
* Load developing economies panel directly into Stata memory:
use "https://raw.githubusercontent.com/Chislo/L-AIPI-Dataset/main/data/laipi_developing_panel_2000_2023.dta", clear
describe
summarize laipi_composite pillar_digital_infra pillar_human_capital pillar_innovation
```

### R (tidyverse)
```r
library(tidyverse)

# Load global panel
url <- "https://raw.githubusercontent.com/Chislo/L-AIPI-Dataset/main/data/laipi_global_panel_2000_2023.csv"
df <- read_csv(url)
glimpse(df)
```

---

## Dataset Coverage & Structure

The repository provides two standardized panel datasets alongside a 2023 cross-sectional ranking table:

1. **`laipi_developing_panel_2000_2023`** (`.csv`, `.dta`, `.xlsx`):
   - **Sample:** 149 developing and emerging economies.
   - **Observations:** 3,512 balanced country-year observations.
   - **Contents:** Composite $\text{L-AIPI}$, 3 foundational pillars, real agricultural labor productivity, surface temperature anomalies, trade openness, and connectivity variables.
2. **`laipi_global_panel_2000_2023`** (`.csv`, `.dta`):
   - **Sample:** 240+ global economies and territories.
   - **Observations:** 6,960 country-year observations.
   - **Contents:** Full global coverage of $\text{L-AIPI}$ and individual pillars.
3. **`laipi_country_rankings_2023.csv`**:
   - Cross-sectional ranking of 213 economies in 2023 comparing $\text{L-AIPI}$ against the official IMF benchmark.

---

## Pillar Architecture & Formula

The Longitudinal AI Preparedness Index is computed as the balanced arithmetic mean of three normalized pillars:

$$\text{L-AIPI}_{i,t} = \frac{1}{3} \left( DI_{i,t} + HC_{i,t} + \text{INN}_{i,t} \right) \in [0, 1]$$

| Pillar | Underlying Indicators | Primary Source | Normalization |
| :--- | :--- | :--- | :--- |
| **Digital Infrastructure ($DI$)** | Internet users (% of population), mobile broadband, telecommunications networks | ITU / World Bank WDI | Scaled to $[0, 1]$ via $\text{InternetPct} / 100$ |
| **Human Capital ($HC$)** | Years of schooling, educational quality, workforce readiness | World Bank HCI / Penn World Table | Min-max scaled to $[0, 1]$ |
| **Innovation & Tech Capability ($\text{INN}$)** | R&D expenditure (% GDP), patent applications (residents), scientific journal articles, high-tech exports (% manufacturing) | World Bank WDI | Cross-panel $Z$-score aggregation, min-max scaled to $[0, 1]$ |

*Note on Regulation Pillar:* Baseline institutional and legal structures are captured via country fixed effects in dynamic panel econometrics, as standardized annual time series for AI-specific regulation are unavailable historically.

---

## Validation against the Official IMF Benchmark

To establish construct validity, the reconstructed $\text{L-AIPI}_{i,2023}$ values were evaluated against the official 2023 IMF AI Preparedness Index (AIPI; Cazzaniga et al., 2024) across 137 developing nations:

- **Pearson Correlation:** $r = 0.912$ ($p < 0.0001$)
- **Spearman Rank Correlation:** $\rho = 0.923$ ($p < 0.0001$)
- **Validation Fit:** $\text{Official\_AIPI}_i = 0.063 + 0.880 \times \text{L-AIPI}_{i,2023}$ ($R^2 = 0.832, \text{MAE} = 0.058$)

The index preserves cross-country rankings while providing a continuous multi-decade time dimension.

---

## Variable Codebook (Summary)

| Variable Name | Type | Description |
| :--- | :--- | :--- |
| `iso3` | String (3) | ISO 3166-1 alpha-3 country code |
| `country_name` | String | Standard country name |
| `region` | String | UN geographical region |
| `continent` | String | Continent |
| `year` | Integer | Observation year (2000–2023) |
| `laipi_composite` | Float $[0, 1]$ | Longitudinal AI Preparedness Index |
| `pillar_digital_infra` | Float $[0, 1]$ | Digital Infrastructure Pillar ($DI$) |
| `pillar_human_capital` | Float $[0, 1]$ | Human Capital Pillar ($HC$) |
| `pillar_innovation` | Float $[0, 1]$ | Innovation and Tech Capability Pillar ($\text{INN}$) |
| `agri_val_add_worker` | Float | Agricultural value added per worker (constant 2015 USD) |
| `temp_anomaly_c` | Float | Surface temperature anomaly ($^\circ\text{C}$, 1951–1980 baseline) |
| `trade_openness_gdp` | Float | Total trade as % of GDP |
| `imf_aipi_2023` | Float $[0, 1]$ | Official IMF AIPI benchmark score (2023) |

*For complete econometric notes, see [CODEBOOK.md](CODEBOOK.md).*

---

## How to Cite

If you use the $\text{L-AIPI}$ dataset in your research, please cite both the empirical paper and the dataset release:

### 1. Empirical Paper Citation
> Ubabukoh, C. L. (2026). *The AI Adaptation Capacity Paradox: Longitudinal AI Preparedness and Agricultural Climate Resilience in Developing Economies*. Under review at *Information Technology for Development*.

```bibtex
@article{ubabukoh2026laipi,
  author    = {Ubabukoh, Chisom L.},
  title     = {The AI Adaptation Capacity Paradox: Longitudinal AI Preparedness and Agricultural Climate Resilience in Developing Economies},
  journal   = {Information Technology for Development},
  year      = {2026},
  note      = {Under review}
}
```

### 2. Dataset Citation
> Ubabukoh, C. L. (2026). *Longitudinal AI Preparedness Index (L-AIPI) Dataset: 2000–2023* [Data set]. Zenodo. https://doi.org/10.5281/zenodo.laipi

```bibtex
@dataset{ubabukoh2026laipi_data,
  author    = {Ubabukoh, Chisom L.},
  title     = {Longitudinal AI Preparedness Index (L-AIPI) Dataset: 2000--2023},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.laipi},
  url       = {https://github.com/Chislo/L-AIPI-Dataset}
}
```

---

## License

This dataset is distributed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). You are free to share, copy, transform, and build upon this data for any purpose, including commercial applications, provided appropriate credit is given.
