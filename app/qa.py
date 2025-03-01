from pydantic import BaseModel
from fastapi import HTTPException
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class QARequest(BaseModel):
    question: str
    top_k: int 

class QAResponse(BaseModel):
    answer: str
    relevant_documents: list 

#Load a small,CPU friendly model 
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
llm_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

def generate_answer(question, documents):
    combined_content = "\n".join([
        doc.page_content if hasattr(doc, "page_content") else doc[1] 
        for doc in documents
    ])


    prompt = f"Answer the following question based on the context:\n\nContext: {combined_content}\n\nQuestion: {question}\nAnswer:"

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = llm_model.generate(inputs.input_ids, max_length=512)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return answer