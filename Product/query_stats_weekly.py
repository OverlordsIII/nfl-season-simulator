import io
from bs4 import BeautifulSoup as soup
import pandas as pd
import threading as th

df = pd.read_csv("week_dates.csv")

df = df[df['season'] == 2003]

links = []
base = "https://www.teamrankings.com"

# getting links from file
with io.open("data_urls.html", "r") as a:
    html = soup(a.read(), "html.parser")
    for i in html.find_all('a'):
        links.append(base + i.get('href', '/'))

endDates = df["end"].tolist()
statList = pd.DataFrame(data=None, columns=["season", "week", "team", 'stat', 'data'])

i = 0
j = len(endDates) * len(links)

def getstuff(link, endDate):
    statDf = pd.read_html(link + "?date=" + endDate)[0]
    statDf = statDf[[statDf.columns[1], statDf.columns[2]]]

    temp2 = df[df['end'] == endDate]
    season = temp2['season'][0]
    week = temp2['week'][0]

   # for index, row in statDf.iterrows():
   #    global season
   #    global week
   #    global link
   #    temptwo = [season, week].append([row["team"], str(link).split("/")[-1], row.iloc[-1], row[0])
   #    statList.loc[-1] = temptwo


for endDate in endDates:
    for link in links:
        print(str(i) + "/" + str(j))
        i = i + 1
        getstuff(link, endDate)

print(statList)



