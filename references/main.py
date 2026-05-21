from references.teams import Teams
from references.pitch_codes import PitchCodes
from helpers import Table

references = {
    "teams": Teams(),
    "pitch_codes": PitchCodes(),
}

def get_references() -> dict[str, Table]:
    tables = {}

    for name, reference in references.items():
        reference.get_data()
        table = reference.extract()
        tables[name] = table

    return tables