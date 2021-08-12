import logging

from env import token
from env.allowed_chats import allowed_chats
from env import server_config
from env import db_credentials
from database_interactor import DBInteractor
from telegram_pybot.bot import Bot

logging.basicConfig(level=logging.INFO)

bot = Bot(token.token)
bot.set_webhook("https://8318ff8ce251.ngrok.io")

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

    responses = ["Banned %user%", "%user% is now banned", "Successfully banned %user%"]
    bot.send_message(context, f"Banned {name}")


def respond_stats_users(context):
    chat_id = context["message"]["chat"]["id"]

    string = "Top 10 bananas:\n"
    users = db.get_table_users(chat_id)

    counter = 1
    for row in users:
        string += f"{counter}. {row.username} issued {row.counter} bans\n"
        counter = counter + 1

    bot.send_message(context, string)


def respond_stats_banned(context):
    chat_id = context["message"]["chat"]["id"]

    string = "Top 10 banned:\n"
    users = db.get_table_banned(chat_id)

    counter = 1
    for row in users:
        string += f"{counter}. {row.username} got banned {row.counter} times\n"
        counter = counter + 1

    bot.send_message(context, string)


def respond_help(context):
    string = "/ban [username] - bans username\n" \
             "/stats_users - shows who used the bot the most\n" \
             "/stats_banned - shows who has been banned the most\n"

    bot.send_message(context, string)


bot.add_command('help', respond_help)
bot.add_command('ban', respond_ban)
bot.add_command('stats_users', respond_stats_users)
bot.add_command('stats_banned', respond_stats_banned)

bot.run(server_config.host, server_config.port)
