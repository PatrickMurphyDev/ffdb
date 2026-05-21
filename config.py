from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    RAW_DATA_DIR: str = os.getenv("RAW_DATA_DIR")
    PROCESSED_DATA_DIR: str = os.getenv("PROCESSED_DATA_DIR")
    DUCKDB_PATH: str = os.getenv("DUCKDB_PATH")

assert Config.RAW_DATA_DIR is not None, "RAW_DATA_DIR environment variable is not set"
assert Config.PROCESSED_DATA_DIR is not None, "PROCESSED_DATA_DIR environment variable is not set"
assert Config.DUCKDB_PATH is not None, "DUCKDB_PATH environment variable is not set"