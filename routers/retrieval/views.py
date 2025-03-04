# Necessary imports 
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from models.models import User
from routers.retrieval.utils import retrieve_documents
from routers.authentication.utils import get_current_user
from dotenv import load_dotenv
import asyncio
import os 

#Load the dotenv file
load_dotenv()

app = APIRouter()

#route to retrieve the list of documents 
@app.get("/documents",)
async def list_documents(current_user: User = Depends(get_current_user)):
    """List documents asynchronously."""
    docs = await asyncio.to_thread(retrieve_documents, "", top_k=100)
    return [{"title": doc.metadata['title'], "content": doc.page_content} for doc in docs]