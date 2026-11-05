import pandas as pd
import datetime as dt

teamsdf = pd.read_csv('data/teams.csv')
matchesdf = pd.read_csv('data/matches.csv')
movesdf = pd.read_csv('data/moves.csv')

def getYearLongStats(df):
    yearLongWinRate = df.groupby("team_id").agg(
        Name=pd.NamedAgg(column="team", aggfunc="max"),
        matches_played=pd.NamedAgg(column="team", aggfunc="count"),
        match_winrate=pd.NamedAgg(column="winner", aggfunc="mean"),
    )
    yearLongWinRate["map_winrate"] = matchesdf["maps_won"].sum() / (matchesdf["maps_won"].sum() + matchesdf["maps_lost"].sum())
    yearLongWinRate["round_winrate"] = matchesdf["rounds_won"].sum() / (matchesdf["rounds_won"].sum() + matchesdf["rounds_lost"].sum())
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
    df = df.groupby(["month", "team"], as_index=False).agg(team_id=("team_id","max"),date=("date", "max"),changes=("changeSeries", ", ".join))
    df = df[df["changes"].str.match(r"(\+\w+, -\w+|-\w+, \+\w+)")]
    return df

def main():
    clean_movesdf = cleanMoves(movesdf)
    yearLong = getYearLongStats(matchesdf)
    rosterSummary = getRosterSummary(clean_movesdf)
    realMoves = consolidateMoves(clean_movesdf)




if __name__ == '__main__':
    main()