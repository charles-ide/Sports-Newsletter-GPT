'''
(c) Charles Ide, November 22 2023
This file will be used to query and parse the NewsData API and save stories to the DB
'''
import os
import requests
import csv

from helper_modules.models import db, Story


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

# A function to call the NewsData API and return a JSON object
def query_news_api():
    my_api_key = os.environ.get("NEWS_DATA_API_KEY")
    response =requests.get('https://newsdata.io/api/1/news?apikey='+my_api_key+'&category=sports&country=us&timeframe=24&prioritydomain=top').json()
    assert response['status'] == "success", f"Expected status code 200, but got {response['status']}"
    print("Total results: " + str(response['totalResults']))
    result = response['results']
    print(len(result))
    page2_key = response['nextPage']
    second_response = requests.get('https://newsdata.io/api/1/news?apikey='+my_api_key+'&category=sports&country=us&timeframe=24&prioritydomain=top&page='+str(page2_key)).json()
    result+=second_response['results']
    print(len(result))
    write_csv(result, "json_output.csv")

    return

# A function to parse JSON API calls into a list of story objects
def parse_json_to_stories(API_call_data):
    return


# A function to parse the JSON story data into Story objects
def parse_json_story(json_story_data):
    return


# A function to save our Story objects to the database
def save_stories_from_api(story_obj_list, app):    
    with app.app_context():
        for story_obj in story_obj_list:
            db.session.add(story_obj)
            db.session.commit()



if __name__ == "__main__":
    query_news_api()


