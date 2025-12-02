# Forest Supply Chain Analytics Dashboard

End-to-end analytics project: generate data → load into SQLite → write SQL queries → build Power BI/Tableau dashboard.

## Business Questions
- Are we meeting weekly plan (planned vs actual)?
- Which mill is under/over-utilized?
- Profit by mill/region/species
- Which high-risk stands contribute most to shipments?

## Tech Stack
Python (pandas) • SQLite • SQL • Power BI / Tableau

## How to Run
```bash
pip install -r requirements.txt
python src/generate_data.py
python src/load_to_sqlite.py
