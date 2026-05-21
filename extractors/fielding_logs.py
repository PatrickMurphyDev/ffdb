import pyarrow as pa

from .base import Extractor
from helpers import Table, sget

class FieldingLogExtractor(Extractor):
    def schema(self) -> pa.schema:
        return pa.schema([
            ('game_id', pa.uint32()),
            ('player', pa.uint32()),

            ('caught_stealing', pa.uint8()),
            ('stolen_bases', pa.uint8()),
            ('assists', pa.uint8()),
            ('put_outs', pa.uint8()),
            ('errors', pa.uint8()),
            ('chances', pa.uint8()),
            ('passed_ball', pa.uint8()),
            ('pickoffs', pa.uint8())
        ])
    
    def extract(self, data: dict, buffer: Table) -> None:
        buffer["caught_stealing"].append(sget(data, "caught_stealing"))
        buffer["stolen_bases"].append(sget(data, "stolen_bases"))
        buffer["assists"].append(sget(data, "assists"))
        buffer["put_outs"].append(sget(data, "put_outs"))
        buffer["errors"].append(sget(data, "errors"))
        buffer["chances"].append(sget(data, "chances"))
        buffer["passed_ball"].append(sget(data, "passed_ball"))
        buffer["pickoffs"].append(sget(data, "pickoffs"))