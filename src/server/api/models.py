from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the sender: 'user', 'assistant', or 'system'")
    content: str = Field(..., description="Text content of the message")

class ActionRequest(BaseModel):
    actionName: str = Field(..., description="The exact name of the tool/C# method to invoke")
    parameters: dict = Field(default_factory=dict, description="JSON key-value pairs representing parameters for the action")
    reasoning: str = Field(..., description="The AI's reasoning for why this action is being proposed")
    requiresApproval: bool = Field(default=True, description="Whether human-in-the-loop approval is required before execution")

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the active chat session")
    messages: List[ChatMessage] = Field(..., description="Current conversation history including the new user message")
    csharp_context: Optional[dict] = Field(None, description="Context extracted from the active C# application screen")

class ChatResponse(BaseModel):
    text_content: str = Field(..., description="The conversational response from the AI")
    action_requests: List[ActionRequest] = Field(default_factory=list, description="Structured actions the AI wishes the C# application to perform")
