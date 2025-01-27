# Project 5: The Pandemmic Generation

## Introduction

This project, "The Pandemic Generation," utilizes daily reports and time series data provided by CSSE at Johns Hopkins University [csse_covid_19_data](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data) covering the period from January 22, 2020, to March 9, 2023, to create a tab-based pandemic dashboard. We used `pandas` and `sqlite3` to build the database, employed `gradio` for proof of concept, and developed the final product.

## How to reproduce

- Install [Miniconda](https://docs.anaconda.com/miniconda)
- Build up environment according to `environment.yml` 

```shell
`conda env create -f environment.yml`
```
- Place the four CSV files: `03-09-2023.csv`, `time_series_covid19_confirmed_global.csv`, `time_series_covid19_deaths_global.csv`, and  `time_series_covid19_vaccine_global.csv` from the `data/` folder into a `data/` directory in the working directory.
- Activate the environment and run `python create_covid_19_db.py`. This will create `covid_19.db` in the `data/` folder.
- Activate the environment and run `python app.py`. This will create `http://127.0.0.1:7860`.
