'''
(c) 2023, Charles Ide
This module stores the models used to store the models for emails and stories
'''

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# A class to store news stories
class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(300), unique=True)
    title = db.Column(db.String(300), unique=True)
    source_name = db.Column(db.String(100))
    published_date = db.Column(db.Date)
    category = db.Column(db.String(100))
    country = db.Column(db.String(100))
    text = db.Column(db.TEXT, nullable=False)

    def __repr__(self):
        return f"Story(id={self.id}, url='{self.url}', title='{self.title}', date='{self.published_date}')"

# A class to store our newsletters after they are sent
class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sent_date = db.Column(db.Date)
    text = db.Column(db.TEXT)

# A class to store email addressess of mailing list members
class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120), unique=True, nullable=False)