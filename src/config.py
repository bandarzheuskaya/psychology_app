import streamlit as st
import os



def setup_page():
    st.set_page_config(
        page_title="PsychoTest Pro",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed",
    )


def load_styles():
    base = os.path.dirname(__file__)
    css_path = os.path.join(base, "styles.css")

    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

