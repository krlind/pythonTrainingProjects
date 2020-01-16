# import data form the 
import requests
import json

body = '{"expanded":true,"message":"","hakusana":"","laji":"y","vireillepv":["2020-01-01","2020-01-05"],"men_alkupv":[null,null],"valvonnatpv":[null,null],"velallisselvityspv":[null,null],"velkojain_kuulpv":[null,null],"vaatimuspv":[null,null],"lausumien_antpv":[null,null],"vaitteiden_esittpv":[null,null],"aanestyslausumat":[null,null],"velallisen_kuulempv":[null,null],"selvittaja":"","pesanhoitaja":""}'
header = {"content-type": "application/json"}
url = "https://maksukyvyttomyysrekisteri.om.fi/search"

responseIds = requests.post( url,  headers = header, data = body )
rawDataResponse = responseIds.json()

dataItems = []

def callExtractApi(id):
    urlExtract = "https://maksukyvyttomyysrekisteri.om.fi/extract"
    headerExtract = {"content-type": "application/json"}
    bodyX = {"id": id, "language": "fi"}
    print("results: ", bodyX)
    return requests.post( 
    urlExtract,  
    headers = headerExtract, 
    data = str(bodyX)
  )

for item in rawDataResponse["Y"]:
  dataItems.append( callExtractApi(item['id']).text )


print( dataItems[0] )
print( '-------------------------')
print( dataItems[1] )
