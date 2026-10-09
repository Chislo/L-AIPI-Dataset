# Longitudinal AI Preparedness Index (L-AIPI): Technical Codebook & User Guide

**Version:** 1.0 (October 2026)  
**Principal Investigator:** Chisom L. Ubabukoh (O.P. Jindal Global University)  
**Permanent Repository:** Zenodo & Harvard Dataverse  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)  

---

## 1. Overview and Conceptual Framework

The Longitudinal AI Preparedness Index ($\text{L-AIPI}$) provides an annual, continuous macroeconomic measure of national readiness to adopt, integrate, and exploit artificial intelligence technologies. While the International Monetary Fund (IMF) published a foundational cross-sectional benchmark across 174 countries for the single year 2023 (Cazzaniga et al., 2024), dynamic macroeconomic modeling requires multi-decade panel series. 

$\text{L-AIPI}$ reconstructs this framework across **2000–2023** by tracking the three time-varying foundational dimensions of technological capacity:
1. **Digital Infrastructure ($DI$)**
2. **Human Capital and Labor Readiness ($HC$)**
3. **Innovation and Domestic Absorption Capability ($\text{INN}$)**

---

## 2. Mathematical Formulation and Normalization Protocols

The composite index is constructed as the unweighted arithmetic mean of the three normalized pillar scores:

$$\text{L-AIPI}_{i,t} = \frac{1}{3} \left( DI_{i,t} + HC_{i,t} + \text{INN}_{i,t} \right) \in [0, 1]$$

### Pillar 1: Digital Infrastructure ($DI_{i,t}$)
Measures telecommunications access, broadband density, and rural connectivity.
- **Underlying Indicator:** Individuals using the Internet as a percentage of population (`IT.NET.USER.ZS`).
- **Primary Source:** International Telecommunication Union (ITU) World Telecommunication/ICT Indicators Database and World Bank World Development Indicators (WDI).
- **Normalization:**
  $$DI_{i,t} = \min\left(1.0, \max\left(0.0, \frac{\text{InternetUsagePct}_{i,t}}{100}\right)\right)$$

### Pillar 2: Human Capital ($HC_{i,t}$)
Measures educational attainment, workforce skill endowments, and technological absorptive capacity.
- **Underlying Indicator:** World Bank Human Capital Index (HCI, database 63, series `HD.HCI.OVRL`). Historical trends are supplemented and interpolated using the Penn World Table (PWT 10.0) human capital index.
- **Normalization (Min-Max Scaling across full sample):**
  $$HC_{i,t} = \frac{\text{HCI}_{i,t} - \min(\text{HCI})}{\max(\text{HCI}) - \min(\text{HCI})} \in [0, 1]$$

### Pillar 3: Innovation and Technological Capability ($\text{INN}_{i,t}$)
Captures domestic scientific capacity, knowledge generation, and high-technology absorptive potential without circular dependency on trade policy indicators.
- **Underlying Indicators (World Bank WDI):**
  1. Research and development expenditure as a percentage of GDP (`GB.XPD.RSDV.GD.ZS`)
  2. Scientific and technical journal articles (`IP.JRN.ARTC.SC`)
  3. Patent applications by residents (`IP.PAT.RESD`)
  4. High-technology exports as a percentage of manufactured exports (`TX.VAL.TECH.MF.ZS`)
- **Aggregation Protocol:**
  Each indicator $k$ is standardized into panel-wide $Z$-scores:
  $$Z_{k,i,t} = \frac{X_{k,i,t} - \bar{X}_k}{\sigma_k}$$
  For each country-year, the raw innovation score $\bar{Z}_{i,t}$ is computed as the arithmetic mean of available standardized indicators.
- **Normalization:**
  $$\text{INN}_{i,t} = \frac{\bar{Z}_{i,t} - \min(\bar{Z})}{\max(\bar{Z}) - \min(\bar{Z})} \in [0, 1]$$

---

## 3. Data Dictionary

The standardized panel datasets contain the following 15 variables:

