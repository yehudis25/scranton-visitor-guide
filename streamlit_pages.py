import streamlit as st
import pandas as pd

def mainmenu():
    st.title("🌆Welcome to Scranton, PA! ")

    st.markdown("""
    ### Bored this Chol Hamoed? We've got you covered!

    Whether you're visiting or you've lived here forever and *still* can't think of where to go —
    this guide is here to save the day.

    🚗 Discover fun trips  
    🌳 Find hidden parks  
    👨‍👩‍👧‍👦 Plan activities your whole family will love  

    👉 Use the sidebar to explore activities or click the buttons below
     """)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Find Activities Now"):
            st.switch_page("pages/activities.py")

    st.markdown("""
    💡 Don't keep your ideas to yourself —
    add your favorite spots to help the next family using this app!
    """)
    if st.button("🚴 Add An Activity to Our List"):
        st.switch_page()

mainmenu()

