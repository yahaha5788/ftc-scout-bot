import json
from http.client import responses
from types import SimpleNamespace
import requests
from typing import NamedTuple
from misc.tupleTemplates import quickStats, locationValues, eventStats, eventData

url = "https://api.ftcscout.org/graphql"


def getCodeDesc(code: int) -> str:
    desc: str = responses[code]
    return desc


def appendSuffix(num: int) -> str:
    num = str(num)
    number = num
    num = list("".join(num))[len(list("".join(num))) - 1] # muahahaha
    match num:
        case '1':
            suf = 'st'
        case '2':
            suf = 'nd'
        case '3':
            suf = 'rd'
        case _:
            suf = 'th'
    fin = f'{number}{suf}'
    return fin

def parseQuery(query):
    response = requests.post(url=url, json={"query": query})
    if response.status_code == 200:
        success = True
        j = response.content
        data: SimpleNamespace = json.loads(j, object_hook=lambda d: SimpleNamespace(**d))
        return success, data

    else:
        success = False
        return success, f"Request did not return code 200, instead returned code {response.status_code}: {getCodeDesc(response.status_code)}"

def getBestTeam():
    query = """
{
    tepRecords(region: All, season: 2024, skip: 1, take: 1, sortDir: Desc, sortBy: "opr") { #gets the best team
        data {
            data {
                team {
                    number: number
                    name: name
                    location {
                        city
                        state
                        country
                    }
                    qStats: quickStats(season: 2024) {
                        Auto: auto {
                            rank: rank
                            opr: value
                        }
                        TeleOp: dc {
                            rank: rank
                            opr: value
                        }
                        Endgame: eg {
                            rank: rank
                            opr: value
                        }
                        TotalNP: tot {
                            rank: rank
                            np: value
                        }
                    }
                    events(season: 2024) {
                        event {
                            name
                            type
                            location {
                                loc: venue
                                city
                                state
                                country
                            }
                            start
                        }
                        stats {
                            ... on TeamEventStats2024 {
                                rank
                                w: wins
                                l: losses
                                t: ties
                            }
                        }
                    }
                }
            }
        }
    }
}
    """

    success, data = parseQuery(query)
    if not success:
        return data
    team = data.data.tepRecords.data[0].data.team #graphqk
    autoData = team.qStats.Auto
    teleOpData = team.qStats.TeleOp
    endGameData = team.qStats.Endgame
    npData = team.qStats.TotalNP
    events = team.events #this is a list, not namespace
    loc = team.location
    number = team.number
    name = team.name
    auto = f"{round(autoData.opr)} | {appendSuffix(autoData.rank)}"
    teleOp = f"{round(teleOpData.opr)} | {appendSuffix(teleOpData.rank)}"
    endGame = f"{round(endGameData.opr)} | {appendSuffix(endGameData.rank)}"
    npData = f"{round(npData.np)} | {appendSuffix(npData.rank)}"
    qStats = quickStats(auto, teleOp, endGame, npData)
