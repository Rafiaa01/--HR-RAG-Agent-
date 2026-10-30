from fastapi import FastAPI
from src.chat.chat_request import chat
from src.config import ChatRequest, ChatResponse

application = FastAPI(
    title="HR RAG Agent API",
    description="An AI-powered HR assistant using LangChain tools and RAG",
    version="1.0.0",
)


@application.get("/")
def home():
    return {"message": "API Running"}


@application.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    return chat(request)
