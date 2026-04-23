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

""" the code below did not work for scaping when I tried it"""
# def scrape_visit_nepa():
#     headers = {"User-Agent": "Mozilla/5.0"}
#     base_url = "https://discovernepa.com/things-to-do/search/"
#     page_num = 1
#     page = requests.get(f"{base_url}?categories%5B%5D=52&categories%5B%5D=53&categories%5B%5D=61&categories%5B%5D=74&categories%5B%5D=93&categories%5B%5D=56&categories%5B%5D=97&categories%5B%5D=70&categories%5B%5D=72&categories%5B%5D=102&categories%5B%5D=99&categories%5B%5D=71&page_num={page_num}&location%5B%5D=269385&locationType%5B%5D=city", headers=headers)
#     soup = BeautifulSoup(page.content, "html.parser")
#     # dictionary with all the activities
#     activities_data = []
#     # html under landmarks and attractions
#     items = soup.find_all("a", class_="vue-listing-card")
#     # go through the heading
#     for item in items:
#         link = item.get("href", "")
#         name = item.find("h3").text
#         category = item.find("div", class_="eyebrow").text
#         # add to the dictionary: only include activities ( not random <a>'s)

#         activities_data.append({
#             "name": name,
#             "category":category,
#             "link": link
#             })
#     return activities_data
#https://www.visitnepa.org/plugins/maps/map/things-to-do-in-scranton/6503247a175f177b67c029f9/?embed=true
        
