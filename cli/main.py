import asyncio
import datetime
import logging

import typer

from duck import create_duckdb
from games import download_games
from pipeline import run_pipeline

app = typer.Typer(no_args_is_help=True)

def _configure_logging(level: str) -> None:
	level_name = level.upper()
	if level_name not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
		raise typer.BadParameter("log-level must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL")
	logging.basicConfig(level=getattr(logging, level_name))

@app.command()
def setup(
	start_year: int = typer.Option(..., help="First season to download and process"),
	end_year: int = typer.Option(..., help="Last season to download and process (inclusive)"),
	max_concurrent: int = typer.Option(5, help="Max concurrent downloads"),
	use_existing_players: bool = typer.Option(True, help="Reuse existing players parquet"),
	log_level: str = typer.Option("INFO", help="Logging level"),
) -> None:
	"""Download, process, and build DuckDB views for a range of seasons."""
	if start_year > end_year:
		raise typer.BadParameter("start-year must be <= end-year")

	_configure_logging(log_level)
	seasons = list(range(start_year, end_year + 1))
	asyncio.run(download_games(seasons=seasons, max_concurrent=max_concurrent))
	run_pipeline(seasons=seasons, use_existing_players=use_existing_players)
	create_duckdb()

@app.command()
def refresh(
	year: int = typer.Option(None, help="Season to refresh (defaults to current year)"),
	max_concurrent: int = typer.Option(5, help="Max concurrent downloads"),
	use_existing_players: bool = typer.Option(True, help="Reuse existing players parquet"),
	log_level: str = typer.Option("INFO", help="Logging level"),
) -> None:
	"""Refresh a single season and rebuild DuckDB views."""
	_configure_logging(log_level)
	if year is None:
		year = datetime.date.today().year

	seasons = [year]
	asyncio.run(download_games(seasons=seasons, max_concurrent=max_concurrent))
	run_pipeline(seasons=seasons, use_existing_players=use_existing_players)
	create_duckdb()

if __name__ == "__main__":
	app()

