import requests
import json

# Consuming COVID API from Brazil
# To Do: Filter by data 

def consumingData():
    dataRequest = requests.get('https://covid19.mathdro.id/api/countries/brazil/deaths')
    #import ipdb; ipdb.set_trace()
    dataJson = dataRequest.json()
    return dataJson