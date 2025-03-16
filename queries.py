import json
from http.client import responses
from types import SimpleNamespace
import requests
from typing import NamedTuple

url = "https://api.ftcscout.org/graphql"


def getCodeDesc(code: int) -> str:
    desc: str = responses[code]
    return desc


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
    tepRecords(region: All, season: 2024, skip: 1, take: 1, sortDir: Desc, sortBy: "opr") {
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
    qstats = team.qStats
    events = team.events #this is a list, not namespace
    loc = team.location
    print(team)
    number = team.number
    name = team.name

getBestTeam()