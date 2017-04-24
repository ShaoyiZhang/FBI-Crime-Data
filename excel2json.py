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
print(stateDict)
df = pandas.read_excel(io='./Table_8_Offenses_Known_to_Law_Enforcement_by_State_by_City_2015.xls')
newHeader = df.iloc[2]#.append('Crime Rate')
df = df[3:]
#df['Crime Rate'] = df.ix['Population']
#print(newHeader)
df.columns = newHeader
#print(df[:10])
df = df.drop(df.index[range(-10,0)]) # deleting comments in EXEL
# print(df[-12:])
numOfCities = df.shape[0]
# print(type(df.iloc[0]["State"]))
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
#totalVio = df[df.columns[3:4]].sum()
#totalVioRate = df[df.columns[3:4]].sum()/
#avgVio = float(totalVio) / df.shape[0]
#print(avgVio)
def getCriRate(row):
    try:
        return float(row['Violent\ncrime']) / row['Population'] * 100 #df.ix[1:10,'Population']
    except ZeroDivisionError:
        return 0.0

df['Crime Rate'] = df.apply(getCriRate, axis = 1)
#try:
#    df['Crime Rate'] = df['Violent\ncrime'] / df['Population']
#except:
#    pass
#print(df.loc[df[''] == 0])
# print(df.columns)
#df['Crime Index'] = df['Violent\ncrime'] / avgVio
# print(df[:10])
# print((df[:,'Population':'Population']))
avgCriRate = df.ix[:,'Crime Rate'].mean()
USPOP = df.ix[:,"Population"].sum()
#df['Crime Index'] = df['Crime Rate'] / avgCriRate * 100

df = df.sort_values(by=['Crime Rate','Population'], ascending = [True,False])
# df['Weighted Crime Rate'] = df['Crime Rate']
# df['Crime Index'] = df['Weighted Crime Rate']
df['Crime Ranking'] = np.nan#df['Crime Rate']
df['Crime Index'] = np.nan
popInSaferCities = 0.0
currentCriRate = 0.0
# calculate crime index by pop
for i in range(0,numOfCities):
    # df.iloc[i]['Crime Index'] 
    
    df.iloc[i,-2] = "{0:.2f}".format((USPOP - popInSaferCities) / USPOP * 100)
    df.iloc[i,-3] = "{0:.2f}".format(df.iloc[i,-3])
    df.iloc[i,-1] = "{0:.2f}".format(float(df.iloc[i,-3]) / avgCriRate * 100)
    # print(df.iloc[i:i+1])
    if currentCriRate != df.iloc[i,-2]:
        popInSaferCities +=  df.iloc[i]['Population']
    # print(df.iloc[i]['Crime Index'])
    # print(i)
# print(df[:10])

# df['Crime Rate Ranking'] = range(0,numOfCities)

# df['Crime Rate Ranking'] = float(df['Crime Rate Ranking']) / numOfCities
df = df.drop(df.columns[range(4,14)], 1)
df = df.drop(["Population","Violent\ncrime"], 1)
print(df[9000:9005])

outDict = df.set_index('City').T.to_dict()
# print(outDict.keys())
out = json.dumps(outDict, sort_keys=True,indent=4, separators=(',', ': '))
with open('crimeByCity.json','w') as f:
    f.write(out)

'''
out = df.to_json()#(orient = 'records')
#out = json.dumps(out, sort_keys=True,indent=4, separators=(',', ': '))
with open('crimeByCity.json','w') as f:
    f.write(out)
'''
