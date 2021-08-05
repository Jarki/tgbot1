from pymitter import EventEmitter
import logging

from core.bot import Bot


class Handler:
    ee = EventEmitter()

    def __init__(self, bot: Bot):
        self.handled = bot

    def subscribe(self, emitter: EventEmitter):
        logging.info("Subscribed to an emitter")
        self.ee = emitter

        self.ee.on("text_message", self.respond_to_text)

    def respond_to_text(self, context):
        logging.info("handling a text message")
        self.handled.send_message(context, "hello")
