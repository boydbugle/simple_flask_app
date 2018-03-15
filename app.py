from flask import Flask, render_template
from data import articles_dstore
app = Flask(__name__)

article = articles_dstore()


@app.route('/')
@app.route('/index/<path:name>')
def index(name=None):
    """Complete this docstring"""
    return render_template('dynamic.html', name=name)


@app.route('/articles')
def articles():
    """Complete this docstring"""
    return render_template('articles.html', articles=article)


@app.route('/article/<string:id>')
def article(article_id):
    """Complete this docstring"""
    return render_template('article.html', id=article_id)


if __name__ == '__main__':
    app.run(debug=True)
