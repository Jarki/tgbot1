import logging

from env import token
from telegram_pybot.bot import Bot

logging.basicConfig(level=logging.INFO)

bot = Bot(token.token)
bot.api_interactor.set_webhook("https://6ccb462f9cd6.ngrok.io")


def respond_start(context):
    bot.api_interactor.send_message(context, "bruh")


bot.add_command('start', respond_start)

bot.run(__name__)

