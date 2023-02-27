import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_ID = Column(Integer, ForeignKey("users.id"))
    film_ID = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.now)
    text = Column(Text)

    def __repr__(self):
        return f"<Comment> {self.id} {self.user_ID} {self.text}"

