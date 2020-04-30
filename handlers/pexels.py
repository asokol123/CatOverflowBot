import logging
import random
import requests
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
        result = get_pexels(search, {
                'query': query,
                'per_page': 1,
                'page': ind,
            })
    if len(result['photos']) > 0:
        return result['photos'][0]


@stats.handler
def cute_cat_handler(update: Update, context: CallbackContext):
    context.bot.send_photo(update.effective_chat.id, photo=get_random_search('cat')['src']['medium'])

@stats.handler
def cute_dog_handler(update: Update, context: CallbackContext):
    context.bot.send_photo(update.effective_chat.id, photo=get_random_search('dog')['src']['medium'])

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
    context.bot.send_photo(update.effective_chat.id, photo=search_result['src']['medium'])
