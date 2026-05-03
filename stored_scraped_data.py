# program to insert, update, delete, and query the scraped activities into a sqlite dtbs

import sqlite3

""" create a dtbs for table of activities to do in Scranton """


def create_database(db="activities.db"):
    conn = sqlite3.connect(db)  # connecting to database
    cur = conn.cursor()
    # make the table:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS activities(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            link TEXT UNIQUE,
            rating_sum INTEGER DEFAULT 0,
            rating_count INTEGER DEFAULT 0
        )
    """)
    conn.commit()

    # make a table with all the comments on each activity
    cur.execute("""
        CREATE TABLE IF NOT EXISTS comments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        activity_id INTEGER,
        comment TEXT,
        FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()


"""insert all the activities into the dtbs"""


def insert_all(activities, db="activities.db"):
    conn = sqlite3.connect(db)  # connecting to database
    cur = conn.cursor()
    activity_tuples = []
    for activity in activities:
        activity_tuples.append((activity["name"], activity["category"], activity["link"]))

    # insert each activity into the dtbs
    cur.executemany(
        "INSERT OR IGNORE INTO activities (name, category, link) VALUES (?,?,?)",
        activity_tuples,
    )
    conn.commit()
    conn.close()


""" method to return all the activities in the dtbs"""


def get_all_activities(db="activities.db"):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("""
        SELECT
            id,
            name,
            category,
            link,
            CASE
                WHEN rating_count = 0 THEN 0
                ELSE CAST(rating_sum AS FLOAT) / rating_count
            END AS rating
        FROM activities
        """)
    rows = cur.fetchall()
    conn.close()
    return rows


""" method to search activities by there categories"""


def search_by_category(category, db="activities.db"):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("""
        SELECT
            id,
            name,
            category,
            link,
            CASE
                WHEN rating_count = 0 THEN 0
                ELSE CAST(rating_sum AS FLOAT) / rating_count
            END AS rating
        FROM activities
        WHERE category = ?
        """, (category,))
    queried_activities = cur.fetchall()
    conn.close()
    return queried_activities


""" method to update the ratings on the activity"""


def update_rating(name, rating, db="activities.db"):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(
        "SELECT rating_sum, rating_count FROM activities WHERE name = ?",
        (name,),
    )
    result = cur.fetchone()
    if result:
        current_sum, current_count = result
        # make them into ints
        if current_sum is None:
            current_sum = 0
        if current_count is None:
            current_count = 0
        # add the rating to the sum and the count to the count of
        # ratings (for future refrences sum / count = rating)
        current_sum += int(rating)
        current_count += 1
        # update the rating
    cur.execute(
        "UPDATE activities SET rating_sum = ?, rating_count = ? WHERE name = ?",
        (current_sum, current_count, name),
    )
    conn.commit()
    conn.close()


""" method to delete an activity"""


def delete_activity(name, db="activities.db"):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("DELETE FROM activities WHERE name = ?", (name, ))
    conn.commit()
    conn.close()


""" method to add comments on the activity"""


def add_comment(activity_name, comment, db="activities.db"):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    # first commect to activities table to get the activity ID
    cur.execute("SELECT id FROM activities WHERE name = ?", (activity_name,))
    result = cur.fetchone()
    if result:
        activity_id = result[0]
        # check if comment exists
        cur.execute(
            "SELECT 1 FROM comments WHERE activity_id = ? AND comment = ?", (activity_id, comment)
        )
        exists = cur.fetchone()
        if not exists:
            cur.execute(
                "INSERT INTO comments (activity_id, comment) VALUES (?,?)",
                (activity_id, comment),
            )
            conn.commit()
    conn.close()


def get_comments(id, db="activities.db"):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("""
        SELECT comment
        FROM comments
        WHERE activity_id = ?
        """, (id,))
    rows = cur.fetchall()
    conn.close()
    return rows


""" method to add an activity to the dtbs"""


def add_activity(activity_name, category, link=None, db="activities.db"):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO activities (name, category, link) VALUES (?,?,?)",
        (activity_name, category, link),
    )
    conn.commit()
    conn.close()
