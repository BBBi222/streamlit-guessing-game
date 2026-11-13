"""This is the starting file for my Streamlit app."""

import streamlit as st

# I set the page settings here because this file starts the whole app.
# I do not need to set them again in guessing_game.py or statistics.py.
st.set_page_config(page_title="Guess the Object", layout="wide")

# st.Page tells Streamlit which Python file belongs to which page.
# Both pages use the same session_state, so Stats can read past results.
play_page = st.Page("guessing_game.py", title="Play", default=True)
stats_page = st.Page("statistics.py", title="Stats")

# I keep the navigation in the sidebar.
st.sidebar.caption("One object. Many possibilities.")
st.navigation([play_page, stats_page]).run()
