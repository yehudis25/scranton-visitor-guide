import streamlit as st
import pandas as pd
from connecter import connecter


@st.cache_resource
def init_db():
    return connecter()

conn = init_db()

st.switch_page("pages/main_menu.py")
import streamlit as st

