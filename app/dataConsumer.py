import requests
import json

from requests.api import request
import app.initials as ini


# Consuming COVID API from Brazil
# To Do: Filter by data 
baseurl = 'https://covid19.mathdro.id/api'
def consumingData():
    dataRequest = requests.get(f'{baseurl}/countries/brazil/deaths')
    dataJson = dataRequest.json()
    treatedData = jsonToDict(dataJson)
    return treatedData


#Check if the date on url is the same of the API
def consumingDataPerDate(date):
    #import ipdb; ipdb.set_trace()
    dataRequest = requests.get(f'{baseurl}/daily/{date}')
    dataJson = dataRequest.json()
    return filterBrazil(dataJson)


#Store data in [blank] dictionary 
def jsonToDict(dataJson):

    dictStates = {}

    for row in dataJson:
        state = row['provinceState']
        dictStates[ini.initialStates[state]] = {
            'estado' : row['provinceState'],
            'confirmados' : row['confirmed'],
            'recuperados' : row['recovered'],
            'mortos' : row['deaths'],
            'casos ativos' : row['active']
        }
    #import ipdb; ipdb.set_trace()
    return dictStates


def filterBrazil(dataJson):
    dictStates = {}

    for row in dataJson:
        if row['countryRegion'] == 'Brazil':
            state = row['provinceState']
            dictStates[ini.initialStates[state]] = {
                'estado' : row['provinceState'],
                'confirmados' : row['confirmed'],
                'recuperados' : row['recovered'],
                'mortos' : row['deaths'],
                'casos ativos' : row['active']
            }
            #import ipdb; ipdb.set_trace()
    return dictStates