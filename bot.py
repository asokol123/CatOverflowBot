#!/usr/bin/env python3
from secrets import TOKEN
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
import logging
import random
import requests

max_offset = {'cat': 369, 'dog': 106}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger()
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


def help_handler(update: Update, context: CallbackContext):
    help_message = """
/help - Показать это сообщение
/cat - Хочу котика!
/dog - Хочу песика!
    """
    context.bot.send_message(update.effective_chat.id, help_message)
dispatcher.add_handler(CommandHandler('start', help_handler))
dispatcher.add_handler(CommandHandler('help', help_handler))

def get_from_url(url):
    try:
        return requests.get(url, verify=False).text
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        logger.warn('Got error: {}'.format(e))

def cat_handler(update: Update, context: CallbackContext):
    offset = random.randint(0, max_offset['cat'])
    url = get_from_url('https://catoverflow.com/api/query/?offset={}&limit={}'.format(offset, 1))
    if url is None:
        message = "Failed to get cat. Sorry"
    else:
        message = url
    context.bot.send_message(update.effective_chat.id, message)
dispatcher.add_handler(CommandHandler('cat', cat_handler))

def dog_handler(update: Update, context: CallbackContext):
    offset = random.randint(0, max_offset['dog'])
    url = get_from_url('https://dogoverflow.com/api/query/?offset={}&limit={}'.format(offset, 1))
    if url is None:
        message = "Failed to get dog. Sorry"
    else:
        message = url
    context.bot.send_message(update.effective_chat.id, message)
dispatcher.add_handler(CommandHandler('dog', dog_handler))


updater.start_polling()