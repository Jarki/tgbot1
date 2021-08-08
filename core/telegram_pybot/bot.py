import logging
from flask import request
from waitress import serve

if __name__ == "__main__":
    from handler import Handler
    from dispatcher import EventDispatcher
    from flask_wrapper import FlaskWrapper
    from bot_api import BotApi
else:
    from telegram_pybot.handler import Handler
    from telegram_pybot.dispatcher import EventDispatcher
    from telegram_pybot.flask_wrapper import FlaskWrapper
    from telegram_pybot.bot_api import BotApi


class Bot(BotApi):
    def __init__(self, token):
        self.app = None

        self.event_dispatcher = EventDispatcher()
        self.event_handler = Handler()
        self.event_handler.subscribe(self.event_dispatcher)

        super().__init__(token)

    def add_command(self, command, handler):
        if command != "":
            self.event_dispatcher.add_command(command)
            self.event_handler.add_handler(f"{command}_command", handler)

    def run(self, name):
        self.app = FlaskWrapper(name)

        self.app.add_endpoint('/', '/', self.__run)

        serve(self.app.app, host="127.0.0.1", port="5000")

    def __run(self):
        if request.method == "POST":
            logging.info("Received a post request")
            print(request.json)
            self.event_dispatcher.dispatch(request.json)

        return {"ok": True}
