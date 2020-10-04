import requests

urltor = "https://torscraper.herokuapp.com/search1337/"
urlanime = "https://torscraper.herokuapp.com/searchNyaa/"

def getTorrents(query):
    rawdata = requests.get(urltor + query)
    return rawdata.text

def getAnimeTorrents(query):
    rawdata = requests.get(urlanime + query)
    return rawdata.text

print(getTorrents('Mahouka'))