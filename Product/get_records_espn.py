import pandas as pd


base = "https://www.jt-sw.com/football/pro/standings.nsf/Seasons/"
end = ""

def getURL(year):
    return ("%s%s" % (base, year))

start = 2003
end = 2023
all = pd.DataFrame()
years = [0] * (end-start)

for i in range(len(years)):
    years[i] = start + i

for k in years:
    df = pd.read_html(getURL(k))
    df = list(filter(lambda x: "PF" in x.columns, df))
    temp = pd.DataFrame()
    print(df)
    
    for j in df:
        j = j.rename(columns={j.columns.to_list()[0]: "team"})
        j.insert(0, column="Year", value=([k] * len(j)))
        temp = pd.concat([temp, j])
    all = pd.concat([all, temp])

all = all[["Year", "team", "%"]]
all.to_csv("records.csv")