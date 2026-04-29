# this is the page which holds the activities to do

import streamlit as st
import pandas as pd
from stored_scraped_data import search_by_category, get_all_activities, update_rating

# return stars for the rating amount
def star(rating):
    if rating is None:
        return ""
    return "⭐" * int(round(float(rating)))

""" find an activity through selecting a category"""

st.title("Find an Activity!")
category = st.selectbox(
    "Choose an Activity Category",
    ["Parks", "Museums", "History", "Recreation", "See All"]
) 
# this is the dataframe, either get all the activities or search for an activity:
if category == "See All":
    activity_df = pd.DataFrame(get_all_activities(), columns=["ID", "Name", "Category", "Link", "Rating"])
else:
    activity_df = pd.DataFrame(search_by_category(category), columns=["ID", "Name", "Category", "Link", "Rating"])

# make rows with each activity
for _, row in activity_df.iterrows():
    with st.container():
        col1, col2 = st.columns([4,1])
        with col1:
            st.markdown(f"### {row['Name']}")
            st.markdown(f"**Category:** {row['Category']}")
            st.markdown(f"[visit 🔗]({row['Link']})")
        with col2:
            st.markdown(f"### {star(row['Rating'])}")
            if st.button("⭐Rate this activity now"):
                rating = st.slider(max_value=5)
                update_rating(row['name'], input)

if st.button("👉 Return to Main Menu"):
    st.switch_page("pages/main_menu.py")