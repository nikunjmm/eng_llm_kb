import os
from google import genai
from google.genai import types
from typing import Dict, Any
from api.models import ChatRequest, ChatResponse, ActionRequest, ChatMessage
from agents.prompts import SYSTEM_INSTRUCTION
from tools.registry import get_tool_definitions, execute_tool
from langfuse import observe

# Initialize the client (automatically uses GEMINI_API_KEY from environment)
client = genai.Client()

@observe()
async def execute_agent_loop(request: ChatRequest) -> ChatResponse:
    """
    Executes the main reasoning loop using the Gemini SDK.
    Handles Tool calls natively.
    """
    if not os.environ.get("GEMINI_API_KEY"):
        raise ValueError("GEMINI_API_KEY environment variable is not set.")

    # Convert our Pydantic history into the format Gemini expects
    gemini_history = []
    for msg in request.messages:
        # Gemini uses 'user' and 'model' as roles
        role = "user" if msg.role == "user" else "model"
        gemini_history.append(
            types.Content(role=role, parts=[types.Part.from_text(text=msg.content)])
        )

    # Prepare the prompt
    prompt = ""
    if request.csharp_context:
        prompt += f"--- CURRENT ACTIVE APP CONTEXT ---\n{str(request.csharp_context)}\n----------------------------------\n\n"
    
    # We simply send an empty prompt if there were no new user messages but we needed to attach context
    # However, usually the last message is what triggers this
    # Let's extract the last user message to use as the immediate prompt, and remove it from history so we don't duplicate
    if len(gemini_history) > 0 and gemini_history[-1].role == "user":
        prompt += request.messages[-1].content
        # Remove the last message from the chat history we just started so it's not duplicate sent
        gemini_history.pop()
    else:
        prompt += "Please evaluate the context."

    # Start a chat session with the converted history and configurations
    chat = client.chats.create(
        model="gemini-2.5-flash",
        history=gemini_history,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            tools=get_tool_definitions(),
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
        )
    )

    # Send the prompt to Gemini
    response = chat.send_message(prompt)

    actions = []
    text_content = ""

    # The Agent Loop: Check if the model wants to call a function
    while True:
        if not response.function_calls:
            break
            
        fn_call = response.function_calls[0]
        function_name = fn_call.name
        
        # We need to construct the args dictionary safely
        args_dict = {}
        if fn_call.args:
            for key, val in fn_call.args.items():
                args_dict[key] = val
        
        # If the tool is intended for the C# Client to execute:
        if function_name.startswith("client_"):
            # Record it as an ActionRequest to send back to the React UI
            clean_name = function_name.replace("client_", "")
            actions.append(ActionRequest(
                actionName=clean_name,
                parameters=args_dict,
                reasoning="Proposed by Agent to assist user based on context.",
                requiresApproval=True
            ))
            # Tell the LLM we are deferring this execution to the client
            response = chat.send_message(
                types.Part.from_function_response(
                    name=function_name,
                    response={"status": "deferred_to_client", "message": f"Action {clean_name} proposed to user for approval."}
                )
            )
        else:
            # It's a server-side tool (e.g., Vector DB lookup)
            try:
                result = execute_tool(function_name, args_dict)
                # Send the tool result back to the model so it can continue reasoning
                response = chat.send_message(
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": result}
                    )
                )
            except Exception as e:
                response = chat.send_message(
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": str(e)}
                    )
                )

    # Once the loop exits (no more function calls), the response contains the final text
    if response.text:
         text_content = response.text
    else:
         text_content = "Action processed."

    return ChatResponse(
        text_content=text_content,
        action_requests=actions
    )
