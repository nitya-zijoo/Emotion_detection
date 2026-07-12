from fastapi import FastAPI
from pydantic import BaseModel
from backend.main import main
from backend.routes.auth_routes import router as auth_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth")

class ChatRequest(BaseModel):
    user_id: str
    message: str
    chat_history: list = []

@app.post("/chat")
def chat(request: ChatRequest):
    result = main(request.user_id, request.message, request.chat_history)
    return result