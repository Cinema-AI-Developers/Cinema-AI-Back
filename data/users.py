import datetime

from sqlalchemy import Column, Integer, String, VARCHAR, Text, DateTime
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from db_session import SqlAlchemyBase

class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String, nullable=False)
    description = Column(Text)
    email = Column(VARCHAR, unique=True, nullable=False)
    phone = Column(VARCHAR, unique=True)
    hashed_password = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now)
    friends_ID = Column(String, nullable=True)
    films_ID = Column(String, nullable=True)
    avatar = Column(String)
    gender = Column(String)
    type = Column(String, nullable=False)

    def __repr__(self):
        return f"<User> {self.id} {self.nickname} {self.email}"

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
