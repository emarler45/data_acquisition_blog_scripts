import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt


teamsdf = pd.read_csv('data/teams.csv')
matchesdf = pd.read_csv('data/matches.csv')
movesdf = pd.read_csv('data/moves.csv')

def getYearLongStats(df):
    yearLongWinRate = df.groupby("team_id", as_index=False).agg(
        Name=pd.NamedAgg(column="team", aggfunc="max"),
        matches_played=pd.NamedAgg(column="team", aggfunc="count"),
        match_winrate=pd.NamedAgg(column="winner", aggfunc="mean"),
        maps_won=pd.NamedAgg(column="maps_won", aggfunc="sum"),
        rounds_won=pd.NamedAgg(column="rounds_won", aggfunc="sum"),
        maps_lost=pd.NamedAgg(column="maps_lost", aggfunc="sum"),
        rounds_lost=pd.NamedAgg(column="rounds_lost", aggfunc="sum")
    )
    yearLongWinRate["map_winrate"] = yearLongWinRate["maps_won"] / (yearLongWinRate["maps_won"] + yearLongWinRate["maps_lost"])
    yearLongWinRate["round_winrate"] = yearLongWinRate["rounds_won"] / (yearLongWinRate["rounds_won"] + yearLongWinRate["rounds_lost"])
    return yearLongWinRate

def getRosterSummary(df):
    grouped = df.groupby("team_id").team.agg(["count"])
    grouped = grouped.merge(teamsdf.drop(["roster"], axis=1), how='right', left_on="team_id", right_on='id').fillna(0)
    grouped.rename(columns={"count": "total_roster_moves"}, inplace=True)
    return grouped[["id", "name", "total_roster_moves"]]


def cleanMoves(df):
    timemask = (pd.to_datetime(df["date"]).dt.date < dt.date(2026, 10, 18)) & (pd.to_datetime(df["date"]).dt.date > dt.date(2026, 1, 15))
    cleandf = df[timemask]
    cleandf["date"] = pd.to_datetime(cleandf["date"])
    cleandf["action_type"] = cleandf["action_type"].str.replace("TransactionAction.", "")
    cleandf.reset_index()
    return cleandf

def consolidateMoves(dframe):
    df = dframe.copy()
    df["changeSeries"] = df["action_type"].map({"Join": "+", "Leave": "-", "Inactive": "-"}) + df["player_name"]
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df["month"] = pd.to_datetime(df["date"]).dt.month
    df = df.groupby(["month", "team"], as_index=False).agg(team_id=("team_id","max"),date=("date", "min"),changes=("changeSeries", ", ".join))
    df = df[df["changes"].str.match(r"([+-]\w+, ){1,}")]
    df = df[df["changes"].str.match(r"(?=.*\+)(?=.*-)")]
    return df


def addRosterIterations(matches, moves):
    matches["date"] = pd.to_datetime(matches["date"])
    matches["date"] = pd.to_datetime(matches["date"].dt.date)
    sortedMoves = moves.sort_values(["team", "date"]).copy()
    sortedMoves["iteration"] = sortedMoves.groupby("team").cumcount() + 1
    sortedMoves["date"] = pd.to_datetime(sortedMoves["date"])
    sortedMatches = matches.sort_values("date")
    sortedMovesDate = sortedMoves.sort_values("date")
    merged = pd.merge_asof(sortedMatches, sortedMovesDate[["team", "date", "iteration"]], on="date", by="team", direction="backward")
    merged["iteration"] = merged["iteration"].fillna(0).astype(int)
    return merged


def iterationStats(df):
    yearLongWinRate = df.groupby(["team_id", "iteration"], as_index=False).agg(
        Name=pd.NamedAgg(column="team", aggfunc="max"),
        matches_played=pd.NamedAgg(column="team", aggfunc="count"),
        match_winrate=pd.NamedAgg(column="winner", aggfunc="mean"),
        maps_won=pd.NamedAgg(column="maps_won", aggfunc="sum"),
        rounds_won=pd.NamedAgg(column="rounds_won", aggfunc="sum"),
        maps_lost=pd.NamedAgg(column="maps_lost", aggfunc="sum"),
        rounds_lost=pd.NamedAgg(column="rounds_lost", aggfunc="sum")
    )
    yearLongWinRate["map_winrate"] = yearLongWinRate["maps_won"] / (yearLongWinRate["maps_won"] + yearLongWinRate["maps_lost"])
    yearLongWinRate["round_winrate"] = yearLongWinRate["rounds_won"] / (yearLongWinRate["rounds_won"] + yearLongWinRate["rounds_lost"])
    return yearLongWinRate

def plotStuff(df):
    matchwin = df.loc[:, ["Name", "iteration", "match_winrate"]].pivot_table(index="Name", columns="iteration", values="match_winrate")
    mapwin = df.loc[:, ["Name", "iteration", "map_winrate"]].pivot_table(index="Name", columns="iteration", values="map_winrate")
    roundwin = df.loc[:, ["Name", "iteration", "round_winrate"]].pivot_table(index="Name", columns="iteration", values="round_winrate")
    matchwin.plot(kind="bar").set_ylim(0, 1)
    plt.title("Match Win Rates Across Iterations")
    plt.savefig("graphs/matchwins.png")
    mapwin.plot(kind="bar").set_ylim(0, 1)
    plt.title("Map Win Rates Across Iterations")
    plt.savefig("graphs/mapwins.png")
    roundwin.plot(kind="bar").set_ylim(0, 1)
    plt.title("Round Win Rates Across Iterations")
    plt.savefig("graphs/roundwins.png")


def main():
    clean_movesdf = cleanMoves(movesdf)
    yearLong = getYearLongStats(matchesdf)
    realMoves = consolidateMoves(clean_movesdf)
    rosterSummary = getRosterSummary(realMoves)
    rosterIterations = addRosterIterations(matchesdf, realMoves)
    rosterIterationWinrates = iterationStats(rosterIterations)
    plotStuff(rosterIterationWinrates)




if __name__ == '__main__':
    main()