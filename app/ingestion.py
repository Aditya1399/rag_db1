#all the necessary imports
from langchain_community.vectorstores import PGVector
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from pydantic import BaseModel
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

# Load the dotenv file
load_dotenv()

DB_URL = os.getenv("DB_URL")
SENTENCE_TRANSFORMERS_MODEL = os.getenv("SENTENCE_TRANSFORMERS_MODEL")

#Initialize the embeddings
embeddings = HuggingFaceEmbeddings(model_name=SENTENCE_TRANSFORMERS_MODEL)

#Initialize the vector store
vector_store = PGVector(
    connection_string=DB_URL,
    embedding_function=embeddings,
    collection_name="documents"
)

class IngestRequest(BaseModel):
    title: str
    content: str

def ingest_document(doc: IngestRequest):
    """
    The function that creates a new document and adds it to the vector store
    args: It takes document object as argument
    """
    new_doc = Document(page_content=doc.content, metadata={"title": doc.title})
    vector_store.add_documents([new_doc])
    return new_doc