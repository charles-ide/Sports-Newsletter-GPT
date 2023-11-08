'''
(c) Charles Ide, November 6 2023
This file will serve as the entrypoint for our Newsletter GPT application
'''
from flask import Flask, render_template, request
from url_processor import get_page_content
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stories.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500))
    title = db.Column(db.String(500))
    text = db.Column(db.String(100000), nullable=False)

with app.app_context():
    db.create_all()
    db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_url', methods=['POST'])
def process_url_route():
    if request.method == 'POST':
        url = request.form['url']
        story_dict = get_page_content(url)

        new_story_obj = Story(url=story_dict['url'], title=story_dict['title'], text=story_dict['text'])

        db.session.add(new_story_obj)
        db.session.commit()

        return render_template('result.html', url=url, page_content=story_dict['text'])
    return render_template('index.html')

@app.route('/new', methods=['GET', 'POST'])
def index_new():
    if request.method == 'POST':
        url = request.form.get('url')
        story_dict = get_page_content(url)
        new_story_obj = Story(url=story_dict['url'], title=story_dict['title'], text=story_dict['text'])

        db.session.add(new_story_obj)
        db.session.commit()
        
    story_list = []

    with app.app_context():
        stories = Story.query.all()
        for story in stories:

            story_data = {
                'url' :  story.url,
                'title' : story.title,
                'text' : story.text
            }

            story_list.append(story_data)
    
    return render_template('index_new.html', story_list = story_list)

if __name__ == '__main__':
    app.run(port=8000, debug=True)