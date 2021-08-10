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
        self.use_allowed_chats = False

        super().__init__(token)

    def add_command(self, command, handler):
        """
        add_command('start', handle_start)
        adds a command to listen for and a handler to handle it
        """
        if command != "":
            self.__event_dispatcher.add_command(command)
            self.__event_handler.add_handler(f"{command}_command", handler)

    def allow_chat(self, chat_id):
        """
        allow_chat(chat_id)
        allow the bot to respond in chat with chat_id
        """
        self.__event_dispatcher.context_proc.allow_chat(chat_id)

    def ignore_disallowed_chats(self, ignore=False):
        """
        ignore_disallowed_chats(ignore: Boolean)
        changes the value of self.use_allowed_chats to the parameter and returns the changed value
        if set to false, respond to any chat
        if set to true, only respond to chats whose chat_id stored in self.allowed_chats
        defaults to False
        """
        self.__event_dispatcher.context_proc.set_use_allowed_chats(ignore)

    def run(self, host, port):
        """
        creates a flask app and runs it using waitress.serve
        """
        self.app = FlaskWrapper(__name__)

        self.app.add_endpoint('/', '/', self.__run)

        serve(self.app.app, host=host, port=port)

    def __run(self):
        """
        method to handle post requests received through flask
        """
        if request.method == "POST":
            logging.info("Received a post request")
            print(request.json)
            self.__event_dispatcher.dispatch(request.json)

        return {"ok": True}
