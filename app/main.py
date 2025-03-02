# Necessary imports 
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime,timedelta
from jose import JWTError, jwt
from models import User, init_db
from sqlalchemy.orm import Session
from ingestion import IngestRequest, ingest_document
from retrieval import retrieve_documents
from dotenv import load_dotenv
from qa import generate_answer, QARequest, QAResponse
from database import get_db
import asyncio
import os 

#Load the dotenv file
load_dotenv()

#Get the environment variables
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def create_access_token(data: dict, expires_delta: timedelta):
    """
    Function that creates an access token by taking data and expiration time as arguments
    args: data: dict, expires_delta: timedelta
    """
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Function that gets the current user by taking token and database session as arguments
    args: token: str, db: Session
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

#Route to generate the access token for accesing the routes    
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

#Route for ingesting the documents asynchronously
@app.post("/ingest")
async def ingest(doc: IngestRequest,background_tasks: BackgroundTasks,current_user: User = Depends(get_current_user)):
    """Asynchronously ingest a document"""
    background_tasks.add_task(ingest_document, doc)
    
    ingested_doc = ingest_document(doc)

    return {"message": "Document ingestion started in the background", "document": ingested_doc}

#Route where user can enter the question and get the response asynchronusly
@app.post("/qa", response_model=QAResponse)
async def qa(request: QARequest,current_user: User = Depends(get_current_user)):
    """Handle Q&A queries asynchronously with streaming responses."""
    docs = await asyncio.to_thread(retrieve_documents, request.question, request.top_k)

    if not docs:
        raise HTTPException(status_code=404, detail="No relevant documents found")

    def stream_answer():
        answer = generate_answer(request.question, docs)
        yield answer

    return StreamingResponse(stream_answer(), media_type="text/plain")

#route to retrieve the list of documents 
@app.get("/documents",)
async def list_documents(current_user: User = Depends(get_current_user)):
    """List documents asynchronously."""
    docs = await asyncio.to_thread(retrieve_documents, "", top_k=100)
    return [{"title": doc.metadata['title'], "content": doc.page_content} for doc in docs]