# import data form the 
import requests
import json
import re
import pandas as pd


def callSearchApi():
	body = '{"expanded":true,"message":"","hakusana":"","laji":"y","vireillepv":["2020-01-01","2020-01-05"],"men_alkupv":[null,null],"valvonnatpv":[null,null],"velallisselvityspv":[null,null],"velkojain_kuulpv":[null,null],"vaatimuspv":[null,null],"lausumien_antpv":[null,null],"vaitteiden_esittpv":[null,null],"aanestyslausumat":[null,null],"velallisen_kuulempv":[null,null],"selvittaja":"","pesanhoitaja":""}'
	header = {"content-type": "application/json"}
	url = "https://maksukyvyttomyysrekisteri.om.fi/search"

	responseIds = requests.post(url,  
															headers=header, 
															data = body
															)

	return parseData(responseIds.json())


def callExtractApi(id):
    urlExtract = "https://maksukyvyttomyysrekisteri.om.fi/extract"
    headerExtract = {"content-type": "application/json"}
    bodyX = {"id": id, "language": "fi"}
    return requests.post( 
												urlExtract,  
												headers = headerExtract, 
												data = str(bodyX)
  )

def parseData(rawDataResponse):
	i = 0
	jsonData = []
	dataItems = []

	for item in rawDataResponse["Y"]:
		dataItems.append( callExtractApi(item['id']).text )
		data = re.findall( "(<p class=.Listaus.|r)\>(.*?)\:\s{0,2}(.*?)<",  dataItems[i] )

		#(<div class=)(?!<p class=.Listaus.>YSL.*?)
		#(<p class=.Listaus.|r)\>(.*?)\:\s{0,2}(.*?)<

		print('---------------------------------------------')
		print(dataItems)
		print('---------------------------------------------')

		i = i + 1
		j = 0
		jsonObject = {}
		
		for items in data:
			itemReg = data[j][1]
			valueReg = data[j][2]
			j = j + 1
			jsonObject[itemReg] = valueReg 

		jsonData.append( jsonObject )
	return jsonData
  



#print( json.dumps( jsonData, indent=4)   )
#print(  jsonData )

#######################################################################################
# write the data into excel
#######################################################################################

#df = pd.DataFrame(jsonData) 

#with pd.ExcelWriter('output.xlsx') as writer:  # doctest: +SKIP
#  df.to_excel(writer, sheet_name='Output')

