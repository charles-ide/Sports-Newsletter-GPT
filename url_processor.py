'''
(c) Charles Ide, November 6 2023
This file will be used to process the page contents of a specified URL in our web app
'''

import requests
from bs4 import BeautifulSoup
import textwrap
from flask_sqlalchemy import SQLAlchemy
from models import db, Story
from flask import Flask


def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title of story
        title_div = soup.find('h1', class_='Page-headline')        
        if title_div:
            # Extract and print the text content
            title = title_div.get_text(strip=True)
        else:
            title = ""

        
        # Extract text content of story
        text_div = soup.find('div', class_='RichTextStoryBody RichTextBody')        
        if text_div:
            # Extract and print the text content
            text_content = textwrap.fill(text_div.get_text(strip=True), width = 80)
        else:
            text_content = ""

        # Return dictionary of result
        return {
            'url' :  url,
            'title' : title,
            'text' : text_content
        }
        

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    
# A function to scrape the top 8 story URLs off of AP Sports Headlines
def scrape_stories():
    story_urls = []
    try:
        response = requests.get("https://apnews.com/sports")
        response.raise_for_status()  # Raise an HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title of story
        soup_list = soup.find('div', class_="PageList-items")
        promo_divs = soup_list.find_all('div', class_='PagePromo-title')
        for promo_div in promo_divs:
            # Extract links from <a> tags within the found <div> tag
            links = [a['href'] for a in promo_div.find_all('a')]
            story_urls += links
        return story_urls


    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    


def save_stories(story_urls):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()
        for url in story_urls:
            story_dict = get_page_content(url)
            new_story_obj = Story(url=story_dict['url'], title=story_dict['title'], text=story_dict['text'])

            db.session.add(new_story_obj)
            db.session.commit()    

if __name__ == "__main__":
    story_urls = scrape_stories()
    save_stories(story_urls)
    print("Saved")