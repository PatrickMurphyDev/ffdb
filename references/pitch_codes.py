from references.base import Reference, Table
from helpers import sget

class PitchCodes(Reference):
    def __init__(self):
        super().__init__("https://statsapi.mlb.com/api/v1/pitchCodes")

    def extract(self) -> Table:
        data = self.data

        for entry in data:
            self.table["code"].append(sget(entry, "code"))
            self.table["description"].append(sget(entry, "description"))
            self.table["swing_status"].append(sget(entry, "swingStatus"))
            self.table["swing_miss_status"].append(sget(entry, "swingMissStatus"))
            self.table["swing_contact_status"].append(sget(entry, "swingContactStatus"))
            self.table["sort_order"].append(sget(entry, "sortOrder"))
            self.table["strike_status"].append(sget(entry, "strikeStatus"))
            self.table["ball_status"].append(sget(entry, "ballStatus"))
            self.table["pitch_status"].append(sget(entry, "pitchStatus"))
            self.table["pitch_result_text"].append(sget(entry, "pitchResultText"))
            self.table["bunt_attempt_status"].append(sget(entry, "buntAttemptStatus"))
            self.table["contact_status"].append(sget(entry, "contactStatus"))
        
        return self.table
            
            