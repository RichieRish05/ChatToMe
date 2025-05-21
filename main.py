from fastapi import FastAPI
from pydantic import BaseModel
from query import query_model
from create_db import generate_data_store

generate_data_store()
app = FastAPI()

class Question(BaseModel):
    text: str

@app.get("/")
async def hello():
    return {"response": "Hello World!"}


@app.post("/ask")
async def ask(question: Question):
    return {"answer": query_model(question.text)}
    

