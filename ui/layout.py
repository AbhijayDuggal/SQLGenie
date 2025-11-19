import streamlit as st

def show_header(title: str):
    st.set_page_config(page_title=title, layout="wide")
    st.title(title)
