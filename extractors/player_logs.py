import pyarrow as pa

from .base import Extractor
from helpers import Table, sget

class PlayerLogExtractor(Extractor):
    def schema(self) -> pa.schema:
        return pa.schema([
            ('game_id', pa.uint32()),
            ('player', pa.uint32()),

            ('jersey_number', pa.string()),
            ('position', pa.dictionary(pa.uint8(), pa.string())),
            ('status_code', pa.dictionary(pa.uint8(), pa.string())),
            ('parent_team_id', pa.uint32()),
            ('batting_order', pa.string())
        ])
    
    def extract(self, data: dict, buffer: Table) -> None:
        buffer['jersey_number'].append(sget(data, "jerseyNumber"))
        buffer['position'].append(sget(data, "position", "abbreviation"))
        buffer['status_code'].append(sget(data, "status", "code"))
        buffer['parent_team_id'].append(sget(data, "parentTeamId"))
        buffer['batting_order'].append(sget(data, "battingOrder"))