# the following code will scrape off all the attractions mentioned on Scranton, PA's wikipidia page

import requests
from bs4 import BeautifulSoup


def scrape_activities():
    # get URL to find activities
    headers = {"User-Agent": "Mozilla/5.0"}   # needed this for wiki to allow me to scrape
    page = requests.get("https://en.wikipedia.org/wiki/Scranton,_Pennsylvania", headers = headers)
    soup = BeautifulSoup(page.content, "html.parser")
    # dictionary with all the activities
    activities_data = []
    # html under landmarks and attractions
    heading = soup.find(id = "Landmarks_and_attractions")
    # go through the heading
    for tag in heading.find_all_next():
        # once it reaches the next h3 heading: stop
        if tag.name == "h3" and tag.encode() != heading.encode():
            break
        # each paragraph of the html code is a new category
        if tag.name == "p":
            text = tag.get_text()
            if ("heritage" in text):
                current_category = "History"
            elif ("Museums" in text):
                current_category = "Museum"
            elif ("recreation" in text):
                current_category = "Recreation"
            else:
                current_category = None

            # every <a> tag is a new attraction
            for attraction in tag.find_all("a"):
                link = attraction.get("href", "")
                name = attraction.get("title", "")
                # there were some things under the wrong category - change it here:
                if ("Park" in name):
                    current_category = "Park"
                if ("Museum" in name):
                    current_category = "Museum"
                # add to the dictionary: only include activities ( not random <a>'s)
                if (name != ""):
                    activities_data.append({
                    "name": name,
                    "category": current_category,
                    "link": "https://en.wikipedia.org" + link
                })
    return activities_data


