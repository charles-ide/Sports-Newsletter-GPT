'''
(c) 2023, Charles Ide
This module stores the models used to store the models for emails and stories
'''

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# A class to store news stories
class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500))
    title = db.Column(db.String(500))
    text = db.Column(db.String(100000), nullable=False)

# A class to store email addressess of mailing list members
class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120), unique=True, nullable=False)