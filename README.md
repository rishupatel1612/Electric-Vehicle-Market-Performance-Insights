# EV Market Intelligence Capstone Project

## Project title
**EV Market Intelligence: Sales, Battery Technology, Manufacturer and Sustainability Analytics**

## Problem statement
Use electric-vehicle market data to explore sales distribution, manufacturer performance, battery technology adoption, driving range, customer satisfaction, and manufacturing geography. The goal is to provide a filterable executive dashboard for strategy, business intelligence, and sustainable mobility research.

## Dataset
- `ev_market_train.csv`: 200,000 records and 37 fields, used for analysis.
- `ev_market_test.csv`: 100,000 records and 37 fields, included for reference and future validation; not merged into dashboard calculations.
- Key fields include manufacturer, model year, manufacturing country, market region, vehicle category, battery capacity/type, range, price, annual sales, customer rating, and CO₂ saved per year.

## Dashboard features
- Interactive filters: model year, category, market region, battery technology, manufacturing country.
- KPI cards: records, summed annual sales, average range, average rating, average price.
- Executive overview: category sales, top manufacturers, model-year trend, regional comparison.
- Technology: battery mix, average range by battery type, battery capacity vs. range, range by category.
- Geography and data quality: manufacturing-country distribution, sales by country, missing-value analysis.
- Data explorer and CSV download.

## How to run
1. Install Python 3.10 or newer.
2. Extract this ZIP to a folder.
3. Open a terminal in that folder and run:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```
4. Streamlit will open the dashboard in your browser.

## Main initial findings (from the training dataset)
- 200,000 rows cover 200 manufacturers, 15 vehicle categories, 10 manufacturing countries and 7 market regions.
- Average listed driving range: 324.5 km.
- Average customer rating: 4.09/5 (among non-missing ratings).
- Average listed price: $64,921.
- Battery types in the data: NMC, LFP, NCA, Sodium-Ion, Solid-State.
- Missing cells across the dataset: 18,996.

## Important interpretation note
The annual-sales column is strongly right-skewed and contains extreme values. Summed sales should not be presented as verified real-world market share without validating the dataset's row definition and outliers. This project is an exploratory analytics capstone, not an audited industry report.

## Suggested capstone deliverables / presentation
1. Introduction and business problem
2. Dataset and data dictionary
3. Data quality and preprocessing
4. Dashboard design and KPIs
5. Findings by category, manufacturer, battery, geography, and ratings
6. Recommendations and limitations
7. Future scope: predictive sales modeling, clustering vehicle segments, and validated forecasting
