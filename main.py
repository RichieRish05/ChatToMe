from fastapi import FastAPI
from pydantic import BaseModel
from query import query_model

app = FastAPI()

class Question(BaseModel):
    text: str


@app.post("/ask")
async def ask(question: Question):
    return {"answer": query_model(question.text)}
    

