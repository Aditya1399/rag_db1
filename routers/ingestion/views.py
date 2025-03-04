# Necessary imports 
from fastapi import APIRouter,BackgroundTasks, Depends
from fastapi.security import OAuth2PasswordBearer
from models.models import User
from .utils import ingest_document
from models.models import IngestRequest
from dotenv import load_dotenv
from routers.authentication.utils import get_current_user


app = APIRouter()

#Route for ingesting the documents asynchronously
@app.post("/ingest")
async def ingest(doc: IngestRequest,background_tasks: BackgroundTasks,current_user: User = Depends(get_current_user)):
    """Asynchronously ingest a document"""
    background_tasks.add_task(ingest_document, doc)
    
    ingested_doc = ingest_document(doc)

    return {"message": "Document ingestion started in the background", "document": ingested_doc}