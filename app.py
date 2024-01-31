import flask
from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mht"
mongo = PyMongo(app)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email': request.form['email']})

        if existing_user is None:
            hashpass = generate_password_hash(request.form['pass'])
            users.insert_one(
                {'username': request.form['username'], 'email': request.form['email'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'email': request.form['email']})

        if login_user and check_password_hash(login_user['password'], request.form['pass']):
            session['username'] = login_user['username']
            return redirect(url_for('index'))

        return 'Invalid username/password combination'

    return render_template('login.html')


@app.route('/index')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']

    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/')
def login_page():
    return flask.render_template('main_page.html')


if __name__ == '__main__':
    app.run(debug=True)
