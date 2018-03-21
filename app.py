from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
from data import articles_dstore
from flaskext.mysql import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.validators import DataRequired
from pymysql.cursors import DictCursor
from passlib.hash import sha256_crypt
import os

app = Flask(__name__)

# config mysql
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ESTD1759'
app.config['MYSQL_DATABASE_DB'] = 'myflask'

# init mysql
mysql = MySQL(cursorclass=DictCursor)
mysql.init_app(app)

article = articles_dstore()


@app.route('/index')
@app.route('/index/<path:name>')
def index(name=None):
    """Complete this docstring"""
    return render_template('dynamic.html', name=name)


@app.route('/articles')
def articles():
    """Complete this docstring"""
    return render_template('articles.html', article=article)


@app.route('/article/<string:article_id>')
def article(article_id):
    """Complete this docstring"""
    return render_template('article.html', article_id=article_id)


class RegisterForm(Form):
    username = StringField('Name', [validators.Length(min=1, max=10)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.EqualTo(
                                          'confirm',
                                          message='Passwords do not match')
                                          ])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # create cursor
        cur = mysql.get_db().cursor()
        # execute query
        cur.execute("INSERT INTO users(username, email, password) VALUES (%s, %s, %s)",
                    (username, email, password))
        mysql.get_db().commit()
        # close cursor
        cur.close()

        flash('Bravo,  You are a registered user', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get Form fields
        username = request.form['username']
        passwordLogin = request.form['password']

        # cursor
        cur = mysql.get_db().cursor()
        # get username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
        if result > 0:
            # get stored hash
            data = cur.fetchone()
            print (data)
            password = data['password']
            # compare password
            if sha256_crypt.verify(passwordLogin, password):
                # when passwords match
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid Password'
                return render_template('login.html', error=error)
            cur.close()
        else:
            error = 'User not found'
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True)
