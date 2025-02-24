# County Health Data API

This API provides access to county health data based on ZIP codes. It uses data from County Health Rankings & Roadmaps and RowZero Zip Code to County mappings.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Convert CSV files to SQLite database:
```bash
python csv_to_sqlite.py data.db zip_county.csv
python csv_to_sqlite.py data.db county_health_rankings.csv
```

## API Usage

### Endpoint: `/county_data`

Send a POST request with JSON data containing:
- `zip`: 5-digit ZIP code
- `measure_name`: One of the following health measures:
  - Violent crime rate
  - Unemployment
  - Children in poverty
  - Diabetic screening
  - Mammography screening
  - Preventable hospital stays
  - Uninsured
  - Sexually transmitted infections
  - Physical inactivity
  - Adult obesity
  - Premature Death
  - Daily fine particulate matter

Example request:
```bash
curl -H 'Content-Type: application/json' \
     -d '{"zip":"02138","measure_name":"Adult obesity"}' \
     https://your-api-endpoint/county_data
```

### Response Codes
- 200: Success
- 400: Missing or invalid parameters
- 404: Data not found
- 418: I'm a teapot (when coffee=teapot is included in request)
