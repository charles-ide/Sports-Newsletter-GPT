'''
(c) 2023, Charles Ide
This module contains functions that generate email contents and send emails to all members of our
mailing list.
'''
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask
import os

from models import db, Email, Story
from gpt_summary import summarize_text

# A function to generate the email subject based on today's date
def generate_email_subject():
    today = datetime.now()
    # Format the date as "Month Day, Year"
    formatted_date = today.strftime("%B %eth, %Y")
    return "Daily GPT Sports Newsletter: " + formatted_date

# A function to query our email mailing list stored in our database
def query_mailing_list(app):
    db.init_app(app)
    
    with app.app_context():
        emails = Email.query.all()

    email_list = [email.address for email in emails]
    return email_list


# A function that generates our email body based on saved story text
# TODO: Break this into functions that return our story body list and that summarize our test
def generate_email_body(app):
    db.init_app(app)
    
    # Query all rows from the Email table
    with app.app_context():
        stories = Story.query.all()
    
    story_body_list = [story.text for story in stories]

    text_summary_full = ""
    n=0
    for story_body in story_body_list: # Rename variables
        n+=1
        print(str(n) + "\n\n") # To track progress during execution
        text_summary = summarize_text(story_body) + "\n"
        text_summary_full += str(text_summary) 
        text_summary_full += "\n\n"

    return text_summary_full

# A function to access our Gmail account and send out the newsletter to our mailing list
def send_email(email_text, email_recipients, subject):
    sender_email = os.environ.get("NEWSLETTER_EMAIL_ADDR")
    sender_password = os.environ.get("NEWSLETTER_APP_PW")

    # Set up the SMTP server and establish a connection
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    server.login(sender_email, sender_password)

    for recipient in email_recipients:
        # Create a MIMEText object for the email body
        email_body = MIMEText(email_text, "plain")

        # Create a MIMEMultipart object to represent the email
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient
        message["Subject"] = subject

        # Attach the email body to the MIMEMultipart object
        message.attach(email_body)

        server.sendmail(sender_email, recipient, message.as_string())

    server.quit()
                  


if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
   
    email_body = generate_email_body(app)
    mailing_list = query_mailing_list(app)
    subject = generate_email_subject()
   
    send_email(email_body, mailing_list, subject)