# this module connects the dtbs setup with the scraped data
from stored_scraped_data import  insert_all, create_database
from scraper import scrape_activities

def connecter():
    # scrape the activities
    activities = scrape_activities()
    create_database()
    insert_all(activities)