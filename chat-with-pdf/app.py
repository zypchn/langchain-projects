### Chat With PDF ###

import os
from dotenv import load_dotenv
import streamlit as st
import cassio
from langchain_community.vectorstores import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from PyPDF2 import PdfReader

load_dotenv()
ASTRADB_APP_TOKEN = os.getenv("ASTRA_DB_TOKEN")
ASTRADB_ID = os.getenv("ASTRA_DB_ID")

# read the uploaded PDF file and chunk the texts
def read_file_and_chunk(pdf):
    reader = PdfReader(pdf)
    raw_text = ""
    for _, page in enumerate(reader.pages):
        content = page.extract_text()
        if content:
            raw_text += content
            
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=400,
        chunk_overlap=100,
        length_function=len
    )
    text_chunks = text_splitter.split_text(raw_text)
    return text_chunks

# initializing database connection with Cassio
def initialize_database():
    cassio.init(
        token=ASTRADB_APP_TOKEN,
        database_id=ASTRADB_ID
    )
    astra_vector_store = Cassandra(
        embedding=embed,
        table_name="pdf_chat",
        session=None,
        keyspace=None
    )
    return astra_vector_store

# loading and indexing chunks into the database
def load_to_db(texts, vector_store):
    vector_store.add_texts(texts)
    vector_index = VectorStoreIndexWrapper(vectorstore=vector_store)
    return vector_index
    

# Initialize Streamlit app

st.set_page_config(page_title="Chat With PDF")
st.header("Ask Questions About Your Documents")

OPENAI_API_KEY = st.text_input("OpenAI API Key: ", type="password")
llm = OpenAI(openai_api_key=OPENAI_API_KEY)
embed = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

uploaded_file = st.file_uploader("Upload your PDF file")
if uploaded_file is not None:
    st.write("Reading and indexing your PDF, this may take a moment...")
    try:
        chunks = read_file_and_chunk(uploaded_file)
        astra_vector_store = initialize_database()
        astra_vector_index = load_to_db(chunks, astra_vector_store)
    except Exception as e:
        st.subheader(e)
    
    user_query = st.text_input("Query: ", key=input)
    submit = st.button("Ask")
    if submit:
        answer = astra_vector_index.query(user_query, llm=llm).strip()
        st.subheader("Answer:")
        st.write(answer)
     
