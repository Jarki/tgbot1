import requests
import json


class Bot:
    def __init__(self, token):
        self.token = token
        self.url = f"https://api.telegram.org/bot{self.token}/"

    def set_webhook(self, url):
        requests.get(f"{self.url}/deleteWebhook")  # clear existing webhooks
        r = requests.get(f"{self.url}/setWebhook", host={"url": url})

        return json.dumps(r.json())

