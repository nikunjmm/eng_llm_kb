import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from api.models import ChatRequest, ChatMessage
from agents.core_agent import execute_agent_loop

async def test_live_agent():
    print("Testing live Gemini agent loop with dummy tools...")
    
    # 1. Provide a message that should trigger the get_equipment_details server-side tool
    # 2. Provide a context that the agent should read.
    # 3. The agent should propose a client-side action (client_set_operating_pressure)
    
    request = ChatRequest(
        session_id="test-session-123",
        messages=[
            ChatMessage(role="user", content="I am looking at PUMP-101. What is its max pressure? Increase its active pressure setting to 120 please.")
        ],
        csharp_context={"current_screen": "Equipment Selection", "selected_item": "PUMP-101", "user_role": "admin"}
    )
    
    response = await execute_agent_loop(request)
    
    print("\n--- AGENT RESPONSE ---")
    print("Response Text:\n", response.text_content)
    print("\nAction Requests:")
    for req in response.action_requests:
        print(f" - Tool: {req.actionName}, Params: {req.parameters}, Reasoning: {req.reasoning}")
    print("----------------------")
    
    assert "150" in response.text_content or len(response.action_requests) > 0, "Agent failed to retrieve details or propose action"
    print("\n✅ Live test passed!")

if __name__ == "__main__":
    asyncio.run(test_live_agent())
