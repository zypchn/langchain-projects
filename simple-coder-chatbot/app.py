### Q&A Chatbot ###

import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

## Load Anthropic model and get response

def get_openai_response(question):
    system_template = "You are a helpful coder assistant. When the user asks a question, your task is to write simple Python codes."
    user_template = "{question}"
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", user_template)
    ])
    
    chat_llm = ChatOpenAI(temperature=0.5, openai_api_key=OPENAI_API_KEY)
    
    chain = chat_prompt | chat_llm
    
    return chain.invoke(question).content
    
    
## Initialize Streamlit app

st.set_page_config(page_title="Simple Langchain App")
st.header("Coder Q&A Demo")

input = st.text_input("Input: ", key=input)
response = get_openai_response(input)

submit = st.button("Ask your question...")
if submit:
    st.subheader("The response is:")
    st.write(response)