#necessary imports 
from pydantic import BaseModel
from fastapi import HTTPException
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from dotenv import load_dotenv
import os 

#load the necessary environmental variables
load_dotenv()

TEXT_GENERATION_MODEL=os.getenv('TEXT_GENERATION_MODEL')

#Loading the GPU friendly model
tokenizer = AutoTokenizer.from_pretrained(TEXT_GENERATION_MODEL)
llm_model = AutoModelForSeq2SeqLM.from_pretrained(TEXT_GENERATION_MODEL)

def generate_answer(question, documents):
    """
    Function that generates the answer to the user question based on the 
    prompt and document retrieved from the vector store
    args: question, documents
    """
    combined_content = "\n".join([
        doc.page_content if hasattr(doc, "page_content") else doc[1] 
        for doc in documents
    ])


    prompt = f"Answer the following question based on the context:\n\nContext: {combined_content}\n\nQuestion: {question}\nAnswer:"

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = llm_model.generate(inputs.input_ids, max_length=512)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return answer