import pandas as pd


from compile_complete_season_data import compile_temp_file
from os.path import exists
from nan_remover import remove_nans

stats = pd.DataFrame()
records = pd.DataFrame() # provided week data is added to week_dates.csv
# records comes from query_records_weekly.py, use that to query properly
# stats comes from query_stats_weekly.py, use that to query properly
def compile_files(year):
    global stats, records
    stats = pd.read_csv(f"yearly_data/stats/data_{year}.csv")
    records = pd.read_csv(f"records_{year}.csv")

compile_files(2024)
tempfile = compile_temp_file([2024], stats, records, True)
tempfile = tempfile[~tempfile.index.duplicated(keep='first')]
tempfile = remove_nans(tempfile)
tempfile.to_csv("temp2024w5.csv", index=False)