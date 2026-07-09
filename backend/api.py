from fastapi import FastAPI
from pydantic import BaseModel
from main import main

app = FastAPI()

class ChatRequest(BaseModel):
    user_id: str
    message: str
    chat_history: list = []

@app.post("/chat")
def chat(request: ChatRequest):
    result = main(request.user_id, request.message, request.chat_history)
    return result