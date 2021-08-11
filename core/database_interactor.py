import sqlalchemy
from sqlalchemy import Table, Column, String, MetaData, Integer, select, desc
from sqlalchemy.dialects.postgresql import insert
import logging

class DBInteractor:
    def __init__(self, username, password, dbname, host="localhost", port=5432):
        connect_string = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"
        self.db = sqlalchemy.create_engine(connect_string)

        self.BOT_USERS = True
        self.MOST_BANNED = False

    def __table_exists(self, tablename):
        """checks if a table exists"""

        return self.db.dialect.has_table(self.db.connect(), table_name=tablename)

    @staticmethod
    def __build_tablename(chat_id, table_type):
        """builds a tablename for chat_id and depending if want a name for users or most banned"""
        if table_type:
            return f"chat_{chat_id}_users"
        else:
            return f"chat_{chat_id}_most_banned"

    def __get_table(self, chat_id, table_type):
        """returns top 10 bot users/banned users in chat with chat_id"""
        table_name = self.__build_tablename(chat_id, table_type=table_type)

        if not self.__table_exists(table_name):
            return False

        table = Table(
            table_name,
            MetaData(self.db),
            autoload=True,
            autoload_with=self.db
        )

        stmt = select([
            table
        ]).order_by(desc(table.columns.counter)).limit(10)

        connection = self.db.connect()
        return connection.execute(stmt)

    def __create_chat_table(self, chat_id, for_users=True):
        table_name = self.__build_tablename(chat_id, for_users)

        if self.__table_exists(table_name):
            return False

        table = Table(table_name, MetaData(self.db),
                      Column('username', String(32), primary_key=True),
                      Column('counter', Integer))

        table.create()
        return True

    def __update_counter(self, chat_id, username, table_type):
        table_name = self.__build_tablename(chat_id, table_type)

        if not self.__table_exists(table_name):
            self.__create_chat_table(chat_id, table_type)

        table = Table(
            table_name,
            MetaData(self.db),
            autoload=True,
            autoload_with=self.db
        )
        stmt = insert(table).values(username=username, counter=1)

        stmt = stmt.on_conflict_do_update(
            index_elements=["username"],
            set_=dict(counter=stmt.table.columns.counter + 1)
        )

        print(stmt)
        connection = self.db.connect()
        connection.execute(stmt)

    def get_table_users(self, chat_id):
        """returns top 10 bot users of chat"""
        logging.info(f"getting table for {chat_id}")
        return self.__get_table(chat_id, self.BOT_USERS)

    def get_table_banned(self, chat_id):
        """returns top 10 most banned users of chat"""
        return self.__get_table(chat_id, self.MOST_BANNED)

    def create_table_bot_users(self, chat_id):
        """creates a table to keep track of who uses the bot the most"""
        self.__create_chat_table(chat_id, self.BOT_USERS)

    def create_table_count_banned(self, chat_id):
        """creates a table to keep track of who gets banned the most"""
        self.__create_chat_table(chat_id, self.MOST_BANNED)

    def update_table_bot_users(self, chat_id, users):
        """updates the user counter for bot usage"""
        self.__update_counter(chat_id, users, self.BOT_USERS)

    def update_table_banned(self, chat_id, users):
        """updates the banned user count for times getting banned"""
        self.__update_counter(chat_id, users, self.MOST_BANNED)

    def ban_user(self, chat_id, banned_by, banned):
        """bans the user"""
        self.update_table_bot_users(chat_id, banned_by)
        self.update_table_banned(chat_id, banned)

