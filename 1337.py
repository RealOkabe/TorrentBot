import requests, json, os, telegram, logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from bs4 import BeautifulSoup



base_url = 'https://1337x.to'
user_agent = 'api'
headers =  {'User-Agent': user_agent}

# Your bot token here.
token = ''
bot = telegram.Bot(token)
id = ''
updater = Updater(token, use_context=True)
dispatcher = updater.dispatcher
fileName = 'tor.json'

#logging to check for errors. These logs are not saved.
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Function to search on 1337x.to
def searchTor(quer):
    search_url = f"{base_url}/search/{quer.replace(' ', '+')}/1/"
    headers = {"User-Agent" : "api"}
    r = requests.get(search_url, headers = headers)
    parsed = BeautifulSoup(r.text, "html.parser")
    nameList = parsed.findAll('td', {"class": "name"})
    if not len(nameList):
        msg = parsed.find('div', {'class': 'box-info-detail'}).text
        return msg
    seedList = parsed.findAll('td', {"class": "seeds"})
    leechList = parsed.findAll('td', {"class": "leeches"})
    dateList = parsed.findAll('td', {"class": "coll-date"})
    sizeList = parsed.findAll('td', {"class": "size"})
    torData = {}
    llen = len(nameList)
    if llen > 10:
    	llen = 10
    for i in range(0, llen):
        torData[f"t{i}"] = {"name": nameList[i].contents[1].text, "url": base_url + nameList[i].contents[1]['href'], "seeders": seedList[i].text, "leechers": leechList[i].text, "date_added": dateList[i].text, "size": sizeList[i].contents[0]}
    return torData

# Function to get the magnet link for a torrent url.
def getMagnet(torUrl):
    parsed = BeautifulSoup(requests.get(torUrl, headers = headers).text, 'html.parser').findAll('a')
    for i in parsed:
        temp = str(i['href'])
        if 'magnet' in temp:
            return(temp)

# Function that takes a query on telegram, searches for it on 1337x.to and returns the results to the user.
def search1337(update, context):
    quer = update.message.text[8:]
    id = update.message.chat_id
    results = searchTor(quer)
    if isinstance(results, str):
        bot.sendMessage(id, f"<b>{results}</b>", parse_mode="html")
    else:
        tors = 'Please select which torrent you would like to mirror: \n\n'
        count = 1
        for i in results.values():
            tors = tors + str(count) + '. ' + f"<code>{i['name']}</code>" + "\n<b>Seeders:</b> " + f"<code>{i['seeders']}</code>" + "\n<b>Leechers:</b> " + f"<code>{i['leechers']}</code>" + "\n<b>Date Added:</b> " + f"<code>{i['date_added']}</code>" + "\n<b>Size:</b> " + f"<code>{i['size']}</code>" + '\n\n'
            count = count + 1
        bot.sendMessage(id, tors, parse_mode="html")
        with open(fileName, 'w') as torFile:
            json.dump(results, torFile)

# Function that takes a number message on telegram as user input and returns the magnet link of the torrent requested.
def sendMagnet(update, context):
    userChoice = update.message.text
    id = update.message.chat_id
    if os.path.exists(fileName):
        if userChoice.isdigit():
        	torChoice = int(userChoice)
            if len(userChoice) <=2 and len(userChoice) > 0 and torChoice <= 10:
                with open(fileName) as torfile:
                    torrdata = list(json.load(torfile).values())
                    print(torrdata)
                msg = getMagnet(torrdata[torChoice - 1]['url'])
                bot.sendMessage(id, msg)
                os.remove(fileName)
        else:
            bot.sendMessage(id, '<b>Please send a valid number to select your torrent.</b>', parse_mode="html")

if __name__ == '__main__':    
    testhandler = CommandHandler('torrent', search1337)
    magnethandler = MessageHandler(Filters.text, sendMagnet)
    dispatcher.add_handler(testhandler)
    dispatcher.add_handler(magnethandler)
    updater.start_polling()
