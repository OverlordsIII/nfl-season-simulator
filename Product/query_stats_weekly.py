import io
from bs4 import BeautifulSoup as soup
import pandas as pd
import threading as th

df = pd.read_csv("week_dates.csv")

links = []
base = "https://www.teamrankings.com"

# getting links from file
with io.open("data_urls.html", "r") as a:
    html = soup(a.read(), "html.parser")
    for i in html.find_all('a'):
        links.append(base + i.get('href', '/'))

endDates = df["end"].tolist()
statList = []

i = 0
j = len(endDates) * len(links)

def getstuff(link):
    statDf = pd.read_html(link + "?date=" + endDate)[0]
    statList.append([statDf.iloc[1].tolist(), statDf.iloc[2]])

for endDate in endDates:
    for link in links:
        th.Thread(target=getstuff, args=(link,)).start()



