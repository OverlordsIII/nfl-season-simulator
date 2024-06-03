import pandas as pd
import threading as th

def getRecords(weeks, years):
    def getURL(year, week):
        base = "https://shrpsports.com/nfl/stand.php?link=Y&season="
        middle = "&divcnf=cnf&week=%20"
        return ("%s%s%s%s" % (base, year, middle, week))

    all = pd.DataFrame()

    for k in years:
        for i in weeks:
            df = pd.read_html(getURL(k, i))
            df = df[3:5]
            temp = pd.DataFrame()
            for j in df:
                j = j.drop(0)
                j = j.drop(1)
                j.columns = [x for x in range(len(j.columns))]
                j = j.rename(columns={2: "percent", 0: "team"})                
                for index in j.index:
                    elements = j['team'][index].split(" ")
                    if (elements.__contains__("Chargers") or elements.__contains__("Rams")):
                        elements = "LA " + elements[-1]
                    elif (elements.__contains__("Giants") or elements.__contains__("Jets")):
                        elements = "NY " + elements[-1]
                    elif (elements.__contains__("Oakland")):
                        elements = "Las Vegas"
                    else:
                        elements = " ".join(elements)
                    j.at[index, 'team'] = elements
                j.insert(0, column="season", value=([k] * len(j)))
                j.insert(1, column="week", value=([i] * len(j)))
                temp = pd.concat([temp, j])
                all = pd.concat([all, temp])
                

    all = all[["season", "week", "team", "percent"]]
    return all

stuff = pd.DataFrame()
dates = pd.read_csv("week_dates.csv")
datesMin = dates.groupby("season").max()["week"]
datesMax = dates.groupby("season").min()["week"]

def runner(i):
    global stuff
    stuff = pd.concat([stuff, getRecords([list(range(datesMin.loc[i], datesMax.loc[i]))], [i])])

# get everything (run at your own risk)
for i in range(2003, 2024):
    th.Thread(target=runner(i)).start()