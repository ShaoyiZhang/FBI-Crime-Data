import json
import pandas
import numpy as np
import re

def stateAbbDict():
    stateDict = {}
    with open('statesDict.txt') as f:
        for line in f.read().split('\n'):
            stateAbbr = line.strip().split(":")
            stateDict[stateAbbr[0].upper()] = stateAbbr[1].upper().strip()
    return stateDict

stateDict = stateAbbDict()

# Cleaning
print("Generating Json file from xls file")
filename = './Table_8_Offenses_Known_to_Law_Enforcement_by_State_by_City_2015.xls'
df = pandas.read_excel(io = filename)
newHeader = df.iloc[2]
df = df[3:] # delete xls header
df.columns = newHeader
df = df.drop(df.index[range(-10,0)]) # deleting comments in EXEL
numOfCities = df.shape[0]

for i in range(1,df.shape[0]):
    if type(df.iloc[i]["State"]) != str:
        df.iloc[i]["State"] = df.iloc[i-1]["State"] # fill state column for all cities
        if re.search(r"[0-9]", df.iloc[i]["City"]) != None:
            df.iloc[i]["City"] = df.iloc[i]["City"][:-1]
            # solve issue "Santa Barbara5"
    else:
        pass
    # dumb way?
df["State"] = df["State"].apply(lambda state: stateDict[state])

# Calculate violent crime rate for each city in df
# number of violent crimes occured for 100k people every year 
# violent crime rate = # of violent crimes/ (city pop * 100000)
def getCriRate(row):
    try:
        return row['Violent\ncrime'] / (row['Population'] / 100000) #df.ix[1:10,'Population']
    except ZeroDivisionError:
        return 0

df['Crime Rate'] = df.apply(getCriRate, axis = 1)

avgCriRate = df.ix[:,'Crime Rate'].mean()
USPOP = df.ix[:,"Population"].sum()

df = df.sort_values(by=['Crime Rate','Population'], ascending = [True,False])
df['Crime Ranking'] = np.nan
df['Crime Index'] = np.nan
popInSaferCities = 0.0
currentCriRate = 0.0

# calculate crime ranking & index by pop
for i in range(0,numOfCities): 
    # -1: Crime Index -2: Crime Ranking -3: Crime Rate
    # Crime Index: Crime Rate / mean Crime Rate
    # Crime Ranking: safter than % of people in U.S.
    df.iloc[i,-2] = (USPOP - popInSaferCities) / USPOP * 100
    try:
        df.iloc[i,-3] = int(df.iloc[i,-3])
    except:
        # missing data in violent crime column, set to zero 
        df.iloc[i,-3] = 0

    df.iloc[i,-1] = float(df.iloc[i,-3]) / avgCriRate * 100

    if currentCriRate != df.iloc[i,-2]:
        popInSaferCities +=  df.iloc[i]['Population']
df = df.drop(df.columns[range(4,14)], 1)
df = df.drop(["Population","Violent\ncrime"], 1)
df['Index'] = range(0,numOfCities) # add index for city(json file need index)
outDict = df.set_index('City').T.to_dict()

for key,value in outDict.items():
    value['Crime Rate'] = int(value['Crime Rate'])
    value['Crime Index'] = int(value['Crime Index'])
    value['Crime Ranking'] = float("{0:.2f}".format(value['Crime Ranking']))
    # should try to avoid this loop
out = json.dumps(outDict, sort_keys=True,indent=4, separators=(',', ': '))
with open('crimeByCity.json','w') as f:
    f.write(out)


# df['Weighted Crime Rate'] = df['Crime Rate']
# df['Crime Index'] = df['Weighted Crime Rate']
print("Json file created: crimeByCity.json")