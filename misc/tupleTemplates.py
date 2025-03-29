from typing import NamedTuple



class quickStats(NamedTuple):
    autoData: str
    teleOpData: str
    endGameData: str
    NpData: str

class locationValues(NamedTuple):
    cityStateCountry: str
    venue: str = None

class eventStats(NamedTuple):
    event_rank: int
    w: int
    l: int
    t: int

class eventData(NamedTuple):
    name: str
    event_type: str
    start: str

    location: locationValues
    stats: eventStats = None

class teamInfo(NamedTuple):
    name: str
    number: int
    loc: locationValues

class bestTeam(NamedTuple):
    info: teamInfo
    stats: quickStats
    events: list
    
class queryResult(NamedTuple):
    result: NamedTuple
    success: bool