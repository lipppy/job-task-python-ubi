from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Welcome to CodingX</h1>"

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404