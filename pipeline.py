from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
import glob
import os

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from tqdm import tqdm

from config import Config
from players import get_players_for_season
from extractors.base import Table
from extractors.main import extractors, extract_game_data
from references.main import get_references

def process_game(file_path: str) -> dict[str, Table]:
    try:
        game_json = json.load(open(file_path, "r"))
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return {name: {col: [] for col in extractor.schema().names} for name, extractor in extractors.items()}
    return extract_game_data(game_json)

def run_pipeline(seasons: list[int], use_existing_players: bool = True) -> None:
    if use_existing_players and os.path.exists(f"{Config.PROCESSED_DATA_DIR}/players.parquet"):
        players = pd.read_parquet(f"{Config.PROCESSED_DATA_DIR}/players.parquet")
    else:
        players = pd.DataFrame()

    for season in seasons:
        game_files = glob.glob(f"{Config.RAW_DATA_DIR}/games/{season}/*.json")

        buffers: dict[str, Table] = {name: {col: [] for col in extractor.schema().names} for name, extractor in extractors.items()}

        with ProcessPoolExecutor() as executor:
            futures = {executor.submit(process_game, file) for file in game_files}

            for future in tqdm(as_completed(futures), desc=f"Season {season}", total=len(futures)):
                game_tables = future.result()
                for name, table in game_tables.items():
                    for col in table:
                        buffers[name][col].extend(table[col])

        for name, buffer in buffers.items():
            os.makedirs(f"{Config.PROCESSED_DATA_DIR}/{name}", exist_ok=True)
            table = pa.Table.from_pydict(buffer)
            pq.write_table(table, f"{Config.PROCESSED_DATA_DIR}/{name}/{season}.parquet")

        season_players = get_players_for_season(season)
        players = pd.concat([players, pd.DataFrame(season_players)], ignore_index=True)
        players = players.drop_duplicates(subset=["id"])
        
    pq.write_table(pa.Table.from_pandas(players), f"{Config.PROCESSED_DATA_DIR}/players.parquet")

    reference_tables = get_references()
    os.makedirs(f"{Config.PROCESSED_DATA_DIR}/.reference", exist_ok=True)
    for name, table in reference_tables.items():
        pa_table = pa.Table.from_pydict(table)
        pq.write_table(pa_table, f"{Config.PROCESSED_DATA_DIR}/.reference/{name}.parquet")


if __name__ == "__main__":
    run_pipeline(seasons=[2026])