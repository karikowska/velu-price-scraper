from langchain.tools import tool
import streamlit as st

@tool
def notify_streamlit(message: str) -> str:
    """Shows a Streamlit notification popup"""
    st.toast(message)
    return "Toast shown!"
