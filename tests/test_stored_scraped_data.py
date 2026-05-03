# test code to test stored_scraped_data

import sqlite3
import pytest
from stored_scraped_data import create_database, insert_all, get_all_activities, search_by_category, update_rating, delete_activity, add_comment, get_comments, add_activity
import os

# the test DTBS
TEST_DB = "test_activities.db"
# fake activities
test_activities = [
    {
        "name": "Test Place",
        "category": "Museums",
        "link": "https://en.wikipedia.org/wiki/Test"
    },
    {
        "name": "Another Place",
        "category": "Parks",
        "link": "https://en.wikipedia.org/wiki/Another"
    }
]

# make new DTBS
@pytest.fixture
def db():
    # ensure clean test DB only
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    create_database(TEST_DB)

    yield TEST_DB

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

""" test create dtbs make sure it creates with proper tables"""
def test_create_database(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # get all table names
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cur.fetchall()]

    conn.close()
    assert "activities" in tables
    assert "comments" in tables

"""test to make sure MT DTBS returns []"""
def test_empty_dtbs(db):
    rows = get_all_activities(db)
    assert rows ==[]
    results = search_by_category("Museums", db)
    assert results == []

"""test the insert all to make sure the data gets inserted"""
def test_insert_all(db):
    insert_all(test_activities, db)
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute("SELECT name, category, link FROM activities")
    rows = cur.fetchall()

    conn.close()

    assert ("Test Place", "Museums", "https://en.wikipedia.org/wiki/Test") in rows
    assert ("Another Place", "Parks", "https://en.wikipedia.org/wiki/Another") in rows

"""test to make sure get all activities really returns activities"""
def test_get_all_activities(db):
    insert_all(test_activities, db)
    rows = get_all_activities(db)
    assert any(
        row[1] == "Test Place" and
        row[2] == "Museums" and
        row[3] == "https://en.wikipedia.org/wiki/Test"
        for row in rows
    )

    assert any(
        row[1] == "Another Place" and
        row[2] == "Parks" and
        row[3] == "https://en.wikipedia.org/wiki/Another"
        for row in rows
    )

"""make sure the search by categorie works"""
def test_search_by_category(db):
    insert_all(test_activities, db)

    results = search_by_category("Museums", db)
    assert any(
        row[1] == "Test Place" and
        row[2] == "Museums" and
        row[3] == "https://en.wikipedia.org/wiki/Test"
        for row in results
    )

"""make sure the update rating works"""
def test_update_rating(db):
    insert_all(test_activities, db)
    name = "Test Place"
    update_rating(name, 4, db)
    update_rating(name, 2, db)
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute("SELECT rating_sum, rating_count FROM activities WHERE NAME = ?", (name,))
    rating_sum, rating_count = cur.fetchone()
    assert rating_sum == 6
    assert rating_count == 2

"""make sure the delete activities works"""
def test_delete_activities(db):
    name = "Test Place"
    delete_activity(name, db)
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute("SELECT * FROM activities WHERE name = ?", (name,))
    result = cur.fetchone()

    assert result is None

"""test for adding and then getting the comment if it works"""
def test_add_get_comment(db):
    insert_all(test_activities, db)
    name = "Test Place"
    comment = "hello, world"

    add_comment(name, comment, db)
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT id FROM activities WHERE name = ?", (name,))
    activity_id = cur.fetchone()[0]
    comments = get_comments(activity_id, db)
    for c in comments:
        assert c[-1] == comment

"""test to add an activity"""
def test_add_activity(db):
    add_activity("Fake", "History", db=db)
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute("SELECT name, category FROM activities")
    rows = cur.fetchall()

    conn.close()
    assert ("Fake", "History") in rows

"""update when thier is no activity"""
def test_update_no_activity(db):
    update_rating("hi", 5, db)
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT * FROM activities WHERE name = ?",("hi",))
    result = cur.fetchone()
    assert result is None
