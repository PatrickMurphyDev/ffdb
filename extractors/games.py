import pyarrow as pa

from .base import Extractor
from helpers import Table, sget

class GameExtractor(Extractor):
    def schema(self) -> pa.schema:
        return pa.schema([
            ('game_id', pa.uint32()),
            ('game_type', pa.dictionary(pa.uint8(), pa.string())),
            ('double_header', pa.dictionary(pa.uint8(), pa.string())),
            ('gameday_type', pa.dictionary(pa.uint8(), pa.string())),
            ('tiebreaker', pa.dictionary(pa.uint8(), pa.string())),
            ('season', pa.uint16()),

            ('date_time', pa.string()),
            ('tz_offset', pa.decimal128(3,2)),

            ('status_code', pa.string()),

            ('away_team_id', pa.uint32()),
            ('home_team_id', pa.uint32()),

            ('venue_id', pa.uint32()),

            ('weather_condition', pa.dictionary(pa.uint8(), pa.string())),
            ('temperature', pa.int16()),
            ('wind_speed', pa.uint8()),
            ('wind_direction', pa.dictionary(pa.uint8(), pa.string())),

            ('attendance', pa.uint32())
        ])
    
    def _parse_wind(self, wind_str: str | None) -> tuple[int | None, str | None]:
        """Split wind info into speed and direction. e.g. '8 mph, Out To LF' -> (8, 'Out To LF')"""
        if not wind_str:
            return None, None

        parts = wind_str.split(",", 1)
        if len(parts) != 2:
            return None, wind_str.strip()
        speed, direction = parts
        return int(speed.replace("mph", "").strip()), direction.strip()

    def extract(self, data: dict, buffer: Table) -> None:
        wind_speed, wind_direction = self._parse_wind(sget(data, "weather", "wind"))
        
        buffer['game_id'].append(sget(data, "game", "pk"))
        buffer['game_type'].append(sget(data, "game", "type"))
        buffer['double_header'].append(sget(data, "game", "doubleHeader"))
        buffer['gameday_type'].append(sget(data, "game", "gamedayType"))
        buffer['tiebreaker'].append(sget(data, "game", "tiebreaker"))
        buffer['season'].append(int(sget(data, "game", "season")))

        buffer['date_time'].append(sget(data, "datetime", "dateTime"))
        buffer['tz_offset'].append(sget(data, "venue", "timeZone", "offsetAtGameTime"))

        buffer['status_code'].append(sget(data, "status", "statusCode"))
        
        buffer['away_team_id'].append(sget(data, "teams", "away", "id"))
        buffer['home_team_id'].append(sget(data, "teams", "home", "id"))

        buffer['venue_id'].append(sget(data, "venue", "id"))

        buffer['weather_condition'].append(sget(data, "weather", "condition"))
        temp_str = sget(data, "weather", "temp")
        try:
            buffer['temperature'].append(int(temp_str))
        except (ValueError, TypeError):
            buffer['temperature'].append(None)
        buffer['wind_speed'].append(wind_speed)
        buffer['wind_direction'].append(wind_direction)

        buffer['attendance'].append(sget(data, "gameInfo", "attendance"))