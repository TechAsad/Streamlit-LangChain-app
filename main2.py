from langchain.llms import GooglePalm
import os
from langchain.prompts import PromptTemplate

from langchain.chains import LLMChain
from langchain.chains import SequentialChain

import streamlit as st

# Set page title and favicon
st.set_page_config(page_title="Game Idea Generator", page_icon="🎮")

# Custom CSS for styling
st.markdown("""
<style>
    body {
        background-color: #17A2B8;
        font-family: 'Helvetica', sans-serif;
    }
    .container {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        padding: 1rem;
        background-color: #17A2B8;
        border-radius: 10px;
        box-shadow: 0px 5px 10px rgba(0, 0.5, 0, 0.1);
    }
    .content {
        flex: 1;
    }
    .header {
        font-size: 2.5rem;
        color: #333333;
        margin-bottom: 1rem;
    }
    .subheader {
        font-size: 1.5rem;
        color: #ffffff;
        margin-bottom: 1rem;
    }
    .function {
        font-size: 1.1rem;
        color: #ffffff;
        margin-top: 0.5rem;
        margin-bottom: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# Main app layout
st.title("🎮 Game Idea Generator 🎮")
st.markdown('<div class="container">', unsafe_allow_html=True)

# Input section on the left side
st.markdown('<div class="content">', unsafe_allow_html=True)
type = st.text_input("🎮 Enter a Game Type: For Example: Action, Arcade, Adventure, Battle Ground, etc.", "")
st.markdown('</div>', unsafe_allow_html=True)



os.environ["GOOGLE_API_KEY"] = "AIzaSyD29fEos3V6S2L-AGSQgNu03GqZEIgJads"


llm = GooglePalm(temperature = 0.9)



def generate_game_name_and_functions(type):

    prompt_template_name = PromptTemplate(
       input_variables = ['type'],
       template = "I want to build a new never build before {type} game, Suggest only one fancy and creative name"
    )
    name_chain = LLMChain(llm=llm, prompt = prompt_template_name, output_key = "game_name")
    
    prompt_template_items = PromptTemplate(
        input_variables = ['game_name'],
        template = "Write a short creative user manual and system requirements for {game_name} game. Tell shortly in bullet points"
    )

    function_chain = LLMChain(llm=llm, prompt = prompt_template_items, output_key = 'functions')

    chain= SequentialChain(chains= [name_chain, function_chain], 
                       input_variables = ["type"], 
                       output_variables = ["game_name","functions"])

    response = chain({'type':type})

    return response


if type:
    response = generate_game_name_and_functions(type)
    st.markdown(f'<h2 class="header">{type}</h2>', unsafe_allow_html=True)
    st.markdown(f'<h3 class="subheader">{response["game_name"].strip()}</h3>', unsafe_allow_html=True)
    functions = response['functions'].strip().split(". ")

    st.markdown("💡 *About The Game*")
    for item in functions:
        st.markdown(f'<p class="function">🎮 {item}</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
