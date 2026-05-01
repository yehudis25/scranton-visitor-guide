# this is the page which holds the activities to do

import streamlit as st
import pandas as pd
import math
from stored_scraped_data import search_by_category, get_all_activities, update_rating, add_comment, get_comments, delete_activity
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


# when activity is deleted this pops up:
if st.session_state.get("show_toast"):
    st.toast("Deleted ✅")
    st.session_state["show_toast"] = False

# when you rate an activity this pops up
if st.session_state.get("show_rated_added"):
    st.toast("Thank you for your feedback✅")
    st.session_state["show_toast"] = False

# 2 columns : one for adding activity btn and 2 for the title
col3, col4 = st.columns([3,1])
with col3:
    st.title("Find an Activity!")
with col4:
    st.write("")
    st.write("")
    if st.button("🚴 Add Activity Here"):
        st.switch_page("pages/add_an_activity.py")
    if st.button("📊 Category Stats"):
        st.switch_page("pages/category_stats.py")

# select a category
category = st.selectbox(
    "Choose an Activity Category",
    ["See All", "Museums", "History", "Recreation", "Parks"]
) 

# this is the dataframe, either get all the activities or search for an activity:
if category == "See All":
    activity_df = pd.DataFrame(get_all_activities(), columns=["ID", "Name", "Category", "Link", "Rating"])
else:
    activity_df = pd.DataFrame(search_by_category(category), columns=["ID", "Name", "Category", "Link", "Rating"])
# sort by rating
activity_df["Rating"] = pd.to_numeric(activity_df["Rating"], errors="coerce")
activity_df = activity_df.sort_values(by="Rating", ascending=False)

st.write("")
st.write("")
st.write("------------------------------------------------------------------------")
# make rows with each activity
for _, row in activity_df.iterrows():
    with st.container():
        col5, col6 = st.columns([3,1])
        with col5:
            st.markdown(f"### {row['Name']}")
        with col6:
            st.write("")
            st.markdown(f"{star(row['Rating'])}")

        # make an expander to see more on the activity
        with st.expander("View More  Info..."):
            st.markdown(f"**Category:** {row['Category']}")
            st.markdown(f"[visit 🔗]({row['Link']})")
            comments = get_comments(row["ID"])
            st.markdown(f"**Feedback:**")
            if not comments:
                st.write("No comments here yet😧")
            else:
                for c in comments:
                    st.markdown(f"• {c}")


            with st.form(key=f"comment_form_{row['ID']}", clear_on_submit=True):
                comment = st.text_area("Provide feedback:", height=100)

                submitted = st.form_submit_button("Submit Feedback")
                if submitted and comment.strip():
                    add_comment(row['Name'], comment)
                    st.toast("Feedback Added ✅")

            # button to add a rating on the activity
            if st.button("⭐Rate this activity now", key = f"actbtn{row['ID']}"):
                st.session_state["active_rating_id"] = row["ID"]
            if st.session_state.get("active_rating_id") == row["ID"]:
                # slider to rate the activity by
                rating = st.slider("Rate",1,5,  key=f"btn_{row['ID']}_{_}")
                if st.button("Submit rating", key=f"slider_{row['ID']}_{_}"):
                    update_rating(row["Name"], rating)
                    st.session_state["show_rated_added"] = True
                    st.session_state["active_rating_id"] = None 
                    st.session_state.messages = []
                    st.rerun()

            # delete an activity
            if st.button("🗑️", key = f"deletebtn{row['ID']}"):
                if st.session_state.get("delete_activity") == row["ID"]:
                    st.session_state["delete_activity"] = None
                else:
                    st.session_state["delete_activity"] = row["ID"]
            # show warning if you want to delete it
            if st.session_state.get("delete_activity")== row["ID"]:
                st.warning("are you sure you want to delete this activity?")
                col1, col2 = st.columns([1,9])
                with col1:
                    if st.button("Yes", key = f"deletebtnyes{row['ID']}"):
                        delete_activity(row["Name"])
                        st.session_state["show_toast"] = True
                        st.session_state["delete_activity"] = None
                        st.rerun()
                with col2:
                    if st.button("No", key = f"deletebtnno{row['ID']}"):
                        st.session_state["delete_activity"] = None
                        st.rerun()

        st.write("----------------------------------------------------------------------------")
        st.write("")
# buttons on the bottom of the page
if st.button("Return to Main Menu"):
    st.switch_page("streamlit_app.py")
if st.button(" 💬ChatBot "):
    st.switch_page("pages/chatbot.py")