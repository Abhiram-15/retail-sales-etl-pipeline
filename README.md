# Retail Sales ETL Pipeline (Python + SQL)

## Overview
A beginner-friendly data engineering project that extracts retail sales from CSV files, validates and cleans records with Python/Pandas, and loads the cleaned data into a SQLite database.

## Data flow
CSV files -> Python validation/cleaning -> SQLite tables -> SQL analysis queries

## Skills demonstrated
- Python and Pandas data processing
- Data quality checks and handling missing/invalid values
- ETL (Extract, Transform, Load)
- Relational database design and SQL queries
- Reproducible project structure and documentation

## Setup
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python src/etl_pipeline.py
```

## Output
The pipeline creates `output/retail_sales.db` and `output/cleaned_sales.csv`.
It prints a short data-quality summary and example sales totals.

## Run SQL queries
Open the SQLite database using DB Browser for SQLite or run:
```bash
python src/run_queries.py
```

## Important
The included data is synthetic sample data created for learning. It does not represent a real company.
