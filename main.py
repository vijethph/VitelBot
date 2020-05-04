# python telegram bot
# done by Vijeth P H

import logging
import os
import random
import sys
import requests
import re

from telegram.ext import Updater, CommandHandler

# Enabling logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Getting mode, so we could define run function for local and Heroku setup
mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")
if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)


def start_handler(bot, update):
    # Creating a handler-function for /start command 
    logger.info("User {} started bot".format(update.effective_user["id"]))
    update.message.reply_text("Hello from Python!\nPress /random to get random number")


def random_handler(bot, update):
    # Creating a handler-function for /random command
    number = random.randint(0, 100)
    logger.info("User {} randomed number {}".format(update.effective_user["id"], number))
    update.message.reply_text("Random number: {}".format(number))

def get_url():
    # A part of handler function that gets dog pics 
    contents = requests.get('https://random.dog/woof.json').json()    
    url = contents['url']
    return url

def dog_handler(bot, update):
    # A handler function for /dog command
    url = get_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)
    
def joke_handler(bot,update):
    # A handler function for /joke command
    headd={'Accept':'application/json'}
    response=requests.get('https://icanhazdadjoke.com/',headers=headd)
    update.message.reply_text(response.json()['joke'])
    
def meme_handler(bot,update):
    # A handler function for /meme command
    respd=requests.get('https://api.imgflip.com/get_memes')
    url=respd.json()['data']['memes'][1]['url']
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)
    
def cat_handler(bot,update):
    # A handler function for /cat command
    respnsed=requests.get('http://aws.random.cat/meow')
    url=respnsed.json()['file']
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)

if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(CommandHandler("random", random_handler))
    updater.dispatcher.add_handler(CommandHandler("dog",dog_handler))
    updater.dispatcher.add_handler(CommandHandler("cat",cat_handler))
    updater.dispatcher.add_handler(CommandHandler("meme",meme_handler))
    updater.dispatcher.add_handler(CommandHandler("joke",joke_handler))

    run(updater)


