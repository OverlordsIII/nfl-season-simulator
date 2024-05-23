import pandas as pd
import os
import numpy as np

stats = pd.DataFrame()
codes = pd.read_csv("team_codes.csv")
records = pd.read_csv("records.csv")

base = "yearly_data/stats"

for item in os.listdir("yearly_data/stats"):
    stats = pd.concat([stats, pd.read_csv(base + "/" + item.__str__())])

stats = stats.drop([stats.columns.to_list()[0]], axis=1)
stats = stats.pivot_table(values='data', index=["season", "team"], columns="stat", aggfunc="first")

records = records.drop([records.columns.to_list()[0]], axis=1)
records = records.rename(columns={"Year": "season", "%": "percent"})
records = records.set_index(["season", "team"])

domo = stats.copy()
stats = stats.to_numpy()

for i in range(len(stats)):
    for j in range(len(stats[i])):
        temp = str(stats[i, j])
        temp.replace("%", "")
        if temp.__contains__("--"):
            print("nan")
            temp = "NaN"
        elif temp.__contains__("%"):
            temp = float(temp.split("%")[0]) / 100
        elif temp.__contains__(":"):
            temp = temp.split(":")
            temp = float(temp[0]) + (float(temp[1])/60)
        stats[i, j] = temp

domo[:] = stats
stats = domo
stats = pd.concat([stats, records])
stats.to_csv("temp.csv")