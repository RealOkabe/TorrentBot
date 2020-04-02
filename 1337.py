import requests
#import urllib.request
#import time
from bs4 import BeautifulSoup



baseurl = 'https://1337x.to'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
headers =  {'User-Agent': user_agent}

# Function to search on 1337x.to
def searchtor(quer):

    # To check if the user's argument contains spaces and make url accordingly
    if len(quer.split(' ')) > 1:
        tempurl = baseurl + '/search/'
        for i in quer.split(' '):
            tempurl = tempurl + f'{i}+'
        tempurl = tempurl[:len(tempurl)-1] + '/1/'
    else:
        tempurl = baseurl + f'/search/{quer}/1/'

    res = requests.get(tempurl, headers = headers)

    if str(res) == '<Response [200]>' and res.text != '':
        # Finding all links
        parsed = BeautifulSoup(res.text, 'html.parser').findAll('a')

        # Check if no links were found
        if len(list(BeautifulSoup(res.text, 'html.parser').findAll('p'))) == 2:
            # return the text that is displayed on the website
            return(BeautifulSoup(res.text, 'html.parser').findAll('p')[0].getText())
        else:
            # Since first 35 a contain useless urls
            torList = []
            urlList = []
            for i in parsed:
                temp = str(i['href'])
                # To find the torrents
                if '/torrent/' in temp:
                    # Splitting the a href and getting the value
                    temp1 = str(i).split('>')[1].split('<')[0].replace('.', ' ')
                    torList.append(temp1)
                    urlList.append(baseurl + temp)


        return(dict(zip(torList, urlList)))
    else:
        return("It seems there is a problem with the bot please contact @RintarouOkabe")

def getMagnet(torUrl):
    parsed = BeautifulSoup(requests.get(torUrl, headers = headers).text, 'html.parser').findAll('a')
    for i in parsed:
        temp = str(i['href'])
        if 'magnet' in temp:
            return(temp)

a = input("Enter search query : ")
b = searchtor(a)
print(getMagnet(list(b.values())[1]))
