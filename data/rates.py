from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class Rate(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Rates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_ID = Column(Integer, ForeignKey("users.id"))
    film_ID = Column(String)
    value = Column(Integer)

    def __repr__(self):
        return f"<Comment> {self.id} {self.user_ID} {self.value}"