import os
import uuid
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import AzureOpenAIEmbeddings
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

def index_chunks_to_azure_search(doc_id, text):
    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50) # 500-character chunks, preserve context between chunks
    chunks = splitter.split_text(text)

    # Generate embeddings
    embeddings = AzureOpenAIEmbeddings(
        deployment=os.getenv("AZURE_EMBEDDING_DEPLOYMENT"),
        chunk_size=512
        )
    vectors = embeddings.embed_documents(chunks)

    # Connect to Azure Search
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    key = os.getenv("AZURE_SEARCH_KEY")
    index_name = os.getenv("AZURE_SEARCH_INDEX")
    client = SearchClient(endpoint=endpoint, index_name=index_name, credential=AzureKeyCredential(key))

    # Upload documents
    docs = []
    for i, chunk in enumerate(chunks):
        docs.append({
            "id": f"{doc_id}_{i}",
            "content": chunk,
            "content_vector": vectors[i]
        })

    client.upload_documents(documents=docs)