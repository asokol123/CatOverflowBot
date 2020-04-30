import logging
from telegram import Update
from telegram.ext import CallbackContext

logger = logging.getLogger()

def handler(func):
    def wrapper(update: Update, context: CallbackContext):
        msg = update.message.text
        user = update.effective_user
        username = user.username
        uid = user.id
        logger.info('username: {}, id: {}, msg: {}'.format(username, uid, msg))
        func(update, context)
    return wrapper

