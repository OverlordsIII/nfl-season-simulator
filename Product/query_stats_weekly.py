import io
from bs4 import BeautifulSoup as soup
import pandas as pd

df = pd.read_csv("week_dates.csv")

df = df.groupby('season').tail(2).groupby('season').first()

links = []
base = "https://www.teamrankings.com"

# getting links from file
with io.open("data_urls.html", "r") as a:
    html = soup(a.read(), "html.parser")
    for i in html.find_all('a'):
        links.append(base + i.get('href', '/'))

endDates = df["end"].tolist()
statList = pd.DataFrame(data=None, columns=["season", "week", "team", 'stat', 'data'])

# i = 0
# j = len(endDates) * len(links)

def getstuff(link, endDate):
    try:
        statDf = pd.read_html(link + "?date=" + endDate)[0]
        statDf = statDf[[statDf.columns[1], statDf.columns[2]]]

        statDf = statDf.rename(columns={statDf.columns.to_list()[-1]: "data", "Team": "team"})
        temp2 = df[df['end'] == endDate]
        season = temp2.index[0]
        week = temp2.iloc[0]['week']
        stat = str(link).split("/")[-1]

        global statList

        statDf.insert(0, column="season", value=([season] * len(statDf)), )
        statDf.insert(1, column="week", value=([week] * len(statDf)))
        statDf.insert(2, column="stat", value=([stat] * len(statDf)))

        statList = pd.concat([statList, statDf], ignore_index=True)
    except Exception as e:
        print(str(e))
        statList.to_csv("data.csv")

iterations = 1

for endDate in endDates:
    i = 0
    j = len(links)
    for link in links:
        print(str(i) + "/" + str(j) + " - iteration " + str(iterations) + " of " + str(len(endDates)))
        i = i + 1
        getstuff(link, endDate)
    statList.to_csv("yearly_data/stats/data_" + str(int(endDate.split("-")[0]) - 1) + ".csv")
    statList = statList.iloc[0:0]
    iterations = iterations + 1

print("done!")
#statList.to_csv("data.csv")