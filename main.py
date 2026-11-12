import streamlit as st

st.sidebar.write("Guess the secret object to win!")
page1 = st.Page("guessing_game.py", title="My guessing game", icon="🤔")

page2 = st.Page("statistics.py", title="Statistics", icon="📈")

pg = st.navigation(pages=[page1, page2])

pg.run()
