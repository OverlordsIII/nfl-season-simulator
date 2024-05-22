import pandas as pd
import os

stats = pd.DataFrame()
codes = pd.read_csv("team_codes.csv")
records = pd.read_csv("records.csv")

base = "yearly_data/stats"

for item in os.listdir("yearly_data/stats"):
    stats = pd.concat([stats, pd.read_csv(base + "/" + item.__str__())])

stats = stats.drop([stats.columns.to_list()[0]], axis=1)
stats = stats.pivot_table(values='data', index=["season", "team"], columns="stat", aggfunc="first")

records = records.drop([records.columns.to_list()[0]], axis=1)
records = records.rename(columns={"Year": "season"})
records = records.set_index(["season", "team"])

for index, row in records.iterrows():
    stats.at[index, 'percent'] = row["%"]
    for rowT in row:
        if str(rowT).split().__contains__("%"):
            rowT = float("".join(str(rowT).split("")[:-1])) / 100
stats.to_csv("temp.csv")