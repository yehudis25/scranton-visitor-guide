# program to insert, update, delete, and query the scraped activities into a sqlite dtbs

from scraper import scrape_activities
import sqlite3
import pandas as pd

""" create a dtbs with a table of activities to do in Scranton """

def create_database(dtbs_name="activities.db"):
    conn = sqlite3.connect(dtbs_name)  # connecting to database
    cur = conn.cursor()
    # make the table:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS activities(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            link TEXT,
            rating_sum INTEGER,
            rating_count INTEGER
        )
    """)
    conn.commit()

    # make a table with all the comments on each activity
    cur.execute("""
        CREATE TABLE IF NOT EXISTS comments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        activity_id INTEGER,
        comment TEXT,
        FOREIGN KEY (activity_id) REFERENCES activities(id)   # Connect the 2 tables
        )
    """)
    conn.commit()
    # scrape the activities and make them into a list of tuples (for sqlite)
    activities = scrape_activities()
    activity_tuples = []
    for activity in activities:
        activity_tuples.append((activity["name"], activity["category"], activity["link"]))
    cur.execute("SELECT COUNT(*) FROM activities")
    count = cur.fetchone()[0]
    if count == 0:
        # insert each activity into the dtbs
         cur.executemany("INSERT INTO activities (name, category, link) VALUES (?,?,?)", activity_tuples)
         conn.commit()
    conn.close()

""" method to return all the activities in the dtbs"""

def get_all_activities():
    conn = sqlite3.connect("activities.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM activities")
    rows = cur.fetchall()
    conn.close()
    return rows

""" method to search activities by there categories"""

def search_by_category(category):
    conn = sqlite3.connect("activities.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM activities WHERE category = ?", (category,))
    queried_activities = cur.fetchall()
    conn.close()
    return queried_activities

""" method to update the ratings on the activity"""

def update_rating(name, rating):
    conn = sqlite3.connect("activities.db")
    cur = conn.cursor()
    cur.execute("SELECT rating_sum, rating_count FROM activities WHERE name = ?", (name,))
    result = cur.fetchone()
    if result:
        current_sum, current_count = result
        # make them into ints
        if current_sum is None:
            current_sum = 0
        if current_count is None:
            current_count = 0
       
       # add the rating to the sum and the count to the count of ratings (for future refrences sum / count = rating)
        current_sum += int(rating)
        current_count += 1
        # update the rating
        cur.execute("UPDATE activities SET rating_sum = ?, rating_count = ? WHERE name = ?", (current_sum, current_count, name))
        conn.commit()
    conn.close()

""" method to delete an activity"""

def delete_activity(name):
    conn = sqlite3.connect("activities.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM activities WHERE name = ?", (name, ))
    conn.commit()
    conn.close()

""" method to add comments on the activity"""

def add_comment(activity_name, comment):
    conn = sqlite3.connect("activities.db")
    cur = conn.cursor()
    # first commect to activities table to get the activity ID
    cur.execute("SELECT id FROM activities WHERE name = ?", (activity_name,))
    result = cur.fetchone()
    if result:
        activity_id = result[0]
        cur.execute("INSERT INTO comments (activity_id, comment) VALUES (?,?)", (activity_id, comment))
        conn.commit()
    conn.close()

""" method to add an activity to the dtbs"""

def add_activity(activity_name, category, link=None):
    conn = sqlite3.connect("activities.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO activities (name, category, link) VALUES (?,?,?)", (activity_name, category, link))
    conn.commit()
    conn.close()