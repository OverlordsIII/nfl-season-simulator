import pandas as pd
import datetime as dt
from bs4 import BeautifulSoup as soup
import io

retrieve = []
dates = pd.read_csv("week_dates.csv")

# # get who played on the day after

# for index, row in games.iterrows():
#     date = (dt.datetime.strptime(row["gameday"], "%Y-%m-%d")) - dt.timedelta(days=1)
#     if not list(map(lambda x: x[0], retrieve)).__contains__(date):
#         retrieve.append([date, [row["home_team"], row["away_team"]]])
#     else:
#         temp = next(a for a in retrieve if a[0] == date)[1]
#         if not temp.__contains__(row["away_team"]):
#             temp.append(row["away_team"])
#         if not temp.__contains__(row["home_team"]):
#             temp.append(row["home_team"])

links = []
base = "https://www.teamrankings.com"

# getting links from file
with io.open("data_urls.html", "r") as a:
    html = soup(a.read(), "html.parser")
    for i in html.find_all('a'):
        links.append(base + i.get('href', '/'))


# retrieve = list(map(lambda x: [list(map(lambda y: y+"?date="+x[0].strftime("%Y-%m-%d"), links)), x[1]], retrieve))

# temp = []
# for x in retrieve:
#     for y in x[0]:
#         temp.append(y)

print(len(links))

# print(len(base) * 32 * 18)
# print(len(temp))
# print(len(set(temp)))
