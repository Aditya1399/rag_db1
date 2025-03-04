#necessary imports 
from langchain_community.vectorstores import PGVector
from langchain.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

#Initialize the secret variable
DB_URL = os.getenv("DB_URL")

# Reuse the vector store with Hugging Face embeddings
vector_store = PGVector(
    connection_string=DB_URL,
    embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
    collection_name="documents"
)

def retrieve_documents(query, top_k=5):
    """
    Function to retrieve the top k documents based on the query
    args: query, top_k
    """
    results = vector_store.similarity_search(query, k=top_k)
    return results