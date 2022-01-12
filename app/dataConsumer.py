import requests
from requests.api import request
import app.initials as ini


# Consuming COVID API from Brazil
baseurl = 'https://covid19.mathdro.id/api'


#Check if the date on url is the same of the API
def consumingDataPerDate(date):
    dataRequest = requests.get(f'{baseurl}/daily/{date}')
    dataJson = dataRequest.json()
    return filterBrazil(dataJson)


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
    return dictStates