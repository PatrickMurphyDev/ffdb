import duckdb

from config import Config
from extractors.main import extractors
from references.main import references

def create_duckdb():
    con = duckdb.connect(Config.DUCKDB_PATH)
    for name in extractors.keys():
        con.execute(f"""
            CREATE OR REPLACE VIEW {name}
            AS SELECT * FROM read_parquet('{Config.PROCESSED_DATA_DIR}/{name}/*.parquet', union_by_name=true)
        """)
    
    con.execute(f"""
        CREATE SCHEMA IF NOT EXISTS ref
    """)

    con.execute(f"""
        CREATE OR REPLACE VIEW ref.players
        AS SELECT * FROM read_parquet('{Config.PROCESSED_DATA_DIR}/players.parquet')
    """)


    for name in references.keys():
        con.execute(f"""
            CREATE OR REPLACE VIEW ref.{name}
            AS SELECT * FROM read_parquet('{Config.PROCESSED_DATA_DIR}/.reference/{name}.parquet')
        """)

    con.close()

if __name__ == "__main__":
    create_duckdb()