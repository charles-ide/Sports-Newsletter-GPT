'''
(c) Charles Ide, November 22 2023
This file will be used to save my past newsletters to the MySQL database
'''

import os
from datetime import datetime

from flask import Flask

from helper_modules.models import db, Newsletter

# A function to add a newsletter object to our MySQL database
def add_newsletter_to_db(app, newsletter_text):
    newsletter_data = Newsletter(
        sent_date = datetime.now().strftime("%Y-%m-%d"),
        text = newsletter_text
    )
    
    with app.app_context():
        db.session.add(newsletter_data)
        db.session.commit()


if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_PATH")
    db.init_app(app)

    sample_body = "This is a sample newsletter body"
   
    add_newsletter_to_db(app, sample_body)

    