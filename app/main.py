from fastapi import FastAPI, HTTPException
from app.ingestion import IngestRequest, ingest_document
from app.retrieval import retrieve_documents
from app.qa import generate_answer, QARequest, QAResponse

app = FastAPI()

@app.post("/ingest")
def ingest(doc: IngestRequest):
    ingested_doc = ingest_document(doc)
    return {"message": "Document ingested successfully", "title": ingested_doc.metadata['title']}


@app.post("/qa", response_model=QAResponse)
def qa(request: QARequest):
    docs = retrieve_documents(request.question, request.top_k)

    if not docs:
        raise HTTPException(status_code=404, detail="No relevant documents found")

    answer = generate_answer(request.question, [(doc.metadata['title'], doc.page_content) for doc in docs])
    relevant_docs = [{"title": doc.metadata['title'], "content": doc.page_content} for doc in docs]

    return QAResponse(answer=answer, relevant_documents=relevant_docs)


@app.get("/documents")
def list_documents():
    docs = retrieve_documents("", top_k=100)
    return [{"title": doc.metadata['title'], "content": doc.page_content} for doc in docs]