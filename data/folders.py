import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Folder(SqlAlchemyBase):
    __tablename__ = 'folders'

    def __repr__(self):
        return self.name

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User', back_populates='folders')

