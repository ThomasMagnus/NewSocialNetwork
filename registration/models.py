from sqlalchemy import MetaData, Table, Column, Text, Integer, Boolean, DateTime, create_engine
from authorization.models import UserFile


class FriendsTable:
    engine = create_engine('postgresql+psycopg2://postgres:Hofman95@localhost:5432/SocialNetwork')

    def __init__(self, login_user):
        self.friend_login = login_user

    def add_friend_table(self):
        metadata = MetaData()
        friend = Table(self.friend_login, metadata,
                       Column('id', Integer, primary_key=True, autoincrement=True),
                       Column('friends_id', Integer()).foreign_keys(UserFile.id),
                       Column('friend_name', Text()),
                       Column('friend_login', Text()),
                       Column('friend_email', Text()),
                       Column('status', Boolean()),
                       Column('date', DateTime()),
                       Column('request_on_friend', Boolean())
                       )

        metadata.create_all(self.engine)
