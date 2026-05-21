import pyarrow as pa

from .base import Extractor
from helpers import Table, sget

class EventExtractor(Extractor):
    def schema(self) -> pa.schema:
        return pa.schema([
            ('game_id', pa.uint32()),
            ('at_bat_index', pa.uint16()),
            ('event_index', pa.uint8()),

            ('description', pa.string()),
            ('event_type', pa.dictionary(pa.uint8(), pa.string())),
            ('code', pa.dictionary(pa.uint8(), pa.string())),
            ('away_score', pa.uint8()),
            ('home_score', pa.uint8()),
            ('is_in_play', pa.bool_()),
            ('is_strike', pa.bool_()),
            ('is_ball', pa.bool_()),
            ('pitch_type', pa.dictionary(pa.uint8(), pa.string())),
            ('is_scoring_play', pa.bool_()),
            ('is_out', pa.bool_()),
            ('has_review', pa.bool_()),

            ('balls', pa.uint8()),
            ('strikes', pa.uint8()),
            ('outs', pa.uint8()),

            ('pre_balls', pa.uint8()),
            ('pre_strikes', pa.uint8()),
            ('pre_outs', pa.uint8()),

            ('start_speed', pa.float32()),
            ('end_speed', pa.float32()),
            ('strike_zone_top', pa.float32()),
            ('strike_zone_bottom', pa.float32()),
            ('a_x', pa.float32()),
            ('a_y', pa.float32()),
            ('a_z', pa.float32()),
            ('pfx_x', pa.float32()),
            ('pfx_z', pa.float32()),
            ('p_x', pa.float32()),
            ('p_z', pa.float32()),
            ('v_x0', pa.float32()),
            ('v_y0', pa.float32()),
            ('v_z0', pa.float32()),
            ('x', pa.float32()),
            ('y', pa.float32()),
            ('x0', pa.float32()),
            ('y0', pa.float32()),
            ('z0', pa.float32()),

            ('break_angle', pa.float32()),
            ('break_length', pa.float32()),
            ('break_y', pa.float32()),
            ('break_vertical', pa.float32()),
            ('break_vertical_induced', pa.float32()),
            ('break_horizontal', pa.float32()),
            ('spin_rate', pa.uint16()),
            ('spin_direction', pa.uint16()),

            ('launch_speed', pa.float32()),
            ('launch_angle', pa.float32()),
            ('total_distance', pa.float32()),
            ('trajectory', pa.dictionary(pa.uint8(), pa.string())),
            ('hardness', pa.dictionary(pa.uint8(), pa.string())),
            ('trajectory', pa.dictionary(pa.uint8(), pa.string())),
            ('hit_coord_x', pa.float32()),
            ('hit_coord_y', pa.float32()),

            ('zone', pa.uint8()),
            ('type_confidence', pa.float32()),
            ('plate_time', pa.float32()),
            ('extension', pa.float32()),

            ('play_id', pa.string()),
            ('pitch_number', pa.uint8()),
            ('start_time', pa.string()),
            ('end_time', pa.string()),
            ('is_pitch', pa.bool_()),
            ('type', pa.dictionary(pa.uint8(), pa.string())),

            ('is_overturned', pa.bool_()),
            ('review_type', pa.dictionary(pa.uint16(), pa.string())),
            ('challenge_team_id', pa.uint32()),
            ('challenge_player', pa.uint32()),

            ('pitcher', pa.uint32()),
            ('pitch_hand', pa.dictionary(pa.uint8(), pa.string())),
            ('catcher', pa.uint32()),
            ('first_baseman', pa.uint32()),
            ('second_baseman', pa.uint32()),
            ('third_baseman', pa.uint32()),
            ('shortstop', pa.uint32()),
            ('left_fielder', pa.uint32()),
            ('center_fielder', pa.uint32()),
            ('right_fielder', pa.uint32()),

            ('batter', pa.uint32()),
            ('bat_side', pa.dictionary(pa.uint8(), pa.string())),
            ('runner_on_first', pa.uint32()),
            ('runner_on_second', pa.uint32()),
            ('runner_on_third', pa.uint32()),

            ('official_home_plate', pa.uint32()),
            ('official_first_base', pa.uint32()),
            ('official_second_base', pa.uint32()),
            ('official_third_base', pa.uint32()),
            ('official_left_field', pa.uint32()),
            ('official_right_field', pa.uint32())
        ])
    
    def extract(self, data: dict, buffer: Table) -> None:
        buffer['description'].append(sget(data, "details", "description"))
        buffer['event_type'].append(sget(data, "details", "eventType"))
        buffer['code'].append(sget(data, "details", "code"))
        buffer['away_score'].append(sget(data, "details", "awayScore"))
        buffer['home_score'].append(sget(data, "details", "homeScore"))
        buffer['is_in_play'].append(sget(data, "details", "isInPlay"))
        buffer['is_strike'].append(sget(data, "details", "isStrike"))
        buffer['is_ball'].append(sget(data, "details", "isBall"))
        buffer['pitch_type'].append(sget(data, "details", "type", "code"))
        buffer['is_scoring_play'].append(sget(data, "details", "isScoringPlay"))
        buffer['is_out'].append(sget(data, "details", "isOut"))
        buffer['has_review'].append(sget(data, "details", "hasReview"))

        buffer['balls'].append(sget(data, "count", "balls"))
        buffer['strikes'].append(sget(data, "count", "strikes"))
        buffer['outs'].append(sget(data, "count", "outs"))

        buffer['pre_balls'].append(sget(data, "preCount", "balls"))
        buffer['pre_strikes'].append(sget(data, "preCount", "strikes"))
        buffer['pre_outs'].append(sget(data, "preCount", "outs"))

        buffer['start_speed'].append(sget(data, "pitchData", "startSpeed"))
        buffer['end_speed'].append(sget(data, "pitchData", "endSpeed"))
        buffer['strike_zone_top'].append(sget(data, "pitchData", "strikeZoneTop"))
        buffer['strike_zone_bottom'].append(sget(data, "pitchData", "strikeZoneBottom"))
        buffer['a_x'].append(sget(data, "pitchData", "coordinates", "aX"))
        buffer['a_y'].append(sget(data, "pitchData", "coordinates", "aY"))
        buffer['a_z'].append(sget(data, "pitchData", "coordinates", "aZ"))
        buffer['pfx_x'].append(sget(data, "pitchData", "coordinates", "pfxX"))
        buffer['pfx_z'].append(sget(data, "pitchData", "coordinates", "pfxZ"))
        buffer['p_x'].append(sget(data, "pitchData", "coordinates", "pX"))
        buffer['p_z'].append(sget(data, "pitchData", "coordinates", "pZ"))
        buffer['v_x0'].append(sget(data, "pitchData", "coordinates", "vX0"))
        buffer['v_y0'].append(sget(data, "pitchData", "coordinates", "vY0"))
        buffer['v_z0'].append(sget(data, "pitchData", "coordinates", "vZ0"))
        buffer['x'].append(sget(data, "pitchData", "coordinates", "x"))
        buffer['y'].append(sget(data, "pitchData", "coordinates", "y"))
        buffer['x0'].append(sget(data, "pitchData", "coordinates", "x0"))
        buffer['y0'].append(sget(data, "pitchData", "coordinates", "y0"))
        buffer['z0'].append(sget(data, "pitchData", "coordinates", "z0"))

        buffer['break_angle'].append(sget(data, "pitchData", "breaks", "breakAngle"))
        buffer['break_length'].append(sget(data, "pitchData", "breaks", "breakLength"))
        buffer['break_y'].append(sget(data, "pitchData", "breaks", "breakY"))
        buffer['break_vertical'].append(sget(data, "pitchData", "breaks", "breakVertical"))
        buffer['break_vertical_induced'].append(sget(data, "pitchData", "breaks", "breakVerticalInduced"))
        buffer['break_horizontal'].append(sget(data, "pitchData", "breaks", "breakHorizontal"))
        buffer['spin_rate'].append(sget(data, "pitchData", "breaks", "spinRate"))
        buffer['spin_direction'].append(sget(data, "pitchData", "breaks", "spinDirection"))

        buffer['launch_speed'].append(sget(data, "hitData", "launchSpeed"))
        buffer['launch_angle'].append(sget(data, "hitData", "launchAngle"))
        buffer['total_distance'].append(sget(data, "hitData", "totalDistance"))
        buffer['trajectory'].append(sget(data, "hitData", "trajectory"))
        buffer['hardness'].append(sget(data, "hitData", "hardness"))
        buffer['hit_coord_x'].append(sget(data, "hitData", "coordinates", "coordX"))
        buffer['hit_coord_y'].append(sget(data, "hitData", "coordinates", "coordY"))

        buffer['zone'].append(sget(data, "pitchData", "zone"))
        buffer['type_confidence'].append(sget(data, "pitchData", "typeConfidence"))
        buffer['plate_time'].append(sget(data, "pitchData", "plateTime"))
        buffer['extension'].append(sget(data, "pitchData", "extension"))

        buffer['play_id'].append(sget(data, "playId"))
        buffer['pitch_number'].append(sget(data, "pitchNumber"))
        buffer['start_time'].append(sget(data, "startTime"))
        buffer['end_time'].append(sget(data, "endTime"))
        buffer['is_pitch'].append(sget(data, "isPitch"))
        buffer['type'].append(sget(data, "type"))

        buffer['is_overturned'].append(sget(data, "reviewDetails", "isOverturned"))
        buffer['review_type'].append(sget(data, "reviewDetails", "reviewType"))
        buffer['challenge_team_id'].append(sget(data, "reviewDetails", "challengeTeamId"))
        buffer['challenge_player'].append(sget(data, "reviewDetails", "player", "id"))
        
        buffer['pitcher'].append(sget(data, "defense", "pitcher", "id"))
        buffer['pitch_hand'].append(sget(data, "defense", "pitcher", "pitchHand", "code"))
        buffer['catcher'].append(sget(data, "defense", "catcher", "id"))
        buffer['first_baseman'].append(sget(data, "defense", "first", "id"))
        buffer['second_baseman'].append(sget(data, "defense", "second", "id"))
        buffer['third_baseman'].append(sget(data, "defense", "third", "id"))
        buffer['shortstop'].append(sget(data, "defense", "shortstop", "id"))
        buffer['left_fielder'].append(sget(data, "defense", "left", "id"))
        buffer['center_fielder'].append(sget(data, "defense", "center", "id"))
        buffer['right_fielder'].append(sget(data, "defense", "right", "id"))

        buffer['batter'].append(sget(data, "offense", "batter", "id"))
        buffer['bat_side'].append(sget(data, "offense", "batter", "batSide", "code"))
        buffer['runner_on_first'].append(sget(data, "offense", "first", "id"))
        buffer['runner_on_second'].append(sget(data, "offense", "second", "id"))
        buffer['runner_on_third'].append(sget(data, "offense", "third", "id"))

        official_home_plate = None
        official_first_base = None
        official_second_base = None
        official_third_base = None
        official_left_field = None
        official_right_field = None
        for official in sget(data, "matchup", "officials", default=[]):
            position = official.get("officialType")
            if position == "Home Plate":
                official_home_plate = sget(official, "official", "id")
            elif position == "First Base":
                official_first_base = sget(official, "official", "id")
            elif position == "Second Base":
                official_second_base = sget(official, "official", "id")
            elif position == "Third Base":
                official_third_base = sget(official, "official", "id")
            elif position == "Left Field":
                official_left_field = sget(official, "official", "id")
            elif position == "Right Field":
                official_right_field = sget(official, "official", "id")

        buffer['official_home_plate'].append(official_home_plate)
        buffer['official_first_base'].append(official_first_base)
        buffer['official_second_base'].append(official_second_base)
        buffer['official_third_base'].append(official_third_base)
        buffer['official_left_field'].append(official_left_field)
        buffer['official_right_field'].append(official_right_field)