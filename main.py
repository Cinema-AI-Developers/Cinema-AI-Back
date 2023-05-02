import datetime

from flask import Flask, request, jsonify
from flask import make_response
from flask_login import LoginManager, login_required, \
    current_user, logout_user, login_user
from flask_restful import Api
from werkzeug.utils import redirect

from data import db_session
from data.comments import Comment
from data.users import User

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'pixelpopcorn_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/CinemaAI.sqlite")
session = db_session.create_session()


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    rqst = request.json
    if rqst["email"]:
        user = session.query(User).filter(User.email == rqst["email"]).first()
    elif rqst["phone"]:
        user = session.query(User).filter(User.email == rqst["phone"]).first()
    else:
        return jsonify(
            {'status': 'error',
             'error_txt': 'Отсутствие телефона или почты в базе'})
    if user and user.check_password(rqst["password"]):
        login_user(user, remember=True)
        print(datetime.datetime.now(), current_user.name, "id: ",
              current_user.id, "вошел")
        return jsonify({'status': 'OK'})
    return jsonify(
        {'status': 'error', 'error_txt': 'Неправильный логин или пароль'})


@app.route('/register', methods=['GET', 'POST'])
def register():
    rqst = request.json
    print(request)
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['email', 'phone', 'name', 'password']):
        return jsonify({'status': 'error', 'error_text': 'Bad request'})
    user = User()
    if not session.query(User).filter(
            User.phone != rqst["phone"]).first() and not session.query(
        User).filter(User.phone != rqst["phone"]).first():
        user.email = rqst["email"]
        user.phone = rqst["phone"]
    else:
        return jsonify({'error': 'Not unique user'})
    user.name = rqst["name"]
    user.friends_ID = ""
    user.type = "user"
    user.set_password(rqst["password"])
    print(datetime.datetime.now(), rqst["name"], "зарегистрировался")
    try:
        session.add(user)
        session.commit()
    except Exception:
        return jsonify({'error': 'Bad parameter'})
    return jsonify({'status': 'OK'})


@app.route('/logout')
@login_required
def logout():
    print(datetime.datetime.now(), current_user.name, "id: ", current_user.id,
          "вышел")
    logout_user()
    return redirect("/")


@app.route("/api/add_comm", methods=['POST'])
@login_required
def add_comm():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['user_id', 'film_id', 'value', 'text']):
        return jsonify({'error': 'Bad request'})
    comm = Comment()
    comm.user_ID = current_user.id
    comm.film_ID = request.json["film_id"]
    comm.text = request.json["text"]
    session.add(comm)
    session.commit()


@app.route("/api/edit_comm", methods=['POST'])
@login_required
def edit_comm():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'text']):
        return jsonify({'error': 'Bad request'})
    comm = session.query(Comment).filter(Comment.id == request.json['id'])
    comm.text = request.json['text']
    session.commit()


@app.route("/api/viewed", method=["POST"])
@login_required
def viewed_films():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not 'film_id' in request.json:
        return jsonify({'error': 'Bad request'})
    user = session.query(User).filter(User.id == current_user.id)
    user.films_id += f" {request.json['film_id']}"
    session.commit()


@app.route("/api/edit_comm", methods=['POST'])
@login_required
def delete_comm():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not 'id' in request.json:
        return jsonify({'error': 'Bad request'})
    comm = session.query(Comment).filter(Comment.id == request.json['id'])
    print(datetime.datetime.now(), current_user.name, "id: ", current_user.id,
          f"удалил коммент {comm.text} к фильму {comm.film_id}")
    session.delete(comm)
    session.commit()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
