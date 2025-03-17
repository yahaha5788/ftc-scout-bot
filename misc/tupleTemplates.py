from typing import NamedTuple



class quickStats(NamedTuple):
    autoData: str
    teleOpData: str
    endGameData: str
    NpData: str

class locationValues(NamedTuple):
    country: str
    state: str
    city: str
    venue: str = None

class eventData(NamedTuple):
    name: str
    event_type: str
    start: str

    location: NamedTuple
    stats: NamedTuple

class eventStats(NamedTuple):
    event_rank: int
    w: int
    l: int
    t: int
