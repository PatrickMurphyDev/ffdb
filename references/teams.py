from references.base import Reference, Table
from helpers import sget

class Teams(Reference):
    def __init__(self):
        super().__init__("https://statsapi.mlb.com/api/v1/teams?sportId=1")

    def extract(self) -> Table:
        data = self.data

        teams = data.get("teams", [])
        for team in teams:
            self.table["spring_league_id"].append(sget(team, "springLeague", "id"))
            self.table["id"].append(sget(team, "id"))
            self.table["name"].append(sget(team, "name"))
            self.table["venue_id"].append(sget(team, "venue", "id"))
            self.table["spring_venue_id"].append(sget(team, "springVenue", "id"))
            self.table["team_code"].append(sget(team, "teamCode"))
            self.table["file_code"].append(sget(team, "fileCode"))
            self.table["abbreviation"].append(sget(team, "abbreviation"))
            self.table["team_name"].append(sget(team, "teamName"))
            self.table["location_name"].append(sget(team, "locationName"))
            self.table["first_year_of_play"].append(sget(team, "firstYearOfPlay"))
            self.table["league_id"].append(sget(team, "league", "id"))
            self.table["division_id"].append(sget(team, "division", "id"))
            self.table["sport_id"].append(sget(team, "sport", "id"))
            self.table["short_name"].append(sget(team, "shortName"))
            self.table["franchise_name"].append(sget(team, "franchiseName"))
            self.table["club_name"].append(sget(team, "clubName"))
        
        return self.table
            
            