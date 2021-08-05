from pymitter import EventEmitter
import logging


class ContextDispatcher:
    def __init__(self):
        """
        ContextDispatcher constructor
        """
        self.ee = EventEmitter()
        self.commands = []
        self.keywords_begins = []

    def get_emitter(self):
        """
        Returns emitter
        """
        return self.ee

    def add_command(self, command: str):
        """
        add_command('start')
        Adds a command for dispatcher to raise events on it
        The event raised will be called name_command
        (if we add command 'start', need to handle start_command event)
        """
        self.commands.append(command)

    def add_keyword(self, keyword: str):
        """
        add_keyword('word')
        Adds a keyword for dispatcher to raise events on it
        The event raised will be called name_keyword
        (if we add command 'word', need to handle word_keyword event)
        """
        self.keywords_begins.append(keyword)

    def dispatch(self, context):
        """
        Dispatches different events
        """
        if 'message' in context.keys():  # if it's a message
            if 'text' in context["message"].keys():  # if the message contains text
                if context["message"]["text"].split(' ')[0][0] == '/':  # if it starts with a '/',
                    # it's considered a command
                    if context["message"]["text"].split(' ')[0][1:] in self.commands:  # if it's a command set by user
                        command_index = self.commands.index(context["message"]["text"].split(' ')[0][1:])
                        logging.info(f"detected a command: {self.commands[command_index]}")
                        self.ee.emit(f"{self.commands[command_index]}_command", context)
                    else:
                        logging.info("detected an unknown command")
                        self.ee.emit("command", context)
                else:
                    if context["message"]["text"].split(' ')[0] in self.keywords_begins:
                        keyword_index = self.keywords_begins.index(context["message"]["text"].split(' ')[0])
                        logging.info(f"detected a keyword at the beginning: {self.keywords_begins[keyword_index]}")
                        self.ee.emit(f"{self.keywords_begins[keyword_index]}_keyword", context)


