from functools import wraps
from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
# from data import articles_dstore
from flaskext.mysql import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.validators import DataRequired
from pymysql.cursors import DictCursor
from passlib.hash import sha256_crypt
import os

app = Flask(__name__)

# config mysql
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'myflask'

# init mysql
mysql = MySQL(cursorclass=DictCursor)
mysql.init_app(app)

# article = articles_dstore()


@app.route('/')
def index():
    """Complete this docstring"""
    return render_template('dynamic.html')


@app.route('/articles')
def articles():
    cur = mysql.get_db().cursor()
    result = cur.execute("SELECT * FROM articles")
    if result > 0:
        articles = cur.fetchall()
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Present'
        return render_template('articles.html', msg=msg)
    cur.close()


@app.route('/article/<string:id>')
def article(id):
    cur = mysql.get_db().cursor()
    result = cur.execute("SELECT * FROM articles WHERE id= %s", (id))
    if result > 0:
        article = cur.fetchone()
        return render_template('article.html', article=article)


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
        result = cur.execute("SELECT * FROM users WHERE username = %s", (username))
        if result > 0:
            # get stored hash
            data = cur.fetchone()
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


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unautorized, please login', 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are logged out', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard')
@is_logged_in
def dashboard():
    cur = mysql.get_db().cursor()
    result = cur.execute("SELECT * FROM articles")
    if result > 0:
        articles = cur.fetchall()
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No Articles Present'
        return render_template('dashboard.html', msg=msg)
    cur.close()


class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])


@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        # create cursor
        cur = mysql.get_db().cursor()
        # execute
        cur.execute("INSERT INTO articles(title, author, body) VALUES(%s, %s, %s)",
                    (title, session['username'], body))
        # commit
        mysql.get_db().commit()
        cur.close()

        flash('Article Created', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form=form)


@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    cur = mysql.get_db().cursor()
    result = cur.execute("SELECT * FROM articles WHERE id= %s", (id))
    article = cur.fetchone()
    form = ArticleForm(request.form)
    form.title.data = article['title']
    form.body.data = article['body']
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
        cur.execute("UPDATE articles SET title= %s, body= %s WHERE id= %s", (title, body, id))
        mysql.get_db().commit()
        flash('Article Updated', 'success')
        return redirect(url_for('dashboard'))
    else:
        return render_template('edit_article.html', form=form)
    cur.close()


@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    cur = mysql.get_db().cursor()
    cur.execute("DELETE FROM articles WHERE id= %s", (id))
    mysql.get_db().commit()
    cur.close()
    flash('Article Deleted', 'success')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True)
