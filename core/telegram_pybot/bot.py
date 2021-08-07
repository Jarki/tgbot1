import requests
import json
import logging
from flask import request

from core.telegram_pybot.handler import Handler
from core.telegram_pybot.dispatcher import EventDispatcher
from core.telegram_pybot.flask_wrapper import FlaskWrapper
from core.telegram_pybot.bot_api import BotApi


class Bot:
    def __init__(self, token):
        self.app = None

        self.event_dispatcher = EventDispatcher()
        self.event_handler = Handler()
        self.event_handler.subscribe(self.event_dispatcher)
        self.api_interactor = BotApi(token)

    def add_command(self, command, handler):
        if command != "":
            self.event_dispatcher.add_command(command)
            self.event_handler.add_handler(f"{command}_command", handler)

    def run(self, name):
        self.app = FlaskWrapper(name)

        self.app.add_endpoint('/', '/', self.__run)

    def __run(self):
        if request.method == "POST":
            logging.info("Received a post request")
            print(request.json)
            self.event_dispatcher.dispatch(request.json)
