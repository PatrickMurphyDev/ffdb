import pyarrow as pa

from .base import Extractor
from helpers import Table, sget

class RunnerExtractor(Extractor):
    def schema(self) -> pa.schema:
        return pa.schema([
            ('game_id', pa.uint32()),
            ('at_bat_index', pa.uint16()),
            ('runner_index', pa.uint8()),

            ('origin_base', pa.dictionary(pa.uint8(), pa.string())),
            ('start', pa.dictionary(pa.uint8(), pa.string())),
            ('end', pa.dictionary(pa.uint8(), pa.string())),
            ('out_base', pa.dictionary(pa.uint8(), pa.string())),
            ('is_out', pa.bool_()),
            ('out_base', pa.dictionary(pa.uint8(), pa.string())),
            ('out_number', pa.uint8()),

            ('event_type', pa.dictionary(pa.uint8(), pa.string())),
            ('movement_reason', pa.dictionary(pa.uint8(), pa.string())),
            ('runner', pa.uint32()),
            ('responsible_pitcher', pa.uint32()),
            ('is_scoring_event', pa.bool_()),
            ('rbi', pa.bool_()),
            ('earned', pa.bool_()),
            ('team_unearned', pa.bool_()),
            ('play_index', pa.uint8())
        ])
    
    def extract(self, data: dict, buffer: Table) -> None:
        buffer['origin_base'].append(sget(data, "movement", "originBase"))
        buffer['start'].append(sget(data, "movement", "start"))
        buffer['end'].append(sget(data, "movement", "end"))
        buffer['out_base'].append(sget(data, "movement", "outBase"))
        buffer['is_out'].append(sget(data, "movement", "isOut"))
        buffer['out_number'].append(sget(data, "movement", "outNumber"))

        buffer['event_type'].append(sget(data, "details", "eventType"))
        buffer['movement_reason'].append(sget(data, "details", "movementReason"))
        buffer['runner'].append(sget(data, "details", "runner", "id"))
        buffer['responsible_pitcher'].append(sget(data, "details", "responsiblePitcher", "id"))
        buffer['is_scoring_event'].append(sget(data, "details", "isScoringEvent"))
        buffer['rbi'].append(sget(data, "details", "rbi"))
        buffer['earned'].append(sget(data, "details", "earned"))
        buffer['team_unearned'].append(sget(data, "details", "teamUnearned"))
        buffer['play_index'].append(sget(data, "details", "playIndex"))
