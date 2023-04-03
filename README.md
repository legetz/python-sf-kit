# python-sf-kit
Collection of Python scripts related to Salesforce

# Setup Python environment
- `python3 -m venv env`
- `source env/bin/activate`
- `pip install --upgrade pip`
- `pip install -r requirements.txt`

# Scripts
- Export records into CSV file using BULK API
  - `python src/bulk_api_export_data.py`
- Import CSV file into SQLite database
  - `python src/import_csv_sqlite.py`
- Update Salesforce records using BULK API with local SQLite records
  - `python src/bulk_api_update_sqlite.py`
