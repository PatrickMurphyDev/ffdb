from collections import defaultdict
import requests

from helpers import Table, sget

def get_data_for_season(season: int) -> dict:
    url = f"https://statsapi.mlb.com/api/v1/sports/1/players?season={season}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch player data for season {season}. Status code: {response.status_code}")

def get_players_for_season(season: int) -> Table:
    data = get_data_for_season(season)

    table = defaultdict(list)

    players = data.get("people", [])
    for player in players:
        table["id"].append(player.get("id"))
        table["full_name"].append(player.get("fullName"))
        table["first_name"].append(player.get("firstName"))
        table["last_name"].append(player.get("lastName"))
        table["primary_number"].append(player.get("primaryNumber"))
        table["birth_date"].append(player.get("birthDate"))
        table["birth_city"].append(player.get("birthCity"))
        table["birth_state_province"].append(player.get("birthStateProvince"))
        table["birth_country"].append(player.get("birthCountry"))
        table["height"].append(player.get("height"))
        table["weight"].append(player.get("weight"))
        table["primary_position"].append(sget(player, "primaryPosition", "code"))
        table["use_name"].append(player.get("useName"))
        table["use_last_name"].append(player.get("useLastName"))
        table["middle_name"].append(player.get("middleName"))
        table["boxscore_name"].append(player.get("boxscoreName"))
        table["draft_year"].append(player.get("draftYear"))
        table["mlb_debut_date"].append(player.get("mlbDebutDate"))
        table["bat_side"].append(sget(player, "batSide", "code"))
        table["pitch_hand"].append(sget(player, "pitchHand", "code"))
        table["name_first_last"].append(player.get("nameFirstLast"))
        table["name_slug"].append(player.get("nameSlug"))
        table["first_last_name"].append(player.get("firstLastName"))
        table["last_first_name"].append(player.get("lastFirstName"))
        table["last_init_name"].append(player.get("lastInitName"))
        table["init_last_name"].append(player.get("initLastName"))
        table["full_fml_name"].append(player.get("fullFMLName"))
        table["full_lfm_name"].append(player.get("fullLFMName"))
        table["strike_zone_top"].append(player.get("strikeZoneTop"))
        table["strike_zone_bottom"].append(player.get("strikeZoneBottom"))
    
    return table