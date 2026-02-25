import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def get_equipment_details(equipment_id: str) -> str:
    """Finds manufacturing equipment details from the knowledge base by ID."""
    return f"Details for {equipment_id}"

def main():
    client = genai.Client() # Uses GEMINI_API_KEY from environment
    
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            tools=[get_equipment_details],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
        )
    )
    
    print("Sending message...")
    response = chat.send_message("What are PUMP-101 details?")
    
    # Check function calls
    if response.function_calls:
        print("Function calls found! (Auto-execution disabled)")
        for fc in response.function_calls:
            print("FN NAME:", fc.name)
            print("FN ARGS:", fc.args)
    else:
        print("No function calls found.")
        print("Text:", response.text)

if __name__ == "__main__":
    main()