| Variable Name | Stata Type | Format | Units / Range | Description | Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `iso3` | `str3` | `%3s` | Text | ISO 3166-1 alpha-3 country code | Standardized |
| `country_name` | `str45` | `%45s` | Text | Standard country name | World Bank |
| `region` | `str30` | `%30s` | Text | UN geographical region | UN M49 |
| `continent` | `str20` | `%20s` | Text | Continent | UN / Coco |
| `year` | `int` | `%4.0f` | 2000–2023 | Observation year | Time |
| `laipi_composite` | `float` | `%9.4f` | $[0.000, 1.000]$ | Longitudinal AI Preparedness Index | Reconstructed composite |
| `pillar_digital_infra` | `float` | `%9.4f` | $[0.000, 1.000]$ | Digital Infrastructure Pillar ($DI$) | ITU / World Bank WDI |
| `pillar_human_capital` | `float` | `%9.4f` | $[0.000, 1.000]$ | Human Capital Pillar ($HC$) | World Bank HCI / PWT |
| `pillar_innovation` | `float` | `%9.4f` | $[0.000, 1.000]$ | Innovation & Tech Capability ($\text{INN}$) | World Bank WDI |
| `agri_val_add_worker` | `double`| `%12.2f` | Constant 2015 USD | Real agricultural value added per worker | World Bank WDI / FAOSTAT |
| `temp_anomaly_c` | `float` | `%9.3f` | $^\circ\text{C}$ | Annual surface temperature anomaly | NASA GISS / FAOSTAT |
| `trade_openness_gdp` | `float` | `%9.2f` | % of GDP | Total trade (exports + imports) / GDP | World Bank WDI |
| `internet_usage_pct` | `float` | `%9.2f` | % of population | Individuals using the Internet | World Bank / ITU |
| `human_capital_index` | `float` | `%9.3f` | Index $[0, 1]$ | Raw Human Capital Index | World Bank HCI |
| `imf_aipi_2023` | `float` | `%9.2f` | Index $[0, 1]$ | Official 2023 IMF benchmark score | IMF SDN/2024/001 |

---

## 4. Descriptive Summary Statistics (Estimation Sample: 2000–2023)

Based on the 3,512 country-year observations across 149 developing economies used in the baseline empirical estimations:

| Variable | Obs | Mean | Std. Dev. | Min | P25 | Median | P75 | Max |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $\text{L-AIPI}$ (Composite) | 3,512 | 0.461 | 0.258 | 0.004 | 0.162 | 0.461 | 0.481 | 0.978 |
| Digital Infrastructure ($DI$) | 3,512 | 0.382 | 0.312 | 0.000 | 0.080 | 0.316 | 0.650 | 1.000 |
| Human Capital ($HC$) | 3,512 | 0.472 | 0.281 | 0.000 | 0.220 | 0.465 | 0.720 | 1.000 |
| Innovation Pillar ($\text{INN}$) | 3,512 | 0.528 | 0.268 | 0.000 | 0.410 | 0.518 | 0.670 | 1.000 |
| Agricultural Value Added / Worker | 3,512 | $5,842 | $7,419 | $61.5 | $852 | $2,553 | $7,845 | $75,950 |
| Surface Temperature Anomaly ($^\circ\text{C}$) | 3,512 | +1.070 | 0.568 | -1.859 | +0.680 | +0.993 | +1.410 | +5.325 |
| Trade Openness (% of GDP) | 3,512 | 84.89 | 54.95 | 0.00 | 50.12 | 71.36 | 104.50 | 863.20 |

---

## 5. Sample Composition by Region (Developing Sample)

The 149 developing economies in the estimation sample span all major geographical areas:
- **Sub-Saharan Africa (SSA):** 46 economies (e.g., Nigeria, Kenya, Ethiopia, Ghana, South Africa, Tanzania, Rwanda).
- **Latin America & Caribbean (LAC):** 31 economies (e.g., Brazil, Colombia, Mexico, Peru, Argentina, Chile, Costa Rica).
- **East Asia & Pacific (EAP):** 21 economies (e.g., China, Vietnam, Indonesia, Philippines, Thailand, Malaysia).
- **Europe & Central Asia (ECA developing):** 23 economies (e.g., Kazakhstan, Turkey, Georgia, Azerbaijan, Albania).
- **Middle East & North Africa (MENA developing):** 16 economies (e.g., Egypt, Morocco, Jordan, Tunisia, Algeria).
- **South Asia (SAS):** 8 economies (e.g., India, Bangladesh, Pakistan, Sri Lanka, Nepal).
- **Small Island Developing States (SIDS):** 4 economies (e.g., Fiji, Samoa, Vanuatu, Solomon Islands).

---

## 6. Guidelines for Econometric Implementation

1. **Panel Identifier Setup:**
   In Stata:
   ```stata
   encode iso3, gen(country_id)
   xtset country_id year
   ```
   In R:
   ```r
   library(fixest)
   panel_fe <- feols(log(agri_val_add_worker) ~ temp_anomaly_c * laipi_composite + trade_openness_gdp | iso3 + year, data = df, cluster = ~iso3)
   ```
2. **Lagged Preparedness Specification:**
   Because technological indicators trend upward, use pre-shock lagged preparedness $\text{L-AIPI}_{i,t-1}$ to test whether pre-existing capability buffers unexpected weather volatility:
   ```stata
   gen l_laipi = L.laipi_composite
   reghdfe ln_agri c.temp_anomaly_c##c.l_laipi trade_openness_gdp, absorb(country_id year) vce(cluster country_id)
   ```

---

## 7. Contact and Maintenance

Questions, issue reports, and updates regarding the dataset should be directed to:
- **Author:** Chisom L. Ubabukoh
- **Affiliation:** Jindal Global Law School, O.P. Jindal Global University, India
- **Email:** `cubabukoh@jgu.edu.in`
