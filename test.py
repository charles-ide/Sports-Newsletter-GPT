'''
(c) Charles Ide, November 6 2023
This file will serve as the entrypoint for our Newsletter GPT application
'''
from flask import Flask, render_template, request
#from url_processor import get_page_content
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=8000, debug=True)