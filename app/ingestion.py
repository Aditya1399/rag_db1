from langchain_community.vectorstores import PGVector
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
# Initialize the vector store with Hugging Face embeddings
load_dotenv()
DB_URL = os.getenv("DB_URL")
print(DB_URL)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#engine = create_engine(DB_URL)
vector_store = PGVector(
    connection_string=DB_URL,
    embedding_function=embeddings,
    collection_name="documents"
)

class IngestRequest(BaseModel):
    title: str
    content: str

def ingest_document(doc: IngestRequest):
    new_doc = Document(page_content=doc.content, metadata={"title": doc.title})
    vector_store.add_documents([new_doc])
    return new_doc