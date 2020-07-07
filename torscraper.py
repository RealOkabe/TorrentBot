import requests
from bs4 import BeautifulSoup

url_nyaa = 'https://nyaa.si'
url_1337 = 'https://1337x.to'
user_agent = 'api'
headers =  {'User-Agent': user_agent}

# What contents does is that it converts the html inside a tag to a list of tags inside it

def searchOnNyaa(quer):
    search_url = f'{url_nyaa}/?f=0&c=1_2&q={quer.replace(" ", "+")}'
    r = requests.get(search_url, headers = headers)
    parsed = BeautifulSoup(r.text, "html.parser")

    # Don't know why but nyaa has these three classes for their torrents in trs
    usable_content = parsed.findAll('tr', {"class": {"default", "danger", "success"}})

    number_of_torrents = len(usable_content)

    if not number_of_torrents:
        return "No Results Found"
    # Limiting the number of torrents to 10 for convenience.
    if number_of_torrents > 10:
        usable_content = usable_content[:10]

    torrentList = {}
    count = 0

    for i in usable_content:
        temp_data = i.contents
        torrent_name = temp_data[3].contents
        torrent_name = torrent_name[3] if 'comment' in torrent_name[1]['title'] else torrent_name[1]
        torrent_name = torrent_name['title']
        torrent_link = temp_data[5].contents[3]['href']
        torrent_size = temp_data[7].text
        torrent_date_added = temp_data[9].text
        torrent_seeders = temp_data[11].text
        torrent_leechers = temp_data[13].text
        torrentList[f't{count}'] = {'name': torrent_name, 'url': torrent_link, 'seeders': torrent_seeders, 'leechers': torrent_leechers, 'date_added': torrent_date_added, 'size': torrent_size}
        count = count + 1

    return torrentList

def searchOn1337(quer):
    search_url = f"{url_1337}/search/{quer.replace(' ', '+')}/1/"
    r = requests.get(search_url, headers = headers)
    parsed = BeautifulSoup(r.text, "html.parser")

    # It turns out 1337x has all torrents in trs and the first tr has categories and such.
    usable_content = parsed.findAll('tr')
    
    number_of_torrents = len(usable_content)

    if not number_of_torrents:
        return "No Results Found"
    
    # Removed the tr that has categories and limited the number of torrents for convenience.
    if number_of_torrents > 10:
        usable_content = usable_content[1:11]

    torrentList = {}
    count = 0
    
    for i in usable_content:
        temp_data = i.contents
        torrent_name = temp_data[1].contents[1].text
        torrent_link = url_1337 + temp_data[1].contents[1]['href']
        torrent_seeders = temp_data[3].text
        torrent_leechers = temp_data[5].text
        torrent_date_added = temp_data[7].text
        torrent_size = temp_data[9].contents[0]

        torrentList[f't{count}'] = {'name': torrent_name, 'url': torrent_link, 'seeders': torrent_seeders, 'leechers': torrent_leechers, 'date_added': torrent_date_added, 'size': torrent_size}
        count = count + 1

    return torrentList

def getMagnetFrom1337(torUrl):
    r = requests.get(torUrl, headers = headers)
    usable_data = BeautifulSoup(r.text, 'html.parser').findAll('div', {'class': 'no-top-radius'})
    # Sorry for the complexity but this is the fastest way to parse to the magnet url of the torrent
    usable_data = usable_data[0].contents[1].contents[1].contents[1].contents[0]
    return usable_data['href']