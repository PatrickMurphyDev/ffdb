import pyarrow as pa

from .base import Extractor
from helpers import Table, sget

class BattingLogExtractor(Extractor):
    def schema(self) -> pa.schema:
        return pa.schema([
            ('game_id', pa.uint32()),
            ('player', pa.uint32()),

            ('summary', pa.string()),
            ('games_played', pa.uint8()),
            ('fly_outs', pa.uint8()),
            ('ground_outs', pa.uint8()),
            ('air_outs', pa.uint8()),
            ('runs', pa.uint8()),
            ('doubles', pa.uint8()),
            ('triples', pa.uint8()),
            ('home_runs', pa.uint8()),
            ('strike_outs', pa.uint8()),
            ('base_on_balls', pa.uint8()),
            ('intentional_walks', pa.uint8()),
            ('hits', pa.uint8()),
            ('hit_by_pitch', pa.uint8()),
            ('at_bats', pa.uint8()),
            ('caught_stealing', pa.uint8()),
            ('stolen_bases', pa.uint8()),
            ('ground_into_double_play', pa.uint8()),
            ('ground_into_triple_play', pa.uint8()),
            ('plate_appearances', pa.uint8()),
            ('total_bases', pa.uint16()),
            ('rbi', pa.uint16()),
            ('left_on_base', pa.uint16()),
            ('sac_bunts', pa.uint16()),
            ('sac_flies', pa.uint16()),
            ('catchers_interference', pa.uint16()),
            ('pickoffs', pa.uint16()),
            ('pop_outs', pa.uint16()),
            ('line_outs', pa.uint16())
        ])

    def extract(self, data: dict, buffer: Table) -> None:
        buffer['summary'].append(sget(data, "summary"))
        buffer['games_played'].append(sget(data, "gamesPlayed"))
        buffer['fly_outs'].append(sget(data, "flyOuts"))
        buffer['ground_outs'].append(sget(data, "groundOuts"))
        buffer['air_outs'].append(sget(data, "airOuts"))
        buffer['runs'].append(sget(data, "runs"))
        buffer['doubles'].append(sget(data, "doubles"))
        buffer['triples'].append(sget(data, "triples"))
        buffer['home_runs'].append(sget(data, "homeRuns"))
        buffer['strike_outs'].append(sget(data, "strikeOuts"))
        buffer['base_on_balls'].append(sget(data, "baseOnBalls"))
        buffer['intentional_walks'].append(sget(data, "intentionalWalks"))
        buffer['hits'].append(sget(data, "hits"))
        buffer['hit_by_pitch'].append(sget(data, "hitByPitch"))
        buffer['at_bats'].append(sget(data, "atBats"))
        buffer['caught_stealing'].append(sget(data, "caughtStealing"))
        buffer['stolen_bases'].append(sget(data, "stolenBases"))
        buffer['ground_into_double_play'].append(sget(data, "groundIntoDoublePlay"))
        buffer['ground_into_triple_play'].append(sget(data, "groundIntoTriplePlay"))
        buffer['plate_appearances'].append(sget(data, "plateAppearances"))
        buffer['total_bases'].append(sget(data, "totalBases"))
        buffer['rbi'].append(sget(data, "rbi"))
        buffer['left_on_base'].append(sget(data, "leftOnBase"))
        buffer['sac_bunts'].append(sget(data, "sacBunts"))
        buffer['sac_flies'].append(sget(data, "sacFlies"))
        buffer['catchers_interference'].append(sget(data, "catchersInterference"))
        buffer['pickoffs'].append(sget(data, "pickoffs"))
        buffer['pop_outs'].append(sget(data, "popOuts"))
        buffer['line_outs'].append(sget(data, "lineOuts"))    