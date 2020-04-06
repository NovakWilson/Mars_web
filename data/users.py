import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from werkzeug.security import generate_password_hash, check_password_hash
from data import db_session
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    position = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    speciality = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    def __repr__(self):
        return '<User> {} {} {}'.format(self.id, self.name, self.email)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Jobs(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    job = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    work_size = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    collaborators = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.Date, nullable=True)
    end_date = sqlalchemy.Column(sqlalchemy.Date, nullable=True)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)

    def __repr__(self):
        return '{} {} {} {} {} {} {}'.format(self.team_leader, self.job, self.work_size,
                                             self.collaborators, self.start_date, self.end_date,
                                             self.is_finished)


class Departments(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'departments'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    chief = orm.relation('User')
    chief_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    members = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)


class JobForm(FlaskForm):
    team_leader = IntegerField('Id тим-лида', validators=[DataRequired()])
    job = StringField('Название работы', validators=[DataRequired()])
    work_size = StringField('Время работы', validators=[DataRequired()])
    collaborators = StringField('Участники работы', validators=[DataRequired()])
    start_date = DateField('Дата начала работы')
    end_date = DateField('Дата оконачния работы')
    is_finished = BooleanField('Работа завершена')
    submit = SubmitField('Добавить')


class DepartmentForm(FlaskForm):
    title = StringField('Title of department', validators=[DataRequired()])
    chief_id = IntegerField('Chief id', validators=[DataRequired()])
    members = StringField('Jobs list', validators=[DataRequired()])
    email = StringField('Department email', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('login/email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')
