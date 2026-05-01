# add an activity to the list
import streamlit as st
from display import display, remove_sidebars
from stored_scraped_data import add_activity, add_comment

display()
remove_sidebars()



st.title("Help out your fellow users and add an activity here!")
# buttons
col1, col2 = st.columns([1,2])
with col1:
    if st.button("👉 Return to Main Menu"):
        st.switch_page("streamlit_app.py")
with col2:
    if st.button("🔍 Back to Activity Page"):
        st.switch_page("pages/activity_page.py")

st.markdown("""
Have you discovered an activity that isn’t on our list?  
Did your family recently visit a new place and have a great experience?

Now’s your chance to share it and help others find amazing activities too!
""")

# from to add activity
with st.form("add_actity_form", clear_on_submit=True):
    name = st.text_input("Activity Name:")
    category = st.selectbox(
        "Choose a Category",
        ["Museums", "History", "Recreation", "Parks", "Other"]
    )
    link = st.text_input("Website Link")
    comment = st.text_area("Provide feedback:", height = 100)
    submitted = st.form_submit_button("Add Activity")

    # check if all categories filled
    if submitted:
        if not name.strip() or not category:
            st.error("Please fill all required fields")
            st.stop()
        if not link.strip():
            add_activity(name, category)
        else:
            add_activity(name, category, link)
        if comment.strip():
            add_comment(name, comment)
        st.toast("✅Activity Added!")
