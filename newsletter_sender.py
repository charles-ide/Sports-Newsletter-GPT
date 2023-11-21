'''
(c) 2023 Charles Ide
This script is meant to be executed daily to send out the newsletter. It performs the following actions:
1. Query and save a fresh slate of story URLs each day
2. Generate an email based on GPT summaries of that day's top stories
3. Send the email out to our mailing list
'''
import os

from flask import Flask

from helper_modules.url_processor import delete_existing_stories, get_page_content, save_stories, scrape_stories
from helper_modules.email_sender import generate_email_body, generate_email_subject, query_mailing_list, send_email
from helper_modules.models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("AMAZON_DB_PATH")
db.init_app(app)

# Clear out our DB of existing stories
# TODO: Attach a date column to our DB and just summarize stories from that day. This way we can save old newsletters
delete_existing_stories(app)
print("Cleared DB")

# Scrape and save today's top stories
story_urls = scrape_stories()
print("Scraped stories")
save_stories(story_urls, app)
print("Saved Stories")

# Generate and send our daily newsletter to our recipients
email_body = generate_email_body(app)
mailing_list = query_mailing_list(app)
subject = generate_email_subject()
send_email(email_body, mailing_list, subject)

# TODO: Save our newsletter text in a new table, newsletters in our DB