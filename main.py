from datetime import datetime as dt

import pandas as pd

import api_caller


def main():
    americasTeams = api_caller.getAmericasTeams()
    teamMatches = api_caller.getTeamMatchHistory(americasTeams)
    teamRosterMoves = api_caller.getRosterMoves(americasTeams)
    matchesdf = pd.DataFrame.from_dict(teamMatches)
    print(matchesdf.head())


if __name__ == "__main__":
    main()
