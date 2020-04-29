#!/usr/bin/env python3
import logging
from handlers import overflow
from handlers import pexels
from secret import TOKEN
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update

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
/search cat dog - Хочу сначала картинок "cat", потом "dog"
/cat_gif - Хочу гифку с котиком!
/dog_gif - Хочу гифку с песиком!
    """
    context.bot.send_message(update.effective_chat.id, help_message)

dispatcher.add_handler(CommandHandler('start', help_handler))
dispatcher.add_handler(CommandHandler('help', help_handler))


dispatcher.add_handler(CommandHandler('cat_gif', overflow.cat_overflow_handler))
dispatcher.add_handler(CommandHandler('dog_gif', overflow.dog_overflow_handler))

dispatcher.add_handler(CommandHandler('cat', pexels.cute_cat_handler))
dispatcher.add_handler(CommandHandler('dog', pexels.cute_dog_handler))
dispatcher.add_handler(CommandHandler('search', pexels.search_handler))


updater.start_polling()
