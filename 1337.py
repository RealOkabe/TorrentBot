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

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def search1337(update, context):
    quer = update.message.text[8:]
    id = update.message.chat_id
    results = searchTor(quer)
    if isinstance(results, str):
        print(results)
        bot.sendMessage(id, results)
    else:
        tors = 'Please select which torrent you would like to mirror: \n\n'
        count = 1
        for i in results.values():
            tors = tors + str(count) + '. ' + i['name'] + "\nSeeders: " + i['seeders'] + "\nLeechers: " + i['leechers'] + "\nDate Added: " + i['date_added'] + "\nSize: " + i['size'] + '\n\n'
            count = count + 1
        bot.sendMessage(id, tors)
        with open(fileName, 'w') as torFile:
            json.dump(results, torFile)

def sendMagnet(update, context):
    userChoice = update.message.text
    id = update.message.chat_id
    if os.path.exists(fileName):
        if len(userChoice) <=2 and len(userChoice) > 0:
            if userChoice.isdigit():
                torChoice = int(userChoice)
                with open(fileName) as torfile:
                    torrdata = list(json.load(torfile).values())
                    print(torrdata)
                msg = getMagnet(torrdata[torChoice - 1]['url'])
                print(msg)
                bot.sendMessage(id, msg)
                os.remove(fileName)
        else:
            print(type(int(userChoice)))
            bot.sendMessage(id, 'Please send a valid number to select your torrent.')

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
    for i in range(0, len(nameList)):
        torData[f"t{i}"] = {"name": nameList[i].contents[1].text, "url": base_url + nameList[i].contents[1]['href'], "seeders": seedList[i].text, "leechers": leechList[i].text, "date_added": dateList[i].text, "size": sizeList[i].contents[0]}
    return torData

def getMagnet(torUrl):
    parsed = BeautifulSoup(requests.get(torUrl, headers = headers).text, 'html.parser').findAll('a')
    for i in parsed:
        temp = str(i['href'])
        if 'magnet' in temp:
            return(temp)

if __name__ == '__main__':    
    testhandler = CommandHandler('torrent', search1337)
    magnethandler = MessageHandler(Filters.text, sendMagnet)
    dispatcher.add_handler(testhandler)
    dispatcher.add_handler(magnethandler)
    updater.start_polling()
