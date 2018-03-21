from flask import Flask, render_template
from data import articles_dstore
# from wtforms import Form, StringField, TextAreaField, PasswordField, validators
# from flask_mysqldb import MySQL
app = Flask(__name__)

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


@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
