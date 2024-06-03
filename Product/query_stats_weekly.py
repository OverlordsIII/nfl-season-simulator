import io
from bs4 import BeautifulSoup as soup
import pandas as pd
import threading as th

def getData(seasons, weeks):
    df = pd.read_csv("week_dates.csv")

    df = df[df["season"].isin(seasons)]
    df = df[df["week"].isin(weeks)]

    links = []
    base = "https://www.teamrankings.com"

    # getting links from file
    with io.open("data_urls.html", "r") as a:
        html = soup(a.read(), "html.parser")
        for i in html.find_all('a'):
            links.append(base + i.get('href', '/'))

    endDates = df["end"].tolist()
    statList = pd.DataFrame(data=None, columns=["season", "week", "team", 'stat', 'data'])

    def getstuff(link, endDate, statList, season):
        try:
            statDf = pd.read_html(link + "?date=" + endDate)[0]
            statDf = statDf[[statDf.columns[1], statDf.columns[2]]]

            statDf = statDf.rename(columns={statDf.columns.to_list()[-1]: "data", "Team": "team"})
            temp2 = df[df['end'] == endDate]
            season = temp2.index[0]
            week = temp2.iloc[0]['week']
            stat = str(link).split("/")[-1]

            statDf.insert(0, column="season", value=([season] * len(statDf)), )
            statDf.insert(1, column="week", value=([week] * len(statDf)))
            statDf.insert(2, column="stat", value=([stat] * len(statDf)))

            statList = pd.concat([statList, statDf], ignore_index=True)
            return statList
        except Exception as e:
            print(str(e), flush=True)
            return statList

    iterations = 1

    length = len(endDates)

    for endDate in endDates:
        i = 0
        j = len(links)
        for link in links:
            print(seasons)
            print(str(i) + "/" + str(j) + " - iteration " + str(iterations) + " of " + str(length), flush=True)
            i = i + 1
            statList = getstuff(link, endDate, statList, df[df["end"] == endDate].iloc[0]["season"])
        # statList.to_csv("yearly_data/stats/data_" + str(int(endDate.split("-")[0]) - 1) + ".csv")
        iterations = iterations + 1

    return statList

stuff = pd.DataFrame()
dates = pd.read_csv("week_dates.csv")
datesMin = dates.groupby("season").min()["week"]
datesMax = dates.groupby("season").max()["week"]

def runner(i):
    try:
        global stuff
        stuff = pd.concat([stuff, getData([i], list(range(datesMin.loc[i], datesMax.loc[i])))])
    except:
        stuff.to_csv("temp_alldata.csv")

# get everything (run at your own risk)
for i in range(2003, 2024):
    th.Thread(target=runner, args=(i,)).start()