from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from query import query_model
from create_db import generate_data_store
import uvicorn

#generate_data_store()
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Question(BaseModel):
    text: str

@app.get("/")
async def hello():
    return {"response": "Hello World!"}


@app.post("/ask")
async def ask(question: Question):
    return {"answer": query_model(question.text)}
    

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    

