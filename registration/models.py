from sqlalchemy import MetaData, Table, Column, Text, Integer, Boolean, DateTime, create_engine, ForeignKey

from authorization.models import UserFile
from abc import ABC, abstractmethod


class TableCreator(ABC):

    def __init__(self, login_user):
        self.login_user = login_user
        self.engine = create_engine('postgresql+psycopg2://postgres:Hofman95@localhost:5432/SocialNetwork')

    @abstractmethod
    def add_table(self):
        pass


class FriendsTable(TableCreator):
    def __init__(self, login_user):
        super().__init__(login_user)

    def add_table(self):
        metadata = MetaData()
        friend = Table(self.login_user, metadata,
                       Column('id', Integer(), primary_key=True, autoincrement=True),
                       Column('friend_id', Integer()),
                       Column('friend_name', Text()),
                       Column('friend_login', Text()),
                       Column('friend_email', Text()),
                       Column('status', Boolean()),
                       Column('date', DateTime()),
                       Column('request_on_friend', Boolean())
                       )
        metadata.create_all(self.engine)


class MessageTable(TableCreator):
    def __init__(self, login_user):
        super().__init__(login_user)

    def add_table(self):
        metadata = MetaData()
        message = Table(self.login_user, metadata,
                        Column('id', Integer(), primary_key=True, autoincrement=True),
                        Column('user_id', Integer(), nullable=False),
                        Column('user_id_to', Integer(), nullable=False),
                        Column('date_write', DateTime()),
                        Column('message_text', Text())
                        )

        metadata.create_all(self.engine)
