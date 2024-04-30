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
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    patronymic = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    birth = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.String,
                               default='student')

    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    school_id = sqlalchemy.Column(sqlalchemy.String,
                                  sqlalchemy.ForeignKey("schools.id"), nullable=True)
    grade_id = sqlalchemy.Column(sqlalchemy.String,
                                 sqlalchemy.ForeignKey("grades.id"), nullable=True)

    school = orm.relationship('School')
    grade = orm.relationship('Grade')
    teach_lessons = orm.relationship('Lesson', back_populates='teacher')
    marks = orm.relationship('Mark', back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class School(SqlAlchemyBase):
    __tablename__ = 'schools'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    users = orm.relationship('User', back_populates='school')
    grades = orm.relationship('Grade', back_populates='school')


class Grade(SqlAlchemyBase):
    __tablename__ = 'grades'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    school_id = sqlalchemy.Column(sqlalchemy.String,
                                  sqlalchemy.ForeignKey("schools.id"))

    school = orm.relationship('School')
    users = orm.relationship('User', back_populates='grade')
    lessons = orm.relationship('Lesson', back_populates='grade')
    days = orm.relationship('Day', back_populates='grade')


class Lesson(SqlAlchemyBase):
    __tablename__ = 'lessons'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    order = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    time = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    homework = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    grade_id = sqlalchemy.Column(sqlalchemy.String,
                                 sqlalchemy.ForeignKey("grades.id"), nullable=True)
    subject_id = sqlalchemy.Column(sqlalchemy.String,
                                   sqlalchemy.ForeignKey("subjects.id"), nullable=True)
    teacher_id = sqlalchemy.Column(sqlalchemy.String,
                                   sqlalchemy.ForeignKey("users.id"), nullable=True)
    day_id = sqlalchemy.Column(sqlalchemy.String,
                               sqlalchemy.ForeignKey("days.id"), nullable=True)

    grade = orm.relationship('Grade')
    day = orm.relationship('Day')
    subject = orm.relationship('Subject')
    teacher = orm.relationship('User')
    marks = orm.relationship('Mark', back_populates='lesson')


class Subject(SqlAlchemyBase):
    __tablename__ = 'subjects'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    marks = orm.relationship('Mark', back_populates='subject')
    lessons = orm.relationship('Lesson', back_populates='subject')


class Day(SqlAlchemyBase):
    __tablename__ = 'days'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    week = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    lessons = orm.relationship('Lesson', back_populates='day')
    marks = orm.relationship('Mark', back_populates='day')
    grade = orm.relationship('Grade')

    grade_id = sqlalchemy.Column(sqlalchemy.String,
                                 sqlalchemy.ForeignKey("grades.id"), nullable=True)


class Mark(SqlAlchemyBase):
    __tablename__ = 'marks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    value = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    coeff = sqlalchemy.Column(sqlalchemy.Float, nullable=True)

    user_id = sqlalchemy.Column(sqlalchemy.String,
                                sqlalchemy.ForeignKey("users.id"), nullable=True)
    lesson_id = sqlalchemy.Column(sqlalchemy.String,
                                  sqlalchemy.ForeignKey("lessons.id"), nullable=True)
    subject_id = sqlalchemy.Column(sqlalchemy.String,
                                   sqlalchemy.ForeignKey("subjects.id"), nullable=True)
    day_id = sqlalchemy.Column(sqlalchemy.String,
                               sqlalchemy.ForeignKey("days.id"), nullable=True)

    user = orm.relationship('User')
    subject = orm.relationship('Subject')
    lesson = orm.relationship('Lesson')
    day = orm.relationship('Day')
