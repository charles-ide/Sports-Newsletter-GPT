'''
(c) 2023 Charles Ide
This script is meant to be executed daily to send out the newsletter. It performs the following actions:
1. Query and save a fresh slate of story URLs each day
2. Generate an email based on GPT summaries of that day's top stories
3. Send the email out to our mailing list
'''
import os

from flask import Flask

from helper_modules.email_sender import generate_email_body, generate_email_subject, query_mailing_list, send_email
from helper_modules.models import db
from helper_modules.api_access import call_api_save_stories
from helper_modules.save_newsletters import add_newsletter_to_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_PATH")
db.init_app(app)

# Scrape and save today's top stories
call_api_save_stories(app)

# Generate and send our daily newsletter to our recipients
email_body = generate_email_body(app)
mailing_list = query_mailing_list(app)
subject = generate_email_subject()
send_email(email_body, mailing_list, subject)

# Save our newsletter to our database
add_newsletter_to_db(app, email_body)
