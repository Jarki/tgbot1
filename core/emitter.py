from pymitter import EventEmitter
import logging


class ContextDispatcher:
    def __init__(self):
        self.ee = EventEmitter()

    def dispatch(self, context):
        if 'message' in context.keys():
            if 'text' in context["message"].keys():
                if context["message"]["text"].split(' ')[0][0] == '/':
                    logging.info("detected a command")
                    self.ee.emit("command", context)
                else:
                    logging.info("detected a text message")
                    self.ee.emit("text_message", context)

    def get_emitter(self):
        return self.ee

