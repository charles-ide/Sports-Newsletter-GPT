'''
(c) 2023, Charles Ide
This module contains code that operates our email newsletter landing page.
It is used to collect emails entered in the central landing page and store them in our SQLite database
'''

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import Email, db
from email_sender import send_email

# Configure the  app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# Create the database tables
with app.app_context():
    db.create_all()

# Route to display the form
@app.route('/')
def index():
    return render_template('email_collector.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        email_address = request.form['email']

        # Check if the email is not already in the database
        if not Email.query.filter_by(address=email_address).first():
            # Add the email to the database
            new_email = Email(address=email_address)
            db.session.add(new_email)
            db.session.commit()

            # Send a welcome email to the new joiner
            email_body = "Thank you for signing up for the daily GPT Sports Newsletter! Each morning you will receive an AI generated summary of the daily top sporting headlines."
            send_email(email_body, [email_address], "Welcome to GPT Daily Sports")
        
            return redirect(url_for('success'))

    return render_template('email_collector.html', error="Email address already exists!")

# Route to display a success page
@app.route('/success')
def success():
    emails = Email.query.all()
    return render_template('email_submitted.html', emails=emails)

if __name__ == '__main__':
    app.run(port = 8080)
