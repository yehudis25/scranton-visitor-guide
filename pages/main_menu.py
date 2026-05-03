"""main menu page"""
import streamlit as st
from display import display, remove_sidebars
remove_sidebars()



st.title("🌆Welcome to Scranton, PA! ")
display()
st.markdown("""
### Bored this Chol Hamoed? We've got you covered!

Whether you're visiting or you've lived here forever and *still* can't think of where to go —
this guide is here to save the day.

🚗 Discover fun trips  
🌳 Find hidden parks  
👨‍👩‍👧‍👦 Plan activities your whole family will love  

    """)
# picture of scranton icon
st.image("https://upload.wikimedia.org/wikipedia/commons/e/e5/Electric_City_sign_daylight_Scranton_PA.JPG")

st.markdown("""
👉 Click the button below to find, rate, and comment on all our activities!
""")
# button to go to activities page
if st.button("🔍 Find Activities Now"):
    st.switch_page("pages/activity_page.py")
# button for stat page
if st.button("📊 See Category Stats"):
    st.switch_page("pages/category_stats.py")

st.markdown("""
💡 Don't keep your ideas to yourself —
add your favorite spots to help the next family using this app!
""")
col1, col2 = st.columns([5,1])
# button to add an activity
with col1:
    if st.button("🚴 Add An Activity to Our List"):
        st.switch_page("pages/add_an_activity.py")
# button to go to chatbot
with col2:
    if st.button(" 💬ChatBot "):
        st.switch_page("pages/chatbot.py")
