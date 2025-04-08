from sqlalchemy import Integer, Column

from .db_session import SqlAlchemyBase


class Group(SqlAlchemyBase):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)

