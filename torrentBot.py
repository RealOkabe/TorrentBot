import json, os, telegram, logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from torscraper import searchOn1337, searchOnNyaa, getMagnetFrom1337

# Your bot token here.
token = ''
bot = telegram.Bot(token)
id = ''
updater = Updater(token, use_context=True)
dispatcher = updater.dispatcher
fileName1337 = 'tor.json'
fileNameNyaa = 'animetor.json'

#logging to check for errors. These logs are not saved.
# logging.basicConfig(level=logging.DEBUG,
                    # format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Function that takes a query on telegram, searches for it on 1337x.to and returns the results to the user.
def search1337(update, context):
    if os.path.exists(fileNameNyaa):
        os.remove(fileNameNyaa)
    quer = update.message.text.split(None, 1)[1]
    id = update.message.chat_id
    results = searchOn1337(quer)
    if isinstance(results, str):
        bot.sendMessage(id, f"<b>{results}</b>", parse_mode="html")
    else:
        tors = 'Please select which torrent you would like to mirror: \n\n'
        count = 1
        for i in results.values():
            tors = tors + str(count) + '. ' + f"<code>{i['name']}</code>" + "\n<b>Seeders:</b> " + f"<code>{i['seeders']}</code>" + "\n<b>Leechers:</b> " + f"<code>{i['leechers']}</code>" + "\n<b>Date Added:</b> " + f"<code>{i['date_added']}</code>" + "\n<b>Size:</b> " + f"<code>{i['size']}</code>" + '\n\n'
            count = count + 1
        bot.sendMessage(id, tors, parse_mode="html")
        with open(fileName1337, 'w') as torFile:
            json.dump(results, torFile)

# Function that takes a query on telegram, searches for it on nyaa.si and returns the results to the user.
def searchNyaa(update, context):
    if os.path.exists(fileName1337):
        os.remove(fileName1337)
    quer = update.message.text.split(None, 1)[1]
    id = update.message.chat_id
    results = searchOnNyaa(quer)
    if isinstance(results, str):
        bot.sendMessage(id, f"<b>{results}</b>", parse_mode="html")
    else:
        tors = 'Please select the anime torrent whose magnet link you want: \n\n'
        count = 1
        for i in results.values():
            tors = tors + str(count) + '. ' + f"<code>{i['name']}</code>" + "\n<b>Seeders:</b> " + f"<code>{i['seeders']}</code>" + "\n<b>Leechers:</b> " + f"<code>{i['leechers']}</code>" + "\n<b>Date Added:</b> " + f"<code>{i['date_added']}</code>" + "\n<b>Size:</b> " + f"<code>{i['size']}</code>" + '\n\n'
            count = count + 1
        bot.sendMessage(id, tors, parse_mode="html")
        with open(fileNameNyaa, 'w') as torFile:
            json.dump(results, torFile)


# Function that takes a number message on telegram as user input and returns the magnet link of the torrent requested.
def sendMagnet(update, context):
    userChoice = update.message.text
    id = update.message.chat_id
    if os.path.exists(fileName1337):
        if userChoice.isdigit():
            torChoice = int(userChoice)
            if len(userChoice) <=2 and len(userChoice) > 0 and torChoice <= 10:
                with open(fileName1337) as torfile:
                    torrdata = list(json.load(torfile).values())
                msg = getMagnetFrom1337(torrdata[torChoice - 1]['url'])
                bot.sendMessage(id, msg)
                os.remove(fileName1337)
    elif os.path.exists(fileNameNyaa):
        if userChoice.isdigit():
            torChoice = int(userChoice)
            if len(userChoice) <=2 and len(userChoice) > 0 and torChoice <= 10:
                with open(fileNameNyaa) as torfile:
                    torrdata = list(json.load(torfile).values())
                msg = torrdata[torChoice - 1]['url']
                bot.sendMessage(id, msg)
                os.remove(fileNameNyaa)

if __name__ == '__main__':    
    handler1337 = CommandHandler('torrent', search1337)
    handlerNyaa = CommandHandler('animetorrent', searchNyaa)
    magnethandler = MessageHandler(Filters.text, sendMagnet)
    dispatcher.add_handler(handler1337)
    dispatcher.add_handler(handlerNyaa)
    dispatcher.add_handler(magnethandler)
    updater.start_polling()