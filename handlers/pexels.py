import logging
import random
import requests
import telegram
from handlers import stats
from secret import PEXELS_KEY
from telegram import Update
from telegram.ext import CallbackContext

logger = logging.getLogger()

def get_pexels(url, params):
    try:
        response = requests.get(
                url="https://api.pexels.com/v1/" + url,
                headers={
                    'Authorization': PEXELS_KEY,
                },
                params=params,
            )
        return response.json()
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        logger.warn('Got error in get_pexels: {}'.format(e))

def get_random_search(query):
    ind = random.randint(1, 1000)
    result = get_pexels('search', {
            'query': query,
            'per_page': 1,
            'page': ind,
        })
    while len(result['photos']) == 0 and result['total_results'] > 0:
        ind = random.randint(1, result['total_results'])
        result = get_pexels('search', {
                'query': query,
                'per_page': 1,
                'page': ind,
            })
    if len(result['photos']) > 0:
        return result['photos'][0]


def get_caption(res):
    return "[Photo]({}) by [{}]({})".format(res['url'], res['photographer'], res['photographer_url'])


def send_search_result(bot, chat_id, result):
    bot.send_photo(chat_id, photo=result['src']['medium'], caption=get_caption(result), parse_mode=telegram.ParseMode.MARKDOWN_V2)


@stats.handler
def cute_cat_handler(update: Update, context: CallbackContext):
    search_result =  get_random_search('cat')
    send_search_result(context.bot, update.effective_chat.id, search_result)

@stats.handler
def cute_dog_handler(update: Update, context: CallbackContext):
    search_result = get_random_search('dog')
    send_search_result(context.bot, update.effective_chat.id, search_result)

@stats.handler
def search_handler(update: Update, context: CallbackContext):
    q = ' '.join(context.args)
    if not q:
        context.bot.send_message(update.effective_chat.id, "Мне нечего искать!")
        return
    search_result = get_random_search(q)
    if search_result is None:
        context.bot.send_message(update.effective_chat.id, "Ничего не нашлось")
        return
    send_search_result(context.bot, update.effective_chat.id, search_result)
