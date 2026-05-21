import pyarrow as pa

from .base import Extractor
from helpers import Table, sget

class PositionLogExtractor(Extractor):
    def schema(self) -> pa.schema:
        return pa.schema([
            ('game_id', pa.uint32()),
            ('player', pa.uint32()),

            ('position', pa.dictionary(pa.uint8(), pa.string()))
        ])

    def extract(self, data: dict, buffer: Table) -> None:
        buffer['position'].append(sget(data, "position"))