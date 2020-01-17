# import data form the 
import requests
import json
import re
import pandas as pd

body = '{"expanded":true,"message":"","hakusana":"","laji":"y","vireillepv":["2020-01-01","2020-01-17"],"men_alkupv":[null,null],"valvonnatpv":[null,null],"velallisselvityspv":[null,null],"velkojain_kuulpv":[null,null],"vaatimuspv":[null,null],"lausumien_antpv":[null,null],"vaitteiden_esittpv":[null,null],"aanestyslausumat":[null,null],"velallisen_kuulempv":[null,null],"selvittaja":"","pesanhoitaja":""}'
header = {"content-type": "application/json"}
url = "https://maksukyvyttomyysrekisteri.om.fi/search"

responseIds = requests.post( url,  headers = header, data = body )
rawDataResponse = responseIds.json()

dataItems = []

def callExtractApi(id):
    urlExtract = "https://maksukyvyttomyysrekisteri.om.fi/extract"
    headerExtract = {"content-type": "application/json"}
    bodyX = {"id": id, "language": "fi"}
    return requests.post( 
    urlExtract,  
    headers = headerExtract, 
    data = str(bodyX)
  )

i = 0
jsonData = []

for item in rawDataResponse["Y"]:
  dataItems.append( callExtractApi(item['id']).text )
  data = re.findall( "(Listaus.|r)\>(.*?)\:\s{0,1}(.*?)<",  dataItems[i] )

  i = i + 1
  j = 0
  jsonObject = {}
  
  for items in data:
    itemReg = data[j][1]
    valueReg = data[j][2]

    j = j + 1

    jsonObject[itemReg] = valueReg 

  jsonData.append( jsonObject )
  
#print( json.dumps( jsonData, indent=4)   )
#print(  jsonData )

#######################################################################################
# write the data into excel
#######################################################################################

df = pd.DataFrame(jsonData) 

with pd.ExcelWriter('output.xlsx') as writer:  # doctest: +SKIP
  df.to_excel(writer, sheet_name='Output')

