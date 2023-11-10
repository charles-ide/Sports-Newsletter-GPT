'''
(c) 2023 Charles Ide
This will be the main script that executes each day to send out 
'''

from url_processor import delete_existing_stories, get_page_content, save_stories, scrape_stories
from email_sender import generate_email_body, generate_email_subject, query_mailing_list, send_email

# Main script
delete_existing_stories()

story_urls = scrape_stories()
save_stories(story_urls)

email_body = generate_email_body()
mailing_list = query_mailing_list()
subject = generate_email_subject()
send_email(email_body, mailing_list, subject)