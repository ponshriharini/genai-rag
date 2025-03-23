from langchain.chat_models import AzureChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores.azuresearch import AzureSearch
from langchain_community.embeddings import AzureOpenAIEmbeddings
import os
from dotenv import load_dotenv
import streamlit as st


load_dotenv()

embedding_model = AzureOpenAIEmbeddings(
    deployment=os.getenv("AZURE_EMBEDDING_DEPLOYMENT"),
    chunk_size=512
)

# Embedding function - to embed the query
# Used to communicate with the Azure Search service
retriever = AzureSearch(
    azure_search_endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    azure_search_key=os.getenv("AZURE_SEARCH_KEY"),
    index_name=os.getenv("AZURE_SEARCH_INDEX"),
    embedding_function=embedding_model.embed_query
).as_retriever()

# temperature=0 means deterministic answers (no randomness)
llm = AzureChatOpenAI(
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("OPENAI_API_VERSION"),
    temperature=0.3
)

# Retriever to get relevant text chunks
# LLM to generate answers
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

def get_validated_answer(question):
    raw_output = qa_chain.run(question)

    return raw_output