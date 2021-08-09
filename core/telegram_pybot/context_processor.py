class ContextProcessor:
    def __init__(self):
        self.recognized_commands = []
        self.recognized_front_keywords = []

        self.allowed_chats = []
        self.use_allowed_chats = False

    def allow_chat(self, chat_id):
        """
        allow_chat(chat_id)
        allow the bot to respond in chat with chat_id
        """
        self.allowed_chats.append(chat_id)

    def set_use_allowed_chats(self, use_chats: bool = False):
        """
        set_use_allowed_chats(use_chats: Boolean)
        changes the value of self.use_allowed_chats to use_chats and returns the changed value
        if set to false, respond to any chat
        if set to true, only respond to chats whose chat_id stored in self.allowed_chats
        """
        self.use_allowed_chats = use_chats

        return self.use_allowed_chats

    def __is_chat_allowed(self, chat_id):
        """
        private func to check if chat is allowed
        """
        return chat_id in self.allowed_chats

    def add_command(self, command: str):
        """
        Adds a command to the list of recognized commands
        """
        self.recognized_commands.append(command)

    def add_front_keyword(self, keyword: str):
        """
        Adds a keyword to look for in the beginning of message
        May be a key sentence
        """
        if keyword in self.recognized_front_keywords:
            return

        self.recognized_front_keywords.append(keyword)

    def __process_text_message(self, text: str):
        result = {
            "type": ""
        }

        if text.split(' ')[0][0] == '/':  # detected a command
            result["type"] = "command"
            result["command"] = ""

            if text.split(' ')[0][1:] in self.recognized_commands:  # if the command is a recognized command
                result["command"] = text.split(' ')[0][1:]  # return the commands name
                return result

            return result

        for keyword in self.recognized_front_keywords:
            if text.startswith(keyword):
                result["type"] = "front_keyword"
                result["front_keyword"] = keyword

        return result

    def __process_message(self, message: dict):
        if self.use_allowed_chats:
            if not self.__is_chat_allowed(message["chat"]["id"]):
                return False

        if 'text' in message.keys():
            return self.__process_text_message(message['text'])

    def process(self, context: dict) -> dict:
        """
        Processes context
        Right now only processes messages
        Returns a dictionary with a type of message
        (available types: "command" - command, "front_keyword" - keyword at the beginning, "" - nothing detected)
        and some additional info
        """
        if 'message' in context.keys():
            return self.__process_message(context['message'])
