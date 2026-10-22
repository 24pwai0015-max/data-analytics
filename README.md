<div align="center">

<picture>
  <source srcset="assets/hero.svg" media="(prefers-color-scheme: dark)">
  <source srcset="assets/hero.svg" media="(prefers-color-scheme: light)">
  <img src="assets/hero.svg" alt="Arsalan – Data analyst in the making → Agent Automation Developer" width="100%">
</picture>

<br/>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-2.0+-013243?logo=numpy&logoColor=white)](https://numpy.org/)
[![pandas](https://img.shields.io/badge/pandas-2.2+-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.9+-11557C)](https://matplotlib.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-0.13+-444876)](https://seaborn.pydata.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)](https://jupyter.org/)
&nbsp;&nbsp;`Phase 1 · Foundation`

</div>

---

## Mission

I'm a 2nd-year AI student at UET Peshawar building a data-analytics foundation one script at a time.
Every file in this repository is something I wrote, ran, debugged, and documented myself.
The long-term goal is to design autonomous agent pipelines (LangChain / CrewAI) — but first, the fundamentals.

---

<div align="center">

<picture>
  <source srcset="assets/roadmap.svg" media="(prefers-color-scheme: dark)">
  <source srcset="assets/roadmap.svg" media="(prefers-color-scheme: light)">
  <img src="assets/roadmap.svg" alt="Roadmap – Phase 1 pulsing, Phases 2-5 outlined" width="100%">
</picture>

</div>

| Phase | Focus | Status |
|:-----:|:------|:------:|
| **1** | **Foundation** — NumPy, Pandas, Matplotlib, Seaborn | 🟢 in progress |
| **2** | Python automation & APIs | ○ next |
| **3** | LLM APIs & vector databases | ○ planned |
| **4** | Agent automation (LangChain / CrewAI) | ○ planned |
| **5** | Freelance & production pipelines | ○ planned |

---

## Skills

Only listing what I have actually used in this repository.

| Data Wrangling | Analysis | Visualization | Tooling |
|:---------------|:---------|:--------------|:--------|
| pandas — Series, DataFrame, `loc`/`iloc` | NumPy — arrays, broadcasting, aggregation | Matplotlib — line, bar, pie, subplots | Jupyter Notebook |
| pandas — `fillna`, `dropna`, string ops | pandas — `groupby`, `agg`, `crosstab` | Seaborn — countplot, boxplot, heatmap | Git & GitHub |
| pandas — `merge`, `concat`, `pivot_table` | pandas — `value_counts`, filtering | Multi-panel dashboards (9-chart stories) | VS Code + venv |

---

## Project Gallery

<table>
<tr>
<td width="33%" align="center">

**Titanic EDA Pipeline**

<img src="assets/titanic_eda.png" alt="Titanic EDA – pandas survival analysis pipeline" width="100%"/>

Survival analysis with cleaning, groupby, and a composite chart.
→ [`pandas/titanic_eda.py`](pandas/titanic_eda.py)

</td>
<td width="33%" align="center">

**Titanic Visual Story (Part 1)**

<img src="assets/titanic_dashboard_1.png" alt="Titanic dashboard – 9-chart visual story, part 1" width="100%"/>

Multi-panel Matplotlib + Seaborn dashboard.
→ [`Matplotlib-Seaborn/week-5/day-6/`](Matplotlib-Seaborn/week-5/day-6/)

</td>
<td width="33%" align="center">

**Titanic Visual Story (Part 2)**

<img src="assets/titanic_dashboard_2.png" alt="Titanic dashboard – 9-chart visual story, part 2" width="100%"/>

Continuation: class distributions, fare analysis, embarkation.
→ [`Matplotlib-Seaborn/week-5/day-6/`](Matplotlib-Seaborn/week-5/day-6/)

</td>
</tr>
</table>

> **Netflix EDA** (8 individual charts) — [`Matplotlib-Seaborn/week-6/day-1/`](Matplotlib-Seaborn/week-6/day-1/)
> &nbsp;|&nbsp; **Wine Quality** — [`pandas/w4_02_wine_quality_dataset.py`](pandas/w4_02_wine_quality_dataset.py)
> &nbsp;|&nbsp; **Zomato mini-project** — [`Matplotlib-Seaborn/week-6/mini project/`](Matplotlib-Seaborn/week-6/mini%20project/)

---

## Repository Map

Generated from the actual directory tree — nothing invented.

```
data-analytics/
├── assets/                          ← SVGs, screenshots (for this README)
├── data/
│   ├── data.csv
│   ├── netflix_raw.csv
│   ├── titanic_cleaned.csv
│   ├── titanic_cleaned_intermediate.csv
│   └── titanic_raw.csv
├── numpy/
│   ├── w1_01_arrays_reshape_slicing.py
│   ├── w1_02_broadcasting.py
│   ├── w1_03_bolean_masking.py
│   ├── w1_04_aggregations..py
│   ├── w1_05_random_tasks.py
│   └── w1_numpy_mini_project.py
├── pandas/
│   ├── titanic_eda.py  (+titanic_eda.png)
│   ├── w2_01_Series_DataFrame.py
│   ├── w2_01_Series_DataFrame_tasks.py
│   ├── w2_02_loc_iloc.py
│   ├── w2_03_missing_values.py
│   ├── w2_03_handling_values_part_2.py
│   ├── w2_05_strings.py
│   ├── w3_01_apply_lambda.py
│   ├── w3_02_groupby_basics.py
│   ├── w3_03_groupby_agg.py
│   ├── w3_04_pivote_tables.py
│   ├── w3_05_value_counts_crosstab.py
│   ├── w3_sunday_titanic_questions.py
│   ├── w4_01_merge_concat_01.py
│   ├── w4_01_merge_concat_02.py
│   ├── w4_02_wine_quality_dataset.py
│   └── w4_05_revision.py
├── Matplotlib-Seaborn/
│   ├── week-5/
│   │   ├── day-1/  (matplotlib basics, pie chart, notes)
│   │   ├── day-2/  (plot customisation, grid lines)
│   │   ├── day-3/  (subplots, tasks, notes)
│   │   ├── day-4/  (seaborn basics, notes)
│   │   ├── day-5/  (pandas ↔ matplotlib integration)
│   │   └── day-6/  (9-chart Titanic dashboards)
│   └── week-6/
│       ├── day-1/  (Netflix 8-chart EDA)
│       ├── day-6/  (advanced filtering, notes)
│       └── mini project/  (Zomato Bangalore dataset)
├── data-mining-labs/
│   └── README.md
├── .gitignore
├── requirements.txt
├── run.ps1
└── README.md                        ← you are here
```

---

## Quick Start (Windows PowerShell)

```powershell
# 1  Clone
git clone https://github.com/24pwai0015-max/data-analytics.git
cd data-analytics

# 2  Virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3  Dependencies
pip install -r requirements.txt

# 4  Run an example
python pandas/titanic_eda.py
```

---

## How I Learn

1. **Predict** what the output should be before running the code.
2. **Struggle** for ~15 minutes before looking anything up.
3. **Read** the official docs and the actual error message.
4. **Document** the insight in a `notes.md` next to the script.
5. **Ship** — commit and push to GitHub the same day.

---

## Current Focus & Next Steps

- **Now:** finishing a full EDA on a fresh Kaggle dataset (clean → transform → visualise).
- **Next:** time-series analysis (ARIMA / Prophet) and a new animated chart SVG.
- **After that:** Phase 2 — Python automation scripts and REST API projects.

---

<div align="center">

<sub>Made with patience by <a href="https://github.com/24pwai0015-max">Arsalan</a> · BS AI · UET Peshawar</sub>

</div>
