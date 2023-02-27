from flask import Flask, render_template
from flask_login import LoginManager, login_user, login_required, \
    logout_user, current_user
from flask_restful import Api

from data.__all_models import *
from data import db_session

app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/CinemaAI.sqlite")
session = db_session.create_session()


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)

@app.route("/")
def index():
    return render_template("index.html", title='Лента')