from langchain.llms import GooglePalm
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

from langchain.chains import LLMChain
from langchain.chains import SequentialChain




os.environ["GOOGLE_API_KEY"] = "AIzaSyD29fEos3V6S2L-AGSQgNu03GqZEIgJads"


llm = GooglePalm(temperature = 0.9)



def generate_game_name_and_functions(type):

    prompt_template_name = PromptTemplate(
       input_variables = ['type'],
       template = "I want to buid a new never build before {type} game, Suggest only one fancy and creative name"
    )
    name_chain = LLMChain(llm=llm, prompt = prompt_template_name, output_key = "game_name")
    
    prompt_template_items = PromptTemplate(
        input_variables = ['game_name'],
        template = "Write a short creative user manual for {game_name} game. Tell shortly in bullet points"
    )

    function_chain = LLMChain(llm=llm, prompt = prompt_template_items, output_key = 'functions')

    chain= SequentialChain(chains= [name_chain, function_chain], 
                       input_variables = ["type"], 
                       output_variables = ["game_name","functions"])

    response = chain({'type':type})

    return response


if __name__ == "__main__":
    print(generate_game_name_and_functions("action"))


