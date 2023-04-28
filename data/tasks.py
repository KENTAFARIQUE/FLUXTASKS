import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Tasks(SqlAlchemyBase):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    deadline = sqlalchemy.Column(sqlalchemy.DateTime)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    status_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('status.id'))
    importance_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('importance.id'))
    folder_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('folders.id'))

    status = orm.relationship('Status')
    importance = orm.relationship('Importance')
    folder = orm.relationship('Folder')
    user = orm.relationship('User', lazy=False)
