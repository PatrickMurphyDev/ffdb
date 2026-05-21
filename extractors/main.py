from helpers import Table, buffer, sget

from .games import GameExtractor
from .plays import PlayExtractor
from .play_credits import PlayCreditExtractor
from .runners import RunnerExtractor
from .runner_credits import RunnerCreditExtractor
from .events import EventExtractor
from .player_logs import PlayerLogExtractor
from .batting_logs import BattingLogExtractor
from .pitching_logs import PitchingLogExtractor
from .fielding_logs import FieldingLogExtractor
from .position_logs import PositionLogExtractor

extractors = {
    "games": GameExtractor(),
    "plays": PlayExtractor(),
    "play_credits": PlayCreditExtractor(),
    "runners": RunnerExtractor(),
    "runner_credits": RunnerCreditExtractor(),
    "events": EventExtractor(),
    "player_logs": PlayerLogExtractor(),
    "batting_logs": BattingLogExtractor(),
    "pitching_logs": PitchingLogExtractor(),
    "fielding_logs": FieldingLogExtractor(),
    "position_logs": PositionLogExtractor()
}

def extract_game_data(gumbo_data: dict) -> dict[str, Table]:
    buffers = {name: buffer(extractor.schema()) for name, extractor in extractors.items()}

    extractors["games"].extract(gumbo_data.get("gameData", {}), buffers["games"])
    game_id = sget(gumbo_data, "gameData", "game", "pk")
    plays = sget(gumbo_data, "liveData", "plays", "allPlays", default=[])
    for play in plays:
        buffers["plays"]['game_id'].append(game_id)
        extractors["plays"].extract(play, buffers["plays"])

        at_bat_index = play.get("atBatIndex")

        runners = sget(play, "runners", default=[])
        for runner_index, runner in enumerate(runners):
            buffers["runners"]['game_id'].append(game_id)
            buffers["runners"]['at_bat_index'].append(at_bat_index)
            buffers["runners"]['runner_index'].append(runner_index)
            extractors["runners"].extract(runner, buffers["runners"])
            
            runner_credits = sget(runner, "credits", default=[])
            for runner_credit in runner_credits:
                buffers["runner_credits"]['game_id'].append(game_id)
                buffers["runner_credits"]['at_bat_index'].append(at_bat_index)
                buffers["runner_credits"]['runner_index'].append(runner_index)
                extractors["runner_credits"].extract(runner_credit, buffers["runner_credits"])

        events = sget(play, "playEvents", default=[])
        for event_index, event in enumerate(events):
            buffers["events"]['game_id'].append(game_id)
            buffers["events"]['at_bat_index'].append(at_bat_index)
            buffers["events"]['event_index'].append(event_index)
            extractors["events"].extract(event, buffers["events"])

        play_credits = sget(play, "credits", default=[])
        for play_credit in play_credits:
            buffers["play_credits"]['game_id'].append(game_id)
            buffers["play_credits"]['at_bat_index'].append(at_bat_index)
            extractors["play_credits"].extract(play_credit, buffers["play_credits"])

    for team in ["away", "home"]:
        players = sget(gumbo_data, "liveData", "boxscore", "teams", team, "players", default={}).values()
        for player in players:
            buffers["player_logs"]['game_id'].append(game_id)
            buffers["player_logs"]['player'].append(sget(player, "person", "id"))
            extractors["player_logs"].extract(player, buffers["player_logs"])

            batting_stats = sget(player, "stats", "batting", default={})
            if batting_stats:
                buffers["batting_logs"]['game_id'].append(game_id)
                buffers["batting_logs"]['player'].append(sget(player, "person", "id"))
                extractors["batting_logs"].extract(batting_stats, buffers["batting_logs"])

            pitching_stats = sget(player, "stats", "pitching", default={})
            if pitching_stats:
                buffers["pitching_logs"]['game_id'].append(game_id)
                buffers["pitching_logs"]['player'].append(sget(player, "person", "id"))
                extractors["pitching_logs"].extract(pitching_stats, buffers["pitching_logs"])

            fielding_stats = sget(player, "stats", "fielding", default={})
            if fielding_stats:
                buffers["fielding_logs"]['game_id'].append(game_id)
                buffers["fielding_logs"]['player'].append(sget(player, "person", "id"))
                extractors["fielding_logs"].extract(fielding_stats, buffers["fielding_logs"])

            if player.get("allPositions"):
                buffers["position_logs"]['game_id'].append(game_id)
                buffers["position_logs"]['player'].append(sget(player, "person", "id"))
                extractors["position_logs"].extract(player, buffers["position_logs"])

    return buffers