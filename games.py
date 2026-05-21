"""
Flow:
1. Get list of game IDs given year from schedule endpoint
2. For each game ID, download the game JSON from the live feed endpoint
3. Save each game JSON to a file named {game_id}.json in the raw/games/{season} directory
"""

from pathlib import Path
import asyncio
import logging
import json
import datetime

from aiohttp import ClientResponseError, ClientSession
import aiofiles

from config import Config

logger = logging.getLogger(__name__)

async def _get_game_ids(session: ClientSession, season: int) -> list[int]:
    """Returns a list of game IDs for a given season."""
    url = "https://statsapi.mlb.com/api/v1/schedule"

    current_date = datetime.date.today()
    if season >= current_date.year:
        end_date = current_date
    else:
        end_date = datetime.date(season, 12, 31)

    params = {
        "sportId": "1",  # MLB
        "startDate": f"{season}-01-01",
        "endDate": end_date.strftime("%Y-%m-%d")
    }

    logger.info(f"Fetching game IDs for season {season}...")
    async with session.get(url, params=params) as response:
        response.raise_for_status()
        data = await response.json()

    logger.info(f"Found {len(data.get('dates', []))} dates with games for season {season}")
    return [
        game["gamePk"] 
        for date in data.get("dates", []) 
        for game in date.get("games", [])
    ]


async def _download_game(session: ClientSession, game_id: int, out_dir: Path, semaphore: asyncio.Semaphore) -> None:
    """Downloads a single game JSON file."""
    url = "https://statsapi.mlb.com/api/v1.1/game/" + f"{game_id}/feed/live"
    params = {
        "hydrate": "credits,alignment,officials,flags,preState"
    }

    path = out_dir / f"{game_id}.json"
    if path.exists():
        logger.debug(f"Game file already exists, skipping: {path}")
        return

    async with semaphore:
        async with session.get(url, params=params) as response:
            try:
                response.raise_for_status()
                data = await response.json()
            except ClientResponseError as e:
                logger.error(f"Failed to download game {game_id}: {e}")
                return
        
        async with aiofiles.open(path, "w") as f:
            await f.write(json.dumps(data))

        logger.debug(f"Saved game {game_id} to {path}")

async def _download_games_for_season(season: int, out_dir: Path, max_concurrent: int = 5) -> None:
    """Downloads all game JSON files for a given season."""
    out_dir.mkdir(parents=True, exist_ok=True)
    semaphore = asyncio.Semaphore(max_concurrent)

    async with ClientSession() as session:
        game_ids = await _get_game_ids(session, season)

        tasks = [
            _download_game(session, game_id, out_dir, semaphore) 
            for game_id in game_ids
        ]
        await asyncio.gather(*tasks)

async def download_games(seasons: list[int], max_concurrent: int = 5) -> None:
    logger.info(f"Starting game download for seasons: {seasons}")
    for season in seasons:
        path = Path(Config.RAW_DATA_DIR + f"/games/{season}")
        await _download_games_for_season(season, path, max_concurrent=max_concurrent)
        logger.info(f"Downloaded games for {season}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    seasons_to_download = [2026]
    asyncio.run(download_games(seasons_to_download))