from pymitter import EventEmitter
import logging

from telegram_pybot.dispatcher import EventDispatcher


class Handler:
    def __init__(self):
        self.ee = EventEmitter

    def subscribe(self, event_dispatcher: EventDispatcher):
        """
        subscribes a handler to all the events emitted by passed EventDispatcher
        """
        logging.info("Subscribed to an emitter")
        self.ee = event_dispatcher.get_emitter()

    def add_handler(self, event, handler):
        """
        uses pymitter.EventEmitter to raise an event, and handle it with a handler
        """
        self.ee.on(event, handler)
