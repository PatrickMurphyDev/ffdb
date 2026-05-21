import pyarrow as pa

from .base import Extractor
from helpers import Table, sget

class PlayCreditExtractor(Extractor):
    def schema(self) -> pa.schema:
        return pa.schema([
            ('game_id', pa.uint32()),
            ('at_bat_index', pa.uint16()),

            ('player', pa.uint32()),
            ('credit', pa.dictionary(pa.uint8(), pa.string()))
        ])

    def extract(self, data: dict, buffer: Table) -> None:
        buffer['player'].append(sget(data, "player", "id"))
        buffer['credit'].append(sget(data, "credit"))