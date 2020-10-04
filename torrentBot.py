import logging, json
from torscraper2 import getTorrents, getAnimeTorrents
from telegram.ext import Updater, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent


# Your bot token here.
token = ''
updater = Updater(token, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def torrentsSearch(update, context):
    query = str(update.inline_query.query)
    if not query or (not query.startswith('t') and not query.startswith('a')) or len(query.split()) < 2:
        return
    flag = query.split(None, 1)[0]
    quer = query.split(None, 1)[1]
    print(query)
    print(quer)
    if flag == 't':
        tempres = json.loads(getTorrents(quer))
    else:
        tempres = json.loads(getAnimeTorrents(quer))
    if len(tempres) > 30:
        tempres = tempres[:30]
    results = list()
    if not tempres:
        results.append(
            InlineQueryResultArticle(
                id=1,
                title="No results found. Please refine search.",
                input_message_content=InputTextMessageContent(tempres)
            )
        )
    else:
        temp = 1
        for i in tempres:
            results.append(InlineQueryResultArticle(
                id=f'{quer.upper()}{temp}',
                title=i['Name'],
                input_message_content=InputTextMessageContent(i['Magnetlink'])
            ))
            temp = temp + 1
        print(results)
    context.bot.answer_inline_query(update.inline_query.id, results)

search_handler = InlineQueryHandler(torrentsSearch)
dispatcher.add_handler(search_handler)
updater.start_polling()