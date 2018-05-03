# Nanjing Metro smartcard data analysis

This repository contains code to replicate results for several different projects using the same dataset, trips logged via smartcard in the Nanjing Metro in early 2015.

The header of our source dataset is located in the `nanjing-metro/` directory.

## Data processing

In order to replicate any of the following results, we need to grab the original dataset (which is not included in this repo due to size constraints). Ask the authors for the source CSVs and place it in the `nanjing-data/` directory. Data was originally provided as mdb files, which `conversion.py` converts into csv format.

`station_list_scraper.js` was used to grab the order and track lengths from the Nanjing Metro Wikipedia pages for use in building the network model.


## CEE 264: Line 3 opening demand modeling

In order to replicate our results for the line opening demand modeling project, after including the data as outlined in the above Data Processing section, run these notebooks in the following order:

1. Induced demand analysis: `induced_demand/Induced Demand.ipynb`
2. Usage evolution analysis: `usage_evo/usage_evo.ipynb`
3. Engineer features and create trip data: `feature_engineering/build_features.ipynb`
4. Create output csv for pylogit: `feature_engineering/build_features/prebuilt/generate_csv.ipynb`
5. Run discrete choice model: `pylogit\Pylogit Test.ipynb`


## CEE 295 and IEOR 290: Traveler station entrance time delta distribution

After including the data outline in the Data Processing Section, to replicate the station entrance time delta distribution model, run the following notebook:

* For the CEE 295 version of the analysis, run `arrivals/arrivals-295.ipynb`
* For the IEOR 290 version of the analysis (still in progress), run `arrivals/arrivals.ipynb`

