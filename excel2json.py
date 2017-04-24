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

removeNonAlpha = re.compile('[^a-zA-Z,\ /]')
for i in range(1,df.shape[0]):
    if type(df.iloc[i]["State"]) != str:
        df.iloc[i]["State"] = df.iloc[i-1]["State"] # fill state column for all cities
        # if 'Village' in df.iloc[i]["City"]:
        #     # print(df.iloc[i]["City"])   
        #     temp = re.findall(r"[0-9]", df.iloc[i]["City"])
        #     # print(temp)         

        reObj = re.findall(r"[0-9]", df.iloc[i]["City"])
        if reObj != None and reObj != []:
            # print(df.iloc[i]["City"].dtype)
            # print(df.iloc[i]["City"])            
            # df.iloc[i]["City"] = df.iloc[i]["City"][:-1]
            df.iloc[i]["City"] = removeNonAlpha.sub('', df.iloc[i]["City"])         
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

df['Rate'] = df.apply(getCriRate, axis = 1)

# avgCriRate = df.ix[:,'Crime Rate'].mean()
# avgCriRate = df.ix[:,'Population'].sum() / (df.ix[:,'Violent\ncrime'].sum()/100000)
avgCriRate = 372.6 # https://ucr.fbi.gov/crime-in-the-u.s/2015/crime-in-the-u.s.-2015/tables/table-1
# print(avgCriRate)
# a = df.ix[:,'Population'].sum()
# b = df.ix[:,'Violent\ncrime'].sum()
# print(a)
# print(b)
# print(b/(a/100000))
USPOP = df.ix[:,"Population"].sum()

df = df.sort_values(by=['Rate','Population'], ascending = [True,False])
df['Ranking'] = np.nan
df['Index'] = np.nan
popInSaferCities = 0.0
currentCriRate = 0.0

# calculate crime ranking & index by pop
for i in range(0,numOfCities):
    df.iloc[i,1] = df.iloc[i,1] + ', ' + df.iloc[i,0] # City name, State name. Avoid key confliction
    # -1: Index -2: Ranking -3: Rate
    # Index:  Rate / mean Rate
    # Ranking: safter than % of people in U.S.
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
df['Num'] = df["Violent\ncrime"]
df = df.drop(["Population","Violent\ncrime","State"], 1)
# df['Index'] = range(0,numOfCities) # add index for city(json file need index)
outDict = df.set_index('City').T.to_dict()

for key,value in outDict.items():
    value['Rate'] = int(value['Rate'])
    value['Index'] = int(value['Index'])
    value['Ranking'] = float("{0:.2f}".format(value['Ranking']))
    # should try to avoid this loop
keys = outDict.keys()
for key in keys:
    outDict[removeNonAlpha.sub('',key)] = outDict.pop(key)
out = json.dumps(outDict, sort_keys=True,indent=4, separators=(',', ': '))
with open('crimeByCity.json','w') as f:
    f.write(out)


# df['Weighted Crime Rate'] = df['Crime Rate']
# df['Crime Index'] = df['Weighted Crime Rate']
print("Json file created: crimeByCity.json")

