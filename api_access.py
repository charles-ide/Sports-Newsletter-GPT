'''
(c) Charles Ide, November 22 2023
This file will be used to query and parse the NewsData API and save stories to the DB
'''
import os
import requests
import csv

from flask import Flask

from helper_modules.models import db, Story
from helper_modules.db_management import delete_existing_stories

# A function to call the NewsData API and return a JSON object
def query_news_api():
    my_api_key = os.environ.get("NEWS_DATA_API_KEY")
    response =requests.get('https://newsdata.io/api/1/news?apikey='+my_api_key+'&category=sports&country=us&timeframe=24&prioritydomain=top&excludedomain=mercurynews.com').json()#&excludedomain=mercurynews
    assert response['status'] == "success", f"Expected status code 200, but got {response['status']}"
    print("Total results: " + str(response['totalResults']))
    result = response['results']
    #write_csv(result, "json_output.csv")
    return result

# A function to parse JSON API calls into a list of story objects
def parse_json_to_stories(API_call_data):
    story_list = []
    for item in API_call_data:
        story_data = parse_json_story(item)
        story_list.append(story_data)
    
    return story_list


# A function to parse the JSON story data into Story objects
def parse_json_story(json_story_data):
    story_data = Story(
        url = json_story_data['link'],
        title = json_story_data['title'],
        source_name = json_story_data['source_id'],
        published_date = json_story_data['pubDate'],
        category = json_story_data['category'],
        country = json_story_data['country'],
        text = json_story_data['content']
    )
    return story_data


# A function to save our Story objects to the database
def save_stories_from_api(story_obj_list, app):    
    with app.app_context():
        for story_obj in story_obj_list:
            db.session.add(story_obj)
            db.session.commit()

# Master function to call API and save stories to database
def call_api_save_stories(app):
    api_call_data = query_news_api()
    print("Queried API")
    story_list = parse_json_to_stories(api_call_data)
    print("Parsed JSON into Story list")
    save_stories_from_api(story_list, app)
    print("Saved stories to SQL database")


if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_PATH")
    db.init_app(app)
   
    #with app.app_context():
        #delete_existing_stories(app)
    
    call_api_save_stories(app)





# A helper function to test API querying
def write_csv(json_data, csv_file_name):
    with open(csv_file_name, 'w', newline='') as csv_file:
    # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        # Write the header (column names) to the CSV file
        header = json_data[0].keys()
        csv_writer.writerow(header)

        # Write the data from the JSON object to the CSV file
        for row in json_data:
            csv_writer.writerow(row.values())

    print(f"CSV file '{csv_file_name}' created successfully.")