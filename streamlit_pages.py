import streamlit as st
import pandas as pd
from stored_scraped_data import search_by_category, get_all_activities
from connecter import connecter

def star(rating):
    if rating is None:
        return ""
    return "⭐" * int(round(float(rating)))

def mainmenu():
    st.title("🌆Welcome to Scranton, PA! ")

    st.markdown("""
    ### Bored this Chol Hamoed? We've got you covered!

    Whether you're visiting or you've lived here forever and *still* can't think of where to go —
    this guide is here to save the day.

    🚗 Discover fun trips  
    🌳 Find hidden parks  
    👨‍👩‍👧‍👦 Plan activities your whole family will love  

     """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e5/Electric_City_sign_daylight_Scranton_PA.JPG")

    st.markdown("""
    👉 Use the sidebar to explore activities or click the buttons below
    """)
    if st.button("🔍 Find Activities Now"):
        st.switch_page("pages/activities.py")

    st.markdown("""
    💡 Don't keep your ideas to yourself —
    add your favorite spots to help the next family using this app!
    """)
    if st.button("🚴 Add An Activity to Our List"):
        st.switch_page()

def activity_page():
    connecter()
    st.title("Find an Activity!")
    category = st.selectbox(
        "Choose an Activity Category",
        ["Parks", "Museums", "History", "Recreation", "See All"]
    ) 
    # this is the list:
    if category == "See All":
        activity_df = pd.DataFrame(get_all_activities(), columns=["ID", "Name", "Category", "Link", "Rating"])
    else:
        activity_df = pd.DataFrame(search_by_category(category), columns=["ID", "Name", "Category", "Link", "Rating"])
    

    for _, row in activity_df.iterrows():
        with st.container():
            col1, col2 = st.columns([4,1])
            with col1:
                st.markdown(f"### {row['Name']}")
                st.markdown(f"**Category:** {row['Category']}")
                st.markdown(f"[visit 🔗]({row['Link']})")
            with col2:
                st.markdown(f"### {star(row['Rating'])}")
activity_page()

