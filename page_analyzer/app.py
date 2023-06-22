from flask import Flask

app = Flask(__name__)


@app.route('/')
def analyzer():
    return 'Welcome to page_analyzer'
