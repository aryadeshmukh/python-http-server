from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<html><body><h1>Hello World!</h1></body></html>"