import pandas as pd

df = pd.read_csv("schedule.csv")
stuff = []

print(df.head(50))

season = df.iloc[0]["season"]
week = df.iloc[0]["week"]
first_date = df.iloc[0]["gameday"]
rowtemp = df.iloc[0]
enddate = df.iloc[0]["gameday"]

for index, row in df.iterrows():
    rowtemp = row
    if (rowtemp["season"] == season and rowtemp["week"] == week):
        enddate = df.iloc[index]["gameday"]
    else:
        stuff.append(dict(season=season, week=week, start=first_date, end=enddate))
        season = df.iloc[index]["season"]
        week = df.iloc[index]["week"]
        first_date = df.iloc[index]["gameday"]
        rowtemp = df.iloc[index]
        enddate = df.iloc[index]["gameday"]

pd.DataFrame(stuff).to_csv("week_dates.csv", index=False)
# need week date ranges to build web scraper