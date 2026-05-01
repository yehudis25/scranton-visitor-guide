# program to change the color of the app and remove the sidebars

import streamlit as st
def display():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f5f7fb;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def remove_sidebars():
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )