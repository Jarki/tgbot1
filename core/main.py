import logging

from env import token
from env.allowed_chats import allowed_chats
from telegram_pybot.bot import Bot

logging.basicConfig(level=logging.INFO)

bot = Bot(token.token)
bot.set_webhook("https://fc34f8a91941.ngrok.io")

if len(allowed_chats) > 0:
    bot.ignore_disallowed_chats(True)

    for chat in allowed_chats:
        bot.allow_chat(int(chat))


def respond_ban(context):
    message = context["message"]["text"]
    message = message.split(' ')  # split the message to get arguments

    name = list(filter(lambda x: x != [], message))  # filter out the empty elements

    if len(name) <= 1:  # if len is <= 1, the number of args is insufficient
        return

    name = name[1]  # select the first argument

    responses = ["Banned ", " is now banned", "Successfully banned "]
    bot.send_message(context, f"Banned {name}")


bot.add_command('ban', respond_ban)

bot.run()

