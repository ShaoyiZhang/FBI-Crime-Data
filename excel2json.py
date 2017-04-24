import json
import pandas
import numpy as np
import re

def stateAbbDict():
    stateDict = {}
    with open('statesDict.txt') as f:
        for line in f.read().split('\n'):
            stateAbbr = line.strip().split(":")
            # print(stateAbbr)
            stateDict[stateAbbr[0].upper()] = stateAbbr[1].upper().strip()
    return stateDict

stateDict = stateAbbDict()
# print(stateDict)
df = pandas.read_excel(io='./Table_8_Offenses_Known_to_Law_Enforcement_by_State_by_City_2015.xls')
newHeader = df.iloc[2]
df = df[3:]

df.columns = newHeader

df = df.drop(df.index[range(-10,0)]) # deleting comments in EXEL

numOfCities = df.shape[0]

for i in range(1,df.shape[0]):
    if type(df.iloc[i]["State"]) != str:
        df.iloc[i]["State"] = df.iloc[i-1]["State"]
        #df.iloc[i]["City"] = re.findall(r"([a-zA-Z]*[\_?])*", df.iloc[i]["City"])[0]
        if re.search(r"[0-9]", df.iloc[i]["City"]) != None:
            df.iloc[i]["City"] = df.iloc[i]["City"][:-1]
    else:
        pass
    # dumb way?
df["State"] = df["State"].apply(lambda state: stateDict[state])

def getCriRate(row):
    try:
        return float(row['Violent\ncrime']) / row['Population'] * 100 #df.ix[1:10,'Population']
    except ZeroDivisionError:
        return 0.0

df['Crime Rate'] = df.apply(getCriRate, axis = 1)

avgCriRate = df.ix[:,'Crime Rate'].mean()
USPOP = df.ix[:,"Population"].sum()

df = df.sort_values(by=['Crime Rate','Population'], ascending = [True,False])
# df['Weighted Crime Rate'] = df['Crime Rate']
# df['Crime Index'] = df['Weighted Crime Rate']
df['Crime Ranking'] = np.nan
df['Crime Index'] = np.nan
popInSaferCities = 0.0
currentCriRate = 0.0

# calculate crime ranking & index by pop
for i in range(0,numOfCities): 
    # -1: Crime Index -2: Crime Ranking -3: Crime Rate
    df.iloc[i,-2] = "{0:.2f}".format((USPOP - popInSaferCities) / USPOP * 100)
    df.iloc[i,-3] = "{0:.2f}".format(df.iloc[i,-3])
    df.iloc[i,-1] = "{0:.2f}".format(float(df.iloc[i,-3]) / avgCriRate * 100)

    if currentCriRate != df.iloc[i,-2]:
        popInSaferCities +=  df.iloc[i]['Population']

df = df.drop(df.columns[range(4,14)], 1)
df = df.drop(["Population","Violent\ncrime"], 1)
print(df[9000:9005])

outDict = df.set_index('City').T.to_dict()
# print(outDict.keys())
out = json.dumps(outDict, sort_keys=True,indent=4, separators=(',', ': '))
with open('crimeByCity.json','w') as f:
    f.write(out)