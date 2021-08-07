import requests
import json
import logging

from core.telegram_pybot.context_processor import ContextProcessor
from core.telegram_pybot.handler import Handler
from core.telegram_pybot.dispatcher import EventDispatcher

class Bot:
    def __init__(self, token):
        self.token = token

        self.event_dispatcher = EventDispatcher()
        self.url = f"https://api.telegram.org/bot{self.token}"

    def __build_url(self, method: str, params: dict):
        url = f"{self.url}/{method}"
        if len(params) == 0:
            return url

        url = f"{url}?"
        for param in params:
            url += f"{param}={params[param]}&"

        return url

    def set_webhook(self, url):
        method = "deleteWebhook"
        requests.get(f"{self.url}/deleteWebhook")  # clear existing webhooks
        r = requests.get(f"{self.url}/setWebhook?url={url}")  # clear existing webhooks
        logging.info("successfully set a webhook")

        return json.dumps(r.json())

    def add_command(self, command, handler):
        pass

    def send_message(self, context, text):
        method = 'sendMessage'
        chat_id = context["message"]["chat"]["id"]

        logging.info("sending a message")

        requests.get(self.__build_url(method, {"chat_id": chat_id,
                                               "text": text}))
