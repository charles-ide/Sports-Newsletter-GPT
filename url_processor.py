'''
(c) Charles Ide, November 6 2023
This file will be used to process the page contents of a specified URL in our web app
'''

import requests
from bs4 import BeautifulSoup

def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text()
        return text_content
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"