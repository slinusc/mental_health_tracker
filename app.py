import flask
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mht"
mongo = PyMongo(app)
app.secret_key = os.urandom(16)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email': request.form['email']})

        if existing_user is None:
            if request.form['password'] != request.form['confirm_password']:
                session['password_match'] = False
                return redirect(url_for('login_page', password_match='1'))
            else:
                hashpass = generate_password_hash(request.form['password'])
                users.insert_one(
                    {'username': request.form['username'], 'email': request.form['email'], 'password': hashpass})
                return redirect(url_for('index'))

        if existing_user:
            session['email_exists'] = True
            return redirect(url_for('login_page', email_exists='1'))

    return redirect(url_for('login_page'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users

        login_user = users.find_one({'email': request.form['email']})

        if login_user is None:
            flash('E-Mail oder Passwort inkorrekt', 'danger')
        elif not check_password_hash(login_user['password'], request.form['password']):
            flash('E-Mail oder Passwort inkorrekt', 'danger')
        else:
            session['username'] = login_user['username']
            return redirect(url_for('index'))

    return render_template('login_page.html')



@app.route('/index')
def index():
    if 'username' in session:
        return render_template('main_page.html', username=session['username'])
    else:
        return redirect(url_for('login_page'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/')
def login_page():
    return render_template('login_page.html')


@app.route('/main')
def main():
    return render_template('main_page.html')


if __name__ == '__main__':
    app.run(debug=True)
