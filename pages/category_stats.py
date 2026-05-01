# program to show category stats

import streamlit as st
import pandas as pd
from stored_scraped_data import search_by_category, get_all_activities
from display import display, remove_sidebars

remove_sidebars()
display()

if st.button("Return to Main Menu"):
    st.switch_page("main_menu.py")

st.subheader("📊 Activity Breakdown")
st.caption("Click filters above to explore how activities are distributed")
activities = get_all_activities()
df = pd.DataFrame(activities)
    
# do the chart based on the activities
chart_data = df[2].value_counts()
# show the top category
top_category = chart_data.idxmax()
st.success(f"🏆 Top Category Count: {top_category}")
# select a category for dataframe
selected = st.selectbox("Explore category", chart_data.index)
st.text("See activities below")

# bar chart with categories
st.bar_chart(chart_data)
st.subheader(f"Activities in: {selected}")
# dataframe of category shown
st.dataframe(df[df[2] == selected])
if st.button("🚴 Explore Activities Now"):
    st.switch_page("pages/activity_page.py")
if st.button(" 💬ChatBot "):
    st.switch_page("pages/chatbot.py")
