from datetime import datetime

from sqlalchemy import Column, Integer, String, VARCHAR, Text, DateTime
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    email = Column(VARCHAR, unique=True, nullable=False)
    phone = Column(VARCHAR, unique=True)
    avatar = Column(String)
    gender = Column(String)
    name = Column(String, nullable=False)
    films_ID = Column(String, nullable=True)
    friends_ID = Column(String, nullable=True)
    description = Column(Text)
    created_date = Column(DateTime, default=datetime.now)
    hashed_password = Column(String, nullable=False)

    def __repr__(self):
        """
        return type if do print()
        :return: string with description
        """
        return f"<User> {self.id} {self.nickname} {self.email}"

    def __str__(self):
        """
        return type if str()
        :return: string with description
        """
        return f"<User> {self.id} {self.n1ame} {self.email}"

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
