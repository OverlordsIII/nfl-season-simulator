import io
from bs4 import BeautifulSoup as soup
import pandas as pd
import threading as th
import sys
import time

df = pd.read_csv("week_dates.csv")

links = []
base = "https://www.teamrankings.com"

# getting links from file
with io.open("data_urls.html", "r") as a:
    html = soup(a.read(), "html.parser")
    for i in html.find_all('a'):
        links.append(base + i.get('href', '/'))

endDates = df["end"].tolist()
tempList = df.columns.tolist()
tempList.append("Team")
tempList = tempList + list(map(lambda x: str(x).split("/")[-1], links))
statList = pd.DataFrame(tempList)
print(tempList)

i = 0
j = len(endDates) * len(links)

def plusOne():
    i+=1
    print(str(i) + "/" + str(j))

def getstuff(link, end):
    global statList
    statDf = pd.read_html(link + "?date=" + end)[0]
    tempYear = df.loc[df["end"] == end]["season"]
    statDf = statDf[["Team", str(tempYear)]]
    tempWeek = df.loc[df["end"] == end]["week"]
    statDf.assign(year=tempYear, week=tempWeek)
    statList = statList.combine(statDf)
    print(statList, flush=True)
    plusOne()

class GetThread(th.Thread):
    tasks = []
    def __init__(self, tasks):
        th.Thread.__init__(self)
        self.tasks = tasks
    
    def run(self):
        for i in self.tasks:
            i.run()
            time.sleep(1)
        sys.exit()

class Get():
    link = ""
    endDate = ""
    def __init__(self, link, enddate):
        self.link = link
        self.endDate = enddate
    
    def run(self):
        try:
            i.run()
        except Exception as e:
            print(str(e), flush=True)
            statList.to_csv("data_2003.csv")
        getstuff(link, endDate)

queue = []
threads = []
threadcount = 100

for endDate in endDates:
    for link in links:
        queue.append(Get(link, endDate))

while not len(queue) == 0:
    temp = []
    for i in range(threadcount):
        if len(queue) == 0:
            break
        temp.append(queue.pop())
    GetThread(temp).start()

statList.to_csv("data_2003.csv")