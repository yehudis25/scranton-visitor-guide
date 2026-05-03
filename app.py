import streamlit as st
from connecter import connecter


@st.cache_resource
def init_db():
    return connecter()


conn = init_db()


st.switch_page("pages/main_menu.py")
