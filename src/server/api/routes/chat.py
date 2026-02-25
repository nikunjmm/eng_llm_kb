from typing import List, AsyncGenerator
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from api.models import ChatRequest, ChatResponse, ActionRequest
from agents.core_agent import execute_agent_loop

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Standard synchronous chat endpoint.
    Processes the conversation history and context, then returns a final response with any actions.
    """
    try:
        # Pass the request to the agent reasoning loop
        response = await execute_agent_loop(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Placeholder for SSE streaming implementation (to be added later)
@router.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    async def generate_responses() -> AsyncGenerator[str, None]:
        yield f"data: {json.dumps({'text_content': 'Streaming not yet implemented.'})}\n\n"
    
    return StreamingResponse(generate_responses(), media_type="text/event-stream")
