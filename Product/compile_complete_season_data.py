import pandas as pd
import os
import numpy as np

stats = pd.DataFrame()
codes = pd.read_csv("team_codes.csv")
records = pd.read_csv("records.csv")

base = "yearly_data/stats"

def compile_temp_file(years, statistics, new_records, rewrite_records):
    global codes, base
    for item in years:
        statistics = pd.concat([statistics, pd.read_csv(base + "/" + "data_" + item.__str__() + ".csv")])

    statistics = statistics.drop([statistics.columns.to_list()[0]], axis=1)
    statistics = statistics.pivot_table(values='data', index=["season", "team"], columns="stat", aggfunc="first")

    if rewrite_records:
        new_records = new_records.drop([new_records.columns.to_list()[0]], axis=1)
        new_records = new_records.rename(columns={"Year": "season", "%": "percent"})
        new_records = new_records.set_index(["season", "team"])

    domo = statistics.copy()
    statistics = statistics.to_numpy()

    for i in range(len(statistics)):
        for j in range(len(statistics[i])):
            temp = str(statistics[i, j])
            temp.replace("%", "")
            if temp.__contains__("--"):
                print("nan")
                temp = "NaN"
            elif temp.__contains__("%"):
                temp = float(temp.split("%")[0]) / 100
            elif temp.__contains__(":"):
                temp = temp.split(":")
                temp = float(temp[0]) + (float(temp[1])/60)
            statistics[i, j] = temp

    domo[:] = statistics
    statistics = domo
    statistics = statistics.join(new_records, on=["season", "team"])
    statistics = pd.concat([statistics] * 3)
    return statistics

def create_old_temp_file(stats, records):
    stats = compile_temp_file(list(range(2003, 2023)), stats, records, True)
    stats.to_csv("temp.csv")