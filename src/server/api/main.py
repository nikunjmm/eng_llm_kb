import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from api.routes import chat
from langfuse.openai import openai # (If we used openai plugin instead of raw API but for gemini we just observe globally via wrapper)
# We will use the Langfuse SDK for custom trace creation instead of the monkeypatch since we are on Gemini
from langfuse import observe

load_dotenv()

app = FastAPI(
    title="Engineering LLM KB Engine",
    description="Agentic RAG framework API for manufacturing constraints and equipment data.",
    version="1.0.0"
)

# Allow React UI to communicate with the API
origins = [
    "http://localhost:5173",  # React Dev server
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}
