### Chat With PDF ###

import os
from dotenv import load_dotenv
import streamlit as st
from langchain_community.vectorstores import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

# Initialize Streamlit app

st.set_page_config(page_title="Chat With PDF")
st.header("Ask Questions About Your Documents")

OPENAI_API_KEY = st.text_input("OpenAI API Key: ", key=input)

uploaded_file = st.file_uploader("Upload your file")
if uploaded_file is not None:
    st.subheader("file uploaded successfully")
