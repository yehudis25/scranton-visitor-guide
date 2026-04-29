"""main menu page"""
import streamlit as st

st.title("🌆Welcome to Scranton, PA! ")

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
👉 Use the sidebar to explore activities or click the buttons below
""")
# button to go to activities page
if st.button("🔍 Find Activities Now"):
    st.switch_page("pages/activity_page.py")

st.markdown("""
💡 Don't keep your ideas to yourself —
add your favorite spots to help the next family using this app!
""")
# button to add an activity
if st.button("🚴 Add An Activity to Our List"):
    st.switch_page()


