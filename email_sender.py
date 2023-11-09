'''
(c) 2023, Charles Ide
This module will automatically send emails to emails stored in a database
'''
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

from models import db, Email, Story

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from gpt_summary import summarize_text


def generate_email_subject():
    # Get today's date
    today = datetime.now()

    # Format the date as "Month Day, Year"
    formatted_date = today.strftime("%B %eth, %Y")

    return "Daily GPT Sports Newsletter: " + formatted_date

def send_email(email_text, email_recipients, subject):
    sender_email = os.environ.get("NEWSLETTER_EMAIL_ADDR")
    sender_password = os.environ.get("NEWSLETTER_APP_PW")

    # Recipient's email address
    for recipient in email_recipients:

    # Email content
        # Create a MIMEText object for the email body
        email_body = MIMEText(email_text, "plain")

        # Create a MIMEMultipart object to represent the email
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient
        message["Subject"] = subject

        # Attach the email body to the MIMEMultipart object
        message.attach(email_body)

        # Set up the SMTP server
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Establish a connection to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Log in to the email account
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, recipient, message.as_string())

        # Close the connection to the SMTP server
        server.quit()
    
def query_mailing_list():
    # Configure the database URI
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'  # Replace with your actual database URI
    db.init_app(app)
    # Query all rows from the Email table
    with app.app_context():
        emails = Email.query.all()

    # Extract the data from the query result
    email_list = [email.address for email in emails]
    # Print the list of emails (you can return it or use it as needed)
    return email_list

def generate_email_body():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'  # Replace with your actual database URI
    db.init_app(app)
    # Query all rows from the Email table
    with app.app_context():
        stories = Story.query.all()
    
    story_text = [story.text for story in stories]

    text_summary_full = ""
    n=0
    for story_body in story_text: # Rename variables
        n+=1
        print(str(n) + "\n\n")
        text_summary = summarize_text(story_body) + "\n"
        text_summary_full += str(text_summary) 
        text_summary_full += "\n\n"


    return text_summary_full
                  



if __name__ == "__main__":
    email_body = generate_email_body()
    print(email_body)
    mailing_list = query_mailing_list()
    print(mailing_list)
    subject = generate_email_subject()
    print(subject)
    send_email(email_body, mailing_list, subject)