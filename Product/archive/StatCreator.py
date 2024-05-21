from io import StringIO

import pandas as pd
import requests
import lxml
import html5lib


if __name__ == '__main__':
  #  request = requests.get("https://www.pro-football-reference.com/years/2023/defense_advanced.htm")
  #  f = open("defense_advanced.html", "w")
  #  print(request.text, file=f)

  df = pd.read_html("defense_advanced.html")[0]
  print(df)

  for i in range(len(df)):
    pos = df.iloc[i, 4]
    team = df.iloc[i, 2].replace("LAC", "sdg")
    name = str(df.iloc[i, 1]).replace("*", "").replace("+", "")
    if pos == 'OLB' or pos == 'DE' or pos == 'DT' or pos == 'DL':
      hurry = df.iloc[i, 20]
      qbHit = df.iloc[i, 21]
      sacks = df.iloc[i, 22]
      pressures = df.iloc[i, 23]
      missedTackles = df.iloc[i, 25]

      url = "https://www.pro-football-reference.com/teams/" + str(team).lower() + "/2023-snap-counts.htm"

      df2 = pd.read_html(url)[0]
      snaps = 0

      for i in range(len(df2)):
        player = df2.iloc[i, 0]
        if player == name:
          snaps = df2.iloc[i, 4]

      ddi = (int(hurry) + int(qbHit) + float(sacks) + int(pressures) - int(missedTackles)) / snaps


      print(name, pos, hurry, qbHit, sacks, pressures, missedTackles, str(ddi * 100) + "%")



