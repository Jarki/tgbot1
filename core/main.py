import logging

from env import token
from env.allowed_chats import allowed_chats
from env import server_config
from env import db_credentials
from database_interactor import DBInteractor
from telegram_pybot.bot import Bot

logging.basicConfig(level=logging.INFO)

bot = Bot(token.token)
bot.set_webhook("https://5982bd18516b.ngrok.io")

if len(allowed_chats) > 0:
    bot.ignore_disallowed_chats(True)

    for chat in allowed_chats:
        bot.allow_chat(int(chat))

db = DBInteractor(db_credentials.username, db_credentials.password, db_credentials.dbname,
                  db_credentials.host, db_credentials.port)


def respond_ban(context):
    message = context["message"]["text"]
    message = message.split(' ')  # split the message to get arguments

    name = list(filter(lambda x: x != [], message))  # filter out the empty elements

    if len(name) <= 1:  # if len is <= 1, the number of args is insufficient
        return

    name = name[1]  # select the first argument

    if len(name) > 64:  # too long
        return

    user = context["message"]
    if "from" in context["message"]:
        user = context["message"]["from"]["username"]
    else:
        user = "idk your username in group chats"

    chat_id = context["message"]["chat"]["id"]

    db.ban_user(chat_id, user, name)

    responses = ["Banned ", " is now banned", "Successfully banned "]
    bot.send_message(context, f"Banned {name}")


bot.add_command('ban', respond_ban)

bot.run(server_config.host, server_config.port)

