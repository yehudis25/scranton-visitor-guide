# this is the page which holds the activities to do

import streamlit as st
import pandas as pd
import math
from stored_scraped_data import search_by_category, get_all_activities, update_rating, add_comment, get_comments
from display import display, remove_sidebars

remove_sidebars()
display()

# return stars for the rating amount
def star(rating):
    try:
        if rating is None or math.isnan(rating):
            return ""
        return "⭐" * int(round(float(rating)))
    except:
        return ""

# Find an activity through selecting a category
if "active_rating_id" not in st.session_state:
    st.session_state.active_rating_id = None

st.title("Find an Activity!")
category = st.selectbox(
    "Choose an Activity Category",
    ["See All", "Museums", "History", "Recreation", "Parks"]
) 
# this is the dataframe, either get all the activities or search for an activity:
if category == "See All":
    activity_df = pd.DataFrame(get_all_activities(), columns=["ID", "Name", "Category", "Link", "Rating"])
else:
    activity_df = pd.DataFrame(search_by_category(category), columns=["ID", "Name", "Category", "Link", "Rating"])

st.write("")
st.write("")
# make rows with each activity
for _, row in activity_df.iterrows():
    with st.container():

        st.markdown(f"### {row['Name']}")
        st.markdown(f"{star(row['Rating'])}")
        st.markdown(f"**Category:** {row['Category']}")
        st.markdown(f"[visit 🔗]({row['Link']})")
        # make an expander to see comments on the activity
        with st.expander("See activity feedback👇"):
            comments = get_comments(row["ID"])
            if not comments:
                st.write("No comments here yet😧")
            else:
                for c in comments:
                    st.markdown(f"• {c}")
        # make an expander to add a comment to the actvity
        with st.expander(" ➕➕➕ Add a comment here:"):
            comment = st.text_area("Provide feedback:", height = 100, key=f"comment_{row['ID']}")
            # submit button:
            submitted = st.button("Submit Feedback", key=f"submit_comment_{row['ID']}")
            if submitted:
                add_comment(row['Name'], comment)
                st.success("Submitted!")
            # button to add a rating on the activity
            if st.button("⭐Rate this activity now", key = f"actbtn{row['ID']}"):
                st.session_state["active_rating_id"] = row["ID"]
            if st.session_state.get("active_rating_id") == row["ID"]:
                # slider to rate the activity by
                rating = st.slider("Rate",1,5,  key=f"btn_{row['ID']}_{_}")
                if st.button("Submit rating", key=f"slider_{row['ID']}_{_}"):
                    update_rating(row["Name"], rating)
                    st.success("Rated! ⭐")
                    st.session_state["active_rating_id"] = None 
                    st.session_state.messages = []
                    st.rerun()

        st.write("----------------------------------------------------------------------------")
        st.write("")
# buttons on the bottom of the page
if st.button("🏠 Return to Main Menu"):
    st.switch_page("pages/main_menu.py")
if st.button(" 💬ChatBot "):
    st.switch_page("pages/chatbot.py")