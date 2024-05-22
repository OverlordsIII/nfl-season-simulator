import pandas as pd

base = "https://www.jt-sw.com/football/pro/standings.nsf/Seasons/"
end = ""

def getURL(year):
    return ("%s%s" % (base, year))

start = 2003
end = 2024
all = pd.DataFrame()
years = [0] * ((end)-start)

for i in range(len(years)):
    years[i] = start + i

for k in years:
    df = pd.read_html(getURL(k))
    df = list(filter(lambda x: "PF" in x.columns, df))
    temp = pd.DataFrame()
    print(df)
    
    for j in df:
        j = j.rename(columns={j.columns.to_list()[0]: "team"})
        for index in j.index:
            elements = j['team'][index].split(" ")
            if (elements.__contains__("Chargers") or elements.__contains__("Rams")):
                elements = "LA " + elements[-1]
            elif (elements.__contains__("Giants") or elements.__contains__("Jets")):
                elements = "NY " + elements[-1]
            else:
                elements = elements[:-1]
                elements = " ".join(elements)
            j.at[index, 'team'] = elements

        j.insert(0, column="Year", value=([k] * len(j)))
        temp = pd.concat([temp, j])
    all = pd.concat([all, temp])

all = all[["Year", "team", "%"]]
all.to_csv("records.csv")