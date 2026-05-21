import pyarrow as pa

from .base import Extractor
from helpers import Table, sget

class PlayExtractor(Extractor):
    def schema(self) -> pa.schema:
        return pa.schema([
            ('game_id', pa.uint32()),
            ('at_bat_index', pa.uint16()),

            ('event_type', pa.dictionary(pa.uint8(), pa.string())),
            ('description', pa.string()),
            ('rbi', pa.uint8()),
            ('away_score', pa.uint8()),
            ('home_score', pa.uint8()),
            ('is_out', pa.bool_()),

            ('half_inning', pa.dictionary(pa.uint8(), pa.string())),
            ('inning', pa.uint8()),
            ('start_time', pa.string()),
            ('end_time', pa.string()),
            ('is_scoring_play', pa.bool_()),
            ('has_review', pa.bool_()),
            ('has_out', pa.bool_()),

            ('balls', pa.uint8()),
            ('strikes', pa.uint8()),
            ('outs', pa.uint8()),

            ('batter_id', pa.uint32()),
            ('bat_side', pa.dictionary(pa.uint8(), pa.string())),
            ('pitcher_id', pa.uint32()),
            ('pitch_hand', pa.dictionary(pa.uint8(), pa.string())),
            ('post_on_first', pa.uint32()),
            ('post_on_second', pa.uint32()),
            ('post_on_third', pa.uint32())
        ])
    
    def extract(self, data: dict, buffer: Table) -> None:
        buffer['at_bat_index'].append(sget(data, "atBatIndex"))
        buffer['event_type'].append(sget(data, "result", "eventType"))
        buffer['description'].append(sget(data, "result", "description"))
        buffer['rbi'].append(sget(data, "result", "rbi"))
        buffer['away_score'].append(sget(data, "result", "awayScore"))
        buffer['home_score'].append(sget(data, "result", "homeScore"))
        buffer['is_out'].append(sget(data, "result", "isOut"))

        buffer['half_inning'].append(sget(data, "about", "halfInning"))
        buffer['inning'].append(sget(data, "about", "inning"))
        buffer['start_time'].append(sget(data, "about", "startTime"))
        buffer['end_time'].append(sget(data, "about", "endTime"))
        buffer['is_scoring_play'].append(sget(data, "about", "isScoringPlay"))
        buffer['has_review'].append(sget(data, "about", "hasReview"))
        buffer['has_out'].append(sget(data, "about", "hasOut"))

        buffer['balls'].append(sget(data, "count", "balls"))
        buffer['strikes'].append(sget(data, "count", "strikes"))
        buffer['outs'].append(sget(data, "count", "outs"))

        buffer['batter_id'].append(sget(data, "matchup", "batter", "id"))
        buffer['bat_side'].append(sget(data, "matchup", "batSide", "code"))
        buffer['pitcher_id'].append(sget(data, "matchup", "pitcher", "id"))
        buffer['pitch_hand'].append(sget(data, "matchup", "pitchHand", "code"))
        buffer['post_on_first'].append(sget(data, "matchup", "postOnFirst", "id"))
        buffer['post_on_second'].append(sget(data, "matchup", "postOnSecond", "id"))
        buffer['post_on_third'].append(sget(data, "matchup", "postOnThird", "id"))