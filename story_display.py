'''
(c) Charles Ide, November 6 2023
This file will serve as the entrypoint for our Newsletter GPT application
'''
from flask import Flask, render_template, request, redirect, url_for
from url_processor import get_page_content
from flask_sqlalchemy import SQLAlchemy
from models import db, Story

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        story_dict = get_page_content(url)
        new_story_obj = Story(url=story_dict['url'], title=story_dict['title'], text=story_dict['text'])

        db.session.add(new_story_obj)
        db.session.commit()
        
    story_list = []

    stories = Story.query.all()
    for story in stories:

        story_data = {
            'url' :  story.url,
            'title' : story.title,
            'text' : story.text
        }

        story_list.append(story_data)
    
    return render_template('story_display.html', story_list = story_list)

@app.route('/scrape_stories', methods=['POST'])
def scrape_stories():
    # Write code to scrape multiple stories

    return redirect(url_for('index'))

@app.route('/delete_all_rows', methods=['POST'])
def delete_all_rows():
    # Delete all rows from the database
    db.session.query(Story).delete()
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/summary', methods=['POST'])
def summarize_results():
    return render_template('summary.html')

if __name__ == '__main__':
    app.run(port=8000, debug=True)
