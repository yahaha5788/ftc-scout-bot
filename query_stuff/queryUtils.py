import json
import requests
from types import SimpleNamespace

from misc.tupleTemplates import quickStats, locationValues, eventData, eventStats, teamInfo
from misc.utilMethods import getCodeDesc, appendSuffix


def parseQuery(query):
    response = requests.post(url="https://api.ftcscout.org/graphql", json={"query": query})
    if response.status_code == 200:
        success = True
        j = response.content
        data: SimpleNamespace = json.loads(j, object_hook=lambda d: SimpleNamespace(**d))
        return success, data

    else:
        success = False
        return success, f"Request did not return code 200, instead returned code {response.status_code}: {getCodeDesc(response.status_code)}"

def formatQStats(auto: SimpleNamespace, teleop: SimpleNamespace, endgame: SimpleNamespace, np: SimpleNamespace) -> quickStats:
    auto = f"{round(auto.opr)} | {appendSuffix(auto.rank)}"

    teleOp = f"{round(teleop.opr)} | {appendSuffix(teleop.rank)}"

    endGame = f"{round(endgame.opr)} | {appendSuffix(endgame.rank)}"

    npData = f"{round(np.np)} | {appendSuffix(np.rank)}"

    return quickStats(auto, teleOp, endGame, npData)

def formatTeamEventData(i: SimpleNamespace) -> eventData:
    event = i.event
    stats = i.stats

    name = event.name
    level = event.type
    time = event.start

    csc = f"{event.location.city}, {event.location.state}, {event.location.country}."
    loc = locationValues(csc, event.location.loc)

    if not stats:
        return eventData(name, level, time, loc)

    team_event_stats = eventStats(stats.rank, stats.w, stats.l, stats.t)

    return eventData(name, level, time, loc, team_event_stats)

def formatEventInfo(event: SimpleNamespace) -> eventData:
    event = event.event
    name = event.name
    level = event.type
    time = event.start

    csc = f"{event.location.city}, {event.location.state}, {event.location.country}."
    loc = locationValues(csc, event.location.loc)
    return eventData(name, level, time, loc)

def formatTeamInfo(team: SimpleNamespace) -> teamInfo:
    name = team.name
    number = team.number
    loc = team.location

    csc = f"{loc.city}, {loc.state}, {loc.country}."
    location = locationValues(csc)

    return teamInfo(name, number, location)