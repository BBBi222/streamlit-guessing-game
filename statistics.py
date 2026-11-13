"""This file displays the results from the games I already played."""

import pandas as pd  # I use pandas to make tables and chart data.
import streamlit as st


st.title("Game statistics")
st.caption("These results are saved for this Streamlit session.")

# The Play page saves one entry per finished game in game_results.
# With .get() I also avoid an error if Stats is opened before Play.
games = st.session_state.get("game_results", [])

# There is nothing to calculate before the first game is finished.
# st.stop() stops this page, but it does not shut down the app.
if not games:
    st.info("No finished games yet. Play a round first.")
    st.stop()


# -------------------- Main statistics --------------------
# I count the games and wins and then calculate two averages.
# Since I already checked that games is not empty, I can divide by its length.
number_of_games = len(games)
number_of_wins = sum(game["won"] for game in games)
average_guesses = sum(game["guesses"] for game in games) / number_of_games
average_comparisons = sum(game["comparisons"] for game in games) / number_of_games

# Four columns make the most important numbers easy to compare.
col1, col2, col3, col4 = st.columns(4)
col1.metric("Games", number_of_games)
col2.metric("Wins", number_of_wins)
col3.metric("Avg. guesses", f"{average_guesses:.1f}")
col4.metric("Avg. comparisons", f"{average_comparisons:.1f}")


# -------------------- Short game history --------------------
# OLD: st.dataframe(df, hide_index=True)
# That showed guess_history as long lists of dictionaries in the table.
# NOW: I create a second list with only the values people want to read.
results = []
for i, game in enumerate(games, start=1):
    # Old games may not have an 'outcome' value, so I add a fallback.
    outcome = game.get("outcome", "won" if game["won"] else "quit")
    result_text = {
        "won": "Won",
        "quit": "Quit",
        "abandoned": "Unfinished",
    }.get(outcome, outcome)

    # I save one row for each game, with no nested lists or dictionaries.
    results.append({
        "Game": f"Game {i}",
        "Result": result_text,
        "Guesses": game["guesses"],
        "Comparisons": game["comparisons"],
    })

summary = pd.DataFrame(results)

st.subheader("Game history")
# I use Game as the row label, not a separate numbered index column.
st.table(summary.set_index("Game"))


# -------------------- Guesses per game --------------------
st.subheader("Guesses per game")
# This is required for the assignment and uses the same summary table.
st.bar_chart(summary, x="Game", y="Guesses", sort=False)


# -------------------- Guess quality --------------------
st.subheader("How close were the guesses?")
st.caption(
    "0 = unrelated, 1 = distant, 2 = somewhat related, 3 = related, "
    "4 = very close, 5 = correct. The AI estimates these scores."
)

# Each game has a guess_history list, so I collect all guesses into one table.
# I also number each guess to show which game it came from.
rows = []
for game_number, game in enumerate(games, start=1):
    for guess_number, guess in enumerate(game.get("guess_history", []), start=1):
        rows.append({
            "Guess": f"Game {game_number}, guess {guess_number}",
            "Object": guess["word"],
            "Score": guess["score"],
            "Quality": guess["quality"],
        })

if not rows:
    st.info("There are no guesses to rate yet.")
else:
    quality = pd.DataFrame(rows)

    # If an AI call failed, a score can be None.
    # I remove these entries only from the score chart, not from the history.
    rated = quality.dropna(subset=["Score"])

    if not rated.empty:
        st.bar_chart(rated, x="Guess", y="Score", sort=False)

        # The average for wrong guesses should not include correct answers.
        wrong = rated[rated["Score"] < 5]
        if not wrong.empty:
            st.metric("Average score of wrong guesses", f"{wrong['Score'].mean():.1f} / 4")

    # I hide the full guess list inside an expander to keep the page shorter.
    with st.expander("See individual guesses"):
        st.dataframe(quality, hide_index=True, use_container_width=True)

# session_state keeps the results only while this browser session is active.
st.caption("Results are not stored permanently.")
