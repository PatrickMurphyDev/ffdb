# FFDB: Local Statcast database

Tired of using the MLB API? Downloads folder full of CSV files exported from Baseball Savant? Look no further. Here's what you can get out of FFDB:

- Access to all of the pitch-level and play-by-play data in the pitch-tracking era (beginning in the late 2000s)
- A robust database schema based on the MLB API format
- Lightning-fast queries using Apache Parquet and DuckDB

(You can find more about me, the author, at (https://harperawl.net). Feel free to contact me with any questions you have about this project!)

### Setup

##### 1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

##### 2. Create a `.env` file (see `.env.example`) and set:

- `RAW_DATA_DIR`
- `PROCESSED_DATA_DIR`
- `DUCKDB_PATH`

##### 3. Run the CLI with args

This command line tool helps you set up the database and refresh it as needed.

Set up the database from start to finish:
```bash
ffdb setup --start-year 2024 --end-year 2026
```

Refresh the database for the current year (defaults to the current year):
```bash
ffdb refresh
```

### Queries

##### Install the DuckDB package into your environment:

**Python:**
```sh
pip install duckdb
```

**R:**
```r
install.packages("duckdb")
```

##### Make your query using SQL syntax:

**Python:**
```python
import duckdb

conn = duckdb.connect("path/to/your/database.duckdb")

data = conn.execute("""
    SELECT * FROM games LIMIT 100;
""")
```

**R:**
```r
library(duckdb)
library(dplyr)

conn <- dbConnect(duckdb(), dbdir = "path/to/your/database.duckdb", read_only = TRUE)

pitches <- dbGetQuery(conn, "
    SELECT * FROM games LIMIT 100;
")
```

See [the database documentation](DATABASE.md) for more information on how to query the database.