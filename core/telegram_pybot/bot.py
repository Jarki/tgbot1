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

        self.__event_dispatcher = EventDispatcher()
        self.__event_handler = Handler()
        self.__event_handler.subscribe(self.__event_dispatcher)

        self.allowed_chats = []
        self.use_allowed_chats = false

        super().__init__(token)

    def add_command(self, command, handler):
        if command != "":
            self.__event_dispatcher.add_command(command)
            self.__event_handler.add_handler(f"{command}_command", handler)

    def allow_chat(self, chat_id):
        """
        allow_chat(chat_id)
        allow the bot to respond in chat with chat_id
        """
        self.allowed_chats.append(chat_id)

    def toggle_allowed_chats(self):
        """
        toggle_allowed_chats()

        """
        self.allowed_chats = not self.allowed_chats

        return self.allowed_chats

    def run(self, name):
        self.app = FlaskWrapper(name)

        self.app.add_endpoint('/', '/', self.__run)

        serve(self.app.app, host="127.0.0.1", port="5000")

    def __run(self):
        if request.method == "POST":
            logging.info("Received a post request")
            print(request.json)
            self.__event_dispatcher.dispatch(request.json)

        return {"ok": True}
