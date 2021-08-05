from pymitter import EventEmitter
import logging


class ContextDispatcher:
    def __init__(self):
        self.ee = EventEmitter()
        self.commands = []

    def get_emitter(self):
        return self.ee

    def add_command(self, command: str):
        """
        add_command('start')
        Adds a command for dispatcher to raise events on it
        The event raised will be called name_command
        (if we add command 'start', need to handle start_command event)
        """
        self.commands.append(command)

    def dispatch(self, context):
        if 'message' in context.keys():  # if it's a message
            if 'text' in context["message"].keys():  # if the message contains text
                if context["message"]["text"].split(' ')[0][0] == '/':  # if it starts with a '/',
                    # it's considered a command
                    if context["message"]["text"].split(' ')[0][1:] in self.commands:  # if it's a command set by user
                        command_index = self.commands.index(context["message"]["text"].split(' ')[0][1:])
                        logging.info(f"detected a command:{self.commands[command_index]}")
                        self.ee.emit(self.commands[command_index], context)
                    else:
                        logging.info("detected an unknown command")
                        self.ee.emit("command", context)
                else:
                    logging.info("detected a text message")
                    self.ee.emit("text_message", context)

