import io
from bs4 import BeautifulSoup as soup
import pandas as pd

df = pd.read_csv("week_dates.csv")

dfSeasons = df.groupby('season').last()
dfSeasons = dfSeasons.iloc[3:]
print(dfSeasons)

links = []
base = "https://www.teamrankings.com"

# getting links from file
with io.open("data_urls.html", "r") as a:
    html = soup(a.read(), "html.parser")
    for i in html.find_all('a'):
        links.append(base + i.get('href', '/'))

for link in links:
    print(link)
    # gonna comment out for now - testing purposes
    # for index, row in dfSeasons.iterrows():
    row = dfSeasons.iloc[-1] # just use 2023 stats for now, can use other seasons later
    dfPpg = pd.read_html(link + "?date=" + row['end'])[0]
    print(dfPpg)


