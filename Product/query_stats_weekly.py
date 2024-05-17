import io
from bs4 import BeautifulSoup as soup
import pandas as pd

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

for endDate in endDates:
    for link in links:
        statDf = pd.read_html(link + "?date=" + endDate)[0]
        statList.append(statDf)

print(statList)


