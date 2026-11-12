# Object guessing game using streamlit

import streamlit as st # helps to create the web app
import random # helps to choose random oject from a list
from openai import OpenAI, AuthenticationError, OpenAIError #helps to use the OpenAI API

st.set_page_config(page_title="My guessing game")

with st.sidebar:
    api_key = st.text_input(
        "UOS AI API-Key",
        type="password",
        key= "uos_api_key",
        placeholder="...",
    ).strip()

# pass the entered key
client = OpenAI(
    base_url="https://litellm.uni-osnabrueck.de/v1",
    api_key= api_key
)

#st.logo("logo2.png") 
#st.sidebar.image("logo2.png", width=200)
st.image("logo2.png", width=250)

WORDS = ["piano", "guitar", "bicycle", "camera", "umbrella"] 
#or change it and generate it with AI

if "secret_word" not in st.session_state: 
    st.session_state.secret_word = random.choice(WORDS) 
# checks if a secret word is already stored in session state, 
# otherwise it selects a random word from the list and stores it in session state
if st.button("Start Game"):
    st.session_state.secret_word = random.choice(WORDS) 
    st.info("A secret object has been selected!")

st.title("Object Guesser")
st.header("Hello Player!")
st.subheader("Let's play an object guessing game!")
st.write("I have an object in mind and you have to guess it. For example: A piano. You have to ask me questions to narrow down the possibilities. Your questions should look like this: Is it more like a guitar or more like a fridge. I would answer: More like a fridge.")

# shows the secret word for debugging purposes
st.write("DEBUG:", st.session_state.secret_word) 

st.subheader("Compare two objects")

object_a = st.text_input("Is it more like a... ")
object_b = st.text_input("or more like a... ")

# Create the prompt for the AI model to compare the two objects with the secret object
prompt = f"""
The secret object is: {st.session_state.secret_word}

Object A: {object_a}
Object B: {object_b}

Which object is more similar to the secret object?

Answer with ONLY: "It is more like a {object_a} or {object_b}.".
Do not explain your answer.
"""


if st.button("Compare", disabled=not prompt.strip()): 
    #button to get the AI comparison of the two objects
    try:
        with st.spinner("Answer is being created …"):
            response = client.chat.completions.create(
                model="google/gemma-4-E4B-it",
                messages=[
                    {"role": "user", "content": prompt},
                ],
            )

        st.write(response.choices[0].message.content)

    except AuthenticationError:
        st.error("API was not accept. Please check it.")

    except OpenAIError:
        st.error(
            "AI API request failed. Please check it and try again. "
        )



#creates an input box for the user to enter their guess
guess = st.text_input("What is your guess?")

# checks if the guess is correct by comparing it to the secret word stored in session state
# make everything lowercase and strip whitespace for comparison
if st.button("Guess"):
    if not guess.strip():
        st.warning("Please enter a guess!")
    elif guess.strip().casefold() == st.session_state.secret_word.casefold():
        st.success("Congratulations! You guessed the correct object!")
        st.balloons() # balloons fly over the screen
    else: 
        st.error("Wrong guess! Try again.")
        # add this: make the AI make fun of the mistake and give penalty points      


if st.button("Quit Game"):
    st.error("You quit the game.")

#rating = st.slider("Choose number of rounds:", 0, 10)
#if rating:
#    st.subheader("Number of rounds")
#    st.write(f"Number of rounds is {rating}")


#guess = st.number_input(label='Guess a number', min_value=1, max_value=100)

#if guess == 42:
#    st.success("Yeah! You did it")


#TO DO: statistics, github, make it look appealing, add tipps, 
# The LLM could estimate the semantic similarity between each guessed object and the secret
#  word using a fixed rating scale
# different games for different rounds: guess the size difference?
# give hints for penalty point
# figure gets steps forward with points
