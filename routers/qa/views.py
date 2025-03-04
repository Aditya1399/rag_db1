# Necessary imports 
from fastapi import APIRouter, HTTPException,Depends
from fastapi.responses import StreamingResponse
from models.models import User, QARequest, QAResponse
from routers.retrieval.utils import retrieve_documents
from routers.qa.utils import generate_answer
from routers.authentication.utils import get_current_user
import asyncio

app = APIRouter()

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