from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/user/<string:username>')
def show_user_profile(username: str) -> None:
    return f'User: {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id: int) -> None:
    return f'Post {escape(post_id)}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath: str) -> None:
    return f'Subpath {escape(subpath)}'