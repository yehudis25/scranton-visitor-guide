# this module connects the dybs setup with the scraped data
from stored_scraped_data import  insert_all
from scraper import scrape_activities

def connecter():
    # scrape the activities
    activities = scrape_activities()
    insert_all(activities)
print(scrape_activities())