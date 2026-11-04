import vlrdevapi as vlr


def getAmericasTeams() -> dict:
    kickoff = vlr.event(2682)
    teamList = kickoff.teams(stage='main-event').stages[0].teams
    teamsDict = {}
    index = 0
    for team in teamList:
        index += 1
        dataDict = {}
        dataDict["id"] = team.id
        dataDict["name"] = team.name
        dataDict["roster"] = []
        for player in team.players:
            dataDict["roster"].append(player.name)
        teamsDict[index] = dataDict
    return teamsDict

def getRoundsWonAndLost(match, team_id: int) -> tuple:
    maps: list = match.games
    roundsWon = 0
    roundsLost = 0
    isTeam1 = 1 if match.team1.id == team_id else 0
    isTeam2 = 1 if isTeam1 == 0 else 0
    for map in maps:
        if map.played  == False:
            break
        roundsWon += (map.team1_score * isTeam1) + (map.team2_score * isTeam2)
        roundsLost += (map.team2_score * isTeam1) + (map.team1_score * isTeam2)
    return roundsWon, roundsLost


def getTeamMatchHistory(teams: dict) -> dict:
    fullDict = {}
    for idx in teams:
        team_id = teams[idx]["id"]
        currTeam = vlr.team(team_id)
        teamInfo = currTeam.info()
        past_matches = currTeam.completed_matches().matches
        for match in past_matches:
            if match.datetime.year != 2026:
                break
            matchDict = {}
            print(f"Current match: {match.event}, {teamInfo.name} vs. {match.opponent.name}, {match.datetime}")
            matchDict["team_id"] = teamInfo.id
            matchDict["date"] = match.datetime
            matchDict["team"] = teamInfo.name
            matchDict["event"] = match.event
            matchDict["opponent"] = match.opponent.name
            matchDict["winner"] = match.is_win
            matchDict["maps_won"] = match.team_score
            matchDict["maps_lost"] = match.opponent_score
            matchMaps = vlr.series(match.match_id)
            matchDict["rounds_won"], matchDict["rounds_lost"] = getRoundsWonAndLost(matchMaps.info(), teamInfo.id)
            fullDict[teamInfo.id] = matchDict

    return fullDict


def getRosterMoves(teams: dict) -> dict:
    movesDict = {}
    i = 0
    for idx in teams:
        team_id = teams[idx]["id"]
        currTeam = vlr.team(team_id)
        teamInfo = currTeam.info()
        movesList = currTeam.transactions().transactions
        for move in movesList:
            i += 1
            moveDict = {}
            if move.date.year != 2026 or move.position != "player":
                break
            moveDict["team_id"] = teamInfo.id
            moveDict["team"] = teamInfo.name
            moveDict["date"] = move.date
            moveDict["player_name"] = move.player.ign
            moveDict["action_type"] = str(move.action)
            movesDict[i] = moveDict
    return movesDict
        



    
    



