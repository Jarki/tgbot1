import logging
import requests
import json


class BotApi:
    def __init__(self, token):
        self.token = token

        self.url = f"https://api.telegram.org/bot{self.token}"

    def __build_url(self, method: str):
        """
        build a url for methods
        """
        url = f"{self.url}/{method}"

        return url

    def set_webhook(self, url):
        """
        tries to delete existing webhooks
        sets a webhook using a token (passed in the constructor) and url form parameters
        """
        method = "deleteWebhook"
        requests.get(f"{self.url}/deleteWebhook")  # clear existing webhooks
        r = requests.get(f"{self.url}/setWebhook?url={url}")  # clear existing webhooks
        logging.info(f"tried setting a webhook: {r.json()}")

        return json.dumps(r.json())

    def send_message(self, context, text):
        method = 'sendMessage'
        chat_id = context["message"]["chat"]["id"]

        logging.info("sending a message")

        print(self.__build_url(method))
        requests.get(self.__build_url(method), params={"chat_id": chat_id,
                                                       "text": text})
