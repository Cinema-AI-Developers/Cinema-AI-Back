from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, login_required, \
    logout_user, current_user
from flask_restful import Api
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import PasswordField, BooleanField, SubmitField, StringField, \
    TextAreaField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email

from data.__all_models import *
from data import db_session

app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/CinemaAI.sqlite")
session = db_session.create_session()


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[Email(), DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль',
                                   validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    gender = SelectField('gender', validators=[DataRequired()])
    description = StringField("Немного о себе")
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


@app.route("/")
def index():
    return render_template("index.html", title='Лента')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter(
            User.email == form.email.data).first()
        print(user)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    print(datetime.datetime.now(), current_user.name, "id: ", current_user.id,
          "вошел")
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/api/add_comm/<film_id>', methods=['POST'])
@login_required
def leave_comment(film_id):
    text = request.form.get("text")
    comm = Comment()
    comm.user_ID = current_user.id
    comm.film_ID = film_id
    comm.text = text


@app.route('/api/edit_comm/<comm_id>', methods=['POST'])
def edit_comment(comm_id):
    text = request.form.get("text")
    comm = session.query(Comment).filter(Comment.id == comm_id)
    comm.text = text
