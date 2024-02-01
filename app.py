from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import os
from pycode.user_logs import UserActivityLogger as ual

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mht"
mongo = PyMongo(app)
app.secret_key = os.urandom(16)
logger = ual(app.config["MONGO_URI"])


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_mail = users.find_one({'email': request.form['email']})
        existing_username = users.find_one({'username': request.form['username']})

        if existing_mail is None and existing_username is None:
            if request.form['password'] != request.form['confirm_password']:
                session['password_match'] = False
                return redirect(url_for('login_page', password_match='1'))
            else:
                hashpass = generate_password_hash(request.form['password'])
                users.insert_one(
                    {'username': request.form['username'], 'email': request.form['email'], 'password': hashpass})
                return redirect(url_for('index'))

        if existing_mail:
            session['email_exists'] = True
            return redirect(url_for('login_page', email_exists='1'))

        if existing_username:
            session['username_exists'] = True
            return redirect(url_for('login_page', username_exists='1'))

    return redirect(url_for('login_page'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'email': request.form['email']})

        if login_user is None or not check_password_hash(login_user['password'], request.form['password']):
            flash('E-Mail oder Passwort inkorrekt', 'danger')
            return render_template('login_page.html')

        # Setzen Sie den 'username' in der Session nach erfolgreicher Authentifizierung
        session['username'] = login_user['username']

        # Generieren Sie eine eindeutige Session-ID
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id

        # Loggen Sie die Benutzeraktivität
        logger.log_login_activity(session_id, session['username'], request.remote_addr, request.headers.get('User-Agent'))

        # Weiterleitung zum Hauptbereich der Anwendung
        return redirect(url_for('index'))

    # Wenn die Methode nicht POST ist, zeigen Sie die Login-Seite
    return render_template('login_page.html')


@app.route('/index')
def index():
    if 'username' in session:
        return render_template('main_page.html', username=session['username'])
    else:
        return redirect(url_for('login_page'))


@app.route('/logout')
def logout():
    session_id = session.get('session_id')
    if session_id:
        logger.log_logout_activity(session_id)
    session.pop('username', None)
    session.pop('session_id', None)
    return redirect(url_for('index'))


@app.route('/')
def login_page():
    return render_template('login_page.html')


@app.route('/main')
def main():
    return render_template('main_page.html')


if __name__ == '__main__':
    app.run(debug=True)
