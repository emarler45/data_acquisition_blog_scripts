from datetime import datetime as dt

import pandas as pd

import api_caller


def main():
    americasTeams = api_caller.getAmericasTeams()
    teamsdf = pd.DataFrame.from_dict(americasTeams, orient='index')
    print(teamsdf.head())
    teamMatches = api_caller.getTeamMatchHistory(americasTeams)
    matchesdf = pd.DataFrame.from_dict(teamMatches, orient='index')
    print(matchesdf.head())
    teamRosterMoves = api_caller.getRosterMoves(americasTeams)
    rosterMovesdf = pd.DataFrame.from_dict(teamRosterMoves, orient='index')
    print(rosterMovesdf.head())


if __name__ == "__main__":
    main()
