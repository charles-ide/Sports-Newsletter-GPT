'''
(c) Charles Ide, November 6 2023
This file will be used to process the page contents of a specified URL in our web app
'''

import requests
from bs4 import BeautifulSoup
import textwrap

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