from flask import Flask, request
import logging

from core.env import token
from core.bot import Bot
from core.emitter import ContextDispatcher
from core.handler import Handler

logging.basicConfig(level=logging.INFO)
updater = Flask(__name__)

bot = Bot(token.token)
# bot.set_webhook("https://831e3fc3b495.ngrok.io")

cd = ContextDispatcher()
handler = Handler(bot)
handler.subscribe(cd.get_emitter())


@updater.route('/', methods=['GET', 'POST'])
def handle():
    if request.method == "POST":
        logging.info("Received a post request")
        print(request.json)
        cd.dispatch(request.json)

    return {"ok": True}
