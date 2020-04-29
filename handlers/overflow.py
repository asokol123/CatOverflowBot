import logging
import random
import requests
from telegram import Update
from telegram.ext import CallbackContext

logger = logging.getLogger()
urls = {}


def get_from_url(url):
    try:
        return requests.get(url, verify=False).text
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        logger.warn('Got error: {}'.format(e))

def cat_overflow_handler(update: Update, context: CallbackContext):
    if 'cat' not in urls or not urls['cat']:
        urls['cat'] = get_from_url('https://catoverflow.com/api/query/').rstrip().split('\n')
    context.bot.send_message(update.effective_chat.id, random.choice(urls['cat']))

def dog_overflow_handler(update: Update, context: CallbackContext):
    if 'dog' not in urls or not urls['dog']:
        urls['dog'] = get_from_url('https://dogoverflow.com/api/query/').rstrip().split('\n')
    context.bot.send_message(update.effective_chat.id, random.choice(urls['dog']))
