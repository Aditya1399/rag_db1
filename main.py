# Necessary imports 
from fastapi import FastAPI
from routers import routes
import asyncio
import os 
import uvicorn

#Load the dotenv file


app = FastAPI()
app.include_router(routes,prefix="/api")
def run():
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )

if __name__ == "__main__":
    run()
