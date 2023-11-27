'''
(c) Charles Ide, November 22 2023
This file will be used to save and delete stories to the MySQL database
'''

from helper_modules.models import db, Story
from archive.url_processor import get_page_content


# A function to delete all rows from the story database
def delete_existing_stories(app):    
    with app.app_context():
        db.session.query(Story).delete()
        db.session.commit()

# A function to save scraped story content to our app database
def save_stories_from_urls(story_urls, app):    
    with app.app_context():
        db.create_all()
        for url in story_urls:
            story_dict = get_page_content(url) # Will need to refactor this
            new_story_obj = Story(url=story_dict['url'], title=story_dict['title'], text=story_dict['text'])

            db.session.add(new_story_obj)
            db.session.commit()