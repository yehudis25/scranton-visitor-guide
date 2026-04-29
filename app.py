import streamlit as st
import pandas as pd
from connecter import connecter

@st.cache_resource
def init_db():
    return connecter()

conn = init_db()
if st.button("go"):
    st.switch_page("pages/activity_page.py")