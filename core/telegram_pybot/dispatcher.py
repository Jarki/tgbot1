from pymitter import EventEmitter
import logging

from telegram_pybot.context_processor import ContextProcessor


class EventDispatcher:
    def __init__(self):
        """
        ContextDispatcher constructor
        """
        self.ee = EventEmitter()
        self.context_proc = ContextProcessor()

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
        (if we add command 'start', will raise start_command event)
        """
        self.context_proc.add_command(command)

    def add_front_keyword(self, keyword: str):
        """
        add_front_keyword('word')
        Adds a keyword for dispatcher to raise events on it
        The event raised will be called name_keyword
        (if we add command 'word', will raise word_keyword event)
        """
        self.context_proc.add_front_keyword(keyword)

    def dispatch(self, context):
        """
        Dispatches different events
        """
        result = self.context_proc.process(context)

        if not result:
            logging.info("Did not raise any event")
            return

        if result is None:
            logging.warning(f"{self.__class__}: dispatch(self, context): unknown state (result was NoneType)")
            return

        if not "type" in result:
            logging.warning(f"{self.__class__}: dispatch(self, context): unknown state (no type returned)")
            return

        if result["type"] == "":
            logging.info("just a text message")
            self.ee.emit("text_message", context)
            return

        if result["type"] == "command":
            if "command" in result:
                if result["command"] == "":
                    logging.info("detected an unknown command")
                    self.ee.emit("command", context)
                    return
                else:
                    logging.info(f"detected a command: {result['command']}")
                    self.ee.emit(f"{result['command']}_command", context)
                    return
            else:
                logging.warning(f"{self.__class__}: dispatch(self, context): unknown state (no command returned)")

        if result["type"] == "front_keyword":
            if not "front_keyword" in result:
                logging.warning(f"{self.__class__}: dispatch(self, context): unknown state (no front keyword returned)")
                return

            logging.info(f"detected a front keyword: {result['front_keyword']}")
            self.ee.emit(f"{result['front_keyword']}_front_command")
