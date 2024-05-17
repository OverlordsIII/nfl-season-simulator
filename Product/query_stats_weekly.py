import pandas as pd

stats = ["points-per-game", 'average-scoring-margin', 'yards-per-point', 'points-per-play']

df = pd.read_csv("week_dates.csv")

dfSeasons = df.groupby('season').last()
dfSeasons = dfSeasons.iloc[3:]
print(dfSeasons)

for stat in stats:
    print(stat)
    # gonna comment out for now - testing purposes
    # for index, row in dfSeasons.iterrows():
    row = dfSeasons.iloc[-1] # just use 2023 stats for now, can use other seasons later
    dfPpg = pd.read_html("https://www.teamrankings.com/nfl/stat/" + stat + "?date=" + row['end'])[0]
    print(dfPpg)


