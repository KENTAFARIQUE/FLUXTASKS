import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Importance(SqlAlchemyBase):
    __tablename__ = 'importance'

    def __repr__(self):
        return self.name

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
