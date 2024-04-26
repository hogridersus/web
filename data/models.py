import datetime
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import orm
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    type = sqlalchemy.Column(sqlalchemy.String, default='student')
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    school = orm.relationship("School", back_populates='user')
    grade = orm.relationship("Grade", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class School(SqlAlchemyBase):
    __tablename__ = 'schools'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = orm.relationship('User')


class Grade(SqlAlchemyBase):
    __tablename__ = 'grades'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    year = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = orm.relationship('User')
