import queryUtils
from misc.tupleTemplates import queryResult


def getBestTeam(region) -> queryResult:
    query = """
{
    tepRecords(region: """+region+""", season: 2024, skip: 0, take: 1, sortDir: Desc, sortBy: "opr") {
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

    success, data = queryUtils.parseQuery(query)
    if not success:
        return queryResult(data, success)

    team = data.data.tepRecords.data[0].data.team #what
    team_info = queryUtils.formatTeamInfo(team)

    autoData = team.qStats.Auto
    teleOpData = team.qStats.TeleOp
    endGameData = team.qStats.Endgame
    npData = team.qStats.TotalNP
    qStats = queryUtils.formatQStats(autoData, teleOpData, endGameData, npData)

    events = team.events #this is a list, not namespace
    team_events = []

    for event in events:
        team_events.append(queryUtils.formatTeamEventData(event))
        
    bt = bestTeam(team_info, qStats, team_events)
    
    return queryResult(bt, success)
    
def teamQuickStats(number):
    query = """
{
    teamByNumber(number: """+number+""") {
        name
        number
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
    }
}     
    """
    
    success, data = queryUtils.parseQuery(query)